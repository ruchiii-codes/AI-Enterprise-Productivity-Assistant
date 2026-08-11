from server.services.multi_tool.result_formatter import format_multi_tool_results


def test_format_successful_results():
    results = [
        {
            "success": True,
            "tool": "gmail_list_messages",
            "result": "Gmail result",
        },
        {
            "success": True,
            "tool": "calendar_get_upcoming_events",
            "result": "Calendar result",
        },
    ]

    formatted = format_multi_tool_results(results)

    assert formatted == (
        "📧 Gmail\n\nGmail result\n\n"
        "📅 Calendar\n\nCalendar result"
    )


def test_format_failed_result():
    results = [
        {
            "success": True,
            "tool": "gmail_list_messages",
            "result": "Gmail result",
        },
        {
            "success": False,
            "tool": "calendar_get_upcoming_events",
            "result": None,
            "error": "Calendar authentication failed",
        },
    ]

    formatted = format_multi_tool_results(results)

    assert formatted == (
        "📧 Gmail\n\nGmail result\n\n"
        "❌ calendar_get_upcoming_events failed\n\n"
        "Calendar authentication failed"
    )