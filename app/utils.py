"""
Utility functions for AAU Helpdesk Chatbot
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aau_chatbot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DataLoader:
    """Load and manage training/test data"""
    
    @staticmethod
    def load_training_data(file_path: str) -> List[Dict[str, Any]]:
        """Load training data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} training samples from {file_path}")
            return data
        except FileNotFoundError:
            logger.warning(f"Training data file not found: {file_path}")
            return DataLoader.get_sample_training_data()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            return []
    
    @staticmethod
    def get_sample_training_data() -> List[Dict[str, Any]]:
        """Generate sample training data for AAU helpdesk"""
        # Try to load all available training data sources
        all_data = []
        
        # Load quality Q&A training data FIRST (highest priority)
        try:
            with open('data/raw/quality_training_data.json', 'r', encoding='utf-8') as f:
                quality_data = json.load(f)
                all_data.extend(quality_data)
                logger.info(f"Loaded {len(quality_data)} samples from quality Q&A data")
        except FileNotFoundError:
            logger.info("No quality training data found")
        
        # Load enhanced training data
        try:
            with open('data/raw/enhanced_training_data.json', 'r', encoding='utf-8') as f:
                enhanced_data = json.load(f)
                # Filter out low-quality entries (hashtags, very short text, etc.)
                filtered_enhanced = [
                    item for item in enhanced_data 
                    if len(item.get('text', '')) > 20 
                    and not item.get('text', '').startswith('#')
                    and '?' in item.get('text', '') or any(word in item.get('text', '').lower() for word in ['how', 'what', 'where', 'when', 'need', 'want', 'help'])
                ]
                all_data.extend(filtered_enhanced)
                logger.info(f"Loaded {len(filtered_enhanced)} samples from enhanced data")
        except FileNotFoundError:
            logger.info("No enhanced training data found")
        
        # Load other training data sources
        try:
            with open('data/raw/aau_training_data.json', 'r', encoding='utf-8') as f:
                aau_data = json.load(f)
                all_data.extend(aau_data)
                logger.info(f"Loaded {len(aau_data)} samples from AAU data")
        except FileNotFoundError:
            logger.info("No AAU training data found")
        
        if all_data:
            logger.info(f"Total training data: {len(all_data)} samples")
            return all_data
        
        # Fallback to basic sample data
        return [
            {
                "text": "Hello, I need help with AAU services",
                "intent": "general_info",
                "parameters": {}
            },
            {
                "text": "I want to apply for computer science admission",
                "intent": "admission_inquiry",
                "parameters": {"department": ["computer science"]}
            },
            {
                "text": "How do I register for second semester 2024?",
                "intent": "registration_help",
                "parameters": {"semester": ["second"], "year": ["2024"]}
            },
            {
                "text": "I need to pay 5000 birr for tuition fees",
                "intent": "fee_payment",
                "parameters": {"fee_amount": ["5000"], "amount": ["5000 birr"]}
            },
            {
                "text": "Can I get my transcript from engineering department?",
                "intent": "transcript_request",
                "parameters": {"document_type": ["transcript"], "department": ["engineering"]}
            },
            {
                "text": "What are my grades for first semester 2023?",
                "intent": "grade_inquiry",
                "parameters": {"semester": ["first"], "year": ["2023"]}
            },
            {
                "text": "Tell me about courses in business department",
                "intent": "course_information",
                "parameters": {"department": ["business"]}
            },
            {
                "text": "When is the class schedule for fall semester 2024?",
                "intent": "schedule_inquiry",
                "parameters": {"semester": ["fall"], "year": ["2024"]}
            },
            {
                "text": "I need a degree certificate",
                "intent": "document_request",
                "parameters": {"document_type": ["degree certificate"]}
            },
            {
                "text": "I can't access my student portal",
                "intent": "technical_support",
                "parameters": {}
            }
        ]
class TextProcessor:
    """Text processing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-.,!?]', '', text)
        
        return text
    
    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """Extract numbers from text"""
        return re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', text)
    
    @staticmethod
    def normalize_department_name(department: str) -> str:
        """Normalize department names"""
        department = department.lower().strip()
        
        # Common abbreviations and variations
        mappings = {
            'cs': 'computer science',
            'cse': 'computer science',
            'comp sci': 'computer science',
            'it': 'information technology',
            'eng': 'engineering',
            'med': 'medicine',
            'biz': 'business',
            'econ': 'economics',
            'psych': 'psychology'
        }
        
        return mappings.get(department, department)

class ValidationUtils:
    """Validation utilities"""
    
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """Validate student ID format"""
        pattern = r'^[A-Z]{2,3}/\d{4}/\d{2}$|^\d{6,8}$'
        return bool(re.match(pattern, student_id.upper()))
    
    @staticmethod
    def validate_year(year: str) -> bool:
        """Validate academic year"""
        try:
            year_int = int(year)
            current_year = datetime.now().year
            return 2000 <= year_int <= current_year + 2
        except ValueError:
            return False

class ConfigManager:
    """Manage configuration settings"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "confidence_threshold": 0.6,
            "max_follow_up_questions": 2,
            "log_conversations": True,
            "model_settings": {
                "max_features": 1000,
                "use_spacy": True,
                "spacy_model": "en_core_web_sm"
            }
        }
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return {**default_config, **config}
        except FileNotFoundError:
            logger.info(f"Config file not found, using defaults")
            return default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

# Global configuration instance
config = ConfigManager()