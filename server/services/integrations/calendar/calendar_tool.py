from server.services.integrations.calendar.calendar_service import (
    get_upcoming_events,
    get_tomorrow_events,
    search_events,
    create_event,
)
from server.services.integrations.calendar.calendar_formatter import format_events
from server.services.integrations.calendar.calendar_parser import parse_calendar_create_query
from datetime import datetime

def calendar_get_upcoming_events(user_id, max_results=10):
    events = get_upcoming_events(
        user_id=user_id,
        max_results=max_results,
    )
    return format_events(events)

def calendar_get_tomorrow_events(user_id, max_results=10):
    events = get_tomorrow_events(
        user_id=user_id,
        max_results=max_results,
    )
    return format_events(
        events,
        title="Tomorrow's Calendar Events",
    )
    

def calendar_search_events(user_id, query, max_results=10):
    events = search_events(
        user_id=user_id,
        query=query,
        max_results=max_results,
    )

    return format_events(
        events,
        title="Calendar Search Results",
    )


def calendar_create_event(
    user_id,
    summary,
    start_datetime,
    end_datetime,
    description=None,
    location=None,
):
    return create_event(
        user_id=user_id,
        summary=summary,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        description=description,
        location=location,
    )

def calendar_create_from_query(user_id, query):
    parsed = parse_calendar_create_query(query)

    if parsed is None:
        return "Please specify the date and time for the event."

    if parsed["date"] is None:
        return "Please specify the event date."

    if parsed["start_time"] is None:
        return "Please specify the event start time."

    # Default to a 1-hour meeting when no end time is provided.
    if parsed["end_time"] is None:
        from datetime import timedelta

        end_time = (
            datetime.combine(
                parsed["date"],
                parsed["start_time"],
            )
            + timedelta(hours=1)
        )

        start_datetime = datetime.combine(
            parsed["date"],
            parsed["start_time"],
        ).isoformat()

        end_datetime = end_time.isoformat()

    else:
        start_datetime = datetime.combine(
            parsed["date"],
            parsed["start_time"],
        ).isoformat()

        end_datetime = datetime.combine(
            parsed["date"],
            parsed["end_time"],
        ).isoformat()

    event = calendar_create_event(
        user_id=user_id,
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