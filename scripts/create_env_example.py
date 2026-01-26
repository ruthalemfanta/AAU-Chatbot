"""Script to create .env.example file."""
import os
from pathlib import Path

env_content = """# AAU Helpdesk Chatbot Environment Variables

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Model Paths (will be set when models are trained)
# INTENT_MODEL_PATH=models/baseline_intent_model.pkl
# NER_MODEL_PATH=models/spacy_ner_model
# VECTORIZER_PATH=models/tfidf_vectorizer.pkl

# Data Paths
DATA_DIR=data
RAW_DATA_PATH=data/raw/collected_data.csv
PROCESSED_DATA_PATH=data/processed/cleaned_data.csv
ANNOTATED_DATA_DIR=data/annotated
KNOWLEDGE_BASE_DIR=data/knowledge_base

# Config Paths
CONFIG_DIR=config
INTENT_CONFIG_PATH=config/intent.yaml

# Logging
LOG_LEVEL=INFO

# Optional: Telegram API (for data collection)
# TELEGRAM_API_TOKEN=your_telegram_token_here
# TELEGRAM_CHANNEL_ID=your_channel_id_here
"""

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env.example"
    
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print(f"Created .env.example at {env_file}")
