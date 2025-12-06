# src/libriscribe/agents/editor.py

import logging
import re
from pathlib import Path
from typing import List

from libriscribe.agents.agent_base import Agent
from libriscribe.utils import prompts_context as prompts
from libriscribe.utils.file_utils import read_markdown_file, write_markdown_file
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient
from libriscribe.agents.content_reviewer import ContentReviewerAgent
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class EditorAgent(Agent):
    """Edits and refines chapters."""

    def __init__(self, llm_client: LLMClient):
        super().__init__("EditorAgent", llm_client)

    def execute(self, project_knowledge_base: ProjectKnowledgeBase, chapter_number: int) -> None:
        """Edits a chapter and overwrites the original file (backup already created by ChapterFlowManager)."""
        try:
            chapter_path = str(Path(project_knowledge_base.project_dir) / f"chapter_{chapter_number}.md")
            chapter_content = read_markdown_file(chapter_path)
            if not chapter_content:
                print(f"ERROR: Chapter file is empty: {chapter_path}")
                return
            chapter_title = self.extract_chapter_title(chapter_content)

            # Load the existing review from file instead of generating a new one
            review_path = Path(project_knowledge_base.project_dir) / "reviews" / f"chapter_{chapter_number}_review.md"
            
            if review_path.exists():
                review_feedback = review_path.read_text(encoding="utf-8")
                console.print(f"📖 [cyan]Using existing review for Chapter {chapter_number}[/cyan]")
            else:
                # Fallback: generate review if file doesn't exist
                console.print(f"⚠️ [yellow]No existing review found, generating new review...[/yellow]")
                reviewer_agent = ContentReviewerAgent(self.llm_client)
                review_results = reviewer_agent.execute(
                    chapter_number=chapter_number,
                    chapter_text=chapter_content,
                    project_path=str(project_knowledge_base.project_dir)
                )
                review_feedback = review_results.get("review_markdown", review_results.get("review", ""))

            scene_titles = self.extract_scene_titles(chapter_content)
            scene_titles_instruction = ""
            if scene_titles:
                scene_titles_str = "\n".join(f"- {title}" for title in scene_titles)
                scene_titles_instruction = f"""
                    IMPORTANT: This chapter contains scene titles that must be preserved in your edit.
                    Make sure each scene begins with its title in the same format as the original.
                    Here are the scene titles to preserve:

                    {scene_titles_str}

                    Preserve the original scene header format (whether ### or **bold**).
                    """
            
            # Build context for editor
            character_context = self._build_character_context(project_knowledge_base)
            worldbuilding_context = self._build_worldbuilding_context(project_knowledge_base)
            previous_chapter_summary = self._get_previous_chapter_summary(project_knowledge_base, chapter_number)
            style_guide = prompts.get_style_guide(project_knowledge_base)
            
            prompt_data = {
                "chapter_number": chapter_number,
                "chapter_title": chapter_title,
                "book_title": project_knowledge_base.title,
                "genre": project_knowledge_base.genre,
                "language": project_knowledge_base.language,
                "book_description": project_knowledge_base.description,
                "chapter_content": chapter_content,
                "review_feedback": review_feedback,
                "character_context": character_context,
                "worldbuilding_context": worldbuilding_context,
                "previous_chapter_summary": previous_chapter_summary,
                "style_guide": style_guide
            }

            console.print(f"✏️ [cyan]Editing Chapter {chapter_number} based on feedback...[/cyan]")
            prompt = prompts.EDITOR_PROMPT.format(**prompt_data) + scene_titles_instruction
            edited_response = self.llm_client.generate_content(prompt, max_tokens=12000)
            
            # Extract revised chapter from response
            revised_chapter = ""
            
            if "```" in edited_response:
                # Extract from code block
                start = edited_response.find("```") + 3
                end = edited_response.rfind("```")
                
                # If there's only one ```, the response might be truncated - use everything after it
                if start == end + 3:  # Only found one set of ```
                    # Skip the language identifier if present (e.g., ```markdown)
                    next_newline = edited_response.find("\n", start)
                    if next_newline != -1:
                        start = next_newline + 1
                    revised_chapter = edited_response[start:].strip()
                else:
                    # Normal case: found opening and closing ```
                    # Skip the language identifier if present (e.g., ```markdown)
                    next_newline = edited_response.find("\n", start)
                    if next_newline < end and next_newline != -1:
                        start = next_newline + 1
                    
                    revised_chapter = edited_response[start:end].strip()
            else:
                # If no code blocks, try to extract the content after a leading explanation
                lines = edited_response.split("\n")
                content_start = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith("#"):  # Look for any heading
                        content_start = i
                        break
                
                if content_start >= 0:
                    revised_chapter = "\n".join(lines[content_start:]).strip()
                    
                    
            if revised_chapter and len(revised_chapter) > 100:  # Ensure it's substantial
                # Overwrite the original chapter file with the edited version
                # (Backup was already created by ChapterFlowManager before calling this)
                write_markdown_file(chapter_path, revised_chapter)
                console.print(f"[green]✅ Edited chapter saved ({len(revised_chapter)} chars)![/green]")
            else:
                print(f"ERROR: Could not extract revised chapter from editor output (got {len(revised_chapter)} chars).")
                logger.error("Could not extract revised chapter content.")
                logger.error(f"Response length: {len(edited_response)} chars")
                logger.error(f"Response preview: {edited_response[:500]}...")  # Only log first 500 chars


        except Exception as e:
            logger.exception(f"Error editing chapter: {e}")
            print(f"ERROR: Failed to edit chapter. See log.")

    def extract_chapter_number(self, chapter_path: str) -> int:
        """Extracts chapter number."""
        try:
            return int(chapter_path.split("_")[1].split(".")[0])
        except:
            return -1

    def extract_chapter_title(self, chapter_content: str) -> str:
        """Extracts chapter title."""
        lines = chapter_content.split("\n")
        for line in lines:
            if line.startswith("#"):
                return line.replace("#", "").strip()
        return "Untitled Chapter"

    def extract_scene_titles(self, chapter_content: str) -> List[str]:
        """Extracts scene titles from chapter content.
        
        Recognizes multiple formats:
        - **Scene 1: Title** (bold format)
        - ### Scene 1: Title (markdown header)
        - **Scene Title** (bold without number)
        """
        scene_titles = []
        
        # Pattern 1: Bold format - **Scene 1: Title** or **Scene Title**
        bold_pattern = r'\*\*Scene\s+\d*:?\s*([^*]+)\*\*'
        bold_matches = re.findall(bold_pattern, chapter_content)
        scene_titles.extend([match.strip() for match in bold_matches])
        
        # Pattern 2: Markdown header format - ### Scene 1: Title
        header_pattern = r'^#{2,3}\s+Scene\s+\d+:?\s*(.+)$'
        header_matches = re.findall(header_pattern, chapter_content, re.MULTILINE)
        scene_titles.extend([match.strip() for match in header_matches])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_titles = []
        for title in scene_titles:
            if title not in seen:
                seen.add(title)
                unique_titles.append(title)
        
        return unique_titles

    def _build_character_context(self, kb: ProjectKnowledgeBase) -> str:
        """Build character context string for editor prompts."""
        if not kb.characters:
            return "No characters defined yet."
        
        chars = []
        for name, char in kb.characters.items():
            # Include appearance for consistency checking
            appearance = ""
            if hasattr(char, 'appearance') and char.appearance:
                appearance = f" Appearance: {char.appearance[:150]}"
            elif hasattr(char, 'physical_description') and char.physical_description:
                appearance = f" Appearance: {char.physical_description[:150]}"
            
            traits = char.personality_traits[:80] if char.personality_traits else "No traits defined"
            role = char.role if hasattr(char, 'role') else "Character"
            chars.append(f"- **{name}**: {role}. {traits}.{appearance}")
        
        return "\n".join(chars)
    
    def _build_worldbuilding_context(self, kb: ProjectKnowledgeBase) -> str:
        """Build worldbuilding context string for editor prompts."""
        if not kb.worldbuilding:
            return "Contemporary/realistic setting."
        
        wb = kb.worldbuilding
        parts = []
        
        if hasattr(wb, 'geography') and wb.geography:
            parts.append(f"**Geography**: {wb.geography[:150]}...")
        if hasattr(wb, 'key_locations') and wb.key_locations:
            parts.append(f"**Key Locations**: {wb.key_locations[:150]}...")
        if hasattr(wb, 'culture_and_society') and wb.culture_and_society:
            parts.append(f"**Culture**: {wb.culture_and_society[:150]}...")
        if hasattr(wb, 'technology_level') and wb.technology_level:
            parts.append(f"**Technology**: {wb.technology_level[:150]}...")
        
        return "\n".join(parts) if parts else "No worldbuilding defined."
    
    def _get_previous_chapter_summary(self, kb: ProjectKnowledgeBase, chapter_number: int) -> str:
        """Get summary of previous chapter for continuity."""
        if chapter_number <= 1:
            return "This is the first chapter."
        
        prev_chapter = kb.get_chapter(chapter_number - 1)
        if prev_chapter and prev_chapter.summary:
            return f"**Chapter {chapter_number - 1}**: {prev_chapter.summary}"
        
        return "Previous chapter summary not available."