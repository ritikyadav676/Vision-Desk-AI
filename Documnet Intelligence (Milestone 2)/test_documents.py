"""Basic test/demo for VisionDesk AI document processing."""

from pathlib import Path

from src.documents.chunker import chunk_text
from src.documents.document_loader import load_document
from src.documents.metadata import extract_metadata
from src.documents.text_cleaner import clean_text


PDF_PATH = Path(__file__).parent / "data" / "safety_manual.pdf"


def main() -> None:
    print("=" * 60)
    print("VISIONDESK AI - DOCUMENT PROCESSING TEST")
    print("=" * 60)

    metadata = extract_metadata(str(PDF_PATH))

    print("\n[1] METADATA")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    document = load_document(str(PDF_PATH))

    print("\n[2] DOCUMENT")
    print(f"Pages loaded: {document['page_count']}")
    print(f"Extracted characters: {len(document['text'])}")

    cleaned = clean_text(document["text"])
    chunks = chunk_text(cleaned, chunk_size=80, overlap=15)

    print("\n[3] CHUNKS")
    print(f"Number of chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)

    assert metadata["page_count"] == 2
    assert "WORKPLACE SAFETY MANUAL" in cleaned
    assert len(chunks) > 0

    print("\nAll document processing checks passed.")


if __name__ == "__main__":
    main()
