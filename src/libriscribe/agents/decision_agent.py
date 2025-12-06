# src/libriscribe/agents/decision_agent.py

from typing import List, Dict, Any
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from rich.console import Console
import json
import logging

console = Console()
logger = logging.getLogger(__name__)


class DecisionAgent(Agent):
    """Converts vague review fixes into specific, actionable tasks."""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("DecisionAgent", llm_client)
    
    def create_task_list(self, review_text: str) -> List[Dict[str, Any]]:
        """
        Create specific task list from review.
        
        Args:
            review_text: Full review markdown
            
        Returns:
            List of specific tasks grouped by review section
        """
        console.print("[cyan]📋 Analyzing review and creating task list...[/cyan]")
        
        # Extract all 6 sections
        sections = self._extract_all_sections(review_text)
        
        if not sections:
            console.print("[yellow]⚠️  No review sections found[/yellow]")
            return []
        
        console.print(f"[cyan]Found {len(sections)} review sections[/cyan]")
        
        # Create tasks from all sections
        all_tasks = []
        task_id = 1
        
        for section_name, section_content in sections.items():
            if not section_content.strip():
                console.print(f"[dim]Skipping {section_name} (empty)[/dim]")
                continue
            
            console.print(f"[cyan]Processing {section_name}... ({len(section_content)} chars)[/cyan]")
            
            # Debug: Show first 200 chars of section
            logger.debug(f"{section_name} content preview: {section_content[:200]}")
            
            # Create tasks for this section
            section_tasks = self._create_tasks_for_section(
                section_name,
                section_content,
                task_id
            )
            
            if section_tasks:
                console.print(f"[green]  ✓ Created {len(section_tasks)} tasks from {section_name}[/green]")
                all_tasks.extend(section_tasks)
                task_id += len(section_tasks)
            else:
                console.print(f"[yellow]  ⚠ No tasks created from {section_name}[/yellow]")
        
        if all_tasks:
            console.print(f"[green]✅ Created {len(all_tasks)} specific tasks from {len(sections)} sections[/green]")
        else:
            console.print("[yellow]⚠️  No tasks created from review[/yellow]")
        
        return all_tasks
    
    def _extract_all_sections(self, review_text: str) -> Dict[str, str]:
        """Extract all 6 review sections."""
        sections = {
            'Internal Consistency': '',
            'Clarity': '',
            'Plot Holes': '',
            'Redundancy': '',
            'Flow and Transitions': '',
            'Actionable Fixes': ''
        }
        
        # Extract each section
        for section_name in sections.keys():
            # Try different header formats (numbered and unnumbered)
            patterns = [
                f"## {section_name}",           # ## Internal Consistency
                f"## 1. {section_name}",        # ## 1. Internal Consistency
                f"## 2. {section_name}",        # ## 2. Clarity
                f"## 3. {section_name}",        # etc.
                f"## 4. {section_name}",
                f"## 5. {section_name}",
                f"## 6. {section_name}",
                f"**{section_name}**",          # **Internal Consistency**
                f"### {section_name}"           # ### Internal Consistency
            ]
            
            found = False
            for pattern in patterns:
                if pattern in review_text:
                    # Find section content
                    pattern_pos = review_text.find(pattern)
                    start = pattern_pos + len(pattern)
                    
                    # Skip to end of current line (to avoid matching the same header)
                    newline_pos = review_text.find('\n', start)
                    if newline_pos != -1:
                        search_start = newline_pos + 1
                    else:
                        search_start = start
                    
                    # Find next section or end
                    next_section = len(review_text)
                    # Only look for next main section (##), not subsections (###)
                    pos = review_text.find("\n## ", search_start)
                    if pos != -1:
                        next_section = pos
                    
                    sections[section_name] = review_text[start:next_section].strip()
                    found = True
                    logger.debug(f"Found {section_name} using pattern: {pattern}")
                    break
            
            if not found:
                logger.debug(f"Could not find {section_name} in review")
                # Show what headers ARE in the review
                logger.debug(f"Review headers: {[line for line in review_text.split('\\n') if line.startswith('##')][:10]}")
        
        return sections
    
    def _create_tasks_for_section(
        self,
        section_name: str,
        section_content: str,
        start_id: int
    ) -> List[Dict[str, Any]]:
        """Create tasks for a specific review section."""
        
        # Build prompt for this section
        prompt = self._build_section_task_prompt(section_name, section_content, start_id)
        
        try:
            response = self.llm_client.generate_content(prompt, max_tokens=16000, temperature=0.3)
            
            # Log response for debugging
            logger.debug(f"{section_name} LLM response length: {len(response)} chars")
            logger.debug(f"{section_name} LLM response preview: {response[:300]}")
            
            tasks = self._parse_task_list(response)
            
            if not tasks:
                logger.warning(f"No tasks parsed from {section_name} response")
                logger.warning(f"Full response: {response[:500]}")
            
            # Add section category to each task
            for task in tasks:
                task['category'] = section_name
            
            return tasks
            
        except Exception as e:
            logger.exception(f"Error creating tasks for {section_name}: {e}")
            console.print(f"[red]  ✗ Error: {str(e)[:100]}[/red]")
            return []
    
    def _build_section_task_prompt(
        self,
        section_name: str,
        section_content: str,
        start_id: int
    ) -> str:
        """Build prompt for creating tasks from a specific section."""
        return f"""
You are a task manager converting review feedback into specific, actionable tasks.

**Review Section**: {section_name}

**Section Content**:
{section_content}

**Your Task**:
Convert the issues in this section into specific, actionable tasks.

**Task Format**:
Each task must have:
1. **id**: Start from {start_id} and increment
2. **description**: Clear, specific description of what to do
3. **action**: One of: "replace", "delete", "insert_after", "insert_before"
4. **find_text**: Exact text to locate in the chapter (must be unique or provide context)
5. **context**: Which scene/paragraph to help locate the text
6. **Operation-specific fields**:
   - For "replace": **replace_with** (new text)
   - For "delete": **delete_scope** ("text_only" or "paragraph")
   - For "insert_after"/"insert_before": **insert_text** (text to add)
7. **expected_outcome**: How to verify completion
8. **priority**: "high", "medium", or "low"

**Guidelines**:
- **find_text** must be EXACT text from the chapter (copy it precisely)
- Make **find_text** long enough to be unique (20-50 characters minimum)
- If text might appear multiple times, use **context** to specify which one
- For replacements: provide complete replacement text
- For insertions: provide complete text to insert
- For deletions: specify if deleting just the text or the whole paragraph

**Examples**:

```json
{{
  "id": 1,
  "description": "Delete duplicate Scene 1 awakening paragraph",
  "action": "delete",
  "find_text": "Inanna regains consciousness among towering figures, their massive forms",
  "context": "Scene 1, second version (duplicate)",
  "delete_scope": "paragraph",
  "expected_outcome": "Duplicate awakening paragraph removed",
  "priority": "high"
}}

{{
  "id": 2,
  "description": "Make Enkidu's dialogue more primal",
  "action": "replace",
  "find_text": "We must proceed with caution through this area",
  "replace_with": "We go slow. Watch.",
  "context": "Scene 4, Enkidu's first dialogue",
  "expected_outcome": "Dialogue changed to primal speech pattern",
  "priority": "high"
}}

{{
  "id": 3,
  "description": "Add sensory detail to crash sequence",
  "action": "insert_after",
  "find_text": "The hull shrieked as atmosphere tore at the craft.",
  "insert_text": "G-forces crushed her into the seat, vision tunneling to a pinpoint as the world spun. Metal screamed against metal, the sound drilling into her skull.",
  "context": "Scene 3, crash sequence",
  "expected_outcome": "Sensory details added after hull shriek sentence",
  "priority": "medium"
}}
```

**Priority Guidelines**:
- Internal Consistency: high (breaks worldbuilding)
- Clarity: medium-high (confuses readers)
- Plot Holes: high (breaks story logic)
- Redundancy: medium (improves flow)
- Flow and Transitions: medium (improves pacing)
- Actionable Fixes: varies (depends on issue)

**Output Format**:
Return ONLY a JSON object with a "tasks" array:

```json
{{
  "tasks": [
    {{
      "id": {start_id},
      "description": "Specific task description",
      "target": "Exact location",
      "specific_change": "Exactly what to do",
      "example": "Optional example",
      "expected_outcome": "How to verify",
      "priority": "high/medium/low"
    }}
  ]
}}
```

Create tasks now:
"""
    
    def _build_task_creation_prompt(self, actionable_fixes: str) -> str:
        """Build prompt for creating specific tasks."""
        return f"""
You are a task manager converting vague editing instructions into specific, actionable tasks.

**Actionable Fixes from Review**:
{actionable_fixes}

**Your Task**:
Convert each fix into a specific task with:
1. **id**: Sequential number (1, 2, 3...)
2. **description**: Clear, specific description of what to do
3. **target**: Exact location (e.g., "Scene 2, lines 45-60", "Throughout chapter", "Scene 3 crash sequence")
4. **specific_change**: Exactly what to change (be very specific)
5. **example**: (optional but helpful) Show what the change should look like
6. **expected_outcome**: How to verify the task is complete
7. **priority**: "high", "medium", or "low"

**Guidelines for Creating Specific Tasks**:

1. **Be SPECIFIC**: 
   - Bad: "Fix character voice"
   - Good: "Make Enkidu's dialogue more primal: replace formal phrases with short, direct speech"

2. **Include EXACT LOCATION**:
   - Bad: "Somewhere in the chapter"
   - Good: "Scene 4, Enkidu's dialogue (approximately lines 150-200)"

3. **Provide EXAMPLES** when helpful:
   - "Change 'We must proceed carefully' to 'We go slow. Watch.'"

4. **Define MEASURABLE SUCCESS**:
   - For replacements: "All 5 instances of 'X' replaced with 'Y'"
   - For additions: "Added 200-300 words to Scene 3"
   - For improvements: "All Enkidu dialogue uses primal speech patterns"

5. **For word count tasks**: Specify exact range
   - "Add 200-300 words of sensory detail"

6. **For find/replace tasks**: Specify exact text
   - "Replace 'Nephilim administrators' with 'scientific caste administrators'"

**Output Format**:
Return ONLY a JSON object with a "tasks" array. Example:

```json
{{
  "tasks": [
    {{
      "id": 1,
      "description": "Replace 'Nephilim administrators' with 'scientific caste'",
      "target": "Throughout chapter",
      "specific_change": "Find all instances of 'Nephilim administrators' and replace with 'scientific caste administrators'",
      "expected_outcome": "All instances replaced (verify by searching for 'Nephilim administrators' returns 0 results)",
      "priority": "high"
    }},
    {{
      "id": 2,
      "description": "Expand Scene 3 crash sequence with sensory detail",
      "target": "Scene 3, crash sequence (approximately lines 150-200)",
      "specific_change": "Add 200-300 words of sensory detail including: metal sounds (shrieking, tearing), g-forces (crushing, pressing), visual effects (distortion, blurring), impact sequence",
      "example": "The hull shrieked as atmosphere tore at the craft. G-forces crushed her into the seat, vision tunneling to a pinpoint...",
      "expected_outcome": "Scene 3 word count increased by 200-300 words, sensory details added",
      "priority": "medium"
    }},
    {{
      "id": 3,
      "description": "Make Enkidu's dialogue more primal and less formal",
      "target": "Scene 4, all Enkidu dialogue",
      "specific_change": "Replace formal speech patterns with short, direct phrases. Use simple words, sentence fragments, present tense.",
      "example": "Change 'We must proceed with caution' to 'We go slow. Watch.' Change 'I believe we should' to 'We do this.'",
      "expected_outcome": "All Enkidu dialogue in Scene 4 uses primal, direct speech patterns",
      "priority": "high"
    }}
  ]
}}
```

**IMPORTANT**: 
- Return ONLY the JSON object, no other text
- Make tasks as specific as possible
- Include examples for complex changes
- Define clear success criteria

Create the task list now:
"""
    
    def _parse_task_list(self, response: str) -> List[Dict[str, Any]]:
        """Parse JSON task list from LLM response."""
        try:
            # Extract JSON from markdown code block if present
            json_str = response.strip()
            
            if "```json" in json_str:
                start = json_str.find("```json") + 7
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()
            elif "```" in json_str:
                start = json_str.find("```") + 3
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()
            
            # Sanitize JSON - fix common invalid escape sequences
            # Replace invalid escapes with valid ones or remove them
            import re
            # Fix invalid escape sequences like \e, \x (except valid ones like \n, \t, \r, \", \\, \/)
            json_str = re.sub(r'\\(?![ntr"\\/ubfx])', r'\\\\', json_str)
            
            # Parse JSON
            data = json.loads(json_str)
            
            # Return tasks array
            if isinstance(data, dict) and "tasks" in data:
                tasks = data["tasks"]
                logger.info(f"Parsed {len(tasks)} tasks from response")
                return tasks
            elif isinstance(data, list):
                logger.info(f"Parsed {len(data)} tasks from response (direct array)")
                return data
            else:
                logger.warning(f"Unexpected JSON structure: {type(data)}")
                return []
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing task list JSON: {e}")
            logger.error(f"Response was: {response[:500]}")
            console.print(f"[red]❌ Failed to parse task list JSON: {e}[/red]")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error parsing task list: {e}")
            console.print(f"[red]❌ Error parsing task list: {e}[/red]")
            return []
