"""Chat endpoint.

Thin transport layer: authenticate, hand off to the chat service, return the
result. The orchestration lives in server/services/agents/chat_service.py.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from server.auth.dependencies import get_current_user
from server.db.base import get_db
from server.db.models import User
from server.schemas.chat import ChatRequest
from server.services.agents.chat_service import handle_chat
from server.utils.rate_limiter import limiter

# No prefix: the path stays exactly "/chat", as the frontend calls it.
router = APIRouter(tags=["Chat"])


@router.post("/chat")
@limiter.limit("30/minute")
def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # `request` is unused here but required: slowapi reads it to identify
    # the caller for rate limiting.
    return handle_chat(
        db=db,
        current_user=current_user,
        chat_request=chat_request,
    )
