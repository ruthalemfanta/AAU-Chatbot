"""
NLP Engine for AAU Helpdesk Chatbot
Handles intent recognition and parameter extraction with precision metrics
"""

import re
from typing import Dict, List, Tuple, Optional, Any

import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


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
    
    def extract_parameters(self, text: str, intent: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Extract intent-specific parameters"""
        text_lower = text.lower()
        parameters = {}
        
        # If this looks like a simple answer to a follow-up question, try to infer the parameter type
        if context and context.get('missing_parameters'):
            missing_params = context['missing_parameters']
            
            # Try to extract all missing parameters from the text
            extracted_params = {}
            
            # Always try to extract all parameter types from the text
            # Extract semester
            semester = self._extract_semester_from_answer(text_lower)
            if semester and 'semester' in missing_params:
                extracted_params['semester'] = [semester]
            
            # Extract year
            year = self._extract_year_from_answer(text)
            if year and 'year' in missing_params:
                extracted_params['year'] = [year]
            
            # Extract department
            dept = self._normalize_department_answer(text_lower)
            if dept and 'department' in missing_params:
                extracted_params['department'] = [dept]
            
            # Extract document type
            doc_type = self._extract_document_from_answer(text_lower)
            if doc_type and 'document_type' in missing_params:
                extracted_params['document_type'] = [doc_type]
            
            # Extract fee amount
            amount = self._extract_amount_from_answer(text)
            if amount and 'fee_amount' in missing_params:
                extracted_params['fee_amount'] = [amount]
            
            # If we extracted any parameters, return them
            if extracted_params:
                parameters.update(extracted_params)
                # If this was a follow-up, we might have gotten everything we need
                if len(extracted_params) >= len(missing_params):
                    return parameters
        
        # Regular parameter extraction (existing logic)
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
    
    def _normalize_department_answer(self, text: str) -> Optional[str]:
        """Normalize a simple department answer"""
        text = text.strip()
        
        # Common department mappings
        dept_mappings = {
            'cs': 'computer science',
            'cse': 'computer science',
            'computer science': 'computer science',
            'comp sci': 'computer science',
            'engineering': 'engineering',
            'eng': 'engineering',
            'medicine': 'medicine',
            'med': 'medicine',
            'law': 'law',
            'business': 'business',
            'biz': 'business',
            'economics': 'economics',
            'econ': 'economics',
            'psychology': 'psychology',
            'psych': 'psychology'
        }
        
        return dept_mappings.get(text)
    
    def _extract_semester_from_answer(self, text: str) -> Optional[str]:
        """Extract semester from a simple answer"""
        text = text.strip()
        
        # Look for ordinal patterns first
        ordinal_match = re.search(r'\b(1st|2nd|3rd|first|second|third)\s*semester\b', text, re.IGNORECASE)
        if ordinal_match:
            ordinal = ordinal_match.group(1).lower()
            if ordinal in ['1st', 'first']:
                return 'first'
            elif ordinal in ['2nd', 'second']:
                return 'second'
            elif ordinal in ['3rd', 'third']:
                return 'third'
        
        # Look for just the ordinal without "semester"
        semester_mappings = {
            'first': 'first',
            '1st': 'first',
            '1': 'first',
            'second': 'second',
            '2nd': 'second',
            '2': 'second',
            'third': 'third',
            '3rd': 'third',
            '3': 'third',
            'fall': 'fall',
            'spring': 'spring',
            'summer': 'summer'
        }
        
        # Check if the whole text is just a semester indicator
        if text in semester_mappings:
            return semester_mappings[text]
        
        # Look for semester words in the text
        for key, value in semester_mappings.items():
            if key in text:
                return value
        
        return None
    
    def _extract_year_from_answer(self, text: str) -> Optional[str]:
        """Extract year from a simple answer"""
        # Look for 4-digit year first
        year_match = re.search(r'\b(20\d{2})\b', text)
        if year_match:
            return year_match.group(1)
        
        # Look for ordinal year patterns like "2nd year", "3rd year"
        ordinal_match = re.search(r'\b(\d+)(?:st|nd|rd|th)?\s*year\b', text, re.IGNORECASE)
        if ordinal_match:
            year_num = int(ordinal_match.group(1))
            # Convert to actual year (assuming current academic year context)
            current_year = 2024  # You can make this dynamic
            return str(current_year - 4 + year_num)  # Rough conversion
        
        # Look for just numbers that could be years
        number_match = re.search(r'\b(\d{4})\b', text)
        if number_match:
            year = int(number_match.group(1))
            if 2020 <= year <= 2030:  # Reasonable year range
                return str(year)
        
        return None
    
    def _extract_document_from_answer(self, text: str) -> Optional[str]:
        """Extract document type from a simple answer"""
        text = text.strip()
        
        doc_mappings = {
            'transcript': 'transcript',
            'certificate': 'certificate',
            'diploma': 'diploma',
            'degree': 'degree certificate',
            'grade report': 'grade report',
            'grades': 'grade report'
        }
        
        return doc_mappings.get(text)
    
    def _extract_amount_from_answer(self, text: str) -> Optional[str]:
        """Extract fee amount from a simple answer"""
        # Look for numbers
        amount_match = re.search(r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\b', text)
        if amount_match:
            return amount_match.group(1)
        return None

class AAUNLPEngine:
    """Main NLP engine combining intent classification and parameter extraction"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.confidence_threshold = 0.3  # Lower threshold for better responsiveness
    
    def process_query(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process user query and return intent, parameters, and confidence"""
        # Clean and preprocess text
        cleaned_text = self._preprocess_text(text)
        
        # Check if this is a follow-up response to a previous question
        if context and context.get('missing_parameters') and len(cleaned_text.split()) <= 5:
            # This looks like a follow-up answer, use the previous intent
            intent = context.get('last_intent', 'general_info')
            confidence = 0.8  # High confidence for follow-up responses
            
            # Extract parameters with context
            parameters = self.parameter_extractor.extract_parameters(cleaned_text, intent, context)
            
            # Merge with previous parameters
            if context.get('all_parameters'):
                merged_parameters = context['all_parameters'].copy()
                merged_parameters.update(parameters)
                parameters = merged_parameters
        else:
            # Regular processing for new queries
            intent, confidence = self.intent_classifier.predict(cleaned_text)
            parameters = self.parameter_extractor.extract_parameters(cleaned_text, intent, context)
            
            # Merge with context parameters if available
            if context and context.get('all_parameters'):
                merged_parameters = context['all_parameters'].copy()
                for key, value in parameters.items():
                    if value:  # Only update if new parameter has a value
                        merged_parameters[key] = value
                parameters = merged_parameters
        
        # Determine if we have enough information
        required_params = self._get_required_parameters(intent)
        missing_params = [param for param in required_params if param not in parameters or not parameters[param]]
        
        return {
            'intent': intent,
            'confidence': confidence,
            'parameters': parameters,
            'missing_parameters': missing_params,
            'needs_clarification': len(missing_params) > 0 or confidence < self.confidence_threshold,
            'processed_text': cleaned_text,
            'context_used': context is not None
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