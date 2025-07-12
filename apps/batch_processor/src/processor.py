"""Batch processor for large-scale email triage."""

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Dict
import json
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table

# Add the packages to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../packages/nlp_utils/src'))

from agent import TriageAgent
from models import Ticket

console = Console()

class BatchProcessor:
    """Processes multiple emails in batch for large-scale operations."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.agent = TriageAgent(model)
        self.results: List[Dict] = []
    
    async def process_email_batch(self, emails: List[str]) -> List[Ticket]:
        """Process a batch of emails concurrently."""
        tickets = []
        
        with Progress() as progress:
            task = progress.add_task("Processing emails...", total=len(emails))
            
            # Process emails with controlled concurrency
            semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests
            
            async def process_single(email_text: str) -> Ticket:
                async with semaphore:
                    try:
                        ticket = await self.agent.process_email(email_text)
                        progress.advance(task)
                        return ticket
                    except Exception as e:
                        console.print(f"[red]Error processing email: {e}[/red]")
                        progress.advance(task)
                        return None
            
            # Process all emails concurrently
            tasks = [process_single(email) for email in emails]
            tickets = await asyncio.gather(*tasks)
            
        # Filter out failed results
        return [ticket for ticket in tickets if ticket is not None]
    
    def load_emails_from_file(self, file_path: str) -> List[str]:
        """Load emails from a text file (one email per line or separated by blank lines)."""
        path = Path(file_path)
        if not path.exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            return []
        
        content = path.read_text()
        
        # Try to split by double newlines first (email separation)
        emails = content.split('\n\n')
        if len(emails) == 1:
            # If no double newlines, split by single newlines
            emails = content.split('\n')
        
        # Filter out empty emails
        emails = [email.strip() for email in emails if email.strip()]
        
        console.print(f"[green]Loaded {len(emails)} emails from {file_path}[/green]")
        return emails
    
    def export_results(self, tickets: List[Ticket], output_format: str = "json", output_file: str = None):
        """Export results in various formats."""
        if not tickets:
            console.print("[yellow]No tickets to export[/yellow]")
            return
        
        if output_format == "json":
            data = [ticket.dict() for ticket in tickets]
            output = json.dumps(data, indent=2)
        elif output_format == "csv":
            # Simple CSV export
            import csv
            import io
            output_io = io.StringIO()
            writer = csv.DictWriter(output_io, fieldnames=tickets[0].dict().keys())
            writer.writeheader()
            for ticket in tickets:
                writer.writerow(ticket.dict())
            output = output_io.getvalue()
        else:
            console.print(f"[red]Unsupported format: {output_format}[/red]")
            return
        
        if output_file:
            Path(output_file).write_text(output)
            console.print(f"[green]Results exported to {output_file}[/green]")
        else:
            console.print(output)
    
    def print_summary(self, tickets: List[Ticket]):
        """Print a summary table of processed tickets."""
        if not tickets:
            console.print("[yellow]No tickets processed[/yellow]")
            return
        
        table = Table(title="Batch Processing Summary")
        table.add_column("Customer ID", style="cyan")
        table.add_column("Product", style="magenta")
        table.add_column("Sentiment", style="green")
        table.add_column("Urgency", style="red")
        table.add_column("Confidence", style="blue")
        
        for ticket in tickets[:10]:  # Show first 10
            table.add_row(
                ticket.customer_id,
                ticket.product,
                ticket.sentiment,
                ticket.urgency,
                f"{ticket.confidence_score:.2f}"
            )
        
        console.print(table)
        
        if len(tickets) > 10:
            console.print(f"[dim]... and {len(tickets) - 10} more tickets[/dim]")
        
        # Summary stats
        urgency_counts = {}
        sentiment_counts = {}
        for ticket in tickets:
            urgency_counts[ticket.urgency] = urgency_counts.get(ticket.urgency, 0) + 1
            sentiment_counts[ticket.sentiment] = sentiment_counts.get(ticket.sentiment, 0) + 1
        
        console.print(f"\n[bold]Processing Summary:[/bold]")
        console.print(f"Total tickets: {len(tickets)}")
        console.print(f"Urgency distribution: {urgency_counts}")
        console.print(f"Sentiment distribution: {sentiment_counts}")
        avg_confidence = sum(t.confidence_score for t in tickets) / len(tickets)
        console.print(f"Average confidence: {avg_confidence:.2f}")

async def main():
    """Main entry point for batch processor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Galaxy Brain Batch Email Processor")
    parser.add_argument("input_file", help="File containing emails to process")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model to use")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--summary", action="store_true", help="Print summary table")
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.model)
    
    # Load and process emails
    emails = processor.load_emails_from_file(args.input_file)
    if not emails:
        return
    
    console.print(f"[blue]Processing {len(emails)} emails with model {args.model}...[/blue]")
    
    tickets = await processor.process_email_batch(emails)
    
    if args.summary:
        processor.print_summary(tickets)
    
    if args.output:
        processor.export_results(tickets, args.format, args.output)
    else:
        processor.export_results(tickets, args.format)

if __name__ == "__main__":
    asyncio.run(main())