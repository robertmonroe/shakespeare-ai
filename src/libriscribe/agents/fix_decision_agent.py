"""
Fix Decision Agent - Evaluates multiple fix options and chooses the best approach

When reviews provide multiple suggestions (e.g., "Option A" or "Option B"),
this agent evaluates each option against story context and chooses the best one.
"""

import logging
from typing import Dict, Any, List, Optional
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from rich.console import Console
import re

console = Console()
logger = logging.getLogger(__name__)


class FixDecisionAgent(Agent):
    """Evaluates multiple fix options and chooses the best approach."""

    def __init__(self, llm_client: LLMClient):
        super().__init__("FixDecisionAgent", llm_client)

    def execute(
        self,
        fix_description: str,
        chapter_context: str,
        worldbuilding_context: str = "",
        character_context: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate fix options and choose the best one.
        
        Args:
            fix_description: The fix with multiple options (e.g., "Replace X with (A or B)")
            chapter_context: Current chapter text for context
            worldbuilding_context: Worldbuilding information
            character_context: Character information
            
        Returns:
            Dict containing:
                - has_options: Whether multiple options were found
                - options: List of extracted options
                - chosen_option: The selected option
                - reasoning: Why this option was chosen
                - score: Quality score (1-10)
                - implementation: Specific guidance
        """
        
        # Extract options from fix description
        options = self._extract_options(fix_description)
        
        if not options or len(options) < 2:
            # No multiple options, return as-is
            return {
                'has_options': False,
                'fix_description': fix_description
            }
        
        console.print(f"🤔 [cyan]Evaluating {len(options)} fix options...[/cyan]")
        
        # Build decision prompt
        prompt = self._build_decision_prompt(
            fix_description,
            options,
            chapter_context,
            worldbuilding_context,
            character_context
        )
        
        # Get decision from LLM
        decision_output = self.llm_client.generate_content(
            prompt,
            max_tokens=2000,
            temperature=0.4  # Moderate temp for reasoned decisions
        )
        
        # Parse decision
        result = self._parse_decision(decision_output, options)
        result['has_options'] = True
        result['options'] = options
        
        # Display decision
        self._display_decision(result)
        
        return result

    def _extract_options(self, fix_description: str) -> List[str]:
        """Extract multiple options from fix description."""
        
        options = []
        
        # Pattern 1: (e.g., "option A" or "option B")
        match = re.search(r'\(e\.g\.,\s*"([^"]+)"\s+or\s+"([^"]+)"\)', fix_description)
        if match:
            options = [match.group(1), match.group(2)]
            return options
        
        # Pattern 2: (Option A, Option B, or Option C)
        match = re.search(r'\(([^)]+)\)', fix_description)
        if match:
            content = match.group(1)
            # Split by "or" or ","
            parts = re.split(r',\s*or\s+|,\s+|\s+or\s+', content)
            options = [p.strip().strip('"\'') for p in parts if p.strip()]
            if len(options) >= 2:
                return options
        
        # Pattern 3: Multiple numbered options in description
        # (Would need more sophisticated parsing)
        
        return options

    def _build_decision_prompt(
        self,
        fix_description: str,
        options: List[str],
        chapter_context: str,
        worldbuilding_context: str,
        character_context: str
    ) -> str:
        """Build the decision evaluation prompt."""
        
        options_list = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        
        prompt = f"""
You are a story consultant helping choose the best fix option.

FIX NEEDED:
{fix_description}

OPTIONS TO EVALUATE:
{options_list}

STORY CONTEXT:

Worldbuilding:
{worldbuilding_context[:500] if worldbuilding_context else "Not provided"}

Characters:
{character_context[:500] if character_context else "Not provided"}

Current Chapter (excerpt):
{chapter_context[:1000]}

EVALUATION CRITERIA:

For each option, score 1-10 on:
1. **Consistency** (30%): Fits established worldbuilding, character, plot
2. **Quality** (25%): Improves story and reader experience
3. **Setup** (20%): Uses existing story elements, creates payoff
4. **Simplicity** (15%): Doesn't add unnecessary complexity
5. **Impact** (10%): Narrative significance

Provide your analysis in this format:

## Option Evaluation

### Option 1: [option text]
**Consistency**: [score]/10 - [reasoning]
**Quality**: [score]/10 - [reasoning]
**Setup**: [score]/10 - [reasoning]
**Simplicity**: [score]/10 - [reasoning]
**Impact**: [score]/10 - [reasoning]
**Total Score**: [weighted total]/10

### Option 2: [option text]
[same format]

## Decision

**Chosen Option**: Option [number]
**Final Score**: [score]/10
**Reasoning**: [2-3 sentences explaining why this is the best choice]
**Implementation**: [Specific guidance on how to apply this fix]

Choose the option with the highest weighted score.
"""
        return prompt

    def _parse_decision(self, decision_output: str, options: List[str]) -> Dict[str, Any]:
        """Parse the decision output."""
        
        result = {
            'chosen_option': None,
            'reasoning': '',
            'score': 0,
            'implementation': '',
            'full_analysis': decision_output
        }
        
        # Extract chosen option
        match = re.search(r'\*\*Chosen Option\*\*:\s*Option\s*(\d+)', decision_output)
        if match:
            option_num = int(match.group(1)) - 1
            if 0 <= option_num < len(options):
                result['chosen_option'] = options[option_num]
        
        # Extract score
        match = re.search(r'\*\*Final Score\*\*:\s*([0-9.]+)', decision_output)
        if match:
            result['score'] = float(match.group(1))
        
        # Extract reasoning
        match = re.search(r'\*\*Reasoning\*\*:\s*(.+?)(?:\n\*\*|$)', decision_output, re.DOTALL)
        if match:
            result['reasoning'] = match.group(1).strip()
        
        # Extract implementation
        match = re.search(r'\*\*Implementation\*\*:\s*(.+?)(?:\n\n|$)', decision_output, re.DOTALL)
        if match:
            result['implementation'] = match.group(1).strip()
        
        # Fallback: if no option chosen, use first one
        if not result['chosen_option'] and options:
            result['chosen_option'] = options[0]
            result['reasoning'] = "Default to first option (parsing failed)"
        
        return result

    def _display_decision(self, result: Dict[str, Any]):
        """Display the decision to console."""
        
        console.print("\n" + "="*80)
        console.print(f"[bold cyan]🎯 FIX DECISION[/bold cyan]")
        console.print("="*80)
        
        if result.get('chosen_option'):
            console.print(f"\n[bold green]✓ Chosen Option:[/bold green] {result['chosen_option']}")
            console.print(f"[cyan]Score:[/cyan] {result.get('score', 0)}/10")
            
            if result.get('reasoning'):
                console.print(f"\n[yellow]Reasoning:[/yellow]")
                console.print(f"  {result['reasoning']}")
            
            if result.get('implementation'):
                console.print(f"\n[blue]Implementation:[/blue]")
                console.print(f"  {result['implementation']}")
        
        console.print("\n" + "="*80 + "\n")


# Example usage in review workflow:
"""
fix = "Replace 'Nephilim administrators' with (e.g., 'scientific caste administrators' or 'lesser bloodline functionaries')"

decision_agent = FixDecisionAgent(llm_client)
result = decision_agent.execute(
    fix_description=fix,
    chapter_context=chapter_text,
    worldbuilding_context=worldbuilding_info,
    character_context=character_info
)

if result['has_options']:
    # Use chosen option
    chosen_fix = f"Replace 'Nephilim administrators' with '{result['chosen_option']}'"
    editor.apply_fix(chosen_fix, result['implementation'])
else:
    # No options, apply as-is
    editor.apply_fix(fix)
"""
