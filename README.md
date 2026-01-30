# AAU Helpdesk Chatbot

A scalable NLP-powered chatbot for Addis Ababa University (AAU) helpdesk services with precise intent recognition and parameter extraction.

## 🎯 Project Overview

This project implements a domain-specific customer support chatbot for AAU that assists users with common helpdesk queries related to:

- **Admissions** - Application requirements, deadlines, procedures
- **Registration** - Course enrollment, semester registration
- **Fees** - Payment information, amounts, methods
- **Transcripts** - Document requests, processing times
- **Grades** - Result inquiries, grade reports
- **General Information** - University services, contact details

## 🚀 Key Features

### NLP Capabilities
- **Intent Recognition**: Supervised text classification with 10 predefined intents
- **Parameter Extraction**: Named Entity Recognition + rule-based methods
- **Parameter-Level Precision**: Individual evaluation of each parameter type
- **Confidence Scoring**: Reliability assessment for responses

### Architecture
- **Modular Design**: Extensible architecture for new intents/parameters
- **Template-Based Responses**: Dynamic response generation with follow-ups
- **Missing Parameter Detection**: Intelligent follow-up questions
- **Multi-Source Training**: Web scraping + Telegram + synthetic data

### Technical Stack
- **Backend**: FastAPI with async support
- **NLP**: spaCy, HuggingFace Transformers, scikit-learn
- **Models**: TF-IDF + Naive Bayes, BERT-based transformers
- **Data**: JSON-based training data with comprehensive validation

## 📁 Project Structure

```
AAU-Chatbot/
├── app/
│   ├── main.py              # FastAPI application
│   ├── nlp_engine.py        # Core NLP processing
│   ├── templates.py         # Response templates
│   └── utils.py             # Utility functions
├── data/
│   ├── raw/                 # Raw training data
│   └── processed/           # Processed datasets
├── models/
│   └── sth.py              # Advanced model implementations
├── scripts/
│   ├── web_scrapper.py     # Data collection from web
│   └── telegram_cli.py     # Telegram data collection
├── tests/
│   └── test.py             # Comprehensive test suite
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone Repository
```bash
git clone <repository-url>
cd AAU-Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 4. Collect Training Data
```bash
# Generate synthetic data and scrape web sources
python scripts/web_scrapper.py

# Collect Telegram data (simulated)
python scripts/telegram_cli.py --collect
```

### 5. Train Models (Optional)
```bash
python models/sth.py
```

### 6. Run the Application
```bash
# Start FastAPI server
python app/main.py

# Or using uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Usage

### API Endpoints

#### Chat with the Bot
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "I want to apply for computer science admission"}'
```

#### Train with New Data
```bash
curl -X POST "http://localhost:8000/train" \
     -H "Content-Type: application/json" \
     -d '{"training_data": [{"text": "How do I register?", "intent": "registration_help"}]}'
```

#### Evaluate Performance
```bash
curl -X POST "http://localhost:8000/evaluate" \
     -H "Content-Type: application/json" \
     -d '[{"text": "I need my transcript", "intent": "transcript_request"}]'
```

### Python Integration

```python
from app.nlp_engine import AAUNLPEngine
from app.templates import ResponseTemplates

# Initialize components
engine = AAUNLPEngine()
templates = ResponseTemplates()

# Process user query
result = engine.process_query("I want to apply for engineering admission")

# Generate response
response = templates.generate_response(
    result['intent'], 
    result['parameters'], 
    result['missing_parameters'], 
    result['confidence']
)

print(response)
```

## 📊 Performance Metrics

### Intent Classification
- **Target Accuracy**: >85%
- **Confidence Threshold**: 0.6
- **Supported Intents**: 10 categories

### Parameter Extraction Precision
- **Department**: >90% precision
- **Semester**: >85% precision  
- **Year**: >95% precision
- **Document Type**: >90% precision
- **Fee Amount**: >85% precision

### Response Quality
- **Template Coverage**: 100% of intents
- **Follow-up Questions**: Automatic for missing parameters
- **Clarification**: Triggered for low confidence (<0.6)

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/test.py -v
```

### Run Specific Test Categories
```bash
# Test NLP engine
python -m pytest tests/test.py::TestAAUNLPEngine -v

# Test parameter extraction
python -m pytest tests/test.py::TestParameterExtractor -v

# Test response templates
python -m pytest tests/test.py::TestResponseTemplates -v
```

### Integration Testing
```bash
# Test full conversation flow
python -m pytest tests/test.py::TestIntegration -v
```

## 📈 Data Collection

### Web Scraping
```bash
python scripts/web_scrapper.py
```
- Scrapes AAU official website
- Extracts relevant content by intent
- Generates training samples automatically

### Telegram Data
```bash
python scripts/telegram_cli.py --interactive
```
- Simulates Telegram channel data
- Filters relevant messages
- Processes for training format

### Synthetic Data
- Template-based generation
- Parameter variation
- Intent-specific examples
- Edge case coverage

## 🔄 Model Training

### Basic Training
```python
from app.nlp_engine import AAUNLPEngine
from app.utils import DataLoader

# Load training data
data = DataLoader.get_sample_training_data()

# Initialize and train
engine = AAUNLPEngine()
engine.train_intent_classifier(data)
```

### Advanced Training
```bash
python models/sth.py
```
- Transformer-based models
- Cross-validation
- Parameter-level evaluation
- Model persistence

## 🎛️ Configuration

### Default Settings
```json
{
  "confidence_threshold": 0.6,
  "max_follow_up_questions": 2,
  "log_conversations": true,
  "model_settings": {
    "max_features": 1000,
    "use_spacy": true,
    "spacy_model": "en_core_web_sm"
  }
}
```

### Environment Variables
- `AAU_CHATBOT_CONFIG`: Path to config file
- `AAU_CHATBOT_LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- `AAU_CHATBOT_PORT`: Server port (default: 8000)

## 🚀 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
- Use PostgreSQL for conversation storage
- Implement Redis for session management
- Add authentication and rate limiting
- Set up monitoring and logging
- Configure HTTPS and security headers

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest`
5. Submit pull request

### Code Standards
- Follow PEP 8 style guide
- Add type hints for functions
- Write comprehensive tests
- Update documentation
- Maintain >80% test coverage

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Addis Ababa University for domain expertise
- spaCy and HuggingFace for NLP tools
- FastAPI for the web framework
- Contributors and testers

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation in `/docs`

---

**Built with ❤️ for Addis Ababa University students and staff**