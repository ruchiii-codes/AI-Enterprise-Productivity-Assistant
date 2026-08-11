from server.services.multi_tool.tool_call import ToolCall

from server.services.integrations.gmail.gmail_tool import (
    gmail_list_messages,
    gmail_search_messages,
)

from server.services.integrations.calendar.calendar_tool import (
    calendar_get_upcoming_events,
    calendar_search_events,
)

from server.services.integrations.github.github_tool import (
    github_list_repositories,
    github_list_pull_requests,
)


def select_tools(question: str) -> list[ToolCall]:
    """
    Select one or more tools based on keywords in the user's question.

    This is the first deterministic version of multi-tool selection.
    """

    question_lower = question.lower()

    tool_calls = []

    # -------------------------
    # Gmail
    # -------------------------
    if any(
        keyword in question_lower
        for keyword in [
            "email",
            "emails",
            "mail",
            "mails",
            "inbox",
        ]
    ):
        tool_calls.append(
            ToolCall(
                tool=gmail_list_messages,
                args={"max_results": 10},
            )
        )

    # -------------------------
    # Calendar
    # -------------------------
    if any(
        keyword in question_lower
        for keyword in [
            "calendar",
            "meeting",
            "meetings",
            "event",
            "events",
            "schedule",
        ]
    ):
        tool_calls.append(
            ToolCall(
                tool=calendar_get_upcoming_events,
                args={"max_results": 10},
            )
        )

    # -------------------------
    # GitHub
    # -------------------------
    if any(
        keyword in question_lower
        for keyword in [
            "github",
            "repository",
            "repositories",
            "repo",
            "repos",
            "pull request",
            "pull requests",
        ]
    ):
        tool_calls.append(
            ToolCall(
                tool=github_list_repositories,
                args={},
            )
        )

    return tool_calls