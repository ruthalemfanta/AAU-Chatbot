"""
NLP Engine for AAU Helpdesk Chatbot
Handles intent recognition and parameter extraction with precision metrics
"""

import spacy
import re
from typing import Dict, List, Tuple, Optional, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import json
from datetime import datetime

class IntentClassifier:
    """Intent classification using scikit-learn pipeline"""
    
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.intent_labels = [
            'admission_inquiry',
            'registration_help',
            'fee_payment',
            'transcript_request',
            'grade_inquiry',
            'course_information',
            'schedule_inquiry',
            'document_request',
            'general_info',
            'technical_support'
        ]
        self.is_trained = False
    
    def train(self, texts: List[str], labels: List[str]):
        """Train the intent classifier"""
        self.pipeline.fit(texts, labels)
        self.is_trained = True
    
    def predict(self, text: str) -> Tuple[str, float]:
        """Predict intent with confidence score"""
        if not self.is_trained:
            return 'general_info', 0.5
        
        prediction = self.pipeline.predict([text])[0]
        probabilities = self.pipeline.predict_proba([text])[0]
        confidence = max(probabilities)
        
        return prediction, confidence

class ParameterExtractor:
    """Extract parameters using NER and rule-based methods"""
    
    def __init__(self):
        # Load spaCy model (you'll need to download: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # AAU-specific patterns
        self.department_patterns = [
            r'\b(computer science|cs|engineering|medicine|law|business|economics|psychology|biology|chemistry|physics|mathematics|english|amharic)\b',
            r'\b(school of|faculty of|department of|college of)\s+([a-zA-Z\s]+)',
        ]
        
        self.document_patterns = [
            r'\b(transcript|certificate|diploma|degree|grade report|academic record|student id|recommendation letter)\b',
        ]
        
        self.semester_patterns = [
            r'\b(semester|sem)\s*(\d+)',
            r'\b(first|second|third|1st|2nd|3rd)\s+(semester|sem)',
            r'\b(fall|spring|summer)\s+(semester|term)',
        ]
        
        self.year_patterns = [
            r'\b(20\d{2})\b',
            r'\b(year|yr)\s*(\d+)',
            r'\b(\d{4})\s*(academic year|ay)',
        ]
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        entities = {
            'PERSON': [],
            'ORG': [],
            'DATE': [],
            'MONEY': [],
            'GPE': []  # Geopolitical entities
        }
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_].append(ent.text)
        
        return entities
    
    def extract_parameters(self, text: str, intent: str) -> Dict[str, Any]:
        """Extract intent-specific parameters"""
        text_lower = text.lower()
        parameters = {}
        
        # Extract departments
        departments = []
        for pattern in self.department_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    departments.extend([match[1].strip() for match in matches])
                else:
                    departments.extend(matches)
        
        if departments:
            parameters['department'] = list(set(departments))
        
        # Extract document types
        documents = []
        for pattern in self.document_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            documents.extend(matches)
        
        if documents:
            parameters['document_type'] = list(set(documents))
        
        # Extract semester information
        semesters = []
        for pattern in self.semester_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    semesters.extend([' '.join(match) for match in matches])
                else:
                    semesters.extend(matches)
        
        if semesters:
            parameters['semester'] = list(set(semesters))
        
        # Extract years
        years = []
        for pattern in self.year_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    years.extend([match[1] if match[1] else match[0] for match in matches])
                else:
                    years.extend(matches)
        
        if years:
            parameters['year'] = list(set(years))
        
        # Extract named entities
        entities = self.extract_entities(text)
        if entities['PERSON']:
            parameters['person'] = entities['PERSON']
        if entities['DATE']:
            parameters['date'] = entities['DATE']
        if entities['MONEY']:
            parameters['amount'] = entities['MONEY']
        
        # Intent-specific parameter extraction
        if intent == 'fee_payment':
            # Look for fee amounts and payment methods
            fee_pattern = r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(birr|etb|usd|\$)?\b'
            fee_matches = re.findall(fee_pattern, text_lower)
            if fee_matches:
                parameters['fee_amount'] = [match[0] for match in fee_matches]
        
        elif intent == 'transcript_request':
            # Look for student ID patterns
            student_id_pattern = r'\b(student\s*id|id\s*number|student\s*number)[\s:]*([a-zA-Z0-9/-]+)\b'
            id_matches = re.findall(student_id_pattern, text_lower)
            if id_matches:
                parameters['student_id'] = [match[1] for match in id_matches]
        
        return parameters

class AAUNLPEngine:
    """Main NLP engine combining intent classification and parameter extraction"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.confidence_threshold = 0.3  # Lower threshold for better responsiveness
    
    def process_query(self, text: str) -> Dict[str, Any]:
        """Process user query and return intent, parameters, and confidence"""
        # Clean and preprocess text
        cleaned_text = self._preprocess_text(text)
        
        # Classify intent
        intent, confidence = self.intent_classifier.predict(cleaned_text)
        
        # Extract parameters
        parameters = self.parameter_extractor.extract_parameters(cleaned_text, intent)
        
        # Determine if we have enough information
        required_params = self._get_required_parameters(intent)
        missing_params = [param for param in required_params if param not in parameters]
        
        return {
            'intent': intent,
            'confidence': confidence,
            'parameters': parameters,
            'missing_parameters': missing_params,
            'needs_clarification': len(missing_params) > 0 or confidence < self.confidence_threshold,
            'processed_text': cleaned_text
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess input text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Expand common abbreviations
        abbreviations = {
            'aau': 'addis ababa university',
            'cs': 'computer science',
            'eng': 'engineering',
            'med': 'medicine',
            'biz': 'business',
            'econ': 'economics'
        }
        
        for abbr, full in abbreviations.items():
            text = re.sub(r'\b' + abbr + r'\b', full, text, flags=re.IGNORECASE)
        
        return text
    
    def _get_required_parameters(self, intent: str) -> List[str]:
        """Get required parameters for each intent"""
        required_params = {
            'admission_inquiry': ['department'],
            'registration_help': ['semester', 'year'],
            'fee_payment': ['fee_amount'],
            'transcript_request': ['document_type'],
            'grade_inquiry': ['semester', 'year'],
            'course_information': ['department'],
            'schedule_inquiry': ['semester', 'year'],
            'document_request': ['document_type'],
            'general_info': [],
            'technical_support': []
        }
        
        return required_params.get(intent, [])
    
    def train_intent_classifier(self, training_data: List[Dict[str, str]]):
        """Train the intent classifier with labeled data"""
        texts = [item['text'] for item in training_data]
        labels = [item['intent'] for item in training_data]
        
        self.intent_classifier.train(texts, labels)
    
    def evaluate_parameters(self, test_data: List[Dict], parameter_name: str) -> Dict[str, float]:
        """Evaluate parameter extraction precision, recall, and F1-score"""
        y_true = []
        y_pred = []
        
        for item in test_data:
            true_params = item.get('parameters', {}).get(parameter_name, [])
            result = self.process_query(item['text'])
            pred_params = result['parameters'].get(parameter_name, [])
            
            # Convert to binary classification for each possible value
            y_true.append(1 if true_params else 0)
            y_pred.append(1 if pred_params else 0)
        
        if not y_true or not y_pred:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        
        precision = precision_score(y_true, y_pred, average='binary', zero_division=0)
        recall = recall_score(y_true, y_pred, average='binary', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='binary', zero_division=0)
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }