from server.services.integrations.github.github_service import (
    get_authenticated_user,
    list_repositories,
    get_repository,
    list_issues,
    create_issue,
    list_pull_requests,
    get_recent_activity,
)
from server.services.integrations.github.github_formatter import (
    format_repositories,
    format_issues,
    format_pull_requests,
    format_repository_details,
)

def github_get_user(user_id: int):
    """
    Returns basic information about the authenticated GitHub user.
    """

    user = get_authenticated_user(user_id)

    return {
        "username": user["login"],
        "name": user.get("name"),
        "profile_url": user["html_url"],
    }


def github_list_repositories(user_id: int):
    """
    Returns a simplified list of repositories.
    """

    repositories = list_repositories(user_id)

    results = []

    for repo in repositories:
        results.append(
            {
                "name": repo["name"],
                "private": repo["private"],
                "url": repo["html_url"],
            }
        )

    return format_repositories(results)


def github_repository_details(
    user_id: int,
    owner: str,
    repo: str,
):
    """
    Returns simplified repository details.
    """

    repository = get_repository(
        user_id=user_id,
        owner=owner,
        repo=repo,
    )

    return format_repository_details({
        "name": repository["name"],
        "description": repository["description"],
        "private": repository["private"],
        "default_branch": repository["default_branch"],
        "stars": repository["stargazers_count"],
        "forks": repository["forks_count"],
        "open_issues": repository["open_issues_count"],
        "url": repository["html_url"],
    })


def github_list_issues(
    user_id: int,
    owner: str,
    repo: str,
):
    """
    Returns simplified GitHub issues.
    """

    issues = list_issues(
        user_id=user_id,
        owner=owner,
        repo=repo,
    )

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

    return format_issues(results)


def github_create_issue(
    user_id: int,
    owner: str,
    repo: str,
    title: str,
    body: str = "",
):
    """
    Creates a GitHub issue.
    """

    issue = create_issue(
        user_id=user_id,
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


def github_list_pull_requests(
    user_id: int,
    owner: str,
    repo: str,
):
    """
    Returns simplified pull requests.
    """

    pull_requests = list_pull_requests(
        user_id=user_id,
        owner=owner,
        repo=repo,
    )

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

    return format_pull_requests(results)


def github_get_owner(user_id: int):
    """
    Returns the authenticated GitHub username.
    """

    user = get_authenticated_user(user_id)

    return user["login"]

def github_get_recent_activity(
    user_id: int,
    max_results=20,
):
    """
    Returns recent GitHub activity in a readable format.
    """

    events = get_recent_activity(
        user_id=user_id,
        max_results=max_results,
    )

    if not events:
        return "No recent GitHub activity found."

    results = []

    for event in events:
        event_type = event.get("type", "Unknown")
        repo = event.get("repo", {}).get("name", "Unknown repository")
        created_at = event.get("created_at", "")

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            count = len(commits)
            description = f"Pushed {count} commit(s)"

        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action", "updated")
            issue = event.get("payload", {}).get("issue", {})
            description = f"{action.capitalize()} issue #{issue.get('number', '')}: {issue.get('title', '')}"

        elif event_type == "PullRequestEvent":
            action = event.get("payload", {}).get("action", "updated")
            pr = event.get("payload", {}).get("pull_request", {})
            description = f"{action.capitalize()} PR #{pr.get('number', '')}: {pr.get('title', '')}"

        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type", "resource")
            description = f"Created {ref_type}"

        elif event_type == "DeleteEvent":
            ref_type = event.get("payload", {}).get("ref_type", "resource")
            description = f"Deleted {ref_type}"

        elif event_type == "WatchEvent":
            description = "Starred repository"

        else:
            description = event_type.replace("Event", "")

        results.append(
            f"- {description} in `{repo}` ({created_at})"
        )

    return "## 🐙 Recent GitHub Activity\n\n" + "\n".join(results)