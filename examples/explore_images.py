#!/usr/bin/env python3
"""
Example script for exploring image datasets.

This script demonstrates how to use the ImageAnalyzer to:
- Scan directories for images
- Extract metadata and EXIF data
- Find duplicate images
- Generate statistics
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from epstein.image_analyzer import ImageAnalyzer
from epstein.utils import export_to_json, export_to_csv


def main():
    """Main function to demonstrate image analysis."""
    
    # Initialize analyzer
    analyzer = ImageAnalyzer()
    
    print("Image Dataset Explorer")
    print("=" * 50)
    
    # Example 1: Scan a directory
    print("\n1. Scanning image directory...")
    image_dir = input("Enter path to image directory (or press Enter to skip): ").strip()
    
    if image_dir and Path(image_dir).exists():
        images = analyzer.scan_directory(image_dir, recursive=True)
        print(f"Found {len(images)} images")
    
    # Display statistics
    if analyzer.images:
        print("\n2. Image Statistics:")
        print("-" * 50)
        stats = analyzer.get_statistics()
        print(f"Total images: {stats['total_images']}")
        print(f"Total size: {stats['total_size_mb']} MB")
        print(f"\nFormats:")
        for fmt, count in stats.get('formats', {}).items():
            print(f"  {fmt}: {count}")
        
        if 'resolution_stats' in stats:
            res = stats['resolution_stats']
            print(f"\nResolution statistics:")
            print(f"  Average: {res['avg_width']}x{res['avg_height']}")
            print(f"  Max: {res['max_width']}x{res['max_height']}")
            print(f"  Min: {res['min_width']}x{res['min_height']}")
        
        # Example 2: Find duplicates
        print("\n3. Duplicate Detection:")
        print("-" * 50)
        duplicates = analyzer.find_duplicates()
        print(f"Found {stats['duplicate_groups']} groups of duplicates")
        print(f"Total duplicate files: {stats['total_duplicates']}")
        
        if duplicates and input("\nShow duplicate groups? (y/n): ").strip().lower() == 'y':
            for i, (hash_val, files) in enumerate(list(duplicates.items())[:5], 1):
                print(f"\nGroup {i} ({len(files)} files):")
                for filepath in files:
                    print(f"  - {filepath}")
        
        # Example 3: Filter by date
        print("\n4. Filter by Date:")
        print("-" * 50)
        days = input("Show images from last N days (or press Enter to skip): ").strip()
        
        if days and days.isdigit():
            end_date = datetime.now()
            start_date = end_date - timedelta(days=int(days))
            recent_images = analyzer.filter_by_date_range(start_date, end_date)
            print(f"Found {len(recent_images)} images from the last {days} days")
        
        # Example 4: Filter by size
        print("\n5. Filter by Size:")
        print("-" * 50)
        min_size = input("Minimum size in MB (or press Enter for 0): ").strip()
        max_size = input("Maximum size in MB (or press Enter for no limit): ").strip()
        
        min_mb = float(min_size) if min_size else 0
        max_mb = float(max_size) if max_size else float('inf')
        
        filtered = analyzer.filter_by_size(min_mb, max_mb)
        print(f"Found {len(filtered)} images between {min_mb} MB and {max_mb} MB")
        
        # Example 5: Export results
        print("\n6. Export results")
        export_choice = input("Export to JSON? (y/n): ").strip().lower()
        
        if export_choice == 'y':
            output_file = "image_analysis.json"
            export_to_json(analyzer.images, output_file)
            print(f"Results exported to {output_file}")
        
        export_csv = input("Export to CSV? (y/n): ").strip().lower()
        
        if export_csv == 'y':
            output_file = "image_analysis.csv"
            export_to_csv(analyzer.images, output_file)
            print(f"Results exported to {output_file}")
    else:
        print("\nNo images were found. Please provide a valid image directory.")
    
    print("\n" + "=" * 50)
    print("Image exploration complete!")


if __name__ == "__main__":
    main()
