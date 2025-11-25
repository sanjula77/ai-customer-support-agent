"""
FastAPI router for the support agent endpoint.

Provides /ask endpoint that uses the intelligent support agent
to route queries to appropriate tools (RAG or direct LLM).
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.agent.support_agent import ask_agent, get_support_agent
from app.utils.logger import get_logger

logger = get_logger()

# Create router (not a new FastAPI app)
router = APIRouter()


class SourceInfo(BaseModel):
    """Source information model."""
    title: Optional[str] = None
    score: Optional[float] = None
    source_file: Optional[str] = None
    section: Optional[str] = None


class AskRequest(BaseModel):
    """Request model for asking the agent."""
    session_id: str = Field(..., description="Unique session ID for conversation context")
    question: str = Field(..., min_length=1, max_length=1500, description="User's question")
    k: int = Field(5, ge=1, le=20, description="Number of RAG chunks to retrieve (if RAG is used)")
    force_rag: Optional[bool] = Field(
        None,
        description="Force RAG usage (True) or direct LLM (False). None for auto-detection."
    )


class AskResponse(BaseModel):
    """Response model from the agent."""
    session_id: str
    message: str
    answer: str
    sources: List[SourceInfo] = []
    tool_used: str = Field(..., description="Tool used: 'rag' or 'direct_llm'")


@router.post("/ask", response_model=AskResponse, tags=["agent"])
async def ask_agent_endpoint(request: AskRequest) -> AskResponse:
    """
    Ask the support agent a question.
    
    The agent intelligently routes queries:
    - Uses RAG for product-specific questions (manuals, troubleshooting, setup)
    - Uses direct LLM for general questions or reasoning
    
    Maintains conversation context via session_id.
    
    Args:
        request: AskRequest with session_id, question, and optional parameters
        
    Returns:
        AskResponse with answer, sources, and metadata
        
    Raises:
        HTTPException: If processing fails
    """
    logger.info(
        f"AGENT API REQUEST | session_id={request.session_id} | "
        f"question='{request.question[:100]}...' | k={request.k}"
    )
    
    try:
        agent = get_support_agent()
        result = await agent.process_query(
            session_id=request.session_id,
            message=request.question,
            k=request.k,
            force_rag=request.force_rag
        )
        
        # Convert sources to SourceInfo models
        sources = []
        for src in result.get("sources", []):
            sources.append(SourceInfo(
                title=src.get("title"),
                score=src.get("score"),
                source_file=src.get("source_file"),
                section=src.get("section")
            ))
        
        logger.info(
            f"AGENT API RESPONSE | session_id={request.session_id} | "
            f"answer_length={len(result['answer'])} | tool_used={result.get('tool_used')}"
        )
        
        return AskResponse(
            session_id=result["session_id"],
            message=result["message"],
            answer=result["answer"],
            sources=sources,
            tool_used=result.get("tool_used", "unknown")
        )
        
    except Exception as e:
        logger.error(
            f"AGENT API ERROR | session_id={request.session_id} | "
            f"error_type={type(e).__name__} | error='{str(e)}'"
        )
        import traceback
        logger.error(f"AGENT API TRACEBACK | session_id={request.session_id}\n{traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing agent query: {str(e)}"
        ) from e


@router.get("/ask", response_model=AskResponse, tags=["agent"])
async def ask_agent_get(
    session_id: str = Query(..., description="Unique session ID"),
    question: str = Query(..., description="User's question"),
    k: int = Query(5, ge=1, le=20, description="Number of RAG chunks"),
    force_rag: Optional[bool] = Query(None, description="Force RAG (True) or direct LLM (False)")
) -> AskResponse:
    """
    GET endpoint for asking the agent (convenience for testing).
    
    Same functionality as POST /ask but via query parameters.
    """
    request = AskRequest(
        session_id=session_id,
        question=question,
        k=k,
        force_rag=force_rag
    )
    return await ask_agent_endpoint(request)
