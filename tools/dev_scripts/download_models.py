"""Script to download and cache required ML models."""

import subprocess
import sys
import os
from pathlib import Path
from huggingface_hub import snapshot_download
import spacy

def download_spacy_models():
    """Download required spaCy models."""
    models = [
        "en_core_web_trf",  # Transformer-based English model
        "en_core_web_sm",   # Small English model (backup)
    ]
    
    for model in models:
        print(f"📥 Downloading spaCy model: {model}")
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", model], check=True)
            print(f"✅ Successfully downloaded {model}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download {model}: {e}")

def download_huggingface_models():
    """Download and cache Hugging Face models."""
    models = [
        "distilbert-base-uncased-finetuned-sst-2-english",  # Sentiment analysis
        "microsoft/DialoGPT-medium",  # Optional: conversational model
    ]
    
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    for model in models:
        print(f"📥 Downloading Hugging Face model: {model}")
        try:
            snapshot_download(
                repo_id=model,
                cache_dir=cache_dir,
                local_files_only=False
            )
            print(f"✅ Successfully downloaded {model}")
        except Exception as e:
            print(f"❌ Failed to download {model}: {e}")

def verify_models():
    """Verify that models are properly installed."""
    print("\n🔍 Verifying model installations...")
    
    # Test spaCy models
    try:
        nlp = spacy.load("en_core_web_trf")
        doc = nlp("Test sentence for verification.")
        print("✅ spaCy transformer model working")
    except Exception as e:
        print(f"❌ spaCy model verification failed: {e}")
    
    # Test Hugging Face models
    try:
        from transformers import pipeline
        classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        result = classifier("This is a test.")
        print("✅ Hugging Face sentiment model working")
    except Exception as e:
        print(f"❌ Hugging Face model verification failed: {e}")

def main():
    """Main model download function."""
    print("🌌 Galaxy Brain Model Download Script")
    print("=" * 40)
    
    # Download spaCy models
    download_spacy_models()
    
    print()
    
    # Download Hugging Face models
    download_huggingface_models()
    
    # Verify installations
    verify_models()
    
    print("\n🎉 Model download completed!")
    print("Models are cached and ready for use.")

if __name__ == "__main__":
    main()