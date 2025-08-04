"""
Pedagogical Quality Analyzer for Educational Resource Quality Evaluator.

This module evaluates educational content for pedagogical quality including
learning objectives, examples, assessments, structure, and overall
educational effectiveness.

"""

import re
import math
from typing import Dict, List, Any, Set
from utils import extract_keywords, calculate_text_statistics


class PedagogicalAnalyzer:
    """
    Analyzes educational content for pedagogical quality and effectiveness.
    
    This class evaluates various aspects of educational content including
    learning objectives, examples and illustrations, assessment elements,
    structure and organization, and overall pedagogical effectiveness.
    """
    
    def __init__(self):
        """Initialize the pedagogical analyzer."""
        # Define pedagogical elements to look for
        self.learning_objective_patterns = [
            r'learning objective[s]?',
            r'objective[s]?',
            r'goal[s]?',
            r'student[s]? will',
            r'student[s]? can',
            r'student[s]? should',
            r'understand',
            r'identify',
            r'describe',
            r'explain',
            r'analyze',
            r'evaluate',
            r'create',
            r'demonstrate'
        ]
        
        self.example_patterns = [
            r'example[s]?',
            r'for example',
            r'such as',
            r'including',
            r'like',
            r'specifically',
            r'instance',
            r'illustration',
            r'case study',
            r'sample'
        ]
        
        self.assessment_patterns = [
            r'question[s]?',
            r'quiz',
            r'test',
            r'assessment',
            r'evaluation',
            r'exercise[s]?',
            r'activity',
            r'practice',
            r'review',
            r'check your understanding'
        ]
        
        self.structure_patterns = [
            r'introduction',
            r'conclusion',
            r'summary',
            r'overview',
            r'background',
            r'key points',
            r'main idea',
            r'important',
            r'note',
            r'remember'
        ]
        
        # Define scoring weights
        self.scoring_weights = {
            'objectives': 0.25,
            'examples': 0.20,
            'assessment': 0.20,
            'structure': 0.20,
            'engagement': 0.15
        }
    
    def evaluate_pedagogy(self, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive pedagogical evaluation.
        
        Args:
            content: Educational content to evaluate
            
        Returns:
            Dict[str, Any]: Dictionary containing pedagogical evaluation results
        """
        # Analyze different pedagogical aspects
        objectives_analysis = self._analyze_learning_objectives(content)
        examples_analysis = self._analyze_examples_and_illustrations(content)
        assessment_analysis = self._analyze_assessment_elements(content)
        structure_analysis = self._analyze_structure_and_organization(content)
        engagement_analysis = self._analyze_engagement_factors(content)
        
        # Calculate individual scores
        objectives_score = self._calculate_objectives_score(objectives_analysis)
        examples_score = self._calculate_examples_score(examples_analysis)
        assessment_score = self._calculate_assessment_score(assessment_analysis)
        structure_score = self._calculate_structure_score(structure_analysis)
        engagement_score = self._calculate_engagement_score(engagement_analysis)
        
        # Calculate weighted overall score
        overall_score = (
            objectives_score * self.scoring_weights['objectives'] +
            examples_score * self.scoring_weights['examples'] +
            assessment_score * self.scoring_weights['assessment'] +
            structure_score * self.scoring_weights['structure'] +
            engagement_score * self.scoring_weights['engagement']
        )
        
        # Get overall assessment
        assessment = self._get_pedagogical_assessment(overall_score)
        
        return {
            'score': round(overall_score, 2),
            'objectives_score': round(objectives_score, 1),
            'examples_score': round(examples_score, 1),
            'assessment_score': round(assessment_score, 1),
            'structure_score': round(structure_score, 1),
            'engagement_score': round(engagement_score, 1),
            'assessment': assessment,
            'objectives_analysis': objectives_analysis,
            'examples_analysis': examples_analysis,
            'assessment_analysis': assessment_analysis,
            'structure_analysis': structure_analysis,
            'engagement_analysis': engagement_analysis,
            'recommendations': self._generate_pedagogical_recommendations({
                'objectives_score': objectives_score,
                'examples_score': examples_score,
                'assessment_score': assessment_score,
                'structure_score': structure_score,
                'engagement_score': engagement_score,
                'overall_score': overall_score
            })
        }
    
    def _analyze_learning_objectives(self, content: str) -> Dict[str, Any]:
        """
        Analyze learning objectives in content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Analysis of learning objectives
        """
        objectives_found = []
        objective_indicators = 0
        
        # Look for learning objective patterns
        for pattern in self.learning_objective_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                objective_indicators += len(matches)
                objectives_found.extend(matches)
        
        # Count sentences that contain objective language
        sentences = re.split(r'[.!?]+', content)
        objective_sentences = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for pattern in self.learning_objective_patterns:
                if re.search(pattern, sentence_lower):
                    objective_sentences += 1
                    break
        
        return {
            'objectives_found': objectives_found,
            'objective_indicators': objective_indicators,
            'objective_sentences': objective_sentences,
            'total_sentences': len(sentences),
            'objectives_percentage': (objective_sentences / len(sentences)) * 100 if sentences else 0
        }
    
    def _analyze_examples_and_illustrations(self, content: str) -> Dict[str, Any]:
        """
        Analyze examples and illustrations in content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Analysis of examples and illustrations
        """
        examples_found = []
        example_indicators = 0
        
        # Look for example patterns
        for pattern in self.example_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                example_indicators += len(matches)
                examples_found.extend(matches)
        
        # Count paragraphs with examples
        paragraphs = re.split(r'\n\s*\n', content)
        example_paragraphs = 0
        
        for paragraph in paragraphs:
            paragraph_lower = paragraph.lower()
            for pattern in self.example_patterns:
                if re.search(pattern, paragraph_lower):
                    example_paragraphs += 1
                    break
        
        return {
            'examples_found': examples_found,
            'example_indicators': example_indicators,
            'example_paragraphs': example_paragraphs,
            'total_paragraphs': len(paragraphs),
            'examples_percentage': (example_paragraphs / len(paragraphs)) * 100 if paragraphs else 0
        }
    
    def _analyze_assessment_elements(self, content: str) -> Dict[str, Any]:
        """
        Analyze assessment elements in content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Analysis of assessment elements
        """
        assessments_found = []
        assessment_indicators = 0
        
        # Look for assessment patterns
        for pattern in self.assessment_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                assessment_indicators += len(matches)
                assessments_found.extend(matches)
        
        # Count sections with assessments
        sections = re.split(r'\n\s*\n', content)
        assessment_sections = 0
        
        for section in sections:
            section_lower = section.lower()
            for pattern in self.assessment_patterns:
                if re.search(pattern, section_lower):
                    assessment_sections += 1
                    break
        
        return {
            'assessments_found': assessments_found,
            'assessment_indicators': assessment_indicators,
            'assessment_sections': assessment_sections,
            'total_sections': len(sections),
            'assessments_percentage': (assessment_sections / len(sections)) * 100 if sections else 0
        }
    
    def _analyze_structure_and_organization(self, content: str) -> Dict[str, Any]:
        """
        Analyze structure and organization of content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Analysis of structure and organization
        """
        structure_indicators = 0
        structure_elements = []
        
        # Look for structure patterns
        for pattern in self.structure_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                structure_indicators += len(matches)
                structure_elements.extend(matches)
        
        # Analyze paragraph structure
        paragraphs = re.split(r'\n\s*\n', content)
        avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        
        # Check for logical flow indicators
        flow_indicators = [
            'first', 'second', 'third', 'next', 'then', 'finally',
            'however', 'therefore', 'consequently', 'in addition',
            'furthermore', 'moreover', 'on the other hand'
        ]
        
        flow_count = 0
        for indicator in flow_indicators:
            flow_count += len(re.findall(indicator, content.lower()))
        
        return {
            'structure_indicators': structure_indicators,
            'structure_elements': structure_elements,
            'avg_paragraph_length': avg_paragraph_length,
            'flow_indicators': flow_count,
            'total_paragraphs': len(paragraphs),
            'structure_score': min(10, (structure_indicators + flow_count) / 2)
        }
    
    def _analyze_engagement_factors(self, content: str) -> Dict[str, Any]:
        """
        Analyze engagement factors in content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Analysis of engagement factors
        """
        # Engagement indicators
        engagement_indicators = {
            'questions': len(re.findall(r'\?', content)),
            'exclamations': len(re.findall(r'!', content)),
            'direct_address': len(re.findall(r'you|your', content.lower())),
            'active_voice': len(re.findall(r'\b(is|are|was|were)\s+\w+ing', content.lower())),
            'varied_sentence_length': self._analyze_sentence_variety(content)
        }
        
        # Calculate engagement score
        engagement_score = (
            engagement_indicators['questions'] * 0.5 +
            engagement_indicators['exclamations'] * 0.3 +
            engagement_indicators['direct_address'] * 0.2 +
            engagement_indicators['varied_sentence_length'] * 0.5
        )
        
        return {
            'engagement_indicators': engagement_indicators,
            'engagement_score': min(10, engagement_score)
        }
    
    def _analyze_sentence_variety(self, content: str) -> float:
        """
        Analyze sentence variety in content.
        
        Args:
            content: Content to analyze
            
        Returns:
            float: Sentence variety score
        """
        sentences = re.split(r'[.!?]+', content)
        if len(sentences) < 2:
            return 0.0
        
        # Calculate sentence length variance
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        if not sentence_lengths:
            return 0.0
        
        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
        
        # Higher variance indicates more variety
        return min(5, variance / 10)
    
    def _calculate_objectives_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate learning objectives score.
        
        Args:
            analysis: Objectives analysis results
            
        Returns:
            float: Objectives score (0-10)
        """
        objectives_percentage = analysis['objectives_percentage']
        objective_indicators = analysis['objective_indicators']
        
        # Base score on percentage of sentences with objectives
        base_score = min(10, objectives_percentage * 0.1)
        
        # Bonus for multiple indicators
        indicator_bonus = min(2, objective_indicators * 0.1)
        
        return min(10, base_score + indicator_bonus)
    
    def _calculate_examples_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate examples and illustrations score.
        
        Args:
            analysis: Examples analysis results
            
        Returns:
            float: Examples score (0-10)
        """
        examples_percentage = analysis['examples_percentage']
        example_indicators = analysis['example_indicators']
        
        # Base score on percentage of paragraphs with examples
        base_score = min(10, examples_percentage * 0.1)
        
        # Bonus for multiple indicators
        indicator_bonus = min(2, example_indicators * 0.1)
        
        return min(10, base_score + indicator_bonus)
    
    def _calculate_assessment_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate assessment elements score.
        
        Args:
            analysis: Assessment analysis results
            
        Returns:
            float: Assessment score (0-10)
        """
        assessments_percentage = analysis['assessments_percentage']
        assessment_indicators = analysis['assessment_indicators']
        
        # Base score on percentage of sections with assessments
        base_score = min(10, assessments_percentage * 0.1)
        
        # Bonus for multiple indicators
        indicator_bonus = min(2, assessment_indicators * 0.1)
        
        return min(10, base_score + indicator_bonus)
    
    def _calculate_structure_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate structure and organization score.
        
        Args:
            analysis: Structure analysis results
            
        Returns:
            float: Structure score (0-10)
        """
        structure_score = analysis['structure_score']
        avg_paragraph_length = analysis['avg_paragraph_length']
        flow_indicators = analysis['flow_indicators']
        
        # Adjust score based on paragraph length (optimal: 3-8 sentences)
        if 3 <= avg_paragraph_length <= 8:
            length_bonus = 1
        elif avg_paragraph_length < 3:
            length_bonus = 0.5
        else:
            length_bonus = 0
        
        # Bonus for flow indicators
        flow_bonus = min(1, flow_indicators * 0.1)
        
        return min(10, structure_score + length_bonus + flow_bonus)
    
    def _calculate_engagement_score(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate engagement score.
        
        Args:
            analysis: Engagement analysis results
            
        Returns:
            float: Engagement score (0-10)
        """
        return analysis['engagement_score']
    
    def _get_pedagogical_assessment(self, score: float) -> str:
        """
        Get pedagogical assessment based on score.
        
        Args:
            score: Overall pedagogical score
            
        Returns:
            str: Assessment description
        """
        if score >= 8.5:
            return "Excellent pedagogical quality"
        elif score >= 7.0:
            return "Good pedagogical quality"
        elif score >= 5.5:
            return "Fair pedagogical quality"
        elif score >= 4.0:
            return "Poor pedagogical quality"
        else:
            return "Very poor pedagogical quality"
    
    def _generate_pedagogical_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate pedagogical recommendations based on scores.
        
        Args:
            scores: Dictionary of pedagogical scores
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Check learning objectives
        if scores['objectives_score'] < 6:
            recommendations.append("Add clear learning objectives at the beginning of each section")
        
        # Check examples
        if scores['examples_score'] < 6:
            recommendations.append("Include more examples and illustrations to support learning")
        
        # Check assessments
        if scores['assessment_score'] < 6:
            recommendations.append("Add assessment elements like questions and exercises")
        
        # Check structure
        if scores['structure_score'] < 6:
            recommendations.append("Improve content structure with clear introductions and summaries")
        
        # Check engagement
        if scores['engagement_score'] < 6:
            recommendations.append("Increase engagement through questions and active voice")
        
        # Overall recommendations
        if scores['overall_score'] < 6:
            recommendations.append("Consider restructuring content to improve pedagogical effectiveness")
        
        if not recommendations:
            recommendations.append("Content demonstrates good pedagogical practices")
        
        return recommendations
