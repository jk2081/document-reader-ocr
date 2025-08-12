"""OCR Reader for PDF documents using EasyOCR."""

import logging
import io
from pathlib import Path
from typing import List, Optional, Tuple, Union, Dict, Any

import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import easyocr
import os

from .image_enhancer import ImageEnhancer

class OCRReader:
    """OCR reader for extracting text from PDF documents using EasyOCR and PyMuPDF."""
    def __init__(
        self,
        language: str = 'en',
        image_resolution_scale: float = 2.0,
        image_quality: int = 80,
        confidence_threshold: float = 0.3,
        enable_enhancement: bool = False,
        enhancement_method: str = "auto",
        enhancement_params: Optional[Dict[str, Any]] = None,
    ):
        self.language = language
        self.image_resolution_scale = image_resolution_scale
        self.image_quality = image_quality
        self.confidence_threshold = confidence_threshold
        self.enable_enhancement = enable_enhancement
        self.enhancement_method = enhancement_method
        self.enhancement_params = enhancement_params or {}
        self._ocr = None
        self.logger = logging.getLogger(__name__)
        self._enhancer = ImageEnhancer(self.logger) if enable_enhancement else None

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

    def _enhance_image_if_enabled(self, image: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Apply image enhancement if enabled."""
        if self._enhancer:
            return self._enhancer.enhance_image(image, self.enhancement_method, self.enhancement_params)
        else:
            return image, {"enhancement_applied": False}

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

    def process_pdf_with_confidence(
        self,
        pdf_path: Union[str, Path],
        page_range: Optional[Tuple[int, int]] = None,
    ) -> Dict[str, Any]:
        """Process PDF and return both text and confidence information."""
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
        confidence_data = {
            'page_confidences': [],
            'text_confidences': [],
            'enhancement_metrics': [],
            'low_confidence_count': 0,
            'total_text_blocks': 0
        }

        for page_num, img in enumerate(images):
            # Apply enhancement if enabled
            enhanced_img, enhancement_metrics = self._enhance_image_if_enabled(img)
            confidence_data['enhancement_metrics'].append(enhancement_metrics)

            # Perform OCR
            result = ocr.readtext(enhanced_img)
            page_text = []
            page_confidences = []

            if result:
                for detection in result:
                    bbox, text, score = detection
                    confidence_data['text_confidences'].append((text, score))
                    confidence_data['total_text_blocks'] += 1

                    if score > self.confidence_threshold:
                        page_text.append(text)
                        page_confidences.append(score)
                    else:
                        confidence_data['low_confidence_count'] += 1

            # Calculate page-level confidence
            page_confidence = np.mean(page_confidences) if page_confidences else 0.0
            confidence_data['page_confidences'].append(page_confidence)

            if page_text:
                all_text.append(f"\n--- Page {page_num + 1} ---\n")
                all_text.extend(page_text)
                all_text.append("\n")

        # Calculate overall confidence metrics
        all_confidences = [conf for _, conf in confidence_data['text_confidences']]
        confidence_data['average_confidence'] = np.mean(all_confidences) if all_confidences else 0.0
        confidence_data['min_confidence'] = np.min(all_confidences) if all_confidences else 0.0
        confidence_data['max_confidence'] = np.max(all_confidences) if all_confidences else 0.0

        return {
            'text': '\n'.join(all_text),
            'confidence_data': confidence_data
        }

    def assess_document_quality(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """Assess overall document quality before processing."""
        result = self.process_pdf_with_confidence(pdf_path)
        confidence_data = result['confidence_data']

        # Quality assessment
        avg_confidence = confidence_data['average_confidence']
        low_conf_ratio = confidence_data['low_confidence_count'] / max(1, confidence_data['total_text_blocks'])

        if avg_confidence >= 0.9 and low_conf_ratio <= 0.1:
            quality_rating = "Excellent"
        elif avg_confidence >= 0.8 and low_conf_ratio <= 0.2:
            quality_rating = "Good"
        elif avg_confidence >= 0.6 and low_conf_ratio <= 0.4:
            quality_rating = "Fair"
        elif avg_confidence >= 0.4:
            quality_rating = "Poor"
        else:
            quality_rating = "Requires Review"

        return {
            'quality_rating': quality_rating,
            'average_confidence': avg_confidence,
            'low_confidence_ratio': low_conf_ratio,
            'requires_manual_review': quality_rating in ["Poor", "Requires Review"],
            'enhancement_recommended': avg_confidence < 0.7,
            'confidence_data': confidence_data
        }

    def get_low_confidence_regions(self, pdf_path: Union[str, Path], threshold: float = 0.5) -> List[Dict]:
        """Get text regions with confidence below threshold."""
        result = self.process_pdf_with_confidence(pdf_path)
        low_conf_regions = []

        for text, confidence in result['confidence_data']['text_confidences']:
            if confidence < threshold:
                low_conf_regions.append({
                    'text': text,
                    'confidence': confidence,
                    'warning': f"Low confidence ({confidence:.1%}) - verify manually"
                })

        return low_conf_regions

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


def extract_text_with_confidence(
    pdf_path: Union[str, Path],
    language: str = 'en',
    page_range: Optional[Tuple[int, int]] = None,
    enable_enhancement: bool = True,
    enhancement_method: str = "auto",
    **kwargs
) -> Dict[str, Any]:
    """
    Extract text from PDF with confidence information and optional enhancement.
    
    Returns:
        Dict containing 'text' and 'confidence_data' keys
    """
    reader = OCRReader(
        language=language,
        enable_enhancement=enable_enhancement,
        enhancement_method=enhancement_method,
        **kwargs
    )
    return reader.process_pdf_with_confidence(pdf_path, page_range)