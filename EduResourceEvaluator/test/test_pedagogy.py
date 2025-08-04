"""
Unit tests for the Pedagogical Analyzer module.

This module contains comprehensive tests for the PedagogicalAnalyzer class,
testing pedagogical quality assessment and educational effectiveness.

"""

import unittest
from pedagogy import PedagogicalAnalyzer


class TestPedagogicalAnalyzer(unittest.TestCase):
    """Test cases for PedagogicalAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PedagogicalAnalyzer()
        
        # Test content samples
        self.good_pedagogy_content = """
        Learning Objectives: Students will understand basic mathematics.
        
        Introduction: Today we will learn about addition.
        
        For example, 2 + 2 = 4. This shows how addition works.
        
        Practice Exercise: Solve the following problems.
        
        Summary: We learned that addition combines numbers.
        """
        
        self.poor_pedagogy_content = "This is some content without clear structure or objectives."
        self.empty_content = ""
    
    def test_evaluate_pedagogy(self):
        """Test comprehensive pedagogical evaluation."""
        result = self.analyzer.evaluate_pedagogy(self.good_pedagogy_content)
        
        # Check required keys
        required_keys = [
            'score', 'objectives_score', 'examples_score', 'assessment_score',
            'structure_score', 'engagement_score', 'assessment', 'recommendations'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check data types
        self.assertIsInstance(result['score'], float)
        self.assertIsInstance(result['assessment'], str)
        self.assertIsInstance(result['recommendations'], list)
        
        # Check score ranges
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 100.0)
    
    def test_analyze_learning_objectives(self):
        """Test learning objectives analysis."""
        result = self.analyzer._analyze_learning_objectives(self.good_pedagogy_content)
        
        required_keys = [
            'objectives_found', 'objective_indicators', 'objective_sentences',
            'total_sentences', 'objectives_percentage'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['objective_indicators'], int)
        self.assertIsInstance(result['objectives_percentage'], float)
    
    def test_analyze_examples_and_illustrations(self):
        """Test examples and illustrations analysis."""
        result = self.analyzer._analyze_examples_and_illustrations(self.good_pedagogy_content)
        
        required_keys = [
            'examples_found', 'example_indicators', 'example_paragraphs',
            'total_paragraphs', 'examples_percentage'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['example_indicators'], int)
        self.assertIsInstance(result['examples_percentage'], float)
    
    def test_analyze_assessment_elements(self):
        """Test assessment elements analysis."""
        result = self.analyzer._analyze_assessment_elements(self.good_pedagogy_content)
        
        required_keys = [
            'assessments_found', 'assessment_indicators', 'assessment_sections',
            'total_sections', 'assessments_percentage'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['assessment_indicators'], int)
        self.assertIsInstance(result['assessments_percentage'], float)
    
    def test_analyze_structure_and_organization(self):
        """Test structure and organization analysis."""
        result = self.analyzer._analyze_structure_and_organization(self.good_pedagogy_content)
        
        required_keys = [
            'structure_indicators', 'structure_elements', 'avg_paragraph_length',
            'flow_indicators', 'total_paragraphs', 'structure_score'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['structure_score'], float)
        self.assertGreaterEqual(result['structure_score'], 0.0)
        self.assertLessEqual(result['structure_score'], 10.0)
    
    def test_analyze_engagement_factors(self):
        """Test engagement factors analysis."""
        result = self.analyzer._analyze_engagement_factors(self.good_pedagogy_content)
        
        required_keys = ['engagement_indicators', 'engagement_score']
        
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertIsInstance(result['engagement_score'], float)
        self.assertGreaterEqual(result['engagement_score'], 0.0)
        self.assertLessEqual(result['engagement_score'], 10.0)
    
    def test_analyze_sentence_variety(self):
        """Test sentence variety analysis."""
        # Test with varied sentences
        varied_content = "Short sentence. This is a longer sentence with more words. Medium length."
        result = self.analyzer._analyze_sentence_variety(varied_content)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        
        # Test with single sentence
        single_sentence = "This is one sentence."
        result = self.analyzer._analyze_sentence_variety(single_sentence)
        self.assertEqual(result, 0.0)
    
    def test_calculate_objectives_score(self):
        """Test learning objectives score calculation."""
        analysis = {
            'objectives_percentage': 25.0,
            'objective_indicators': 3
        }
        
        result = self.analyzer._calculate_objectives_score(analysis)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 10.0)
    
    def test_calculate_examples_score(self):
        """Test examples score calculation."""
        analysis = {
            'examples_percentage': 30.0,
            'example_indicators': 2
        }
        
        result = self.analyzer._calculate_examples_score(analysis)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 10.0)
    
    def test_calculate_assessment_score(self):
        """Test assessment score calculation."""
        analysis = {
            'assessments_percentage': 20.0,
            'assessment_indicators': 1
        }
        
        result = self.analyzer._calculate_assessment_score(analysis)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 10.0)
    
    def test_calculate_structure_score(self):
        """Test structure score calculation."""
        analysis = {
            'structure_score': 5.0,
            'avg_paragraph_length': 4.0,
            'flow_indicators': 2
        }
        
        result = self.analyzer._calculate_structure_score(analysis)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 10.0)
    
    def test_calculate_engagement_score(self):
        """Test engagement score calculation."""
        analysis = {'engagement_score': 6.0}
        
        result = self.analyzer._calculate_engagement_score(analysis)
        self.assertEqual(result, 6.0)
    
    def test_pedagogical_assessment(self):
        """Test pedagogical assessment generation."""
        # Test excellent quality
        assessment = self.analyzer._get_pedagogical_assessment(9.0)
        self.assertIn("Excellent", assessment)
        
        # Test poor quality
        assessment = self.analyzer._get_pedagogical_assessment(3.0)
        self.assertIn("Very poor", assessment)
        
        # Test very poor quality
        assessment = self.analyzer._get_pedagogical_assessment(1.0)
        self.assertIn("Very poor", assessment)
    
    def test_generate_pedagogical_recommendations(self):
        """Test pedagogical recommendations generation."""
        scores = {
            'objectives_score': 3.0,
            'examples_score': 4.0,
            'assessment_score': 5.0,
            'structure_score': 6.0,
            'engagement_score': 7.0,
            'overall_score': 5.0
        }
        
        recommendations = self.analyzer._generate_pedagogical_recommendations(scores)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check for specific recommendation types
        recommendation_text = ' '.join(recommendations).lower()
        self.assertIn('objectives', recommendation_text)
    

    

    
    def test_good_vs_poor_pedagogy(self):
        """Test comparison between good and poor pedagogical content."""
        good_result = self.analyzer.evaluate_pedagogy(self.good_pedagogy_content)
        poor_result = self.analyzer.evaluate_pedagogy(self.poor_pedagogy_content)
        
        # Good content should score higher
        self.assertGreater(good_result['score'], poor_result['score'])
        
        # Good content should have more recommendations
        self.assertGreater(len(good_result['recommendations']), 0)
    
    def test_empty_content_handling(self):
        """Test handling of empty content."""
        result = self.analyzer.evaluate_pedagogy(self.empty_content)
        
        # Should still return valid structure
        self.assertIn('score', result)
        self.assertIn('assessment', result)
        self.assertIn('recommendations', result)
    
    def test_score_normalization(self):
        """Test that all scores are properly normalized."""
        result = self.analyzer.evaluate_pedagogy(self.good_pedagogy_content)
        
        # Check individual component scores
        component_scores = [
            result['objectives_score'],
            result['examples_score'],
            result['assessment_score'],
            result['structure_score'],
            result['engagement_score']
        ]
        
        for score in component_scores:
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)
        
        # Check overall score
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 100.0)


if __name__ == '__main__':
    unittest.main() 