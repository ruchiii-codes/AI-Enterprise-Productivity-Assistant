import secrets
from urllib.parse import urlencode

import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User, GmailConnection

from server.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)


router = APIRouter(
    prefix="/auth/gmail",
    tags=["Gmail OAuth"],
)


# Temporary in-memory OAuth state storage.
# Good enough for local development.
oauth_states = {}


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


@router.get("/status")
def gmail_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(GmailConnection)
        .filter(GmailConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "connected": False,
            "email": None,
        }

    return {
        "connected": True,
        "email": connection.gmail_email,
    }


@router.delete("/disconnect")
def gmail_disconnect(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(GmailConnection)
        .filter(GmailConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "disconnected": True,
            "message": "Gmail is already disconnected.",
        }

    db.delete(connection)
    db.commit()

    return {
        "disconnected": True,
        "message": "Gmail disconnected successfully.",
    }


@router.get("/start")
def gmail_start(
    current_user: User = Depends(get_current_user),
):
    """
    Create a Google OAuth authorization URL
    for the currently authenticated WorkMind user.
    """

    state = secrets.token_urlsafe(32)

    oauth_states[state] = current_user.id

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GMAIL_SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    google_url = (
        GOOGLE_AUTH_URL
        + "?"
        + urlencode(params)
    )

    return {
        "authorization_url": google_url
    }


@router.get("/callback")
def gmail_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth callback.
    """

    # Validate OAuth state
    user_id = oauth_states.pop(state, None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired Gmail OAuth state.",
        )

    # Exchange authorization code for tokens
    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI,
        },
        timeout=15,
    )

    if not token_response.ok:
        raise HTTPException(
            status_code=400,
            detail="Google token exchange failed.",
        )

    token_data = token_response.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    token_uri = GOOGLE_TOKEN_URL

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Google did not return an access token.",
        )

    if not refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Google did not return a refresh token.",
        )

    # Get Gmail profile
    profile_response = requests.get(
        "https://gmail.googleapis.com/gmail/v1/users/me/profile",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=15,
    )

    if not profile_response.ok:
        raise HTTPException(
            status_code=400,
            detail="Unable to retrieve Gmail profile.",
        )

    profile = profile_response.json()

    gmail_email = profile.get("emailAddress")

    if not gmail_email:
        raise HTTPException(
            status_code=400,
            detail="Unable to determine Gmail account email.",
        )

    # Check whether this WorkMind user already has a Gmail connection
    connection = (
        db.query(GmailConnection)
        .filter(GmailConnection.user_id == user_id)
        .first()
    )

    if connection:
        connection.gmail_email = gmail_email
        connection.access_token = access_token
        connection.refresh_token = refresh_token
        connection.token_uri = token_uri

    else:
        connection = GmailConnection(
            user_id=user_id,
            gmail_email=gmail_email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
        )

        db.add(connection)

    db.commit()

    # Return to frontend
    return RedirectResponse(
        url="http://localhost:5173/tools"
    )