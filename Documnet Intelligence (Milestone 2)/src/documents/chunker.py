"""Simple word-based text chunking utilities."""

from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 200,
    overlap: int = 40
) -> List[str]:
    """Split text into overlapping word chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    words = text.split()

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size]).strip()

        if chunk:
            chunks.append(chunk)

        if start + chunk_size >= len(words):
            break

    return chunks
