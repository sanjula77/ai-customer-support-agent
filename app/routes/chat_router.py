# app/routes/chat_router.py

import traceback
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.chat.chat_chain import ChatChain
from app.utils.logger import get_logger

router = APIRouter()
chat_chain = ChatChain()
logger = get_logger()


class SourceModel(BaseModel):
    title: Optional[str] = None
    score: Optional[float] = None
    source_file: Optional[str] = None
    section: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Opaque identifier that scopes chat memory")
    message: str = Field(..., min_length=1, max_length=1500)
    k: int = Field(5, ge=1, le=10, description="Number of knowledge chunks to include")


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceModel] = []


@router.post("/message", response_model=ChatResponse, tags=["chat"])
async def chat_message(payload: ChatRequest) -> ChatResponse:
    """
    Chat endpoint with full request/response logging.
    Logs: incoming request, memory retrieval, RAG retrieval, AI response, and errors.
    """
    request_timestamp = datetime.now().isoformat()
    
    # 1. Log incoming request
    logger.info(
        f"INCOMING REQUEST | session_id={payload.session_id} | "
        f"message='{payload.message[:100]}...' | k={payload.k} | timestamp={request_timestamp}"
    )
    
    try:
        # Generate reply (this will log memory, RAG, and AI steps internally)
        reply = await chat_chain.generate_reply(
            session_id=payload.session_id,
            user_message=payload.message,
            k=payload.k,
        )
        
        # 4. Log AI/Gemini response
        answer = reply["answer"]
        sources = reply.get("sources", [])
        response_timestamp = datetime.now().isoformat()
        
        logger.info(
            f"AI RESPONSE | session_id={payload.session_id} | "
            f"answer_length={len(answer)} | num_sources={len(sources)} | timestamp={response_timestamp}"
        )
        logger.debug(f"AI RESPONSE CONTENT | session_id={payload.session_id} | answer='{answer[:200]}...'")
        
        # Log final output summary
        logger.info(
            f"REQUEST COMPLETE | session_id={payload.session_id} | "
            f"status=success | answer_length={len(answer)} | sources_count={len(sources)}"
        )
        
        return ChatResponse(
            answer=answer,
            sources=[SourceModel(**src) for src in sources if src],
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (these are intentional)
        raise
    except Exception as exc:
        # 5. Log errors/exceptions with full traceback
        error_timestamp = datetime.now().isoformat()
        error_traceback = traceback.format_exc()
        
        logger.error(
            f"ERROR | session_id={payload.session_id} | "
            f"exception_type={type(exc).__name__} | error='{str(exc)}' | timestamp={error_timestamp}"
        )
        logger.error(f"FULL TRACEBACK | session_id={payload.session_id}\n{error_traceback}")
        
        raise HTTPException(status_code=500, detail=f"Unable to generate reply: {exc}") from exc
