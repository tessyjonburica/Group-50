#!/usr/bin/env python3
"""
Educational Resource Quality Evaluator - Main CLI Interface

This module provides the command-line interface for the Educational Resource
Quality Evaluator. It handles user interaction, menu navigation, and
coordinates all evaluation components.

"""

import os
import sys
from typing import Optional, Dict, Any

# Import our custom modules
from loader import MaterialLoader
from curriculum_checker import CurriculumChecker
from readability import ReadabilityAnalyzer
from pedagogy import PedagogicalAnalyzer
from bias_detection import BiasDetector
from report import ReportGenerator
from utils import clear_screen, validate_file_path


class EducationalResourceEvaluator:
    """
    Main CLI application class for educational resource evaluation.
    
    This class manages the user interface and coordinates all evaluation
    components including file loading, curriculum checking, readability
    analysis, pedagogical assessment, bias detection, and report generation.
    """
    
    def __init__(self):
        """Initialize the evaluator with all analysis components."""
        self.loader = MaterialLoader()
        self.curriculum_checker = CurriculumChecker()
        self.readability_analyzer = ReadabilityAnalyzer()
        self.pedagogical_analyzer = PedagogicalAnalyzer()
        self.bias_detector = BiasDetector()
        self.report_generator = ReportGenerator()
        
        # Store evaluation data
        self.current_material = None
        self.evaluation_results = {}
    
    def display_welcome(self):
        """Display welcome message and application information."""
        clear_screen()
        print("=" * 60)
        print("Educational Resource Quality Evaluator")
        print("=" * 60)
        print("A comprehensive tool for evaluating educational materials")
        print("including textbooks, lesson plans, and learning content.")
        print()
        print("Features:")
        print("- Curriculum alignment analysis")
        print("- Readability scoring")
        print("- Pedagogical quality assessment")
        print("- Bias and sensitivity detection")
        print("- Comprehensive reporting")
        print("=" * 60)
        print()
    
    def display_menu(self):
        """Display the main menu options."""
        print("Main Menu:")
        print("1. Load Educational Material")
        print("2. Check Curriculum Alignment")
        print("3. Analyze Readability Score")
        print("4. Evaluate Pedagogical Quality")
        print("5. Run Bias & Sensitivity Analysis")
        print("6. Generate Final Evaluation Report")
        print("7. Exit")
        print()
    
    def get_user_choice(self) -> str:
        """Get and validate user menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                print("Invalid choice. Please enter a number between 1 and 7.")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                sys.exit(0)
    
    def load_material(self):
        """Handle educational material loading."""
        print("\n" + "=" * 40)
        print("Load Educational Material")
        print("=" * 40)
        
        while True:
            file_path = input("Enter the path to your educational material file: ").strip()
            
            if not file_path:
                print("Please provide a file path.")
                continue
            
            if not validate_file_path(file_path):
                print("Invalid file path. Please check the file exists and is accessible.")
                continue
            
            try:
                self.current_material = self.loader.load_material(file_path)
                print(f"Successfully loaded: {file_path}")
                print(f"Content length: {len(self.current_material['content'])} characters")
                print(f"Paragraphs: {len(self.current_material['paragraphs'])}")
                break
            except Exception as e:
                print(f"Error loading file: {e}")
                retry = input("Would you like to try another file? (y/n): ").strip().lower()
                if retry != 'y':
                    break
        
        input("\nPress Enter to continue...")
    
    def check_curriculum_alignment(self):
        """Handle curriculum alignment analysis."""
        if not self.current_material:
            print("Please load educational material first (Option 1).")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 40)
        print("Curriculum Alignment Analysis")
        print("=" * 40)
        
        try:
            alignment_results = self.curriculum_checker.analyze_alignment(
                self.current_material['content']
            )
            self.evaluation_results['curriculum'] = alignment_results
            
            print(f"Alignment Score: {alignment_results['score']:.2f}/100")
            print(f"Covered Topics: {len(alignment_results['covered_topics'])}")
            print(f"Missing Topics: {len(alignment_results['missing_topics'])}")
            print(f"Overall Assessment: {alignment_results['assessment']}")
            
        except Exception as e:
            print(f"Error during curriculum analysis: {e}")
        
        input("\nPress Enter to continue...")
    
    def analyze_readability(self):
        """Handle readability analysis."""
        if not self.current_material:
            print("Please load educational material first (Option 1).")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 40)
        print("Readability Analysis")
        print("=" * 40)
        
        try:
            readability_results = self.readability_analyzer.analyze_readability(
                self.current_material['content']
            )
            self.evaluation_results['readability'] = readability_results
            
            print(f"Flesch-Kincaid Grade Level: {readability_results['grade_level']:.1f}")
            print(f"Flesch Reading Ease: {readability_results['reading_ease']:.1f}")
            print(f"Average Words per Sentence: {readability_results['avg_words_per_sentence']:.1f}")
            print(f"Average Syllables per Word: {readability_results['avg_syllables_per_word']:.2f}")
            print(f"Readability Assessment: {readability_results['assessment']}")
            
        except Exception as e:
            print(f"Error during readability analysis: {e}")
        
        input("\nPress Enter to continue...")
    
    def evaluate_pedagogy(self):
        """Handle pedagogical quality evaluation."""
        if not self.current_material:
            print("Please load educational material first (Option 1).")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 40)
        print("Pedagogical Quality Evaluation")
        print("=" * 40)
        
        try:
            pedagogy_results = self.pedagogical_analyzer.evaluate_pedagogy(
                self.current_material['content']
            )
            self.evaluation_results['pedagogy'] = pedagogy_results
            
            print(f"Pedagogical Score: {pedagogy_results['score']:.2f}/100")
            print(f"Learning Objectives: {pedagogy_results['objectives_score']:.1f}/10")
            print(f"Examples and Illustrations: {pedagogy_results['examples_score']:.1f}/10")
            print(f"Assessment Elements: {pedagogy_results['assessment_score']:.1f}/10")
            print(f"Structure and Organization: {pedagogy_results['structure_score']:.1f}/10")
            print(f"Overall Assessment: {pedagogy_results['assessment']}")
            
        except Exception as e:
            print(f"Error during pedagogical analysis: {e}")
        
        input("\nPress Enter to continue...")
    
    def run_bias_analysis(self):
        """Handle bias and sensitivity analysis."""
        if not self.current_material:
            print("Please load educational material first (Option 1).")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 40)
        print("Bias & Sensitivity Analysis")
        print("=" * 40)
        
        try:
            bias_results = self.bias_detector.analyze_bias(
                self.current_material['content']
            )
            self.evaluation_results['bias'] = bias_results
            
            print(f"Bias Score: {bias_results['score']:.2f}/100")
            print(f"Cultural Sensitivity: {bias_results['cultural_sensitivity']}")
            print(f"Gender Bias: {bias_results['gender_bias']}")
            print(f"Racial Bias: {bias_results['racial_bias']}")
            print(f"Age Bias: {bias_results['age_bias']}")
            print(f"Overall Assessment: {bias_results['assessment']}")
            
            if bias_results['flagged_phrases']:
                print("\nFlagged Phrases:")
                for phrase in bias_results['flagged_phrases'][:5]:  # Show first 5
                    print(f"- {phrase}")
                if len(bias_results['flagged_phrases']) > 5:
                    print(f"... and {len(bias_results['flagged_phrases']) - 5} more")
            
        except Exception as e:
            print(f"Error during bias analysis: {e}")
        
        input("\nPress Enter to continue...")
    
    def generate_report(self):
        """Handle final evaluation report generation."""
        if not self.current_material:
            print("Please load educational material first (Option 1).")
            input("Press Enter to continue...")
            return
        
        if not self.evaluation_results:
            print("Please run at least one analysis before generating a report.")
            input("Press Enter to continue...")
            return
        
        print("\n" + "=" * 40)
        print("Generate Final Evaluation Report")
        print("=" * 40)
        
        try:
            # Generate comprehensive report
            report_path = self.report_generator.generate_comprehensive_report(
                self.current_material,
                self.evaluation_results
            )
            
            print(f"Report generated successfully: {report_path}")
            print("\nReport Summary:")
            
            scores = []
            for component in ['curriculum', 'readability', 'pedagogy', 'bias']:
                if component in self.evaluation_results:
                    score = self.evaluation_results[component]['score']
                    if component == 'readability':
                        score = self.evaluation_results[component]['grade_level']
                    scores.append(score)
            
            if scores:
                overall_score = sum(scores) / len(scores)
                print(f"Overall Quality Score: {overall_score:.2f}/100")
                
                if overall_score >= 80:
                    recommendation = "Excellent - Ready for use"
                elif overall_score >= 60:
                    recommendation = "Good - Minor improvements needed"
                elif overall_score >= 40:
                    recommendation = "Fair - Significant improvements needed"
                else:
                    recommendation = "Poor - Major revisions required"
                
                print(f"Recommendation: {recommendation}")
            
        except Exception as e:
            print(f"Error generating report: {e}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop."""
        self.display_welcome()
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.load_material()
            elif choice == '2':
                self.check_curriculum_alignment()
            elif choice == '3':
                self.analyze_readability()
            elif choice == '4':
                self.evaluate_pedagogy()
            elif choice == '5':
                self.run_bias_analysis()
            elif choice == '6':
                self.generate_report()
            elif choice == '7':
                print("Thank you for using the Educational Resource Quality Evaluator!")
                sys.exit(0)


def main():
    """Main entry point for the application."""
    try:
        evaluator = EducationalResourceEvaluator()
        evaluator.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 