from server.services.gmail_service import (
    get_profile,
    list_messages,
    search_messages,
    get_message,
    send_email,
)


def gmail_get_profile():
    return get_profile()


def gmail_list_messages(max_results=10):
    return list_messages(max_results=max_results)


def gmail_search_messages(query, max_results=10):
    return search_messages(
        query=query,
        max_results=max_results,
    )


def gmail_get_message(message_id):
    return get_message(message_id)


def gmail_send_email(to, subject, body):
    return send_email(
        to=to,
        subject=subject,
        body=body,
    )