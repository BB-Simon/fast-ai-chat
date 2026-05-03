from fastapi import APIRouter, Depends, Request
from app.db.deps import get_current_user
from app.service.stripe_service import create_checkout_session, handle_stripe_events, create_billing_portal 


router = APIRouter()


# Note: Frontend redirects user to Stripe checkout
@router.post("/create-checkout")
def create_checkout(user = Depends(get_current_user)):
  url = create_checkout_session(user["user_id"], user.get("email", "test@gmail.com"))
  return { "checkout_url": url}

@router.post("/stripe-webhook")
def stripe_webhook(req: Request):
  success = handle_stripe_events(req=req)

  if success:
    return {"status": "ok"}
  

@router.get("/billing-portal")
def billing_portal(user = Depends(get_current_user)):
  url = create_billing_portal(customer_id=user.stripe_customer_id)
  return {
    "url": url
  }