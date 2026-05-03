import stripe
from fastapi import Request, HTTPException, Depends
from app.db.deps import get_db
from app.db.models import User

from app.core.config import STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_ID, STRIPE_SECRET_KEY, FRONTEND_URL


stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(user_id: int, email: str):
  session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="subscription",
    customer_email=email,
    line_items=[{
      "price": STRIPE_PRICE_ID,
      "quantity": 1
    }],
    success_url=f"{FRONTEND_URL}/success",
    cancel_url=f"{FRONTEND_URL}/cencel",
    metadata={
      "user_id": user_id
    }
  )

  return session.url


async def handle_stripe_events(req: Request, db = Depends(get_db)):
  payload = await req.body()
  sig_header = req.headers.get("stripe-signature")

  try:
    event = stripe.Webhook.construct_event(
      payload,
      sig_header,
      STRIPE_WEBHOOK_SECRET,
    )
  except:
    raise HTTPException(status_code=400, detail="Invalid webhook")
  
  # Hnale events
  if event["type"] == "checkout.session.completed":
    session = event["data"]["object"]

    user_id = int(session["metadata"]["user_id"])
    customer_id = session["customer"]

    upgrade_user_to_pro(db, user_id, customer_id)

  return True

def upgrade_user_to_pro(db, user_id, customer_id):
  user = db.query(User).filter(User.id == user_id).first()
  user.stripe_customer_id = customer_id
  db.commit()



def create_billing_portal(customer_id: str):
  session = stripe.billing_portal.Session.create(
    customer=customer_id,
    return_url=FRONTEND_URL
  )

  return session.url