from server.config import settings

UPLOAD_FOLDER = settings.UPLOAD_DIR


def count_uploaded_pdfs() -> int:

    pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))

    return len(pdf_files)
