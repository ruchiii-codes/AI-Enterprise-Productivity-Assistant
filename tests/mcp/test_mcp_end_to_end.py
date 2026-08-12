from unittest.mock import patch

from server.services.mcp.mcp_orchestrator import execute_mcp_tools
from server.services.multi_tool.tool_selector import select_tools


def test_natural_language_request_selects_all_mcp_tools():
    question = (
        "Check my latest emails, show my upcoming meetings, "
        "and show my GitHub repositories"
    )

    selected_tools = select_tools(question)

    tool_names = [tool.tool.__name__ for tool in selected_tools]

    assert "gmail_list_messages" in tool_names
    assert "calendar_get_upcoming_events" in tool_names
    assert "github_list_repositories" in tool_names


def test_natural_language_request_executes_all_mcp_tools():
    question = (
        "Check my latest emails, show my upcoming meetings, "
        "and show my GitHub repositories"
    )

    selected_tools = select_tools(question)

    with patch(
        "server.services.mcp.mcp_orchestrator.execute_mcp_tool"
    ) as mock_execute:

        mock_execute.side_effect = [
            ["Gmail result"],
            ["Calendar result"],
            ["GitHub result"],
        ]

        results = execute_mcp_tools(selected_tools)

    assert len(results) == 3
    assert results[0]["success"] is True
    assert results[1]["success"] is True
    assert results[2]["success"] is True