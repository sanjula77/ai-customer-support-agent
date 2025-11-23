import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Default file paths (relative to project root)
DEFAULT_EMBEDDINGS_FILE = "data/embeddings.npy"
DEFAULT_METADATA_FILE = "data/metadata.jsonl"
DEFAULT_FAISS_INDEX_FILE = "data/faiss_index.bin"
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_project_root() -> Path:
    """Get the project root directory (3 levels up from this file)."""
    return Path(__file__).parent.parent.parent


class VectorStore:
    """
    Vector store for semantic search using FAISS and SentenceTransformers.
    """
    
    def __init__(
        self,
        embeddings_file: str = DEFAULT_EMBEDDINGS_FILE,
        metadata_file: str = DEFAULT_METADATA_FILE,
        index_file: str = DEFAULT_FAISS_INDEX_FILE,
        model_name: str = DEFAULT_MODEL_NAME
    ):
        """
        Initialize the vector store.
        
        Args:
            embeddings_file: Path to embeddings .npy file
            metadata_file: Path to metadata JSONL file
            index_file: Path to FAISS index file
            model_name: Name of the SentenceTransformer model
        """
        self.embeddings_file = Path(embeddings_file)
        if not self.embeddings_file.is_absolute():
            self.embeddings_file = get_project_root() / embeddings_file
        
        self.metadata_file = Path(metadata_file)
        if not self.metadata_file.is_absolute():
            self.metadata_file = get_project_root() / metadata_file
        
        self.index_file = Path(index_file)
        if not self.index_file.is_absolute():
            self.index_file = get_project_root() / index_file
        
        self.model_name = model_name
        self.model = None
        self.index = None
        self.metadata = None
        self.embeddings = None
    
    def load_model(self):
        """Load the SentenceTransformer model."""
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise RuntimeError(f"Failed to load model '{self.model_name}': {e}")
        return self.model
    
    def load_embeddings(self) -> np.ndarray:
        """Load embeddings from file."""
        if self.embeddings is None:
            if not self.embeddings_file.exists():
                raise FileNotFoundError(f"Embeddings file not found: {self.embeddings_file}")
            try:
                self.embeddings = np.load(self.embeddings_file).astype(np.float32)
            except Exception as e:
                raise IOError(f"Error loading embeddings: {e}")
        return self.embeddings
    
    def load_metadata(self) -> List[Dict]:
        """Load metadata from JSONL file."""
        if self.metadata is None:
            if not self.metadata_file.exists():
                raise FileNotFoundError(f"Metadata file not found: {self.metadata_file}")
            try:
                self.metadata = []
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.metadata.append(json.loads(line))
            except Exception as e:
                raise IOError(f"Error loading metadata: {e}")
        return self.metadata
    
    def build_index(self, use_gpu: bool = False, index_type: str = "flat") -> faiss.Index:
        """
        Build FAISS index from embeddings.
        
        Args:
            use_gpu: Whether to use GPU (requires faiss-gpu)
            index_type: Type of index ("flat" for exact search, "ivf" for approximate)
            
        Returns:
            FAISS index
        """
        vectors = self.load_embeddings()
        dim = vectors.shape[1]
        
        if index_type == "flat":
            # Exact search - IndexFlatL2 for L2 distance
            index = faiss.IndexFlatL2(dim)
        elif index_type == "ivf":
            # Approximate search - faster for large datasets
            nlist = min(100, len(vectors) // 10)  # Number of clusters
            quantizer = faiss.IndexFlatL2(dim)
            index = faiss.IndexIVFFlat(quantizer, dim, nlist)
            index.train(vectors)
        else:
            raise ValueError(f"Unknown index type: {index_type}")
        
        if use_gpu:
            try:
                res = faiss.StandardGpuResources()
                index = faiss.index_cpu_to_gpu(res, 0, index)
            except Exception as e:
                print(f"⚠️  Warning: GPU not available, using CPU: {e}")
        
        index.add(vectors)
        
        self.index = index
        return index
    
    def load_index(self) -> faiss.Index:
        """Load FAISS index from file."""
        if self.index is None:
            if not self.index_file.exists():
                raise FileNotFoundError(f"Index file not found: {self.index_file}. Run build_index() first.")
            try:
                self.index = faiss.read_index(str(self.index_file))
            except Exception as e:
                raise IOError(f"Error loading index: {e}")
        return self.index
    
    def save_index(self, index: Optional[faiss.Index] = None):
        """Save FAISS index to file."""
        if index is None:
            index = self.index
        if index is None:
            raise ValueError("No index to save. Build or load index first.")
        
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle GPU index
        if hasattr(index, 'index'):
            # GPU index - convert to CPU first
            index = faiss.index_gpu_to_cpu(index)
        
        try:
            faiss.write_index(index, str(self.index_file))
        except Exception as e:
            raise IOError(f"Error saving index: {e}")
    
    def search(
        self,
        query: str,
        k: int = 5,
        return_distances: bool = True
    ) -> List[Dict]:
        """
        Search for similar chunks.
        
        Args:
            query: Query text
            k: Number of results to return
            return_distances: Whether to include distance scores
            
        Returns:
            List of result dictionaries with content and metadata
        """
        # Load model and encode query
        model = self.load_model()
        query_vector = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        query_vector = query_vector.astype(np.float32).reshape(1, -1)
        
        # Load index and search
        index = self.load_index()
        distances, indices = index.search(query_vector, k)
        
        # Load metadata
        metadata = self.load_metadata()
        
        # Build results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(metadata):
                continue
            
            chunk = metadata[idx].copy()
            result = {
                "content": chunk.get("content") or chunk.get("text", ""),
                "title": chunk.get("title", ""),
                "metadata": chunk.get("metadata", {}),
                "rank": i + 1
            }
            
            if return_distances:
                result["distance"] = float(distances[0][i])
                result["score"] = 1.0 / (1.0 + distances[0][i])  # Convert distance to similarity score
            
            results.append(result)
        
        return results


def build_faiss_index(
    embeddings_file: str = DEFAULT_EMBEDDINGS_FILE,
    metadata_file: str = DEFAULT_METADATA_FILE,
    index_file: str = DEFAULT_FAISS_INDEX_FILE,
    index_type: str = "flat",
    use_gpu: bool = False,
    verbose: bool = True
) -> Path:
    """
    Build and save FAISS index from embeddings.
    
    Args:
        embeddings_file: Path to embeddings file
        metadata_file: Path to metadata file
        index_file: Path to save index file
        index_type: Type of index ("flat" or "ivf")
        use_gpu: Whether to use GPU
        verbose: If True, print progress information
        
    Returns:
        Path to saved index file
    """
    if verbose:
        print("=" * 70)
        print("Building FAISS Index")
        print("=" * 70)
    
    store = VectorStore(embeddings_file, metadata_file, index_file)
    
    if verbose:
        print(f"\n📌 Loading embeddings from: {embeddings_file}")
    vectors = store.load_embeddings()
    
    if verbose:
        print(f"📐 Vector dimension: {vectors.shape[1]}")
        print(f"📊 Total vectors: {vectors.shape[0]}")
        print(f"⚙️  Building FAISS index (type: {index_type})...")
    
    index = store.build_index(use_gpu=use_gpu, index_type=index_type)
    
    if verbose:
        print(f"💾 Saving index to: {index_file}")
    store.save_index(index)
    
    if verbose:
        print(f"✅ FAISS index created!")
        print(f"📁 Saved to: {store.index_file}")
        print(f"🔢 Total vectors stored: {index.ntotal}")
        print("=" * 70)
    
    return store.index_file


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build FAISS index for vector search")
    parser.add_argument("--embeddings", default=DEFAULT_EMBEDDINGS_FILE, help="Path to embeddings file")
    parser.add_argument("--metadata", default=DEFAULT_METADATA_FILE, help="Path to metadata file")
    parser.add_argument("--index", default=DEFAULT_FAISS_INDEX_FILE, help="Path to output index file")
    parser.add_argument("--type", choices=["flat", "ivf"], default="flat", help="Index type")
    parser.add_argument("--gpu", action="store_true", help="Use GPU (requires faiss-gpu)")
    parser.add_argument("--test", action="store_true", help="Run test search after building")
    
    args = parser.parse_args()
    
    try:
        # Build index
        build_faiss_index(
            embeddings_file=args.embeddings,
            metadata_file=args.metadata,
            index_file=args.index,
            index_type=args.type,
            use_gpu=args.gpu,
            verbose=True
        )
        
        # Test search if requested
        if args.test:
            print("\n" + "=" * 70)
            print("Test Search")
            print("=" * 70)
            
            store = VectorStore(args.embeddings, args.metadata, args.index)
            query = "How to reset NH-Hub X1?"
            
            print(f"\n🔍 Query: {query}")
            results = store.search(query, k=3)
            
            print(f"\n📋 Top {len(results)} results:")
            for result in results:
                print(f"\n{'='*70}")
                print(f"Rank #{result['rank']}")
                if 'score' in result:
                    print(f"Score: {result['score']:.4f} (Distance: {result['distance']:.4f})")
                print(f"Title: {result['title']}")
                print(f"Content: {result['content'][:200]}..." if len(result['content']) > 200 else f"Content: {result['content']}")
                if result['metadata']:
                    print(f"Metadata: {result['metadata']}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
