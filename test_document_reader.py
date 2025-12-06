# test_document_reader.py
# Test if DocumentReader can read AutoCrit RTF files

from pathlib import Path
from src.libriscribe.utils.document_reader import DocumentReader

autocrit_folder = Path("Autocrit")

if autocrit_folder.exists():
    print(f"Testing DocumentReader on: {autocrit_folder}\n")
    
    reader = DocumentReader()
    documents = reader.read_folder(autocrit_folder)
    
    print(f"✓ Read {len(documents)} documents:\n")
    
    for filename, content in documents.items():
        print(f"  • {filename}")
        print(f"    - Size: {len(content)} chars")
        print(f"    - Preview: {content[:200]}...")
        print()
    
else:
    print(f"Autocrit folder not found: {autocrit_folder}")
