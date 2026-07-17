from fastapi import APIRouter, File, UploadFile, HTTPException

from server.services.upload_service import save_uploaded_file

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

    filename = save_uploaded_file(file)

    return {
        "message": "File uploaded successfully.",
        "filename": filename
    }