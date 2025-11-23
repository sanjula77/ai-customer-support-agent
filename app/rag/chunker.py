import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Handle import for both module and direct execution
try:
    from .loader import load_markdown_files
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from loader import load_markdown_files

# Default output file path (relative to project root)
DEFAULT_OUTPUT_FILE = "data/rag_kb_chunks.jsonl"


def is_meaningful_content(content: str) -> bool:
    """
    Check if content has meaningful text (not just separators or whitespace).
    
    Args:
        content: Content string to check
        
    Returns:
        True if content has meaningful text, False otherwise
    """
    if not content:
        return False
    
    # Remove horizontal rules, empty lines, and whitespace
    cleaned = re.sub(r'^---+$', '', content, flags=re.MULTILINE)  # Remove --- lines
    cleaned = re.sub(r'^\s*$', '', cleaned, flags=re.MULTILINE)  # Remove empty lines
    cleaned = cleaned.strip()
    
    # Check if there's any non-whitespace content left
    return len(cleaned) >= 10  # At least 10 characters of actual content


def extract_sections(content: str) -> List[Dict[str, str]]:
    """
    Extract sections from markdown content by detecting headings.
    Splits on H1 (#) and H2 (##) headings only. H3 (###) and deeper are kept as part of the section.
    Filters out sections that only contain separators or whitespace.
    
    Args:
        content: Markdown content string
        
    Returns:
        List of dictionaries with 'heading' and 'content' keys
    """
    sections = []
    
    # Pattern to match only H1 and H2 headings (not H3+)
    # H3 and deeper headings are treated as part of the section content
    heading_pattern = r'^(#{1,2})\s+(.+)$'
    
    lines = content.split('\n')
    current_heading = None
    current_content = []
    
    for line in lines:
        match = re.match(heading_pattern, line)
        if match:
            # Save previous section if it has meaningful content
            if current_heading is not None:
                section_content = '\n'.join(current_content).strip()
                if is_meaningful_content(section_content):
                    sections.append({
                        'heading': current_heading,
                        'content': section_content
                    })
                # If section is empty, skip it (handles cases where H1 is just a title)
            
            # Start new section
            heading_level = len(match.group(1))
            current_heading = match.group(2).strip()
            current_content = []
        else:
            # Include all non-H1/H2 lines in current section (including H3+ headings)
            current_content.append(line)
    
    # Add the last section if it has meaningful content
    if current_heading is not None:
        section_content = '\n'.join(current_content).strip()
        if is_meaningful_content(section_content):
            sections.append({
                'heading': current_heading,
                'content': section_content
            })
    
    # If no headings found, treat entire content as one section
    if not sections and content.strip():
        cleaned_content = content.strip()
        if is_meaningful_content(cleaned_content):
            sections.append({
                'heading': 'Introduction',
                'content': cleaned_content
            })
    
    return sections


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    verbose: bool = False
) -> List[Dict]:
    """
    Split documents into chunks using LangChain RecursiveCharacterTextSplitter.
    
    Args:
        documents: List of document dictionaries from load_markdown_files()
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
        verbose: If True, print progress information
        
    Returns:
        List of chunk dictionaries with title, content, and metadata
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []
    stats = {
        'total_docs': len(documents),
        'total_sections': 0,
        'total_chunks': 0,
        'docs_without_sections': 0
    }
    
    for doc_idx, doc in enumerate(documents, 1):
        if verbose:
            print(f"Processing document {doc_idx}/{stats['total_docs']}: {doc['filename']}")
        
        try:
            # Extract sections from document
            sections = extract_sections(doc['content'])
            
            if not sections:
                if verbose:
                    print(f"  ⚠️  Warning: No sections found in {doc['filename']}")
                stats['docs_without_sections'] += 1
                continue
            
            stats['total_sections'] += len(sections)
            
            # Process each section
            for section in sections:
                heading = section['heading']
                content = section['content']
                
                # Double-check content is meaningful (should already be filtered, but safety check)
                if not is_meaningful_content(content):
                    if verbose:
                        print(f"  ⚠️  Skipping empty section: {heading}")
                    continue
                
                # Split section into chunks
                try:
                    chunks = text_splitter.split_text(content)
                    
                    for chunk_idx, chunk in enumerate(chunks, 1):
                        if not chunk.strip():
                            continue
                        
                        chunk_metadata = {
                            "source": doc['filename'],
                            "category": doc['category'],
                            "section": heading,
                            "chunk_index": chunk_idx,
                            "total_chunks_in_section": len(chunks)
                        }
                        
                        # Add filepath if available
                        if 'filepath' in doc:
                            chunk_metadata['filepath'] = doc['filepath']
                        
                        all_chunks.append({
                            "title": f"{doc['filename']} - {heading}",
                            "content": chunk.strip(),
                            "metadata": chunk_metadata
                        })
                        stats['total_chunks'] += 1
                        
                except Exception as e:
                    if verbose:
                        print(f"  ⚠️  Error chunking section '{heading}': {e}")
                    continue
                    
        except Exception as e:
            if verbose:
                print(f"  ⚠️  Error processing {doc['filename']}: {e}")
            continue
    
    if verbose:
        print(f"\n📊 Chunking Statistics:")
        print(f"  - Documents processed: {stats['total_docs']}")
        print(f"  - Sections extracted: {stats['total_sections']}")
        print(f"  - Total chunks created: {stats['total_chunks']}")
        print(f"  - Documents without sections: {stats['docs_without_sections']}")
        if stats['total_chunks'] > 0:
            avg_chunks_per_doc = stats['total_chunks'] / stats['total_docs']
            print(f"  - Average chunks per document: {avg_chunks_per_doc:.1f}")
    
    return all_chunks


def save_chunks_to_jsonl(chunks: List[Dict], output_file: str = DEFAULT_OUTPUT_FILE) -> Path:
    """
    Save chunks to a JSONL file.
    
    Args:
        chunks: List of chunk dictionaries
        output_file: Path to output file (relative or absolute)
        
    Returns:
        Path object of the saved file
    """
    # Convert to absolute path if relative
    output_path = Path(output_file)
    if not output_path.is_absolute():
        # Make relative to project root (two levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        output_path = project_root / output_file
    
    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write chunks to JSONL file
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    
    return output_path


if __name__ == "__main__":
    print("=" * 70)
    print("Document Chunking Tool")
    print("=" * 70)
    
    # Load documents
    print("\n📂 Loading documents...")
    documents = load_markdown_files(verbose=True)
    
    if not documents:
        print("\n⚠️  No documents loaded. Exiting.")
        sys.exit(1)
    
    # Chunk documents
    print(f"\n✂️  Chunking {len(documents)} documents...")
    chunks = chunk_documents(documents, chunk_size=500, chunk_overlap=50, verbose=True)
    
    if not chunks:
        print("\n⚠️  No chunks created. Exiting.")
        sys.exit(1)
    
    # Save chunks
    print(f"\n💾 Saving chunks to file...")
    output_path = save_chunks_to_jsonl(chunks, DEFAULT_OUTPUT_FILE)
    
    print(f"\n✅ Successfully saved {len(chunks)} chunks to:")
    print(f"   {output_path}")
    print("=" * 70)
