import re


def extract_repository_name(query: str):
    """
    Extracts the repository name from the user's query.
    """

    query = query.strip()

    patterns = [
        r"repository details of (.+)",
        r"details of (.+)",
        r"issues for (.+)",
        r"pull requests for (.+)",
        r"repository (.+)",

        r"create an issue in (.+?) titled",
        r"create issue in (.+?) titled",
        r"open an issue in (.+?) titled",
        r"open issue in (.+?) titled",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query,
            re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

    return None