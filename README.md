# Document Reader

Extract text from PDF documents using OCR with EasyOCR.

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
    confidence_threshold=0.3
)

# Extract all pages
text = reader.process_pdf("document.pdf")

# Extract specific pages
text = reader.process_pdf("document.pdf", page_range=(1, 5))
```

## API

### `extract_text_from_pdf(pdf_path, language='en')`
Extract text from PDF file.

### `OCRReader(language='en', confidence_threshold=0.3, image_resolution_scale=2.0, image_quality=80)`
OCR reader with configurable options.

**Methods:**
- `process_pdf(pdf_path, page_range=None)` - Extract text from PDF

## Languages

Common language codes: `en`, `fr`, `de`, `es`, `zh`, `ja`, `ko`

See [EasyOCR docs](https://github.com/JaidedAI/EasyOCR) for full list.

## Requirements

Python 3.8+ (dependencies installed automatically)

## License

MIT