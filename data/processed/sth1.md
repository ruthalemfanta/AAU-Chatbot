# AAU Helpdesk Chatbot - Processed Data Documentation

## Data Processing Pipeline

This document outlines the data processing pipeline for the AAU Helpdesk Chatbot project.

### 1. Data Collection Sources

#### Web Scraping
- AAU official website (www.aau.edu.et)
- Academic department pages
- Student services information
- Admission and registration guidelines

#### Telegram Channels
- Official AAU channels
- Student discussion groups
- Announcement channels
- Q&A sessions

#### Synthetic Data Generation
- Template-based query generation
- Parameter variation
- Intent-specific examples
- Edge case scenarios

### 2. Data Preprocessing Steps

#### Text Cleaning
1. Remove extra whitespace
2. Normalize punctuation
3. Handle special characters
4. Convert to lowercase for processing

#### Parameter Extraction
1. Named Entity Recognition (NER)
2. Rule-based pattern matching
3. Department name normalization
4. Date and number extraction

#### Intent Classification
1. Keyword-based initial classification
2. Context analysis
3. Confidence scoring
4. Fallback to general_info

### 3. Training Data Format

```json
{
  "text": "User query text",
  "intent": "intent_category",
  "parameters": {
    "department": ["computer science"],
    "semester": ["second"],
    "year": ["2024"]
  },
  "source": "web|telegram|synthetic",
  "confidence": 0.95
}
```

### 4. Quality Metrics

#### Intent Classification
- Accuracy: Target >85%
- Precision per intent: Target >80%
- Recall per intent: Target >80%
- F1-score: Target >80%

#### Parameter Extraction
- Department extraction: Target precision >90%
- Semester extraction: Target precision >85%
- Year extraction: Target precision >95%
- Document type: Target precision >90%
- Fee amount: Target precision >85%

### 5. Data Validation Rules

#### Text Quality
- Minimum length: 10 characters
- Maximum length: 500 characters
- Language: English (with some Amharic terms)
- No personal information (PII)

#### Parameter Validation
- Years: 2000-2027 range
- Semesters: Valid semester names
- Departments: AAU department list
- Amounts: Numeric values only

### 6. Evaluation Methodology

#### Cross-Validation
- 80% training, 20% testing split
- Stratified sampling by intent
- 5-fold cross-validation for robustness

#### Parameter-Level Precision
- Individual parameter evaluation
- Precision, Recall, F1 per parameter type
- Confusion matrix analysis
- Error case analysis

### 7. Continuous Improvement

#### Data Collection
- Regular web scraping updates
- New Telegram message collection
- User feedback integration
- Edge case identification

#### Model Updates
- Monthly retraining cycles
- Performance monitoring
- A/B testing for improvements
- Feedback loop integration

## Processed Data Statistics

- Total training samples: ~500-1000
- Intent distribution: Balanced across 10 categories
- Parameter coverage: 95% of common scenarios
- Data sources: 40% synthetic, 30% web, 30% Telegram
- Quality score: >90% manually verified

## Usage Guidelines

1. Load processed data using DataLoader utility
2. Validate data format before training
3. Monitor parameter extraction precision
4. Regular evaluation against test set
5. Update training data monthly