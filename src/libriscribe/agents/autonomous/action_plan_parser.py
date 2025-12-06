# src/libriscribe/agents/autonomous/action_plan_parser.py

import logging
import re
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ActionPlanParser:
    """
    Parses editorial_action_plan.md and extracts recommendations.
    
    Reads markdown file and extracts actionable items from the
    "Recommended Actions" section.
    """
    
    def __init__(self):
        pass
    
    def parse_action_plan(self, plan_path: Path) -> List[Dict[str, Any]]:
        """
        Parse action plan markdown file.
        
        Args:
            plan_path: Path to editorial_action_plan.md
            
        Returns:
            List of recommendations:
            [
                {
                    "id": 1,
                    "text": "Develop the villain network...",
                    "completed": False
                },
                ...
            ]
        """
        if not plan_path.exists():
            logger.error(f"Action plan not found: {plan_path}")
            return []
        
        try:
            content = plan_path.read_text(encoding='utf-8')
            return self._extract_recommendations(content)
            
        except Exception as e:
            logger.exception(f"Error parsing action plan: {e}")
            return []
    
    def _extract_recommendations(self, content: str) -> List[Dict[str, Any]]:
        """Extract recommendation items from markdown content."""
        recommendations = []
        
        # Find "Recommended Actions" section
        sections = content.split('##')
        rec_section = None
        
        for section in sections:
            if 'Recommended Actions' in section or '📝 Recommended Actions' in section:
                rec_section = section
                break
        
        if not rec_section:
            logger.warning("No 'Recommended Actions' section found in action plan")
            return []
        
        # Extract checkbox items
        # Pattern: - [ ] text or - [x] text
        checkbox_pattern = r'^-\s*\[([ x])\]\s*(.+)$'
        
        lines = rec_section.split('\n')
        item_id = 1
        
        for line in lines:
            line = line.strip()
            match = re.match(checkbox_pattern, line)
            
            if match:
                checkbox_state = match.group(1)
                text = match.group(2).strip()
                
                # Skip if already completed
                completed = (checkbox_state.lower() == 'x')
                
                recommendations.append({
                    "id": item_id,
                    "text": text,
                    "completed": completed,
                    "original_line": line
                })
                
                item_id += 1
        
        logger.info(f"Extracted {len(recommendations)} recommendations")
        return recommendations
    
    def mark_as_complete(self, plan_path: Path, recommendation_id: int) -> bool:
        """
        Mark a recommendation as complete by changing [ ] to [x].
        
        Args:
            plan_path: Path to editorial_action_plan.md
            recommendation_id: ID of recommendation to mark complete
            
        Returns:
            True if successful
        """
        try:
            content = plan_path.read_text(encoding='utf-8')
            recommendations = self._extract_recommendations(content)
            
            if recommendation_id > len(recommendations):
                logger.error(f"Invalid recommendation ID: {recommendation_id}")
                return False
            
            # Find and replace the specific checkbox
            target_rec = recommendations[recommendation_id - 1]
            old_line = target_rec["original_line"]
            new_line = old_line.replace('- [ ]', '- [x]', 1)
            
            # Replace in content
            updated_content = content.replace(old_line, new_line, 1)
            
            # Write back
            plan_path.write_text(updated_content, encoding='utf-8')
            
            logger.info(f"Marked recommendation {recommendation_id} as complete")
            return True
            
        except Exception as e:
            logger.exception(f"Error marking recommendation complete: {e}")
            return False
