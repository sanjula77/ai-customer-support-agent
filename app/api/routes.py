# API routes placeholder

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agent.support_agent import get_support_agent
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger()


class SourceInfo(BaseModel):
    """Source metadata returned by the agent (if the RAG tool fires)."""

    title: Optional[str] = None
    score: Optional[float] = None
    source_file: Optional[str] = None
    section: Optional[str] = None


class AgentAskRequest(BaseModel):
    """Request schema for the /agent/ask endpoint."""

    session_id: str = Field(..., description="Conversation identifier used for memory threading")
    question: str = Field(..., min_length=1, max_length=1500, description="Customer message or query")
    k: int = Field(5, ge=1, le=20, description="Maximum RAG chunks when retrieval is selected")
    force_rag: Optional[bool] = Field(
        None,
        description="Debug flag: True forces RAG, False forces LLM reasoning, None lets the agent decide",
    )


class AgentAskResponse(BaseModel):
    """Response schema for the /agent/ask endpoint."""

    session_id: str
    message: str
    answer: str
    sources: List[SourceInfo] = []
    tool_used: str = Field(..., description="Tool chosen by the agent: rag or direct_llm")


@router.get("/")
def root():
    """Simple heartbeat for the API router."""
    return {"message": "AI Customer Support Agent Backend is running"}


@router.post("/agent/ask", response_model=AgentAskResponse, tags=["agent"])
async def agent_ask(payload: AgentAskRequest) -> AgentAskResponse:
    """
    Intelligent support-agent endpoint powered by the LangChain ReAct agent.

    The SupportAgent internally decides whether to call the RAG retrieval tool
    (for policy/manual questions) or the direct reasoning tool (for general tasks).
    """
    logger.info(
        "API | /agent/ask | session_id=%s | question='%s...'",
        payload.session_id,
        payload.question[:80],
    )

    try:
        agent = get_support_agent()
        result = await agent.process_query(
            session_id=payload.session_id,
            message=payload.question,
            k=payload.k,
            force_rag=payload.force_rag,
        )

        source_models = [
            SourceInfo(
                title=src.get("title"),
                score=src.get("score"),
                source_file=src.get("source_file"),
                section=src.get("section"),
            )
            for src in result.get("sources", [])
        ]

        return AgentAskResponse(
            session_id=result["session_id"],
            message=result["message"],
            answer=result["answer"],
            sources=source_models,
            tool_used=result.get("tool_used", "unknown"),
        )

    except HTTPException:
        # Bubble up FastAPI-native errors unchanged so their status codes are preserved
        raise
    except Exception as exc:
        logger.error(
            "API ERROR | /agent/ask | session_id=%s | error=%s",
            payload.session_id,
            exc,
        )
        raise HTTPException(status_code=500, detail=f"Failed to process question: {exc}") from exc
