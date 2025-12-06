# Test script to verify JSON extraction fix
import sys
sys.path.insert(0, 'src')

from libriscribe.utils.file_utils import extract_json_from_markdown

# Test 1: JSON object (should work before and after fix)
test_object = """
Here's the data:
```json
{"name": "Inanna", "age": "immortal"}
```
"""

# Test 2: JSON array (this is what was failing)
test_array = """
Here are the characters:
```json
[
  {"name": "Inanna", "role": "protagonist"},
  {"name": "Enkidu", "role": "deuteragonist"}
]
```
"""

print("Testing JSON object extraction...")
result1 = extract_json_from_markdown(test_object)
print(f"Result: {result1}")
print(f"Type: {type(result1)}")
print()

print("Testing JSON array extraction...")
result2 = extract_json_from_markdown(test_array)
print(f"Result: {result2}")
print(f"Type: {type(result2)}")
print(f"Is list: {isinstance(result2, list)}")
