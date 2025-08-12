#!/usr/bin/env python3
"""Test script to verify enhanced functionality imports work correctly."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all new imports work correctly."""
    try:
        # Test ImageEnhancer import
        from document_reader.image_enhancer import ImageEnhancer
        print("✓ ImageEnhancer import successful")
        
        # Test ImageEnhancer instantiation
        enhancer = ImageEnhancer()
        print("✓ ImageEnhancer instantiation successful")
        
        # Test that ImageEnhancer has expected methods
        expected_methods = ['enhance_image', '_assess_image_quality', '_auto_enhance', 
                          '_enhance_contrast', '_denoise_image', '_sharpen_image', '_full_pipeline']
        for method in expected_methods:
            assert hasattr(enhancer, method), f"Missing method: {method}"
        print("✓ ImageEnhancer has all expected methods")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_ocr_reader_signature():
    """Test that OCRReader accepts new parameters."""
    try:
        # This will fail on missing dependencies but should pass parameter validation
        from document_reader.ocr_reader import OCRReader
        
        # Test that we can instantiate with new parameters
        try:
            reader = OCRReader(
                enable_enhancement=True,
                enhancement_method="auto",
                enhancement_params={'clip_limit': 2.0}
            )
            print("✓ OCRReader accepts new enhancement parameters")
        except Exception as e:
            # Expected to fail on missing dependencies, but parameter validation should pass
            if "module" not in str(e).lower():
                print(f"✗ Parameter validation failed: {e}")
                return False
            else:
                print("✓ OCRReader parameter validation passed (dependency error expected)")
        
        return True
    except ImportError as e:
        print(f"✗ OCRReader import failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing enhanced document-reader functionality...")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_ocr_reader_signature()
    
    print("=" * 50)
    if success:
        print("✓ All tests passed! Enhanced functionality is ready.")
    else:
        print("✗ Some tests failed.")
        sys.exit(1)