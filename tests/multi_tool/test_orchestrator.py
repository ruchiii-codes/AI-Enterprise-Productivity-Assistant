from unittest.mock import patch

from server.services.planner_service import Route
from server.services.orchestrator_service import execute


def test_orchestrator_uses_single_tool_flow():
    plan = {
        "route": Route.TOOL,
        "tool": "gmail",
        "intent": "list_messages",
        "parameters": {},
    }

    with patch(
        "server.services.tool_dispatcher.dispatch_tool",
        return_value="Single tool result",
    ):
        result = execute(
            plan=plan,
            question="Find my emails",
        )

    assert result == {
        "answer": "Single tool result",
        "sources": [],
    }


def test_orchestrator_uses_tool_flow_for_combined_request():
    plan = {
        "route": Route.TOOL,
        "tool": "gmail",
        "intent": "list_messages",
        "parameters": {},
    }

    with patch(
        "server.services.tool_dispatcher.dispatch_tool",
        return_value="Gmail result",
    ):
        result = execute(
            plan=plan,
            question="Check emails and calendar",
        )

    assert result == {
        "answer": "Gmail result",
        "sources": [],
    }