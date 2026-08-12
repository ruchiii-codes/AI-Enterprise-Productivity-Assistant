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
    Select one or more tools from natural-language user requests.
    """

    question_lower = question.lower()

    tool_calls = []

    # -------------------------
    # Gmail
    # -------------------------
    gmail_keywords = [
        "email",
        "emails",
        "mail",
        "mails",
        "inbox",
        "gmail",
        "message",
        "messages",
        "unread",
        "received",
        "sent email",
    ]

    if any(keyword in question_lower for keyword in gmail_keywords):
        tool_calls.append(
            ToolCall(
                tool=gmail_list_messages,
                args={"max_results": 10},
            )
        )

    # -------------------------
    # Calendar
    # -------------------------
    calendar_keywords = [
        "calendar",
        "meeting",
        "meetings",
        "event",
        "events",
        "schedule",
        "appointment",
        "appointments",
        "upcoming",
        "agenda",
        "availability",
        "planned",
        "plan",
    ]

    if any(keyword in question_lower for keyword in calendar_keywords):
        tool_calls.append(
            ToolCall(
                tool=calendar_get_upcoming_events,
                args={"max_results": 10},
            )
        )

    # -------------------------
    # GitHub
    # -------------------------
    github_keywords = [
        "github",
        "repository",
        "repositories",
        "repo",
        "repos",
        "pull request",
        "pull requests",
        "pulls",
        "code repository",
    ]

    if any(keyword in question_lower for keyword in github_keywords):
        tool_calls.append(
            ToolCall(
                tool=github_list_repositories,
                args={},
            )
        )

    return tool_calls