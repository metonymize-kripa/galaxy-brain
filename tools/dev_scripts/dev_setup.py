"""Development environment setup script."""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_requirements():
    """Check if required tools are installed."""
    requirements = {
        "uv": "uv --version",
        "bazel": "bazel --version", 
        "python": "python --version"
    }
    
    missing = []
    for tool, cmd in requirements.items():
        result = run_command(cmd, f"Checking {tool}")
        if result is None:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("Please install them before continuing.")
        return False
    
    return True

def setup_python_environment():
    """Set up Python environment with uv."""
    commands = [
        ("uv venv", "Creating virtual environment"),
        ("uv pip install -e .", "Installing project dependencies"),
    ]
    
    for cmd, desc in commands:
        if run_command(cmd, desc) is None:
            return False
    
    return True

def download_spacy_models():
    """Download required spaCy models."""
    models = ["en_core_web_trf"]
    
    for model in models:
        cmd = f"uv run python -m spacy download {model}"
        if run_command(cmd, f"Downloading spaCy model {model}") is None:
            print(f"⚠️  Failed to download {model}, but continuing...")

def setup_bazel():
    """Set up Bazel workspace."""
    commands = [
        ("bazel clean", "Cleaning Bazel workspace"),
        ("bazel sync", "Syncing external dependencies"),
    ]
    
    for cmd, desc in commands:
        if run_command(cmd, desc) is None:
            return False
    
    return True

def verify_setup():
    """Verify the setup by running basic tests."""
    print("\n🧪 Verifying setup...")
    
    # Test Bazel build
    if run_command("bazel build //packages/nlp_utils:nlp_utils", "Testing Bazel build"):
        print("✅ Bazel build successful")
    else:
        print("❌ Bazel build failed")
        return False
    
    # Test Python imports
    test_import = """
import sys
sys.path.append('packages/nlp_utils/src')
try:
    from models import Ticket, Entity
    from extractors import EntityExtractor
    print('✅ Python imports successful')
except ImportError as e:
    print(f'❌ Python import failed: {e}')
    sys.exit(1)
"""
    
    if run_command(f'uv run python -c "{test_import}"', "Testing Python imports"):
        print("✅ Python environment verified")
    else:
        print("❌ Python environment verification failed")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🌌 Galaxy Brain Development Environment Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup Python environment
    if not setup_python_environment():
        print("❌ Failed to set up Python environment")
        sys.exit(1)
    
    # Download models
    download_spacy_models()
    
    # Setup Bazel
    if not setup_bazel():
        print("❌ Failed to set up Bazel workspace")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("❌ Setup verification failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: bazel test //... to run all tests")
    print("2. Run: bazel build //apps/api_service:api_service_container to build API container")
    print("3. Run: uv run python apps/batch_processor/src/test_demo.py for a quick demo")

if __name__ == "__main__":
    main()