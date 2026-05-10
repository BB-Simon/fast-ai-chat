from datetime import datetime, timedelta
from app.db.models import User
from app.service.email_service import send_email

GRACE_PERIOD = 7

def process_failed_payment(db):
  users = db.query(User).filter(
    User.payment_failed_At != None,
    User.plan == "pro",
  ).all()

  for user in users:
    expired = (
      datetime.utcnow() - user.payment_failed_at
    ) > timedelta(GRACE_PERIOD)

    if expired:
      user.plan = "free"
      user.stripe_subscription_id = None

      db.commit()

      # Notify user
      send_email(
        user.email,
        "Subscription downgrade",
        """
        <h1>Subscription Expired</h1>
        <p>Your Pro subscription has been downgraded to Free.</p>
        """
      )