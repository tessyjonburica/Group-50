"""
Utility functions for the Educational Resource Quality Evaluator.

This module provides shared helper functions for text processing,
input/output formatting, file validation, and other common operations
used across the evaluation components.

"""

import os
import re
from typing import List, Dict, Any, Optional


def clear_screen():
    """Clear the terminal screen for better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is accessible.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        bool: True if file exists and is accessible, False otherwise
    """
    try:
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    except (OSError, ValueError):
        return False


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis.
    
    Args:
        text: Raw text to clean
        
    Returns:
        str: Cleaned text with normalized whitespace and punctuation
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Normalize punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    return text


def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs based on double line breaks.
    
    Args:
        text: Text to split into paragraphs
        
    Returns:
        List[str]: List of paragraphs
    """
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def count_syllables(word: str) -> int:
    """
    Count syllables in a word using basic heuristics.
    
    Args:
        word: Word to count syllables for
        
    Returns:
        int: Number of syllables
    """
    word = word.lower()
    if word.endswith('e'):
        word = word[:-1]
    
    # Count vowel groups
    vowels = re.findall(r'[aeiouy]+', word)
    return max(1, len(vowels))


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        int: Number of words
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)


def count_sentences(text: str) -> int:
    """
    Count sentences in text.
    
    Args:
        text: Text to count sentences in
        
    Returns:
        int: Number of sentences
    """
    # Split on sentence endings followed by space or end of string
    sentences = re.split(r'[.!?]+(?:\s|$)', text)
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def calculate_average_words_per_sentence(text: str) -> float:
    """
    Calculate average words per sentence.
    
    Args:
        text: Text to analyze
        
    Returns:
        float: Average words per sentence
    """
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    
    if sentence_count == 0:
        return 0.0
    
    return word_count / sentence_count


def calculate_average_syllables_per_word(text: str) -> float:
    """
    Calculate average syllables per word.
    
    Args:
        text: Text to analyze
        
    Returns:
        float: Average syllables per word
    """
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return 0.0
    
    total_syllables = sum(count_syllables(word) for word in words)
    return total_syllables / len(words)


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum word length to consider as keyword
        
    Returns:
        List[str]: List of keywords
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [word for word in words if len(word) >= min_length and word not in stop_words]
    
    return keywords


def calculate_text_statistics(text: str) -> Dict[str, Any]:
    """
    Calculate comprehensive text statistics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dict[str, Any]: Dictionary containing various text statistics
    """
    words = count_words(text)
    sentences = count_sentences(text)
    paragraphs = len(split_into_paragraphs(text))
    
    stats = {
        'word_count': words,
        'sentence_count': sentences,
        'paragraph_count': paragraphs,
        'avg_words_per_sentence': calculate_average_words_per_sentence(text),
        'avg_syllables_per_word': calculate_average_syllables_per_word(text),
        'avg_words_per_paragraph': words / paragraphs if paragraphs > 0 else 0
    }
    
    return stats











def validate_grade_level(grade_level: float) -> float:
    """
    Validate and constrain grade level to reasonable range.
    
    Args:
        grade_level: Raw grade level
        
    Returns:
        float: Validated grade level (0-20)
    """
    return max(0.0, min(20.0, grade_level))


def format_timestamp() -> str:
    """
    Get current timestamp in readable format.
    
    Returns:
        str: Formatted timestamp
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")





 