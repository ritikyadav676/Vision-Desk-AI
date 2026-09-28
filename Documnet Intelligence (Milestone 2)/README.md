# VisionDesk AI - Document Processing

This project provides a PDF document-processing foundation for VisionDesk AI.

## Project structure

```text
visiondesk_ai/
├── data/
│   └── safety_manual.pdf
├── src/
│   └── documents/
│       ├── __init__.py
│       ├── metadata.py
│       ├── text_cleaner.py
│       ├── document_loader.py
│       └── chunker.py
├── test_documents.py
├── requirements.txt
└── README.md
```

## What it does

1. Loads a PDF using `pypdf`.
2. Extracts text page-by-page.
3. Cleans PDF extraction whitespace.
4. Extracts basic PDF/file metadata.
5. Splits text into overlapping word chunks.

## Run

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python test_documents.py
```

The included PDF is the supplied VisionDesk AI workplace safety manual.
