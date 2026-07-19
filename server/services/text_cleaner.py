import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    # Remove form feed characters
    text = text.replace("\f", "\n")

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace 3 or more newlines with exactly 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text