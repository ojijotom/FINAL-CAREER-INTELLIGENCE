"""Basic document validation before adding extraction libraries."""

from pathlib import Path


CV_EXTENSIONS = {".pdf", ".doc", ".docx"}
TRANSCRIPT_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

CV_MAX_BYTES = 5 * 1024 * 1024
TRANSCRIPT_MAX_BYTES = 10 * 1024 * 1024


def validate_document(
    filename: str,
    file_size: int,
    document_type: str,
) -> dict:
    """
    Validate document extension and size.

    This is preliminary validation only. Actual uploads must also
    validate file content, ownership and storage permissions.
    """
    extension = Path(filename).suffix.casefold()

    if document_type == "cv":
        allowed = CV_EXTENSIONS
        max_size = CV_MAX_BYTES
    elif document_type == "transcript":
        allowed = TRANSCRIPT_EXTENSIONS
        max_size = TRANSCRIPT_MAX_BYTES
    else:
        return {
            "valid": False,
            "message": "Unsupported document type.",
        }

    if extension not in allowed:
        return {
            "valid": False,
            "message": "This file extension is not supported.",
        }

    if file_size <= 0 or file_size > max_size:
        return {
            "valid": False,
            "message": "The file is empty or exceeds the size limit.",
        }

    return {
        "valid": True,
        "message": "Basic document validation passed.",
        "document_type": document_type,
        "extension": extension,
        "size_bytes": file_size,
    }
