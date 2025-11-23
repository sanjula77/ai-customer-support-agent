"""
Query Engine for RAG-based question answering.

This module provides a simple interface to query the RAG system.
It uses lazy initialization to avoid loading everything at import time.
"""

import sys
from pathlib import Path
from typing import Optional, Dict

# Handle imports
try:
    from .rag_chain import RAGChain
except ImportError:
    # Fallback: add parent directory to path
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    try:
        from app.rag.rag_chain import RAGChain
    except ImportError:
        # Last resort: try relative import
        sys.path.insert(0, str(Path(__file__).parent))
        from rag_chain import RAGChain


# Global RAG instance (lazy initialization)
_rag_instance: Optional[RAGChain] = None


def get_rag_instance(verbose: bool = False) -> RAGChain:
    """
    Get or create the RAG instance (singleton pattern).
    
    Args:
        verbose: If True, print initialization messages
        
    Returns:
        RAGChain instance
    """
    global _rag_instance
    
    if _rag_instance is None:
        try:
            _rag_instance = RAGChain(verbose=verbose)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAG chain: {e}")
    
    return _rag_instance


def ask_question(question: str, k: int = 5, verbose: bool = False) -> str:
    """
    Query the RAG system and return AI answer.
    
    Args:
        question: Question string
        k: Number of context chunks to retrieve
        verbose: If True, print debug information
        
    Returns:
        Answer string
        
    Raises:
        RuntimeError: If RAG chain fails to initialize or process query
    """
    try:
        rag = get_rag_instance(verbose=verbose)
        return rag.ask(question, k=k)
    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        if verbose:
            print(f"❌ {error_msg}")
        raise RuntimeError(error_msg) from e


def ask_question_with_sources(question: str, k: int = 5, verbose: bool = False) -> Dict:
    """
    Query the RAG system and return answer with source information.
    
    Args:
        question: Question string
        k: Number of context chunks to retrieve
        verbose: If True, print debug information
        
    Returns:
        Dictionary with 'answer', 'sources', and 'context' keys
        
    Raises:
        RuntimeError: If RAG chain fails to initialize or process query
    """
    try:
        rag = get_rag_instance(verbose=verbose)
        return rag.ask_with_sources(question, k=k)
    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        if verbose:
            print(f"❌ {error_msg}")
        raise RuntimeError(error_msg) from e


def reset_rag_instance():
    """
    Reset the global RAG instance (useful for testing or reinitialization).
    """
    global _rag_instance
    _rag_instance = None


# Quick test
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test RAG query engine")
    parser.add_argument("--question", "-q", type=str, default="How do I reset my NH-Hub X1?", help="Question to ask")
    parser.add_argument("--k", type=int, default=5, help="Number of context chunks")
    parser.add_argument("--sources", action="store_true", help="Include source information")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        print("=" * 70)
        print("RAG Query Engine Test")
        print("=" * 70)
        print(f"\nQuestion: {args.question}\n")
        
        if args.sources:
            result = ask_question_with_sources(args.question, k=args.k, verbose=args.verbose)
            print("Answer:")
            print(result['answer'])
            print("\n" + "=" * 70)
            print("Sources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"\n{i}. {source.get('title', 'N/A')}")
                print(f"   Score: {source.get('score', 0):.4f}")
                print(f"   Category: {source.get('category', 'N/A')}")
                print(f"   File: {source.get('source_file', 'N/A')}")
        else:
            answer = ask_question(args.question, k=args.k, verbose=args.verbose)
            print("Answer:")
            print(answer)
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
