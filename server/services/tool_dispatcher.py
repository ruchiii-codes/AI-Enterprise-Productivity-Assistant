from server.services.github_tool import (
    github_get_user,
    github_list_repositories,
)


def dispatch_tool(tool: str, action: str):
    """
    Dispatches tool requests.
    """

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

    raise ValueError(
        f"Unknown tool/action: {tool}/{action}"
    )