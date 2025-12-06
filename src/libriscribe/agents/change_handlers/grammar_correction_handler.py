# src/libriscribe/agents/change_handlers/grammar_correction_handler.py

import logging
import re
from pathlib import Path
from typing import Dict, Any

from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class GrammarCorrectionHandler:
    """
    Handles simple grammar/pronoun corrections.
    
    Example: "Replace 'him' with 'his' for character M"
    """
    
    def __init__(self, llm_client, project_dir, project_knowledge_base):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """Execute grammar correction."""
        try:
            incorrect = intent.get("incorrect_pronoun", "")
            correct = intent.get("correct_pronoun", "")
            
            if not incorrect or not correct:
                return {"success": False, "error": "Missing pronouns to replace"}
            
            # Get all chapters
            chapters = sorted(self.project_dir.glob("chapter_*.md"))
            
            changes_applied = 0
            chapters_updated = []
            
            console.print(f"   [cyan]✓[/cyan] Replacing '{incorrect}' with '{correct}'")
            
            for chapter_path in chapters:
                count = self._replace_in_chapter(chapter_path, incorrect, correct)
                if count > 0:
                    changes_applied += count
                    chapter_num = self._extract_chapter_number(chapter_path.name)
                    chapters_updated.append(chapter_num)
            
            return {
                "success": True,
                "changes_applied": changes_applied,
                "chapters_updated": chapters_updated,
                "review_recommended": chapters_updated[:3] if len(chapters_updated) > 3 else chapters_updated
            }
            
        except Exception as e:
            logger.exception(f"Error in grammar correction: {e}")
            return {"success": False, "error": str(e)}
    
    def _replace_in_chapter(self, chapter_path: Path, old: str, new: str) -> int:
        """Replace word in chapter with word boundary awareness."""
        try:
            text = chapter_path.read_text(encoding='utf-8')
            original = text
            
            # Word boundary aware replacement
            pattern = r'\b' + re.escape(old) + r'\b'
            text, count = re.subn(pattern, new, text, flags=re.IGNORECASE)
            
            if text != original:
                chapter_path.write_text(text, encoding='utf-8')
                logger.info(f"Replaced {count} occurrences in {chapter_path.name}")
            
            return count
            
        except Exception as e:
            logger.exception(f"Error replacing in {chapter_path}: {e}")
            return 0
    
    def _extract_chapter_number(self, filename: str) -> int:
        """Extract chapter number from filename."""
        match = re.search(r'chapter_(\d+)', filename)
        return int(match.group(1)) if match else 0
