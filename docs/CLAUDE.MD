# Document Reader - Claude Context

## Project Overview

OCR-based PDF document reader with AI-powered document analysis. Supports both EasyOCR (stable) and PaddleOCR (experimental) for text extraction, with Claude AI integration for structured document analysis.

## Architecture

- **Core Module**: `src/document_reader/ocr_reader.py` - Main OCR functionality using EasyOCR
- **Orchestrator**: `orchestrator.py` - AI-powered document analysis using Claude
- **Policy Processor**: `sample_processor.py` - Insurance policy processing (uses PaddleOCR)
- **Package Entry**: `src/document_reader/__init__.py` - Exports `OCRReader` and `extract_text_from_pdf`
- **Examples**: `example_usage.py` - Usage examples and testing

## Key Dependencies

- **EasyOCR**: Primary OCR engine (`easyocr>=1.6.0`) - Stable on macOS ARM
- **PaddleOCR**: Alternative OCR engine (`paddleocr>=3.1.0`) - Experimental, may segfault on macOS ARM
- **PyMuPDF (fitz)**: PDF to image conversion
- **PIL/Pillow**: Image processing
- **NumPy**: Array operations
- **Anthropic**: Claude AI integration

## Main Classes & Functions

### OCRReader Class (EasyOCR)

```python
from src.document_reader import OCRReader

reader = OCRReader(
    language='en',                    # OCR language
    image_resolution_scale=2.0,       # PDF to image scale
    image_quality=80,                 # JPEG quality
    confidence_threshold=0.3          # Min confidence for text
)

# Process PDF with optional page range
text = reader.process_pdf(pdf_path, page_range=(1, 5))
```

### Helper Function

```python
from src.document_reader import extract_text_from_pdf

# Simple extraction
text = extract_text_from_pdf("document.pdf", language='en')
```

### AI-Powered Document Analysis

```python
# Using the orchestrator script
python orchestrator.py document.pdf hins

# Available prompt types:
# hins  - Health Insurance
# mtins - Motor Insurance
# txnv  - Tax Invoice
# general - General Document
```

## OCR Engine Comparison

### EasyOCR (Recommended)

- ✅ **Stable** on macOS ARM64
- ✅ **Fast** initialization
- ✅ **Good accuracy** for most documents
- ✅ **Python 3.12 compatible**

## EasyOCR API Notes

- **Initialization**: `easyocr.Reader(['en'])`
- **Processing**: `reader.readtext(image_array)`
- **Output Format**: `[(bbox, text, confidence), ...]`
- **First run**: Downloads models automatically

## AI Integration

### Orchestrator Script

The `orchestrator.py` script provides:

- **Document text extraction** using OCR
- **Structured analysis** using Claude AI
- **Prompt-based processing** for different document types
- **JSON output** for structured data extraction

### Prompt System

- **Short codes**: `hins`, `mtins`, `txnv`, `general`
- **Configurable**: Edit `prompts.json` for custom prompts
- **Auto-creation**: Default prompts created if file missing

## Testing & Development

### Basic Testing

```bash
# Test OCR functionality
python test_ocr.py sample.pdf

# Test PDF processing
python test_simple.py sample.pdf

# Run examples
python example_usage.py sample.pdf
```

### AI Analysis Testing

```bash
# Health insurance document
python orchestrator.py health_policy.pdf hins

# Motor insurance document
python orchestrator.py motor_policy.pdf mtins

# Tax invoice
python orchestrator.py invoice.pdf txnv
```

## Environment Setup

### Python 3.11 (Recommended for PaddleOCR)

```bash
# Create environment
python3.11 -m venv doc-reader-3-11
source doc-reader-3-11/bin/activate

# Install dependencies
pip install paddleocr pymupdf pillow numpy anthropic
```

### Python 3.12 (Recommended for EasyOCR)

```bash
# Create environment
python3.12 -m venv doc-reader-3-12
source doc-reader-3-12/bin/activate

# Install dependencies
pip install easyocr pymupdf pillow numpy anthropic
```

## Development Commands

```bash
# Install in development mode
pip install -e .

# Test basic functionality
python test_ocr.py sample.pdf

# Run examples
python example_usage.py sample.pdf

# Test AI analysis
python orchestrator.py document.pdf hins
```

## Recent Changes

- **AI Integration**: Added Claude AI-powered document analysis
- **Prompt System**: Implemented short-code prompt system (`hins`, `mtins`, `txnv`)
- **Stability**: EasyOCR as primary engine, PaddleOCR as experimental
- **Validation**: Prompt validation before document processing
- **Error Handling**: Improved error messages and fallback options
