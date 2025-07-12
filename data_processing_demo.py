#!/usr/bin/env python3
"""
Galaxy Brain 🌌 - Data Processing Demo
Shows how our structured approach handles real email data
"""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path("packages/nlp_utils/src")))

def process_sample_emails():
    """Process real sample email data with Galaxy Brain models."""
    
    print("🌌 Galaxy Brain Data Processing Demo")
    print("=" * 50)
    
    # Import our models
    from models import Entity, Ticket
    
    # Read sample email data
    sample_files = [
        "ml_pipelines/single_email.txt",
        "ml_pipelines/complex_email.txt"
    ]
    
    processed_tickets = []
    
    for i, file_path in enumerate(sample_files):
        if Path(file_path).exists():
            email_content = Path(file_path).read_text().strip()
            
            print(f"\n📧 Processing Email {i+1}:")
            print(f"   File: {file_path}")
            print(f"   Length: {len(email_content):,} characters")
            print(f"   Preview: {email_content[:100]}...")
            
            # Mock NLP processing (in production this would use spaCy + HF)
            if "URGENT" in email_content.upper() or "critical" in email_content.lower():
                sentiment = "negative"
                urgency = "high"
            elif "question" in email_content.lower() or "help" in email_content.lower():
                sentiment = "neutral" 
                urgency = "medium"
            else:
                sentiment = "positive"
                urgency = "low"
            
            # Extract mock entities
            entities = []
            if "Widget-X" in email_content:
                entities.append(Entity(
                    text="Widget-X",
                    label="PRODUCT",
                    start=email_content.find("Widget-X"),
                    end=email_content.find("Widget-X") + 8,
                    confidence=0.95
                ))
            
            # Create ticket
            ticket = Ticket(
                customer_id=f"C_EMAIL_{i+1:03d}",
                product="Widget-X" if "Widget-X" in email_content else "General Support",
                sentiment=sentiment,
                urgency=urgency,
                entities=entities,
                summary=email_content.split('\n')[0][:100] + "..." if len(email_content.split('\n')[0]) > 100 else email_content.split('\n')[0],
                next_action="escalate_to_tier_2" if urgency == "high" else "assign_to_support",
                confidence_score=0.85 + (len(entities) * 0.05)
            )
            
            processed_tickets.append(ticket)
            
            print(f"   ✅ Processed: {sentiment} sentiment, {urgency} urgency")
            print(f"   🏷️  Entities: {len(entities)} found")
            print(f"   🎫 Customer: {ticket.customer_id}")
            
    # Show summary
    print(f"\n📊 Processing Summary:")
    print(f"   Total emails processed: {len(processed_tickets)}")
    print(f"   High urgency tickets: {sum(1 for t in processed_tickets if t.urgency == 'high')}")
    print(f"   Negative sentiment: {sum(1 for t in processed_tickets if t.sentiment == 'negative')}")
    print(f"   Average confidence: {sum(t.confidence_score for t in processed_tickets) / len(processed_tickets):.2f}")
    
    # Show JSON export capability
    print(f"\n💾 JSON Export Demo:")
    for i, ticket in enumerate(processed_tickets):
        json_output = ticket.model_dump_json(indent=2)
        print(f"   Ticket {i+1}: {len(json_output):,} characters")
        
        # Show first few lines of JSON
        lines = json_output.split('\n')[:5]
        for line in lines:
            print(f"     {line}")
        print("     ...")
    
    print(f"\n🎯 Galaxy Brain Advantage Demonstrated:")
    print(f"   ✅ Raw text → Structured JSON automatically")
    print(f"   ✅ Type-safe data models with validation")
    print(f"   ✅ Consistent output format for downstream systems")
    print(f"   ✅ Ready for API responses, database storage, or CRM integration")
    
    return processed_tickets

if __name__ == "__main__":
    tickets = process_sample_emails()
    print(f"\n🌌 Successfully processed {len(tickets)} emails with Galaxy Brain!")