"""Image analyzer for extracting metadata and analyzing image datasets."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import hashlib


class ImageAnalyzer:
    """Analyze images and extract metadata."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the image analyzer.
        
        Args:
            data_dir: Directory containing image files
        """
        self.data_dir = Path(data_dir) if data_dir else None
        self.images = []
        
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Scan directory for image files.
        
        Args:
            directory: Directory path to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of dictionaries containing image metadata
        """
        dir_path = Path(directory)
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        images = []
        
        if recursive:
            pattern = '**/*'
        else:
            pattern = '*'
        
        for filepath in dir_path.glob(pattern):
            if filepath.is_file() and filepath.suffix.lower() in image_extensions:
                try:
                    image_data = self._extract_basic_metadata(filepath)
                    images.append(image_data)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
        
        self.images.extend(images)
        return images
    
    def _extract_basic_metadata(self, filepath: Path) -> Dict[str, Any]:
        """
        Extract basic metadata from an image file.
        
        Args:
            filepath: Path to the image file
            
        Returns:
            Dictionary containing image metadata
        """
        stat = filepath.stat()
        
        # Calculate file hash
        file_hash = self._calculate_file_hash(filepath)
        
        metadata = {
            'filepath': str(filepath),
            'filename': filepath.name,
            'extension': filepath.suffix.lower(),
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified_time': datetime.fromtimestamp(stat.st_mtime),
            'created_time': datetime.fromtimestamp(stat.st_ctime),
            'file_hash': file_hash
        }
        
        # Try to extract image dimensions and EXIF data
        try:
            from PIL import Image
            with Image.open(filepath) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                metadata['mode'] = img.mode
                
                # Extract EXIF data if available
                exif_data = self._extract_exif_data(img)
                if exif_data:
                    metadata['exif'] = exif_data
        except Exception as e:
            metadata['error'] = str(e)
        
        return metadata
    
    def _extract_exif_data(self, img) -> Optional[Dict[str, Any]]:
        """
        Extract EXIF data from an image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Dictionary containing EXIF data or None
        """
        try:
            exif = img.getexif()
            if not exif:
                return None
            
            # Extract common EXIF tags
            exif_data = {}
            
            # Common EXIF tag IDs
            tags = {
                271: 'Make',
                272: 'Model',
                274: 'Orientation',
                306: 'DateTime',
                36867: 'DateTimeOriginal',
                36868: 'DateTimeDigitized',
                37377: 'ShutterSpeedValue',
                37378: 'ApertureValue',
                37379: 'BrightnessValue',
                37380: 'ExposureBiasValue',
                37381: 'MaxApertureValue',
                37382: 'SubjectDistance',
                37383: 'MeteringMode',
                37384: 'LightSource',
                37385: 'Flash',
                37386: 'FocalLength',
                34850: 'ExposureProgram',
                34855: 'ISOSpeedRatings',
            }
            
            for tag_id, tag_name in tags.items():
                if tag_id in exif:
                    exif_data[tag_name] = exif[tag_id]
            
            return exif_data if exif_data else None
        except Exception:
            return None
    
    def _calculate_file_hash(self, filepath: Path, algorithm: str = 'sha256') -> str:
        """
        Calculate hash of a file.
        
        Args:
            filepath: Path to the file
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string
        """
        hash_obj = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def find_duplicates(self) -> Dict[str, List[str]]:
        """
        Find duplicate images based on file hash.
        
        Returns:
            Dictionary mapping hashes to lists of duplicate file paths
        """
        hash_to_files = {}
        
        for image_data in self.images:
            file_hash = image_data.get('file_hash')
            filepath = image_data.get('filepath')
            
            if file_hash:
                if file_hash not in hash_to_files:
                    hash_to_files[file_hash] = []
                hash_to_files[file_hash].append(filepath)
        
        # Filter to only duplicates
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
        
        return duplicates
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the image collection.
        
        Returns:
            Dictionary containing image statistics
        """
        if not self.images:
            return {
                'total_images': 0,
                'error': 'No images have been scanned yet'
            }
        
        total_size = sum(img.get('size_bytes', 0) for img in self.images)
        
        # Count by format
        formats = {}
        for img in self.images:
            fmt = img.get('format', 'Unknown')
            formats[fmt] = formats.get(fmt, 0) + 1
        
        # Find duplicates
        duplicates = self.find_duplicates()
        
        # Resolution statistics
        widths = [img.get('width', 0) for img in self.images if 'width' in img]
        heights = [img.get('height', 0) for img in self.images if 'height' in img]
        
        stats = {
            'total_images': len(self.images),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'formats': formats,
            'duplicate_groups': len(duplicates),
            'total_duplicates': sum(len(files) - 1 for files in duplicates.values()),
        }
        
        if widths and heights:
            stats['resolution_stats'] = {
                'avg_width': round(sum(widths) / len(widths)),
                'avg_height': round(sum(heights) / len(heights)),
                'max_width': max(widths),
                'max_height': max(heights),
                'min_width': min(widths),
                'min_height': min(heights),
            }
        
        return stats
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Filter images by modification date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of images within the date range
        """
        filtered = []
        
        for img in self.images:
            mod_time = img.get('modified_time')
            if mod_time and start_date <= mod_time <= end_date:
                filtered.append(img)
        
        return filtered
    
    def filter_by_size(self, min_size_mb: float = 0, max_size_mb: float = float('inf')) -> List[Dict[str, Any]]:
        """
        Filter images by file size.
        
        Args:
            min_size_mb: Minimum size in megabytes
            max_size_mb: Maximum size in megabytes
            
        Returns:
            List of images within the size range
        """
        filtered = []
        
        for img in self.images:
            size_mb = img.get('size_mb', 0)
            if min_size_mb <= size_mb <= max_size_mb:
                filtered.append(img)
        
        return filtered
