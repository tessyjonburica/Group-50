"""
Curriculum Alignment Checker for Educational Resource Quality Evaluator.

This module analyzes educational content for alignment with curriculum
standards, identifying covered and missing topics, and providing
comprehensive alignment scoring.

"""

import re
import math
from typing import Dict, List, Any, Set
from utils import extract_keywords, calculate_text_statistics


class CurriculumChecker:
    """
    Analyzes educational content for curriculum alignment.
    
    This class provides methods to check educational content against
    curriculum standards, identify covered and missing topics, and
    generate alignment scores and recommendations.
    """
    
    def __init__(self):
        """Initialize the curriculum checker with standard topics."""
        # Define curriculum standards by subject area
        self.curriculum_standards = {
            'mathematics': {
                'elementary': {
                    'number_sense': ['counting', 'addition', 'subtraction', 'multiplication', 'division', 'fractions', 'decimals', 'place value'],
                    'geometry': ['shapes', 'angles', 'area', 'perimeter', 'volume', 'symmetry', 'transformations'],
                    'measurement': ['length', 'weight', 'time', 'money', 'temperature', 'capacity'],
                    'data_analysis': ['graphs', 'charts', 'statistics', 'probability', 'patterns']
                },
                'middle_school': {
                    'algebra': ['variables', 'equations', 'inequalities', 'functions', 'linear relationships'],
                    'geometry': ['angles', 'triangles', 'circles', 'area', 'perimeter', 'volume', 'coordinate plane'],
                    'number_systems': ['integers', 'rational numbers', 'irrational numbers', 'exponents'],
                    'statistics': ['data collection', 'mean', 'median', 'mode', 'probability', 'graphs']
                },
                'high_school': {
                    'algebra': ['functions', 'polynomials', 'quadratic equations', 'systems of equations'],
                    'geometry': ['proofs', 'theorems', 'trigonometry', 'circles', 'polygons'],
                    'calculus': ['limits', 'derivatives', 'integrals', 'applications'],
                    'statistics': ['probability', 'distributions', 'hypothesis testing', 'regression']
                }
            },
            'science': {
                'elementary': {
                    'life_science': ['plants', 'animals', 'ecosystems', 'life cycles', 'habitats', 'adaptations'],
                    'physical_science': ['matter', 'energy', 'forces', 'motion', 'simple machines', 'light', 'sound'],
                    'earth_science': ['weather', 'climate', 'rocks', 'minerals', 'water cycle', 'solar system'],
                    'scientific_method': ['observation', 'hypothesis', 'experiment', 'conclusion']
                },
                'middle_school': {
                    'life_science': ['cells', 'genetics', 'evolution', 'ecosystems', 'biodiversity'],
                    'physical_science': ['atoms', 'molecules', 'chemical reactions', 'energy', 'forces'],
                    'earth_science': ['plate tectonics', 'weathering', 'erosion', 'climate change'],
                    'scientific_inquiry': ['hypothesis', 'variables', 'data analysis', 'conclusions']
                },
                'high_school': {
                    'biology': ['cell biology', 'genetics', 'evolution', 'ecology', 'human anatomy'],
                    'chemistry': ['atomic structure', 'chemical bonding', 'reactions', 'stoichiometry'],
                    'physics': ['mechanics', 'energy', 'waves', 'electricity', 'magnetism'],
                    'earth_science': ['geology', 'meteorology', 'astronomy', 'oceanography']
                }
            },
            'language_arts': {
                'elementary': {
                    'reading': ['phonics', 'comprehension', 'vocabulary', 'fluency', 'literature'],
                    'writing': ['sentences', 'paragraphs', 'narrative', 'informative', 'opinion'],
                    'grammar': ['parts of speech', 'punctuation', 'capitalization', 'spelling'],
                    'communication': ['speaking', 'listening', 'presentation']
                },
                'middle_school': {
                    'reading': ['comprehension', 'analysis', 'inference', 'text structure', 'literary elements'],
                    'writing': ['essays', 'research', 'argumentative', 'narrative', 'expository'],
                    'grammar': ['sentence structure', 'clauses', 'agreement', 'style'],
                    'communication': ['debate', 'presentation', 'collaboration']
                },
                'high_school': {
                    'literature': ['analysis', 'interpretation', 'critical thinking', 'literary devices'],
                    'composition': ['research papers', 'essays', 'creative writing', 'argumentation'],
                    'grammar': ['advanced grammar', 'style', 'rhetoric', 'editing'],
                    'communication': ['public speaking', 'debate', 'media literacy']
                }
            },
            'social_studies': {
                'elementary': {
                    'history': ['communities', 'families', 'local history', 'national symbols'],
                    'geography': ['maps', 'landforms', 'continents', 'oceans', 'climate'],
                    'civics': ['citizenship', 'government', 'rights', 'responsibilities'],
                    'economics': ['goods', 'services', 'money', 'trade', 'needs', 'wants']
                },
                'middle_school': {
                    'history': ['ancient civilizations', 'world history', 'american history', 'historical thinking'],
                    'geography': ['physical geography', 'human geography', 'regions', 'culture'],
                    'civics': ['democracy', 'constitution', 'branches of government', 'citizenship'],
                    'economics': ['supply and demand', 'market economy', 'global trade', 'personal finance']
                },
                'high_school': {
                    'history': ['world history', 'american history', 'historical analysis', 'primary sources'],
                    'geography': ['human geography', 'physical geography', 'global issues', 'sustainability'],
                    'civics': ['constitutional law', 'political systems', 'civic engagement', 'public policy'],
                    'economics': ['microeconomics', 'macroeconomics', 'economic systems', 'global economy']
                }
            }
        }
    
    def analyze_alignment(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for curriculum alignment.
        
        Args:
            content: Educational content to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing alignment analysis results
        """
        # Extract keywords from content
        content_keywords = set(extract_keywords(content.lower()))
        
        # Analyze alignment for each subject area
        subject_alignments = {}
        total_score = 0
        total_topics = 0
        
        for subject, grade_levels in self.curriculum_standards.items():
            subject_alignment = self._analyze_subject_alignment(content_keywords, grade_levels)
            subject_alignments[subject] = subject_alignment
            total_score += subject_alignment['score']
            total_topics += subject_alignment['total_topics']
        
        # Calculate overall alignment score
        overall_score = total_score / len(self.curriculum_standards) if self.curriculum_standards else 0
        
        # Determine overall assessment
        assessment = self._get_alignment_assessment(overall_score)
        
        # Compile covered and missing topics across all subjects
        all_covered_topics = []
        all_missing_topics = []
        
        for subject, alignment in subject_alignments.items():
            all_covered_topics.extend(alignment['covered_topics'])
            all_missing_topics.extend(alignment['missing_topics'])
        
        return {
            'score': round(overall_score, 2),
            'assessment': assessment,
            'subject_alignments': subject_alignments,
            'covered_topics': all_covered_topics,
            'missing_topics': all_missing_topics,
            'total_topics_covered': len(all_covered_topics),
            'total_topics_missing': len(all_missing_topics),
            'coverage_percentage': self._calculate_coverage_percentage(len(all_covered_topics), len(all_covered_topics) + len(all_missing_topics))
        }
    
    def _analyze_subject_alignment(self, content_keywords: Set[str], grade_levels: Dict[str, Dict[str, List[str]]]) -> Dict[str, Any]:
        """
        Analyze alignment for a specific subject area.
        
        Args:
            content_keywords: Set of keywords from content
            grade_levels: Dictionary of grade levels and their topics
            
        Returns:
            Dict[str, Any]: Dictionary containing subject alignment results
        """
        covered_topics = []
        missing_topics = []
        total_topics = 0
        
        # Check each grade level and topic area
        for grade_level, topic_areas in grade_levels.items():
            for topic_area, topics in topic_areas.items():
                total_topics += len(topics)
                
                for topic in topics:
                    # Check if topic is mentioned in content
                    if self._topic_matches_content(topic, content_keywords):
                        covered_topics.append(f"{grade_level}_{topic_area}_{topic}")
                    else:
                        missing_topics.append(f"{grade_level}_{topic_area}_{topic}")
        
        # Calculate subject score
        coverage_ratio = len(covered_topics) / total_topics if total_topics > 0 else 0
        subject_score = coverage_ratio * 100
        
        return {
            'score': round(subject_score, 2),
            'covered_topics': covered_topics,
            'missing_topics': missing_topics,
            'total_topics': total_topics,
            'coverage_ratio': coverage_ratio
        }
    
    def _topic_matches_content(self, topic: str, content_keywords: Set[str]) -> bool:
        """
        Check if a topic is mentioned in the content.
        
        Args:
            topic: Topic to check
            content_keywords: Set of keywords from content
            
        Returns:
            bool: True if topic is found in content, False otherwise
        """
        # Split topic into individual words
        topic_words = topic.lower().split()
        
        # Check if any topic word appears in content keywords
        for word in topic_words:
            if word in content_keywords:
                return True
        
        # Also check for exact topic match
        if topic.lower() in content_keywords:
            return True
        
        # Check for partial matches (e.g., "addition" matches "addition facts")
        for keyword in content_keywords:
            if topic.lower() in keyword or keyword in topic.lower():
                return True
        
        return False
    
    def _calculate_coverage_percentage(self, covered: int, total: int) -> float:
        """
        Calculate the percentage of topics covered.
        
        Args:
            covered: Number of covered topics
            total: Total number of topics
            
        Returns:
            float: Coverage percentage
        """
        if total == 0:
            return 0.0
        return (covered / total) * 100
    
    def _get_alignment_assessment(self, score: float) -> str:
        """
        Get assessment based on alignment score.
        
        Args:
            score: Alignment score (0-100)
            
        Returns:
            str: Assessment description
        """
        if score >= 90:
            return "Excellent alignment with curriculum standards"
        elif score >= 75:
            return "Good alignment with minor gaps"
        elif score >= 60:
            return "Fair alignment with some gaps"
        elif score >= 40:
            return "Poor alignment with significant gaps"
        else:
            return "Very poor alignment with major gaps"
    
    def get_curriculum_recommendations(self, alignment_results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on alignment analysis.
        
        Args:
            alignment_results: Results from alignment analysis
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Check overall score
        score = alignment_results['score']
        if score < 60:
            recommendations.append("Consider expanding content to cover more curriculum standards")
        
        # Check missing topics by subject
        subject_alignments = alignment_results['subject_alignments']
        
        for subject, alignment in subject_alignments.items():
            if alignment['score'] < 50:
                recommendations.append(f"Focus on improving {subject} content coverage")
            
            # Check specific missing topics
            missing_topics = alignment['missing_topics']
            if missing_topics:
                top_missing = missing_topics[:3]  # Show top 3 missing topics
                recommendations.append(f"Add content covering: {', '.join(top_missing)}")
        
        # Check coverage percentage
        coverage = alignment_results['coverage_percentage']
        if coverage < 50:
            recommendations.append("Significantly expand topic coverage to meet curriculum requirements")
        
        if not recommendations:
            recommendations.append("Content shows good alignment with curriculum standards")
        
        return recommendations
    
    def get_grade_level_recommendation(self, content: str) -> str:
        """
        Recommend appropriate grade level based on content analysis.
        
        Args:
            content: Educational content to analyze
            
        Returns:
            str: Recommended grade level
        """
        # Analyze content complexity
        stats = calculate_text_statistics(content)
        
        # Use readability and complexity to determine grade level
        avg_words_per_sentence = stats['avg_words_per_sentence']
        avg_syllables_per_word = stats['avg_syllables_per_word']
        
        # Simple grade level estimation
        if avg_words_per_sentence < 10 and avg_syllables_per_word < 1.5:
            return "Elementary (K-5)"
        elif avg_words_per_sentence < 15 and avg_syllables_per_word < 1.8:
            return "Middle School (6-8)"
        elif avg_words_per_sentence < 20 and avg_syllables_per_word < 2.1:
            return "High School (9-12)"
        else:
            return "Advanced/College Level"
    
 