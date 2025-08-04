# Educational Resource Quality Evaluator

A comprehensive Command Line Interface (CLI) application for evaluating educational resources including textbooks, lesson plans, and learning content. The tool provides detailed analysis of curriculum alignment, readability, pedagogical quality, bias detection, and generates comprehensive reports.

## Project Overview

The Educational Resource Quality Evaluator is designed to help educators, curriculum developers, and educational institutions assess the quality and effectiveness of educational materials. The application uses advanced text analysis techniques to evaluate multiple aspects of educational content and provide actionable recommendations for improvement.

### Key Features

- **Curriculum Alignment Analysis**: Evaluates content against standard curriculum frameworks
- **Readability Assessment**: Calculates Flesch-Kincaid Grade Level and other readability metrics
- **Pedagogical Quality Evaluation**: Assesses learning objectives, examples, assessments, and structure
- **Bias & Sensitivity Detection**: Identifies potential bias and cultural sensitivity issues
- **Comprehensive Reporting**: Generates detailed evaluation reports with recommendations
- **Modular Architecture**: Object-oriented design with inheritance and polymorphism

## Requirements Specification

### System Requirements
- Python 3.8 or higher
- No external dependencies (uses only Python standard library)
- Minimum 50MB available disk space for reports
- Text-based educational materials (TXT, CSV formats)

### Standard Library Modules Used
- `csv`: CSV file processing
- `re`: Regular expressions for text analysis
- `os`: File system operations
- `math`: Mathematical calculations
- `statistics`: Statistical analysis
- `textwrap`: Text formatting
- `datetime`: Timestamp generation

### Supported File Formats
- **TXT**: Plain text files with educational content
- **CSV**: Comma-separated values files (content extracted from cells)

## User Guide

### Installation

1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd EduResourceEvaluator
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### CLI Commands and Usage

The application provides an interactive menu-driven interface:

```
Educational Resource Quality Evaluator
============================================================
A comprehensive tool for evaluating educational materials
including textbooks, lesson plans, and learning content.

Features:
- Curriculum alignment analysis
- Readability scoring
- Pedagogical quality assessment
- Bias and sensitivity detection
- Comprehensive reporting
============================================================

Main Menu:
1. Load Educational Material
2. Check Curriculum Alignment
3. Analyze Readability Score
4. Evaluate Pedagogical Quality
5. Run Bias & Sensitivity Analysis
6. Generate Final Evaluation Report
7. Exit
```

### Input Format

Educational materials should be in TXT or CSV format with the following structure:

**TXT Format Example:**
```
Title: Introduction to Basic Mathematics
Author: Educational Resource Team
Subject: Mathematics
Grade Level: Elementary (3-5)

Learning Objectives:
Students will understand basic addition and subtraction concepts.

Introduction:
Mathematics is a fundamental subject...

Examples:
• 4 + 2 = 6
• 7 + 1 = 8

Practice Exercises:
Complete the following problems...
```

**CSV Format:**
Content is extracted from all cells and combined into a single text for analysis.

### Sample Workflow

1. **Load Material**: Select option 1 and provide the path to your educational material file
2. **Run Analysis**: Select options 2-5 to perform different types of analysis
3. **Generate Report**: Select option 6 to create a comprehensive evaluation report
4. **Review Results**: Check the generated report in the `reports/` directory

### Sample Output

```
Curriculum Alignment Analysis
========================================
Alignment Score: 85.50/100
Covered Topics: 12
Missing Topics: 3
Overall Assessment: Good alignment with minor gaps

Readability Analysis
========================================
Flesch-Kincaid Grade Level: 6.2
Flesch Reading Ease: 72.5
Average Words per Sentence: 12.3
Readability Assessment: Appropriate for middle school students

Pedagogical Quality Evaluation
========================================
Pedagogical Score: 78.50/100
Learning Objectives: 8.5/10
Examples and Illustrations: 7.0/10
Assessment Elements: 8.0/10
Overall Assessment: Good pedagogical quality
```

## Technical Documentation

### Project Architecture

The application follows a modular, object-oriented design with clear separation of concerns:

```
EduResourceEvaluator/
├── main.py                   # CLI interface and application coordination
├── loader.py                 # File loading and format validation
├── curriculum_checker.py     # Curriculum alignment analysis
├── readability.py            # Readability metrics calculation
├── pedagogy.py               # Pedagogical quality assessment
├── bias_detection.py         # Bias and sensitivity analysis
├── report.py                 # Report generation and formatting
├── utils.py                  # Shared utility functions
├── test/                     # Unit tests
│   ├── test_readability.py
│   ├── test_curriculum.py
│   └── test_pedagogy.py
├── data/                     # Sample materials
│   └── sample_material.txt
└── reports/                  # Generated reports (created automatically)
```

### Module Purposes

#### main.py
- **Purpose**: Main CLI interface and application coordination
- **Key Classes**: `EducationalResourceEvaluator`
- **Responsibilities**: User interaction, menu navigation, component coordination

#### loader.py
- **Purpose**: File loading and content processing
- **Key Classes**: `MaterialLoader`
- **Responsibilities**: File validation, content extraction, metadata parsing

#### curriculum_checker.py
- **Purpose**: Curriculum alignment analysis
- **Key Classes**: `CurriculumChecker`
- **Responsibilities**: Topic matching, coverage analysis, alignment scoring

#### readability.py
- **Purpose**: Readability metrics calculation
- **Key Classes**: `ReadabilityAnalyzer`
- **Responsibilities**: Flesch-Kincaid, Gunning Fog, SMOG calculations

#### pedagogy.py
- **Purpose**: Pedagogical quality assessment
- **Key Classes**: `PedagogicalAnalyzer`
- **Responsibilities**: Learning objectives, examples, assessments, structure analysis

#### bias_detection.py
- **Purpose**: Bias and sensitivity analysis
- **Key Classes**: `BiasDetector`
- **Responsibilities**: Gender, racial, age bias detection, cultural sensitivity

#### report.py
- **Purpose**: Report generation and formatting
- **Key Classes**: `ReportGenerator`
- **Responsibilities**: Report creation, formatting, file output

#### utils.py
- **Purpose**: Shared utility functions
- **Key Functions**: Text processing, validation, formatting helpers

### Design Patterns

#### Object-Oriented Design
- **Inheritance**: All analyzer classes inherit common patterns
- **Polymorphism**: Different analyzers implement consistent interfaces
- **Encapsulation**: Each module encapsulates its specific functionality

#### Error Handling
- **Comprehensive Validation**: Input validation at multiple levels
- **Graceful Degradation**: Application continues with partial results
- **User-Friendly Messages**: Clear error messages and recovery options

#### Modular Structure
- **Loose Coupling**: Modules communicate through well-defined interfaces
- **High Cohesion**: Each module has a single, focused responsibility
- **Testability**: Each module can be tested independently

### Testing

Run the unit tests to verify functionality:

```bash
# Run all tests
python -m unittest discover test/

# Run specific test modules
python -m unittest test.test_readability
python -m unittest test.test_curriculum
python -m unittest test.test_pedagogy
```

### Performance Considerations

- **Text Processing**: Efficient regex patterns for text analysis
- **Memory Management**: Streaming processing for large files
- **File Size Limits**: 10MB maximum file size for performance
- **Caching**: Results cached during session for efficiency

### Extensibility

The modular design allows for easy extension:

1. **New Analyzers**: Add new analysis modules following the established pattern
2. **Additional Metrics**: Extend existing analyzers with new calculations
3. **File Formats**: Add support for new file formats in the loader
4. **Report Formats**: Create new report generators for different output formats

## Troubleshooting

### Common Issues

1. **File Not Found**: Ensure the file path is correct and the file exists
2. **Encoding Issues**: Files should be UTF-8 encoded for best results
3. **Large Files**: Files over 10MB may cause performance issues
4. **Empty Content**: Ensure files contain actual educational content

### Error Messages

- `File not found or not accessible`: Check file path and permissions
- `Unsupported file format`: Use TXT or CSV files only
- `File too large`: Reduce file size or split into smaller files
- `Unable to decode file content`: Check file encoding (use UTF-8)

## Contributing

This project follows best practices for educational software development:

1. **Code Quality**: Comprehensive docstrings and inline comments
2. **Testing**: Unit tests for all core functionality
3. **Documentation**: Clear user and technical documentation
4. **Accessibility**: CLI interface suitable for various users

## License

This project is designed for educational use and follows open-source principles. The code is provided as-is for educational and research purposes.

---

**Educational Resource Quality Evaluator Team**  
*Empowering educators with comprehensive content analysis tools* 