import re
import shutil
import uuid
from pathlib import PurePosixPath, PureWindowsPath

from server.config import settings

# Upload folder
UPLOAD_FOLDER = settings.UPLOAD_DIR

# Anything outside this set is replaced, so a name can never carry a path
# separator, a drive letter or a parent-directory reference. \w keeps letters
# from any alphabet, so a non-English filename survives intact.
_UNSAFE_CHARS = re.compile(r"[^\w.-]")


def safe_display_name(raw_name):
    """
    Reduce an uploaded file's name to something safe to store and display.

    Both path flavours are applied because the name arrives in a multipart
    header the client writes by hand: a browser sends a bare name, an attacker
    sends whichever separator the server might honour.
    """

    candidate = PureWindowsPath(PurePosixPath(raw_name or "").name).name
    candidate = _UNSAFE_CHARS.sub("_", candidate).lstrip(".")

    return candidate[:120] or "document.pdf"


def save_uploaded_file(file, user_id):
    """
    Save an uploaded PDF and return (path on disk, name to show the user).
    """

    # Create upload folder if it doesn't exist
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    display_name = safe_display_name(file.filename)

    # The name on disk is generated, never client text. file.filename comes
    # from an attacker-controlled header, and joining it onto a directory lets
    # "../../server/main.py" overwrite application code, since the container
    # runs as the user that owns /app. The uuid also ends the silent
    # collisions that let one user's "report.pdf" replace another's.
    destination = UPLOAD_FOLDER / f"u{user_id}_{uuid.uuid4().hex}_{display_name}"

    # Defence in depth: refuse to write anywhere but the uploads directory,
    # whatever the sanitising above might have missed.
    if destination.resolve().parent != UPLOAD_FOLDER.resolve():
        raise ValueError("Refusing to write outside the upload directory.")

    # Save file
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination, display_name
