"""Export utilities for saving analysis results."""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any


def export_to_json(data: List[Dict[str, Any]], filepath: str, indent: int = 2) -> None:
    """
    Export data to JSON file.
    
    Args:
        data: List of dictionaries to export
        filepath: Output file path
        indent: JSON indentation level
    """
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert datetime objects to strings
    serializable_data = []
    for item in data:
        serializable_item = {}
        for key, value in item.items():
            if hasattr(value, 'isoformat'):
                serializable_item[key] = value.isoformat()
            elif isinstance(value, (list, dict)):
                serializable_item[key] = str(value)
            else:
                serializable_item[key] = value
        serializable_data.append(serializable_item)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, indent=indent, ensure_ascii=False)
    
    print(f"Exported {len(data)} records to {filepath}")


def export_to_csv(data: List[Dict[str, Any]], filepath: str) -> None:
    """
    Export data to CSV file.
    
    Args:
        data: List of dictionaries to export
        filepath: Output file path
    """
    if not data:
        print("No data to export")
        return
    
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get all unique keys
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            row = {}
            for key, value in item.items():
                if hasattr(value, 'isoformat'):
                    row[key] = value.isoformat()
                elif isinstance(value, (list, dict)):
                    row[key] = str(value)
                else:
                    row[key] = value
            writer.writerow(row)
    
    print(f"Exported {len(data)} records to {filepath}")
