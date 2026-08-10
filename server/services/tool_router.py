from server.services.github_tool import github_get_owner
from server.services.tool_dispatcher import dispatch_tool
from server.services.github_parser import extract_repository_name
from server.services.github_issue_parser import extract_issue_title
from server.services.github_tool import github_create_issue
from server.services.github_formatter import format_created_issue

from server.services.github_formatter import (
    format_repositories,
    format_repository_details,
    format_issues,
    format_pull_requests,
    format_created_issue,
)

from server.services.github_tool import (
    github_get_user,
    github_list_repositories,
    github_repository_details,
    github_list_issues,
    github_list_pull_requests,
)

from server.services.gmail_tool import (
    gmail_get_profile,
    gmail_list_messages,
    gmail_search_messages,
    gmail_get_message,
)

from server.services.calendar_tool import (
    calendar_get_upcoming_events,
    calendar_search_events,
    calendar_create_event,
)

from server.services.gmail_formatter import (
    format_profile,
    format_messages,
    format_message,
)

from server.services.gmail_parser import (
    extract_gmail_search_query,
)

def resolve_tool(query: str):
    """
    Routes tool requests and formats the response.
    """

    query = query.lower()

    # -----------------------------
    # Gmail Profile
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "gmail profile",
            "my gmail account",
            "my email account",
        ]
    ):
        profile = gmail_get_profile()

        return format_profile(profile)

    # -----------------------------
    # Gmail Latest Email Summary
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "summarize my latest email",
            "summarize my latest mail",
            "summarize the latest email",
            "summarize the latest mail",
        ]
    ):
        from server.services.gmail_tool import gmail_summarize_latest_email

        return gmail_summarize_latest_email()

    # -----------------------------
    # Gmail Recent Emails
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "recent emails",
            "latest emails",
            "recent mails",
            "latest mails",
            "show my emails",
            "show my mails",
        ]
    ):
        messages = gmail_list_messages(
            max_results=10
        )

        return format_messages(messages)

    # -----------------------------
    # Gmail Search
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "find emails",
            "search emails",
            "find mails",
            "search mails",
            "emails from",
            "emails about",
            "mail from",
            "mail about",
        ]
    ):
        search_query = extract_gmail_search_query(query)

        if search_query is None:
            return "Please specify what emails you want to search for."

        messages = gmail_search_messages(
            query=search_query,
            max_results=10,
        )

        return format_messages(messages)

    # -----------------------------
    # Calendar - Upcoming Events
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "upcoming events",
            "upcoming meetings",
            "upcoming appointments",
            "show my calendar",
            "show my upcoming meetings",
            "show my upcoming events",
        ]
    ):
        return calendar_get_upcoming_events(max_results=10)

    # -----------------------------
    # Calendar - Search Events
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "find my meeting",
            "find my meetings",
            "find my event",
            "find my events",
            "find meeting",
            "find meetings",
            "find event",
            "find events",
            "find my interview",
            "find interview",
            "search my calendar",
            "search calendar",
        ]
    ):
        search_query = query

        return calendar_search_events(
            query=search_query,
            max_results=10,
        )  

    # -----------------------------
    # Calendar - Create Event
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "schedule a meeting",
            "schedule a meeting",
            "schedule an event",
            "create a meeting",
            "create an event",
        ]
    ):
        from server.services.calendar_tool import calendar_create_from_query

        return calendar_create_from_query(query)


    # -----------------------------
    # GitHub User
    # -----------------------------
    if "who am i on github" in query:

        user = github_get_user()

        return (
            f"GitHub Username: {user['username']}\n"
            f"Profile: {user['profile_url']}"
        )

    # -----------------------------
    # Repository Details
    # -----------------------------
    if "repository details" in query:

        repo = extract_repository_name(query)

        if repo is None:
            return "Please specify a repository name."

        repository = github_repository_details(
            owner=github_get_owner(),
            repo=repo,
        )

        return format_repository_details(repository)

    # -----------------------------
    # Create Issue
    # -----------------------------

    if any(
        phrase in query
        for phrase in [
            "create issue",
            "create an issue",
            "open issue",
            "open an issue",
            "new issue",
        ]
    ):

        repo = extract_repository_name(query)

        if repo is None:
            return "Please specify a repository."

        title = extract_issue_title(query)
    
        if title is None:
            return 'Please provide an issue title using: titled "Your Title".'

        issue = github_create_issue(
            owner=github_get_owner(),
            repo=repo,
            title=title,
        )

        return format_created_issue(issue)


    # -----------------------------
    # List Issues
    # -----------------------------
    if "issues" in query:

        repo = extract_repository_name(query)

        if repo is None:
            return "Please specify a repository name."

        issues = github_list_issues(
            owner=github_get_owner(),
            repo=repo,
        )

        return format_issues(issues)

    # -----------------------------
    # Pull Requests
    # -----------------------------
    if "pull request" in query or "pull requests" in query:

        repo = extract_repository_name(query)

        if repo is None:
            return "Please specify a repository name."

        pull_requests = github_list_pull_requests(
            owner=github_get_owner(),
            repo=repo,
        )

        return format_pull_requests(pull_requests)

    # -----------------------------
    # List Repositories
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "repositories",
            "repository",
            "repos",
            "repo",
        ]
    ):
        repositories = github_list_repositories()
        return format_repositories(repositories)