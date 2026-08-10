import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
)

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials",
    "calendar_credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "credentials",
    "calendar_token.json"
)


def get_calendar_credentials():
    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if credentials and credentials.valid:
        return credentials

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0
        )

    with open(TOKEN_FILE, "w") as token:
        token.write(credentials.to_json())

    return credentials