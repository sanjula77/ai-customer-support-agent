# app/chat/chat_chain.py

from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from app.memory.memory import Message, get_memory_store
from app.rag.query_engine import get_rag_instance
from app.utils.logger import get_logger

logger = get_logger()


class ChatChain:
    """
    Conversation-aware coordinator that glues together:
    - Redis-backed chat memory
    - Existing RAG pipeline (vector store + Gemini LLM)
    The class keeps the synchronous RAG stack off the event loop by delegating
    blocking work to a thread executor.
    """

    def __init__(self, history_window: int = 10):
        self.memory = get_memory_store()
        self.history_window = history_window
        self._rag_chain = None

    def _get_rag_chain(self):
        if self._rag_chain is None:
            # Lazily initialize so the API can start even if RAG warm-up is heavy
            self._rag_chain = get_rag_instance(verbose=False)
        return self._rag_chain

    async def _run_in_executor(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    async def _search_docs(self, query: str, k: int):
        rag_chain = self._get_rag_chain()
        return await self._run_in_executor(rag_chain.vector_store.search, query, k, True)

    async def _invoke_chain(self, context: str, question: str) -> str:
        rag_chain = self._get_rag_chain()

        def _call_chain() -> str:
            response = rag_chain.chain.invoke({"context": context, "question": question})
            if hasattr(response, "content"):
                return response.content  # type: ignore[attr-defined]
            return str(response)

        result = await self._run_in_executor(_call_chain)
        return result.strip()

    @staticmethod
    def _format_history(history: List[Message]) -> str:
        if not history:
            return "No previous conversation."
        return "\n".join(f"{msg.role.title()}: {msg.content}" for msg in history)

    @staticmethod
    def _format_sources(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        formatted = []
        for item in results:
            metadata = item.get("metadata", {}) or {}
            formatted.append(
                {
                    "title": item.get("title") or metadata.get("title"),
                    "score": item.get("score"),
                    "source_file": metadata.get("source") or metadata.get("file"),
                    "section": metadata.get("section"),
                }
            )
        return formatted

    @staticmethod
    def _build_context(history_text: str, chunks: List[str]) -> str:
        knowledge = "\n\n---\n\n".join(chunks) if chunks else "No product context retrieved."
        return (
            f"Chat history:\n{history_text}\n\n"
            "Relevant product documentation:\n"
            f"{knowledge}"
        )

    async def generate_reply(self, session_id: str, user_message: str, k: int = 5) -> Dict[str, Any]:
        """
        Generate a conversational reply with full logging of each step.
        """
        try:
            # Persist the latest user input
            await self.memory.add_message(session_id, Message(role="user", content=user_message))
            logger.debug(f"MEMORY | session_id={session_id} | action=add_user_message | message_length={len(user_message)}")

            # 2. Fetch recent turns for conversational grounding
            history = await self.memory.get_recent(session_id, n=self.history_window)
            num_messages = len(history)
            
            logger.info(
                f"MEMORY RETRIEVAL | session_id={session_id} | "
                f"messages_retrieved={num_messages} | history_window={self.history_window}"
            )
            
            if history:
                # Log what messages were retrieved
                history_summary = "; ".join([
                    f"{msg.role}:{msg.content[:50]}..." if len(msg.content) > 50 else f"{msg.role}:{msg.content}"
                    for msg in history[-3:]  # Log last 3 messages as summary
                ])
                logger.debug(f"MEMORY RETRIEVAL CONTENT | session_id={session_id} | recent_messages={history_summary}")
            else:
                logger.debug(f"MEMORY RETRIEVAL | session_id={session_id} | status=no_history_found")

            # 3. Retrieve knowledge base chunks via the existing vector store
            logger.info(f"RAG RETRIEVAL START | session_id={session_id} | query='{user_message[:100]}...' | k={k}")
            
            rag_results = await self._search_docs(user_message, k)
            
            # Log RAG retrieval results
            logger.info(f"RAG RETRIEVAL COMPLETE | session_id={session_id} | chunks_retrieved={len(rag_results)}")
            
            for idx, result in enumerate(rag_results, 1):
                title = result.get("title") or result.get("metadata", {}).get("title", "N/A")
                score = result.get("score", 0.0)
                content_snippet = result.get("content", "")[:150] + "..." if len(result.get("content", "")) > 150 else result.get("content", "")
                
                logger.info(
                    f"RAG CHUNK {idx} | session_id={session_id} | "
                    f"title='{title}' | score={score:.4f} | content_snippet='{content_snippet}'"
                )
            
            context_chunks = [res.get("content", "") for res in rag_results if res.get("content")]
            history_text = self._format_history(history)
            full_context = self._build_context(history_text, context_chunks)
            
            logger.debug(f"CONTEXT BUILT | session_id={session_id} | context_length={len(full_context)}")

            # 4. Let the configured prompt template + Gemini LLM craft the answer
            logger.info(f"AI GENERATION START | session_id={session_id} | calling_gemini_api")
            
            answer = await self._invoke_chain(full_context, user_message)
            
            logger.info(
                f"AI GENERATION COMPLETE | session_id={session_id} | "
                f"answer_length={len(answer)} | answer_preview='{answer[:150]}...'"
            )

            # Store assistant response for continuity
            await self.memory.add_message(session_id, Message(role="assistant", content=answer))
            logger.debug(f"MEMORY | session_id={session_id} | action=add_assistant_message | answer_length={len(answer)}")

            formatted_sources = self._format_sources(rag_results)
            
            logger.info(
                f"CHAT CHAIN COMPLETE | session_id={session_id} | "
                f"answer_length={len(answer)} | sources_count={len(formatted_sources)}"
            )

            return {"answer": answer, "sources": formatted_sources}
            
        except Exception as e:
            # Log any errors during the chat chain execution
            logger.error(
                f"CHAT CHAIN ERROR | session_id={session_id} | "
                f"error_type={type(e).__name__} | error='{str(e)}'"
            )
            raise
