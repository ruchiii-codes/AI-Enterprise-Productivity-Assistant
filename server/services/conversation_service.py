from sqlalchemy.orm import Session

from server.auth.models import Conversation

from datetime import datetime

def create_conversation(
    db: Session,
    user_id: int,
    title: str = "New Conversation",
):
    """
    Create a new conversation.
    """

    conversation = Conversation(
        title=title,
        user_id=user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
):
    """
    Return a conversation owned by the user.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )


def get_user_conversations(
    db: Session,
    user_id: int,
):
    """
    Return all conversations of a user with message counts.
    """

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.is_pinned.desc(),
            Conversation.pinned_at.asc(),
            Conversation.id.asc(),
        )
        .all()
    )

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "user_id": conversation.user_id,
            "message_count": len(conversation.messages),
            "is_pinned": conversation.is_pinned,
            "pinned_at": conversation.pinned_at,
        }
        for conversation in conversations
    ]

def update_conversation_title(
    db: Session,
    conversation_id: int,
    user_id: int,
    title: str,
):
    """
    Update the title of a conversation owned by the user.
    """

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if conversation is None:
        return None

    conversation.title = title.strip()

    db.commit()
    db.refresh(conversation)

    return conversation

def delete_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
):
    """
    Delete a conversation owned by the user.
    """

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if conversation is None:
        return None

    db.delete(conversation)
    db.commit()

    return True    

def toggle_pin_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
):
    """
    Toggle the pinned status of a conversation owned by the user.
    """

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if conversation is None:
        return None

    if conversation.is_pinned:
        conversation.is_pinned = False
        conversation.pinned_at = None
    else:
        conversation.is_pinned = True
        conversation.pinned_at = datetime.utcnow()
    
    db.commit()
    db.refresh(conversation)

    return conversation    

def search_user_conversations(
    db: Session,
    user_id: int,
    query: str,
):
    """
    Search a user's conversations by title or message content.
    """

    search_term = query.strip()

    if not search_term:
        return []

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .all()
    )

    results = []

    for conversation in conversations:
        title = conversation.title or ""

        title_match = search_term.lower() in title.lower()

        matching_message = None

        if not title_match:
            for message in conversation.messages:
                if search_term.lower() in (message.content or "").lower():
                    matching_message = message
                    break

        if title_match or matching_message:
            result = {
                "id": conversation.id,
                "title": title or "New Conversation",
                "is_pinned": conversation.is_pinned,
                "pinned_at": conversation.pinned_at,
            }

            if matching_message:
                content = matching_message.content or ""
                index = content.lower().find(search_term.lower())

                start = max(0, index - 60)
                end = min(len(content), index + len(search_term) + 100)

                snippet = content[start:end].strip()

                if start > 0:
                    snippet = "..." + snippet

                if end < len(content):
                    snippet += "..."

                result["snippet"] = snippet
            else:
                result["snippet"] = ""

            results.append(result)

    return results