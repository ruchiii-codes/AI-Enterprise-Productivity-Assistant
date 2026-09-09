import hashlib
import secrets
from datetime import timedelta

from sqlalchemy.orm import Session

from server.auth.security import (
    hash_password,
    verify_password,
)
from server.db.models import User
from server.schemas.auth import UserRegister
from server.services.providers.email_service import (
    send_password_reset_email,
    send_verification_email,
)
from server.utils.time_utils import utcnow

# A reset token grants account takeover, so it gets a short life -- unlike the
# 24-hour verification token.
RESET_TOKEN_TTL = timedelta(hours=1)


def register_user(
    db: Session,
    user: UserRegister,
):

    # Check if email already exists
    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:
        return "email_exists"

    # Check if username already exists
    existing_username = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_username:
        return "username_exists"

    verification_token = secrets.token_urlsafe(32)
    verification_token_expires = utcnow() + timedelta(hours=24)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_verified=False,
        verification_token=verification_token,
        verification_token_expires=verification_token_expires,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(
        recipient_email=new_user.email,
        verification_token=verification_token,
    )

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def hash_reset_token(token: str) -> str:
    """Hash a reset token for storage.

    SHA-256 rather than bcrypt: the lookup needs to be deterministic so the
    presented token can be found, and the token is already 32 bytes of
    cryptographic randomness, so it needs no salt or key stretching. Storing
    the hash means a database read alone cannot be used to reset a password.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def request_password_reset(db: Session, email: str) -> None:
    """Issue a reset token and email it.

    Returns None whether or not the address belongs to an account. The caller
    must respond identically in both cases, otherwise this endpoint reveals
    which email addresses are registered.
    """
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return

    token = secrets.token_urlsafe(32)

    user.reset_token = hash_reset_token(token)
    user.reset_token_expires = utcnow() + RESET_TOKEN_TTL

    db.commit()

    # The plaintext token exists only here and in the email.
    send_password_reset_email(
        recipient_email=user.email,
        reset_token=token,
    )


def reset_password(db: Session, token: str, new_password: str) -> bool:
    """Consume a reset token and set a new password.

    Returns False when the token is unknown or expired.
    """
    user = (
        db.query(User)
        .filter(User.reset_token == hash_reset_token(token))
        .first()
    )

    if not user:
        return False

    if user.reset_token_expires is None:
        return False

    if utcnow() > user.reset_token_expires:
        return False

    user.hashed_password = hash_password(new_password)

    # Single use.
    user.reset_token = None
    user.reset_token_expires = None

    # Someone who can prove control of the inbox has verified it.
    user.is_verified = True

    db.commit()

    return True
