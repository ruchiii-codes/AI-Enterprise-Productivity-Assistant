import smtplib
from email.message import EmailMessage

from server.config import settings


def _send(message: EmailMessage):
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(message)


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

    _send(message)


def send_password_reset_email(
    recipient_email: str,
    reset_token: str,
):
    reset_link = (
        f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    )

    message = EmailMessage()

    message["Subject"] = "Reset your WorkMind password"
    message["From"] = settings.EMAIL_USERNAME
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

We received a request to reset your WorkMind password.

Choose a new password using the link below:

{reset_link}

This link will expire in 1 hour and can only be used once.

If you did not request a password reset, you can safely ignore this email.
Your password will not change until you use the link above.

Best,
WorkMind
"""
    )

    _send(message)
