"""Comprehensive verification script for Milestone 0."""
import sys
from pathlib import Path

def check_structure():
    """Check directory structure."""
    print("=" * 60)
    print("1. VERIFYING DIRECTORY STRUCTURE")
    print("=" * 60)
    
    required_dirs = {
        "app": "Main application directory",
        "app/models": "NLP models directory",
        "config": "Configuration files directory",
        "data/raw": "Raw data directory",
        "data/processed": "Processed data directory",
        "data/annotated": "Annotated data directory",
        "data/knowledge_base": "Knowledge base directory",
        "scripts": "Utility scripts directory",
        "tests": "Test files directory",
        "docs": "Documentation directory",
        "reports": "Reports directory"
    }
    
    all_exist = True
    for dir_path, description in required_dirs.items():
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path:30s} - {description}")
        else:
            print(f"✗ {dir_path:30s} - MISSING: {description}")
            all_exist = False
    
    return all_exist

def check_files():
    """Check required files."""
    print("\n" + "=" * 60)
    print("2. VERIFYING REQUIRED FILES")
    print("=" * 60)
    
    required_files = {
        "requirements.txt": "Python dependencies",
        "README.md": "Project documentation",
        ".gitignore": "Git ignore rules",
        "app/__init__.py": "App package init",
        "app/main.py": "FastAPI application",
        "app/config.py": "Configuration management",
        "app/models/__init__.py": "Models package init",
        "app/models/intent_classifier.py": "Intent classifier stub",
        "app/models/parameter_extractor.py": "Parameter extractor stub",
        "app/dialogue_manager.py": "Dialogue manager stub",
        "app/response_generator.py": "Response generator stub",
        "app/chatbot.py": "Chatbot stub",
        "tests/test_setup.py": "Setup test script"
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {file_path:35s} - {description:30s} ({size} bytes)")
        else:
            print(f"✗ {file_path:35s} - MISSING: {description}")
            all_exist = False
    
    return all_exist

def check_imports():
    """Check Python imports."""
    print("\n" + "=" * 60)
    print("3. VERIFYING PYTHON IMPORTS")
    print("=" * 60)
    
    try:
        from app.config import settings
        print(f"✓ app.config imported - API_HOST={settings.API_HOST}, PORT={settings.API_PORT}")
    except Exception as e:
        print(f"✗ app.config import failed: {e}")
        return False
    
    try:
        from app.main import app
        print(f"✓ app.main imported - FastAPI app: {app.title}")
    except Exception as e:
        print(f"✗ app.main import failed: {e}")
        return False
    
    return True

def check_requirements():
    """Check requirements.txt content."""
    print("\n" + "=" * 60)
    print("4. VERIFYING REQUIREMENTS.TXT")
    print("=" * 60)
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("✗ requirements.txt not found")
        return False
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "spacy",
        "transformers",
        "scikit-learn",
        "pandas",
        "pydantic",
        "pydantic-settings"
    ]
    
    content = req_file.read_text()
    found_packages = []
    missing_packages = []
    
    for package in required_packages:
        if package.lower() in content.lower():
            found_packages.append(package)
            print(f"✓ {package} found in requirements.txt")
        else:
            missing_packages.append(package)
            print(f"✗ {package} NOT found in requirements.txt")
    
    return len(missing_packages) == 0

def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("MILESTONE 0 VERIFICATION REPORT")
    print("=" * 60 + "\n")
    
    results = {
        "Structure": check_structure(),
        "Files": check_files(),
        "Imports": check_imports(),
        "Requirements": check_requirements()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name:20s}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED! Milestone 0 is complete.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Create .env file: python scripts/create_env_example.py")
        print("  3. Test server: uvicorn app.main:app --reload")
        return 0
    else:
        print("\n⚠️  SOME CHECKS FAILED. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
