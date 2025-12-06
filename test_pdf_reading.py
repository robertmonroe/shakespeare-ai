# test_pdf_reading.py
# Test if we can read Scorpio.pdf including any images

from pathlib import Path
from src.libriscribe.utils.document_reader import DocumentReader

pdf_path = Path("Autocrit/Scorpio.pdf")

if pdf_path.exists():
    print(f"Testing PDF reading: {pdf_path}\n")
    
    reader = DocumentReader()
    content = reader.read_document(pdf_path)
    
    if content:
        print(f"✓ Successfully read PDF")
        print(f"  Total characters: {len(content)}")
        print(f"\nFirst 1000 characters:")
        print("-" * 60)
        print(content[:1000])
        print("-" * 60)
        
        # Check if it has meaningful content
        if len(content) > 100:
            print("\n✅ PDF reading works!")
            print("Note: PyPDF2 extracts text but NOT images from PDFs")
            print("For image analysis in PDFs, we'd need a different library")
        else:
            print("\n⚠️ PDF might be image-based or encrypted")
    else:
        print("❌ Failed to read PDF")
else:
    print(f"PDF not found: {pdf_path}")
