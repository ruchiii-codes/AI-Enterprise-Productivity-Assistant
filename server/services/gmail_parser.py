import re


def extract_gmail_search_query(query: str):
    """
    Converts natural language Gmail searches
    into Gmail search syntax.
    """

    # Emails from a person/company/domain
    match = re.search(
        r"emails? from (.+)",
        query,
        re.IGNORECASE,
    )

    if match:
        value = match.group(1).strip()

        if "@" in value:
            return f"from:{value}"

        return f"from:{value}"

    # Emails about a topic
    match = re.search(
        r"emails? about (.+)",
        query,
        re.IGNORECASE,
    )

    if match:
        value = match.group(1).strip()

        return f"subject:{value}"

    # Search emails for a topic
    match = re.search(
        r"(?:search|find) emails? (?:for|about) (.+)",
        query,
        re.IGNORECASE,
    )

    if match:
        value = match.group(1).strip()

        return value

    return None


def extract_message_id(query: str):
    match = re.search(
        r"message id[:\s]+([a-zA-Z0-9_-]+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_email_recipient(query: str):
    match = re.search(
        r"(?:to|send to)\s+([^\s]+@[^\s]+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_message_id(query: str):
    """
    Extracts a Gmail message ID when explicitly provided.
    """

    match = re.search(
        r"message id[:\s]+([a-zA-Z0-9_-]+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_email_recipient(query: str):
    """
    Extracts an email recipient.
    """

    match = re.search(
        r"(?:to|send to)\s+([^\s]+@[^\s]+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None