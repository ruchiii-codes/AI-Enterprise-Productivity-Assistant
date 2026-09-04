from sqlalchemy.orm import Session

from server.auth.models import Message


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
    sources=None,
):
    """
    Store a message in a conversation.
    """

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        sources=sources or [],
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

def get_messages(
    db: Session,
    conversation_id: int,
):
    """
    Return all messages in a conversation.
    """

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at)
        .all()
    )


def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 6,
):
    """
    Return the most recent messages.
    """

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    return list(reversed(messages))