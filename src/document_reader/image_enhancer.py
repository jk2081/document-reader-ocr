import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple, Dict, Any
import logging


class ImageEnhancer:
    """Advanced image preprocessing for better OCR results on poor quality documents."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def enhance_image(self, image: np.ndarray, method: str = "auto", 
                     enhancement_params: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Enhance image quality for better OCR results.
        
        Args:
            image: Input image as numpy array
            method: Enhancement method ("auto", "contrast", "denoise", "sharpen", "full")
            enhancement_params: Custom parameters for enhancement
            
        Returns:
            Tuple of (enhanced_image, enhancement_metrics)
        """
        params = enhancement_params or {}
        metrics = {"original_quality": self._assess_image_quality(image)}

        if method == "auto":
            enhanced = self._auto_enhance(image, params)
        elif method == "contrast":
            enhanced = self._enhance_contrast(image, params)
        elif method == "denoise":
            enhanced = self._denoise_image(image, params)
        elif method == "sharpen":
            enhanced = self._sharpen_image(image, params)
        elif method == "full":
            enhanced = self._full_pipeline(image, params)
        else:
            enhanced = image

        metrics["enhanced_quality"] = self._assess_image_quality(enhanced)
        metrics["improvement_factor"] = metrics["enhanced_quality"] / metrics["original_quality"]
        metrics["enhancement_applied"] = method != "none"

        return enhanced, metrics

    def _assess_image_quality(self, image: np.ndarray) -> float:
        """Assess image quality using multiple metrics."""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        # Combine multiple quality metrics
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()  # Sharpness
        mean_brightness = np.mean(gray)  # Brightness
        contrast = np.std(gray)  # Contrast

        # Normalize and combine (0-1 scale)
        quality_score = min(1.0, (variance / 1000 + contrast / 128 + (1 - abs(mean_brightness - 127) / 127)) / 3)
        return quality_score

    def _auto_enhance(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Automatically detect and apply best enhancement."""
        quality = self._assess_image_quality(image)

        if quality < 0.3:  # Very poor quality
            return self._full_pipeline(image, params)
        elif quality < 0.6:  # Medium quality
            return self._enhance_contrast(self._denoise_image(image, params), params)
        else:  # Good quality, light enhancement only
            return self._sharpen_image(image, params)

    def _enhance_contrast(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Apply CLAHE contrast enhancement."""
        if len(image.shape) == 3:
            # Convert to LAB, enhance L channel, convert back
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            clahe = cv2.createCLAHE(clipLimit=params.get('clip_limit', 2.0),
                                   tileGridSize=params.get('tile_size', (8,8)))
            lab[:,:,0] = clahe.apply(lab[:,:,0])
            return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        else:
            clahe = cv2.createCLAHE(clipLimit=params.get('clip_limit', 2.0))
            return clahe.apply(image)

    def _denoise_image(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Remove noise from scanned documents."""
        if len(image.shape) == 3:
            return cv2.fastNlMeansDenoisingColored(image, None,
                                                  params.get('h', 10),
                                                  params.get('h_color', 10),
                                                  params.get('template_size', 7),
                                                  params.get('search_size', 21))
        else:
            return cv2.fastNlMeansDenoising(image, None, params.get('h', 10))

    def _sharpen_image(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Sharpen text edges."""
        strength = params.get('sharpen_strength', 1.0)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * strength
        return cv2.filter2D(image, -1, kernel)

    def _full_pipeline(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Apply full enhancement pipeline for very poor quality images."""
        # 1. Denoise
        enhanced = self._denoise_image(image, params)
        # 2. Enhance contrast
        enhanced = self._enhance_contrast(enhanced, params)
        # 3. Sharpen
        enhanced = self._sharpen_image(enhanced, params)
        return enhanced