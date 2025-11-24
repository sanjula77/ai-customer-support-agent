# app/memory/memory.py
"""
Async Redis conversational memory module.

Usage:
    from app.memory.memory import MemoryStore, Message

    mem = MemoryStore()  # reads config from env or uses defaults
    await mem.add_message("session123", Message(role="user", content="Hello"))
    history = await mem.get_history("session123")  # list[Message]
"""

import asyncio
import json
import os
import traceback
from dataclasses import asdict, dataclass
from typing import List, Optional

try:
    import redis.asyncio as aioredis
except ImportError as exc:  # pragma: no cover - defensive import guard
    raise ImportError(
        "The 'redis' extra is required for chat memory. Install it via `pip install redis>=5`."
    ) from exc

from app.utils.logger import get_logger

logger = get_logger()

# Configuration -- override via environment variables if needed
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MAX_HISTORY = int(os.getenv("RAG_MEMORY_MAX_HISTORY", "10"))       # keep last N messages
SESSION_TTL_SECONDS = int(os.getenv("RAG_MEMORY_TTL", str(60 * 60 * 24 * 7)))  # default 7 days


@dataclass
class Message:
    role: str  # "user", "assistant", "system", etc.
    content: str


class MemoryStore:
    def __init__(self, url: str = REDIS_URL, max_history: int = MAX_HISTORY, ttl: int = SESSION_TTL_SECONDS):
        """
        Initialize Redis connection (async).
        """
        self._url = url
        self._redis = aioredis.from_url(self._url, encoding="utf-8", decode_responses=True)
        self._max_history = max_history
        self._ttl = ttl

    def _key(self, session_id: str) -> str:
        return f"chat_history:{session_id}"

    async def add_message(self, session_id: str, message: Message) -> None:
        """
        Append a message to the session history and trim to MAX_HISTORY.
        Stores message as JSON string in a Redis list.
        Also sets TTL on the session key.
        """
        try:
            key = self._key(session_id)
            payload = json.dumps(asdict(message), ensure_ascii=False)

            # RPUSH then LTRIM keeps only latest `max_history` elements
            # Using pipeline to group commands
            async with self._redis.pipeline() as pipe:
                pipe.rpush(key, payload)
                # Keep only last N messages (negative indexing)
                pipe.ltrim(key, -self._max_history, -1)
                # Reset TTL to keep session alive for configured time
                if self._ttl > 0:
                    pipe.expire(key, self._ttl)
                await pipe.execute()
            
            logger.debug(
                f"MEMORY OPERATION | session_id={session_id} | action=add_message | "
                f"role={message.role} | content_length={len(message.content)}"
            )
        except Exception as e:
            logger.error(
                f"MEMORY ERROR | session_id={session_id} | operation=add_message | "
                f"error_type={type(e).__name__} | error='{str(e)}'"
            )
            logger.error(f"MEMORY TRACEBACK | session_id={session_id}\n{traceback.format_exc()}")
            raise

    async def get_history(self, session_id: str) -> List[Message]:
        """
        Retrieve all stored messages for session_id (oldest -> newest).
        Returns a list of Message objects.
        If no history, returns an empty list.
        """
        key = self._key(session_id)
        raw = await self._redis.lrange(key, 0, -1)
        messages: List[Message] = []
        for item in raw:
            try:
                data = json.loads(item)
                messages.append(Message(role=data.get("role", "user"), content=data.get("content", "")))
            except Exception:
                # Skip malformed entries
                continue
        return messages

    async def get_recent(self, session_id: str, n: Optional[int] = None) -> List[Message]:
        """
        Retrieve the most recent n messages (newest last).
        If n is None, returns full history (up to max_history).
        """
        try:
            key = self._key(session_id)
            if n is None:
                raw = await self._redis.lrange(key, 0, -1)
            else:
                # lrange with negative index: -n to -1 (last n items)
                raw = await self._redis.lrange(key, -n, -1)
            
            messages: List[Message] = []
            for item in raw:
                try:
                    data = json.loads(item)
                    messages.append(Message(role=data.get("role", "user"), content=data.get("content", "")))
                except Exception as parse_err:
                    logger.warning(
                        f"MEMORY WARNING | session_id={session_id} | "
                        f"action=parse_message | error='{str(parse_err)}' | skipping_malformed_entry"
                    )
                    continue
            
            logger.debug(
                f"MEMORY OPERATION | session_id={session_id} | action=get_recent | "
                f"requested_n={n} | messages_returned={len(messages)}"
            )
            return messages
        except Exception as e:
            logger.error(
                f"MEMORY ERROR | session_id={session_id} | operation=get_recent | "
                f"error_type={type(e).__name__} | error='{str(e)}'"
            )
            logger.error(f"MEMORY TRACEBACK | session_id={session_id}\n{traceback.format_exc()}")
            raise

    async def clear_history(self, session_id: str) -> None:
        """
        Remove the whole session history from Redis.
        """
        key = self._key(session_id)
        await self._redis.delete(key)

    async def session_exists(self, session_id: str) -> bool:
        key = self._key(session_id)
        return await self._redis.exists(key) == 1

    async def close(self) -> None:
        """
        Close redis connection gracefully.
        """
        await self._redis.close()
        # redis.asyncio sometimes needs explicit wait_closed
        try:
            await self._redis.connection_pool.disconnect()
        except Exception:
            pass


# Convenience: singleton MemoryStore instance for quick imports
_memory_instance: Optional[MemoryStore] = None

__all__ = ["Message", "MemoryStore", "get_memory_store", "reset_memory_store"]


def get_memory_store() -> MemoryStore:
    """
    Return a process-wide singleton MemoryStore so Redis connections are reused.
    """
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryStore()
    return _memory_instance


def reset_memory_store() -> None:
    """
    Reset the cached MemoryStore instance. Mainly useful for unit tests.
    """
    global _memory_instance
    _memory_instance = None


# ----------------------
# Simple test runner
# ----------------------
if __name__ == "__main__":
    async def _test():
        mem = MemoryStore()
        sid = "test_session_1"
        print("Clearing test session...")
        await mem.clear_history(sid)

        print("Adding messages...")
        await mem.add_message(sid, Message(role="user", content="Hello"))
        await mem.add_message(sid, Message(role="assistant", content="Hi, how can I help?"))
        await mem.add_message(sid, Message(role="user", content="How to reset my hub?"))

        print("History:")
        hist = await mem.get_history(sid)
        for m in hist:
            print(f" - {m.role}: {m.content}")

        print("Recent 2:")
        recent = await mem.get_recent(sid, 2)
        for m in recent:
            print(f" - {m.role}: {m.content}")

        print("Clearing history...")
        await mem.clear_history(sid)
        await mem.close()

    asyncio.run(_test())
