def format_repositories(repositories):
    """
    Formats repository information for the AI response.
    """

    if not repositories:
        return "You don't have any repositories."

    response = f"You have {len(repositories)} repository(ies):\n\n"

    for repo in repositories:

        visibility = "Private" if repo["private"] else "Public"

        response += (
            f"• {repo['name']} ({visibility})\n"
            f"{repo['url']}\n\n"
        )

    return response.strip()


def format_repository_details(repository):
    """
    Formats repository details.
    """

    visibility = "Private" if repository["private"] else "Public"

    return (
        f"Repository: {repository['name']}\n\n"
        f"Visibility: {visibility}\n"
        f"Default Branch: {repository['default_branch']}\n"
        f"Stars: {repository['stars']}\n"
        f"Forks: {repository['forks']}\n"
        f"Open Issues: {repository['open_issues']}\n\n"
        f"URL:\n{repository['url']}"
    )


def format_issues(issues):
    """
    Formats GitHub issues.
    """

    if not issues:
        return "There are no open issues."

    response = f"Found {len(issues)} issue(s):\n\n"

    for issue in issues:

        response += (
            f"#{issue['number']} - {issue['title']}\n"
            f"Status: {issue['state']}\n"
            f"{issue['url']}\n\n"
        )

    return response.strip()


def format_pull_requests(pull_requests):
    """
    Formats pull requests.
    """

    if not pull_requests:
        return "There are no open pull requests."

    response = f"Found {len(pull_requests)} pull request(s):\n\n"

    for pr in pull_requests:

        response += (
            f"#{pr['number']} - {pr['title']}\n"
            f"Status: {pr['state']}\n"
            f"{pr['url']}\n\n"
        )

    return response.strip()


def format_created_issue(issue):
    """
    Formats a created issue.
    """

    return (
        "GitHub issue created successfully!\n\n"
        f"Issue #{issue['number']}\n"
        f"Title: {issue['title']}\n"
        f"Status: {issue['state']}\n\n"
        f"{issue['url']}"
    )