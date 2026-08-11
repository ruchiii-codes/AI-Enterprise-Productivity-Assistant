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