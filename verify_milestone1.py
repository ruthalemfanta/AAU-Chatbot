"""Quick verification script for Milestone 1."""
import yaml
from pathlib import Path
import sys

def verify_milestone1():
    """Verify Milestone 1 deliverables."""
    print("=" * 60)
    print("MILESTONE 1 VERIFICATION")
    print("=" * 60)
    
    # Check intent.yaml
    yaml_path = Path("config/intent.yaml")
    if not yaml_path.exists():
        print("✗ config/intent.yaml not found")
        return False
    print("✓ config/intent.yaml exists")
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Check intents
        if 'intents' not in data:
            print("✗ 'intents' key missing")
            return False
        
        intents = data['intents']
        intent_count = len(intents)
        print(f"✓ Found {intent_count} intents")
        
        if intent_count < 10:
            print(f"  ⚠ Warning: Only {intent_count} intents (target: 10-15)")
        elif intent_count > 15:
            print(f"  ⚠ Warning: {intent_count} intents (target: 10-15)")
        else:
            print(f"  ✓ Intent count within target range (10-15)")
        
        # Check required fields for each intent
        required_fields = ['description', 'required_slots', 'optional_slots', 
                          'example_utterances', 'response_template', 'follow_up_questions']
        
        all_valid = True
        for intent_name, intent_data in intents.items():
            for field in required_fields:
                if field not in intent_data:
                    print(f"  ✗ Intent '{intent_name}' missing field: {field}")
                    all_valid = False
            
            # Check example utterances
            if 'example_utterances' in intent_data:
                count = len(intent_data['example_utterances'])
                if count < 5:
                    print(f"  ⚠ Intent '{intent_name}': Only {count} examples (recommended: 5-10)")
        
        # Check slots
        if 'slots' not in data:
            print("✗ 'slots' key missing")
            return False
        
        slots = data['slots']
        slot_count = len(slots)
        print(f"✓ Found {slot_count} slot definitions")
        
        # Check schemas.py
        schemas_path = Path("app/schemas.py")
        if not schemas_path.exists():
            print("✗ app/schemas.py not found")
            return False
        print("✓ app/schemas.py exists")
        
        # Check for required classes in schemas
        schemas_content = schemas_path.read_text()
        required_classes = ['IntentRequest', 'IntentResponse', 'Slot', 'ConversationState']
        for class_name in required_classes:
            if f"class {class_name}" in schemas_content:
                print(f"✓ {class_name} class found in schemas.py")
            else:
                print(f"✗ {class_name} class missing in schemas.py")
                all_valid = False
        
        print("\n" + "=" * 60)
        if all_valid:
            print("✓ MILESTONE 1 VERIFICATION PASSED!")
            print(f"\nSummary:")
            print(f"  - {intent_count} intents defined")
            print(f"  - {slot_count} slots defined")
            print(f"  - All required Pydantic models present")
            return True
        else:
            print("✗ MILESTONE 1 VERIFICATION FAILED")
            return False
            
    except yaml.YAMLError as e:
        print(f"✗ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_milestone1()
    sys.exit(0 if success else 1)
