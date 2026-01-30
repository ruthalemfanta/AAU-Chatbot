#!/usr/bin/env python3
"""
Test script for the new training data with granular intents
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from utils import DataLoader
from nlp_engine import AAUNLPEngine
from templates import ResponseTemplates
import json

def test_training_data():
    """Test the new training data"""
    print("🧪 Testing New AAU Training Data\n")
    print("=" * 60)
    
    # Load training data
    training_data = DataLoader.get_sample_training_data()
    print(f"📊 Total training samples loaded: {len(training_data)}")
    
    # Count intents
    intent_counts = {}
    for item in training_data:
        intent = item.get('intent', 'unknown')
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
    
    print(f"📋 Unique intents found: {len(intent_counts)}")
    print("\n🎯 Intent Distribution:")
    for intent, count in sorted(intent_counts.items()):
        print(f"  • {intent}: {count} samples")
    
    # Test NLP engine with new intents
    print(f"\n🔧 Testing NLP Engine...")
    nlp_engine = AAUNLPEngine()
    templates = ResponseTemplates()
    
    # Test some sample queries
    test_queries = [
        "I want to apply for undergraduate computer science",
        "What are the GAT exam dates?", 
        "How much are graduate fees for engineering?",
        "I need an official transcript",
        "Where is the main campus?",
        "What's the weather like today?",  # out of domain
        "Can you help me cook injera?"     # out of domain
    ]
    
    print(f"\n🧪 Testing Sample Queries:")
    print("-" * 40)
    
    for query in test_queries:
        try:
            result = nlp_engine.process_query(query)
            response = templates.generate_response(
                intent=result['intent'],
                parameters=result['parameters'],
                missing_parameters=result['missing_parameters'],
                confidence=result['confidence']
            )
            
            print(f"\n📝 Query: {query}")
            print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
            print(f"📄 Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error processing '{query}': {e}")
    
    print(f"\n" + "=" * 60)
    print("✅ Training data testing completed!")

def analyze_new_intents():
    """Analyze the new intents training data specifically"""
    print("\n🔍 Analyzing New Intents Training Data")
    print("=" * 60)
    
    try:
        with open('data/raw/new_intents_training_data.json', 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        
        print(f"📊 New training data samples: {len(new_data)}")
        
        # Count new intents
        new_intent_counts = {}
        for item in new_data:
            intent = item.get('intent', 'unknown')
            new_intent_counts[intent] = new_intent_counts.get(intent, 0) + 1
        
        print(f"📋 New intents: {len(new_intent_counts)}")
        print("\n🎯 New Intent Distribution:")
        for intent, count in sorted(new_intent_counts.items()):
            print(f"  • {intent}: {count} samples")
        
        # Check for out_of_domain samples
        out_of_domain_samples = [item for item in new_data if item.get('intent') == 'out_of_domain']
        print(f"\n🚫 Out-of-domain samples: {len(out_of_domain_samples)}")
        
        if out_of_domain_samples:
            print("📝 Sample out-of-domain queries:")
            for i, sample in enumerate(out_of_domain_samples[:5], 1):
                print(f"  {i}. {sample['text']}")
        
    except FileNotFoundError:
        print("❌ New intents training data file not found!")
    except Exception as e:
        print(f"❌ Error analyzing new intents data: {e}")

if __name__ == "__main__":
    test_training_data()
    analyze_new_intents()