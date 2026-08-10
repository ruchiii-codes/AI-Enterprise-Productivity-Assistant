from server.services.calendar_service import (
    get_upcoming_events,
    search_events,
    create_event,
)
from server.services.calendar_formatter import format_events
from server.services.calendar_parser import parse_calendar_create_query
from datetime import datetime

def calendar_get_upcoming_events(max_results=10):
    events = get_upcoming_events(max_results=max_results)
    return format_events(events)


def calendar_search_events(query, max_results=10):
    events = search_events(
        query=query,
        max_results=max_results,
    )

    return format_events(events)


def calendar_create_event(
    summary,
    start_datetime,
    end_datetime,
    description=None,
    location=None,
):
    return create_event(
        summary=summary,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        description=description,
        location=location,
    )

def calendar_create_from_query(query):
    parsed = parse_calendar_create_query(query)

    if parsed is None:
        return "Please specify the date and time for the event."

    if parsed["date"] is None:
        return "Please specify the event date."

    if parsed["end_time"] is None:
        return (
            f"I can schedule '{parsed['summary']}' at "
            f"{parsed['start_time'].strftime('%I:%M %p').lstrip('0')}. "
            "Please provide the end time."
        )

    start_datetime = datetime.combine(
        parsed["date"],
        parsed["start_time"],
    ).isoformat()

    end_datetime = datetime.combine(
        parsed["date"],
        parsed["end_time"],
    ).isoformat()

    event = calendar_create_event(
        summary=parsed["summary"],
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )

    return (
        f"Calendar event created successfully.\n"
        f"Title: {event.get('summary')}\n"
        f"Event ID: {event.get('id')}\n"
        f"Link: {event.get('htmlLink')}"
    )