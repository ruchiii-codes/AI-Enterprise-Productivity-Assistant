import smtplib
from email.message import EmailMessage

from server.config import settings


def send_verification_email(
    recipient_email: str,
    verification_token: str,
):
    verification_link = (
        f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
    )

    message = EmailMessage()

    message["Subject"] = "Verify your WorkMind email"
    message["From"] = settings.EMAIL_USERNAME
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

Welcome to WorkMind!

Please verify your email address by clicking the link below:

{verification_link}

This verification link will expire in 24 hours.

If you did not create a WorkMind account, you can safely ignore this email.

Best,
WorkMind
"""
    )

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(message)
