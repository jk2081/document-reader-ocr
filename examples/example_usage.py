#!/usr/bin/env python3
"""Example usage of document-reader OCR package."""

import json
from pathlib import Path
import sys

from src.document_reader import OCRReader, extract_text_from_pdf


def example_basic_usage():
    """Basic usage example with simple text extraction."""
    print("=== Basic Text Extraction ===")
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    try:
        print(f"[INFO] Extracting text from '{PDF_PATH}' (basic usage)...")
        # Simple function call
        text = extract_text_from_pdf(PDF_PATH)
        print(f"[INFO] Extraction complete.")
        print(f"Extracted text length: {len(text)} characters")
        print("First 200 characters:")
        print(text[:200] + "..." if len(text) > 200 else text)
        print()
        
    except FileNotFoundError:
        print(f"PDF file '{PDF_PATH}' not found. Please provide a valid PDF file.")
    except Exception as e:
        print(f"Error processing PDF: {e}")


def example_layout_preservation():
    """Example showing layout-aware text extraction."""
    print("=== Layout-Aware Extraction ===")
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    try:
        print(f"[INFO] Extracting text from '{PDF_PATH}' with layout preservation...")
        # Extract with layout information
        results = extract_text_from_pdf(PDF_PATH)
        print(f"[INFO] Extraction complete.")
        
        print(f"Number of pages processed: {len(results)}")
        
        # Show details for first page
        if results:
            first_page = results[0]
            if isinstance(first_page, dict) and 'blocks' in first_page:
                print(f"First page has {first_page['num_blocks']} text blocks")
                print("\nFirst few text blocks:")
                for i, block in enumerate(first_page['blocks'][:3]):
                    print(f"Block {i+1}: '{block['text']}' (confidence: {block['confidence']:.2f})")
        print()
        
    except FileNotFoundError:
        print(f"PDF file '{PDF_PATH}' not found. Please provide a valid PDF file.")
    except Exception as e:
        print(f"Error processing PDF: {e}")


def example_class_based_usage():
    """Example using the OCRReader class directly."""
    print("=== Class-Based Usage ===")
    
    # Initialize with custom settings
    reader = OCRReader(
        language='en'
    )
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    try:
        print(f"[INFO] Initializing OCRReader and processing pages 1-2 of '{PDF_PATH}'...")
        # Process specific pages only (pages 1-2)
        text = reader.process_pdf(PDF_PATH, page_range=(1, 2))
        print(f"[INFO] Extraction complete.")
        print(f"Text from pages 1-2: {len(text)} characters")
        print("Sample text:")
        print(text[:150] + "..." if len(text) > 150 else text)
        print()
        
    except FileNotFoundError:
        print(f"PDF file '{PDF_PATH}' not found. Please provide a valid PDF file.")
    except Exception as e:
        print(f"Error processing PDF: {e}")


def example_llm_ready_output():
    """Example showing output formatted for LLM consumption."""
    print("=== LLM-Ready Output ===")
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    try:
        print(f"[INFO] Extracting text from '{PDF_PATH}' for LLM-ready output...")
        # Extract text optimized for LLM processing
        text = extract_text_from_pdf(PDF_PATH)
        print(f"[INFO] Extraction complete. Formatting for LLM prompt...")
        
        # Format for LLM prompt
        llm_prompt = f"""Please analyze the following document text and extract key information:

Document Content:
{text}

Please provide:
1. Main topics discussed
2. Key dates mentioned
3. Important names or organizations
4. Summary in 2-3 sentences
"""
        
        print("LLM-ready prompt created:")
        print(f"Prompt length: {len(llm_prompt)} characters")
        print("Preview:")
        print(llm_prompt[:300] + "..." if len(llm_prompt) > 300 else llm_prompt)
        print()
        
    except FileNotFoundError:
        print(f"PDF file '{PDF_PATH}' not found. Please provide a valid PDF file.")
    except Exception as e:
        print(f"Error processing PDF: {e}")


def example_save_results():
    """Example showing how to save results to files."""
    print("=== Saving Results ===")
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    try:
        print(f"[INFO] Extracting text from '{PDF_PATH}' with layout preservation for saving...")
        # Extract with layout information
        results = extract_text_from_pdf(PDF_PATH)
        print(f"[INFO] Extraction complete. Saving results to file...")
        # Save as JSON for later use
        output_file = "ocr_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Results saved to '{output_file}'")
        print(f"[INFO] Extracting plain text for saving...")
        # Save plain text version
        text_only = extract_text_from_pdf(PDF_PATH)
        text_file = "extracted_text.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_only)
        print(f"Plain text saved to '{text_file}'")
        print()
        
    except FileNotFoundError:
        print(f"PDF file '{PDF_PATH}' not found. Please provide a valid PDF file.")
    except Exception as e:
        print(f"Error processing PDF: {e}")


if __name__ == "__main__":
    print("Document Reader OCR - Usage Examples")
    print("=" * 50)
    print("[INFO] Starting all example runs...")
    
    # Determine PDF path from command line argument or default
    if len(sys.argv) > 1:
        PDF_PATH = sys.argv[1]
    else:
        PDF_PATH = "sample.pdf"
    
    # Check if sample PDF exists
    if not Path(PDF_PATH).exists():
        print(f"Note: These examples use '{PDF_PATH}' as input.")
        print(f"Please place a PDF file named '{PDF_PATH}' in this directory to run the examples.")
        print("Or provide a PDF path as a command line argument, or modify the PDF_PATH variable.")
        print()
    
    # Run examples
    example_basic_usage()
    example_layout_preservation()
    example_class_based_usage()
    example_llm_ready_output()
    example_save_results()
    
    print("All examples completed!")
    print("[INFO] All example runs finished.")
    print("\nTo use this in other projects:")
    print("1. Install the package: pip install -e .")
    print("2. Import: from document_reader import extract_text_from_pdf, OCRReader")
    print("3. Use the functions as shown in these examples")