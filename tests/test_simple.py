#!/usr/bin/env python3
"""Simple test to isolate PDF processing issues."""

import sys
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import io

def test_pdf_to_image(pdf_path):
    """Test PDF to image conversion."""
    print(f"Testing PDF to image conversion for: {pdf_path}")
    
    try:
        doc = fitz.open(str(pdf_path))
        print(f"PDF opened successfully. Number of pages: {len(doc)}")
        
        # Test first page only
        page = doc[0]
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale
        pix = page.get_pixmap(matrix=mat)
        print(f"Page converted to pixmap. Size: {pix.width}x{pix.height}")
        
        img_data = pix.tobytes("jpeg", jpg_quality=80)
        img = Image.open(io.BytesIO(img_data))
        print(f"Image created successfully. Size: {img.size}")
        
        img_array = np.array(img)
        print(f"Converted to numpy array. Shape: {img_array.shape}")
        
        doc.close()
        print("PDF processing test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in PDF processing: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "sample.pdf"
    
    test_pdf_to_image(pdf_path) 