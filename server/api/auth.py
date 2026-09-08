from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.auth.dependencies import get_current_user
from server.auth.security import create_access_token
from server.auth.service import (
    authenticate_user,
    register_user,
    request_password_reset,
    reset_password,
)
from server.db.base import get_db
from server.db.models import User
from server.schemas.auth import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserRegister,
    UserResponse,
)
from server.utils.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Responded with whether or not the address is registered, so that this
# endpoint cannot be used to discover which emails have accounts.
PASSWORD_RESET_ACCEPTED = {
    "message": (
        "If that email address has an account, a password reset link is on "
        "its way."
    )
}


@router.post(
    "/register",
    response_model=UserResponse,
)
@limiter.limit("5/minute")
def register(
    request: Request,
    user: UserRegister,
    db: Session = Depends(get_db),
):

    new_user = register_user(db, user)

    if new_user == "email_exists":
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

    if new_user == "username_exists":
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    return new_user

@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.verification_token == token)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token.",
        )

    if user.verification_token_expires is None:
        raise HTTPException(
            status_code=400,
            detail="Verification token is invalid.",
        )

    if datetime.utcnow() > user.verification_token_expires:
        raise HTTPException(
            status_code=400,
            detail="Verification token has expired.",
        )

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None

    db.commit()

    return {
        "message": "Email verified successfully. You can now sign in."
    }

@router.post("/login")
@limiter.limit("10/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    authenticated_user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    if not authenticated_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before signing in.",
        )

    access_token = create_access_token(
        {
            "sub": authenticated_user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@router.post("/forgot-password")
@limiter.limit("5/minute")
def forgot_password(
    request: Request,
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """Email a password reset link.

    Always returns the same response. Telling the caller whether the address
    exists would turn this into an account-enumeration tool, and the rate
    limit keeps it from being used to send bulk mail to arbitrary addresses.
    """
    request_password_reset(db, payload.email)

    return PASSWORD_RESET_ACCEPTED


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password_endpoint(
    request: Request,
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    succeeded = reset_password(
        db,
        payload.token,
        payload.new_password,
    )

    if not succeeded:
        raise HTTPException(
            status_code=400,
            detail="This password reset link is invalid or has expired.",
        )

    return {
        "message": "Your password has been reset. You can now sign in."
    }
