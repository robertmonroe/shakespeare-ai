import sys
sys.path.insert(0, r'c:\Users\3dmax\Libriscribe\src')

from pathlib import Path

# Read the actual review
review_path = Path(r"c:\Users\3dmax\Libriscribe\projects\Inanna 4\reviews\chapter_5_review.md")
review_text = review_path.read_text(encoding='utf-8')

# Find Internal Consistency section
pattern = "## 1. Internal Consistency"
start = review_text.find(pattern)
print(f"Pattern found at position: {start}")
print(f"Pattern: '{pattern}'")
print(f"Content after pattern (500 chars):")
print(review_text[start:start+500])

# Find next ##
content_start = start + len(pattern)
next_section = review_text.find("## ", content_start + 1)
print(f"\nNext '## ' found at position: {next_section}")
print(f"Distance: {next_section - content_start} chars")

if next_section != -1:
    content = review_text[content_start:next_section]
    print(f"\nExtracted content length: {len(content)} chars")
    print(f"Extracted content (first 300 chars):")
    print(content[:300])
