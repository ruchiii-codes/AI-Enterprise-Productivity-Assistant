import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser


def parse_calendar_create_query(query):
    if not query:
        return None

    query_lower = query.lower().strip()

    # -------------------------------------------------
    # Detect title
    # -------------------------------------------------
    title = None

    title_match = re.search(
        r"(?:called|named|titled)\s+(.+?)(?=\s+(?:from|to|on|at)\b|$)",
        query,
        re.IGNORECASE,
    )

    if title_match:
        title = title_match.group(1).strip()

    if not title:
        if "interview" in query_lower:
            title = "Interview"
        elif "appointment" in query_lower:
            title = "Appointment"
        elif "meeting" in query_lower:
            title = "Meeting"
        else:
            title = "Event"

    # -------------------------------------------------
    # Detect event date
    # -------------------------------------------------
    event_date = None

    if "tomorrow" in query_lower:
        event_date = datetime.now().date() + timedelta(days=1)

    elif "today" in query_lower:
        event_date = datetime.now().date()

    else:
        # Explicit date with optional year:
        # August 25
        # August 25, 2026
        # Aug 25
        # Aug 25, 2026
        date_match = re.search(
            r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
            r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|"
            r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
            r"\s+\d{1,2}(?:st|nd|rd|th)?"
            r"(?:,\s*|\s+)?(?:\d{4})?\b",
            query,
            re.IGNORECASE,
        )

        if date_match:
            date_text = date_match.group(0)

            try:
                parsed_date = date_parser.parse(
                    date_text,
                    fuzzy=True,
                    default=datetime.now(),
                )

                # If year wasn't supplied, use current year.
                if not re.search(r"\b\d{4}\b", date_text):
                    parsed_date = parsed_date.replace(
                        year=datetime.now().year
                    )

                event_date = parsed_date.date()

            except (ValueError, TypeError):
                event_date = None

    # -------------------------------------------------
    # Find times
    # -------------------------------------------------
    time_matches = re.findall(
        r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b"
        r"|\b\d{1,2}:\d{2}\b"
        r"|\b(?:[01]?\d|2[0-3]):[0-5]\d\b",
        query,
        re.IGNORECASE,
    )

    times = [match.strip() for match in time_matches]

    if not times:
        return None

    # -------------------------------------------------
    # Detect duration
    # -------------------------------------------------
    duration_match = re.search(
        r"\bfor\s+(\d+(?:\.\d+)?)\s*"
        r"(hour|hours|hr|hrs|minute|minutes|min|mins)\b",
        query,
        re.IGNORECASE,
    )

    duration_minutes = None

    if duration_match:
        value = float(duration_match.group(1))
        unit = duration_match.group(2).lower()

        if unit in {"hour", "hours", "hr", "hrs"}:
            duration_minutes = int(value * 60)
        else:
            duration_minutes = int(value)

    # -------------------------------------------------
    # Parse start time
    # -------------------------------------------------
    start_time = date_parser.parse(times[0]).time()

    # -------------------------------------------------
    # Parse end time
    # -------------------------------------------------
    end_time = None

    if len(times) >= 2:
        # Explicit end time:
        # "from 3 PM to 4 PM"
        end_time = date_parser.parse(times[1]).time()

    elif duration_minutes is not None and event_date is not None:
        # Duration-based event:
        # "at 3 PM for 1 hour"
        start_datetime = datetime.combine(
            event_date,
            start_time,
        )

        end_datetime = start_datetime + timedelta(
            minutes=duration_minutes
        )

        end_time = end_datetime.time()

    return {
        "summary": title,
        "date": event_date,
        "start_time": start_time,
        "end_time": end_time,
    }