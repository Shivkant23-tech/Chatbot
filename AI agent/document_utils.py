import os
import re
import zipfile
from pathlib import Path


def extract_text_from_upload(file_storage) -> str:
    filename = (file_storage.filename or "").lower()
    temp_path = Path(file_storage.filename or "upload.tmp")
    file_storage.save(temp_path)

    try:
        if filename.endswith(".pdf"):
            try:
                import PyPDF2
            except ImportError:
                return ""
            reader = PyPDF2.PdfReader(str(temp_path))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)

        if filename.endswith(".docx"):
            try:
                import docx
            except ImportError:
                return ""
            document = docx.Document(str(temp_path))
            return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)

        return ""
    finally:
        if temp_path.exists():
            temp_path.unlink()


def build_context_with_document(message: str, document_text: str) -> str:
    if not document_text:
        return message
    cleaned = re.sub(r"\s+", " ", document_text).strip()
    if not cleaned:
        return message
    return f"Document content:\n{cleaned}\n\nUser question:\n{message}"
