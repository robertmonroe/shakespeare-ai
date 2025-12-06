import sys
sys.path.insert(0, r'c:\Users\3dmax\Libriscribe\src')

from pathlib import Path

# Read the actual review
review_path = Path(r"c:\Users\3dmax\Libriscribe\projects\Inanna 4\reviews\chapter_5_review.md")
review_text = review_path.read_text(encoding='utf-8')

print("=== REVIEW FILE CONTENT (first 500 chars) ===")
print(review_text[:500])
print("\n=== ALL HEADERS IN REVIEW ===")
for line in review_text.split('\n'):
    if line.startswith('##'):
        print(f"Found: '{line}'")

print("\n=== TESTING PATTERN MATCHING ===")

sections = {
    'Internal Consistency': '',
    'Clarity': '',
    'Plot Holes': '',
    'Redundancy': '',
    'Flow and Transitions': '',
    'Actionable Fixes': ''
}

for section_name in sections.keys():
    patterns = [
        f"## {section_name}",
        f"## 1. {section_name}",
        f"## 2. {section_name}",
        f"## 3. {section_name}",
        f"## 4. {section_name}",
        f"## 5. {section_name}",
        f"## 6. {section_name}",
    ]
    
    found = False
    for pattern in patterns:
        if pattern in review_text:
            start = review_text.find(pattern) + len(pattern)
            next_section = len(review_text)
            for next_pattern in ["## ", "### ", "\n**"]:
                pos = review_text.find(next_pattern, start + 1)
                if pos != -1 and pos < next_section:
                    next_section = pos
            
            content = review_text[start:next_section].strip()
            sections[section_name] = content
            print(f"✓ {section_name}: Found with pattern '{pattern}' ({len(content)} chars)")
            found = True
            break
    
    if not found:
        print(f"✗ {section_name}: NOT FOUND")

print("\n=== SECTION LENGTHS ===")
for name, content in sections.items():
    print(f"{name}: {len(content)} chars")
