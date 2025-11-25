"""
Main FastAPI application for NeuraHome AI Customer Support.

This is the entry point for the customer support AI application.
It provides REST API endpoints for querying the RAG system.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path for imports
# This allows the script to be run directly: python app/main.py
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Import routers (use absolute package paths only to avoid reload issues)
from app.api.routes import router as api_router
from app.routes.chat_router import router as chat_router

try:
    from app.api.ask import router as agent_router
except ImportError as e:
    import sys
    print(f"Warning: Could not import agent router: {e}", file=sys.stderr)
    agent_router = None

# Import RAG query engine
try:
    from app.rag.query_engine import ask_question, ask_question_with_sources
except ImportError:
    # Fallback for direct execution
    from rag.query_engine import ask_question, ask_question_with_sources


# Initialize FastAPI app
app = FastAPI(
    title="NeuraHome AI Customer Support",
    description="AI-powered customer support system using RAG (Retrieval-Augmented Generation)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

# Include agent router if available
if agent_router:
    app.include_router(agent_router, prefix="/agent", tags=["agent"])


# Request/Response models
class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str = Field(..., description="The question to ask", min_length=1, max_length=1000)
    k: Optional[int] = Field(5, description="Number of context chunks to retrieve", ge=1, le=20)
    include_sources: Optional[bool] = Field(False, description="Whether to include source information")


class SourceInfo(BaseModel):
    """Source information model."""
    title: str
    score: float
    category: Optional[str] = None
    source_file: Optional[str] = None
    section: Optional[str] = None


class AnswerResponse(BaseModel):
    """Response model for answer."""
    answer: str
    sources: Optional[List[SourceInfo]] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
    api_key_configured: bool


# API Endpoints
@app.get("/", tags=["root"])
def root():
    """Root endpoint."""
    return {
        "message": "NeuraHome AI Customer Support API is running!",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check():
    """Health check endpoint."""
    api_key_configured = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    
    return HealthResponse(
        status="ok",
        message="Service is healthy" if api_key_configured else "Service is running but API key not configured",
        api_key_configured=api_key_configured
    )


@app.post("/ask", response_model=AnswerResponse, tags=["query"])
async def ask(request: QuestionRequest):
    """
    Ask a question - uses intelligent agent that routes to RAG or direct LLM.
    
    This endpoint uses the support agent which automatically:
    - Uses RAG for product-specific questions (manuals, troubleshooting)
    - Uses direct LLM for general questions (math, general knowledge)
    
    Args:
        request: QuestionRequest with question and optional parameters
        
    Returns:
        AnswerResponse with answer and optionally sources
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        # Use agent for intelligent routing (if available)
        if agent_router:
            from app.agent.support_agent import get_support_agent
            
            agent = get_support_agent()
            # Use a default session_id if not provided (for backward compatibility)
            session_id = f"ask-endpoint-{hash(request.question) % 10000}"
            
            result = await agent.process_query(
                session_id=session_id,
                message=request.question,
                k=request.k
            )
            
            # Convert to AnswerResponse format
            sources = None
            if request.include_sources and result.get('sources'):
                sources = [
                    SourceInfo(
                        title=src.get('title', ''),
                        score=src.get('score', 0.0),
                        category=src.get('category'),
                        source_file=src.get('source_file'),
                        section=src.get('section')
                    )
                    for src in result['sources']
                ]
            
            return AnswerResponse(
                answer=result['answer'],
                sources=sources
            )
        else:
            # Fallback to old RAG-only system if agent not available
            if request.include_sources:
                result = ask_question_with_sources(request.question, k=request.k, verbose=False)
                
                # Convert sources to SourceInfo models
                sources = None
                if result.get('sources'):
                    sources = [
                        SourceInfo(
                            title=src.get('title', ''),
                            score=src.get('score', 0.0),
                            category=src.get('category'),
                            source_file=src.get('source_file'),
                            section=src.get('section')
                        )
                        for src in result['sources']
                    ]
                
                return AnswerResponse(
                    answer=result['answer'],
                    sources=sources
                )
            else:
                answer = ask_question(request.question, k=request.k, verbose=False)
                return AnswerResponse(answer=answer)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/ask", tags=["query"])
async def ask_get(
    question: str = Query(..., description="The question to ask"),
    k: int = Query(5, ge=1, le=20, description="Number of context chunks"),
    session_id: Optional[str] = Query(None, description="Optional session ID for conversation context")
):
    """
    Ask a question via GET request (for simple testing).
    Uses intelligent agent that routes to RAG or direct LLM.
    
    Args:
        question: The question to ask
        k: Number of context chunks to retrieve
        session_id: Optional session ID for conversation memory
        
    Returns:
        AnswerResponse with answer
    """
    try:
        # Use agent for intelligent routing (if available)
        if agent_router:
            from app.agent.support_agent import get_support_agent
            
            agent = get_support_agent()
            # Use provided session_id or generate one
            sid = session_id or f"ask-get-{hash(question) % 10000}"
            
            result = await agent.process_query(
                session_id=sid,
                message=question,
                k=k
            )
            
            return AnswerResponse(
                answer=result['answer'],
                sources=None  # GET endpoint doesn't return sources by default
            )
        else:
            # Fallback to old RAG-only system
            answer = ask_question(question, k=k, verbose=False)
            return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # Use __name__ to work when run directly or as module
    uvicorn.run(
        app,  # Pass app directly instead of string
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload when running directly
    )
