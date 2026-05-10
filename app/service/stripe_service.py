import stripe
from datetime import datetime
from fastapi import Request, HTTPException, Depends
from app.db.deps import get_db
from app.db.models import User
from app.service.email_service import send_email

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
  
  # Hndale events
  if event["type"] == "checkout.session.completed":
    session = event["data"]["object"]

    user_id = int(session["metadata"]["user_id"])
    customer_id = session["customer"]
    subscription_id = session["subscription"]

    upgrade_user_to_pro(db, user_id, customer_id, subscription_id)

  elif event["type"] == "invoice.payment_failed":
    customer_id = session["customer"]

    user = db.query(User).filter(User.id == user_id).first()
    if user:
      user.paymet_failed_at = datetime.utcnow()
      db.commit()

      # Send email
      send_email(
        user.email,
        "Payment failed",
        """
        <h1>Payment Failed</h1>
        <p>Your payment failed. We will retry automatically.</p>
        <p>Your Pro plan remains active temporarily.</p>
        """
      )


  elif event["type"] == "customer.subscription.canceled":
    customer_id = session["customer"]
    user = db.query(User).filter(User.id == user_id).first()
    if user:
      user.plan = "free"
      user.stripe_subscription_id = None
      db.commit()
    
  return True

def upgrade_user_to_pro(db, user_id, customer_id, subscription_id):
  user = db.query(User).filter(User.id == user_id).first()

  user.plan = "pro"
  user.stripe_customer_id = customer_id
  user.stripe_subscription_id = subscription_id

  db.commit()



def create_billing_portal(customer_id: str):
  session = stripe.billing_portal.Session.create(
    customer=customer_id,
    return_url=FRONTEND_URL
  )

  return session.url