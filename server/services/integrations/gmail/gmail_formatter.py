import re


def redact_sensitive_content(text):
    if not text:
        return text

    # Redact WorkMind email verification tokens
    text = re.sub(
        r'([?&]token=)[A-Za-z0-9_-]+',
        r'\1[REDACTED]',
        text,
        flags=re.IGNORECASE,
    )

    return text



def format_messages(messages):
    if not messages:
        return "No emails found."

    response = f"Found {len(messages)} email(s):\n\n"

    for message in messages:
        response += (
            f"From: {message.get('from', 'Unknown')}\n"
            f"Subject: {message.get('subject') or 'No Subject'}\n"
            f"Date: {message.get('date', 'Unknown')}\n"
            f"Snippet: {redact_sensitive_content(message.get('snippet', ''))}\n\n"
        )

    return response.strip()


def format_message(message):
    return (
        f"From: {message.get('from', 'Unknown')}\n"
        f"To: {message.get('to', 'Unknown')}\n"
        f"Subject: {message.get('subject') or 'No Subject'}\n"
        f"Date: {message.get('date', 'Unknown')}\n\n"
        f"{redact_sensitive_content(message.get('body', ''))}"
    )


