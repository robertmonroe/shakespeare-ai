import logging
import os
from typing import Dict, Any
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from libriscribe.utils.file_utils import ensure_directory
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class ContentReviewerAgent(Agent):
    """
    Improved Content Reviewer Agent
    
    ✔ Saves review to /reviews/
    ✔ Returns structured feedback for next agent
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__("ContentReviewerAgent", llm_client)

    def execute(self, chapter_number: int, chapter_text: str, project_path: str, **kwargs) -> Dict[str, Any]:
        console.print(f"🔍 [cyan]Reviewing Chapter {chapter_number}...[/cyan]")

        # ---- RUN LLM REVIEW ----
        prompt = f"""
You are a professional content reviewer.
Analyze the chapter below for issues in:

- internal consistency
- clarity
- plot holes
- redundancy
- flow and transitions

Provide your output in markdown format with individual sections.
Then provide a final section titled **Actionable Fixes** listing ALL concrete changes needed. Do not limit the number of fixes.

CHAPTER NUMBER: {chapter_number}
CHAPTER TEXT:
{chapter_text}
"""
        review_output = self.llm_client.generate_content(prompt, max_tokens=8000)

        # ---- SAVE REVIEW ----
        reviews_dir = os.path.join(project_path, "reviews")
        ensure_directory(reviews_dir)

        save_path = os.path.join(reviews_dir, f"chapter_{chapter_number}_review.md")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(review_output)

        console.print(f"💾 [green]Saved review → {save_path}[/green]")

        # ---- RETURN STRUCTURED FEEDBACK FOR NEXT PASS ----
        return {
            "review_markdown": review_output,
            "actionable_feedback": self._extract_actionable(review_output)
        }

    def _extract_actionable(self, review_md: str):
        """
        Extract ONLY the actionable fixes section.
        """
        if "**Actionable Fixes**" not in review_md:
            return "No actionable fixes found."

        section = review_md.split("**Actionable Fixes**", 1)[-1]
        return section.strip()
