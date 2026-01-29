#!/usr/bin/env python3
"""
Simple test script for AAU Helpdesk Chatbot with conversation context
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

import warnings
warnings.filterwarnings("ignore")

print("🤖 AAU Helpdesk Chatbot - Quick Test")
print("=" * 50)

# Test data loading
print("\n1️⃣ Testing data loading...")
from utils import DataLoader

training_data = DataLoader.get_sample_training_data()
print(f"✅ Loaded {len(training_data)} training samples")

# Show intent distribution
intent_counts = {}
for sample in training_data:
    intent = sample.get('intent', 'unknown')
    intent_counts[intent] = intent_counts.get(intent, 0) + 1

print("\n📊 Intent distribution:")
for intent, count in sorted(intent_counts.items(), key=lambda x: -x[1]):
    print(f"   {intent}: {count}")

# Interactive chat with context
print("\n" + "=" * 50)
print("2️⃣ Interactive Chat (type 'quit' to exit)")
print("=" * 50)

from nlp_engine import AAUNLPEngine
from templates import ResponseTemplates

print("🔄 Initializing NLP engine...")
engine = AAUNLPEngine()
templates = ResponseTemplates()

print("📚 Training classifier...")
engine.train_intent_classifier(training_data)
print("✅ Ready!\n")

# Conversation context to remember previous interactions
conversation_context = {
    'last_intent': None,
    'last_parameters': {},
    'waiting_for': None  # What info we're waiting for (e.g., 'semester', 'year')
}

def merge_context(new_result, context, user_text):
    """Merge new result with conversation context"""
    import re
    
    # Check if user is providing missing info (short response)
    if context['waiting_for'] and len(user_text.split()) <= 3:
        # Keep the previous intent
        if context['last_intent']:
            new_result['intent'] = context['last_intent']
            # Start with previous parameters, then add new ones
            merged_params = context['last_parameters'].copy()
            
            # Check what was provided
            text_lower = user_text.lower().strip()
            
            # Semester detection - only update if detected
            semester_detected = False
            if any(s in text_lower for s in ['1st', 'first']):
                merged_params['semester'] = ['first']
                semester_detected = True
            elif any(s in text_lower for s in ['2nd', 'second']):
                merged_params['semester'] = ['second']
                semester_detected = True
            elif any(s in text_lower for s in ['3rd', 'third']):
                merged_params['semester'] = ['third']
                semester_detected = True
            elif 'fall' in text_lower:
                merged_params['semester'] = ['fall']
                semester_detected = True
            elif 'spring' in text_lower:
                merged_params['semester'] = ['spring']
                semester_detected = True
            elif 'summer' in text_lower:
                merged_params['semester'] = ['summer']
                semester_detected = True
            
            # Year detection - only update if detected
            year_match = re.search(r'20\d{2}', text_lower)
            if year_match:
                merged_params['year'] = [year_match.group()]
            
            # Apply merged params
            new_result['parameters'] = merged_params
            
            # Recalculate missing parameters
            new_result['missing_parameters'] = [
                p for p in context.get('original_missing', [])
                if p not in new_result['parameters']
            ]
            
            # Boost confidence since we're using context
            new_result['confidence'] = max(new_result['confidence'], 0.75)
    
    return new_result

while True:
    try:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Process query
        result = engine.process_query(user_input)
        
        # Apply context for follow-up responses
        result = merge_context(result, conversation_context, user_input)
        
        # Generate response
        response = templates.generate_response(
            result['intent'],
            result['parameters'],
            result['missing_parameters'],
            result['confidence']
        )
        
        # Update context
        conversation_context['last_intent'] = result['intent']
        conversation_context['last_parameters'] = result['parameters']
        conversation_context['original_missing'] = result.get('missing_parameters', [])
        
        # Check what we're waiting for
        if result['missing_parameters']:
            conversation_context['waiting_for'] = result['missing_parameters'][0]
        else:
            conversation_context['waiting_for'] = None
        
        print(f"\n🤖 Bot: {response}")
        print(f"   📊 Intent: {result['intent']} ({result['confidence']:.2%} confidence)")
        
        if result['parameters']:
            print(f"   🔍 Extracted: {result['parameters']}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
