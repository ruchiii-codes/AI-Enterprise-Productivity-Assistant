from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User
from server.services.conversation_service import (
    create_conversation,
    get_user_conversations,
    delete_conversation,
    toggle_pin_conversation,
    search_user_conversations,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/")
def new_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    conversation = create_conversation(
        db=db,
        user_id=current_user.id,
    )

    return conversation


@router.get("/")
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return get_user_conversations(
        db=db,
        user_id=current_user.id,
    )

@router.get("/search")
def search_conversations(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return search_user_conversations(
        db=db,
        user_id=current_user.id,
        query=q,
    )

@router.delete("/{conversation_id}")
def remove_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if deleted is None:
        return {
            "message": "Conversation not found."
        }

    return {
        "message": "Conversation deleted successfully."
    }  

@router.put("/{conversation_id}/pin")
def pin_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = toggle_pin_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        return {
            "message": "Conversation not found."
        }

    return {
        "message": "Conversation pin status updated.",
        "is_pinned": conversation.is_pinned,
        "pinned_at": conversation.pinned_at,
    }    