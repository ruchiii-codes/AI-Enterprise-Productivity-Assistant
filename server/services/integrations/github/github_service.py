import requests

from server.auth.database import SessionLocal
from server.auth.models import GitHubConnection


BASE_URL = "https://api.github.com"


def get_github_headers(user_id: int):
    """
    Get GitHub API headers for a specific WorkMind user.
    Uses the user's OAuth connection.
    """

    db = SessionLocal()

    try:
        connection = (
            db.query(GitHubConnection)
            .filter(GitHubConnection.user_id == user_id)
            .first()
        )

        if not connection:
            raise ValueError(
                "GitHub is not connected for this WorkMind user."
            )

        return {
            "Authorization": f"Bearer {connection.access_token}",
            "Accept": "application/vnd.github+json",
        }

    finally:
        db.close()


def get_authenticated_user(user_id: int):
    """
    Returns the authenticated GitHub user.
    """

    headers = get_github_headers(user_id)

    response = requests.get(
        f"{BASE_URL}/user",
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def list_repositories(user_id: int):
    """
    Returns all repositories owned by the authenticated GitHub user.
    """

    headers = get_github_headers(user_id)

    response = requests.get(
        f"{BASE_URL}/user/repos",
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def get_repository(user_id: int, owner: str, repo: str):
    """
    Returns details about a repository.
    """

    headers = get_github_headers(user_id)

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}",
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def list_issues(user_id: int, owner: str, repo: str):
    """
    Returns all issues for a repository.
    """

    headers = get_github_headers(user_id)

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/issues",
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def create_issue(
    user_id: int,
    owner: str,
    repo: str,
    title: str,
    body: str = "",
):
    """
    Creates a GitHub issue.
    """

    headers = get_github_headers(user_id)

    response = requests.post(
        f"{BASE_URL}/repos/{owner}/{repo}/issues",
        headers=headers,
        json={
            "title": title,
            "body": body,
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def list_pull_requests(user_id: int, owner: str, repo: str):
    """
    Returns all pull requests for a repository.
    """

    headers = get_github_headers(user_id)

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/pulls",
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()

def get_recent_activity(user_id: int, max_results=20):
    """
    Returns recent GitHub activity for the authenticated user.
    """

    headers = get_github_headers(user_id)

    user = get_authenticated_user(user_id)
    username = user["login"]

    response = requests.get(
        f"{BASE_URL}/users/{username}/events",
        headers=headers,
        params={"per_page": max_results},
        timeout=15,
    )

    response.raise_for_status()

    return response.json()