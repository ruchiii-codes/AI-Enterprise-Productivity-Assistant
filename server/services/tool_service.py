from pathlib import Path


UPLOAD_FOLDER = Path("data/uploads")


def count_uploaded_pdfs() -> int:

    pdf_files = list(UPLOAD_FOLDER.glob("*.pdf"))

    return len(pdf_files)