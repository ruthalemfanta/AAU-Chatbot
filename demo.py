#!/usr/bin/env python3
"""
AAU Helpdesk Chatbot Demo
Demonstrates the chatbot functionality with sample queries
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent / 'app'))

from nlp_engine import AAUNLPEngine
from templates import ResponseTemplates
from utils import DataLoader

def main():
    print("🤖 AAU Helpdesk Chatbot - Demo")
    print("=" * 50)
    
    # Initialize components
    print("🔄 Initializing chatbot components...")
    engine = AAUNLPEngine()
    templates = ResponseTemplates()
    
    # Load and train with sample data
    print("📚 Loading training data...")
    training_data = DataLoader.get_sample_training_data()
    engine.train_intent_classifier(training_data)
    print(f"✅ Trained with {len(training_data)} samples")
    
    # Demo queries
    demo_queries = [
        "Hello, I need help with AAU services",
        "I want to apply for computer science admission",
        "How do I register for second semester 2024?",
        "I need to pay 5000 birr for tuition fees",
        "Can I get my transcript from engineering department?",
        "What are my grades for first semester 2023?",
        "I can't access my student portal",
        "Thank you for your help"
    ]
    
    print("\n🎯 Demo Conversations:")
    print("=" * 50)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. User: {query}")
        
        # Process query
        result = engine.process_query(query)
        
        # Generate response
        response = templates.generate_response(
            result['intent'],
            result['parameters'],
            result['missing_parameters'],
            result['confidence']
        )
        
        print(f"   Bot: {response}")
        print(f"   📊 Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        
        if result['parameters']:
            print(f"   🔍 Parameters: {result['parameters']}")
        
        if result['missing_parameters']:
            print(f"   ❓ Missing: {result['missing_parameters']}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start the API server: python app/main.py")
    print("2. Test with curl or visit http://localhost:8000/docs")
    print("3. Run comprehensive tests: python -m pytest tests/test.py -v")
    print("4. Collect more data: python scripts/web_scrapper.py")

if __name__ == "__main__":
    main()