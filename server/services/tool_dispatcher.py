from server.services.github_tool import (
    github_get_user,
    github_list_repositories,
)

from server.services.gmail_tool import (
    gmail_get_profile,
    gmail_list_messages,
    gmail_search_messages,
    gmail_get_message,
    gmail_send_email,
)


def dispatch_tool(tool: str, action: str, params=None):
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

        if action == "user":
            return github_get_user()

        if action == "repositories":
            return github_list_repositories()

    # -----------------------------
    # Gmail
    # -----------------------------
    if tool == "gmail":

        if action == "profile":
            return gmail_get_profile()

        if action == "list_messages":
            return gmail_list_messages(
                max_results=params.get(
                    "max_results",
                    10,
                )
            )

        if action == "search_messages":
            return gmail_search_messages(
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
                message_id=params.get(
                    "message_id"
                )
            )

        if action == "send_email":
            return gmail_send_email(
                to=params.get("to"),
                subject=params.get("subject"),
                body=params.get("body"),
            )

    raise ValueError(
        f"Unknown tool/action: {tool}/{action}"
    )