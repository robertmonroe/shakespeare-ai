import logging
from typing import Dict, Any
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from libriscribe.utils.prompt_integration import ExternalPromptMixin
from libriscribe.utils import prompts_context as prompts
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class EnhancedEditorAgent(Agent, ExternalPromptMixin):
    """Editor agent that now supports reviewer feedback for a second pass."""

    def __init__(self, llm_client: LLMClient):
        Agent.__init__(self, "EnhancedEditorAgent", llm_client)
        ExternalPromptMixin.__init__(self)

    def execute(
        self,
        chapter_number: int,
        chapter_content: str,
        actionable_feedback: str = "",
        genre: str = "fiction",
        book_title: str = "Untitled",
        language: str = "English",
        project_knowledge_base = None,
        **kwargs
    ) -> Dict[str, Any]:

        # Build context if knowledge base provided
        if project_knowledge_base:
            from libriscribe.knowledge_base import ProjectKnowledgeBase
            kb = project_knowledge_base
            
            # Build character context
            character_context = "No characters defined yet."
            if kb.characters:
                chars = []
                for name, char in kb.characters.items():
                    traits = char.personality_traits[:80] if char.personality_traits else "No traits defined"
                    role = char.role if hasattr(char, 'role') else "Character"
                    chars.append(f"- **{name}**: {role}. {traits}")
                character_context = "\n".join(chars)
            
            # Build worldbuilding context
            worldbuilding_context = "Contemporary/realistic setting."
            if kb.worldbuilding:
                wb = kb.worldbuilding
                parts = []
                if wb.geography:
                    parts.append(f"**Geography**: {wb.geography[:150]}...")
                if wb.key_locations:
                    parts.append(f"**Key Locations**: {wb.key_locations[:150]}...")
                if wb.culture_and_society:
                    parts.append(f"**Culture**: {wb.culture_and_society[:150]}...")
                worldbuilding_context = "\n".join(parts) if parts else "No worldbuilding defined."
            
            # Get previous chapter summary
            previous_chapter_summary = "This is the first chapter."
            if chapter_number > 1:
                prev_chapter = kb.get_chapter(chapter_number - 1)
                if prev_chapter and prev_chapter.summary:
                    previous_chapter_summary = f"**Chapter {chapter_number - 1}**: {prev_chapter.summary}"
            
            book_description = kb.description
        else:
            # Fallback if no knowledge base
            character_context = "No context available"
            worldbuilding_context = "No context available"
            previous_chapter_summary = "No context available"
            book_description = "No description available"

        prompt_data = {
            "genre": genre,
            "book_title": book_title,
            "language": language,
            "chapter_number": chapter_number,
            "chapter_title": f"Chapter {chapter_number}",
            "chapter_content": chapter_content,
            "review_feedback": actionable_feedback or "No reviewer feedback provided.",
            "book_description": book_description,
            "character_context": character_context,
            "worldbuilding_context": worldbuilding_context,
            "previous_chapter_summary": previous_chapter_summary
        }

        console.print(f"✏️ [cyan]Rewriting Chapter {chapter_number} using reviewer feedback...[/cyan]")

        edited = self.generate_with_external_prompt(
            prompt_name="editor",
            fallback_prompt=prompts.EDITOR_PROMPT,
            prompt_data=prompt_data,
            default_max_tokens=8000
        )

        console.print(f"📘 [green]Chapter {chapter_number} re-edited successfully[/green]")

        return {"edited_content": edited}
