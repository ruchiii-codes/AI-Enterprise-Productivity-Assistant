import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser


def parse_calendar_create_query(query):
    query_lower = query.lower()

    # Detect title
    if "interview" in query_lower:
        title = "Interview"
    elif "appointment" in query_lower:
        title = "Appointment"
    elif "meeting" in query_lower:
        title = "Meeting"
    else:
        title = "Event"

    # Detect "tomorrow"
    if "tomorrow" in query_lower:
        event_date = datetime.now().date() + timedelta(days=1)
    elif "today" in query_lower:
        event_date = datetime.now().date()
    else:
        event_date = None

    # Find times such as:
    # 3 PM
    # 3:00 PM
    # 15:00
    times = re.findall(
        r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)?\b",
        query,
        re.IGNORECASE,
    )

    if not times:
        return None

    start_time = date_parser.parse(times[0]).time()

    # If there is no second time, don't create an event yet.
    if len(times) < 2:
        return {
            "summary": title,
            "date": event_date,
            "start_time": start_time,
            "end_time": None,
        }

    end_time = date_parser.parse(times[1]).time()

    return {
        "summary": title,
        "date": event_date,
        "start_time": start_time,
        "end_time": end_time,
    }