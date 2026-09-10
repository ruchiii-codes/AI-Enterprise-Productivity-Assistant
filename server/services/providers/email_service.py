import logging
import smtplib
from email.message import EmailMessage

from server.config import settings

logger = logging.getLogger(__name__)


def _send(message: EmailMessage) -> bool:
    """Deliver a message, returning whether it was sent.

    Failures are logged and swallowed rather than raised. That matters most
    for password reset: /auth/forgot-password deliberately answers the same
    way whether or not an address is registered, and letting an SMTP error
    escape would break that. Only registered addresses reach this function, so
    a raised exception would turn into a 500 for exactly those addresses --
    handing an attacker the account-enumeration oracle the endpoint exists to
    deny during any mail outage.

    The timeout matters for the same reason smtplib's default of "none" is
    dangerous here: a hung SMTP host would otherwise block the worker
    indefinitely.
    """
    if not settings.email_configured:
        logger.error(
            "Cannot send %r: EMAIL_HOST, EMAIL_USERNAME and EMAIL_PASSWORD "
            "are not all configured.",
            message["Subject"],
        )
        return False

    try:
        with smtplib.SMTP(
            settings.EMAIL_HOST,
            settings.EMAIL_PORT,
            timeout=settings.EMAIL_TIMEOUT,
        ) as server:
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(message)

        logger.info("Sent %r", message["Subject"])
        return True

    except Exception:
        # The recipient is deliberately not logged: these messages go to
        # password-reset and verification addresses.
        logger.exception("Failed to send %r", message["Subject"])
        return False


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

    return _send(message)


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

    return _send(message)
