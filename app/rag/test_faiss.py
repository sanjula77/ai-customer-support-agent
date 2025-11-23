"""
Test script for FAISS vector search functionality.

This script tests the vector store search capabilities with various queries.
It can be used to verify that embeddings, index, and metadata are working correctly.
"""

import sys
from pathlib import Path
from typing import List, Dict

# Import VectorStore class for proper testing
try:
    from .vector_store import VectorStore, DEFAULT_EMBEDDINGS_FILE, DEFAULT_METADATA_FILE, DEFAULT_FAISS_INDEX_FILE
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from vector_store import VectorStore, DEFAULT_EMBEDDINGS_FILE, DEFAULT_METADATA_FILE, DEFAULT_FAISS_INDEX_FILE


# Test queries covering different categories
TEST_QUERIES = [
    # Product setup and troubleshooting
    "How do I reset my smart hub?",
    "Camera night vision not working",
    "How to pair my smart bulb?",
    
    # Policy questions
    "What is your refund policy?",
    "How long is the warranty?",
    "What is your privacy policy?",
    
    # Product information
    "What are the specifications of NH-Cam Pro 360?",
    "How do I install the smart lock?",
    "What devices are compatible with NH-Hub X1?",
    
    # Troubleshooting
    "My device keeps disconnecting from WiFi",
    "App crashes when I try to open it",
    "Firmware update failed",
    
    # General questions
    "How to contact customer support?",
    "What payment methods do you accept?",
]


def test_single_query(store: VectorStore, query: str, k: int = 5, verbose: bool = True) -> List[Dict]:
    """
    Test a single query and display results.
    
    Args:
        store: VectorStore instance
        query: Query string
        k: Number of results to return
        verbose: If True, print results
        
    Returns:
        List of search results
    """
    try:
        results = store.search(query, k=k, return_distances=True)
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔍 Query: {query}")
            print(f"{'='*70}")
            
            if not results:
                print("⚠️  No results found!")
                return results
            
            print(f"\n📋 Top {len(results)} results:\n")
            
            for result in results:
                print(f"Rank #{result['rank']}")
                if 'score' in result:
                    print(f"  Score: {result['score']:.4f} (Distance: {result['distance']:.4f})")
                print(f"  Title: {result.get('title', 'N/A')}")
                
                # Display content (truncated if long)
                content = result['content']
                if len(content) > 300:
                    content = content[:300] + "..."
                content = content.replace("\n", " ").strip()
                print(f"  Content: {content}")
                
                # Display metadata if available
                if result.get('metadata'):
                    meta = result['metadata']
                    if 'category' in meta:
                        print(f"  Category: {meta['category']}")
                    if 'source' in meta:
                        print(f"  Source: {meta['source']}")
                    if 'section' in meta:
                        print(f"  Section: {meta['section']}")
                
                print()
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"❌ Error searching for '{query}': {e}")
        return []


def test_batch_queries(store: VectorStore, queries: List[str], k: int = 3, verbose: bool = True):
    """
    Test multiple queries and provide summary statistics.
    
    Args:
        store: VectorStore instance
        queries: List of query strings
        k: Number of results per query
        verbose: If True, print detailed results
    """
    print("=" * 70)
    print("Batch Query Testing")
    print("=" * 70)
    print(f"Testing {len(queries)} queries...\n")
    
    results_summary = {
        'total_queries': len(queries),
        'successful_queries': 0,
        'failed_queries': 0,
        'total_results': 0,
        'avg_score': 0.0,
        'min_score': 1.0,
        'max_score': 0.0
    }
    
    all_scores = []
    
    for i, query in enumerate(queries, 1):
        if verbose:
            print(f"\n[{i}/{len(queries)}] ", end="")
        
        results = test_single_query(store, query, k=k, verbose=verbose)
        
        if results:
            results_summary['successful_queries'] += 1
            results_summary['total_results'] += len(results)
            
            for result in results:
                if 'score' in result:
                    score = result['score']
                    all_scores.append(score)
                    results_summary['min_score'] = min(results_summary['min_score'], score)
                    results_summary['max_score'] = max(results_summary['max_score'], score)
        else:
            results_summary['failed_queries'] += 1
    
    # Calculate average score
    if all_scores:
        results_summary['avg_score'] = sum(all_scores) / len(all_scores)
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total queries: {results_summary['total_queries']}")
    print(f"Successful: {results_summary['successful_queries']}")
    print(f"Failed: {results_summary['failed_queries']}")
    print(f"Total results: {results_summary['total_results']}")
    if all_scores:
        print(f"Average score: {results_summary['avg_score']:.4f}")
        print(f"Min score: {results_summary['min_score']:.4f}")
        print(f"Max score: {results_summary['max_score']:.4f}")
    print("=" * 70)
    
    return results_summary


def test_vector_store_initialization(
    embeddings_file: str = DEFAULT_EMBEDDINGS_FILE,
    metadata_file: str = DEFAULT_METADATA_FILE,
    index_file: str = DEFAULT_FAISS_INDEX_FILE
) -> VectorStore:
    """
    Test VectorStore initialization and file loading.
    
    Args:
        embeddings_file: Path to embeddings file
        metadata_file: Path to metadata file
        index_file: Path to index file
        
    Returns:
        Initialized VectorStore instance
    """
    print("=" * 70)
    print("VectorStore Initialization Test")
    print("=" * 70)
    
    try:
        print(f"\n📂 Initializing VectorStore...")
        print(f"   Embeddings: {embeddings_file}")
        print(f"   Metadata: {metadata_file}")
        print(f"   Index: {index_file}")
        
        store = VectorStore(embeddings_file, metadata_file, index_file)
        
        # Test loading components
        print("\n📌 Testing component loading...")
        
        print("   Loading embeddings...", end=" ")
        embeddings = store.load_embeddings()
        print(f"✅ Shape: {embeddings.shape}")
        
        print("   Loading metadata...", end=" ")
        metadata = store.load_metadata()
        print(f"✅ {len(metadata)} chunks")
        
        print("   Loading index...", end=" ")
        index = store.load_index()
        print(f"✅ {index.ntotal} vectors")
        
        print("   Loading model...", end=" ")
        model = store.load_model()
        print(f"✅ {store.model_name}")
        
        print("\n✅ VectorStore initialized successfully!")
        print("=" * 70)
        
        return store
        
    except Exception as e:
        print(f"\n❌ Error initializing VectorStore: {e}")
        raise


def main():
    """Main test function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test FAISS vector search")
    parser.add_argument("--embeddings", default=DEFAULT_EMBEDDINGS_FILE, help="Path to embeddings file")
    parser.add_argument("--metadata", default=DEFAULT_METADATA_FILE, help="Path to metadata file")
    parser.add_argument("--index", default=DEFAULT_FAISS_INDEX_FILE, help="Path to index file")
    parser.add_argument("--query", type=str, help="Single query to test (if not provided, runs all test queries)")
    parser.add_argument("--k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output")
    
    args = parser.parse_args()
    
    try:
        # Initialize store
        store = test_vector_store_initialization(
            args.embeddings,
            args.metadata,
            args.index
        )
        
        # Run tests
        if args.query:
            # Single query test
            test_single_query(store, args.query, k=args.k, verbose=not args.quiet)
        else:
            # Batch test with default queries
            test_batch_queries(store, TEST_QUERIES, k=args.k, verbose=not args.quiet)
        
        print("\n✅ All tests completed!")
        
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Run chunker.py to create chunks")
        print("   2. Run embedder.py to generate embeddings")
        print("   3. Run vector_store.py to build the index")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
