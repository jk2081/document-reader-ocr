#!/usr/bin/env python3
"""
Enhanced document reader with command line PDF processing.

Usage: python enhanced_usage.py <path_to_pdf>

This demonstrates the v0.3.0 features:
- Image enhancement for poor quality documents  
- Confidence scoring and quality assessment
- Real PDF processing from command line
"""

import sys
import os
from pathlib import Path

# Add src directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from document_reader import OCRReader, extract_text_with_confidence, ImageEnhancer
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Error: Unable to import document_reader library ({e})")
    print("Please ensure dependencies are installed: pip install -e .")
    sys.exit(1)

def process_pdf_with_enhancement(pdf_path):
    """Process PDF using enhanced OCR with confidence scoring and image enhancement."""
    print("Document Reader v0.3.0 - Enhanced PDF Processing")
    print("=" * 60)
    print(f"Processing: {pdf_path}")
    print()
    
    try:
        # Check if file exists
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file '{pdf_path}' not found")
        
        print("[1/3] Extracting text with automatic enhancement...")
        # Use enhanced extraction with confidence scoring
        result = extract_text_with_confidence(
            pdf_path,
            language='en',
            enable_enhancement=True,
            enhancement_method="auto"
        )
        
        extracted_text = result['text']
        confidence_data = result['confidence_data']
        
        print("[2/3] Analyzing confidence metrics...")
        avg_confidence = confidence_data['average_confidence']
        enhancement_applied = any(
            m.get('enhancement_applied', False) 
            for m in confidence_data.get('enhancement_metrics', [])
        )
        
        print("[3/3] Displaying results...")
        print()
        
        # Display confidence and enhancement info
        print("Processing Results:")
        print("-" * 40)
        print(f"Average OCR Confidence: {avg_confidence:.1%}")
        print(f"Enhancement Applied: {'Yes' if enhancement_applied else 'No'}")
        print(f"Text Length: {len(extracted_text)} characters")
        
        if avg_confidence < 0.7:
            print("⚠️  Low confidence detected - document may need manual review")
        else:
            print("✓ Good OCR confidence")
        
        print()
        print("Extracted Text:")
        print("=" * 60)
        
        # Display the extracted text with proper formatting
        if extracted_text.strip():
            # Show full text if short, otherwise show preview
            if len(extracted_text) <= 2000:
                print(extracted_text)
            else:
                print(extracted_text[:2000])
                print()
                print(f"... [Text truncated - showing first 2000 of {len(extracted_text)} characters]")
        else:
            print("No text was extracted from the PDF.")
        
        print()
        print("=" * 60)
        print("✅ Processing completed successfully!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please provide a valid PDF file path.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        sys.exit(1)

def main():
    """Process PDF from command line arguments."""
    # Check for command line arguments
    if len(sys.argv) != 2:
        print("Enhanced Document Reader v0.3.0")
        print("Usage: python enhanced_usage.py <path_to_pdf>")
        print()
        print("Features:")
        print("• Automatic image enhancement for poor quality documents")
        print("• OCR confidence scoring and quality assessment") 
        print("• Supports multiple languages (default: English)")
        print("• Real-time processing feedback")
        print()
        print("Example:")
        print("  python enhanced_usage.py document.pdf")
        print("  python enhanced_usage.py /path/to/my/file.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    process_pdf_with_enhancement(pdf_path)

if __name__ == "__main__":
    main()