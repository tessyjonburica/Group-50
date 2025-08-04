"""
Bias Detection Analyzer for Educational Resource Quality Evaluator.

This module analyzes educational content for various types of bias including
cultural sensitivity, gender bias, racial bias, age bias, and other forms
of discriminatory or insensitive language.

"""

import re
from typing import Dict, List, Any, Set
from utils import extract_keywords


class BiasDetector:
    """
    Analyzes educational content for various types of bias and sensitivity issues.
    
    This class provides comprehensive bias detection including cultural
    sensitivity, gender bias, racial bias, age bias, and other forms of
    discriminatory or insensitive language patterns.
    """
    
    def __init__(self):
        """Initialize the bias detector with bias patterns."""
        # Define bias patterns and sensitive terms
        self.gender_bias_patterns = {
            'stereotypical_roles': [
                r'\b(boys|girls)\s+(should|must|always)\s+(play|like|enjoy)',
                r'\b(men|women)\s+(naturally|typically)\s+(are|do)',
                r'\b(he|she)\s+(should|must)\s+(be|act|look)',
                r'\b(father|mother)\s+(role|responsibility)',
                r'\b(manly|womanly|feminine|masculine)\s+(traits|qualities)'
            ],
            'gendered_language': [
                r'\b(he|him|his)\s+(only|always)',
                r'\b(she|her|hers)\s+(only|always)',
                r'\b(man|woman)\s+(as|like)',
                r'\b(guys|gals|boys|girls)\s+(only)',
                r'\b(gentlemen|ladies)\s+(only)'
            ],
            'occupation_stereotypes': [
                r'\b(male|female)\s+(nurse|doctor|engineer|teacher)',
                r'\b(man|woman)\s+(nurse|doctor|engineer|teacher)',
                r'\b(he|she)\s+(is|was)\s+(a)\s+(nurse|doctor|engineer|teacher)'
            ]
        }
        
        self.racial_bias_patterns = {
            'stereotypical_descriptions': [
                r'\b(race|ethnicity)\s+(determines|affects)\s+(intelligence|ability)',
                r'\b(certain|specific)\s+(races|ethnicities)\s+(are|tend|typically)',
                r'\b(racial|ethnic)\s+(characteristics|traits|qualities)',
                r'\b(white|black|asian|hispanic)\s+(people|students)\s+(always|typically)'
            ],
            'cultural_assumptions': [
                r'\b(they|them)\s+(all|always)\s+(speak|eat|dress)',
                r'\b(their|them)\s+(culture|background)\s+(means|implies)',
                r'\b(foreign|exotic|different)\s+(ways|customs|traditions)',
                r'\b(primitive|advanced)\s+(cultures|societies)'
            ],
            'exclusionary_language': [
                r'\b(we|our|us)\s+(vs|versus)\s+(they|them|their)',
                r'\b(our|american)\s+(way|culture|values)\s+(vs|versus)',
                r'\b(them|they)\s+(don\'t|can\'t|won\'t)\s+(understand|appreciate)'
            ]
        }
        
        self.age_bias_patterns = {
            'age_stereotypes': [
                r'\b(young|old)\s+(people|students)\s+(can\'t|don\'t|won\'t)',
                r'\b(age|generation)\s+(determines|affects)\s+(ability|intelligence)',
                r'\b(teenagers|elderly|children)\s+(always|typically|naturally)',
                r'\b(too\s+(young|old))\s+(for|to)'
            ],
            'generational_assumptions': [
                r'\b(millennials|boomers|gen\s+z)\s+(all|always|typically)',
                r'\b(young|old)\s+(generation)\s+(doesn\'t|can\'t)',
                r'\b(modern|traditional)\s+(vs|versus)\s+(old|new)'
            ]
        }
        
        self.cultural_sensitivity_patterns = {
            'insensitive_terms': [
                r'\b(oriental|exotic|primitive|savage|uncivilized)',
                r'\b(third\s+world|developing|underdeveloped)',
                r'\b(foreign|alien|strange|weird)\s+(customs|traditions)',
                r'\b(their|them)\s+(kind|type|sort)'
            ],
            'cultural_misappropriation': [
                r'\b(costume|dress|outfit)\s+(as|like)\s+(native|tribal)',
                r'\b(cultural|traditional)\s+(items|objects)\s+(for|as)\s+(decoration)',
                r'\b(authentic|real)\s+(native|tribal|ethnic)\s+(experience)'
            ],
            'religious_sensitivity': [
                r'\b(religion|faith)\s+(vs|versus)\s+(science|reason)',
                r'\b(believers|non-believers)\s+(vs|versus)',
                r'\b(religious|spiritual)\s+(vs|versus)\s+(rational|logical)'
            ]
        }
        
        # Define positive inclusive language patterns
        self.inclusive_language_patterns = {
            'gender_inclusive': [
                r'\b(they|them|their)\s+(as|for)\s+(singular)',
                r'\b(person|individual|student)\s+(instead\s+of)',
                r'\b(people|persons)\s+(instead\s+of)',
                r'\b(professional|expert|specialist)\s+(instead\s+of)'
            ],
            'culturally_sensitive': [
                r'\b(diverse|inclusive|representative)',
                r'\b(cultural|ethnic|racial)\s+(diversity)',
                r'\b(respectful|respecting)\s+(differences)',
                r'\b(understanding|appreciating)\s+(cultures)'
            ],
            'age_inclusive': [
                r'\b(all\s+ages|diverse\s+ages)',
                r'\b(age-appropriate|age-inclusive)',
                r'\b(intergenerational|multi-generational)',
                r'\b(accessible|inclusive)\s+(for\s+all)'
            ]
        }
    
    def analyze_bias(self, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive bias analysis.
        
        Args:
            content: Content to analyze for bias
            
        Returns:
            Dict[str, Any]: Dictionary containing bias analysis results
        """
        # Analyze different types of bias
        gender_bias_results = self._analyze_gender_bias(content)
        racial_bias_results = self._analyze_racial_bias(content)
        age_bias_results = self._analyze_age_bias(content)
        cultural_sensitivity_results = self._analyze_cultural_sensitivity(content)
        inclusive_language_results = self._analyze_inclusive_language(content)
        
        # Calculate bias scores
        gender_bias_score = self._calculate_bias_score(gender_bias_results, 'gender')
        racial_bias_score = self._calculate_bias_score(racial_bias_results, 'racial')
        age_bias_score = self._calculate_bias_score(age_bias_results, 'age')
        cultural_sensitivity_score = self._calculate_bias_score(cultural_sensitivity_results, 'cultural')
        
        # Calculate overall bias score (lower is better)
        overall_bias_score = (
            gender_bias_score * 0.25 +
            racial_bias_score * 0.25 +
            age_bias_score * 0.20 +
            cultural_sensitivity_score * 0.30
        )
        
        # Calculate inclusive language bonus
        inclusive_bonus = self._calculate_inclusive_bonus(inclusive_language_results)
        
        # Final score (higher is better, with inclusive language bonus)
        final_score = max(0, min(100, 100 - overall_bias_score + inclusive_bonus))
        
        # Get assessment
        assessment = self._get_bias_assessment(final_score)
        
        # Compile flagged phrases
        flagged_phrases = (
            gender_bias_results['flagged_phrases'] +
            racial_bias_results['flagged_phrases'] +
            age_bias_results['flagged_phrases'] +
            cultural_sensitivity_results['flagged_phrases']
        )
        
        return {
            'score': round(final_score, 2),
            'gender_bias': gender_bias_score,
            'racial_bias': racial_bias_score,
            'age_bias': age_bias_score,
            'cultural_sensitivity': cultural_sensitivity_score,
            'assessment': assessment,
            'flagged_phrases': flagged_phrases,
            'gender_bias_details': gender_bias_results,
            'racial_bias_details': racial_bias_results,
            'age_bias_details': age_bias_results,
            'cultural_sensitivity_details': cultural_sensitivity_results,
            'inclusive_language_details': inclusive_language_results,
            'recommendations': self._generate_bias_recommendations({
                'gender_bias': gender_bias_score,
                'racial_bias': racial_bias_score,
                'age_bias': age_bias_score,
                'cultural_sensitivity': cultural_sensitivity_score,
                'overall_score': final_score
            })
        }
    
    def _analyze_gender_bias(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for gender bias.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Gender bias analysis results
        """
        flagged_phrases = []
        bias_indicators = 0
        
        # Check each type of gender bias
        for bias_type, patterns in self.gender_bias_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content.lower())
                if matches:
                    bias_indicators += len(matches)
                    flagged_phrases.extend(matches)
        
        return {
            'bias_indicators': bias_indicators,
            'flagged_phrases': flagged_phrases,
            'bias_types_found': list(self.gender_bias_patterns.keys())
        }
    
    def _analyze_racial_bias(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for racial bias.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Racial bias analysis results
        """
        flagged_phrases = []
        bias_indicators = 0
        
        # Check each type of racial bias
        for bias_type, patterns in self.racial_bias_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content.lower())
                if matches:
                    bias_indicators += len(matches)
                    flagged_phrases.extend(matches)
        
        return {
            'bias_indicators': bias_indicators,
            'flagged_phrases': flagged_phrases,
            'bias_types_found': list(self.racial_bias_patterns.keys())
        }
    
    def _analyze_age_bias(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for age bias.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Age bias analysis results
        """
        flagged_phrases = []
        bias_indicators = 0
        
        # Check each type of age bias
        for bias_type, patterns in self.age_bias_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content.lower())
                if matches:
                    bias_indicators += len(matches)
                    flagged_phrases.extend(matches)
        
        return {
            'bias_indicators': bias_indicators,
            'flagged_phrases': flagged_phrases,
            'bias_types_found': list(self.age_bias_patterns.keys())
        }
    
    def _analyze_cultural_sensitivity(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for cultural sensitivity issues.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Cultural sensitivity analysis results
        """
        flagged_phrases = []
        sensitivity_indicators = 0
        
        # Check each type of cultural sensitivity issue
        for sensitivity_type, patterns in self.cultural_sensitivity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content.lower())
                if matches:
                    sensitivity_indicators += len(matches)
                    flagged_phrases.extend(matches)
        
        return {
            'sensitivity_indicators': sensitivity_indicators,
            'flagged_phrases': flagged_phrases,
            'sensitivity_types_found': list(self.cultural_sensitivity_patterns.keys())
        }
    
    def _analyze_inclusive_language(self, content: str) -> Dict[str, Any]:
        """
        Analyze content for inclusive language usage.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Inclusive language analysis results
        """
        inclusive_indicators = 0
        inclusive_phrases = []
        
        # Check each type of inclusive language
        for inclusive_type, patterns in self.inclusive_language_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content.lower())
                if matches:
                    inclusive_indicators += len(matches)
                    inclusive_phrases.extend(matches)
        
        return {
            'inclusive_indicators': inclusive_indicators,
            'inclusive_phrases': inclusive_phrases,
            'inclusive_types_found': list(self.inclusive_language_patterns.keys())
        }
    
    def _calculate_bias_score(self, bias_results: Dict[str, Any], bias_type: str) -> float:
        """
        Calculate bias score for a specific type of bias.
        
        Args:
            bias_results: Results from bias analysis
            bias_type: Type of bias being scored
            
        Returns:
            float: Bias score (0-100, higher means more bias)
        """
        if bias_type == 'gender':
            indicators = bias_results['bias_indicators']
        elif bias_type == 'racial':
            indicators = bias_results['bias_indicators']
        elif bias_type == 'age':
            indicators = bias_results['bias_indicators']
        elif bias_type == 'cultural':
            indicators = bias_results['sensitivity_indicators']
        else:
            indicators = 0
        
        # Convert indicators to score (0-100)
        # More indicators = higher bias score
        if indicators == 0:
            return 0.0
        elif indicators <= 2:
            return 20.0
        elif indicators <= 5:
            return 40.0
        elif indicators <= 10:
            return 60.0
        elif indicators <= 15:
            return 80.0
        else:
            return 100.0
    
    def _calculate_inclusive_bonus(self, inclusive_results: Dict[str, Any]) -> float:
        """
        Calculate bonus for inclusive language usage.
        
        Args:
            inclusive_results: Results from inclusive language analysis
            
        Returns:
            float: Inclusive language bonus (0-20)
        """
        indicators = inclusive_results['inclusive_indicators']
        
        # Convert indicators to bonus (0-20)
        if indicators == 0:
            return 0.0
        elif indicators <= 3:
            return 5.0
        elif indicators <= 6:
            return 10.0
        elif indicators <= 10:
            return 15.0
        else:
            return 20.0
    
    def _get_bias_assessment(self, score: float) -> str:
        """
        Get bias assessment based on score.
        
        Args:
            score: Bias score (0-100, higher is better)
            
        Returns:
            str: Assessment description
        """
        if score >= 90:
            return "Excellent - Very inclusive and culturally sensitive"
        elif score >= 80:
            return "Good - Generally inclusive with minor issues"
        elif score >= 70:
            return "Fair - Some bias issues that should be addressed"
        elif score >= 60:
            return "Poor - Significant bias issues need attention"
        else:
            return "Very poor - Major bias issues require immediate attention"
    
    def _generate_bias_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate bias-related recommendations.
        
        Args:
            scores: Dictionary of bias scores
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Check gender bias
        if scores['gender_bias'] > 40:
            recommendations.append("Review and revise gender-specific language and stereotypes")
        
        # Check racial bias
        if scores['racial_bias'] > 40:
            recommendations.append("Address racial stereotypes and cultural assumptions")
        
        # Check age bias
        if scores['age_bias'] > 40:
            recommendations.append("Remove age-based assumptions and stereotypes")
        
        # Check cultural sensitivity
        if scores['cultural_sensitivity'] > 40:
            recommendations.append("Improve cultural sensitivity and avoid insensitive terms")
        
        # Overall recommendations
        if scores['overall_score'] < 70:
            recommendations.append("Conduct comprehensive bias review with diverse perspectives")
        
        if not recommendations:
            recommendations.append("Content demonstrates good cultural sensitivity and inclusivity")
        
        return recommendations
    

    

    
 