"""
Unit tests for the Curriculum Checker module.

This module contains comprehensive tests for the CurriculumChecker class,
testing curriculum alignment analysis and topic matching.

"""

import unittest
from curriculum_checker import CurriculumChecker


class TestCurriculumChecker(unittest.TestCase):
    """Test cases for CurriculumChecker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = CurriculumChecker()
        
        # Test content samples
        self.math_content = "Students will learn addition and subtraction. They will understand fractions and decimals."
        self.science_content = "The scientific method involves observation and hypothesis. Students conduct experiments."
        self.language_content = "Reading comprehension is important. Students practice writing essays and stories."
        self.empty_content = ""
    
    def test_analyze_alignment(self):
        """Test curriculum alignment analysis."""
        result = self.checker.analyze_alignment(self.math_content)
        
        # Check required keys
        required_keys = [
            'score', 'assessment', 'subject_alignments', 'covered_topics',
            'missing_topics', 'total_topics_covered', 'total_topics_missing',
            'coverage_percentage'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check data types
        self.assertIsInstance(result['score'], float)
        self.assertIsInstance(result['assessment'], str)
        self.assertIsInstance(result['covered_topics'], list)
        self.assertIsInstance(result['missing_topics'], list)
    
    def test_subject_alignment_analysis(self):
        """Test subject-specific alignment analysis."""
        content_keywords = {'addition', 'subtraction', 'fractions', 'mathematics'}
        grade_levels = self.checker.curriculum_standards['mathematics']
        
        result = self.checker._analyze_subject_alignment(content_keywords, grade_levels)
        
        required_keys = ['score', 'covered_topics', 'missing_topics', 'total_topics', 'coverage_ratio']
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['score'], float)
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 100.0)
    
    def test_topic_matching(self):
        """Test topic matching functionality."""
        content_keywords = {'addition', 'subtraction', 'mathematics'}
        
        # Test matching topic
        result = self.checker._topic_matches_content('addition', content_keywords)
        self.assertTrue(result)
        
        # Test non-matching topic
        result = self.checker._topic_matches_content('quantum physics', content_keywords)
        self.assertFalse(result)
        
        # Test partial matching
        result = self.checker._topic_matches_content('addition facts', content_keywords)
        self.assertTrue(result)
    
    def test_coverage_percentage_calculation(self):
        """Test coverage percentage calculation."""
        # Test with covered topics
        result = self.checker._calculate_coverage_percentage(5, 10)
        self.assertEqual(result, 50.0)
        
        # Test with no covered topics
        result = self.checker._calculate_coverage_percentage(0, 10)
        self.assertEqual(result, 0.0)
        
        # Test with zero total
        result = self.checker._calculate_coverage_percentage(5, 0)
        self.assertEqual(result, 0.0)
    
    def test_alignment_assessment(self):
        """Test alignment assessment generation."""
        # Test excellent alignment
        assessment = self.checker._get_alignment_assessment(95.0)
        self.assertIn("Excellent", assessment)
        
        # Test poor alignment
        assessment = self.checker._get_alignment_assessment(30.0)
        self.assertIn("Very poor", assessment)
        
        # Test very poor alignment
        assessment = self.checker._get_alignment_assessment(10.0)
        self.assertIn("Very poor", assessment)
    
    def test_curriculum_recommendations(self):
        """Test curriculum recommendations generation."""
        alignment_results = {
            'score': 45.0,
            'subject_alignments': {
                'mathematics': {'score': 30.0, 'missing_topics': ['algebra', 'geometry']},
                'science': {'score': 60.0, 'missing_topics': ['chemistry']}
            },
            'coverage_percentage': 40.0
        }
        
        recommendations = self.checker.get_curriculum_recommendations(alignment_results)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check for specific recommendation types
        recommendation_text = ' '.join(recommendations).lower()
        self.assertIn('expand', recommendation_text)
    
    def test_grade_level_recommendation(self):
        """Test grade level recommendation."""
        # Test simple content
        simple_content = "This is a simple sentence. It has few words."
        recommendation = self.checker.get_grade_level_recommendation(simple_content)
        self.assertIsInstance(recommendation, str)
        self.assertIn("Elementary", recommendation)
        
        # Test complex content
        complex_content = "The sophisticated implementation of multifaceted algorithms necessitates comprehensive understanding."
        recommendation = self.checker.get_grade_level_recommendation(complex_content)
        self.assertIsInstance(recommendation, str)
    

    
    def test_math_content_alignment(self):
        """Test mathematics content alignment."""
        result = self.checker.analyze_alignment(self.math_content)
        
        # Check that mathematics alignment exists
        self.assertIn('mathematics', result['subject_alignments'])
        
        # Check that some topics are covered
        self.assertGreater(len(result['covered_topics']), 0)
    
    def test_science_content_alignment(self):
        """Test science content alignment."""
        result = self.checker.analyze_alignment(self.science_content)
        
        # Check that science alignment exists
        self.assertIn('science', result['subject_alignments'])
        
        # Check that some topics are covered
        self.assertGreater(len(result['covered_topics']), 0)
    
    def test_language_content_alignment(self):
        """Test language arts content alignment."""
        result = self.checker.analyze_alignment(self.language_content)
        
        # Check that language arts alignment exists
        self.assertIn('language_arts', result['subject_alignments'])
        
        # Check that some topics are covered
        self.assertGreater(len(result['covered_topics']), 0)
    
    def test_empty_content_handling(self):
        """Test handling of empty content."""
        result = self.checker.analyze_alignment(self.empty_content)
        
        # Should still return valid structure
        self.assertIn('score', result)
        self.assertIn('assessment', result)
        self.assertIn('covered_topics', result)
        self.assertIn('missing_topics', result)
    
    def test_all_subjects_coverage(self):
        """Test that all subjects are covered in analysis."""
        result = self.checker.analyze_alignment(self.math_content)
        
        expected_subjects = ['mathematics', 'science', 'language_arts', 'social_studies']
        
        for subject in expected_subjects:
            self.assertIn(subject, result['subject_alignments'])
    
    def test_score_normalization(self):
        """Test that scores are properly normalized."""
        result = self.checker.analyze_alignment(self.math_content)
        
        # Overall score should be between 0 and 100
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 100.0)
        
        # Subject scores should also be normalized
        for subject, alignment in result['subject_alignments'].items():
            self.assertGreaterEqual(alignment['score'], 0.0)
            self.assertLessEqual(alignment['score'], 100.0)


if __name__ == '__main__':
    unittest.main() 