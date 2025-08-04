"""
Report Generator for Educational Resource Quality Evaluator.

This module generates comprehensive evaluation reports in various formats
including text reports with detailed analysis, recommendations, and
summaries of all evaluation components.

"""

import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from utils import format_timestamp


class ReportGenerator:
    """
    Generates comprehensive evaluation reports for educational resources.
    
    This class provides methods to create detailed reports including
    all evaluation results, recommendations, and actionable insights
    for improving educational content quality.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        self.report_directory = "reports"
        self.max_line_length = 80
        
        # Ensure reports directory exists
        if not os.path.exists(self.report_directory):
            os.makedirs(self.report_directory)
    
    def generate_comprehensive_report(self, material_data: Dict[str, Any], 
                                   evaluation_results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive evaluation report.
        
        Args:
            material_data: Loaded material data
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Path to the generated report file
        """
        # Create report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_report_{timestamp}.txt"
        filepath = os.path.join(self.report_directory, filename)
        
        # Generate report content
        report_content = self._create_report_content(material_data, evaluation_results)
        
        # Write report to file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(report_content)
        
        return filepath
    
    def _create_report_content(self, material_data: Dict[str, Any], 
                             evaluation_results: Dict[str, Any]) -> str:
        """
        Create the complete report content.
        
        Args:
            material_data: Loaded material data
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Complete report content
        """
        content_parts = []
        
        # Header
        content_parts.append(self._create_header())
        
        # Material information
        content_parts.append(self._create_material_section(material_data))
        
        # Executive summary
        content_parts.append(self._create_executive_summary(evaluation_results))
        
        # Detailed analysis sections
        if 'curriculum' in evaluation_results:
            content_parts.append(self._create_curriculum_section(evaluation_results['curriculum']))
        
        if 'readability' in evaluation_results:
            content_parts.append(self._create_readability_section(evaluation_results['readability']))
        
        if 'pedagogy' in evaluation_results:
            content_parts.append(self._create_pedagogy_section(evaluation_results['pedagogy']))
        
        if 'bias' in evaluation_results:
            content_parts.append(self._create_bias_section(evaluation_results['bias']))
        
        # Overall assessment and recommendations
        content_parts.append(self._create_overall_assessment(evaluation_results))
        
        # Footer
        content_parts.append(self._create_footer())
        
        return '\n\n'.join(content_parts)
    
    def _create_header(self) -> str:
        """
        Create report header.
        
        Returns:
            str: Report header
        """
        header = [
            "=" * 80,
            "EDUCATIONAL RESOURCE QUALITY EVALUATION REPORT",
            "=" * 80,
            f"Generated: {format_timestamp()}",
            "Educational Resource Quality Evaluator",
            "Comprehensive Analysis and Recommendations",
            "=" * 80
        ]
        
        return '\n'.join(header)
    
    def _create_material_section(self, material_data: Dict[str, Any]) -> str:
        """
        Create material information section.
        
        Args:
            material_data: Loaded material data
            
        Returns:
            str: Material information section
        """
        sections = [
            "MATERIAL INFORMATION",
            "-" * 40
        ]
        
        # Basic file information
        sections.append(f"File Path: {material_data.get('file_path', 'Unknown')}")
        sections.append(f"File Type: {material_data.get('file_type', 'Unknown')}")
        
        # Content statistics
        content = material_data.get('content', '')
        sections.append(f"Content Length: {len(content)} characters")
        sections.append(f"Word Count: {len(content.split())}")
        sections.append(f"Paragraph Count: {len(material_data.get('paragraphs', []))}")
        
        # Metadata
        metadata = material_data.get('metadata', {})
        if metadata:
            sections.append("\nMetadata:")
            for key, value in metadata.items():
                if value:
                    sections.append(f"  {key.title()}: {value}")
        
        return '\n'.join(sections)
    
    def _create_executive_summary(self, evaluation_results: Dict[str, Any]) -> str:
        """
        Create executive summary section.
        
        Args:
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Executive summary section
        """
        sections = [
            "EXECUTIVE SUMMARY",
            "-" * 40
        ]
        
        # Calculate overall score
        scores = []
        if 'curriculum' in evaluation_results:
            scores.append(evaluation_results['curriculum']['score'])
        if 'readability' in evaluation_results:
            scores.append(evaluation_results['readability']['grade_level'])
        if 'pedagogy' in evaluation_results:
            scores.append(evaluation_results['pedagogy']['score'])
        if 'bias' in evaluation_results:
            scores.append(evaluation_results['bias']['score'])
        
        if scores:
            overall_score = sum(scores) / len(scores)
            sections.append(f"Overall Quality Score: {overall_score:.2f}/100")
            
            if overall_score >= 80:
                recommendation = "EXCELLENT - Ready for use with minor improvements"
            elif overall_score >= 60:
                recommendation = "GOOD - Suitable with some modifications"
            elif overall_score >= 40:
                recommendation = "FAIR - Requires significant improvements"
            else:
                recommendation = "POOR - Major revisions needed"
            
            sections.append(f"Recommendation: {recommendation}")
        
        # Key findings
        sections.append("\nKey Findings:")
        
        if 'curriculum' in evaluation_results:
            curriculum = evaluation_results['curriculum']
            sections.append(f"  • Curriculum Alignment: {curriculum['score']:.1f}/100")
            sections.append(f"  • Topics Covered: {len(curriculum['covered_topics'])}")
            sections.append(f"  • Topics Missing: {len(curriculum['missing_topics'])}")
        
        if 'readability' in evaluation_results:
            readability = evaluation_results['readability']
            sections.append(f"  • Readability Grade Level: {readability['grade_level']:.1f}")
            sections.append(f"  • Reading Ease: {readability['reading_ease']:.1f}")
        
        if 'pedagogy' in evaluation_results:
            pedagogy = evaluation_results['pedagogy']
            sections.append(f"  • Pedagogical Quality: {pedagogy['score']:.1f}/100")
        
        if 'bias' in evaluation_results:
            bias = evaluation_results['bias']
            sections.append(f"  • Bias Assessment: {bias['score']:.1f}/100")
            sections.append(f"  • Flagged Phrases: {len(bias['flagged_phrases'])}")
        
        return '\n'.join(sections)
    
    def _create_curriculum_section(self, curriculum_results: Dict[str, Any]) -> str:
        """
        Create curriculum alignment section.
        
        Args:
            curriculum_results: Curriculum evaluation results
            
        Returns:
            str: Curriculum section
        """
        sections = [
            "CURRICULUM ALIGNMENT ANALYSIS",
            "-" * 40,
            f"Alignment Score: {curriculum_results['score']:.2f}/100",
            f"Assessment: {curriculum_results['assessment']}",
            ""
        ]
        
        # Subject breakdown
        if 'subject_alignments' in curriculum_results:
            sections.append("Subject Area Breakdown:")
            for subject, alignment in curriculum_results['subject_alignments'].items():
                sections.append(f"  • {subject.title()}: {alignment['score']:.1f}/100")
        
        # Coverage details
        sections.append(f"\nCoverage Details:")
        sections.append(f"  • Topics Covered: {len(curriculum_results['covered_topics'])}")
        sections.append(f"  • Topics Missing: {len(curriculum_results['missing_topics'])}")
        sections.append(f"  • Coverage Percentage: {curriculum_results['coverage_percentage']:.1f}%")
        
        # Recommendations
        if 'recommendations' in curriculum_results:
            sections.append("\nRecommendations:")
            for rec in curriculum_results['recommendations']:
                sections.append(f"  • {rec}")
        
        return '\n'.join(sections)
    
    def _create_readability_section(self, readability_results: Dict[str, Any]) -> str:
        """
        Create readability analysis section.
        
        Args:
            readability_results: Readability evaluation results
            
        Returns:
            str: Readability section
        """
        sections = [
            "READABILITY ANALYSIS",
            "-" * 40,
            f"Flesch-Kincaid Grade Level: {readability_results['grade_level']:.1f}",
            f"Flesch Reading Ease: {readability_results['reading_ease']:.1f}",
            f"Assessment: {readability_results['assessment']}",
            ""
        ]
        
        # Detailed metrics
        sections.append("Detailed Metrics:")
        sections.append(f"  • Average Words per Sentence: {readability_results['avg_words_per_sentence']:.1f}")
        sections.append(f"  • Average Syllables per Word: {readability_results['avg_syllables_per_word']:.2f}")
        sections.append(f"  • Word Count: {readability_results['word_count']}")
        sections.append(f"  • Sentence Count: {readability_results['sentence_count']}")
        sections.append(f"  • Complexity Level: {readability_results['complexity_level']}")
        sections.append(f"  • Recommended Audience: {readability_results['recommended_audience']}")
        
        # Additional formulas
        if 'gunning_fog_index' in readability_results:
            sections.append(f"  • Gunning Fog Index: {readability_results['gunning_fog_index']:.1f}")
        if 'smog_index' in readability_results:
            sections.append(f"  • SMOG Index: {readability_results['smog_index']:.1f}")
        
        return '\n'.join(sections)
    
    def _create_pedagogy_section(self, pedagogy_results: Dict[str, Any]) -> str:
        """
        Create pedagogical quality section.
        
        Args:
            pedagogy_results: Pedagogical evaluation results
            
        Returns:
            str: Pedagogy section
        """
        sections = [
            "PEDAGOGICAL QUALITY ANALYSIS",
            "-" * 40,
            f"Overall Pedagogical Score: {pedagogy_results['score']:.2f}/100",
            f"Assessment: {pedagogy_results['assessment']}",
            ""
        ]
        
        # Component scores
        sections.append("Component Scores:")
        sections.append(f"  • Learning Objectives: {pedagogy_results['objectives_score']:.1f}/10")
        sections.append(f"  • Examples & Illustrations: {pedagogy_results['examples_score']:.1f}/10")
        sections.append(f"  • Assessment Elements: {pedagogy_results['assessment_score']:.1f}/10")
        sections.append(f"  • Structure & Organization: {pedagogy_results['structure_score']:.1f}/10")
        sections.append(f"  • Engagement Factors: {pedagogy_results['engagement_score']:.1f}/10")
        
        # Recommendations
        if 'recommendations' in pedagogy_results:
            sections.append("\nRecommendations:")
            for rec in pedagogy_results['recommendations']:
                sections.append(f"  • {rec}")
        
        return '\n'.join(sections)
    
    def _create_bias_section(self, bias_results: Dict[str, Any]) -> str:
        """
        Create bias and sensitivity section.
        
        Args:
            bias_results: Bias evaluation results
            
        Returns:
            str: Bias section
        """
        sections = [
            "BIAS & SENSITIVITY ANALYSIS",
            "-" * 40,
            f"Overall Bias Score: {bias_results['score']:.2f}/100",
            f"Assessment: {bias_results['assessment']}",
            ""
        ]
        
        # Bias breakdown
        sections.append("Bias Analysis:")
        sections.append(f"  • Gender Bias: {bias_results['gender_bias']:.1f}/100")
        sections.append(f"  • Racial Bias: {bias_results['racial_bias']:.1f}/100")
        sections.append(f"  • Age Bias: {bias_results['age_bias']:.1f}/100")
        sections.append(f"  • Cultural Sensitivity: {bias_results['cultural_sensitivity']:.1f}/100")
        
        # Flagged phrases
        if bias_results['flagged_phrases']:
            sections.append(f"\nFlagged Phrases ({len(bias_results['flagged_phrases'])} found):")
            for phrase in bias_results['flagged_phrases'][:10]:  # Show first 10
                sections.append(f"  • {phrase}")
            if len(bias_results['flagged_phrases']) > 10:
                sections.append(f"  ... and {len(bias_results['flagged_phrases']) - 10} more")
        
        # Recommendations
        if 'recommendations' in bias_results:
            sections.append("\nRecommendations:")
            for rec in bias_results['recommendations']:
                sections.append(f"  • {rec}")
        
        return '\n'.join(sections)
    
    def _create_overall_assessment(self, evaluation_results: Dict[str, Any]) -> str:
        """
        Create overall assessment and recommendations section.
        
        Args:
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Overall assessment section
        """
        sections = [
            "OVERALL ASSESSMENT & RECOMMENDATIONS",
            "-" * 40
        ]
        
        # Compile all recommendations
        all_recommendations = []
        
        for component, results in evaluation_results.items():
            if 'recommendations' in results:
                all_recommendations.extend(results['recommendations'])
        
        if all_recommendations:
            sections.append("Priority Recommendations:")
            for i, rec in enumerate(all_recommendations[:5], 1):  # Top 5
                sections.append(f"  {i}. {rec}")
        
        # Action items
        sections.append("\nAction Items:")
        sections.append("  1. Review flagged bias issues and revise insensitive language")
        sections.append("  2. Address curriculum gaps by adding missing topics")
        sections.append("  3. Improve readability if grade level is inappropriate")
        sections.append("  4. Enhance pedagogical elements (objectives, examples, assessments)")
        sections.append("  5. Consider feedback from diverse stakeholders")
        
        return '\n'.join(sections)
    
    def _create_footer(self) -> str:
        """
        Create report footer.
        
        Returns:
            str: Report footer
        """
        footer = [
            "=" * 80,
            "Report generated by Educational Resource Quality Evaluator",
            f"Generated on: {format_timestamp()}",
            "For questions or support, please refer to the user manual",
            "=" * 80
        ]
        
        return '\n'.join(footer)
    
    def generate_summary_report(self, material_data: Dict[str, Any], 
                              evaluation_results: Dict[str, Any]) -> str:
        """
        Generate a concise summary report.
        
        Args:
            material_data: Loaded material data
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Path to the generated summary report file
        """
        # Create summary filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.txt"
        filepath = os.path.join(self.report_directory, filename)
        
        # Generate summary content
        summary_content = self._create_summary_content(material_data, evaluation_results)
        
        # Write summary to file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(summary_content)
        
        return filepath
    
    def _create_summary_content(self, material_data: Dict[str, Any], 
                              evaluation_results: Dict[str, Any]) -> str:
        """
        Create summary report content.
        
        Args:
            material_data: Loaded material data
            evaluation_results: Results from all evaluations
            
        Returns:
            str: Summary report content
        """
        sections = [
            "EDUCATIONAL RESOURCE EVALUATION SUMMARY",
            "=" * 50,
            f"File: {material_data.get('file_path', 'Unknown')}",
            f"Generated: {format_timestamp()}",
            ""
        ]
        
        # Quick scores
        sections.append("QUICK SCORES:")
        if 'curriculum' in evaluation_results:
            sections.append(f"  Curriculum Alignment: {evaluation_results['curriculum']['score']:.1f}/100")
        if 'readability' in evaluation_results:
            sections.append(f"  Readability Grade: {evaluation_results['readability']['grade_level']:.1f}")
        if 'pedagogy' in evaluation_results:
            sections.append(f"  Pedagogical Quality: {evaluation_results['pedagogy']['score']:.1f}/100")
        if 'bias' in evaluation_results:
            sections.append(f"  Bias Assessment: {evaluation_results['bias']['score']:.1f}/100")
        
        # Overall recommendation
        scores = []
        for component in ['curriculum', 'pedagogy', 'bias']:
            if component in evaluation_results:
                scores.append(evaluation_results[component]['score'])
        
        if scores:
            avg_score = sum(scores) / len(scores)
            sections.append(f"\nOverall Score: {avg_score:.1f}/100")
            
            if avg_score >= 80:
                recommendation = "EXCELLENT - Ready for use"
            elif avg_score >= 60:
                recommendation = "GOOD - Minor improvements needed"
            elif avg_score >= 40:
                recommendation = "FAIR - Significant improvements needed"
            else:
                recommendation = "POOR - Major revisions required"
            
            sections.append(f"Recommendation: {recommendation}")
        
        return '\n'.join(sections)
    
 