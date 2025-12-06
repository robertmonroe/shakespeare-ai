import sys
sys.path.insert(0, r'c:\Users\3dmax\Libriscribe\src')

from pathlib import Path

# Read Chapter 1 review
review_path = Path(r"c:\Users\3dmax\Libriscribe\projects\Inanna 4\reviews\chapter_1_review.md")
review_text = review_path.read_text(encoding='utf-8')

print("=== TESTING CHAPTER 1 EXTRACTION ===\n")

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
            # Find section content
            pattern_pos = review_text.find(pattern)
            start = pattern_pos + len(pattern)
            
            # Skip to end of current line
            newline_pos = review_text.find('\n', start)
            if newline_pos != -1:
                search_start = newline_pos + 1
            else:
                search_start = start
            
            # Find next MAIN section (##), not subsections (###)
            next_section = len(review_text)
            pos = review_text.find("\n## ", search_start)
            if pos != -1:
                next_section = pos
            
            content = review_text[start:next_section].strip()
            sections[section_name] = content
            print(f"✓ {section_name}: {len(content)} chars")
            if len(content) > 0:
                print(f"  Preview: {content[:80]}...")
            found = True
            break
    
    if not found:
        print(f"✗ {section_name}: NOT FOUND")

print("\n=== SUMMARY ===")
total = sum(1 for c in sections.values() if len(c) > 0)
print(f"Sections with content: {total}/6")
print("✅ SUCCESS!" if total >= 5 else "❌ FAILED")
