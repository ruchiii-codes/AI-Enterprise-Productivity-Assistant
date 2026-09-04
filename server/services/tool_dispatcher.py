from server.services.integrations.github.github_tool import (
    github_get_user,
    github_list_repositories,
    github_list_issues,
    github_list_pull_requests,
    github_repository_details,
    github_create_issue,
    github_get_recent_activity,
)

from server.services.integrations.gmail.gmail_tool import (
    gmail_get_profile,
    gmail_list_messages,
    gmail_search_messages,
    gmail_search_and_summarize,
    gmail_get_message,
    gmail_send_email,
    gmail_summarize_message,
    gmail_summarize_latest_email,
    gmail_get_latest_message,
)

from server.services.integrations.calendar.calendar_tool import (
    calendar_get_tomorrow_events,
    calendar_get_upcoming_events,
    calendar_search_events,
    calendar_create_event,
    calendar_create_from_query,
)

def dispatch_tool(
    tool: str,
    action: str,
    params=None,
    user_id: int = None,
    question: str = None,
):
    """
    Dispatches tool requests with optional parameters.
    """

    if params is None:
        params = {}

    tool = tool.lower().strip()
    action = action.lower().strip()

    # -----------------------------
    # GitHub
    # -----------------------------
    if tool == "github":

        if action == "recent_activity":
            return github_get_recent_activity(
                user_id=user_id,
                max_results=params.get("max_results", 20),
            )

        if action == "user":
            return github_get_user(user_id)

        if action == "repositories":
            return github_list_repositories(user_id)

        if action == "list_issues":
            repo = params.get("repo")
        
            if not repo:
                raise ValueError("Repository name is required.")
        
            github_user = github_get_user(user_id)
            owner = github_user["username"]
        
            return github_list_issues(
                user_id=user_id,
                owner=owner,
                repo=repo,
            )

        if action == "list_pull_requests":
            repo = params.get("repo")
        
            if not repo:
                raise ValueError("Repository name is required.")
        
            github_user = github_get_user(user_id)
            owner = github_user["username"]
        
            return github_list_pull_requests(
                user_id=user_id,
                owner=owner,
                repo=repo,
            )     

        if action == "repository_details":
            repo = params.get("repo")
        
            if not repo:
                raise ValueError("Repository name is required.")
        
            github_user = github_get_user(user_id)
            owner = github_user["username"]
        
            return github_repository_details(
                user_id=user_id,
                owner=owner,
                repo=repo,
            )   

        if action == "create_issue":
            repo = params.get("repo")
            title = params.get("title")
            body = params.get("body", "")
        
            if not repo:
                raise ValueError("Repository name is required.")
        
            if not title:
                raise ValueError("Issue title is required.")
        
            github_user = github_get_user(user_id)
            owner = github_user["username"]
        
            return github_create_issue(
                user_id=user_id,
                owner=owner,
                repo=repo,
                title=title,
                body=body,
            )   

    # -----------------------------
    # Gmail
    # -----------------------------
    if tool == "gmail":

        if action == "profile":
            return gmail_get_profile(user_id=user_id)

        if action == "list_messages":
            return gmail_list_messages(
                user_id=user_id,
                max_results=params.get(
                    "max_results",
                    10,
                )
            )

        if action == "get_latest_message":
            return gmail_get_latest_message(user_id=user_id)

        if action == "search_messages":
            return gmail_search_messages(
                user_id=user_id,
                query=params.get(
                    "query",
                    "",
                ),
                max_results=params.get(
                    "max_results",
                    10,
                ),
            )

        if action == "search_and_summarize":
            return gmail_search_and_summarize(
                user_id=user_id,
                query=params.get(
                    "query",
                    "",
                ),
                max_results=params.get(
                    "max_results",
                    10,
                ),
            )

        if action == "get_message":
            return gmail_get_message(
                user_id=user_id,
                message_id=params.get(
                    "message_id"
                )
            )

        if action == "send_email":
            result = gmail_send_email(
                user_id=user_id,
                to=params.get("to"),
                subject=params.get("subject"),
                body=params.get("body"),
            )
        
            return {
                "success": True,
                "message": "Email sent successfully.",
                "to": params.get("to"),
                "subject": params.get("subject"),
            }

        if action == "summarize_message":
            return gmail_summarize_message(
                user_id=user_id,
                message_id=params.get("message_id")
            )

        if action in ["summarize_latest", "summarize_latest_message"]:
            return gmail_summarize_latest_email(user_id=user_id)


    # -----------------------------
    # Calendar
    # -----------------------------
    if tool == "calendar":

        if action == "upcoming_events":
            return calendar_get_upcoming_events(
                user_id=user_id,
                max_results=params.get("max_results", 10),
            )

        if action == "tomorrow_events":
            return calendar_get_tomorrow_events(
                user_id=user_id,
                max_results=params.get("max_results", 10),
            )
        
        if action == "search_events":
            return calendar_search_events(
                user_id=user_id,
                query=params.get("query", ""),
                max_results=params.get("max_results", 10),
            )
        
        if action == "create_event":

            # If the planner has already extracted structured
            # event parameters, create the event directly.
            if (
                params.get("summary")
                and params.get("start_datetime")
                and params.get("end_datetime")
            ):
                return calendar_create_event(
                    user_id=user_id,
                    summary=params.get("summary"),
                    start_datetime=params.get("start_datetime"),
                    end_datetime=params.get("end_datetime"),
                    description=params.get("description"),
                    location=params.get("location"),
                )
        
            # Otherwise use the original natural-language parser.
            if question:
                return calendar_create_from_query(
                    user_id=user_id,
                    query=question,
                )
        
            raise ValueError("Calendar event details are missing.")

    raise ValueError(
        f"Unknown tool/action: {tool}/{action}"
    )