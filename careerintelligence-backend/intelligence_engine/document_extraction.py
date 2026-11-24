from pathlib import Path

from docx import Document
from pypdf import PdfReader


MAX_EXTRACTED_CHARACTERS = 100_000


def _limit_text(text):
    """Limit extracted text to prevent excessively large database records."""
    text = text.strip()
    truncated = len(text) > MAX_EXTRACTED_CHARACTERS

    if truncated:
        text = text[:MAX_EXTRACTED_CHARACTERS]

    return text, truncated


def _extract_pdf(file_path):
    """Extract text and metadata from a PDF document."""
    reader = PdfReader(str(file_path))

    if reader.is_encrypted:
        raise ValueError("Encrypted PDF documents are not supported.")

    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    full_text = "\n\n".join(pages).strip()
    full_text, truncated = _limit_text(full_text)

    metadata = {}
    if reader.metadata:
        for key, value in reader.metadata.items():
            if value is not None:
                metadata[str(key)] = str(value)[:500]

    return {
        "format": "pdf",
        "page_count": len(reader.pages),
        "text": full_text,
        "character_count": len(full_text),
        "truncated": truncated,
        "is_empty": not bool(full_text),
        "requires_ocr": not bool(full_text),
        "metadata": metadata,
    }


def _extract_docx(file_path):
    """Extract paragraphs and tables from a Microsoft Word document."""
    document = Document(str(file_path))

    text_parts = []

    # Extract paragraphs.
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            text_parts.append(text)

    # Extract text from tables, which often contain CV information.
    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if cells:
                text_parts.append(" | ".join(cells))

    full_text = "\n".join(text_parts).strip()
    full_text, truncated = _limit_text(full_text)

    properties = document.core_properties

    metadata = {}
    if properties.title:
        metadata["title"] = properties.title[:500]

    if properties.author:
        metadata["author"] = properties.author[:500]

    if properties.subject:
        metadata["subject"] = properties.subject[:500]

    return {
        "format": "docx",
        "paragraph_count": len(document.paragraphs),
        "table_count": len(document.tables),
        "text": full_text,
        "character_count": len(full_text),
        "truncated": truncated,
        "is_empty": not bool(full_text),
        "requires_ocr": False,
        "metadata": metadata,
    }


def extract_document(file_path):
    """
    Extract text from supported document types.

    Supported:
        PDF (.pdf)
        Microsoft Word (.docx)

    Returns a dictionary containing the extracted text and metadata.
    """
    file_path = Path(file_path)

    if not file_path.exists() or not file_path.is_file():
        raise ValueError("The document file could not be found.")

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return _extract_pdf(file_path)

    if extension == ".docx":
        return _extract_docx(file_path)

    raise ValueError("Unsupported document format.")