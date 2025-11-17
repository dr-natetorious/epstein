# Epstein Document Exploration Toolkit

A comprehensive Python toolkit for exploring email dumps and image datasets. This toolkit provides tools for parsing, analyzing, and visualizing email archives and image collections.

## Features

### Email Analysis
- **Multiple Format Support**: Parse EML, MBOX, and PST email formats
- **Metadata Extraction**: Extract sender, recipient, date, subject, and attachment information
- **Content Analysis**: Search email bodies and headers for keywords
- **Statistics Generation**: Get insights about email volumes, sender domains, and attachment counts
- **Export Capabilities**: Export results to JSON and CSV formats

### Image Analysis
- **Metadata Extraction**: Extract EXIF data, dimensions, file sizes, and creation dates
- **Duplicate Detection**: Identify duplicate images using file hashing
- **Format Analysis**: Analyze distribution of image formats (JPEG, PNG, etc.)
- **Filtering**: Filter images by date range, size, or resolution
- **Statistics Generation**: Get comprehensive statistics about your image collection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dr-natetorious/epstein.git
cd epstein
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Command-Line Scripts

#### Email Exploration
```bash
python examples/explore_emails.py
```

This interactive script allows you to:
- Parse email directories or MBOX files
- View email statistics
- Search for keywords
- Export results

#### Image Exploration
```bash
python examples/explore_images.py
```

This interactive script allows you to:
- Scan directories for images
- View image statistics and metadata
- Find duplicate images
- Filter by date or size
- Export results

### Python API

#### Email Parsing Example
```python
from epstein.email_parser import EmailParser

# Initialize parser
parser = EmailParser()

# Parse emails
parser.parse_directory('/path/to/emails')
parser.parse_mbox('/path/to/mailbox.mbox')

# Get statistics
stats = parser.get_email_statistics()
print(f"Total emails: {stats['total_emails']}")

# Search emails
results = parser.search_emails('keyword', field='body')
print(f"Found {len(results)} matching emails")
```

#### Image Analysis Example
```python
from epstein.image_analyzer import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer()

# Scan directory
analyzer.scan_directory('/path/to/images', recursive=True)

# Get statistics
stats = analyzer.get_statistics()
print(f"Total images: {stats['total_images']}")
print(f"Total size: {stats['total_size_mb']} MB")

# Find duplicates
duplicates = analyzer.find_duplicates()
print(f"Found {len(duplicates)} groups of duplicates")
```

### Jupyter Notebook

For interactive exploration, use the provided Jupyter notebook:

```bash
jupyter notebook src/epstein/notebooks/exploration.ipynb
```

The notebook includes:
- Interactive email and image analysis
- Data visualization with matplotlib and seaborn
- Pandas DataFrames for advanced filtering
- Export capabilities

## Project Structure

```
epstein/
├── src/
│   └── epstein/
│       ├── email_parser/       # Email parsing module
│       │   ├── __init__.py
│       │   └── parser.py
│       ├── image_analyzer/     # Image analysis module
│       │   ├── __init__.py
│       │   └── analyzer.py
│       ├── utils/              # Utility functions
│       │   ├── __init__.py
│       │   └── export.py
│       └── notebooks/          # Jupyter notebooks
│           └── exploration.ipynb
├── examples/                   # Example scripts
│   ├── explore_emails.py
│   └── explore_images.py
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Requirements

- Python 3.8+
- See `requirements.txt` for full list of dependencies

Key dependencies:
- Pillow (image processing)
- pandas (data analysis)
- matplotlib/seaborn (visualization)
- jupyter (interactive notebooks)

## Use Cases

This toolkit is designed for:
- **Digital Forensics**: Analyze email archives and image collections
- **Data Discovery**: Explore and understand large document dumps
- **Compliance Review**: Search for specific content across email archives
- **Duplicate Management**: Identify and manage duplicate images
- **Timeline Analysis**: Understand communication patterns over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Disclaimer

This toolkit is provided for legal research and analysis purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations.
