"""
Unit tests for the Readability Analyzer module.

This module contains comprehensive tests for the ReadabilityAnalyzer class,
testing all readability formulas and analysis methods.

"""

import unittest
from readability import ReadabilityAnalyzer


class TestReadabilityAnalyzer(unittest.TestCase):
    """Test cases for ReadabilityAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ReadabilityAnalyzer()
        
        # Test content samples
        self.simple_text = "This is a simple sentence. It has few words. It is easy to read."
        self.complex_text = "The sophisticated implementation of multifaceted algorithms necessitates comprehensive understanding of computational complexity and theoretical foundations."
        self.empty_text = ""
        self.single_word = "Hello"
    
    def test_flesch_kincaid_grade_level(self):
        """Test Flesch-Kincaid Grade Level calculation."""
        # Test simple text
        result = self.analyzer._calculate_flesch_kincaid_grade_level(self.simple_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        
        # Test complex text
        result = self.analyzer._calculate_flesch_kincaid_grade_level(self.complex_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        
        # Test empty text
        result = self.analyzer._calculate_flesch_kincaid_grade_level(self.empty_text)
        self.assertEqual(result, 0.0)
    
    def test_flesch_reading_ease(self):
        """Test Flesch Reading Ease calculation."""
        # Test simple text
        result = self.analyzer._calculate_flesch_reading_ease(self.simple_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 100.0)
        
        # Test complex text
        result = self.analyzer._calculate_flesch_reading_ease(self.complex_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 100.0)
    
    def test_gunning_fog_index(self):
        """Test Gunning Fog Index calculation."""
        result = self.analyzer._calculate_gunning_fog_index(self.simple_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
    
    def test_smog_index(self):
        """Test SMOG Index calculation."""
        result = self.analyzer._calculate_smog_index(self.simple_text)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
    
    def test_count_total_syllables(self):
        """Test total syllable counting."""
        result = self.analyzer._count_total_syllables(self.simple_text)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
    
    def test_count_complex_words(self):
        """Test complex word counting."""
        result = self.analyzer._count_complex_words(self.simple_text)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
    
    def test_analyze_readability(self):
        """Test comprehensive readability analysis."""
        result = self.analyzer.analyze_readability(self.simple_text)
        
        # Check required keys
        required_keys = [
            'grade_level', 'reading_ease', 'gunning_fog_index', 'smog_index',
            'avg_words_per_sentence', 'avg_syllables_per_word', 'word_count',
            'sentence_count', 'assessment', 'reading_ease_assessment',
            'complexity_level', 'recommended_audience'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check data types
        self.assertIsInstance(result['grade_level'], float)
        self.assertIsInstance(result['reading_ease'], float)
        self.assertIsInstance(result['assessment'], str)
    
    def test_grade_level_assessment(self):
        """Test grade level assessment."""
        # Test elementary level
        assessment = self.analyzer._get_grade_level_assessment(3.0)
        self.assertIn("elementary", assessment.lower())
        
        # Test high school level
        assessment = self.analyzer._get_grade_level_assessment(10.0)
        self.assertIn("high school", assessment.lower())
        
        # Test college level
        assessment = self.analyzer._get_grade_level_assessment(15.0)
        self.assertIn("college", assessment.lower())
    
    def test_reading_ease_assessment(self):
        """Test reading ease assessment."""
        # Test easy reading
        assessment = self.analyzer._get_reading_ease_assessment(85.0)
        self.assertIn("easy", assessment.lower())
        
        # Test difficult reading
        assessment = self.analyzer._get_reading_ease_assessment(25.0)
        self.assertIn("difficult", assessment.lower())
    
    def test_complexity_level(self):
        """Test complexity level determination."""
        # Test elementary
        level = self.analyzer._get_complexity_level(3.0)
        self.assertIn("Elementary", level)
        
        # Test high school
        level = self.analyzer._get_complexity_level(10.0)
        self.assertIn("High School", level)
    
    def test_recommended_audience(self):
        """Test recommended audience determination."""
        # Test early elementary
        audience = self.analyzer._get_recommended_audience(2.0)
        self.assertIn("Early elementary", audience)
        
        # Test college
        audience = self.analyzer._get_recommended_audience(15.0)
        self.assertIn("College", audience)
    
    def test_analyze_paragraph_readability(self):
        """Test paragraph-by-paragraph readability analysis."""
        multi_paragraph_text = "First paragraph. It has simple words.\n\nSecond paragraph. It is also simple."
        results = self.analyzer.analyze_paragraph_readability(multi_paragraph_text)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)  # Two paragraphs
        
        for result in results:
            self.assertIn('paragraph_number', result)
            self.assertIn('paragraph_text', result)
            self.assertIn('grade_level', result)
    
    def test_readability_recommendations(self):
        """Test readability recommendations generation."""
        # Test with high grade level
        high_grade_result = {
            'grade_level': 15.0,
            'reading_ease': 30.0,
            'avg_words_per_sentence': 25.0,
            'avg_syllables_per_word': 2.5
        }
        recommendations = self.analyzer.get_readability_recommendations(high_grade_result)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_compare_readability_formulas(self):
        """Test comparison of different readability formulas."""
        result = self.analyzer.compare_readability_formulas(self.simple_text)
        
        required_keys = [
            'flesch_kincaid_grade', 'flesch_reading_ease', 'gunning_fog_index',
            'smog_index', 'average_grade_level', 'formula_agreement'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_formula_agreement(self):
        """Test formula agreement assessment."""
        # Test high agreement
        high_agreement = [5.0, 5.5, 4.8]
        agreement = self.analyzer._assess_formula_agreement(high_agreement)
        self.assertIn("High agreement", agreement)
        
        # Test low agreement
        low_agreement = [3.0, 8.0, 12.0]
        agreement = self.analyzer._assess_formula_agreement(low_agreement)
        self.assertIn("Low agreement", agreement)


if __name__ == '__main__':
    unittest.main() 