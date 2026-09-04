import secrets
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User, GitHubConnection
from server.config import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
)

router = APIRouter(
    prefix="/auth/github",
    tags=["GitHub OAuth"],
)

# Temporary in-memory OAuth state storage.
# Good enough for local development.
oauth_states = {}

@router.get("/status")
def github_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(GitHubConnection)
        .filter(GitHubConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "connected": False,
            "username": None,
        }

    return {
        "connected": True,
        "username": connection.github_username,
    }

@router.delete("/disconnect")
def github_disconnect(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = (
        db.query(GitHubConnection)
        .filter(GitHubConnection.user_id == current_user.id)
        .first()
    )

    if not connection:
        return {
            "disconnected": True,
            "message": "GitHub is already disconnected.",
        }

    db.delete(connection)
    db.commit()

    return {
        "disconnected": True,
        "message": "GitHub disconnected successfully.",
    }

@router.get("/start")
def github_start(
    current_user=Depends(get_current_user),
):
    """
    Create a GitHub OAuth authorization URL
    for the currently authenticated WorkMind user.
    """

    state = secrets.token_urlsafe(32)

    oauth_states[state] = current_user.id

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "repo",
        "state": state,
    }

    github_url = (
        "https://github.com/login/oauth/authorize?"
        + urlencode(params)
    )

    return {
        "authorization_url": github_url
    }

@router.get("/callback")
def github_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Handle GitHub OAuth callback.
    """

    # Validate OAuth state
    user_id = oauth_states.pop(state, None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired GitHub OAuth state.",
        )

    # Exchange authorization code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={
            "Accept": "application/json",
        },
        timeout=15,
    )

    token_response.raise_for_status()

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="GitHub did not return an access token.",
        )

    # Get GitHub user information
    github_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=15,
    )

    github_response.raise_for_status()

    github_user = github_response.json()

    github_user_id = github_user["id"]
    github_username = github_user["login"]

    # Check whether this WorkMind user already has a GitHub connection
    connection = (
        db.query(GitHubConnection)
        .filter(GitHubConnection.user_id == user_id)
        .first()
    )

    if connection:
        connection.github_user_id = github_user_id
        connection.github_username = github_username
        connection.access_token = access_token
    else:
        connection = GitHubConnection(
            user_id=user_id,
            github_user_id=github_user_id,
            github_username=github_username,
            access_token=access_token,
        )

        db.add(connection)

    db.commit()

    # Return to frontend
    return RedirectResponse(
        url="http://localhost:5173/tools"
    )