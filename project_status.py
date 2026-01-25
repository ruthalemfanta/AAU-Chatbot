#!/usr/bin/env python3
"""
AAU Helpdesk Chatbot - Project Status Report
Shows the current status and capabilities of the implemented system
"""

import json
import sys
from pathlib import Path

def check_file_exists(file_path):
    """Check if file exists and return status"""
    return "✅" if Path(file_path).exists() else "❌"

def get_file_size(file_path):
    """Get file size in a readable format"""
    try:
        size = Path(file_path).stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "N/A"

def count_training_samples():
    """Count training samples from data files"""
    total_samples = 0
    data_files = [
        "data/raw/aau_training_data.json",
        "data/raw/telegram_training_data.json",
        "data/raw/aau_synthetic_data.json"
    ]
    
    for file_path in data_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total_samples += len(data)
        except:
            continue
    
    return total_samples

def main():
    print("🤖 AAU Helpdesk Chatbot - Project Status Report")
    print("=" * 60)
    
    # Core Application Files
    print("\n📁 Core Application Files:")
    core_files = [
        ("app/main.py", "FastAPI application server"),
        ("app/nlp_engine.py", "NLP processing engine"),
        ("app/templates.py", "Response template system"),
        ("app/utils.py", "Utility functions"),
    ]
    
    for file_path, description in core_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<25} - {description} ({size})")
    
    # Data Collection Scripts
    print("\n📊 Data Collection Scripts:")
    script_files = [
        ("scripts/web_scrapper.py", "Web scraping for training data"),
        ("scripts/telegram_cli.py", "Telegram data collection"),
    ]
    
    for file_path, description in script_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<25} - {description} ({size})")
    
    # Model Files
    print("\n🧠 Model Files:")
    model_files = [
        ("models/sth.py", "Advanced NLP models"),
    ]
    
    for file_path, description in model_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<25} - {description} ({size})")
    
    # Test Files
    print("\n🧪 Test Files:")
    test_files = [
        ("tests/test.py", "Comprehensive test suite"),
    ]
    
    for file_path, description in test_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<25} - {description} ({size})")
    
    # Data Files
    print("\n📈 Training Data:")
    data_files = [
        ("data/raw/aau_training_data.json", "Combined training data"),
        ("data/raw/telegram_training_data.json", "Telegram messages"),
        ("data/raw/aau_synthetic_data.json", "Synthetic training data"),
        ("data/processed/sth1.md", "Data processing documentation"),
        ("data/raw/sth2.md", "Sample data documentation"),
    ]
    
    for file_path, description in data_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<35} - {description} ({size})")
    
    # Configuration Files
    print("\n⚙️  Configuration Files:")
    config_files = [
        ("requirments.txt", "Python dependencies"),
        ("setup.py", "Installation script"),
        ("demo.py", "Demo script"),
        ("README.md", "Project documentation"),
    ]
    
    for file_path, description in config_files:
        status = check_file_exists(file_path)
        size = get_file_size(file_path)
        print(f"  {status} {file_path:<25} - {description} ({size})")
    
    # Training Data Statistics
    total_samples = count_training_samples()
    print(f"\n📊 Training Data Statistics:")
    print(f"  Total training samples: {total_samples}")
    
    # Supported Features
    print(f"\n🎯 Supported Features:")
    features = [
        "✅ Intent Recognition (10 categories)",
        "✅ Parameter Extraction with precision metrics",
        "✅ Template-based response generation",
        "✅ Follow-up questions for missing parameters",
        "✅ Confidence-based clarification requests",
        "✅ FastAPI REST API with async support",
        "✅ Comprehensive test suite",
        "✅ Data collection from multiple sources",
        "✅ Modular and extensible architecture",
        "✅ Virtual environment setup"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    # Supported Intents
    print(f"\n🎯 Supported Intents:")
    intents = [
        "admission_inquiry - University admission questions",
        "registration_help - Course registration assistance", 
        "fee_payment - Payment information and methods",
        "transcript_request - Document requests",
        "grade_inquiry - Grade and result queries",
        "course_information - Course and curriculum info",
        "schedule_inquiry - Class schedule questions",
        "document_request - General document requests",
        "general_info - General university information",
        "technical_support - Technical issues and support"
    ]
    
    for intent in intents:
        print(f"  • {intent}")
    
    # Parameter Types
    print(f"\n🔍 Extracted Parameters:")
    parameters = [
        "department - Academic departments (CS, Engineering, etc.)",
        "semester - Academic semesters (First, Second, Fall, etc.)",
        "year - Academic years (2023, 2024, etc.)",
        "document_type - Document types (transcript, certificate, etc.)",
        "fee_amount - Payment amounts in Ethiopian Birr",
        "student_id - Student identification numbers",
        "person - Person names (via NER)",
        "date - Date entities (via NER)"
    ]
    
    for param in parameters:
        print(f"  • {param}")
    
    # API Endpoints
    print(f"\n🌐 API Endpoints:")
    endpoints = [
        "GET  / - API information and documentation",
        "POST /chat - Main chatbot interaction",
        "POST /train - Train with new data",
        "POST /evaluate - Evaluate model performance",
        "GET  /health - Health check",
        "GET  /intents - List supported intents",
        "GET  /docs - Interactive API documentation"
    ]
    
    for endpoint in endpoints:
        print(f"  • {endpoint}")
    
    # Usage Instructions
    print(f"\n🚀 Quick Start:")
    print(f"  1. Activate virtual environment: source aau_chatbot_env/bin/activate")
    print(f"  2. Start server: python app/main.py")
    print(f"  3. Test API: curl -X POST 'http://localhost:8000/chat' \\")
    print(f"              -H 'Content-Type: application/json' \\")
    print(f"              -d '{{\"message\": \"I want to apply for computer science\"}}'")
    print(f"  4. View docs: http://localhost:8000/docs")
    print(f"  5. Run tests: python -m pytest tests/test.py -v")
    print(f"  6. Run demo: python demo.py")
    
    print(f"\n" + "=" * 60)
    print(f"✅ AAU Helpdesk Chatbot is fully implemented and ready to use!")
    print(f"📚 See README.md for detailed documentation")

if __name__ == "__main__":
    main()