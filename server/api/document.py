from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import Document, User


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/")
def get_documents(
    conversation_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
    )

    if conversation_id is not None:
        query = query.filter(
            Document.conversation_id == conversation_id
        )

    documents = (
        query
        .order_by(Document.id.desc())
        .all()
    )

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "created_at": document.created_at,
            "page_count": document.page_count,
            "conversation_id": document.conversation_id,
        }
        for document in documents
    ]