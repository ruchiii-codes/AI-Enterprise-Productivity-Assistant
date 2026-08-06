from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User
from server.services.conversation_service import (
    create_conversation,
    get_user_conversations,
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