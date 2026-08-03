from collections import deque

MAX_HISTORY = 6

conversation_history = deque(maxlen=MAX_HISTORY)


def add_message(role: str, content: str):

    conversation_history.append(
        {
            "role": role,
            "content": content,
        }
    )


def get_conversation():

    return list(conversation_history)


def clear_memory():

    conversation_history.clear()


import json
from pathlib import Path


MEMORY_FILE = Path("data/memory/conversation.json")


def save_memory():

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            list(conversation_history),
            f,
            ensure_ascii=False,
            indent=4,
        )


def load_memory():

    if not MEMORY_FILE.exists():
        return

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)

        conversation_history.clear()
        conversation_history.extend(messages)

    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to load memory: {e}")

        conversation_history.clear()