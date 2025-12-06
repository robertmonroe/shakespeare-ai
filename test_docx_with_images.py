# test_docx_with_images.py
# Test if DocumentReader can extract text AND images from DOCX

from pathlib import Path
from src.libriscribe.utils.document_reader import DocumentReader

# Test with AutoCrit DOCX files (if you have any)
autocrit_folder = Path("Autocrit")

reader = DocumentReader()

print("Testing DOCX reading with image extraction...\n")

# Look for DOCX files
docx_files = list(autocrit_folder.glob("*.docx"))

if docx_files:
    for docx_file in docx_files:
        print(f"Reading: {docx_file.name}")
        content = reader.read_document(docx_file)
        
        if content:
            print(f"  ✓ Extracted {len(content)} chars")
            
            # Check if images were found
            if "--- EMBEDDED IMAGES ---" in content:
                print(f"  ✓ Images found and analyzed!")
                # Show image descriptions
                image_section = content.split("--- EMBEDDED IMAGES ---")[1]
                print(f"  Image descriptions:\n{image_section[:500]}...")
            else:
                print(f"  • No images found in this document")
            
            print()
else:
    print("No DOCX files found in Autocrit folder")
    print("\nTesting with RTF files instead...")
    
    rtf_files = list(autocrit_folder.glob("*.rtf"))
    for rtf_file in rtf_files[:1]:  # Just test one
        print(f"\nReading: {rtf_file.name}")
        content = reader.read_document(rtf_file)
        if content:
            print(f"  ✓ Extracted {len(content)} chars")
            print(f"  Preview: {content[:300]}...")
