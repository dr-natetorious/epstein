#!/usr/bin/env python3
"""
Example script for exploring email dumps.

This script demonstrates how to use the EmailParser to:
- Parse email files from various formats
- Extract metadata and content
- Search for specific keywords
- Generate statistics
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from epstein.email_parser import EmailParser
from epstein.utils import export_to_json, export_to_csv


def main():
    """Main function to demonstrate email parsing."""
    
    # Initialize parser
    parser = EmailParser()
    
    print("Email Dump Explorer")
    print("=" * 50)
    
    # Example 1: Parse a directory of EML files
    print("\n1. Parsing email directory...")
    email_dir = input("Enter path to email directory (or press Enter to skip): ").strip()
    
    if email_dir and Path(email_dir).exists():
        emails = parser.parse_directory(email_dir)
        print(f"Parsed {len(emails)} emails")
    
    # Example 2: Parse an MBOX file
    print("\n2. Parsing MBOX file...")
    mbox_path = input("Enter path to MBOX file (or press Enter to skip): ").strip()
    
    if mbox_path and Path(mbox_path).exists():
        emails = parser.parse_mbox(mbox_path)
        print(f"Parsed {len(emails)} emails from MBOX")
    
    # Display statistics
    if parser.emails:
        print("\n3. Email Statistics:")
        print("-" * 50)
        stats = parser.get_email_statistics()
        print(f"Total emails: {stats['total_emails']}")
        print(f"Total attachments: {stats['total_attachments']}")
        print(f"Unique sender domains: {stats['unique_sender_domains']}")
        
        if stats.get('date_range'):
            print(f"Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        
        # Example 3: Search emails
        print("\n4. Search emails")
        keyword = input("Enter keyword to search (or press Enter to skip): ").strip()
        
        if keyword:
            results = parser.search_emails(keyword, field='body')
            print(f"Found {len(results)} emails containing '{keyword}'")
            
            if results:
                print("\nFirst 3 matches:")
                for i, email in enumerate(results[:3], 1):
                    print(f"\n  {i}. From: {email['from']}")
                    print(f"     Subject: {email['subject']}")
                    print(f"     Date: {email['date']}")
        
        # Example 4: Export results
        print("\n5. Export results")
        export_choice = input("Export to JSON? (y/n): ").strip().lower()
        
        if export_choice == 'y':
            output_file = "email_analysis.json"
            export_to_json(parser.emails, output_file)
            print(f"Results exported to {output_file}")
        
        export_csv = input("Export to CSV? (y/n): ").strip().lower()
        
        if export_csv == 'y':
            output_file = "email_analysis.csv"
            export_to_csv(parser.emails, output_file)
            print(f"Results exported to {output_file}")
    else:
        print("\nNo emails were parsed. Please provide valid email files or directories.")
    
    print("\n" + "=" * 50)
    print("Email exploration complete!")


if __name__ == "__main__":
    main()
