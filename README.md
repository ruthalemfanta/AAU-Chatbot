# AAU Helpdesk Chatbot

A scalable NLP-based chatbot for Addis Ababa University (AAU) helpdesk services, capable of intent recognition and parameter extraction for handling common support queries.

## Project Overview

This chatbot assists users by answering common helpdesk queries related to:
- Admissions
- Registration
- Fees and payments
- Transcripts
- Academic information
- General administrative services

## Features

- **Intent Recognition**: Classifies user queries into 10-15 predefined intents
- **Parameter Extraction**: Extracts required parameters (department, document type, dates, IDs, etc.)
- **Multi-turn Conversations**: Handles follow-up questions and slot-filling
- **Template-based Responses**: Provides structured responses based on extracted information
- **Knowledge Grounding**: Retrieves information from official AAU sources

## Technology Stack

- **Python 3.10+**
- **FastAPI**: Backend API framework
- **spaCy**: NLP and NER
- **HuggingFace Transformers**: Advanced NLP models
- **scikit-learn**: Machine learning models
- **Pydantic**: Data validation

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd AAU-Chatbot
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Project Structure

```
AAU-Chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── chatbot.py           # Main chatbot class
│   ├── dialogue_manager.py  # Conversation state management
│   ├── response_generator.py # Response generation
│   ├── data_processor.py    # Data cleaning utilities
│   ├── evaluation.py        # Evaluation metrics
│   └── models/              # NLP models
│       ├── intent_classifier.py
│       ├── parameter_extractor.py
│       ├── spacy_ner.py
│       └── transformer_intent.py
├── config/                  # Configuration files
│   └── intent.yaml          # Intent definitions
├── data/
│   ├── raw/                 # Raw collected data
│   ├── processed/           # Cleaned data
│   ├── annotated/           # Labeled training data
│   └── knowledge_base/      # Knowledge base entries
├── models/                  # Trained model files
├── scripts/                 # Utility scripts
│   ├── web_scrapper.py
│   ├── telegram_cli.py
│   └── train_baseline.py
├── tests/                   # Unit tests
├── reports/                 # Evaluation reports
├── docs/                    # Documentation
├── requirements.txt
├── .env.example
└── README.md
```

## Running the Application

### Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload

# Or using Python
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

### Health Check

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health check with model status

### Chat (To be implemented)
- `POST /chat` - Chat endpoint for user interactions

## Development Status

This project is currently in **Milestone 0** (Environment & Repository Setup).

See [MILESTONES.md](MILESTONES.md) for detailed progress tracking.

## Contributing

1. Follow the milestone structure outlined in `MILESTONES.md`
2. Ensure code follows PEP 8 style guidelines
3. Write tests for new features
4. Update documentation as needed

## License

[Add your license here]

## Contact

[Add contact information here]

## Acknowledgments

Built for Addis Ababa University helpdesk services.
