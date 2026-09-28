"""Metadata extraction utilities for PDF documents."""

from pathlib import Path
from typing import Any, Dict
from pypdf import PdfReader


def extract_metadata(pdf_path: str) -> Dict[str, Any]:
    """Extract basic file and PDF metadata."""
    path = Path(pdf_path)
    reader = PdfReader(str(path))
    pdf_metadata = reader.metadata or {}

    return {
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size,
        "page_count": len(reader.pages),
        "title": pdf_metadata.get("/Title"),
        "author": pdf_metadata.get("/Author"),
        "subject": pdf_metadata.get("/Subject"),
        "creator": pdf_metadata.get("/Creator"),
        "producer": pdf_metadata.get("/Producer"),
    }
