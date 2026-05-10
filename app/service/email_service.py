import resend
from app.core.config import FROM_EMAIL, RESEND_API_KEY

resend.api_key = RESEND_API_KEY

def send_email(to_email, subject, html):
  resend.Email.send({
    "from": FROM_EMAIL,
    "to": to_email,
    "subject": subject,
    "html": html
  })