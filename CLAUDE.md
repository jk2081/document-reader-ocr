# Document Reader - Claude Context

## Project Overview

**Status**: ✅ **Enhanced OCR Library v0.3.0 Ready for Production**

This is a clean, focused Python library for extracting text from PDF documents using EasyOCR with advanced image enhancement and confidence scoring. The project has been successfully organized, built, and tested as a pip-installable package.

## Current State

### ✅ **Completed Tasks**
- **Package Structure**: Clean, organized directory structure following Python best practices
- **OCR Implementation**: Working EasyOCR-based text extraction from PDFs
- **Image Enhancement**: OpenCV + scikit-image preprocessing for poor quality documents
- **Confidence Scoring**: Quality assessment and low-confidence region detection
- **Dependencies**: EasyOCR + PyMuPDF + OpenCV + scikit-image
- **Build System**: Successfully builds wheel and source distributions
- **Testing**: Verified imports and basic functionality work correctly
- **Documentation**: Updated README.md and examples for v0.3.0 features
- **Organization**: All files properly organized into logical directories

### 📦 **Package Details**
- **Name**: `document-reader`
- **Version**: `0.3.0`
- **Author**: Jai Kejriwal (jai@clapgrow.com)
- **License**: MIT
- **Python**: 3.8+
- **Status**: Enhanced with image preprocessing and confidence scoring

## Project Structure

```
document-reader/
├── src/                          # Core package source
│   └── document_reader/          
│       ├── __init__.py          # Exports: OCRReader, extract_text_from_pdf
│       └── ocr_reader.py        # Main OCR implementation using EasyOCR
├── tests/                        # Test files
│   ├── __init__.py              
│   ├── test_ocr.py              # OCR functionality tests
│   └── test_simple.py           # Basic tests
├── examples/                     # Example scripts and AI integration
│   ├── __init__.py              
│   ├── example_usage.py         # Basic OCR usage examples
│   ├── enhanced_usage.py        # CLI script for enhanced OCR with confidence (v0.3.0)
│   └── orchestrator.py          # AI-powered document analysis (separate from core)
├── docs/                         # Documentation
│   └── CLAUDE.MD                # Original project documentation (legacy)
├── config/                       # Configuration files
│   └── prompts.json             # AI prompt templates (used by orchestrator)
├── dev/                          # Development artifacts (gitignored)
│   └── doc-reader-3-11/         # Virtual environment
├── dist/                         # Build outputs
│   ├── document_reader-0.2.0-py3-none-any.whl  # Ready for pip install
│   └── document_reader-0.2.0.tar.gz
├── pyproject.toml               # Package configuration
├── README.md                    # User documentation (concise)
├── LICENSE                      # MIT license
├── .gitignore                   # Git ignore rules
└── CLAUDE.md                    # This file - project context
```

## Core Functionality

### **Primary API**

**Simple Function**:
```python
from document_reader import extract_text_from_pdf
text = extract_text_from_pdf("document.pdf", language='en')
```

**Enhanced Function (v0.3.0)**:
```python
from document_reader import extract_text_with_confidence
result = extract_text_with_confidence("document.pdf", enable_enhancement=True)
text = result['text']
confidence = result['confidence_data']['average_confidence']
```

**Advanced Class**:
```python
from document_reader import OCRReader

reader = OCRReader(
    language='en',
    confidence_threshold=0.3,
    enable_enhancement=True,  # New in v0.3.0
    enhancement_method="auto"  # New in v0.3.0
)

# Traditional extraction (backward compatible)
text = reader.process_pdf("document.pdf", page_range=(1, 5))

# Enhanced extraction with confidence (v0.3.0)
result = reader.process_pdf_with_confidence("document.pdf")
quality = reader.assess_document_quality("document.pdf")
```

### **Dependencies**
- **EasyOCR**: Primary OCR engine (stable on macOS ARM)
- **PyMuPDF**: PDF to image conversion
- **OpenCV**: Image enhancement and preprocessing (v0.3.0)
- **scikit-image**: Advanced image processing (v0.3.0)
- **Pillow**: Image processing
- **NumPy**: Array operations

## Key Design Decisions

### ✅ **OCR-Only Focus**
- **Separation of Concerns**: Core library only handles OCR text extraction
- **AI Integration**: Separate concern - handled by orchestrator.py example
- **Clean API**: Simple, focused interface with sensible defaults

### ✅ **EasyOCR Choice**
- **Stability**: Works reliably on macOS ARM64
- **Performance**: Fast initialization and processing
- **Accuracy**: Good text recognition for most documents
- **Compatibility**: Python 3.12 compatible

### ✅ **Package Organization**
- **src/ layout**: Standard Python package structure
- **Examples separate**: AI integration examples don't clutter core package
- **Dev artifacts isolated**: Clean root directory for distribution

## Installation & Usage

### **For End Users**
```bash
pip install dist/document_reader-0.3.0-py3-none-any.whl
```

### **For Development**
```bash
cd document-reader
pip install -e .  # Editable install
```

### **Command Line Usage (v0.3.0)**
For quick PDF processing with enhanced features:
```bash
python examples/enhanced_usage.py document.pdf
```
This provides enhanced OCR with confidence scoring and image enhancement.

### **For Frappe Integration**
The library is designed to be imported into Frappe apps:
```python
import frappe
from document_reader import extract_text_from_pdf

@frappe.whitelist()
def process_pdf_document(file_path):
    return extract_text_from_pdf(file_path)
```

## Future Enhancements (If Needed)

### **Potential Improvements**
1. **Batch Processing**: Process multiple PDFs efficiently
2. **Image Formats**: Support JPEG, PNG input in addition to PDF
3. **Layout Preservation**: Optional bounding box information
4. **Performance**: GPU acceleration options
5. **Caching**: Cache OCR results for repeated processing

### **API Considerations**
- Current API is stable and backward-compatible
- Any new features should be optional parameters
- Maintain simple `extract_text_from_pdf()` interface

## Related Projects

### **Document Reader API**
- **Location**: Separate `document-reader-api` project (planned)
- **Purpose**: REST API that combines this OCR library + Claude AI
- **Architecture**: FastAPI service using this library + Anthropic API
- **PRD**: Available in docs/PRD.md and docs/CODE_STANDARDS.md

### **AI Integration**
- **Current**: `examples/orchestrator.py` shows AI-powered document analysis
- **Future**: Separate API service will handle AI integration
- **Prompts**: `config/prompts.json` contains templates for different document types

## Development Notes

### **Build Process**
```bash
# Clean and build
rm -rf dist/ build/ src/*.egg-info/
python -m build

# Test installation
pip install dist/document_reader-0.3.0-py3-none-any.whl --force-reinstall

# Verify imports
python -c "from document_reader import OCRReader, extract_text_from_pdf; print('✓ Success')"
```

### **Virtual Environment**
- **Location**: `dev/doc-reader-3-11/`
- **Python**: 3.11 (recommended for stability)
- **Activation**: `source dev/doc-reader-3-11/bin/activate`

### **Testing**
```bash
# Run basic tests
python tests/test_simple.py

# Test with real PDF
python tests/test_ocr.py sample.pdf
```

## Important Files

### **Core Implementation**
- `src/document_reader/ocr_reader.py` - Main OCR logic
- `src/document_reader/__init__.py` - Package exports

### **Configuration**
- `pyproject.toml` - Package metadata and dependencies
- `.gitignore` - Excludes dev/ and build artifacts

### **Documentation**
- `README.md` - User-facing documentation (concise)
- `examples/` - Usage examples and AI integration demos

## Next Steps (If Continuing)

### **If Building API Service**
1. Create new `document-reader-api` repository
2. Use this library as dependency: `pip install document-reader`
3. Follow docs/PRD.md and docs/CODE_STANDARDS.md
4. Implement FastAPI endpoints that call this library + Claude AI

### **If Enhancing OCR Library**
1. Add tests to `tests/` directory
2. Implement new features in `src/document_reader/ocr_reader.py`
3. Update version in `pyproject.toml`
4. Rebuild with `python -m build`

### **If Publishing**
1. Create GitHub repository
2. Upload to PyPI: `python -m twine upload dist/*`
3. Update README.md with real installation instructions

## Status Summary

**✅ READY**: This OCR library is complete and production-ready
- Clean, focused API
- Stable dependencies
- Proper package structure
- Successfully builds and installs
- Tested and verified working

The library can be immediately used in Frappe environments or any Python project requiring PDF text extraction via OCR.