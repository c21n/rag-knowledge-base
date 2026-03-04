"""Document loaders for parsing different file formats.

This module provides functions to extract text from various document formats:
- PDF files using PyPDF2
- Word documents using python-docx
- Markdown files
- Plain text files

Each loader handles encoding errors gracefully and returns clean text content.
"""

import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text_parts = []
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        text = "\n\n".join(text_parts)
        return _clean_text(text)
    except Exception as e:
        logger.warning(f"Failed to parse PDF {file_path}: {e}")
        return ""


def load_docx(file_path: str) -> str:
    """Extract text from a Word document (.docx)."""
    try:
        from docx import Document
        doc = Document(file_path)
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text.strip())
        text = "\n\n".join(text_parts)
        return _clean_text(text)
    except Exception as e:
        logger.warning(f"Failed to parse DOCX {file_path}: {e}")
        return ""


def load_markdown(file_path: str) -> str:
    """Read and return markdown file content."""
    return _load_text_file(file_path)


def load_txt(file_path: str) -> str:
    """Read plain text file content."""
    return _load_text_file(file_path)


def _load_text_file(file_path: str) -> str:
    """Load a text file with encoding fallback."""
    encodings = ["utf-8", "latin-1"]
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                return _clean_text(content)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return ""
    return ""


def _clean_text(text: str) -> str:
    """Clean extracted text by removing excessive whitespace."""
    if not text:
        return ""
    text = text.strip()
    text = text.replace('\t', ' ')
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def get_loader(file_extension: str) -> Optional[callable]:
    """Return the appropriate loader function for a file extension."""
    loaders = {
        '.pdf': load_pdf,
        '.docx': load_docx,
        '.md': load_markdown,
        '.txt': load_txt,
    }
    ext_lower = file_extension.lower()
    loader = loaders.get(ext_lower)
    if loader is None:
        logger.warning(f"No loader available for extension: {file_extension}")
    return loader


def load_document(file_path: str) -> str:
    """Load a document using the appropriate loader based on extension."""
    ext = Path(file_path).suffix.lower()
    loader = get_loader(ext)
    if loader is None:
        logger.warning(f"Unsupported file format: {file_path}")
        return ""
    return loader(file_path)
