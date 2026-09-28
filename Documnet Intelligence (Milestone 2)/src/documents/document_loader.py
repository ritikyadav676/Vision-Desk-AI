"""PDF document loading and text extraction."""

from pathlib import Path
from typing import Dict, List
from pypdf import PdfReader
from .text_cleaner import clean_text


def load_document(pdf_path: str) -> Dict[str, object]:
    """Load a PDF and return cleaned text page-by-page plus combined text."""
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The document loader currently supports PDF files only.")

    reader = PdfReader(str(path))
    pages: List[Dict[str, object]] = []

    for page_number, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        text = clean_text(raw_text)

        pages.append({
            "page_number": page_number,
            "text": text,
            "character_count": len(text),
        })

    combined_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages if page["text"]
    )

    return {
        "file_name": path.name,
        "page_count": len(reader.pages),
        "pages": pages,
        "text": combined_text,
    }
