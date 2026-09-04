from server.services.integrations.gmail.gmail_service import (
    get_profile,
    list_messages,
    search_messages,
    get_message,
    send_email,
)
from server.services.integrations.gmail.gmail_formatter import (
    format_message,
    format_messages,
)
from server.services.summarization_service import summarize_gmail_message

def gmail_get_profile(user_id: int):
    return get_profile(user_id)

def gmail_list_messages(user_id: int, max_results=10):
    messages = list_messages(user_id=user_id, max_results=max_results)

    if not messages:
        return "No emails found."

    return format_messages(messages)


def gmail_get_latest_message(user_id: int):
    messages = list_messages(user_id=user_id, max_results=1)

    if not messages:
        return "No emails found."

    return format_message(messages[0])

def gmail_search_messages(user_id: int, query: str, max_results=10):
    messages = search_messages(
        user_id=user_id,
        query=query,
        max_results=max_results,
    )

    if not messages:
        return "No matching emails found."

    return format_messages(messages)

def gmail_search_and_summarize(
    user_id: int,
    query: str,
    max_results=10,
):
    messages = search_messages(
        user_id=user_id,
        query=query,
        max_results=max_results,
    )

    if not messages:
        return "No matching emails found."

    summaries = []

    for message in messages:
        try:
            full_message = gmail_get_message(
                user_id=user_id,
                message_id=message["id"],
            )

            summary = summarize_gmail_message(full_message)

            summaries.append(
                {
                    "from": message.get("from"),
                    "subject": message.get("subject"),
                    "date": message.get("date"),
                    "summary": summary,
                }
            )

        except Exception as error:
            summaries.append(
                {
                    "from": message.get("from"),
                    "subject": message.get("subject"),
                    "date": message.get("date"),
                    "summary": "Unable to summarize this email.",
                }
            )

    output = "## 📧 Email Summary\n\n"

    for index, item in enumerate(summaries, start=1):
        output += f"### {index}. {item.get('subject') or 'No Subject'}\n\n"
        output += f"**From:** {item.get('from') or 'Unknown'}\n\n"
        output += f"**Date:** {item.get('date') or 'Unknown'}\n\n"
        output += f"**Summary:** {item.get('summary')}\n\n"

    return output

def gmail_get_message(user_id: int, message_id: str):
    return get_message(user_id=user_id, message_id=message_id)


def gmail_send_email(user_id: int, to: str, subject: str, body: str):
    return send_email(
        user_id=user_id,
        to=to,
        subject=subject,
        body=body,
    )

def gmail_summarize_message(user_id: int, message_id: str):
    message = gmail_get_message(user_id=user_id, message_id=message_id)

    return summarize_gmail_message(message)

def gmail_summarize_latest_email(user_id: int):
    messages = list_messages(
        user_id=user_id,
        max_results=1,
    )

    if not messages:
        return "No emails found."

    message_id = messages[0]["id"]

    return gmail_summarize_message(
        user_id=user_id,
        message_id=message_id,
    )