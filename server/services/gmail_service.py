from googleapiclient.discovery import build

from server.services.gmail_auth import get_gmail_credentials

from email.mime.text import MIMEText
import base64

def get_gmail_service():
    """
    Creates and returns an authenticated Gmail API service.
    """

    credentials = get_gmail_credentials()

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )


def get_profile():
    """
    Returns the authenticated Gmail user's profile.
    """

    service = get_gmail_service()

    profile = (
        service.users()
        .getProfile(userId="me")
        .execute()
    )

    return {
        "email": profile["emailAddress"],
        "messages_total": profile["messagesTotal"],
        "threads_total": profile["threadsTotal"],
    }


def list_messages(max_results=10):
    """
    Returns recent Gmail messages.
    """

    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
        )
        .execute()
    )

    messages = response.get("messages", [])

    results = []

    for message in messages:
        message_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = message_data.get(
            "payload",
            {}
        ).get(
            "headers",
            []
        )

        header_dict = {
            header["name"]: header["value"]
            for header in headers
        }

        results.append(
            {
                "id": message_data["id"],
                "thread_id": message_data["threadId"],
                "from": header_dict.get("From"),
                "to": header_dict.get("To"),
                "subject": header_dict.get("Subject"),
                "date": header_dict.get("Date"),
                "snippet": message_data.get("snippet"),
            }
        )

    return results


def search_messages(query: str, max_results=10):
    """
    Searches Gmail using Gmail search syntax.
    """

    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=max_results,
        )
        .execute()
    )

    messages = response.get("messages", [])

    results = []

    for message in messages:
        message_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = message_data.get(
            "payload",
            {}
        ).get(
            "headers",
            []
        )

        header_dict = {
            header["name"]: header["value"]
            for header in headers
        }

        results.append(
            {
                "id": message_data["id"],
                "thread_id": message_data["threadId"],
                "from": header_dict.get("From"),
                "to": header_dict.get("To"),
                "subject": header_dict.get("Subject"),
                "date": header_dict.get("Date"),
                "snippet": message_data.get("snippet"),
            }
        )

    return results    


import base64


def extract_message_body(payload):
    """
    Extracts readable text from a Gmail message payload.
    """

    if "body" in payload and payload["body"].get("data"):
        data = payload["body"]["data"]

        return base64.urlsafe_b64decode(
            data
        ).decode(
            "utf-8",
            errors="ignore",
        )

    for part in payload.get("parts", []):
        body = extract_message_body(part)

        if body:
            return body

    return ""


def get_message(message_id: str):
    """
    Returns the full content of a Gmail message.
    """

    service = get_gmail_service()

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )

    headers = message.get(
        "payload",
        {}
    ).get(
        "headers",
        []
    )

    header_dict = {
        header["name"]: header["value"]
        for header in headers
    }

    payload = message.get("payload", {})

    body = extract_message_body(payload)

    return {
        "id": message["id"],
        "thread_id": message["threadId"],
        "from": header_dict.get("From"),
        "to": header_dict.get("To"),
        "subject": header_dict.get("Subject"),
        "date": header_dict.get("Date"),
        "body": body,
    }    


def send_email(to: str, subject: str, body: str):
    """
    Sends an email through Gmail.
    """

    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = (
        service.users()
        .messages()
        .send(
            userId="me",
            body={
                "raw": encoded_message
            },
        )
        .execute()
    )

    return {
        "id": result["id"],
        "thread_id": result.get("threadId"),
    }