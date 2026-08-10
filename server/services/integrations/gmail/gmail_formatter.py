def format_profile(profile):
    return (
        f"Gmail Account: {profile['email']}\n"
        f"Total Messages: {profile['messages_total']}\n"
        f"Total Threads: {profile['threads_total']}"
    )


def format_messages(messages):
    if not messages:
        return "No emails found."

    response = f"Found {len(messages)} email(s):\n\n"

    for message in messages:
        response += (
            f"From: {message.get('from', 'Unknown')}\n"
            f"Subject: {message.get('subject') or 'No Subject'}\n"
            f"Date: {message.get('date', 'Unknown')}\n"
            f"Snippet: {message.get('snippet', '')}\n\n"
        )

    return response.strip()


def format_message(message):
    return (
        f"From: {message.get('from', 'Unknown')}\n"
        f"To: {message.get('to', 'Unknown')}\n"
        f"Subject: {message.get('subject') or 'No Subject'}\n"
        f"Date: {message.get('date', 'Unknown')}\n\n"
        f"{message.get('body', '')}"
    )


def format_sent_email(result):
    return (
        "Email sent successfully!\n\n"
        f"Message ID: {result['id']}\n"
        f"Thread ID: {result.get('thread_id', 'Unknown')}"
    )