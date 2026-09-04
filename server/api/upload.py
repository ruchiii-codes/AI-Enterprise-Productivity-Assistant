from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from server.auth.database import get_db
from server.auth.dependencies import get_current_user
from server.auth.models import Document, User, Conversation
from server.services.document_processor import process_document


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...),
    conversation_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload a PDF file.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )
    
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )    

    # Process the document
    result = process_document(
        file=file,
        user_id=current_user.id,
        conversation_id=conversation_id,
    )

    # Save document ownership
    document = Document(
        filename=result["filename"],
        file_path=result["file_path"],
        user_id=current_user.id,
        page_count=result["page_count"],
        conversation_id=conversation_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return result