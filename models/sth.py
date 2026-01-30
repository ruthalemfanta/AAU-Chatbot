"""
Advanced NLP Models for AAU Helpdesk Chatbot
Includes transformer-based models and evaluation utilities
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import json
import logging
from pathlib import Path
import pickle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransformerIntentClassifier(nn.Module):
    """Transformer-based intent classifier using pre-trained models"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased", num_intents: int = 10, dropout: float = 0.3):
        super().__init__()
        self.model_name = model_name
        self.num_intents = num_intents
        
        # Load pre-trained transformer
        self.config = AutoConfig.from_pretrained(model_name)
        self.transformer = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Classification head
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.config.hidden_size, num_intents)
        
        # Intent labels
        self.intent_labels = [
            'admission_inquiry', 'registration_help', 'fee_payment',
            'transcript_request', 'grade_inquiry', 'course_information',
            'schedule_inquiry', 'document_request', 'general_info', 'technical_support'
        ]
        self.label_to_id = {label: i for i, label in enumerate(self.intent_labels)}
        self.id_to_label = {i: label for i, label in enumerate(self.intent_labels)}
    
    def forward(self, input_ids, attention_mask):
        """Forward pass"""
        outputs = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.last_hidden_state[:, 0]  # Use [CLS] token
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits
    
    def predict(self, texts: List[str], max_length: int = 128) -> List[Tuple[str, float]]:
        """Predict intents for given texts"""
        self.eval()
        predictions = []
        
        with torch.no_grad():
            for text in texts:
                # Tokenize
                encoded = self.tokenizer(
                    text,
                    truncation=True,
                    padding='max_length',
                    max_length=max_length,
                    return_tensors='pt'
                )
                
                # Forward pass
                logits = self.forward(encoded['input_ids'], encoded['attention_mask'])
                probabilities = torch.softmax(logits, dim=-1)
                
                # Get prediction
                predicted_id = torch.argmax(probabilities, dim=-1).item()
                confidence = probabilities[0][predicted_id].item()
                predicted_label = self.id_to_label[predicted_id]
                
                predictions.append((predicted_label, confidence))
        
        return predictions

class ParameterExtractorNER:
    """Named Entity Recognition for parameter extraction"""
    
    def __init__(self, model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english"):
        try:
            from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(model_name)
            self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
        except ImportError:
            logger.warning("Transformers not available for NER. Using rule-based extraction.")
            self.ner_pipeline = None
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        entities = {
            'PERSON': [],
            'ORG': [],
            'DATE': [],
            'MONEY': [],
            'MISC': []
        }
        
        if self.ner_pipeline:
            try:
                ner_results = self.ner_pipeline(text)
                for entity in ner_results:
                    entity_type = entity['entity_group']
                    entity_text = entity['word']
                    
                    if entity_type in entities:
                        entities[entity_type].append(entity_text)
            except Exception as e:
                logger.error(f"NER extraction failed: {e}")
        
        return entities

class ModelTrainer:
    """Training utilities for AAU helpdesk models"""
    
    def __init__(self, model_save_path: str = "models/saved"):
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)
    
    def load_training_data(self, data_path: str) -> Tuple[List[str], List[str]]:
        """Load training data from JSON file"""
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            texts = [item['text'] for item in data if 'text' in item and 'intent' in item]
            labels = [item['intent'] for item in data if 'text' in item and 'intent' in item]
            
            logger.info(f"Loaded {len(texts)} training samples")
            return texts, labels
            
        except FileNotFoundError:
            logger.error(f"Training data file not found: {data_path}")
            return [], []
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return [], []
    
    def prepare_data(self, texts: List[str], labels: List[str], test_size: float = 0.2) -> Tuple:
        """Prepare data for training"""
        if not texts or not labels:
            raise ValueError("No training data available")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        logger.info(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        return X_train, X_test, y_train, y_test
    
    def train_transformer_model(self, X_train: List[str], y_train: List[str], 
                              X_test: List[str], y_test: List[str],
                              epochs: int = 3, batch_size: int = 16) -> TransformerIntentClassifier:
        """Train transformer-based intent classifier"""
        
        # Initialize model
        unique_labels = list(set(y_train + y_test))
        model = TransformerIntentClassifier(num_intents=len(unique_labels))
        
        # Update label mappings
        model.intent_labels = unique_labels
        model.label_to_id = {label: i for i, label in enumerate(unique_labels)}
        model.id_to_label = {i: label for i, label in enumerate(unique_labels)}
        
        # Convert labels to IDs
        y_train_ids = [model.label_to_id[label] for label in y_train]
        y_test_ids = [model.label_to_id[label] for label in y_test]
        
        # Training setup
        optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
        criterion = nn.CrossEntropyLoss()
        
        model.train()
        
        # Simple training loop (in production, use proper DataLoader and batching)
        for epoch in range(epochs):
            total_loss = 0
            correct_predictions = 0
            
            for i in range(0, len(X_train), batch_size):
                batch_texts = X_train[i:i+batch_size]
                batch_labels = torch.tensor(y_train_ids[i:i+batch_size])
                
                # Tokenize batch
                encoded = model.tokenizer(
                    batch_texts,
                    truncation=True,
                    padding=True,
                    max_length=128,
                    return_tensors='pt'
                )
                
                # Forward pass
                optimizer.zero_grad()
                logits = model(encoded['input_ids'], encoded['attention_mask'])
                loss = criterion(logits, batch_labels)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                
                # Calculate accuracy
                predictions = torch.argmax(logits, dim=-1)
                correct_predictions += (predictions == batch_labels).sum().item()
            
            avg_loss = total_loss / (len(X_train) // batch_size)
            accuracy = correct_predictions / len(X_train)
            
            logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")
        
        # Evaluate on test set
        test_predictions = model.predict(X_test)
        test_pred_labels = [pred[0] for pred in test_predictions]
        
        # Print evaluation metrics
        print("\nClassification Report:")
        print(classification_report(y_test, test_pred_labels))
        
        # Save model
        model_path = self.model_save_path / "transformer_intent_classifier.pt"
        torch.save({
            'model_state_dict': model.state_dict(),
            'intent_labels': model.intent_labels,
            'label_to_id': model.label_to_id,
            'id_to_label': model.id_to_label,
            'model_config': {
                'model_name': model.model_name,
                'num_intents': model.num_intents
            }
        }, model_path)
        
        logger.info(f"Model saved to {model_path}")
        return model
    
    def evaluate_parameter_extraction(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluate parameter extraction performance"""
        from app.nlp_engine import ParameterExtractor
        
        extractor = ParameterExtractor()
        results = {
            'department': {'tp': 0, 'fp': 0, 'fn': 0},
            'semester': {'tp': 0, 'fp': 0, 'fn': 0},
            'year': {'tp': 0, 'fp': 0, 'fn': 0},
            'document_type': {'tp': 0, 'fp': 0, 'fn': 0},
            'fee_amount': {'tp': 0, 'fp': 0, 'fn': 0}
        }
        
        for item in test_data:
            text = item.get('text', '')
            true_params = item.get('parameters', {})
            
            # Extract parameters
            predicted_params = extractor.extract_parameters(text, item.get('intent', 'general_info'))
            
            # Calculate metrics for each parameter type
            for param_type in results.keys():
                true_values = set(true_params.get(param_type, []))
                pred_values = set(predicted_params.get(param_type, []))
                
                tp = len(true_values & pred_values)
                fp = len(pred_values - true_values)
                fn = len(true_values - pred_values)
                
                results[param_type]['tp'] += tp
                results[param_type]['fp'] += fp
                results[param_type]['fn'] += fn
        
        # Calculate precision, recall, F1 for each parameter
        metrics = {}
        for param_type, counts in results.items():
            tp, fp, fn = counts['tp'], counts['fp'], counts['fn']
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics[param_type] = {
                'precision': precision,
                'recall': recall,
                'f1': f1
            }
        
        return metrics

def main():
    """Main training script"""
    print("🤖 AAU Helpdesk Chatbot - Model Training")
    print("=" * 50)
    
    trainer = ModelTrainer()
    
    # Load training data
    data_paths = [
        'data/raw/aau_training_data.json',
        'data/raw/telegram_training_data.json'
    ]
    
    all_texts = []
    all_labels = []
    
    for data_path in data_paths:
        if Path(data_path).exists():
            texts, labels = trainer.load_training_data(data_path)
            all_texts.extend(texts)
            all_labels.extend(labels)
    
    if not all_texts:
        print("❌ No training data found. Please run data collection first.")
        return
    
    print(f"📊 Total training samples: {len(all_texts)}")
    
    # Prepare data
    try:
        X_train, X_test, y_train, y_test = trainer.prepare_data(all_texts, all_labels)
        
        print("🚀 Starting model training...")
        
        # Train transformer model
        model = trainer.train_transformer_model(X_train, y_train, X_test, y_test)
        
        print("✅ Model training completed!")
        
        # Evaluate parameter extraction if test data available
        test_data_path = 'data/raw/test_data.json'
        if Path(test_data_path).exists():
            with open(test_data_path, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            
            param_metrics = trainer.evaluate_parameter_extraction(test_data)
            
            print("\n📈 Parameter Extraction Metrics:")
            for param, metrics in param_metrics.items():
                print(f"  {param}:")
                print(f"    Precision: {metrics['precision']:.3f}")
                print(f"    Recall: {metrics['recall']:.3f}")
                print(f"    F1-Score: {metrics['f1']:.3f}")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        logger.error(f"Training error: {e}")

if __name__ == "__main__":
    main()