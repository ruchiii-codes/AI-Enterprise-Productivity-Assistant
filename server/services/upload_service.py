from pathlib import Path
import shutil

# Upload folder
UPLOAD_FOLDER = Path("data/uploads")


def save_uploaded_file(file):
    """
    Save uploaded PDF file to the uploads directory.
    """

    # Create upload folder if it doesn't exist
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    # Destination path
    destination = UPLOAD_FOLDER / file.filename

    # Save file
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination