"""
NLP Engine for AAU Helpdesk Chatbot
Handles intent recognition and parameter extraction with precision metrics
"""

import re
from typing import Dict, List, Tuple, Optional, Any

import spacy
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder

# Import ML parameter extractor
try:
    from models.ml_parameter_extractor import MLParameterExtractor
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("ML Parameter Extractor not available, using rule-based extraction")

# Removed out-of-domain detector - using simple confidence-based fallback instead


class IntentDataset(Dataset):
    """Dataset class for DistilBERT training"""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


class IntentClassifier:
    """Intent classification using DistilBERT"""
    
    def __init__(self):
        self.model_name = 'distilbert-base-uncased'
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
        self.model = None
        self.label_encoder = LabelEncoder()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        self.intent_labels = [
            # Original intents (for backward compatibility)
            'admission_inquiry',
            'registration_help', 
            'fee_payment',
            'transcript_request',
            'grade_inquiry',
            'course_information',
            'schedule_inquiry',
            'document_request',
            'general_info',
            'technical_support',
            
            # New granular admission & application intents
            'undergraduate_admission',
            'graduate_admission',
            'gat_exam_inquiry',
            'international_admission',
            
            # New fee & payment intents
            'undergraduate_fee_inquiry',
            'graduate_fee_inquiry',
            'international_student_fees',
            'payment_methods_inquiry',
            
            # New academic & course intents
            'course_catalog_inquiry',
            'prerequisite_inquiry',
            'academic_calendar_inquiry',
            
            # New examination & grading intents
            'exam_schedule_inquiry',
            'grade_report_request',
            
            # New document & service intents
            'official_transcript_request',
            'certificate_request',
            'student_id_services',
            
            # New campus & facility intents
            'library_services_inquiry',
            'accommodation_inquiry',
            'campus_location_inquiry',
            'facility_booking_inquiry',
            
            # New research & graduate intents
            'thesis_submission_process',
            'research_opportunity_inquiry',
            
            # New administrative & support intents
            'readmission_inquiry',
            'alumni_services_inquiry',
            
            # New specialized AAU service intents
            'hospital_services_inquiry',
            'book_center_inquiry',
            'radio_station_inquiry',
            'museum_services_inquiry',
            'student_portal_inquiry',
            
        ]
        self.is_trained = False
    
    def train(self, texts: List[str], labels: List[str]):
        """Train the DistilBERT intent classifier"""
        print("🔧 Training DistilBERT intent classifier...")
        
        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)
        num_labels = len(self.label_encoder.classes_)
        
        # Initialize model
        self.model = DistilBertForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=num_labels
        ).to(self.device)
        
        # Create dataset
        dataset = IntentDataset(texts, encoded_labels, self.tokenizer)
        
        # Improved training arguments for better performance
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=5,  # More epochs
            per_device_train_batch_size=8,  # Smaller batch size for better gradients
            per_device_eval_batch_size=8,
            warmup_steps=100,  # Fewer warmup steps
            weight_decay=0.01,
            learning_rate=2e-5,  # Better learning rate for DistilBERT
            logging_steps=10,
            save_strategy='no'  # Don't save checkpoints
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset
        )
        
        # Train the model
        trainer.train()
        
        # Save the trained model and label encoder
        self.save_model()
        
        self.is_trained = True
        print("✅ DistilBERT training completed!")
    
    def save_model(self, model_dir='./trained_model'):
        """Save the trained model and label encoder"""
        import os
        import pickle
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save the model and tokenizer
        self.model.save_pretrained(model_dir)
        self.tokenizer.save_pretrained(model_dir)
        
        # Save the label encoder
        with open(f'{model_dir}/label_encoder.pkl', 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print(f"✅ Model saved to {model_dir}")
    
    def load_model(self, model_dir='./trained_model'):
        """Load a previously trained model"""
        import os
        import pickle
        
        if not os.path.exists(model_dir):
            print(f"❌ No trained model found at {model_dir}")
            return False
        
        try:
            # Load the model and tokenizer
            self.model = DistilBertForSequenceClassification.from_pretrained(model_dir).to(self.device)
            self.tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
            
            # Load the label encoder
            with open(f'{model_dir}/label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            self.is_trained = True
            print(f"✅ Model loaded from {model_dir}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def predict(self, text: str) -> Tuple[str, float]:
        """Predict intent with confidence score"""
        if not self.is_trained:
            return 'general_info', 0.5
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=128,
            return_tensors='pt'
        ).to(self.device)
        
        # Get prediction
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
            
            predicted_class_id = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class_id].item()
            
            # Decode label
            predicted_label = self.label_encoder.inverse_transform([predicted_class_id])[0]
            
        return predicted_label, confidence

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
            r'\b(veterinary medicine|pharmacy|architecture|information science|software engineering)\b',
            r'\b(social sciences|education|journalism|music|art|theatre)\b',
            r'\b(school of|faculty of|department of|college of)\s+([a-zA-Z\s]+)',
        ]
        
        self.document_patterns = [
            r'\b(transcript|certificate|diploma|degree|grade report|academic record|student id|recommendation letter)\b',
            r'\b(enrollment verification|graduation certificate|academic standing certificate)\b',
        ]
        
        self.semester_patterns = [
            r'\b(semester|sem)\s*(\d+)',
            r'\b(first|second|third|1st|2nd|3rd)\s+(semester|sem)',
            r'\b(fall|spring|summer|kiremt)\s+(semester|term)',
        ]
        
        self.year_patterns = [
            r'\b(20\d{2})\b',
            r'\b(year|yr)\s*(\d+)',
            r'\b(\d{4})\s*(academic year|ay)',
        ]
        
        self.fee_patterns = [
            r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(birr|etb|usd|\$)?\b',
            r'\b(undergraduate|graduate|masters|phd|international|foreign)\s+fee\b',
        ]
        
        self.student_type_patterns = [
            r'\b(international|foreign)\s+(student|students)\b',
            r'\b(refugee|refugees)\b',
            r'\b(igad|east\s+african)\s+(student|students|country|countries)\b',
        ]
        
        self.campus_patterns = [
            r'\b(sidist kilo|main campus|sefere selam|science campus|4 kilo|bishoftu)\b',
            r'\b(6 kilo|main|medical campus)\b',
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
        
        # Extract fee amounts and payment methods
        fees = []
        for pattern in self.fee_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    fees.extend([match[0] for match in matches if match[0]])
                else:
                    fees.extend(matches)
        
        if fees:
            parameters['fee_amount'] = list(set(fees))
        
        # Extract campus locations
        campuses = []
        for pattern in self.campus_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            campuses.extend(matches)
        
        if campuses:
            parameters['campus'] = list(set(campuses))
        
        # Extract student type (international, refugee, etc.)
        student_types = []
        for pattern in self.student_type_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    student_types.extend([match[0] for match in matches])
                else:
                    student_types.extend(matches)
        
        if student_types:
            parameters['student_type'] = list(set(student_types))
        
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
            'software engineering': 'software engineering',
            'information science': 'information science',
            'engineering': 'engineering',
            'eng': 'engineering',
            'medicine': 'medicine',
            'med': 'medicine',
            'veterinary medicine': 'veterinary medicine',
            'vet med': 'veterinary medicine',
            'pharmacy': 'pharmacy',
            'architecture': 'architecture',
            'law': 'law',
            'business': 'business',
            'biz': 'business',
            'economics': 'economics',
            'econ': 'economics',
            'psychology': 'psychology',
            'psych': 'psychology',
            'biology': 'biology',
            'bio': 'biology',
            'chemistry': 'chemistry',
            'chem': 'chemistry',
            'physics': 'physics',
            'mathematics': 'mathematics',
            'math': 'mathematics',
            'english': 'english',
            'amharic': 'amharic',
            'social sciences': 'social sciences',
            'education': 'education',
            'journalism': 'journalism',
            'music': 'music',
            'art': 'art',
            'theatre': 'theatre'
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
    
    def __init__(self, use_ml_extraction: bool = True):
        self.intent_classifier = IntentClassifier()
        
        # Choose parameter extraction method
        self.use_ml_extraction = use_ml_extraction and ML_AVAILABLE
        
        if self.use_ml_extraction:
            try:
                self.parameter_extractor = MLParameterExtractor()
                print("✅ Using ML-based parameter extraction")
            except Exception as e:
                print(f"❌ Failed to load ML extractor: {e}")
                print("🔄 Falling back to rule-based extraction")
                self.parameter_extractor = ParameterExtractor()
                self.use_ml_extraction = False
        else:
            self.parameter_extractor = ParameterExtractor()
            print("📝 Using rule-based parameter extraction")
        
        # Removed out-of-domain detector initialization
        
        # Removed confidence threshold - always use the predicted intent
        self.confidence_threshold = 0.0  # Accept all predictions
    
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
            
            # Removed out-of-domain detection - using simple confidence threshold instead
            
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
            'needs_clarification': len(missing_params) > 0,  # Only check for missing parameters
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
            # Original intents
            'admission_inquiry': ['department'],
            'registration_help': ['semester', 'year'],
            'fee_payment': ['fee_amount'],
            'transcript_request': ['document_type'],
            'grade_inquiry': ['semester', 'year'],
            'course_information': ['department'],
            'schedule_inquiry': ['semester', 'year'],
            'document_request': ['document_type'],
            'general_info': [],
            'technical_support': [],
            
            # New granular intents
            'undergraduate_admission': ['department'],
            'graduate_admission': ['department'],
            'gat_exam_inquiry': [],
            'international_admission': [],
            
            'undergraduate_fee_inquiry': ['department'],
            'graduate_fee_inquiry': ['department'],
            'international_student_fees': [],
            'payment_methods_inquiry': [],
            
            'course_catalog_inquiry': ['department'],
            'prerequisite_inquiry': ['department'],
            'academic_calendar_inquiry': ['year'],
            
            'exam_schedule_inquiry': ['semester', 'year'],
            'grade_report_request': [],
            
            'official_transcript_request': ['document_type'],
            'certificate_request': ['document_type'],
            'student_id_services': [],
            
            'library_services_inquiry': [],
            'accommodation_inquiry': [],
            'campus_location_inquiry': [],
            'facility_booking_inquiry': [],
            
            'thesis_submission_process': [],
            'research_opportunity_inquiry': [],
            
            'readmission_inquiry': [],
            'alumni_services_inquiry': [],
            
            'hospital_services_inquiry': [],
            'book_center_inquiry': [],
            'radio_station_inquiry': [],
            'museum_services_inquiry': [],
            'student_portal_inquiry': [],
        }
        
        return required_params.get(intent, [])
    
    def train_intent_classifier(self, training_data: List[Dict[str, str]]):
        """Train the intent classifier with labeled data"""
        # Try to load existing model first
        if self.intent_classifier.load_model():
            print("🔄 Using previously trained DistilBERT model")
            return
        
        # If no existing model, train from scratch
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