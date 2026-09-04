from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from server.auth.auth_service import (
    authenticate_user,
    register_user,
)
from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User

from server.auth.schemas import (
    UserRegister,
    UserResponse,
)
from server.auth.security import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
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
def login(
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