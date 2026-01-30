#!/usr/bin/env python3
"""
Test script for the new AAU chatbot templates
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from templates import ResponseTemplates
from nlp_engine import AAUNLPEngine

def test_new_intents():
    """Test the new granular intents"""
    templates = ResponseTemplates()
    nlp_engine = AAUNLPEngine()
    
    # Test cases for new intents
    test_cases = [
        {
            'intent': 'undergraduate_admission',
            'parameters': {'department': ['computer science']},
            'missing_parameters': [],
            'confidence': 0.9
        },
        {
            'intent': 'gat_exam_inquiry',
            'parameters': {},
            'missing_parameters': [],
            'confidence': 0.8
        },
        {
            'intent': 'undergraduate_fee_inquiry',
            'parameters': {'department': ['medicine']},
            'missing_parameters': [],
            'confidence': 0.85
        },
        {
            'intent': 'official_transcript_request',
            'parameters': {'document_type': ['transcript']},
            'missing_parameters': [],
            'confidence': 0.9
        },
        {
            'intent': 'library_services_inquiry',
            'parameters': {},
            'missing_parameters': [],
            'confidence': 0.8
        },
        {
            'intent': 'campus_location_inquiry',
            'parameters': {},
            'missing_parameters': [],
            'confidence': 0.85
        }
    ]
    
    print("🧪 Testing New AAU Chatbot Templates\n")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['intent']}")
        print("-" * 40)
        
        try:
            response = templates.generate_response(
                intent=test_case['intent'],
                parameters=test_case['parameters'],
                missing_parameters=test_case['missing_parameters'],
                confidence=test_case['confidence']
            )
            
            print("✅ Response generated successfully!")
            print(f"📝 Response preview: {response[:200]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing intent labels in NLP engine...")
    
    print(f"📊 Total intents supported: {len(nlp_engine.intent_classifier.intent_labels)}")
    print("📋 New intents added:")
    
    new_intents = [
        'undergraduate_admission', 'graduate_admission', 'gat_exam_inquiry',
        'undergraduate_fee_inquiry', 'official_transcript_request', 
        'library_services_inquiry', 'campus_location_inquiry'
    ]
    
    for intent in new_intents:
        if intent in nlp_engine.intent_classifier.intent_labels:
            print(f"  ✅ {intent}")
        else:
            print(f"  ❌ {intent} - Missing!")
    
    print("\n🎉 Template testing completed!")

if __name__ == "__main__":
    test_new_intents()