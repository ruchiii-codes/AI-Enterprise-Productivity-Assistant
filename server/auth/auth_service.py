from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta
from server.auth.models import User
from server.auth.schemas import UserRegister
from server.auth.security import (
    hash_password,
    verify_password,
)
from server.services.email_service import send_verification_email

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
    verification_token_expires = datetime.utcnow() + timedelta(hours=24)

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