# Quick Start Guide

This guide will help you get started with the Epstein Document Exploration Toolkit.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/dr-natetorious/epstein.git
cd epstein
```

### 2. Set up Python environment
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify installation
```bash
python3 -c "import sys; sys.path.insert(0, 'src'); from epstein.email_parser import EmailParser; from epstein.image_analyzer import ImageAnalyzer; print('✓ Installation successful!')"
```

## Quick Examples

### Email Analysis

#### Parse a directory of emails
```python
import sys
sys.path.insert(0, 'src')

from epstein.email_parser import EmailParser

# Initialize parser
parser = EmailParser()

# Parse emails from a directory
emails = parser.parse_directory('/path/to/your/emails')

# Display statistics
stats = parser.get_email_statistics()
print(f"Total emails: {stats['total_emails']}")
print(f"Attachments: {stats['total_attachments']}")
```

#### Search for specific content
```python
# Search in email bodies
results = parser.search_emails('meeting', field='body')
print(f"Found {len(results)} emails containing 'meeting'")

# Search in subjects
results = parser.search_emails('urgent', field='subject')
print(f"Found {len(results)} emails with 'urgent' in subject")
```

#### Export results
```python
from epstein.utils import export_to_json, export_to_csv

# Export to JSON
export_to_json(parser.emails, 'email_results.json')

# Export to CSV for Excel
export_to_csv(parser.emails, 'email_results.csv')
```

### Image Analysis

#### Scan an image directory
```python
import sys
sys.path.insert(0, 'src')

from epstein.image_analyzer import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer()

# Scan directory recursively
images = analyzer.scan_directory('/path/to/your/images', recursive=True)

# Display statistics
stats = analyzer.get_statistics()
print(f"Total images: {stats['total_images']}")
print(f"Total size: {stats['total_size_mb']} MB")
print(f"Formats: {stats['formats']}")
```

#### Find duplicate images
```python
# Find duplicates based on file hash
duplicates = analyzer.find_duplicates()

print(f"Found {len(duplicates)} groups of duplicate images")

# Display duplicate groups
for hash_val, files in duplicates.items():
    print(f"\nDuplicate group ({len(files)} files):")
    for filepath in files:
        print(f"  - {filepath}")
```

#### Filter images
```python
from datetime import datetime, timedelta

# Filter by date (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
recent_images = analyzer.filter_by_date_range(start_date, end_date)

# Filter by size (between 1MB and 10MB)
medium_images = analyzer.filter_by_size(min_size_mb=1, max_size_mb=10)
```

## Using the Interactive Scripts

### Email Explorer
```bash
python examples/explore_emails.py
```

Follow the prompts to:
1. Select email directory or MBOX file
2. View statistics
3. Search for keywords
4. Export results

### Image Explorer
```bash
python examples/explore_images.py
```

Follow the prompts to:
1. Select image directory
2. View statistics
3. Find duplicates
4. Filter by date or size
5. Export results

## Using Jupyter Notebook

For interactive data exploration with visualizations:

```bash
# Start Jupyter
jupyter notebook

# Open the exploration notebook
# Navigate to: src/epstein/notebooks/exploration.ipynb
```

The notebook provides:
- Interactive analysis workflows
- Data visualization with charts and graphs
- Pandas DataFrames for advanced filtering
- Export capabilities

## Common Use Cases

### 1. Email Archive Analysis
```python
from epstein.email_parser import EmailParser
import pandas as pd

parser = EmailParser()
parser.parse_directory('/path/to/archive')

# Convert to DataFrame for analysis
df = pd.DataFrame(parser.emails)

# Find all emails from a specific domain
company_emails = df[df['from'].str.contains('@company.com')]

# Group by date
df['date_only'] = pd.to_datetime(df['parsed_date']).dt.date
daily_counts = df.groupby('date_only').size()
```

### 2. Image Collection Management
```python
from epstein.image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer()
analyzer.scan_directory('/path/to/photos', recursive=True)

# Find large files (over 5MB)
large_images = analyzer.filter_by_size(min_size_mb=5)
print(f"Found {len(large_images)} large images")

# Identify duplicates to save space
duplicates = analyzer.find_duplicates()
duplicate_count = sum(len(files) - 1 for files in duplicates.values())
print(f"Can remove {duplicate_count} duplicate files")
```

### 3. Timeline Reconstruction
```python
from epstein.email_parser import EmailParser
import pandas as pd
import matplotlib.pyplot as plt

parser = EmailParser()
parser.parse_mbox('/path/to/mailbox.mbox')

df = pd.DataFrame(parser.emails)
df = df[df['parsed_date'].notna()]

# Plot email volume over time
df['date'] = pd.to_datetime(df['parsed_date']).dt.date
email_counts = df.groupby('date').size()
email_counts.plot(kind='line', figsize=(12, 6))
plt.title('Email Volume Timeline')
plt.xlabel('Date')
plt.ylabel('Number of Emails')
plt.show()
```

## Troubleshooting

### Import Errors
If you get import errors, make sure to add the src directory to your Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'src'))
```

### Memory Issues with Large Datasets
For very large datasets, process files in batches:
```python
# Process emails in batches
batch_size = 1000
for i in range(0, len(email_files), batch_size):
    batch = email_files[i:i+batch_size]
    # Process batch
```

### Missing Dependencies
Some optional features require additional packages:
```bash
# For PST file support
pip install libpff-python

# For advanced NLP
pip install nltk
python -m nltk.downloader stopwords
```

## Next Steps

- Read the full README.md for detailed documentation
- Explore the example scripts in the `examples/` directory
- Try the Jupyter notebook for interactive analysis
- Check the API documentation in each module's docstrings

## Getting Help

If you encounter issues:
1. Check this quick start guide
2. Review the README.md
3. Look at the example scripts
4. Examine the docstrings in the source code
5. Open an issue on GitHub
