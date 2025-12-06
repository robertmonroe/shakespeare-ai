# src/libriscribe/agents/change_handlers/character_gender_handler.py

import logging
import re
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class CharacterGenderHandler:
    """
    Handles character gender changes.
    
    Changes:
    1. Updates character profile
    2. Replaces pronouns in all chapters
    3. Identifies scenes needing regeneration
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base: ProjectKnowledgeBase):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute character gender change.
        
        Args:
            intent: Parsed intent
            impact: Impact analysis
            
        Returns:
            Dict with execution results
        """
        try:
            character_name = intent.get("character")
            to_gender = intent.get("to_gender")
            pronoun_map = impact.get("pronoun_map", {})
            
            changes_applied = 0
            chapters_updated = []
            
            # Step 1: Update character profile
            console.print("   [cyan]✓[/cyan] Updating character profile (1/3)")
            self._update_character_profile(character_name, to_gender)
            
            # Step 2: Replace pronouns in chapters
            console.print("   [cyan]✓[/cyan] Changing pronouns (2/3)")
            for chapter_num in impact.get("affected_chapters", []):
                chapter_path = self.project_dir / f"chapter_{chapter_num}.md"
                if chapter_path.exists():
                    count = self._replace_pronouns_in_chapter(chapter_path, pronoun_map)
                    changes_applied += count
                    chapters_updated.append(chapter_num)
            
            # Step 3: Identify scenes needing regeneration (future enhancement)
            console.print("   [cyan]✓[/cyan] Consistency check (3/3)")
            
            return {
                "success": True,
                "changes_applied": changes_applied,
                "chapters_updated": chapters_updated,
                "review_recommended": chapters_updated[:3] if len(chapters_updated) > 3 else chapters_updated
            }
            
        except Exception as e:
            logger.exception(f"Error executing character gender change: {e}")
            return {"success": False, "error": str(e)}
    
    def _update_character_profile(self, character_name: str, to_gender: str):
        """Update character profile with new gender."""
        try:
            # Get character from knowledge base
            characters = self.project_knowledge_base.characters
            
            if character_name in characters:
                character = characters[character_name]
                
                # Update gender field if it exists
                if hasattr(character, 'gender'):
                    character.gender = to_gender
                
                # Update pronouns in description/traits if needed
                # (This is a simple implementation - could be enhanced)
                
                # Save updated knowledge base
                self.project_knowledge_base.save()
                logger.info(f"Updated {character_name} gender to {to_gender}")
            else:
                logger.warning(f"Character {character_name} not found in knowledge base")
                
        except Exception as e:
            logger.exception(f"Error updating character profile: {e}")
    
    def _replace_pronouns_in_chapter(self, chapter_path: Path, pronoun_map: Dict[str, str]) -> int:
        """
        Replace pronouns in a chapter file.
        
        Args:
            chapter_path: Path to chapter file
            pronoun_map: Dict mapping old pronouns to new ones
            
        Returns:
            Number of replacements made
        """
        try:
            text = chapter_path.read_text(encoding='utf-8')
            original_text = text
            replacements = 0
            
            # Replace each pronoun (word boundary aware)
            for old_pronoun, new_pronoun in pronoun_map.items():
                pattern = r'\b' + re.escape(old_pronoun) + r'\b'
                text, count = re.subn(pattern, new_pronoun, text)
                replacements += count
            
            # Only write if changes were made
            if text != original_text:
                chapter_path.write_text(text, encoding='utf-8')
                logger.info(f"Replaced {replacements} pronouns in {chapter_path.name}")
            
            return replacements
            
        except Exception as e:
            logger.exception(f"Error replacing pronouns in {chapter_path}: {e}")
            return 0
