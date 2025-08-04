"""
Readability Analyzer for Educational Resource Quality Evaluator.

This module provides readability analysis using various metrics including
Flesch-Kincaid Grade Level, Flesch Reading Ease, and other readability
formulas to assess the complexity of educational content.


"""

import re
import math
from typing import Dict, List, Any, Tuple
from utils import (
    count_words, count_sentences, count_syllables, 
    calculate_average_words_per_sentence, calculate_average_syllables_per_word,
    validate_grade_level, calculate_text_statistics
)


class ReadabilityAnalyzer:
    """
    Analyzes text readability using various metrics and formulas.
    
    This class provides comprehensive readability analysis including
    Flesch-Kincaid Grade Level, Flesch Reading Ease, and other
    readability formulas commonly used in educational assessment.
    """
    
    def __init__(self):
        """Initialize the readability analyzer."""
        # Define readability thresholds
        self.readability_thresholds = {
            'very_easy': (90, 100),
            'easy': (80, 89),
            'fairly_easy': (70, 79),
            'standard': (60, 69),
            'fairly_difficult': (50, 59),
            'difficult': (30, 49),
            'very_difficult': (0, 29)
        }
        
        # Grade level descriptions
        self.grade_level_descriptions = {
            (0, 5): "Elementary (K-5)",
            (6, 8): "Middle School (6-8)",
            (9, 12): "High School (9-12)",
            (13, 16): "College Level",
            (17, 20): "Advanced/Professional"
        }
    
    def analyze_readability(self, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive readability analysis.
        
        Args:
            content: Text content to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing readability analysis results
        """
        # Get basic text statistics
        stats = calculate_text_statistics(content)
        
        # Calculate readability scores
        flesch_kincaid_grade = self._calculate_flesch_kincaid_grade_level(content)
        flesch_reading_ease = self._calculate_flesch_reading_ease(content)
        gunning_fog_index = self._calculate_gunning_fog_index(content)
        smog_index = self._calculate_smog_index(content)
        
        # Validate and normalize scores
        flesch_kincaid_grade = validate_grade_level(flesch_kincaid_grade)
        
        # Get assessments
        grade_assessment = self._get_grade_level_assessment(flesch_kincaid_grade)
        reading_ease_assessment = self._get_reading_ease_assessment(flesch_reading_ease)
        
        # Calculate average readability metrics
        avg_words_per_sentence = stats['avg_words_per_sentence']
        avg_syllables_per_word = stats['avg_syllables_per_word']
        
        return {
            'grade_level': round(flesch_kincaid_grade, 1),
            'reading_ease': round(flesch_reading_ease, 1),
            'gunning_fog_index': round(gunning_fog_index, 1),
            'smog_index': round(smog_index, 1),
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'word_count': stats['word_count'],
            'sentence_count': stats['sentence_count'],
            'assessment': grade_assessment,
            'reading_ease_assessment': reading_ease_assessment,
            'complexity_level': self._get_complexity_level(flesch_kincaid_grade),
            'recommended_audience': self._get_recommended_audience(flesch_kincaid_grade)
        }
    
    def _calculate_flesch_kincaid_grade_level(self, content: str) -> float:
        """
        Calculate Flesch-Kincaid Grade Level.
        
        Formula: 0.39 × (total words ÷ total sentences) + 11.8 × (total syllables ÷ total words) - 15.59
        
        Args:
            content: Text content to analyze
            
        Returns:
            float: Flesch-Kincaid Grade Level
        """
        words = count_words(content)
        sentences = count_sentences(content)
        syllables = self._count_total_syllables(content)
        
        if words == 0 or sentences == 0:
            return 0.0
        
        # Flesch-Kincaid Grade Level formula
        grade_level = (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59
        
        return max(0.0, grade_level)
    
    def _calculate_flesch_reading_ease(self, content: str) -> float:
        """
        Calculate Flesch Reading Ease score.
        
        Formula: 206.835 - 1.015 × (total words ÷ total sentences) - 84.6 × (total syllables ÷ total words)
        
        Args:
            content: Text content to analyze
            
        Returns:
            float: Flesch Reading Ease score (0-100, higher is easier)
        """
        words = count_words(content)
        sentences = count_sentences(content)
        syllables = self._count_total_syllables(content)
        
        if words == 0 or sentences == 0:
            return 0.0
        
        # Flesch Reading Ease formula
        reading_ease = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
        
        return max(0.0, min(100.0, reading_ease))
    
    def _calculate_gunning_fog_index(self, content: str) -> float:
        """
        Calculate Gunning Fog Index.
        
        Formula: 0.4 × [(words ÷ sentences) + 100 × (complex words ÷ words)]
        
        Args:
            content: Text content to analyze
            
        Returns:
            float: Gunning Fog Index
        """
        words = count_words(content)
        sentences = count_sentences(content)
        complex_words = self._count_complex_words(content)
        
        if words == 0 or sentences == 0:
            return 0.0
        
        # Gunning Fog Index formula
        fog_index = 0.4 * ((words / sentences) + (100 * (complex_words / words)))
        
        return max(0.0, fog_index)
    
    def _calculate_smog_index(self, content: str) -> float:
        """
        Calculate SMOG Index.
        
        Formula: 1.043 × √(complex words × 30 ÷ sentences) + 3.1291
        
        Args:
            content: Text content to analyze
            
        Returns:
            float: SMOG Index
        """
        sentences = count_sentences(content)
        complex_words = self._count_complex_words(content)
        
        if sentences == 0:
            return 0.0
        
        # SMOG Index formula
        smog_index = 1.043 * math.sqrt(complex_words * 30 / sentences) + 3.1291
        
        return max(0.0, smog_index)
    
    def _count_total_syllables(self, content: str) -> int:
        """
        Count total syllables in content.
        
        Args:
            content: Text content to analyze
            
        Returns:
            int: Total number of syllables
        """
        words = re.findall(r'\b\w+\b', content.lower())
        return sum(count_syllables(word) for word in words)
    
    def _count_complex_words(self, content: str) -> int:
        """
        Count complex words (words with 3+ syllables).
        
        Args:
            content: Text content to analyze
            
        Returns:
            int: Number of complex words
        """
        words = re.findall(r'\b\w+\b', content.lower())
        complex_words = 0
        
        for word in words:
            # Skip common suffixes that don't add complexity
            if word.endswith(('es', 'ed', 'ing')):
                word = word[:-2] if word.endswith('es') else word[:-3]
            
            if count_syllables(word) >= 3:
                complex_words += 1
        
        return complex_words
    
    def _get_grade_level_assessment(self, grade_level: float) -> str:
        """
        Get assessment based on grade level.
        
        Args:
            grade_level: Flesch-Kincaid Grade Level
            
        Returns:
            str: Assessment description
        """
        if grade_level <= 5:
            return "Appropriate for elementary students"
        elif grade_level <= 8:
            return "Appropriate for middle school students"
        elif grade_level <= 12:
            return "Appropriate for high school students"
        elif grade_level <= 16:
            return "Appropriate for college students"
        else:
            return "Advanced level, suitable for specialized audiences"
    
    def _get_reading_ease_assessment(self, reading_ease: float) -> str:
        """
        Get assessment based on reading ease score.
        
        Args:
            reading_ease: Flesch Reading Ease score
            
        Returns:
            str: Assessment description
        """
        if reading_ease >= 90:
            return "Very easy to read"
        elif reading_ease >= 80:
            return "Easy to read"
        elif reading_ease >= 70:
            return "Fairly easy to read"
        elif reading_ease >= 60:
            return "Standard reading level"
        elif reading_ease >= 50:
            return "Fairly difficult to read"
        elif reading_ease >= 30:
            return "Difficult to read"
        else:
            return "Very difficult to read"
    
    def _get_complexity_level(self, grade_level: float) -> str:
        """
        Get complexity level description.
        
        Args:
            grade_level: Flesch-Kincaid Grade Level
            
        Returns:
            str: Complexity level description
        """
        for (min_grade, max_grade), description in self.grade_level_descriptions.items():
            if min_grade <= grade_level <= max_grade:
                return description
        
        return "Advanced/Professional"
    
    def _get_recommended_audience(self, grade_level: float) -> str:
        """
        Get recommended audience based on grade level.
        
        Args:
            grade_level: Flesch-Kincaid Grade Level
            
        Returns:
            str: Recommended audience
        """
        if grade_level <= 3:
            return "Early elementary students (K-3)"
        elif grade_level <= 5:
            return "Upper elementary students (4-5)"
        elif grade_level <= 8:
            return "Middle school students (6-8)"
        elif grade_level <= 12:
            return "High school students (9-12)"
        elif grade_level <= 16:
            return "College students and adults"
        else:
            return "Specialized professionals and experts"
    
    def analyze_paragraph_readability(self, content: str) -> List[Dict[str, Any]]:
        """
        Analyze readability for each paragraph separately.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List[Dict[str, Any]]: List of paragraph readability analyses
        """
        paragraphs = re.split(r'\n\s*\n', content.strip())
        paragraph_analyses = []
        
        for i, paragraph in enumerate(paragraphs, 1):
            if paragraph.strip():
                analysis = self.analyze_readability(paragraph.strip())
                analysis['paragraph_number'] = i
                analysis['paragraph_text'] = paragraph.strip()[:100] + "..." if len(paragraph.strip()) > 100 else paragraph.strip()
                paragraph_analyses.append(analysis)
        
        return paragraph_analyses
    
    def get_readability_recommendations(self, readability_results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on readability analysis.
        
        Args:
            readability_results: Results from readability analysis
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        grade_level = readability_results['grade_level']
        reading_ease = readability_results['reading_ease']
        avg_words_per_sentence = readability_results['avg_words_per_sentence']
        avg_syllables_per_word = readability_results['avg_syllables_per_word']
        
        # Check grade level appropriateness
        if grade_level > 12:
            recommendations.append("Consider simplifying language for broader accessibility")
        elif grade_level < 5:
            recommendations.append("Content may be too simple for target audience")
        
        # Check reading ease
        if reading_ease < 50:
            recommendations.append("Text is difficult to read - consider simplifying sentence structure")
        elif reading_ease > 90:
            recommendations.append("Text is very easy - may need more complexity for target audience")
        
        # Check sentence length
        if avg_words_per_sentence > 20:
            recommendations.append("Sentences are long - consider breaking them into shorter sentences")
        elif avg_words_per_sentence < 8:
            recommendations.append("Sentences are very short - consider combining some for better flow")
        
        # Check word complexity
        if avg_syllables_per_word > 2.0:
            recommendations.append("Words are complex - consider using simpler vocabulary")
        elif avg_syllables_per_word < 1.3:
            recommendations.append("Vocabulary is very simple - may need more sophisticated terms")
        
        if not recommendations:
            recommendations.append("Readability is appropriate for the target audience")
        
        return recommendations
    
    def compare_readability_formulas(self, content: str) -> Dict[str, Any]:
        """
        Compare different readability formulas for the same content.
        
        Args:
            content: Text content to analyze
            
        Returns:
            Dict[str, Any]: Comparison of different readability formulas
        """
        # Calculate all formulas
        flesch_kincaid = self._calculate_flesch_kincaid_grade_level(content)
        flesch_ease = self._calculate_flesch_reading_ease(content)
        gunning_fog = self._calculate_gunning_fog_index(content)
        smog = self._calculate_smog_index(content)
        
        # Calculate average grade level
        grade_levels = [flesch_kincaid, gunning_fog, smog]
        avg_grade = sum(grade_levels) / len(grade_levels)
        
        return {
            'flesch_kincaid_grade': round(flesch_kincaid, 1),
            'flesch_reading_ease': round(flesch_ease, 1),
            'gunning_fog_index': round(gunning_fog, 1),
            'smog_index': round(smog, 1),
            'average_grade_level': round(avg_grade, 1),
            'formula_agreement': self._assess_formula_agreement(grade_levels)
        }
    
    def _assess_formula_agreement(self, grade_levels: List[float]) -> str:
        """
        Assess how well different formulas agree on grade level.
        
        Args:
            grade_levels: List of grade levels from different formulas
            
        Returns:
            str: Assessment of formula agreement
        """
        if not grade_levels:
            return "Insufficient data"
        
        min_grade = min(grade_levels)
        max_grade = max(grade_levels)
        range_diff = max_grade - min_grade
        
        if range_diff <= 2:
            return "High agreement between formulas"
        elif range_diff <= 4:
            return "Moderate agreement between formulas"
        else:
            return "Low agreement between formulas - content may be complex" 