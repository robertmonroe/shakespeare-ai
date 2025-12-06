# src/libriscribe/agents/autonomous/recommendation_interpreter.py

import logging
import json
from typing import Dict, Any

from libriscribe.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class RecommendationInterpreter:
    """
    Uses LLM to interpret editorial recommendations into actionable changes.
    
    Converts natural language recommendations into structured commands
    that can be executed by the Autonomous Modifier.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def interpret_recommendation(self, recommendation: str, character_name: str = None) -> Dict[str, Any]:
        """
        Interpret a recommendation and convert to actionable change.
        
        Args:
            recommendation: Text of the recommendation
            character_name: Optional character name if known
            
        Returns:
            Dict with:
            {
                "command": "Director command to execute",
                "type": "character_development|plot|worldbuilding|etc",
                "priority": "high|medium|low"
            }
        """
        try:
            prompt = f"""Analyze this editorial recommendation and convert it into a specific, actionable command.

Recommendation: "{recommendation}"

Determine:
1. What type of change is needed? (character_development, plot_change, worldbuilding, pacing, etc.)
2. What specific command should be executed?
3. Priority level (high, medium, low)

Output as JSON:
{{
  "command": "Specific Director command (e.g., 'Develop villain network: add names, motives, and methods')",
  "type": "character_development",
  "priority": "high"
}}

Make the command specific and actionable. Focus on WHAT needs to change, not HOW to change it.
"""
            
            response = self.llm_client.generate_content(prompt, max_tokens=300, temperature=0.1)
            
            # Extract JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                result = json.loads(response[start:end])
                logger.info(f"Interpreted recommendation: {result['command']}")
                return result
            
            # Fallback
            logger.warning("Could not parse LLM response, using fallback")
            return {
                "command": recommendation,
                "type": "general",
                "priority": "medium"
            }
            
        except Exception as e:
            logger.exception(f"Error interpreting recommendation: {e}")
            return {
                "command": recommendation,
                "type": "general",
                "priority": "medium"
            }
