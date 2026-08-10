import re


def extract_issue_title(query: str):
    """
    Extracts the issue title from a user's query.
    """

    patterns = [
        r'titled\s+"([^"]+)"',
        r"title\s+\"([^\"]+)\"",
        r'titled\s+\'([^\']+)\'',
        r"title\s+\'([^\']+)\'",
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None