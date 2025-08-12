#!/usr/bin/env python3
"""Test EasyOCR with a simple image."""

import sys
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import io
import easyocr

def test_ocr_on_pdf_image(pdf_path):
    """Test OCR on a PDF image."""
    print(f"Testing OCR on PDF image: {pdf_path}")
    
    try:
        # Convert PDF to image
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("jpeg", jpg_quality=80)
        img = Image.open(io.BytesIO(img_data))
        img_array = np.array(img)
        doc.close()
        
        print(f"Image prepared. Shape: {img_array.shape}")
        
        # Initialize EasyOCR
        print("Initializing EasyOCR...")
        ocr = easyocr.Reader(['en'])
        print("EasyOCR initialized successfully!")
        
        # Test OCR
        print("Running OCR on image...")
        result = ocr.readtext(img_array)
        print(f"OCR completed. Result type: {type(result)}")
        
        if result:
            print(f"Found {len(result)} text detections")
            for i, detection in enumerate(result[:3]):  # Show first 3 detections
                bbox, text, score = detection
                print(f"Detection {i+1}: '{text}' (confidence: {score:.2f})")
        else:
            print("No text detected")
        
        print("OCR test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in OCR test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "sample.pdf"
    
    test_ocr_on_pdf_image(pdf_path) 