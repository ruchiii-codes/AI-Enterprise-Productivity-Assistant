from unittest.mock import patch

from server.services.planner_service import Route
from server.services.orchestrator_service import execute
from server.services.multi_tool.tool_call import ToolCall


def test_orchestrator_uses_single_tool_flow():
    with patch(
        "server.services.orchestrator_service.select_tools",
        return_value=[],
    ), patch(
        "server.services.tool_router.resolve_tool",
        return_value="Single tool result",
    ):

        result = execute(
            route=Route.TOOL,
            question="Find my emails",
        )

    assert result == {
        "answer": "Single tool result",
        "sources": [],
    }


def test_orchestrator_uses_multi_tool_flow():
    def gmail_tool():
        return "Gmail result"

    def calendar_tool():
        return "Calendar result"

    selected_tools = [
        ToolCall(tool=gmail_tool),
        ToolCall(tool=calendar_tool),
    ]

    expected_results = [
        {
            "success": True,
            "tool": "gmail_tool",
            "result": "Gmail result",
        },
        {
            "success": True,
            "tool": "calendar_tool",
            "result": "Calendar result",
        },
    ]

    with patch(
        "server.services.orchestrator_service.select_tools",
        return_value=selected_tools,
    ), patch(
        "server.services.orchestrator_service.execute_multiple_tools",
        return_value=expected_results,
    ):

        result = execute(
            route=Route.TOOL,
            question="Check emails and calendar",
        )

    assert result == {
        "answer": (
            "📧 Gmail\n\nGmail result\n\n"
            "📅 Calendar\n\nCalendar result"
        ),
        "sources": [],
    }