#!/usr/bin/env python3
"""
Setup script for AAU Helpdesk Chatbot
Automates installation and initial setup
"""

import subprocess
import sys
import os
from pathlib import Path
import json

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install main dependencies
    result = run_command("pip install -r requirements.txt", "Installing Python packages")
    if result is None:
        print("❌ Failed to install dependencies")
        return False
    
    # Download spaCy model
    result = run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model")
    if result is None:
        print("⚠️  spaCy model download failed - NER features may be limited")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "models/saved",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")

def generate_sample_data():
    """Generate initial training data"""
    print("\n📊 Generating sample training data...")
    
    try:
        # Import and run data generation
        sys.path.append('scripts')
        from web_scrapper import AAUWebScraper
        
        scraper = AAUWebScraper()
        synthetic_data = scraper.generate_synthetic_data()
        
        # Save sample data
        output_path = Path('data/raw/initial_training_data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(synthetic_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {len(synthetic_data)} training samples")
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate sample data: {e}")
        return False

def create_config_file():
    """Create default configuration file"""
    print("\n⚙️  Creating configuration file...")
    
    config = {
        "confidence_threshold": 0.6,
        "max_follow_up_questions": 2,
        "log_conversations": True,
        "model_settings": {
            "max_features": 1000,
            "use_spacy": True,
            "spacy_model": "en_core_web_sm"
        },
        "response_settings": {
            "use_random_templates": True,
            "include_emojis": True
        },
        "server_settings": {
            "host": "0.0.0.0",
            "port": 8000,
            "reload": True
        }
    }
    
    config_path = Path('config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to {config_path}")

def run_tests():
    """Run basic tests to verify installation"""
    print("\n🧪 Running basic tests...")
    
    # Test imports
    try:
        sys.path.append('app')
        from nlp_engine import AAUNLPEngine
        from templates import ResponseTemplates
        from utils import DataLoader
        
        print("✅ Core modules import successfully")
        
        # Test basic functionality
        engine = AAUNLPEngine()
        templates = ResponseTemplates()
        data = DataLoader.get_sample_training_data()
        
        if data:
            engine.train_intent_classifier(data)
            result = engine.process_query("Hello, I need help with admission")
            response = templates.generate_response(
                result['intent'], result['parameters'], 
                result['missing_parameters'], result['confidence']
            )
            
            if response:
                print("✅ Basic functionality test passed")
                return True
        
        print("❌ Basic functionality test failed")
        return False
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def show_next_steps():
    """Show next steps after installation"""
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start the chatbot server:")
    print("   python app/main.py")
    print("\n2. Or use uvicorn:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n3. Test the API:")
    print('   curl -X POST "http://localhost:8000/chat" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"message": "I want to apply for computer science"}\'')
    print("\n4. Access API documentation:")
    print("   http://localhost:8000/docs")
    print("\n5. Run comprehensive tests:")
    print("   python -m pytest tests/test.py -v")
    print("\n6. Collect more training data:")
    print("   python scripts/web_scrapper.py")
    print("   python scripts/telegram_cli.py --collect")
    print("\n📚 Documentation: README.md")
    print("🐛 Issues: Create an issue on GitHub")

def main():
    """Main setup function"""
    print("🤖 AAU Helpdesk Chatbot - Setup Script")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Generate sample data
    generate_sample_data()
    
    # Create config file
    create_config_file()
    
    # Run tests
    if not run_tests():
        print("⚠️  Setup completed but tests failed - check installation")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()