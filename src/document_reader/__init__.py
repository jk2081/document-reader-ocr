"""Document Reader - OCR package for PDF processing using PaddleOCR 3."""

from .ocr_reader import OCRReader, extract_text_from_pdf

__version__ = "0.1.0"
__all__ = ["OCRReader", "extract_text_from_pdf"]