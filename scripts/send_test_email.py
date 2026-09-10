"""Send a real password-reset email to prove SMTP works.

This exercises the same code path the application uses, so it verifies the
credentials, the TLS handshake, the timeout and deliverability -- none of
which the test suite covers, because every test stubs the send.

The token is fake and no database row is touched, so the link in the email
will correctly fail with "invalid or expired". That is the expected result:
this checks delivery, not the reset flow. Follow it with a real reset from
the running application.

Usage:
    python -m scripts.send_test_email you@example.com
"""

import sys

from server.config import settings
from server.services.providers.email_service import send_password_reset_email


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    recipient = sys.argv[1]

    print(f"Host      : {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    print(f"From      : {settings.EMAIL_USERNAME}")
    print(f"To        : {recipient}")
    print(f"Link base : {settings.FRONTEND_URL}")
    print(f"Timeout   : {settings.EMAIL_TIMEOUT}s")

    if not settings.email_configured:
        print(
            "\nEMAIL_HOST, EMAIL_USERNAME and EMAIL_PASSWORD are not all set. "
            "Fill them in .env first."
        )
        return 1

    print("\nSending...")

    delivered = send_password_reset_email(
        recipient_email=recipient,
        reset_token="test-token-not-valid-for-reset",
    )

    if delivered:
        print(
            "\nAccepted by the SMTP server. Check the inbox -- and the spam "
            "folder, which is where a first message from a new sender often "
            "lands.\n"
            "The link in it is expected to report an invalid token."
        )
        return 0

    print(
        "\nNot sent. The reason was logged above.\n"
        "For Gmail, the usual causes are using the account password instead "
        "of a 16-character App Password, or 2-Step Verification being off."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
