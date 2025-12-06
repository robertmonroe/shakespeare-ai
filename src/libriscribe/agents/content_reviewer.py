import logging
import os
import json
from typing import Dict, Any
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from libriscribe.utils.file_utils import ensure_directory, read_json_file
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class ContentReviewerAgent(Agent):
    """
    Improved Content Reviewer Agent
    
    ✔ Includes character/world context for consistency checking
    ✔ Saves review to /reviews/
    ✔ Returns structured feedback for next agent
    ✔ Fiction-specific review categories
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__("ContentReviewerAgent", llm_client)

    def execute(self, chapter_number: int, chapter_text: str, project_path: str, **kwargs) -> Dict[str, Any]:
        console.print(f"🔍 [cyan]Reviewing Chapter {chapter_number}...[/cyan]")

        # ---- LOAD CONTEXT ----
        character_context = self._get_character_context(project_path)
        world_context = self._get_world_context(project_path)
        outline_context = self._get_outline_context(project_path, chapter_number)
        style_guide = self._get_style_guide(project_path)

        # ---- BUILD REVIEW PROMPT WITH FULL CONTEXT ----
        prompt = f"""
You are a professional content reviewer for fiction manuscripts.

**CRITICAL CONTEXT - Use this to verify consistency:**

**Characters (verify these EXACT descriptions are used):**
{character_context}

**World/Setting:**
{world_context}

**Chapter Outline (verify chapter follows this):**
{outline_context}

**Style Guide:**
{style_guide}

---

**Analyze the chapter below for issues in:**

## 1. Character Consistency
- Are character appearances EXACTLY as defined above? (skin color, hair, eyes, etc.)
- Is each character's voice consistent with their personality?
- Do actions match established traits and motivations?

## 2. Worldbuilding Consistency  
- Are locations, technology, culture elements consistent with the world context?
- Any anachronisms or contradictions?

## 3. Plot & Continuity
- Does the chapter follow the outline summary?
- Any plot holes or logic breaks?
- Timeline consistency?

## 4. Pacing & Flow
- Any sections that drag or feel rushed?
- Smooth transitions between scenes?
- Balance of action, dialogue, and description?

## 5. Prose Quality
- Show vs tell balance (too much internal monologue?)
- Sensory details present?
- Dialogue natural and distinct per character?
- Passive voice overuse?

## 6. Emotional Beats
- Are the intended emotional moments landing?
- Character reactions believable?

## 7. Actionable Fixes
List ALL specific changes needed, with exact quotes when possible.

---

**CHAPTER NUMBER:** {chapter_number}
**CHAPTER TEXT:**
{chapter_text}

Provide your review in markdown format with the numbered sections above.
"""
        review_output = self.llm_client.generate_content(prompt, max_tokens=8000)

        # ---- SAVE REVIEW ----
        reviews_dir = os.path.join(project_path, "reviews")
        ensure_directory(reviews_dir)

        save_path = os.path.join(reviews_dir, f"chapter_{chapter_number}_review.md")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(review_output)

        console.print(f"💾 [green]Saved review → {save_path}[/green]")

        # ---- RETURN STRUCTURED FEEDBACK FOR NEXT PASS ----
        return {
            "review_markdown": review_output,
            "actionable_feedback": self._extract_actionable(review_output)
        }

    def _get_character_context(self, project_path: str) -> str:
        """Load character details from characters.json."""
        try:
            chars_file = os.path.join(project_path, "characters.json")
            if os.path.exists(chars_file):
                chars = read_json_file(chars_file)
                if isinstance(chars, list):
                    context_lines = []
                    for char in chars:
                        name = char.get('name', 'Unknown')
                        appearance = char.get('appearance', char.get('physical_description', 'Not specified'))
                        personality = char.get('personality_traits', 'Not specified')
                        role = char.get('role', 'Not specified')
                        context_lines.append(f"**{name}**:")
                        context_lines.append(f"  - Appearance: {appearance}")
                        context_lines.append(f"  - Personality: {personality}")
                        context_lines.append(f"  - Role: {role}")
                        context_lines.append("")
                    return "\n".join(context_lines)
            return "No character data available."
        except Exception as e:
            logger.warning(f"Could not load character context: {e}")
            return "Error loading character data."

    def _get_world_context(self, project_path: str) -> str:
        """Load worldbuilding from world.json."""
        try:
            world_file = os.path.join(project_path, "world.json")
            if os.path.exists(world_file):
                world = read_json_file(world_file)
                if isinstance(world, dict):
                    context_lines = []
                    for key, value in world.items():
                        if value and key not in ['id', 'created_at'] and isinstance(value, str):
                            # Truncate long values
                            display_val = value[:300] + "..." if len(value) > 300 else value
                            context_lines.append(f"**{key.replace('_', ' ').title()}**: {display_val}")
                    return "\n".join(context_lines) if context_lines else "No worldbuilding data."
            return "No worldbuilding data available."
        except Exception as e:
            logger.warning(f"Could not load world context: {e}")
            return "Error loading world data."

    def _get_outline_context(self, project_path: str, chapter_number: int) -> str:
        """Get chapter summary from outline."""
        try:
            outline_file = os.path.join(project_path, "outline.md")
            if os.path.exists(outline_file):
                with open(outline_file, 'r', encoding='utf-8') as f:
                    outline = f.read()
                
                # Extract this chapter's section
                chapter_marker = f"## Chapter {chapter_number}:"
                if chapter_marker in outline:
                    start = outline.find(chapter_marker)
                    # Find next chapter or end
                    next_chapter = outline.find(f"## Chapter {chapter_number + 1}:", start)
                    if next_chapter == -1:
                        chapter_section = outline[start:]
                    else:
                        chapter_section = outline[start:next_chapter]
                    return chapter_section[:1500]  # Limit size
            return "No outline available."
        except Exception as e:
            logger.warning(f"Could not load outline context: {e}")
            return "Error loading outline."

    def _get_style_guide(self, project_path: str) -> str:
        """Get style/pacing preferences from project data."""
        try:
            project_file = os.path.join(project_path, "project_data.json")
            if os.path.exists(project_file):
                data = read_json_file(project_file)
                parts = []
                
                if data.get('tone'):
                    parts.append(f"Tone: {data['tone']}")
                if data.get('inspired_by'):
                    parts.append(f"Style inspiration: {data['inspired_by']}")
                if data.get('pacing_preference'):
                    parts.append(f"Pacing: {data['pacing_preference']}")
                if data.get('genre'):
                    parts.append(f"Genre: {data['genre']}")
                    
                return "\n".join(parts) if parts else "No style guide specified."
            return "No project data available."
        except Exception as e:
            logger.warning(f"Could not load style guide: {e}")
            return "Error loading style guide."

    def _extract_actionable(self, review_md: str) -> str:
        """Extract the actionable fixes section."""
        # Try multiple possible headers
        markers = ["## 7. Actionable Fixes", "**Actionable Fixes**", "## Actionable Fixes", "# Actionable Fixes"]
        
        for marker in markers:
            if marker in review_md:
                section = review_md.split(marker, 1)[-1]
                # Stop at next major section if present
                for stopper in ["## 8", "---", "# "]:
                    if stopper in section:
                        section = section.split(stopper)[0]
                return section.strip()
        
        return "No actionable fixes section found."
