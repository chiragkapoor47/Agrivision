"""
TAH-015: Image Validation and Storage Utilities
Ensures uploaded leaf images are verified for format, size, and integrity.
"""
import os
import uuid
import io
from PIL import Image
from fastapi import UploadFile, HTTPException, status
from app.config import settings

def validate_and_save_leaf_image(file: UploadFile) -> tuple[str, str, bytes]:
    """
    Validates file extension, size limit, and image format.
    Saves file to settings.UPLOAD_DIR with unique name.
    Returns: (filename, relative_url, raw_bytes)
    """
    # 1. Check extension
    filename = file.filename or "leaf.jpg"
    ext = filename.split(".")[-1].lower() if "." in filename else "jpg"
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image file format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # 2. Read bytes & check size limit
    contents = file.file.read()
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image file exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB."
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty. Please select or capture a valid plant leaf image."
        )

    # 3. Verify image integrity with PIL
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
        # Re-open after verify() to inspect size
        img = Image.open(io.BytesIO(contents))
        width, height = img.size
        if width < 50 or height < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image resolution is too low (<50x50px) for computer vision disease classification."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted image data. Error: {str(e)}"
        )

    # 4. Save unique file
    unique_filename = f"leaf_{uuid.uuid4().hex[:12]}.{ext if ext in ['jpg', 'png', 'webp'] else 'jpg'}"
    dest_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    with open(dest_path, "wb") as f:
        f.write(contents)

    relative_url = f"/uploads/{unique_filename}"
    return unique_filename, relative_url, contents
