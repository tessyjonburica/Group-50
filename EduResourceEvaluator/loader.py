"""
Material Loader for Educational Resource Quality Evaluator.

This module handles loading and parsing of educational materials from
various file formats (TXT, CSV) and provides validation for content
structure and format.


"""

import os
import csv
import re
from typing import Dict, List, Any, Optional
from utils import clean_text, split_into_paragraphs, validate_file_path


class MaterialLoader:
    """
    Handles loading and parsing of educational materials from files.
    
    This class provides methods to load educational content from various
    file formats, validate the content structure, and prepare it for
    analysis by other evaluation components.
    """
    
    def __init__(self):
        """Initialize the material loader."""
        self.supported_formats = ['.txt', '.csv']
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
    
    def load_material(self, file_path: str) -> Dict[str, Any]:
        """
        Load educational material from file.
        
        Args:
            file_path: Path to the educational material file
            
        Returns:
            Dict[str, Any]: Dictionary containing loaded material data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
            IOError: If file cannot be read
        """
        # Validate file path
        if not validate_file_path(file_path):
            raise FileNotFoundError(f"File not found or not accessible: {file_path}")
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            raise ValueError(f"File too large ({file_size} bytes). Maximum size is {self.max_file_size} bytes.")
        
        # Determine file format and load accordingly
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            return self._load_txt_file(file_path)
        elif file_extension == '.csv':
            return self._load_csv_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(self.supported_formats)}")
    
    def _load_txt_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load content from a TXT file.
        
        Args:
            file_path: Path to the TXT file
            
        Returns:
            Dict[str, Any]: Dictionary containing loaded material data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Clean and process content
            cleaned_content = clean_text(content)
            paragraphs = split_into_paragraphs(cleaned_content)
            
            # Validate content
            if not cleaned_content.strip():
                raise ValueError("File appears to be empty or contains no readable content")
            
            return {
                'file_path': file_path,
                'file_type': 'txt',
                'content': cleaned_content,
                'paragraphs': paragraphs,
                'original_content': content,
                'metadata': self._extract_metadata(content)
            }
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                
                cleaned_content = clean_text(content)
                paragraphs = split_into_paragraphs(cleaned_content)
                
                return {
                    'file_path': file_path,
                    'file_type': 'txt',
                    'content': cleaned_content,
                    'paragraphs': paragraphs,
                    'original_content': content,
                    'metadata': self._extract_metadata(content)
                }
            except UnicodeDecodeError:
                raise ValueError("Unable to decode file content. Please ensure the file contains valid text.")
    
    def _load_csv_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load content from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dict[str, Any]: Dictionary containing loaded material data
        """
        try:
            content_parts = []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                for row_num, row in enumerate(csv_reader, 1):
                    if row:  # Skip empty rows
                        # Join row elements with spaces
                        row_content = ' '.join(str(cell) for cell in row if cell.strip())
                        if row_content:
                            content_parts.append(row_content)
            
            if not content_parts:
                raise ValueError("CSV file appears to be empty or contains no readable content")
            
            # Combine all content
            full_content = '\n\n'.join(content_parts)
            cleaned_content = clean_text(full_content)
            paragraphs = split_into_paragraphs(cleaned_content)
            
            return {
                'file_path': file_path,
                'file_type': 'csv',
                'content': cleaned_content,
                'paragraphs': paragraphs,
                'original_content': full_content,
                'metadata': self._extract_metadata(full_content)
            }
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                content_parts = []
                
                with open(file_path, 'r', encoding='latin-1') as file:
                    csv_reader = csv.reader(file)
                    
                    for row_num, row in enumerate(csv_reader, 1):
                        if row:
                            row_content = ' '.join(str(cell) for cell in row if cell.strip())
                            if row_content:
                                content_parts.append(row_content)
                
                if not content_parts:
                    raise ValueError("CSV file appears to be empty or contains no readable content")
                
                full_content = '\n\n'.join(content_parts)
                cleaned_content = clean_text(full_content)
                paragraphs = split_into_paragraphs(cleaned_content)
                
                return {
                    'file_path': file_path,
                    'file_type': 'csv',
                    'content': cleaned_content,
                    'paragraphs': paragraphs,
                    'original_content': full_content,
                    'metadata': self._extract_metadata(full_content)
                }
            except UnicodeDecodeError:
                raise ValueError("Unable to decode CSV file content. Please ensure the file contains valid text.")
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """
        Extract metadata from content.
        
        Args:
            content: Raw content to extract metadata from
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted metadata
        """
        metadata = {
            'title': None,
            'author': None,
            'subject': None,
            'grade_level': None,
            'date_created': None
        }
        
        # Look for title patterns
        title_patterns = [
            r'Title:\s*(.+)',
            r'Subject:\s*(.+)',
            r'Chapter\s+\d+:\s*(.+)',
            r'Lesson\s+\d+:\s*(.+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and not metadata['title']:
                metadata['title'] = match.group(1).strip()
                break
        
        # Look for author patterns
        author_patterns = [
            r'Author:\s*(.+)',
            r'By:\s*(.+)',
            r'Written by:\s*(.+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and not metadata['author']:
                metadata['author'] = match.group(1).strip()
                break
        
        # Look for subject patterns
        subject_patterns = [
            r'Subject:\s*(.+)',
            r'Topic:\s*(.+)',
            r'Course:\s*(.+)'
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and not metadata['subject']:
                metadata['subject'] = match.group(1).strip()
                break
        
        # Look for grade level patterns
        grade_patterns = [
            r'Grade\s+Level:\s*(.+)',
            r'Grade:\s*(.+)',
            r'Level:\s*(.+)'
        ]
        
        for pattern in grade_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and not metadata['grade_level']:
                metadata['grade_level'] = match.group(1).strip()
                break
        
        # Look for date patterns
        date_patterns = [
            r'Date:\s*(.+)',
            r'Created:\s*(.+)',
            r'Published:\s*(.+)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and not metadata['date_created']:
                metadata['date_created'] = match.group(1).strip()
                break
        
        return metadata
    
    def validate_content_structure(self, material_data: Dict[str, Any]) -> bool:
        """
        Validate the structure of loaded material.
        
        Args:
            material_data: Dictionary containing loaded material data
            
        Returns:
            bool: True if structure is valid, False otherwise
        """
        required_keys = ['content', 'paragraphs', 'file_path', 'file_type']
        
        # Check required keys
        for key in required_keys:
            if key not in material_data:
                return False
        
        # Check content is not empty
        if not material_data['content'].strip():
            return False
        
        # Check at least one paragraph
        if not material_data['paragraphs']:
            return False
        
        # Check file path is valid
        if not os.path.exists(material_data['file_path']):
            return False
        
        return True
    
    def get_content_summary(self, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the loaded content.
        
        Args:
            material_data: Dictionary containing loaded material data
            
        Returns:
            Dict[str, Any]: Dictionary containing content summary
        """
        content = material_data['content']
        paragraphs = material_data['paragraphs']
        
        # Count basic statistics
        word_count = len(re.findall(r'\b\w+\b', content.lower()))
        sentence_count = len(re.findall(r'[.!?]+', content))
        character_count = len(content)
        
        # Calculate average paragraph length
        avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'character_count': character_count,
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': avg_paragraph_length,
            'file_size': os.path.getsize(material_data['file_path']),
            'file_type': material_data['file_type']
        }
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.
        
        Returns:
            List[str]: List of supported file extensions
        """
        return self.supported_formats.copy() 