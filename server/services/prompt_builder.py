from server.auth.models import Message


SYSTEM_PROMPT = """
You are an AI Enterprise Productivity Assistant.

Answer accurately using the conversation history and any retrieved context.

If retrieved context is provided, prioritize it.
"""


def build_messages(history, current_prompt):
    """
    Convert database messages into OpenAI chat format.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for message in history:
        messages.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": current_prompt,
        }
    )

    return messages