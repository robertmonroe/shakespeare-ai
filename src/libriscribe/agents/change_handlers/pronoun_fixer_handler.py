# src/libriscribe/agents/change_handlers/pronoun_fixer_handler.py

import logging
import re
from pathlib import Path
from typing import Dict, Any, List

from rich.console import Console
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class PronounFixerHandler:
    """
    Context-aware pronoun correction using LLM.
    
    Analyzes each sentence to determine if pronoun usage is correct.
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """Execute context-aware pronoun fixing."""
        try:
            character = intent.get("character", "")
            
            if not character:
                return {"success": False, "error": "No character specified"}
            
            console.print(f"   [cyan]Analyzing pronoun usage for {character}...[/cyan]")
            
            chapters = sorted(self.project_dir.glob("chapter_*.md"))
            changes_applied = 0
            chapters_updated = []
            
            for chapter_path in chapters:
                count = self._fix_pronouns_in_chapter(chapter_path, character)
                if count > 0:
                    changes_applied += count
                    chapter_num = self._extract_chapter_number(chapter_path.name)
                    chapters_updated.append(chapter_num)
            
            return {
                "success": True,
                "changes_applied": changes_applied,
                "chapters_updated": chapters_updated,
                "review_recommended": chapters_updated
            }
            
        except Exception as e:
            logger.exception(f"Error fixing pronouns: {e}")
            return {"success": False, "error": str(e)}
    
    def _fix_pronouns_in_chapter(self, chapter_path: Path, character: str) -> int:
        """Fix pronouns in a chapter using LLM analysis."""
        try:
            text = chapter_path.read_text(encoding='utf-8')
            
            # Split into sentences
            sentences = re.split(r'([.!?]+\s+)', text)
            
            fixed_sentences = []
            changes = 0
            
            for i, sentence in enumerate(sentences):
                # Skip punctuation-only segments
                if not sentence.strip() or sentence.strip() in '.!?':
                    fixed_sentences.append(sentence)
                    continue
                
                # Check if sentence mentions the character
                if character.lower() in sentence.lower():
                    fixed = self._fix_sentence_pronouns(sentence, character)
                    if fixed != sentence:
                        changes += 1
                    fixed_sentences.append(fixed)
                else:
                    fixed_sentences.append(sentence)
            
            if changes > 0:
                fixed_text = ''.join(fixed_sentences)
                chapter_path.write_text(fixed_text, encoding='utf-8')
                logger.info(f"Fixed {changes} pronoun issues in {chapter_path.name}")
            
            return changes
            
        except Exception as e:
            logger.exception(f"Error processing {chapter_path}: {e}")
            return 0
    
    def _fix_sentence_pronouns(self, sentence: str, character: str) -> str:
        """Use LLM to fix pronouns in a single sentence."""
        prompt = f"""Fix any incorrect pronoun usage in this sentence for the character "{character}".

Sentence: "{sentence}"

Rules:
- Use "his" for possessive (his book, his car)
- Use "him" for object (give it to him, saw him)
- Use "he" for subject (he went, he said)
- Only fix grammatically incorrect usage
- Return the EXACT sentence with corrections, nothing else

Corrected sentence:"""

        try:
            response = self.llm_client.generate_content(prompt, max_tokens=200, temperature=0.1)
            fixed = response.strip().strip('"')
            return fixed if fixed else sentence
        except Exception as e:
            logger.error(f"Error fixing sentence: {e}")
            return sentence
    
    def _extract_chapter_number(self, filename: str) -> int:
        """Extract chapter number from filename."""
        match = re.search(r'chapter_(\d+)', filename)
        return int(match.group(1)) if match else 0
