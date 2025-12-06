# src/libriscribe/agents/chapter_flow/review_manager.py

import logging
from pathlib import Path
from typing import Dict, Any, Optional

from libriscribe.utils.llm_client import LLMClient
from libriscribe.utils.file_utils import ensure_directory
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class ReviewManager:
    """Manages chapter review process using ContentReviewerAgent logic."""

    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base):
        """Initialize the review manager.
        
        Args:
            llm_client: The LLM client for generating reviews
            project_dir: The project directory path
            project_knowledge_base: The project knowledge base for context
        """
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
        self.reviews_dir = self.project_dir / "reviews"
        self.reviews_dir.mkdir(exist_ok=True)
        logger.info(f"ReviewManager initialized for {project_dir}")

    def review_chapter(self, chapter_number: int, chapter_text: str) -> Dict[str, Any]:
        """Review a chapter and save the review.
        
        Args:
            chapter_number: The chapter number
            chapter_text: The chapter content to review
            
        Returns:
            Dict containing review_markdown and actionable_feedback
        """
        console.print(f"🔍 [cyan]Reviewing Chapter {chapter_number}...[/cyan]")

        try:
            # Build context from project knowledge base
            kb = self.project_knowledge_base
            
            # Build full character context
            character_context = self._build_character_context(kb)
            
            # Build full worldbuilding context
            worldbuilding_context = self._build_worldbuilding_context(kb)
            
            # Build outline context for this chapter
            outline_context = self._build_outline_context(kb, chapter_number)
            
            # Generate review using LLM with full context
            prompt = f"""
You are a professional content reviewer for a {kb.genre} book titled "{kb.title}".

**Book Context:**
- Genre: {kb.genre}
- Category: {kb.category}
- Description: {kb.description}
- Language: {kb.language}
- Tone: {kb.tone}
- Target Audience: {kb.target_audience}

**Character Details (USE AS REFERENCE - DO NOT FLAG CORRECT DESCRIPTIONS AS ERRORS):**
{character_context}

**World Context:**
{worldbuilding_context}

**Chapter {chapter_number} Outline:**
{outline_context}

**Your Task:**
Analyze Chapter {chapter_number} for issues in:
- Internal consistency (with the book's established world, characters, and plot)
- Clarity and readability
- Plot holes or logical inconsistencies
- Redundancy or repetitive content
- Flow and transitions between scenes
- Character voice consistency

**CRITICAL INSTRUCTIONS:**
- DO NOT flag character descriptions that match the character details provided above
- DO NOT flag dialogue or nicknames as description errors (e.g., if characters call someone "white skin" as a nickname, that's dialogue, not a description error)
- Only flag issues that are actual errors, not intentional choices
- Do NOT flag:
  * Intentional character development or changes
  * Deliberate plot twists or reveals
  * Stylistic choices that fit the genre
  * Timeline jumps that are clearly intentional
  * Dialogue that reflects character perspective (not narrative fact)

Provide your output in markdown format with these sections:
1. **Internal Consistency** - Issues with continuity, character behavior, world rules
2. **Clarity** - Confusing passages, unclear motivations
3. **Plot Holes** - Logical inconsistencies or unexplained events
4. **Redundancy** - Repetitive content or unnecessary scenes
5. **Flow and Transitions** - Pacing issues, abrupt scene changes
6. **Actionable Fixes** - List ALL concrete, specific changes needed. Do not limit the number of fixes. Include every issue that needs addressing, numbered sequentially.

If no issues are found in a category, state "No issues found."

CHAPTER TEXT:
{chapter_text}
"""
            review_output = self.llm_client.generate_content(prompt, max_tokens=8000)

            # Save review to file with versioning
            # Find the next available version number
            version = 1
            while True:
                if version == 1:
                    save_path = self.reviews_dir / f"chapter_{chapter_number}_review.md"
                else:
                    save_path = self.reviews_dir / f"chapter_{chapter_number}_review_v{version}.md"
                
                if not save_path.exists():
                    break
                version += 1
            
            save_path.write_text(review_output, encoding="utf-8")
            console.print(f"[green]✅ Review saved to {save_path.name}[/green]")

            # Extract actionable feedback
            actionable = self._extract_actionable(review_output)

            return {
                "review_markdown": review_output,
                "actionable_feedback": actionable
            }

        except Exception as e:
            logger.exception(f"Error reviewing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to review chapter {chapter_number}[/red]")
            return {
                "review_markdown": f"Error during review: {str(e)}",
                "actionable_feedback": "Review failed"
            }

    def _extract_actionable(self, review_md: str) -> str:
        """Extract the actionable fixes section from review.
        
        Args:
            review_md: The full review markdown
            
        Returns:
            str: The actionable fixes section
        """
        if "**Actionable Fixes**" not in review_md:
            return "No actionable fixes found."

        section = review_md.split("**Actionable Fixes**", 1)[-1]
        return section.strip()

    def load_review(self, chapter_number: int) -> Optional[str]:
        """Load a saved review for a chapter.
        
        Args:
            chapter_number: The chapter number
            
        Returns:
            Optional[str]: The review content or None if not found
        """
        review_path = self.reviews_dir / f"chapter_{chapter_number}_review.md"
        if review_path.exists():
            return review_path.read_text(encoding="utf-8")
        return None
    
    def _build_character_context(self, kb) -> str:
        """Build detailed character context from characters.json."""
        if not kb.characters:
            return "No characters defined"
        
        context_parts = []
        for name, char in kb.characters.items():
            details = [f"**{name}**:"]
            
            if hasattr(char, 'physical_description') and char.physical_description:
                details.append(f"  - Physical: {char.physical_description}")
            if hasattr(char, 'personality_traits') and char.personality_traits:
                details.append(f"  - Personality: {char.personality_traits}")
            if hasattr(char, 'role') and char.role:
                details.append(f"  - Role: {char.role}")
            
            context_parts.append('\n'.join(details))
        
        return '\n\n'.join(context_parts)
    
    def _build_worldbuilding_context(self, kb) -> str:
        """Build world context from world.json."""
        if not kb.worldbuilding:
            return "No worldbuilding defined"
        
        wb = kb.worldbuilding
        parts = []
        
        if hasattr(wb, 'geography') and wb.geography:
            parts.append(f"**Geography**: {wb.geography}")
        if hasattr(wb, 'culture_and_society') and wb.culture_and_society:
            parts.append(f"**Culture**: {wb.culture_and_society}")
        if hasattr(wb, 'key_locations') and wb.key_locations:
            parts.append(f"**Key Locations**: {wb.key_locations}")
        
        return '\n'.join(parts) if parts else "No worldbuilding defined"
    
    def _build_outline_context(self, kb, chapter_number: int) -> str:
        """Build outline context for specific chapter."""
        chapter = kb.get_chapter(chapter_number)
        if not chapter:
            return "No outline available"
        
        return f"**Chapter Summary**: {chapter.summary}\n**Scenes**: {len(chapter.scenes) if chapter.scenes else 0}"
