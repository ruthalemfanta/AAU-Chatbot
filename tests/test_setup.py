"""Test script to verify Milestone 0 setup."""
import sys
from pathlib import Path

def test_imports():
    """Test that all main modules can be imported."""
    try:
        from app.config import settings
        print("✓ app.config imported successfully")
        
        from app.main import app
        print("✓ app.main imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_structure():
    """Test that required directories exist."""
    required_dirs = [
        "app",
        "app/models",
        "config",
        "data/raw",
        "data/processed",
        "data/annotated",
        "data/knowledge_base",
        "scripts",
        "tests",
        "docs",
        "reports"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_exist = False
    
    return all_exist

def test_files():
    """Test that required files exist."""
    required_files = [
        "requirements.txt",
        "README.md",
        ".gitignore",
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/models/__init__.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ File missing: {file_path}")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("Testing Milestone 0 Setup...")
    print("=" * 50)
    
    print("\n1. Testing directory structure:")
    structure_ok = test_structure()
    
    print("\n2. Testing required files:")
    files_ok = test_files()
    
    print("\n3. Testing imports:")
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    if structure_ok and files_ok and imports_ok:
        print("✓ All tests passed! Milestone 0 setup is complete.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
