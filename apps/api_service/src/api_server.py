"""FastAPI server for Galaxy Brain NLP services."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import os

# Add the packages to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../packages/nlp_utils/src'))

from agent import TriageAgent
from models import Ticket

app = FastAPI(
    title="Galaxy Brain NLP API",
    description="Production-ready NLP services powered by spaCy, Hugging Face, and PydanticAI",
    version="0.1.0"
)

# Global agent instance
triage_agent = TriageAgent()

class EmailRequest(BaseModel):
    """Request model for email processing."""
    email_text: str
    model: Optional[str] = "gpt-4o-mini"

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")

@app.post("/triage", response_model=Ticket)
async def triage_email(request: EmailRequest):
    """
    Process a customer email and return structured ticket information.
    
    This endpoint combines spaCy NER, Hugging Face sentiment analysis,
    and PydanticAI reasoning to create a complete support ticket.
    """
    try:
        ticket = await triage_agent.process_email(request.email_text)
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Galaxy Brain 🌌 NLP API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "triage": "/triage"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )