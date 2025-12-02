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
            
            # Get character names for context
            character_list = ", ".join(kb.characters.keys()) if kb.characters else "No characters defined"
            
            # Build worldbuilding context if available
            worldbuilding_context = ""
            if kb.worldbuilding:
                wb = kb.worldbuilding
                worldbuilding_context = f"""
**Worldbuilding Context:**
- Geography: {wb.geography or 'Not defined'}
- Culture: {wb.culture_and_society or 'Not defined'}
- Key Locations: {wb.key_locations or 'Not defined'}
"""
            
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
- Characters: {character_list}

{worldbuilding_context}

**Your Task:**
Analyze Chapter {chapter_number} for issues in:
- Internal consistency (with the book's established world, characters, and plot)
- Clarity and readability
- Plot holes or logical inconsistencies
- Redundancy or repetitive content
- Flow and transitions between scenes
- Character voice consistency

**IMPORTANT:** Only flag issues that are actual errors. Do NOT flag:
- Intentional character development or changes
- Deliberate plot twists or reveals
- Stylistic choices that fit the genre
- Timeline jumps that are clearly intentional

Provide your output in markdown format with these sections:
1. **Internal Consistency** - Issues with continuity, character behavior, world rules
2. **Clarity** - Confusing passages, unclear motivations
3. **Plot Holes** - Logical inconsistencies or unexplained events
4. **Redundancy** - Repetitive content or unnecessary scenes
5. **Flow and Transitions** - Pacing issues, abrupt scene changes
6. **Actionable Fixes** - ONLY concrete, specific changes needed (be brief)

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
            
            console.print(f"💾 [green]Saved review → {save_path.name}[/green]")
            
            # Print the review content to terminal
            console.print("\n" + "="*80)
            console.print(f"[bold cyan]📋 REVIEW FOR CHAPTER {chapter_number} (Version {version})[/bold cyan]")
            console.print("="*80)
            console.print(review_output)
            console.print("="*80 + "\n")

            # Return structured feedback
            return {
                "review_markdown": review_output,
                "actionable_feedback": self._extract_actionable(review_output)
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
