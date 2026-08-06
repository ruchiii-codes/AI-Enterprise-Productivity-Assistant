from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from server.auth.auth_service import (
    authenticate_user,
    register_user,
)
from server.auth.database import get_db

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

    if new_user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

    return new_user


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

    access_token = create_access_token(
        {
            "sub": authenticated_user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }