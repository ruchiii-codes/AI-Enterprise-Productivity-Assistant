import requests

from server.config import GITHUB_ACCESS_TOKEN


BASE_URL = "https://api.github.com"


headers = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_authenticated_user():
    """
    Returns the authenticated GitHub user.
    """

    response = requests.get(
        f"{BASE_URL}/user",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def list_repositories():
    """
    Returns all repositories owned by the authenticated user.
    """

    response = requests.get(
        f"{BASE_URL}/user/repos",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def get_repository(owner: str, repo: str):
    """
    Returns details about a repository.
    """

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def list_issues(owner: str, repo: str):
    """
    Returns all issues for a repository.
    """

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/issues",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def create_issue(owner: str, repo: str, title: str, body: str = ""):
    """
    Creates a GitHub issue.
    """

    response = requests.post(
        f"{BASE_URL}/repos/{owner}/{repo}/issues",
        headers=headers,
        json={
            "title": title,
            "body": body,
        },
    )

    response.raise_for_status()

    return response.json() 


def list_pull_requests(owner: str, repo: str):
    """
    Returns all pull requests for a repository.
    """

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/pulls",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()    