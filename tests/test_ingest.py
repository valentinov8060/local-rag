import os
import pytest
from unittest.mock import MagicMock, patch
from ingest import normalize_text, extract_pdf_text


def test_normalize_text_basic():
    raw = "Hello    World!\n\n\nThis is\t a test.\r\n\r\n"
    expected = "Hello World!\n\nThis is a test."
    assert normalize_text(raw) == expected


def test_normalize_text_empty():
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_normalize_text_whitespace_only():
    assert normalize_text("   \n\n   ") == ""


def test_extract_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_pdf_text("non_existent_file.pdf")


@patch("ingest.os.path.exists", return_value=True)
@patch("ingest.pdfplumber.open")
def test_extract_pdf_text_success(mock_pdf_open, mock_exists):
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1   text."
    
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 text."
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    result = extract_pdf_text("dummy.pdf")
    assert "Page 1 text." in result
    assert "Page 2 text." in result
    assert "\n\n" in result


@patch("ingest.os.path.exists", return_value=True)
@patch("ingest.pdfplumber.open")
def test_extract_pdf_text_page_error(mock_pdf_open, mock_exists):
    mock_page1 = MagicMock()
    mock_page1.extract_text.side_effect = Exception("Extraction failed")
    
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Valid page text."
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    result = extract_pdf_text("dummy.pdf")
    assert "Valid page text." in result
