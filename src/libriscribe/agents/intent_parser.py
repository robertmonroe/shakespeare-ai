# src/libriscribe/agents/intent_parser.py

import logging
import json
from typing import Dict, Any, Optional

from libriscribe.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class IntentParser:
    """
    Parses natural language commands into structured intents.
    
    Examples:
        "Make M a man" → {type: "character_gender", character: "M", to_gender: "male"}
        "Change Sarah from blonde to red" → {type: "character_trait", ...}
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def parse(self, user_command: str) -> Optional[Dict[str, Any]]:
        """
        Parse a natural language command into a structured intent.
        
        Args:
            user_command: Natural language command
            
        Returns:
            Dict with intent details or None if parsing fails
        """
        prompt = self._build_parse_prompt(user_command)
        
        try:
            response = self.llm_client.generate_content(prompt, max_tokens=500, temperature=0.1)
            
            # Extract JSON from response
            intent = self._extract_json(response)
            
            if intent:
                logger.info(f"Parsed intent: {intent}")
                return intent
            else:
                logger.warning(f"Failed to parse intent from: {user_command}")
                return {"type": "unknown", "raw_command": user_command}
                
        except Exception as e:
            logger.exception(f"Error parsing intent: {e}")
            return None
    
    def _build_parse_prompt(self, user_command: str) -> str:
        """Build the LLM prompt for intent parsing."""
        return f"""Analyze this creative direction and classify it into a structured intent.

User command: "{user_command}"

Classify the command type and extract relevant details:

**Character Gender Change:**
- Pattern: "Make {{character}} a {{gender}}" or "Change {{character}} to {{gender}}"
- Output: {{"type": "character_gender", "character": "name", "to_gender": "male/female/non-binary", "raw_command": "original command"}}

**Character Attribute Change:**
- Pattern: "Make {{character}} {{attribute}}" or "Change {{character}}'s {{attribute}} to {{value}}" or "{{character}} should be {{attribute}}"
- Examples: "Make M taller", "Change Sarah's hair to red", "Bond should be more ruthless"
- Output: {{"type": "character_attribute", "character": "name", "attribute": "description", "raw_command": "original command"}}

**Grammar/Pronoun Correction:**
- Pattern: "replace {{word1}} with {{word2}}" or "{{word1}} should be {{word2}}"
- Output: {{"type": "grammar_correction", "incorrect_pronoun": "word1", "correct_pronoun": "word2"}}

**Pronoun Fix (Context-Aware):**
- Pattern: "fix pronouns for {{character}}" or "correct {{character}} pronouns" or "for {{character}} there are places where it says {{word1}} where it should be {{word2}}"
- Output: {{"type": "pronoun_fix", "character": "name"}}

**Analyze Reports:**
- Pattern: "analyze reports in {{folder}}" or "look at files in {{folder}}" or "read reports from {{folder}} and create action plan"
- Output: {{"type": "analyze_reports", "folder_path": "folder"}}

**Execute Action Plan:**
- Pattern: "execute the action plan" or "apply the recommendations" or "implement the editorial plan" or "run the action plan"
- Output: {{"type": "execute_action_plan"}}

**Character Name Change:**
- Pattern: "Rename {{old_name}} to {{new_name}}"
- Output: {{"type": "character_name", "old_name": "...", "new_name": "..."}}

**Plot Change:**
- Pattern: "The {{event}} should {{outcome}}"
- Output: {{"type": "plot_change", "event": "...", "outcome": "..."}}

**Unknown:**
- If you cannot classify, output: {{"type": "unknown", "reason": "..."}}

Output ONLY valid JSON, no explanation:
"""
    
    def _extract_json(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM response."""
        try:
            # Try to find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            
            # If no JSON found, try parsing entire response
            return json.loads(response)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from response: {response[:200]}")
            return None
