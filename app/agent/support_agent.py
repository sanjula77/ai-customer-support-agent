"""
LangChain ReAct Agent for Customer Support.

This agent uses LangChain's ReAct framework to intelligently decide:
- When to use RAG (retrieval tool)
- When to use direct LLM reasoning
- When to ask follow-up questions

Uses LangChain's create_react_agent with proper tools and guardrails.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import json

from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

from app.memory.memory import Message, get_memory_store
from app.rag.query_engine import get_rag_instance
from app.utils.logger import get_logger
from app.tools import OrderLookupTool, TicketTool, UpdateAddressTool

logger = get_logger()

# Cache for whichever AgentExecutor class exists in the installed LangChain version
_AGENT_EXECUTOR_CLS = None


def _get_agent_executor_cls():
    """Return the AgentExecutor class regardless of LangChain version."""
    global _AGENT_EXECUTOR_CLS
    if _AGENT_EXECUTOR_CLS is not None:
        return _AGENT_EXECUTOR_CLS

    candidate_modules = [
        "langchain.agents",
        "langchain.agents.agent",
        "langchain.agents.agent_executor",
    ]

    for module_path in candidate_modules:
        try:
            module = __import__(module_path, fromlist=["AgentExecutor"])
            _AGENT_EXECUTOR_CLS = getattr(module, "AgentExecutor")
            return _AGENT_EXECUTOR_CLS
        except (ImportError, AttributeError):
            continue

    raise ImportError(
        "Could not import AgentExecutor from LangChain. "
        "Please upgrade langchain to >=0.1.0 or ensure agent components are installed."
    )


class SupportAgent:
    """
    LangChain ReAct Agent for intelligent customer support.
    
    The agent can:
    - Use RAG tool for product documentation questions
    - Use LLM reasoning tool for general questions
    - Ask clarifying questions when needed
    - Maintain conversation context
    """

    def __init__(self, history_window: int = 10):
        """
        Initialize the LangChain ReAct Agent.
        
        Args:
            history_window: Number of recent messages to include in context
        """
        self.memory = get_memory_store()
        self.history_window = history_window
        self._rag_chain = None
        self._llm = None
        self._agent_executor = None
        self._order_tool = OrderLookupTool()
        self._ticket_tool = TicketTool()
        self._address_tool = UpdateAddressTool()

    def _get_rag_chain(self):
        """Lazy initialization of RAG chain."""
        if self._rag_chain is None:
            self._rag_chain = get_rag_instance(verbose=False)
        return self._rag_chain

    def _get_llm(self):
        """Lazy initialization of LLM for agent."""
        if self._llm is None:
            import os
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Google API key not found!")
            
            self._llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.2,
                google_api_key=api_key
            )
        return self._llm

    async def _run_in_executor(self, func, *args, **kwargs):
        """Run synchronous function in thread executor."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    def _create_rag_tool(self) -> Tool:
        """
        Create RAG retrieval tool for LangChain agent.
        
        Returns:
            LangChain Tool for RAG retrieval
        """
        def rag_search(query: str) -> str:
            """
            Search the NeuraHome knowledge base for product information.
            
            Use this tool for questions about:
            - Product manuals and setup instructions
            - Troubleshooting guides
            - Policy documents (shipping, returns, warranty)
            - FAQs about NeuraHome products
            
            Args:
                query: The question to search for
                
            Returns:
                Answer from knowledge base
            """
            try:
                logger.info(f"RAG TOOL CALLED | query='{query[:100]}...'")
                rag_chain = self._get_rag_chain()
                result = rag_chain.ask_with_sources(query, k=5)
                answer = result.get("answer", "No information found.")
                
                # Include source information
                sources = result.get("sources", [])
                if sources:
                    source_info = "\n\nSources:\n" + "\n".join([
                        f"- {src.get('title', 'N/A')}" for src in sources[:3]
                    ])
                    answer += source_info
                
                logger.info(f"RAG TOOL RESULT | answer_length={len(answer)}")
                return answer
            except Exception as e:
                logger.error(f"RAG TOOL ERROR | error='{str(e)}'")
                return f"Error searching knowledge base: {str(e)}"

        return Tool(
            name="rag_knowledge_base",
            func=rag_search,
            description=(
                "Search the NeuraHome product knowledge base. "
                "Use this tool for questions about: product manuals, setup instructions, "
                "troubleshooting, policies (shipping, returns, warranty), FAQs, and any "
                "NeuraHome product-specific information. "
                "Input should be a clear question about NeuraHome products or policies."
            )
        )

    def _create_reasoning_tool(self) -> Tool:
        """
        Create LLM reasoning tool for general questions.
        
        Returns:
            LangChain Tool for direct LLM reasoning
        """
        def llm_reasoning(query: str) -> str:
            """
            Use LLM for general reasoning, calculations, or questions not in knowledge base.
            
            Use this tool for:
            - Mathematical calculations
            - General knowledge questions
            - Questions not related to NeuraHome products
            - Conversational responses
            
            Args:
                query: The question or statement to reason about
                
            Returns:
                LLM-generated answer
            """
            try:
                logger.info(f"REASONING TOOL CALLED | query='{query[:100]}...'")
                llm = self._get_llm()
                response = llm.invoke(query)
                answer = response.content if hasattr(response, "content") else str(response)
                logger.info(f"REASONING TOOL RESULT | answer_length={len(answer)}")
                return answer.strip()
            except Exception as e:
                logger.error(f"REASONING TOOL ERROR | error='{str(e)}'")
                return f"Error processing question: {str(e)}"

        return Tool(
            name="llm_reasoning",
            func=llm_reasoning,
            description=(
                "Use this tool for general reasoning, calculations, or questions that don't "
                "require NeuraHome product knowledge. Use for: math problems, general knowledge, "
                "conversational responses, or questions outside the product documentation. "
                "Input should be the question or statement to reason about."
            )
        )

    def _create_order_lookup_tool(self) -> Tool:
        """Create a tool for looking up order details."""

        def lookup(order_id: str) -> str:
            oid = order_id.strip()
            if not oid:
                return "Please provide an order ID (e.g., 1234)."

            result = self._order_tool.lookup(oid)
            if "error" in result:
                return result["error"]

            items = ", ".join(result.get("items", [])) or "No items recorded"
            total = result.get("total_price", "Unknown")
            status = result.get("status", "Unknown")
            eta = result.get("expected_delivery", "Unknown delivery date")
            return (
                f"Order {oid} for user {result.get('user_id', 'unknown')}:\n"
                f"- Status: {status}\n"
                f"- Items: {items}\n"
                f"- Total Price: ${total}\n"
                f"- Expected Delivery: {eta}"
            )

        return Tool(
            name="order_lookup",
            func=lookup,
            description=(
                "Fetch order status and items. Input must be the order ID string, "
                "e.g., '1234'."
            ),
        )

    def _create_ticket_tool(self) -> Tool:
        """Create a tool for logging customer support tickets."""

        def create_ticket(payload: str) -> str:
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                return (
                    "Invalid input. Provide JSON like "
                    '{"issue_type":"delivery_issue","description":"details","user_id":"u001"}.'
                )

            required = ["issue_type", "description", "user_id"]
            missing = [field for field in required if not data.get(field)]
            if missing:
                return f"Missing required fields: {', '.join(missing)}"

            ticket = self._ticket_tool.create_ticket(
                issue_type=data["issue_type"],
                description=data["description"],
                user_id=data["user_id"],
            )
            return (
                f"Ticket {ticket['ticket_id']} created for user {ticket['user_id']} "
                f"({ticket['issue_type']}). Status: {ticket['status']}."
            )

        return Tool(
            name="ticket_creator",
            func=create_ticket,
            description=(
                "Create a support ticket. Input must be JSON with "
                "'issue_type', 'description', and 'user_id'."
            ),
        )

    def _create_address_update_tool(self) -> Tool:
        """Create a tool for updating user addresses."""

        def update_address(payload: str) -> str:
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                return (
                    "Invalid input. Provide JSON like "
                    '{"user_id":"u001","new_address":"123 Main St"}.'
                )

            user_id = data.get("user_id")
            new_address = data.get("new_address")
            if not user_id or not new_address:
                return "Both 'user_id' and 'new_address' are required."

            result = self._address_tool.update(user_id, new_address)
            if "error" in result:
                return result["error"]

            return (
                f"Address updated for {result.get('name', 'user')} "
                f"({result['user_id']}). New address: {result['address']}."
            )

        return Tool(
            name="update_address",
            func=update_address,
            description=(
                "Update a user's address. Input must be JSON with "
                "'user_id' and 'new_address'."
            ),
        )

    def _create_agent_executor(self) -> Any:
        """
        Create LangChain ReAct Agent with tools.
        
        Returns:
            Configured AgentExecutor
        """
        if self._agent_executor is None:
            # Create tools
            tools = [
                self._create_rag_tool(),
                self._create_reasoning_tool(),
                self._create_order_lookup_tool(),
                self._create_ticket_tool(),
                self._create_address_update_tool(),
            ]

            # Create ReAct agent
            llm = self._get_llm()
            
            # Try new LangChain API first (v0.1.0+)
            try:
                from langchain.agents import create_react_agent

                prompt = PromptTemplate.from_template(
                    """You are NeuraHome's AI support agent that must decide when to use tools.
Always follow these rules:
- Use order_lookup when the customer asks about an order number or shipment status; pass only the order ID string.
- Use ticket_creator when the customer reports a problem that needs follow-up; pass JSON with issue_type, description, user_id.
- Use update_address when the customer requests an address change; pass JSON with user_id and new_address.
- Use rag_knowledge_base for policy, manual, or troubleshooting questions.
- Use llm_reasoning for general conversation, calculations, or when no tool is appropriate.

Respond in the ReAct format:

Question: {input}
Thought: consider whether a tool is needed
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the tool result
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the response for the user, citing tool results when used

Begin!

Thought: {agent_scratchpad}"""
                )

                agent = create_react_agent(llm, tools, prompt)
                
                # Create executor
                AgentExecutorCls = _get_agent_executor_cls()
                self._agent_executor = AgentExecutorCls(
                    agent=agent,
                    tools=tools,
                    verbose=False,
                    max_iterations=5,
                    max_execution_time=30,
                    handle_parsing_errors=True,
                    return_intermediate_steps=True
                )
                logger.info("LangChain ReAct Agent initialized (new API)")
                
            except (ImportError, Exception) as e:
                # Fallback to old API
                logger.warning(f"New LangChain API not available, using fallback: {e}")
                try:
                    from langchain.agents import initialize_agent, AgentType
                    
                    try:
                        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
                    except AttributeError:
                        agent_type = AgentType.REACT_DOCSTORE
                    
                    self._agent_executor = initialize_agent(
                        tools=tools,
                        llm=llm,
                        agent=agent_type,
                        verbose=False,
                        max_iterations=5,
                        max_execution_time=30,
                        handle_parsing_errors=True,
                        return_intermediate_steps=True
                    )
                    logger.info("LangChain ReAct Agent initialized (legacy API)")
                except ImportError:
                    raise ImportError(
                        "Could not initialize LangChain agent. "
                        "Please ensure langchain is installed: pip install langchain"
                    )

        return self._agent_executor

    async def process_query(
        self,
        session_id: str,
        message: str,
        k: int = 5,
        force_rag: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Process a user query through the LangChain ReAct Agent.
        
        Args:
            session_id: Session identifier for conversation memory
            message: User's question
            k: Number of RAG chunks (ignored if agent chooses tool)
            force_rag: Ignored (agent decides automatically)
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        logger.info(
            f"AGENT QUERY START | session_id={session_id} | "
            f"message='{message[:100]}...'"
        )

        try:
            # 1. Retrieve conversation history
            history = await self.memory.get_recent(session_id, n=self.history_window)
            history_text = self._format_history(history)
            
            logger.info(
                f"AGENT MEMORY | session_id={session_id} | "
                f"history_messages={len(history)}"
            )

            # 2. Build input with conversation context
            if history_text and history_text != "No previous conversation.":
                full_input = f"""Previous conversation context:
{history_text}

Current question: {message}

Answer the current question, considering the conversation history if relevant."""
            else:
                full_input = message

            # 3. Execute agent
            agent_executor = self._create_agent_executor()
            
            logger.info(f"AGENT EXECUTION START | session_id={session_id}")
            
            result = await self._run_in_executor(
                agent_executor.invoke,
                {"input": full_input}
            )
            
            answer = result.get("output", "I couldn't process your question.")
            tools_used = []
            sources = []
            
            # Extract which tools were used (if available in result)
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    if len(step) > 0:
                        action = step[0]
                        if hasattr(action, "tool"):
                            tool_name = action.tool
                            tools_used.append(tool_name)
                            # If RAG tool was used, try to extract sources from the observation
                            if tool_name == "rag_knowledge_base" and len(step) > 1:
                                observation = step[1]
                                # Sources are embedded in the RAG tool's response
                                # The RAG tool already includes source info in its answer
            
            # Determine tool_used for response
            if "order_lookup" in tools_used:
                tool_used = "order_lookup"
            elif "ticket_creator" in tools_used:
                tool_used = "ticket_creator"
            elif "update_address" in tools_used:
                tool_used = "update_address"
            elif "rag_knowledge_base" in tools_used:
                tool_used = "rag"
            elif "llm_reasoning" in tools_used:
                tool_used = "direct_llm"
            elif tools_used:
                tool_used = tools_used[0]
            else:
                tool_used = "direct_llm"

            logger.info(
                f"AGENT EXECUTION COMPLETE | session_id={session_id} | "
                f"answer_length={len(answer)} | tool_used={tool_used}"
            )

            # 4. Store interaction in memory
            await self.memory.add_message(session_id, Message(role="user", content=message))
            await self.memory.add_message(session_id, Message(role="assistant", content=answer))

            return {
                "session_id": session_id,
                "message": message,
                "answer": answer,
                "sources": sources,
                "tool_used": tool_used
            }

        except Exception as e:
            logger.error(
                f"AGENT ERROR | session_id={session_id} | "
                f"error_type={type(e).__name__} | error='{str(e)}'"
            )
            import traceback
            logger.error(f"AGENT TRACEBACK | session_id={session_id}\n{traceback.format_exc()}")
            
            return {
                "session_id": session_id,
                "message": message,
                "answer": "I encountered an error processing your request. Please try again or contact support.",
                "sources": [],
                "tool_used": "error",
                "error": str(e)
            }

    @staticmethod
    def _format_history(history: List[Message]) -> str:
        """Format conversation history as text."""
        if not history:
            return "No previous conversation."
        return "\n".join(f"{msg.role.title()}: {msg.content}" for msg in history)


# Global agent instance
_agent_instance: Optional[SupportAgent] = None


def get_support_agent() -> SupportAgent:
    """Get or create the global support agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SupportAgent()
    return _agent_instance


# Convenience function for backward compatibility
async def ask_agent(session_id: str, message: str, k: int = 5) -> Dict[str, Any]:
    """
    Convenience function to ask the support agent a question.
    
    Args:
        session_id: Session identifier
        message: User's question
        k: Number of RAG chunks (ignored, agent decides)
        
    Returns:
        Dictionary with answer and metadata
    """
    agent = get_support_agent()
    return await agent.process_query(session_id, message, k)


