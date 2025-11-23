import os
from pathlib import Path

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base")

def load_markdown_files(verbose=False):
    """
    Load all markdown files from knowledge base directories.
    
    Args:
        verbose (bool): If True, print detailed loading information
        
    Returns:
        list: List of dictionaries with keys: {"filename": str, "content": str, "category": str, "filepath": str}
    """
    documents = []
    # Fixed: Use correct folder names and include all categories
    categories = [
        "product_manuals",      # Fixed: was "manuals"
        "policy_documents",
        "troubleshooting_guides",
        "faqs"                  # Added: missing category
    ]
    
    if verbose:
        print(f"Knowledge base directory: {KB_DIR}")
        print(f"Looking for categories: {', '.join(categories)}\n")

    for category in categories:
        folder_path = os.path.join(KB_DIR, category)
        
        if not os.path.exists(folder_path):
            if verbose:
                print(f"⚠️  Warning: Category folder not found: {category}")
            continue
        
        if not os.path.isdir(folder_path):
            if verbose:
                print(f"⚠️  Warning: {category} is not a directory")
            continue

        files_loaded = 0
        try:
            for file in os.listdir(folder_path):
                if file.endswith(".md"):
                    filepath = os.path.join(folder_path, file)
                    
                    # Skip if it's a directory
                    if os.path.isdir(filepath):
                        continue
                    
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            
                            if not content:
                                if verbose:
                                    print(f"⚠️  Warning: Empty file skipped: {file}")
                                continue
                            
                            documents.append({
                                "filename": file,
                                "content": content,
                                "category": category,
                                "filepath": filepath
                            })
                            files_loaded += 1
                            
                    except UnicodeDecodeError as e:
                        if verbose:
                            print(f"⚠️  Error: Could not decode {file} - {e}")
                    except Exception as e:
                        if verbose:
                            print(f"⚠️  Error: Could not read {file} - {e}")
            
            if verbose:
                print(f"✓ Loaded {files_loaded} file(s) from {category}/")
                
        except PermissionError as e:
            if verbose:
                print(f"⚠️  Error: Permission denied for {category} - {e}")
        except Exception as e:
            if verbose:
                print(f"⚠️  Error: Could not access {category} - {e}")

    return documents

if __name__ == "__main__":
    print("=" * 60)
    print("Loading markdown files from knowledge base...")
    print("=" * 60)
    docs = load_markdown_files(verbose=True)
    print("\n" + "=" * 60)
    print(f"✓ Successfully loaded {len(docs)} documents total")
    print("=" * 60)
    
    if docs:
        print("\nLoaded documents by category:")
        categories_count = {}
        for doc in docs:
            cat = doc['category']
            categories_count[cat] = categories_count.get(cat, 0) + 1
        
        for category, count in sorted(categories_count.items()):
            print(f"  {category}: {count} file(s)")
        
        print("\nAll loaded files:")
        for doc in sorted(docs, key=lambda x: (x['category'], x['filename'])):
            print(f"  - {doc['category']}/{doc['filename']}")
    else:
        print("\n⚠️  No documents were loaded!")
