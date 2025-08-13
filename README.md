# Document Reader

Extract text from PDF documents using OCR with EasyOCR. Enhanced with image preprocessing and confidence scoring for better accuracy on poor-quality documents.

## Installation

```bash
pip install document-reader
```

## Usage

### Simple

```python
from document_reader import extract_text_from_pdf

text = extract_text_from_pdf("document.pdf")
print(text)
```

### Advanced

```python
from document_reader import OCRReader

reader = OCRReader(
    language='en',
    confidence_threshold=0.3,
    enable_enhancement=True,  # v0.3.0: Image enhancement
    enhancement_method="auto"  # auto, contrast, denoise, sharpen, full
)

# Extract all pages
text = reader.process_pdf("document.pdf")

# Extract with confidence data (v0.3.0)
result = reader.process_pdf_with_confidence("document.pdf")
text = result['text']
confidence = result['confidence_data']['average_confidence']
```

### Enhanced Extraction (v0.3.0)

```python
from document_reader import extract_text_with_confidence

# One-line extraction with enhancement
result = extract_text_with_confidence(
    "poor_quality_scan.pdf",
    enable_enhancement=True
)

print(f"Text: {result['text']}")
print(f"Confidence: {result['confidence_data']['average_confidence']:.1%}")

# Quality assessment
from document_reader import OCRReader
reader = OCRReader(enable_enhancement=True)
quality = reader.assess_document_quality("document.pdf")

if quality['requires_manual_review']:
    print(f"⚠️ Document needs review - Quality: {quality['quality_rating']}")
```

### Command Line Usage

For quick PDF processing from the command line, use the enhanced example script:

```bash
# Process a PDF with enhanced OCR and confidence scoring
python examples/enhanced_usage.py document.pdf

# Example output:
# Document Reader v0.3.0 - Enhanced PDF Processing
# ============================================================
# Processing: document.pdf
# 
# [1/3] Extracting text with automatic enhancement...
# [2/3] Analyzing confidence metrics...
# [3/3] Displaying results...
# 
# Processing Results:
# ----------------------------------------
# Average OCR Confidence: 87.3%
# Enhancement Applied: Yes
# Text Length: 1245 characters
# ✓ Good OCR confidence
# 
# Extracted Text:
# ============================================================
# [Your PDF text content here...]
```

## API

### `extract_text_from_pdf(pdf_path, language='en')`
Extract text from PDF file (basic, backward compatible).

### `extract_text_with_confidence(pdf_path, enable_enhancement=True)` *(v0.3.0)*
Extract text with confidence scoring and optional image enhancement.

### `OCRReader(...)`
OCR reader with configurable options.

**Parameters:**
- `language='en'` - OCR language
- `confidence_threshold=0.3` - Minimum confidence for text inclusion  
- `enable_enhancement=False` - *(v0.3.0)* Enable image preprocessing
- `enhancement_method="auto"` - *(v0.3.0)* Enhancement method
- `enhancement_params={}` - *(v0.3.0)* Custom enhancement parameters

**Methods:**
- `process_pdf(pdf_path, page_range=None)` - Extract text (backward compatible)
- `process_pdf_with_confidence(pdf_path)` - *(v0.3.0)* Extract text with confidence data
- `assess_document_quality(pdf_path)` - *(v0.3.0)* Assess document quality
- `get_low_confidence_regions(pdf_path)` - *(v0.3.0)* Find low-confidence text

## Confidence Scores *(v0.3.0)*

OCR confidence scores indicate text recognition accuracy:

- **90-100%**: Excellent quality, high accuracy
- **70-89%**: Good quality, suitable for most uses  
- **50-69%**: Fair quality, may need review for critical applications
- **Below 50%**: Poor quality, manual review recommended

**Factors affecting confidence:**
- Document scan quality and resolution
- Text clarity and font readability  
- Image enhancement effectiveness
- Language complexity and character recognition

**When to use enhancement:**
```python
# Automatic enhancement for poor quality documents
result = extract_text_with_confidence("scan.pdf", enable_enhancement=True)
if result['confidence_data']['average_confidence'] < 0.7:
    print("Consider manual review or document rescanning")
```

## Languages

Common language codes: `en`, `fr`, `de`, `es`, `zh`, `ja`, `ko`

See [EasyOCR docs](https://github.com/JaidedAI/EasyOCR) for full list.

## Requirements

Python 3.8+ (dependencies installed automatically)

**New in v0.3.0**: OpenCV and scikit-image for image enhancement.

## Troubleshooting

**Low confidence scores (<70%)?**
- Enable image enhancement: `enable_enhancement=True`
- Try different enhancement methods: `enhancement_method="full"`
- Check document quality (resolution, clarity)
- Verify correct language setting

**No text extracted?**
- Ensure PDF contains text (not just images)
- Try lower confidence threshold: `confidence_threshold=0.1`
- Check file path and permissions

**Slow processing?**
- Use page ranges for large PDFs: `page_range=(1, 5)`
- Disable enhancement for high-quality documents

## License

MIT