"""OCR Reader for PDF documents using EasyOCR."""

import logging
import io
from pathlib import Path
from typing import List, Optional, Tuple, Union

import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import easyocr
import os

class OCRReader:
    """OCR reader for extracting text from PDF documents using EasyOCR and PyMuPDF."""
    def __init__(
        self,
        language: str = 'en',
        image_resolution_scale: float = 2.0,
        image_quality: int = 80,
        confidence_threshold: float = 0.3,
    ):
        self.language = language
        self.image_resolution_scale = image_resolution_scale
        self.image_quality = image_quality
        self.confidence_threshold = confidence_threshold
        self._ocr = None
        self.logger = logging.getLogger(__name__)
        # Removed use_gpu logic

    def _get_ocr_instance(self) -> easyocr.Reader:
        if self._ocr is None:
            self.logger.info("Initializing EasyOCR (one-time setup)...")
            self._ocr = easyocr.Reader([self.language])
        return self._ocr

    def _pdf_to_images(self, pdf_path: Union[str, Path]) -> List[np.ndarray]:
        doc = fitz.open(str(pdf_path))
        images = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            mat = fitz.Matrix(self.image_resolution_scale, self.image_resolution_scale)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("jpeg", jpg_quality=self.image_quality)
            img = Image.open(io.BytesIO(img_data))
            images.append(np.array(img))
        doc.close()
        return images

    def process_pdf(
        self,
        pdf_path: Union[str, Path],
        page_range: Optional[Tuple[int, int]] = None,
    ) -> str:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        images = self._pdf_to_images(pdf_path)
        if page_range:
            start_page, end_page = page_range
            start_page = max(0, start_page - 1)
            end_page = min(len(images), end_page)
            images = images[start_page:end_page]
        ocr = self._get_ocr_instance()
        all_text = []
        for page_num, img in enumerate(images):
            result = ocr.readtext(img)
            page_text = []
            if result:
                for detection in result:
                    bbox, text, score = detection
                    if score > self.confidence_threshold:
                        page_text.append(text)
            if page_text:
                all_text.append(f"\n--- Page {page_num + 1} ---\n")
                all_text.extend(page_text)
                all_text.append("\n")
        return '\n'.join(all_text)

def extract_text_from_pdf(
    pdf_path: Union[str, Path],
    language: str = 'en',
    page_range: Optional[Tuple[int, int]] = None,
    **ocr_kwargs
) -> str:
    """
    Extract text from PDF using robust OCR logic (PyMuPDF + EasyOCR).
    """
    reader = OCRReader(language=language, **ocr_kwargs)
    return reader.process_pdf(pdf_path, page_range)