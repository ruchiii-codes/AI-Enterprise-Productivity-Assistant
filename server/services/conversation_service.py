from sqlalchemy.orm import Session

from server.auth.models import Conversation


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
    Return all conversations of a user.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .all()
    )