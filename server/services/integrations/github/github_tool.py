from server.services.integrations.github.github_service import (
    get_authenticated_user,
    list_repositories,
)

from server.services.integrations.github.github_service import get_repository

from server.services.integrations.github.github_service import (
    list_issues,
    create_issue,
)

from server.services.integrations.github.github_service import list_pull_requests

def github_get_user():
    """
    Returns basic information about the authenticated GitHub user.
    """

    user = get_authenticated_user()

    return {
        "username": user["login"],
        "name": user.get("name"),
        "profile_url": user["html_url"],
    }


def github_list_repositories():
    """
    Returns a simplified list of repositories.
    """

    repositories = list_repositories()

    results = []

    for repo in repositories:
        results.append(
            {
                "name": repo["name"],
                "private": repo["private"],
                "url": repo["html_url"],
            }
        )

    return results


def github_repository_details(owner: str, repo: str):
    """
    Returns simplified repository details.
    """

    repository = get_repository(owner, repo)

    return {
        "name": repository["name"],
        "description": repository["description"],
        "private": repository["private"],
        "default_branch": repository["default_branch"],
        "stars": repository["stargazers_count"],
        "forks": repository["forks_count"],
        "open_issues": repository["open_issues_count"],
        "url": repository["html_url"],
    }


def github_list_issues(owner: str, repo: str):
    """
    Returns simplified GitHub issues.
    """

    issues = list_issues(owner, repo)

    results = []

    for issue in issues:

        # Skip pull requests
        if "pull_request" in issue:
            continue

        results.append(
            {
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "url": issue["html_url"],
            }
        )

    return results


def github_create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str = "",
):
    """
    Creates a GitHub issue.
    """

    issue = create_issue(
        owner=owner,
        repo=repo,
        title=title,
        body=body,
    )

    return {
        "number": issue["number"],
        "title": issue["title"],
        "state": issue["state"],
        "url": issue["html_url"],
    }   


def github_list_pull_requests(owner: str, repo: str):
    """
    Returns simplified pull requests.
    """

    pull_requests = list_pull_requests(owner, repo)

    results = []

    for pr in pull_requests:

        results.append(
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "url": pr["html_url"],
            }
        )

    return results    


def github_get_owner():
    """
    Returns the authenticated GitHub username.
    """

    user = get_authenticated_user()

    return user["login"]    