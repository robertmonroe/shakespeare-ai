# src/libriscribe/agents/autonomous/change_analyzer.py

import logging
import json
from typing import Dict, List, Any

from libriscribe.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class ChangeAnalyzer:
    """
    Uses LLM to analyze what needs changing across all project files.
    
    Given a user command and all project files, returns a change plan.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def analyze_change(
        self,
        user_command: str,
        project_files: Dict[str, str],
        character_name: str = None
    ) -> Dict[str, List[str]]:
        """
        Analyze what needs to change in each file.
        
        Args:
            user_command: User's natural language command
            project_files: Dict of {filename: content}
            character_name: Optional character name to focus on
            
        Returns:
            Dict of {filename: [list of changes to make]}
        """
        try:
            prompt = self._build_analysis_prompt(user_command, project_files, character_name)
            
            response = self.llm_client.generate_content(prompt, max_tokens=2000, temperature=0.1)
            
            change_plan = self._parse_change_plan(response)
            
            logger.info(f"Analyzed change: {len(change_plan)} files affected")
            return change_plan
            
        except Exception as e:
            logger.exception(f"Error analyzing change: {e}")
            return {}
    
    def _build_analysis_prompt(
        self,
        user_command: str,
        project_files: Dict[str, str],
        character_name: str = None
    ) -> str:
        """Build LLM prompt for change analysis."""
        
        # Build file summaries (truncate large files)
        file_summaries = []
        for filename, content in project_files.items():
            if len(content) > 1000:
                summary = content[:500] + "\n...\n" + content[-500:]
            else:
                summary = content
            file_summaries.append(f"**{filename}**:\n{summary}\n")
        
        files_text = "\n".join(file_summaries)
        
        focus = f" Focus on character: {character_name}." if character_name else ""
        
        return f"""Analyze what needs to change in the project files based on this user command.

User command: "{user_command}"{focus}

Project files:
{files_text}

For each file that needs changes, list what specifically needs to be updated.

Output ONLY valid JSON in this format:
{{
  "filename1": ["change description 1", "change description 2"],
  "filename2": ["change description 1"],
  ...
}}

Only include files that need changes. Be specific about what to change.
"""
    
    def _parse_change_plan(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM response into change plan."""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            
            logger.warning("Could not find JSON in response")
            return {}
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse change plan: {e}")
            return {}
