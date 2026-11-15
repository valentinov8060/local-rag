#!/usr/bin/env python3
"""
PDF Text Ingestion and Normalization Script for Local RAG.

Accepts a PDF file, extracts text page by page using pdfplumber,
normalizes excessive whitespace, and writes the result to a text file.
"""

import argparse
import os
import re
import sys
import pdfplumber

def normalize_text(text: str) -> str:
    """Normalize whitespace, remove repeated spaces, and clean up blank lines."""
    if not text:
        return ""
    
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    lines = text.split("\n")
    normalized_lines = []
    
    for line in lines:
        # Strip leading/trailing whitespace from each line
        stripped = line.strip()
        if not stripped:
            normalized_lines.append("")
        else:
            # Replace multiple consecutive spaces or tabs with a single space
            cleaned_line = re.sub(r'[ \t]+', ' ', stripped)
            normalized_lines.append(cleaned_line)
            
    # Collapse excessive consecutive blank lines into a single blank line
    result_lines = []
    blank_count = 0
    for line in normalized_lines:
        if line == "":
            blank_count += 1
            if blank_count <= 1:
                result_lines.append("")
        else:
            blank_count = 0
            result_lines.append(line)
            
    # Strip leading/trailing blank lines from the entire text
    while result_lines and result_lines[0] == "":
        result_lines.pop(0)
    while result_lines and result_lines[-1] == "":
        result_lines.pop()
        
    return "\n".join(result_lines)


def extract_pdf_text(pdf_path: str) -> str:
    """Open a PDF file, extract text from each page in order, and return normalized text."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    pages_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                    else:
                        pages_text.append("")
                except Exception as e:
                    print(f"Warning: Could not extract text from page {i+1}: {e}", file=sys.stderr)
                    pages_text.append("")
    except Exception as e:
        raise RuntimeError(f"Failed to process PDF file {pdf_path}: {e}")
        
    combined_text = "\n\n".join(pages_text)
    return normalize_text(combined_text)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and normalize text from a PDF file for local RAG."
    )
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument(
        "-o", "--output",
        help="Path to the output text file (default: <pdf_filename>.txt)"
    )
    
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    if args.output:
        output_path = args.output
    else:
        base, _ = os.path.splitext(pdf_path)
        output_path = f"{base}.txt"
        
    try:
        print(f"Extracting text from {pdf_path}...")
        extracted_text = extract_pdf_text(pdf_path)
        
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
            
        print(f"Successfully extracted and normalized text to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
