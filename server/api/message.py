from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import User
from server.services.message_service import (
    get_messages,
)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/{conversation_id}")
def conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_messages(
        db=db,
        conversation_id=conversation_id,
    )