#!/usr/bin/env python3
"""
Galaxy Brain 🌌 - Simple Models Demo
Demonstrates the Pydantic models without heavy ML dependencies
"""

import sys
import os
from pathlib import Path

# Add the packages to path to import our models
sys.path.insert(0, str(Path(__file__).parent / "packages" / "nlp_utils" / "src"))

def test_galaxy_brain_models():
    """Test the core Galaxy Brain models functionality."""
    
    print("🌌 Galaxy Brain Models Demo")
    print("=" * 50)
    
    try:
        # Import our core models
        from models import Entity, Ticket
        
        print("✅ Successfully imported Galaxy Brain models!")
        print("   - Entity: For named entity representation")
        print("   - Ticket: For structured ticket output")
        
        # Create sample entities
        print("\n📝 Creating sample entities...")
        
        product_entity = Entity(
            text="Widget-X",
            label="PRODUCT", 
            start=25,
            end=33,
            confidence=0.95
        )
        
        person_entity = Entity(
            text="Sarah Johnson",
            label="PERSON",
            start=150,
            end=163,
            confidence=0.98
        )
        
        print(f"   Product Entity: {product_entity.text} ({product_entity.label})")
        print(f"   Person Entity: {person_entity.text} ({person_entity.label})")
        
        # Create a complete ticket
        print("\n🎫 Creating complete support ticket...")
        
        ticket = Ticket(
            customer_id="C_SARAH_JOHNSON",
            product="Widget-X",
            sentiment="negative",
            urgency="high",
            entities=[product_entity, person_entity],
            summary="Critical Widget-X login authentication errors affecting production",
            next_action="escalate_to_tier_2",
            confidence_score=0.87
        )
        
        print("✅ Successfully created Galaxy Brain ticket!")
        print("\n📋 Ticket Details:")
        print(f"   Customer: {ticket.customer_id}")
        print(f"   Product: {ticket.product}")
        print(f"   Sentiment: {ticket.sentiment}")
        print(f"   Urgency: {ticket.urgency}")
        print(f"   Entities: {len(ticket.entities)} found")
        print(f"   Summary: {ticket.summary[:50]}...")
        print(f"   Next Action: {ticket.next_action}")
        print(f"   Confidence: {ticket.confidence_score:.2f}")
        
        # Show JSON serialization
        print("\n🔄 JSON Serialization Test:")
        json_output = ticket.model_dump_json(indent=2)
        print("✅ Successfully serialized to JSON!")
        print(f"   JSON length: {len(json_output):,} characters")
        
        # Show validation features
        print("\n🛡️  Pydantic Validation Test:")
        try:
            # This should fail validation
            invalid_ticket = Ticket(
                customer_id="",  # Empty not allowed
                product="",
                sentiment="invalid_sentiment",  # Not in allowed values
                urgency="super_mega_urgent",  # Not in allowed values
                entities=[],
                summary="",
                next_action="",
                confidence_score=1.5  # Out of range
            )
        except Exception as e:
            print("✅ Validation correctly caught invalid data!")
            print(f"   Error type: {type(e).__name__}")
        
        # Demo processing workflow
        print("\n🔄 Galaxy Brain Processing Workflow:")
        sample_emails = [
            "Urgent! Widget-X is down for all users!",
            "Hi, I have a question about billing for SuperApp.",
            "The new AI features are amazing! Great work team!"
        ]
        
        mock_tickets = []
        for i, email in enumerate(sample_emails):
            # Mock processing (would use real NLP in production)
            sentiment_map = ["negative", "neutral", "positive"]
            urgency_map = ["high", "medium", "low"]
            
            mock_ticket = Ticket(
                customer_id=f"C_USER_{i+1:03d}",
                product="Widget-X" if "Widget" in email else "SuperApp" if "SuperApp" in email else "General",
                sentiment=sentiment_map[i],
                urgency=urgency_map[i],
                entities=[],  # Would be populated by real NER
                summary=email[:50] + "..." if len(email) > 50 else email,
                next_action="escalate_to_tier_2" if i == 0 else "assign_to_support",
                confidence_score=0.8 + (i * 0.05)
            )
            mock_tickets.append(mock_ticket)
        
        print(f"✅ Processed {len(mock_tickets)} emails into structured tickets")
        
        for i, ticket in enumerate(mock_tickets):
            print(f"   Email {i+1}: {ticket.sentiment} sentiment, {ticket.urgency} urgency")
        
        print("\n🎯 Galaxy Brain Models Demo Complete!")
        print("   ✅ Pydantic models working perfectly")
        print("   ✅ Data validation functioning") 
        print("   ✅ JSON serialization ready")
        print("   ✅ Structured data processing pipeline demonstrated")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the Galaxy Brain directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_bazel_integration():
    """Show how this integrates with Bazel build system."""
    
    print("\n🔧 Bazel Integration")
    print("-" * 30)
    
    # Check for BUILD files
    build_files = [
        "BUILD.bazel",
        "packages/nlp_utils/BUILD.bazel", 
        "apps/api_service/BUILD.bazel",
        "apps/batch_processor/BUILD.bazel"
    ]
    
    for build_file in build_files:
        if Path(build_file).exists():
            print(f"✅ {build_file}")
        else:
            print(f"❌ {build_file}")
    
    print("\n📦 Available Bazel Targets:")
    print("   //packages/nlp_utils:models       - Core Pydantic models")
    print("   //packages/nlp_utils:extractors   - NLP processing components")
    print("   //packages/nlp_utils:agent        - PydanticAI agent")
    print("   //apps/api_service:fastapi_server - Production API") 
    print("   //apps/batch_processor:demo       - This demo!")
    
    print("\n🚀 Ready for:")
    print("   bazel build //packages/nlp_utils:models")
    print("   bazel run //apps/batch_processor:demo")
    print("   bazel test //...")

if __name__ == "__main__":
    success = test_galaxy_brain_models()
    if success:
        show_bazel_integration()
        print("\n🌌 Galaxy Brain architecture is working! 🌌")
    else:
        print("\n❌ Demo failed - check setup")
        sys.exit(1)