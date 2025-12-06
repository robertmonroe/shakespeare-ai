import sys
sys.path.insert(0, r'c:\Users\3dmax\Libriscribe\src')

from pathlib import Path
from libriscribe.agents.decision_agent import DecisionAgent
from libriscribe.utils.llm_client import LLMClient

# Find the most recent review file
review_files = list(Path(r"c:\Users\3dmax\Libriscribe\projects\pig 3\reviews").glob("chapter_1_review*.md"))
if not review_files:
    print("No review files found!")
    exit(1)

latest_review = max(review_files, key=lambda p: p.stat().st_mtime)
print(f"Testing with: {latest_review.name}\n")

review_text = latest_review.read_text(encoding='utf-8')
print(f"Review file size: {len(review_text)} chars\n")

# Create Decision Agent
llm_client = LLMClient('google_ai_studio')
agent = DecisionAgent(llm_client)

# Test section extraction
sections = agent._extract_all_sections(review_text)

print("=== SECTION EXTRACTION TEST ===\n")
for section_name, content in sections.items():
    if content:
        print(f"✅ {section_name}: {len(content)} chars")
        print(f"   Preview: {content[:100]}...\n")
    else:
        print(f"❌ {section_name}: EMPTY\n")

total_found = sum(1 for c in sections.values() if c)
print(f"\n{'='*50}")
print(f"Result: {total_found}/6 sections extracted")
print("✅ TEST PASSED" if total_found >= 5 else "❌ TEST FAILED")
