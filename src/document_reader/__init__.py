"""Document Reader - OCR package for PDF processing using EasyOCR with enhancement."""

from .ocr_reader import OCRReader, extract_text_from_pdf, extract_text_with_confidence
from .image_enhancer import ImageEnhancer

__version__ = "0.3.0"
__all__ = ["OCRReader", "extract_text_from_pdf", "extract_text_with_confidence", "ImageEnhancer"]