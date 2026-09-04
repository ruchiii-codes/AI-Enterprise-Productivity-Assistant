from datetime import datetime


def format_event(event):
    summary = event.get("summary", "No title")

    start = event.get("start", {})
    end = event.get("end", {})

    start_value = start.get("dateTime") or start.get("date")
    end_value = end.get("dateTime") or end.get("date")

    location = event.get("location")
    description = event.get("description")

    result = [
        f"Title: {summary}",
        f"Start: {start_value}",
        f"End: {end_value}",
    ]

    if location:
        result.append(f"Location: {location}")

    if description:
        result.append(f"Description: {description}")

    return "\n".join(result)


def format_events(events, title="Upcoming Calendar Events"):
    if not events:
        return "No upcoming calendar events found."

    output = [title, ""]

    for index, event in enumerate(events, start=1):
        output.append(f"{index}. {format_event(event)}")
        output.append("")

    return "\n".join(output)