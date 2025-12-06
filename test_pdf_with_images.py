# test_pdf_with_images.py
# Test if we can read Scorpio.pdf with image analysis using Poppler

from pathlib import Path
from src.libriscribe.utils.document_reader import DocumentReader

pdf_path = Path("projects/pig 10/Autocrit/Scorpio.pdf")

if pdf_path.exists():
    print(f"Testing PDF with image analysis: {pdf_path}\n")
    
    reader = DocumentReader()
    content = reader.read_document(pdf_path)
    
    if content:
        print(f"✓ Successfully read PDF")
        print(f"  Total characters: {len(content)}")
        
        # Check if images were analyzed
        if "--- EMBEDDED IMAGES/CHARTS ---" in content:
            print(f"\n✅ IMAGE ANALYSIS WORKED!")
            print("\nImage/Chart descriptions found:")
            print("-" * 60)
            image_section = content.split("--- EMBEDDED IMAGES/CHARTS ---")[1]
            print(image_section[:1000])
            print("-" * 60)
        else:
            print(f"\n⚠️ No images/charts found (or Poppler not working)")
            print("First 500 chars of content:")
            print(content[:500])
    else:
        print("❌ Failed to read PDF")
else:
    print(f"PDF not found: {pdf_path}")
