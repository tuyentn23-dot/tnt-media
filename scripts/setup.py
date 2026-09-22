"""Setup Script for TNT Media"""
import os
import sys
import subprocess
import json
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [OK] {description}")
        return True
    else:
        print(f"  [FAILED] {description}")
        print(f"  Error: {result.stderr}")
        return False


def create_directory_structure():
    """Create necessary directories"""
    print("\nCreating directory structure...")
    directories = [
        'src', 'src/core', 'src/services', 'src/models', 'src/utils',
        'src/ai_composer', 'src/publishers', 'src/analytics',
        'tests', 'tests/unit', 'tests/integration',
        'docs', 'scripts', 'backups', 'deploy', 'logs',
        'memory', 'config', 'channels', 'output',
        'queue'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {directory}/")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  [OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  [FAILED] Python 3.8+ required, found {version.major}.{version.minor}")
        return False


def install_dependencies():
    """Install Python dependencies"""
    return run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    )


def run_tests():
    """Run test suite"""
    return run_command(
        "python -m pytest tests/ -v",
        "Running tests"
    )


def create_env_file():
    """Create .env file from example"""
    if not Path(".env").exists() and Path(".env.example").exists():
        print("\nCreating .env file...")
        shutil.copy(".env.example", ".env")
        print("  [OK] .env created from .env.example")
        print("  [NOTE] Please update .env with your actual values")
    else:
        print("\n.env file already exists or .env.example not found")


def initialize_database():
    """Initialize database"""
    print("\nInitializing database...")
    try:
        sys.path.insert(0, os.getcwd())
        from src.utils.database import DatabaseManager
        db = DatabaseManager()
        print("  [OK] Database initialized")
        return True
    except Exception as e:
        print(f"  [FAILED] Database initialization: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("TNT Media Setup")
    print("=" * 60)
    
    import shutil
    
    results = {
        "python_version": check_python_version(),
        "directory_structure": None,
        "dependencies": None,
        "database": None,
        "env_file": None,
        "tests": None
    }
    
    # Create directory structure
    create_directory_structure()
    results["directory_structure"] = True
    
    # Create .env file
    create_env_file()
    results["env_file"] = True
    
    # Install dependencies
    if results["python_version"]:
        results["dependencies"] = install_dependencies()
        
        # Initialize database
        if results["dependencies"]:
            results["database"] = initialize_database()
            
            # Run tests
            results["tests"] = run_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Setup Summary")
    print("=" * 60)
    
    for key, value in results.items():
        status = "OK" if value else "FAILED"
        print(f"  [{status}] {key}")
    
    print("\nSetup completed!")
    
    # Print next steps
    print("\nNext steps:")
    print("  1. Update .env with your API keys")
    print("  2. Run API server: python src/api_server.py")
    print("  3. Run worker: python scripts/worker.py")
    print("  4. Create backup: python scripts/backup.py backup")


if __name__ == '__main__':
    main()
