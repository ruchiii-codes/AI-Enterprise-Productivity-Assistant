from server.services.multi_tool.tool_selector import select_tools


def test_select_gmail_and_calendar():
    tool_calls = select_tools(
        "Check my latest emails and show my upcoming meetings"
    )

    assert len(tool_calls) == 2


def test_select_github():
    tool_calls = select_tools(
        "Show my GitHub repositories"
    )

    assert len(tool_calls) == 1


def test_select_single_gmail_tool():
    tool_calls = select_tools(
        "Find my latest emails"
    )

    assert len(tool_calls) == 1


def test_select_no_tools():
    tool_calls = select_tools(
        "What is the weather today?"
    )

    assert len(tool_calls) == 0


def test_select_natural_language_gmail_calendar():
    tools = select_tools(
        "Check my emails and tell me what's on my schedule"
    )

    assert len(tools) == 2
    assert tools[0].tool.__name__ == "gmail_list_messages"
    assert tools[1].tool.__name__ == "calendar_get_upcoming_events"


def test_select_natural_language_all_tools():
    tools = select_tools(
        "Check my mail, upcoming meetings, and GitHub repositories"
    )

    assert len(tools) == 3

    tool_names = [tool.tool.__name__ for tool in tools]

    assert "gmail_list_messages" in tool_names
    assert "calendar_get_upcoming_events" in tool_names
    assert "github_list_repositories" in tool_names


def test_select_natural_language_calendar():
    tools = select_tools(
        "What do I have planned for today?"
    )

    assert len(tools) == 1
    assert tools[0].tool.__name__ == "calendar_get_upcoming_events"


def test_select_natural_language_github():
    tools = select_tools(
        "Show me my projects on GitHub"
    )

    assert len(tools) == 1
    assert tools[0].tool.__name__ == "github_list_repositories"