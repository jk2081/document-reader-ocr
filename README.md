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

## Languages

Common language codes: `en`, `fr`, `de`, `es`, `zh`, `ja`, `ko`

See [EasyOCR docs](https://github.com/JaidedAI/EasyOCR) for full list.

## Requirements

Python 3.8+ (dependencies installed automatically)

**New in v0.3.0**: OpenCV and scikit-image for image enhancement.

## License

MIT