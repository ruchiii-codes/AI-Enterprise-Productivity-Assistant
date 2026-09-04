from datetime import datetime, timezone, timedelta

from googleapiclient.discovery import build

from server.auth.database import SessionLocal
from server.auth.models import CalendarConnection
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from server.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

def get_calendar_service(user_id):
    db = SessionLocal()

    try:
        connection = (
            db.query(CalendarConnection)
            .filter(CalendarConnection.user_id == user_id)
            .first()
        )

        if not connection:
            raise ValueError(
                "Google Calendar is not connected for this user."
            )

        credentials = Credentials(
            token=connection.access_token,
            refresh_token=connection.refresh_token,
            token_uri=connection.token_uri,
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scopes=[
                "https://www.googleapis.com/auth/calendar"
            ],
        )

        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

            connection.access_token = credentials.token
            db.commit()

        return build(
            "calendar",
            "v3",
            credentials=credentials,
        )

    finally:
        db.close()


def get_upcoming_events(user_id, max_results=10):
    service = get_calendar_service(user_id)

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return result.get("items", [])

def get_tomorrow_events(user_id, max_results=10):
    service = get_calendar_service(user_id)

    india_timezone = timezone(timedelta(hours=5, minutes=30))

    tomorrow = datetime.now(india_timezone).date() + timedelta(days=1)

    start_of_tomorrow = datetime.combine(
        tomorrow,
        datetime.min.time(),
        tzinfo=india_timezone,
    )

    start_of_day_after = start_of_tomorrow + timedelta(days=1)

    result = service.events().list(
        calendarId="primary",
        timeMin=start_of_tomorrow.isoformat(),
        timeMax=start_of_day_after.isoformat(),
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return result.get("items", [])

def search_events(user_id, query, max_results=10):
    service = get_calendar_service(user_id)

    now = datetime.now(timezone.utc).isoformat()

    result = service.events().list(
    
    
        calendarId="primary",
    
    
        q=query,
    
    
        maxResults=max_results,
    
    
        singleEvents=True,
    
    
        orderBy="startTime",
    
    
    ).execute()

    return result.get("items", [])    


def create_event(
    user_id,
    summary,
    start_datetime,
    end_datetime,
    description=None,
    location=None,
):
    service = get_calendar_service(user_id)

    def normalize_datetime(value):
        if not value:
            raise ValueError("Event date/time is required.")

        value = value.strip()

        # Already ISO/RFC3339 format
        if "T" in value:
            if "+" in value or value.endswith("Z"):
                return value

            # ISO datetime without timezone
            return value + "+05:30"

        # Convert "YYYY-MM-DD HH:MM"
        try:
            dt = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M"
            )

            return dt.strftime(
                "%Y-%m-%dT%H:%M:%S+05:30"
            )

        except ValueError:
            raise ValueError(
                f"Invalid datetime format: {value}. "
                "Expected YYYY-MM-DD HH:MM."
            )

    start_datetime = normalize_datetime(start_datetime)
    end_datetime = normalize_datetime(end_datetime)

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