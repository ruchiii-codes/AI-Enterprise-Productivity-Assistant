from fastapi import APIRouter, File, UploadFile, HTTPException
from server.services.document_processor import process_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

from fastapi import APIRouter, File, UploadFile, HTTPException
from server.services.document_processor import process_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    return process_document(file)