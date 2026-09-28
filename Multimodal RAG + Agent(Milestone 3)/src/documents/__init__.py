# src/documents/__init__.py
# Import the modules without referencing names that do not exist in this project.
# This keeps the package importable while allowing direct module imports such as:
# from src.documents.document_loader import load_document

__all__ = [
    "document_loader",
    "text_cleaner",
    "chunker",
    "metadata",
]
