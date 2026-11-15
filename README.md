# Local RAG

A lightweight local Retrieval-Augmented Generation (RAG) project setup for processing and ingesting documents.

## Purpose

This project provides utilities to extract text from PDF documents, normalize whitespace, and prepare clean text suitable for embedding and downstream RAG tasks.

## Requirements

- **Python**: Python 3.8 or higher (Python 3.12+ recommended).
- **Dependencies**: Listed in `requirements.txt` (primarily `pdfplumber` for PDF parsing).

## Setup Instructions

### 1. Create a Virtual Environment

Open a terminal in the project root and run:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux / Git Bash**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

To extract and normalize text from a PDF file, run the `ingest.py` script:

```bash
python ingest.py path/to/document.pdf
```

### Options

- `-o`, `--output`: Specify a custom path for the output text file. If omitted, the script automatically writes the normalized text to a `.txt` file with the same base name as the input PDF (e.g., `document.txt`).

## Running Tests

To run the test suite using `pytest`:

```bash
python -m pytest
```
