# src/libriscribe/agents/chapter_writer.py

import logging
from pathlib import Path
from typing import Optional, Dict, List
from libriscribe.agents.agent_base import Agent
from libriscribe.utils import prompts_context as prompts
from libriscribe.utils.file_utils import read_markdown_file, read_json_file, write_markdown_file, extract_json_from_markdown
from libriscribe.knowledge_base import ProjectKnowledgeBase, Chapter, Scene
from libriscribe.utils.llm_client import LLMClient

import json
from rich.console import Console

console = Console()

logger = logging.getLogger(__name__)

class ChapterWriterAgent(Agent):
    """Writes chapters with full context awareness."""

    def __init__(self, llm_client: LLMClient):
        super().__init__("ChapterWriterAgent", llm_client)


    def execute(self, project_knowledge_base: ProjectKnowledgeBase, chapter_number: int, output_path: Optional[str] = None) -> None:
        """Writes a chapter scene by scene with full context."""
        try:
            # Get chapter data
            chapter = project_knowledge_base.get_chapter(chapter_number)
            if not chapter:
                console.print(f"[red]ERROR: Chapter {chapter_number} not found in outline.[/red]")
                return
            
            if not chapter.scenes:
                console.print(f"[yellow]WARNING: Chapter {chapter_number} has no scenes defined.[/yellow]")
                return
            
            # Sort scenes by scene number
            ordered_scenes = sorted(chapter.scenes, key=lambda s: s.scene_number)
            
            console.print(f"\n[bold cyan]Writing Chapter {chapter_number}: {chapter.title}[/bold cyan]")
            console.print(f"[dim]Scenes to write: {len(ordered_scenes)}[/dim]\n")
            
            # Get previous chapter summary for continuity
            previous_chapter_summary = self._get_previous_chapter_summary(project_knowledge_base, chapter_number)
            
            # Get style guide and pacing
            style_guide = prompts.get_style_guide(project_knowledge_base)
            pacing_instruction = prompts.get_pacing_instruction(project_knowledge_base)
            character_appearances = prompts.get_character_appearances(project_knowledge_base)
            
            scene_contents = []
            
            for i, scene in enumerate(ordered_scenes, 1):
                console.print(f"[yellow]Writing Scene {scene.scene_number}/{len(ordered_scenes)}...[/yellow]")
                
                # Build character context for this scene
                character_context = self._build_character_context(scene.characters, project_knowledge_base)
                
                # Build world context
                world_context = self._build_world_context(project_knowledge_base)
                
                # Build previous scenes context (for continuity within chapter)
                previous_scenes_text = self._build_previous_scenes_context(scene_contents)
                
                # Create a prompt for this specific scene with full context
                scene_prompt = prompts.SCENE_PROMPT.format(
                    chapter_number=chapter_number,
                    chapter_title=chapter.title,
                    book_title=project_knowledge_base.title,
                    genre=project_knowledge_base.genre,
                    category=project_knowledge_base.category,
                    language=project_knowledge_base.language,
                    chapter_summary=chapter.summary,
                    scene_number=scene.scene_number,
                    scene_summary=scene.summary,
                    characters=", ".join(scene.characters) if scene.characters else "None specified",
                    character_details=character_context,
                    character_appearances=character_appearances,
                    world_details=world_context,
                    setting=scene.setting if scene.setting else "None specified",
                    goal=scene.goal if scene.goal else "None specified",
                    emotional_beat=scene.emotional_beat if scene.emotional_beat else "None specified",
                    total_scenes=len(ordered_scenes),
                    previous_chapter_summary=previous_chapter_summary,
                    previous_scenes=previous_scenes_text,
                    style_guide=style_guide,
                    pacing_instruction=pacing_instruction
                )
                
                # Generate the scene content with higher token limit for rich scenes
                scene_content = self.llm_client.generate_content(scene_prompt, max_tokens=4000)
                if not scene_content:
                    console.print(f"[yellow]Warning: Failed to generate content for Scene {scene.scene_number}. Using placeholder.[/yellow]")
                    scene_content = f"[Scene {scene.scene_number} content unavailable]"
                
                scene_contents.append(scene_content)
                console.print(f"[green]  ✓ Scene {scene.scene_number} complete ({len(scene_content)} chars)[/green]")
            
            
            # Combine scenes into a complete chapter
            chapter_content = f"## Chapter {chapter_number}: {chapter.title}\n\n"
            chapter_content += "\n\n---\n\n".join(scene_contents)
            
            # Save the chapter
            if output_path is None:
                output_path = str(Path(project_knowledge_base.project_dir) / f"chapter_{chapter_number}.md")
            write_markdown_file(output_path, chapter_content)
            
            console.print(f"[green]✅ Chapter {chapter_number} completed with {len(ordered_scenes)} scenes![/green]")
            
        except Exception as e:
            self.logger.exception(f"Error writing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to write chapter {chapter_number}. See log for details.[/red]")
    
    def _get_previous_chapter_summary(self, knowledge_base: ProjectKnowledgeBase, chapter_number: int) -> str:
        """Get summary of previous chapter for continuity."""
        if chapter_number <= 1:
            return "This is the first chapter - no previous events."
        
        prev_chapter = knowledge_base.get_chapter(chapter_number - 1)
        if prev_chapter:
            summary = prev_chapter.summary or "No summary available."
            return f"**Chapter {chapter_number - 1}: {prev_chapter.title}**\n{summary}"
        
        # Try to read the actual previous chapter file for more context
        prev_file = Path(knowledge_base.project_dir) / f"chapter_{chapter_number - 1}.md"
        if prev_file.exists():
            try:
                content = prev_file.read_text(encoding='utf-8')
                # Return last ~500 chars as context
                if len(content) > 500:
                    return f"[End of previous chapter]:\n...{content[-500:]}"
                return content
            except Exception:
                pass
        
        return "Previous chapter summary not available."
    
    def _build_previous_scenes_context(self, previous_scene_contents: List[str]) -> str:
        """Build context from already-written scenes in this chapter."""
        if not previous_scene_contents:
            return "This is the first scene of the chapter."
        
        # For efficiency, only include summaries/endings of previous scenes
        context_parts = []
        for i, scene in enumerate(previous_scene_contents, 1):
            # Get last 300 chars of each previous scene
            if len(scene) > 300:
                context_parts.append(f"**Scene {i} (ending):** ...{scene[-300:]}")
            else:
                context_parts.append(f"**Scene {i}:** {scene}")
        
        return "\n\n".join(context_parts)
    
    def _build_character_context(self, character_names: List[str], knowledge_base: ProjectKnowledgeBase) -> str:
        """Build detailed character context from characters.json."""
        if not character_names:
            return "No characters specified"
        
        context_parts = []
        for name in character_names:
            char = knowledge_base.get_character(name)
            if char:
                details = [f"**{name}**:"]
                
                # Add all available character attributes
                if hasattr(char, 'appearance') and char.appearance:
                    details.append(f"  - Appearance: {char.appearance}")
                if hasattr(char, 'physical_description') and char.physical_description:
                    details.append(f"  - Physical: {char.physical_description}")
                if hasattr(char, 'personality_traits') and char.personality_traits:
                    traits = char.personality_traits if isinstance(char.personality_traits, str) else ', '.join(char.personality_traits)
                    details.append(f"  - Personality: {traits}")
                if hasattr(char, 'role') and char.role:
                    details.append(f"  - Role: {char.role}")
                if hasattr(char, 'backstory') and char.backstory:
                    # Truncate long backstories
                    backstory = char.backstory[:300] + "..." if len(char.backstory) > 300 else char.backstory
                    details.append(f"  - Backstory: {backstory}")
                if hasattr(char, 'motivations') and char.motivations:
                    details.append(f"  - Motivations: {char.motivations}")
                
                context_parts.append('\n'.join(details))
        
        return '\n\n'.join(context_parts) if context_parts else "Character details not available"
    
    def _build_world_context(self, knowledge_base: ProjectKnowledgeBase) -> str:
        """Build world context from worldbuilding data."""
        try:
            # Access worldbuilding data from knowledge base
            if hasattr(knowledge_base, 'worldbuilding') and knowledge_base.worldbuilding:
                world = knowledge_base.worldbuilding
                context_parts = []
                
                # Handle as object with attributes
                if hasattr(world, '__dict__'):
                    for key, value in world.__dict__.items():
                        if value and key not in ['id', 'created_at'] and isinstance(value, str) and value.strip():
                            # Truncate long values
                            display_val = value[:200] + "..." if len(value) > 200 else value
                            context_parts.append(f"**{key.replace('_', ' ').title()}**: {display_val}")
                # Handle as dict
                elif isinstance(world, dict):
                    for key, value in world.items():
                        if value and key not in ['id', 'created_at'] and isinstance(value, str):
                            display_val = value[:200] + "..." if len(value) > 200 else value
                            context_parts.append(f"**{key.replace('_', ' ').title()}**: {display_val}")
                
                return '\n'.join(context_parts) if context_parts else "World details not available"
            
            return "World details not available"
        except Exception as e:
            logger.warning(f"Could not build world context: {e}")
            return "World details not available"