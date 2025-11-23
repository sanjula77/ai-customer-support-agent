import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

# Default file paths (relative to project root)
DEFAULT_CHUNKS_FILE = "data/rag_kb_chunks.jsonl"
DEFAULT_EMBEDDINGS_OUTPUT = "data/embeddings.npy"
DEFAULT_METADATA_OUTPUT = "data/metadata.jsonl"
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_project_root() -> Path:
    """Get the project root directory (3 levels up from this file)."""
    return Path(__file__).parent.parent.parent


def load_chunks(chunks_file: str = DEFAULT_CHUNKS_FILE) -> List[Dict]:
    """
    Load chunks from JSONL file.
    
    Args:
        chunks_file: Path to chunks JSONL file (relative to project root or absolute)
        
    Returns:
        List of chunk dictionaries
    """
    chunks_path = Path(chunks_file)
    if not chunks_path.is_absolute():
        chunks_path = get_project_root() / chunks_file
    
    if not chunks_path.exists():
        raise FileNotFoundError(f"Chunks file not found: {chunks_path}")
    
    chunks = []
    try:
        with open(chunks_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    chunks.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Skipping invalid JSON on line {line_num}: {e}")
                    continue
    except Exception as e:
        raise IOError(f"Error reading chunks file: {e}")
    
    return chunks


def generate_embeddings(
    chunks_file: str = DEFAULT_CHUNKS_FILE,
    embeddings_output: str = DEFAULT_EMBEDDINGS_OUTPUT,
    metadata_output: str = DEFAULT_METADATA_OUTPUT,
    model_name: str = DEFAULT_MODEL_NAME,
    batch_size: int = 32,
    verbose: bool = True
) -> tuple[Path, Path]:
    """
    Generate embeddings for chunks and save to files.
    
    Args:
        chunks_file: Path to input chunks JSONL file
        embeddings_output: Path to output embeddings .npy file
        metadata_output: Path to output metadata JSONL file
        model_name: Name of the SentenceTransformer model to use
        batch_size: Batch size for encoding
        verbose: If True, print progress information
        
    Returns:
        Tuple of (embeddings_path, metadata_path)
    """
    if verbose:
        print("=" * 70)
        print("Embedding Generation")
        print("=" * 70)
    
    # Load chunks
    if verbose:
        print(f"\n📂 Loading chunks from: {chunks_file}")
    chunks = load_chunks(chunks_file)
    
    if not chunks:
        raise ValueError("No chunks found in file!")
    
    # Extract content (chunker.py uses "content" key, not "text")
    texts = []
    for i, chunk in enumerate(chunks, 1):
        if "content" in chunk:
            texts.append(chunk["content"])
        elif "text" in chunk:  # Fallback for old format
            texts.append(chunk["text"])
        else:
            raise KeyError(f"Chunk {i} missing 'content' or 'text' key. Available keys: {list(chunk.keys())}")
    
    if len(texts) != len(chunks):
        raise ValueError(f"Mismatch: {len(chunks)} chunks but {len(texts)} texts extracted")
    
    # Load model
    if verbose:
        print(f"📌 Loading embedding model: {model_name}...")
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to load model '{model_name}': {e}")
    
    # Generate embeddings
    if verbose:
        print(f"⚙️  Generating embeddings for {len(texts)} chunks...")
        print(f"   Batch size: {batch_size}")
    
    try:
        vectors = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=verbose,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for better cosine similarity
        )
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}")
    
    # Convert to float32 for efficiency
    vectors = vectors.astype(np.float32)
    
    if verbose:
        print(f"✅ Generated embeddings shape: {vectors.shape}")
        print(f"   Dimension: {vectors.shape[1]}")
    
    # Resolve output paths
    embeddings_path = Path(embeddings_output)
    if not embeddings_path.is_absolute():
        embeddings_path = get_project_root() / embeddings_output
    
    metadata_path = Path(metadata_output)
    if not metadata_path.is_absolute():
        metadata_path = get_project_root() / metadata_output
    
    # Create parent directories
    embeddings_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save embeddings
    if verbose:
        print(f"\n💾 Saving embeddings to: {embeddings_path}")
    try:
        np.save(embeddings_path, vectors)
    except Exception as e:
        raise IOError(f"Error saving embeddings: {e}")
    
    # Save metadata
    if verbose:
        print(f"💾 Saving metadata to: {metadata_path}")
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    except Exception as e:
        raise IOError(f"Error saving metadata: {e}")
    
    if verbose:
        print(f"\n✅ Successfully saved embeddings and metadata!")
        print(f"   Embeddings: {embeddings_path}")
        print(f"   Metadata: {metadata_path}")
        print("=" * 70)
    
    return embeddings_path, metadata_path


if __name__ == "__main__":
    try:
        generate_embeddings(verbose=True)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
