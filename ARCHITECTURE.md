# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Epstein Exploration Toolkit                │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
        ┌───────▼────────┐         ┌───────▼────────┐
        │  Email Parser  │         │ Image Analyzer │
        │    Module      │         │     Module     │
        └───────┬────────┘         └───────┬────────┘
                │                           │
    ┌───────────┼───────────┐   ┌───────────┼───────────┐
    │           │           │   │           │           │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐ │  ┌────▼────┐  ┌────▼────┐
│  EML  │  │ MBOX  │  │  PST  │ │  │  Scan   │  │ Extract │
│Parser │  │Parser │  │Parser │ │  │Directory│  │  EXIF   │
└───┬───┘  └───┬───┘  └───┬───┘ │  └────┬────┘  └────┬────┘
    │          │          │     │       │            │
    └──────────┼──────────┘     │       │            │
               │                │   ┌───▼────┐  ┌────▼────┐
         ┌─────▼─────┐          │   │  Hash  │  │ Filter  │
         │  Extract  │          │   │  Files │  │ Images  │
         │ Metadata  │          │   └───┬────┘  └────┬────┘
         └─────┬─────┘          │       │            │
               │                │       └─────┬──────┘
         ┌─────▼─────┐          │             │
         │  Search   │          │      ┌──────▼──────┐
         │   Text    │          │      │Find Duplicate│
         └─────┬─────┘          │      └──────┬──────┘
               │                │             │
               └────────┬───────┴─────────────┘
                        │
                ┌───────▼────────┐
                │  Utility Layer │
                │  (Export/Stats)│
                └───────┬────────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
        ┌───▼───┐   ┌───▼───┐  ┌───▼────┐
        │  JSON │   │  CSV  │  │ Stats  │
        │Export │   │Export │  │ Report │
        └───────┘   └───────┘  └────────┘
```

## User Interfaces

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼───────┐ ┌───▼────┐ ┌─────▼──────┐
        │  CLI Scripts  │ │Python  │ │  Jupyter   │
        │  (Interactive)│ │  API   │ │  Notebook  │
        └───────┬───────┘ └───┬────┘ └─────┬──────┘
                │             │            │
                └─────────────┼────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Core Modules    │
                    │ (Email + Image)   │
                    └───────────────────┘
```

## Data Flow

### Email Processing Flow
```
Input Sources        Processing           Output
─────────────       ──────────          ────────

┌─────────┐         ┌──────────┐       ┌─────────┐
│ .eml    │────────▶│  Parse   │──────▶│ Email   │
│ files   │         │  Headers │       │ Objects │
└─────────┘         └──────────┘       └────┬────┘
                                             │
┌─────────┐         ┌──────────┐            │
│ .mbox   │────────▶│  Extract │            │
│ files   │         │   Body   │            │
└─────────┘         └──────────┘            │
                                             │
┌─────────┐         ┌──────────┐            │
│ .pst    │────────▶│  Track   │            │
│ files   │         │Attachment│            │
└─────────┘         └──────────┘            │
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │  Search  │──────▶│ Search  │
                    │ Keywords │       │ Results │
                    └──────────┘       └─────────┘
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │Generate  │──────▶│Statistics│
                    │  Stats   │       └─────────┘
                    └──────────┘             │
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │  Export  │──────▶│JSON/CSV │
                    └──────────┘       └─────────┘
```

### Image Processing Flow
```
Input Sources        Processing           Output
─────────────       ──────────          ────────

┌─────────┐         ┌──────────┐       ┌─────────┐
│Image    │────────▶│  Scan    │──────▶│ Image   │
│Directory│         │  Files   │       │ List    │
└─────────┘         └──────────┘       └────┬────┘
                                             │
                    ┌──────────┐            │
                    │ Extract  │            │
                    │ Metadata │            │
                    └──────────┘            │
                                             │
                    ┌──────────┐            │
                    │ Read     │            │
                    │  EXIF    │            │
                    └──────────┘            │
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │Calculate │──────▶│  Hash   │
                    │  Hash    │       │  Table  │
                    └──────────┘       └────┬────┘
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │  Find    │──────▶│Duplicate│
                    │Duplicates│       │ Groups  │
                    └──────────┘       └─────────┘
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │  Filter  │──────▶│Filtered │
                    │Date/Size │       │  List   │
                    └──────────┘       └─────────┘
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │Generate  │──────▶│Statistics│
                    │  Stats   │       └─────────┘
                    └──────────┘             │
                                             │
                    ┌──────────┐       ┌────▼────┐
                    │  Export  │──────▶│JSON/CSV │
                    └──────────┘       └─────────┘
```

## Module Dependencies

```
┌─────────────────────────────────────────────┐
│          External Dependencies              │
│  (email, mailbox, pathlib, hashlib, PIL)   │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼──────┐ ┌────▼────┐ ┌─────▼────┐
│  email   │ │  image  │ │  utils   │
│ _parser  │ │_analyzer│ │          │
└───┬──────┘ └────┬────┘ └─────┬────┘
    │             │            │
    └─────────────┼────────────┘
                  │
          ┌───────▼────────┐
          │   Examples     │
          │  & Notebooks   │
          └────────────────┘
```

## Use Case Scenarios

### Scenario 1: Forensic Email Analysis
```
User → explore_emails.py → Email Parser
                                │
                                ├─ Parse MBOX archive
                                ├─ Search for keywords
                                ├─ Extract date range
                                └─ Export to CSV → Excel Analysis
```

### Scenario 2: Image Collection Management
```
User → explore_images.py → Image Analyzer
                                │
                                ├─ Scan directory
                                ├─ Find duplicates
                                ├─ Check file sizes
                                └─ Export report → Cleanup Script
```

### Scenario 3: Interactive Research
```
User → Jupyter Notebook → Both Modules
                                │
                                ├─ Load data
                                ├─ Visualize trends
                                ├─ Filter results
                                └─ Export findings → Publication
```

## Performance Considerations

### Email Processing
- Streaming for large MBOX files
- Lazy evaluation of body content
- Incremental statistics updates

### Image Processing
- Directory scanning with generators
- Hash calculation in chunks
- Optional EXIF extraction

### Memory Management
- Process files individually
- Clear intermediate data
- Export in batches for large datasets

## Security Features

✓ No external API calls
✓ Local file processing only
✓ No credential storage
✓ Safe file handling
✓ Input validation
✓ Error handling
✓ Read-only operations (no file modification)
