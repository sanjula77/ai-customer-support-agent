"""
RAG Chain implementation using LangChain, FAISS, and Google Gemini.

This module provides a RAG (Retrieval-Augmented Generation) chain that:
1. Retrieves relevant context from vector store
2. Uses Google Gemini LLM to generate answers based on retrieved context
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Workaround for LangChain 1.0+ compatibility
# ChatGoogleGenerativeAI tries to access langchain.verbose which doesn't exist
try:
    import langchain
    if not hasattr(langchain, 'verbose'):
        langchain.verbose = False
except ImportError:
    pass

# Import LangChain components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Import VectorStore for retrieval
try:
    from .vector_store import VectorStore, DEFAULT_EMBEDDINGS_FILE, DEFAULT_METADATA_FILE, DEFAULT_FAISS_INDEX_FILE
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from vector_store import VectorStore, DEFAULT_EMBEDDINGS_FILE, DEFAULT_METADATA_FILE, DEFAULT_FAISS_INDEX_FILE


class RAGChain:
    """
    RAG Chain for question answering using vector retrieval and LLM generation.
    """
    
    def __init__(
        self,
        embeddings_file: str = DEFAULT_EMBEDDINGS_FILE,
        metadata_file: str = DEFAULT_METADATA_FILE,
        index_file: str = DEFAULT_FAISS_INDEX_FILE,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
        verbose: bool = False
    ):
        """
        Initialize RAG Chain.
        
        Args:
            embeddings_file: Path to embeddings file
            metadata_file: Path to metadata file
            index_file: Path to FAISS index file
            model_name: Gemini model name
            temperature: LLM temperature (0.0-1.0)
            verbose: If True, print initialization messages
        """
        self.verbose = verbose
        
        # Check for API key
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Google API key not found! Please set GOOGLE_API_KEY or GEMINI_API_KEY "
                "in your .env file or environment variables."
            )
        
        if self.verbose:
            print("📄 Initializing RAG Chain...")
        
        # Initialize vector store for retrieval
        if self.verbose:
            print("📌 Loading vector store...")
        try:
            self.vector_store = VectorStore(embeddings_file, metadata_file, index_file)
            # Pre-load components
            self.vector_store.load_index()
            self.vector_store.load_metadata()
            self.vector_store.load_model()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize vector store: {e}")
        
        # Initialize Gemini LLM
        if self.verbose:
            print(f"⚙️  Loading Gemini LLM ({model_name})...")
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=api_key
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini LLM: {e}")
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful and professional AI assistant for NeuraHome Systems, "
                "a smart home technology company.\n\n"
                "Your role is to answer customer questions based on the provided context from "
                "product manuals, FAQs, troubleshooting guides, advanced settings guides, user management guides, "
                "edge cases documentation, and policy documents.\n\n"
                "Guidelines:\n"
                "- Answer questions clearly, concisely, and helpfully\n"
                "- Only use information from the provided context\n"
                "- Structure answers with clear steps, bullet points, or numbered lists when appropriate\n"
                "- Include specific details like model numbers, error codes, settings paths, or step-by-step instructions\n\n"
                "When the context contains the answer:\n"
                "- Provide a complete, detailed answer\n"
                "- Include all relevant information from the context\n"
                "- Reference specific sections or features when helpful\n"
                "- If troubleshooting, provide step-by-step solutions in order\n\n"
                "When the context doesn't fully answer the question:\n"
                "- Acknowledge what specific information is missing\n"
                "- Provide ANY related information from the context that might be helpful, even if not a direct answer\n"
                "- Suggest what the user might try based on similar information in the context\n"
                "- Mention that more detailed instructions may be available in the NeuraHome mobile app\n"
                "- Provide contact information for support: support@neurahome.com or +1-800-NEURA-HOME\n"
                "- Be helpful and constructive, not dismissive\n\n"
                "Additional guidelines:\n"
                "- Be friendly, professional, and empathetic\n"
                "- If asked about troubleshooting, provide comprehensive step-by-step solutions\n"
                "- Include relevant technical details, specifications, or error codes when available\n"
                "- If multiple solutions exist, present them in order from simplest to most complex\n"
                "- For setup questions, provide clear step-by-step instructions\n"
                "- For feature questions, explain how to access and use the feature\n"
                "- Always end with helpful next steps or support contact if the answer is incomplete\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        )
        
        # Create chain using LangChain 1.0+ API
        # In LangChain 1.0+, we use prompt | llm pattern instead of LLMChain
        self.chain = self.prompt_template | self.llm
        
        if self.verbose:
            print("✅ RAG Chain initialized successfully!")
    
    def retrieve(self, query: str, k: int = 5) -> str:
        """
        Retrieve relevant context chunks for a query.
        
        Args:
            query: Query string
            k: Number of chunks to retrieve
            
        Returns:
            Formatted context string with retrieved chunks
        """
        try:
            results = self.vector_store.search(query, k=k, return_distances=True)
            
            if not results:
                return "No relevant context found."
            
            # Format retrieved chunks
            chunks = []
            for i, result in enumerate(results, 1):
                content = result['content']
                title = result.get('title', '')
                metadata = result.get('metadata', {})
                
                # Build chunk header
                chunk_header = f"[Chunk {i}]"
                if title:
                    chunk_header += f" {title}"
                if metadata.get('section'):
                    chunk_header += f" - {metadata['section']}"
                
                chunks.append(f"{chunk_header}\n{content}")
            
            return "\n\n---\n\n".join(chunks)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error during retrieval: {e}")
            return f"Error retrieving context: {str(e)}"
    
    def ask(self, question: str, k: int = 5) -> str:
        """
        Ask a question and get an answer using RAG.
        
        Args:
            question: Question string
            k: Number of context chunks to retrieve
            
        Returns:
            Answer string
        """
        try:
            # Retrieve relevant context
            context = self.retrieve(question, k=k)
            
            # Generate answer using LLM (LangChain 1.0+ API)
            response = self.chain.invoke({"context": context, "question": question})
            # Extract content from response (handles both string and AIMessage)
            if hasattr(response, 'content'):
                answer = response.content
            else:
                answer = str(response)
            
            return answer.strip()
            
        except Exception as e:
            error_msg = f"Error generating answer: {str(e)}"
            if self.verbose:
                print(f"❌ {error_msg}")
            return error_msg
    
    def ask_with_sources(self, question: str, k: int = 5) -> Dict:
        """
        Ask a question and return answer with source information.
        
        Args:
            question: Question string
            k: Number of context chunks to retrieve
            
        Returns:
            Dictionary with 'answer', 'sources', and 'context' keys
        """
        try:
            # Retrieve relevant context with metadata
            results = self.vector_store.search(question, k=k, return_distances=True)
            
            if not results:
                return {
                    "answer": "I couldn't find relevant information to answer your question.",
                    "sources": [],
                    "context": ""
                }
            
            # Format context
            chunks = []
            sources = []
            for result in results:
                content = result['content']
                title = result.get('title', '')
                metadata = result.get('metadata', {})
                
                chunks.append(content)
                
                # Collect source information
                source_info = {
                    "title": title,
                    "score": result.get('score', 0.0),
                    "category": metadata.get('category', ''),
                    "source_file": metadata.get('source', ''),
                    "section": metadata.get('section', '')
                }
                sources.append(source_info)
            
            context = "\n\n---\n\n".join(chunks)
            
            # Generate answer (LangChain 1.0+ API)
            response = self.chain.invoke({"context": context, "question": question})
            # Extract content from response (handles both string and AIMessage)
            if hasattr(response, 'content'):
                answer = response.content
            else:
                answer = str(response)
            
            return {
                "answer": answer.strip(),
                "sources": sources,
                "context": context
            }
            
        except Exception as e:
            error_msg = f"Error generating answer: {str(e)}"
            if self.verbose:
                print(f"❌ {error_msg}")
            return {
                "answer": error_msg,
                "sources": [],
                "context": ""
            }
