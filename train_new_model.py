#!/usr/bin/env python3
"""
Train the AAU chatbot with new granular intents
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from utils import DataLoader
from nlp_engine import AAUNLPEngine
from templates import ResponseTemplates
import json

def train_and_test_model():
    """Train the model with new data and test it"""
    print("🚀 Training AAU Chatbot with New Intents\n")
    print("=" * 60)
    
    # Load training data
    training_data = DataLoader.get_sample_training_data()
    print(f"📊 Training samples: {len(training_data)}")
    
    # Initialize NLP engine
    nlp_engine = AAUNLPEngine()
    templates = ResponseTemplates()
    
    # Train the model
    print("🔧 Training intent classifier...")
    nlp_engine.train_intent_classifier(training_data)
    print("✅ Training completed!")
    
    # Test with specific queries for each new intent
    test_cases = [
        # Undergraduate admission
        ("I want to apply for undergraduate computer science", "undergraduate_admission"),
        ("What are undergraduate admission requirements?", "undergraduate_admission"),
        
        # Graduate admission  
        ("How do I apply for Masters in engineering?", "graduate_admission"),
        ("What are PhD admission requirements?", "graduate_admission"),
        
        # GAT exam
        ("When is the GAT exam?", "gat_exam_inquiry"),
        ("Where is my GAT exam venue?", "gat_exam_inquiry"),
        
        # Fees
        ("How much are undergraduate fees for medicine?", "undergraduate_fee_inquiry"),
        ("What are graduate program costs?", "graduate_fee_inquiry"),
        
        # Documents
        ("I need an official transcript", "official_transcript_request"),
        ("How do I get my degree certificate?", "certificate_request"),
        
        # Campus and services
        ("Where is the main campus?", "campus_location_inquiry"),
        ("What library services are available?", "library_services_inquiry"),
        
        # Out of domain
        ("What's the weather today?", "out_of_domain"),
        ("Can you help me cook food?", "out_of_domain"),
        ("What's the capital of France?", "out_of_domain"),
    ]
    
    print(f"\n🧪 Testing Trained Model:")
    print("-" * 40)
    
    correct_predictions = 0
    total_predictions = len(test_cases)
    
    for query, expected_intent in test_cases:
        try:
            result = nlp_engine.process_query(query)
            predicted_intent = result['intent']
            confidence = result['confidence']
            
            is_correct = predicted_intent == expected_intent
            if is_correct:
                correct_predictions += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"\n{status} Query: {query}")
            print(f"   Expected: {expected_intent}")
            print(f"   Predicted: {predicted_intent} (confidence: {confidence:.3f})")
            
            # Generate response
            response = templates.generate_response(
                intent=result['intent'],
                parameters=result['parameters'],
                missing_parameters=result['missing_parameters'],
                confidence=result['confidence']
            )
            print(f"   Response: {response[:80]}...")
            
        except Exception as e:
            print(f"❌ Error processing '{query}': {e}")
    
    accuracy = correct_predictions / total_predictions * 100
    print(f"\n📊 Model Performance:")
    print(f"   Correct predictions: {correct_predictions}/{total_predictions}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 70:
        print("🎉 Good model performance!")
    elif accuracy >= 50:
        print("⚠️  Moderate model performance - may need more training data")
    else:
        print("🔴 Poor model performance - needs more training data")
    
    print(f"\n" + "=" * 60)
    print("✅ Training and testing completed!")

if __name__ == "__main__":
    train_and_test_model()