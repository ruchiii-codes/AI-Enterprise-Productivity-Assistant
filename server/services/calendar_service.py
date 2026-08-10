from datetime import datetime, timezone

from googleapiclient.discovery import build

from server.services.calendar_auth import get_calendar_credentials


def get_calendar_service():
    credentials = get_calendar_credentials()

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )


def get_upcoming_events(max_results=10):
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return result.get("items", [])


def search_events(query, max_results=10):
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        q=query,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return result.get("items", [])    


def create_event(
    summary,
    start_datetime,
    end_datetime,
    description=None,
    location=None,
):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Asia/Kolkata",
        },
    }

    if description:
        event["description"] = description

    if location:
        event["location"] = location

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    return created_event    
