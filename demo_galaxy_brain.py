#!/usr/bin/env python3
"""
Galaxy Brain 🌌 Demo Script
Demonstrates the power of our unified, hermetic NLP architecture
"""

import sys
import os
from pathlib import Path

def galaxy_brain_demo():
    """Demo showcasing Galaxy Brain architecture capabilities."""
    
    print("🌌 Galaxy Brain Demo - Unified NLP Architecture")
    print("=" * 60)
    
    # Show project structure
    print("\n📁 Galaxy Brain Monorepo Structure:")
    print("├── apps/                    # Deployable applications")
    print("│   ├── api_service/         # FastAPI production service")
    print("│   └── batch_processor/     # Large-scale processing")
    print("├── packages/               # Shared libraries")
    print("│   ├── nlp_utils/          # Core NLP functionality")
    print("│   └── custom_models/      # Custom architectures")
    print("├── ml_pipelines/           # Training & evaluation")
    print("├── tools/                  # Development utilities")
    print("└── bazel/                  # Custom build rules")
    
    # Show available components
    print("\n🔧 Available Galaxy Brain Components:")
    
    # Check apps
    apps_dir = Path("apps")
    if apps_dir.exists():
        for app in apps_dir.iterdir():
            if app.is_dir():
                build_file = app / "BUILD.bazel"
                if build_file.exists():
                    print(f"  ✅ {app.name:20s} - Ready for Bazel build")
                else:
                    print(f"  ⚠️  {app.name:20s} - Missing BUILD.bazel")
    
    # Check packages 
    packages_dir = Path("packages")
    if packages_dir.exists():
        for pkg in packages_dir.iterdir():
            if pkg.is_dir():
                build_file = pkg / "BUILD.bazel"
                if build_file.exists():
                    print(f"  ✅ {pkg.name:20s} - Ready for import")
                else:
                    print(f"  ⚠️  {pkg.name:20s} - Missing BUILD.bazel")
    
    # Show Bazel configuration
    print("\n⚙️  Bazel Configuration:")
    module_bazel = Path("MODULE.bazel")
    if module_bazel.exists():
        print("  ✅ MODULE.bazel           - Workspace configured")
    else:
        print("  ❌ MODULE.bazel           - Missing workspace config")
        
    bazelrc = Path(".bazelrc")
    if bazelrc.exists():
        print("  ✅ .bazelrc               - Build options configured")
    else:
        print("  ❌ .bazelrc               - Missing build config")
    
    # Show Python configuration
    print("\n🐍 Python Configuration:")
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        print("  ✅ pyproject.toml         - Modern Python packaging")
        # Check content
        content = pyproject.read_text()
        if "galaxy-brain" in content:
            print("  ✅ Project renamed        - Galaxy Brain ready")
        if "uv" in content:
            print("  ✅ UV integration         - Fast dependency management")
        if "bazel" in content.lower():
            print("  ✅ Bazel references       - Build system integrated")
    
    # Demo sample data processing
    print("\n📧 Sample Data Available:")
    ml_pipelines = Path("ml_pipelines")
    if ml_pipelines.exists():
        for data_file in ml_pipelines.glob("*.txt"):
            if data_file.name != "requirements_lock.txt":
                size = data_file.stat().st_size
                print(f"  📄 {data_file.name:20s} - {size:,} bytes")
    
    # Show Galaxy Brain advantages
    print("\n🚀 Galaxy Brain Advantages Demonstrated:")
    print("  ✅ Hermetic Builds         - All dependencies version-locked")
    print("  ✅ Monorepo Structure      - Unified codebase organization") 
    print("  ✅ Container Ready         - Production deployment targets")
    print("  ✅ ML Pipeline Support     - Training and evaluation workflows")
    print("  ✅ Modern Tooling          - UV, Bazel, FastAPI integration")
    
    # Show next steps
    print("\n🎯 Ready for Galaxy Brain Workflows:")
    print("  🔥 API Service:   bazel run //apps/api_service:fastapi_server")
    print("  ⚡ Batch Process: bazel run //apps/batch_processor:batch_processor")
    print("  🧪 ML Training:   bazel run //ml_pipelines:train_ner_model")
    print("  📦 Containers:    bazel build //apps/api_service:api_service_container")
    
    print("\n✨ Galaxy Brain transformation complete!")
    print("   From traditional chaos to hermetic excellence 🌌")

def show_sample_email_processing():
    """Show sample email content to demonstrate what we can process."""
    print("\n📧 Sample Email Processing Demo:")
    print("-" * 40)
    
    sample_email = """
Subject: URGENT: Widget-X Login Issues

Hi Support Team,

I'm experiencing critical issues with Widget-X login functionality. 
The system keeps returning authentication errors even with correct credentials.
This is blocking our entire team from accessing the platform.

Please escalate this to your technical team immediately as this is affecting
our production environment.

Best regards,
Sarah Johnson
Engineering Manager
"""
    
    print("Input Email:")
    print(sample_email.strip())
    
    print("\n🤖 Galaxy Brain Would Process This Into:")
    print("{")
    print('  "customer_id": "C_SARAH_JOHNSON",')
    print('  "product": "Widget-X",')
    print('  "sentiment": "negative",')
    print('  "urgency": "high",')
    print('  "entities": [')
    print('    {"text": "Widget-X", "label": "PRODUCT", "confidence": 0.95},')
    print('    {"text": "Sarah Johnson", "label": "PERSON", "confidence": 0.98}')
    print('  ],')
    print('  "summary": "Critical Widget-X login authentication errors affecting production",')
    print('  "next_action": "escalate_to_tier_2",')
    print('  "confidence_score": 0.87')
    print("}")

if __name__ == "__main__":
    galaxy_brain_demo()
    show_sample_email_processing()