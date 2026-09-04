import secrets
from urllib.parse import urlencode

import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User, CalendarConnection

from server.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CALENDAR_REDIRECT_URI,
)


router = APIRouter(
    prefix="/auth/calendar",
    tags=["Calendar OAuth"],
)


# Temporary in-memory OAuth state storage.
# Good enough for local development.
oauth_states = {}


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "openid",
    "email",
    "profile",
]


@router.get("/status")
def calendar_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(CalendarConnection)
        .filter(CalendarConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "connected": False,
            "email": None,
        }

    return {
        "connected": True,
        "email": connection.calendar_email,
    }


@router.delete("/disconnect")
def calendar_disconnect(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(CalendarConnection)
        .filter(CalendarConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "disconnected": True,
            "message": "Calendar is already disconnected.",
        }

    db.delete(connection)
    db.commit()

    return {
        "disconnected": True,
        "message": "Calendar disconnected successfully.",
    }


@router.get("/start")
def calendar_start(
    current_user: User = Depends(get_current_user),
):
    state = secrets.token_urlsafe(32)

    oauth_states[state] = current_user.id

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_CALENDAR_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(CALENDAR_SCOPES),
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
def calendar_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    user_id = oauth_states.pop(state, None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired Calendar OAuth state.",
        )

    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_CALENDAR_REDIRECT_URI,
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

    # Get Google account email
    profile_response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=15,
    )
    
    if not profile_response.ok:
        raise HTTPException(
            status_code=400,
            detail="Unable to retrieve Google account profile.",
        )
    
    profile = profile_response.json()
    
    calendar_email = profile.get("email")

    if not calendar_email:
        raise HTTPException(
            status_code=400,
            detail="Unable to determine Google account email.",
        )

    # Check whether this WorkMind user already has a Calendar connection
    connection = (
        db.query(CalendarConnection)
        .filter(CalendarConnection.user_id == user_id)
        .first()
    )

    if connection:
        connection.calendar_email = calendar_email
        connection.access_token = access_token
        connection.refresh_token = refresh_token
        connection.token_uri = token_uri

    else:
        connection = CalendarConnection(
            user_id=user_id,
            calendar_email=calendar_email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
        )

        db.add(connection)

    db.commit()

    return RedirectResponse(
        url="http://localhost:5173/tools"
    )