"""Script to validate intent.yaml file."""
import yaml
from pathlib import Path
import sys

def validate_intent_yaml():
    """Validate the intent.yaml file structure."""
    yaml_path = Path("config/intent.yaml")
    
    if not yaml_path.exists():
        print(f"✗ Error: {yaml_path} not found")
        return False
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        print("=" * 60)
        print("VALIDATING INTENT.YAML")
        print("=" * 60)
        
        # Check structure
        if 'intents' not in data:
            print("✗ Error: 'intents' key not found")
            return False
        print("✓ 'intents' key found")
        
        if 'slots' not in data:
            print("✗ Error: 'slots' key not found")
            return False
        print("✓ 'slots' key found")
        
        # Validate intents
        intents = data['intents']
        print(f"\n✓ Found {len(intents)} intents")
        
        required_fields = ['description', 'required_slots', 'optional_slots', 
                          'example_utterances', 'response_template', 'follow_up_questions']
        
        all_valid = True
        for intent_name, intent_data in intents.items():
            print(f"\n  Validating intent: {intent_name}")
            
            for field in required_fields:
                if field not in intent_data:
                    print(f"    ✗ Missing field: {field}")
                    all_valid = False
                else:
                    print(f"    ✓ {field} present")
            
            # Check example utterances count
            if 'example_utterances' in intent_data:
                count = len(intent_data['example_utterances'])
                if count < 5:
                    print(f"    ⚠ Warning: Only {count} example utterances (recommended: 5-10)")
                else:
                    print(f"    ✓ {count} example utterances")
        
        # Validate slots
        slots = data['slots']
        print(f"\n✓ Found {len(slots)} slot definitions")
        
        slot_fields = ['description', 'examples', 'extraction_hints']
        for slot_name, slot_data in slots.items():
            for field in slot_fields:
                if field not in slot_data:
                    print(f"  ⚠ Warning: Slot '{slot_name}' missing field: {field}")
        
        print("\n" + "=" * 60)
        if all_valid:
            print("✓ VALIDATION PASSED - intent.yaml is valid!")
            return True
        else:
            print("✗ VALIDATION FAILED - Please fix the errors above")
            return False
            
    except yaml.YAMLError as e:
        print(f"✗ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = validate_intent_yaml()
    sys.exit(0 if success else 1)
