# src/libriscribe/agents/impact_analyzer.py

import logging
import re
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ImpactAnalyzer:
    """
    Analyzes the impact of a proposed change across the project.
    
    Scans chapters to find affected content and estimates scope of changes.
    """
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
    
    def analyze(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze impact of an intent.
        
        Args:
            intent: Parsed intent from IntentParser
            
        Returns:
            Dict with impact analysis
        """
        intent_type = intent.get("type")
        
        if intent_type == "character_gender":
            return self._analyze_character_gender_change(intent)
        elif intent_type == "pronoun_fix":
            return self._analyze_pronoun_fix(intent)
        elif intent_type == "character_attribute":
            return self._analyze_character_attribute_change(intent)
        elif intent_type == "analyze_reports":
            return self._analyze_reports(intent)
        elif intent_type == "execute_action_plan":
            return self._analyze_execute_action_plan(intent)
        else:
            return {"error": f"Unsupported intent type: {intent_type}"}
    
    def _analyze_character_gender_change(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of changing a character's gender."""
        character_name = intent.get("character", "")
        to_gender = intent.get("to_gender", "")
        
        # Scan all chapters for character mentions
        chapters = self._get_all_chapters()
        affected_chapters = []
        pronoun_changes = []
        
        # Determine pronoun mappings based on target gender
        if to_gender == "male":
            pronoun_map = {
                "she": "he",
                "She": "He",
                "her": "him",
                "Her": "Him",
                "hers": "his",
                "Hers": "His",
                "herself": "himself",
                "Herself": "Himself"
            }
        elif to_gender == "female":
            pronoun_map = {
                "he": "she",
                "He": "She",
                "him": "her",
                "Him": "Her",
                "his": "hers",
                "His": "Hers",
                "himself": "herself",
                "Himself": "Herself"
            }
        else:
            pronoun_map = {}  # Non-binary handling would go here
        
        # Scan each chapter
        for chapter_path in chapters:
            chapter_text = chapter_path.read_text(encoding='utf-8')
            
            # Check if character is mentioned
            if character_name.lower() in chapter_text.lower():
                chapter_num = self._extract_chapter_number(chapter_path.name)
                affected_chapters.append(chapter_num)
                
                # Count pronoun occurrences (rough estimate)
                for old_pronoun, new_pronoun in pronoun_map.items():
                    count = len(re.findall(r'\b' + re.escape(old_pronoun) + r'\b', chapter_text))
                    if count > 0:
                        pronoun_changes.append({
                            "chapter": chapter_num,
                            "from": old_pronoun,
                            "to": new_pronoun,
                            "count": count
                        })
        
        total_changes = sum(change["count"] for change in pronoun_changes)
        
        # Estimate time and cost
        estimated_time_minutes = max(5, len(affected_chapters) * 2)  # 2 min per chapter minimum
        estimated_cost_usd = total_changes * 0.01  # Rough estimate
        
        return {
            "character": character_name,
            "to_gender": to_gender,
            "affected_chapters": affected_chapters,
            "pronoun_changes": pronoun_changes,
            "changes_count": total_changes,
            "estimated_time_minutes": estimated_time_minutes,
            "estimated_cost_usd": estimated_cost_usd,
            "pronoun_map": pronoun_map
        }
    
    def _get_all_chapters(self) -> List[Path]:
        """Get all chapter files in the project."""
        return sorted(self.project_dir.glob("chapter_*.md"))
    
    def _extract_chapter_number(self, filename: str) -> int:
        """Extract chapter number from filename."""
        match = re.search(r'chapter_(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    def _analyze_pronoun_fix(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of pronoun fixing."""
        character_name = intent.get("character", "")
        
        # Scan all chapters for character mentions
        chapters = self._get_all_chapters()
        affected_chapters = []
        
        for chapter_path in chapters:
            chapter_text = chapter_path.read_text(encoding='utf-8')
            
            # Check if character is mentioned
            if character_name.lower() in chapter_text.lower():
                chapter_num = self._extract_chapter_number(chapter_path.name)
                affected_chapters.append(chapter_num)
        
        # Estimate: LLM will analyze each sentence mentioning the character
        # Rough estimate: 1 sentence per 100 characters
        estimated_sentences = len(affected_chapters) * 10  # ~10 sentences per chapter
        estimated_time_minutes = max(5, len(affected_chapters) * 3)  # 3 min per chapter
        estimated_cost_usd = estimated_sentences * 0.02  # ~$0.02 per sentence analysis
        
        return {
            "character": character_name,
            "affected_chapters": affected_chapters,
            "changes_count": estimated_sentences,
            "estimated_time_minutes": estimated_time_minutes,
            "estimated_cost_usd": estimated_cost_usd
        }

    def _analyze_character_attribute_change(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of character attribute change."""
        character_name = intent.get("character", "")
        
        # Scan all project files for character mentions
        all_files = []
        
        # JSON files
        for filename in ["characters.json", "scenes.json", "outline.md", "worldbuilding.json"]:
            file_path = self.project_dir / filename
            if file_path.exists():
                all_files.append(filename)
        
        # Chapters
        chapters = self._get_all_chapters()
        affected_chapters = []
        
        for chapter_path in chapters:
            chapter_text = chapter_path.read_text(encoding='utf-8')
            if character_name.lower() in chapter_text.lower():
                chapter_num = self._extract_chapter_number(chapter_path.name)
                affected_chapters.append(chapter_num)
                all_files.append(chapter_path.name)
        
        # Estimate: LLM will analyze and update multiple files
        estimated_time_minutes = max(5, len(all_files) * 2)
        estimated_cost_usd = len(all_files) * 0.15  # ~$0.15 per file
        
        return {
            "character": character_name,
            "affected_files": all_files,
            "affected_chapters": affected_chapters,
            "changes_count": len(all_files),
            "estimated_time_minutes": estimated_time_minutes,
            "estimated_cost_usd": estimated_cost_usd
        }


    def _analyze_reports(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of report analysis."""
        folder_path = intent.get("folder_path", "reports")
        report_folder = self.project_dir / folder_path
        
        # Count files in folder
        file_count = 0
        if report_folder.exists():
            supported_formats = ['.txt', '.md', '.rtf', '.docx', '.pdf']
            for file_path in report_folder.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                    file_count += 1
        
        # Estimate: Reading and analyzing reports
        estimated_time_minutes = max(3, file_count * 2)
        estimated_cost_usd = file_count * 0.10  # ~$0.10 per report
        
        return {
            "folder_path": folder_path,
            "reports_found": file_count,
            "changes_count": 1,  # Creates one action plan
            "estimated_time_minutes": estimated_time_minutes,
            "estimated_cost_usd": estimated_cost_usd
        }

    def _analyze_execute_action_plan(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of executing action plan."""
        plan_path = self.project_dir / "editorial_action_plan.md"
        
        if not plan_path.exists():
            return {
                "error": "No action plan found",
                "changes_count": 0,
                "estimated_time_minutes": 0,
                "estimated_cost_usd": 0
            }
        
        # Count pending recommendations
        try:
            content = plan_path.read_text(encoding='utf-8')
            pending_count = content.count('- [ ]')
            
            # Estimate based on number of recommendations
            # Each recommendation might affect 2-5 files
            estimated_files = pending_count * 3
            estimated_time_minutes = max(10, pending_count * 5)
            estimated_cost_usd = pending_count * 0.50  # ~$0.50 per recommendation
            
            return {
                "pending_recommendations": pending_count,
                "estimated_files_affected": estimated_files,
                "changes_count": pending_count,
                "estimated_time_minutes": estimated_time_minutes,
                "estimated_cost_usd": estimated_cost_usd
            }
            
        except Exception as e:
            logger.exception(f"Error analyzing action plan: {e}")
            return {
                "error": str(e),
                "changes_count": 0,
                "estimated_time_minutes": 0,
                "estimated_cost_usd": 0
            }
