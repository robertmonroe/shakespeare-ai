# src/libriscribe/agents/chapter_flow/chapter_flow_manager.py

import logging
from pathlib import Path
from typing import Dict, Any, Optional

import typer
from rich.console import Console

from libriscribe.agents.chapter_flow.backup_manager import BackupManager
from libriscribe.agents.chapter_flow.review_manager import ReviewManager
from libriscribe.agents.decision_agent import DecisionAgent
from libriscribe.agents.task_based_editor import TaskBasedEditor
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class ChapterFlowManager:
    """Manages the complete chapter writing, review, and editing workflow."""

    def __init__(
        self,
        llm_client: LLMClient,
        project_dir: Path,
        project_knowledge_base: ProjectKnowledgeBase,
        agents: Dict[str, Any]
    ):
        """Initialize the chapter flow manager.
        
        Args:
            llm_client: The LLM client instance
            project_dir: The project directory path
            project_knowledge_base: The project knowledge base
            agents: Dictionary of initialized agents
        """
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
        self.agents = agents
        
        # Initialize sub-managers
        self.backup_manager = BackupManager(self.project_dir)
        self.review_manager = ReviewManager(llm_client, self.project_dir, project_knowledge_base)
        
        logger.info(f"ChapterFlowManager initialized for {project_dir}")

    def get_chapter_path(self, chapter_number: int) -> Path:
        """Get the path for a chapter file.
        
        Args:
            chapter_number: The chapter number
            
        Returns:
            Path: The chapter file path
        """
        return self.project_dir / f"chapter_{chapter_number}.md"

    def write_chapter(self, chapter_number: int) -> None:
        """Write a chapter using the chapter writer agent.
        
        Args:
            chapter_number: The chapter number to write
        """
        try:
            chapter_path = self.get_chapter_path(chapter_number)
            
            console.print(f"[bold cyan]✍️ Writing Chapter {chapter_number}...[/bold cyan]")
            
            # Use the chapter writer agent
            self.agents["chapter_writer"].execute(
                project_knowledge_base=self.project_knowledge_base,
                chapter_number=chapter_number,
                output_path=str(chapter_path)
            )
            
            logger.info(f"Chapter {chapter_number} written successfully")
            
        except Exception as e:
            logger.exception(f"Error writing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to write chapter {chapter_number}[/red]")

    def review_chapter(self, chapter_number: int) -> Dict[str, Any]:
        """Review a chapter's content.
        
        Args:
            chapter_number: The chapter number to review
            
        Returns:
            Dict containing review results
        """
        try:
            chapter_path = self.get_chapter_path(chapter_number)
            
            if not chapter_path.exists():
                console.print(f"[red]ERROR: Chapter {chapter_number} does not exist[/red]")
                return {}

            chapter_text = chapter_path.read_text(encoding="utf-8")
            return self.review_manager.review_chapter(chapter_number, chapter_text)
            
        except Exception as e:
            logger.exception(f"Error reviewing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to review chapter {chapter_number}[/red]")
            return {}

    def edit_chapter(self, chapter_number: int) -> None:
        """Edit a chapter using task-based system.
        
        Args:
            chapter_number: The chapter number to edit
        """
        try:
            # Load review
            review_path = self.project_dir / "reviews" / f"chapter_{chapter_number}_review.md"
            if not review_path.exists():
                console.print(f"[red]❌ No review found for Chapter {chapter_number}[/red]")
                console.print(f"[yellow]Run review first before editing[/yellow]")
                return
            
            review_text = review_path.read_text(encoding="utf-8")
            
            # DEBUG: Show what we're loading
            console.print(f"[dim]Loading review from: {review_path}[/dim]")
            console.print(f"[dim]Review length: {len(review_text)} chars[/dim]")
            console.print(f"[dim]First 200 chars: {review_text[:200]}...[/dim]")
            
            # 1. Decision Agent creates task list
            decision_agent = DecisionAgent(self.llm_client)
            task_list = decision_agent.create_task_list(review_text)
            
            if not task_list:
                console.print(f"[yellow]⚠️  No tasks created for Chapter {chapter_number}[/yellow]")
                return
            
            # 2. Task-Based Editor applies tasks
            editor = TaskBasedEditor(self.llm_client)
            
            chapter_path = self.get_chapter_path(chapter_number)
            chapter_text = chapter_path.read_text(encoding="utf-8")
            
            # Build context
            context = {
                'characters': self._build_character_context(),
                'worldbuilding': self._build_worldbuilding_context()
            }
            
            result = editor.execute(chapter_text, task_list, context)
            
            # 3. Create backup before saving edited chapter
            backup_path = self.backup_manager.create_backup(chapter_path)
            if backup_path:
                console.print(f"[blue]💾 Backup created: {Path(backup_path).name}[/blue]")
            
            # 4. Save edited chapter
            chapter_path.write_text(result['edited_chapter'], encoding="utf-8")
            
            summary = result['completion_summary']
            console.print(f"[green]✅ Chapter {chapter_number} edited[/green]")
            console.print(f"   {summary['completed']}/{summary['total_tasks']} tasks completed")
            console.print(f"   Success rate: {summary['success_rate']*100:.0f}%")
            
            logger.info(f"Chapter {chapter_number} edited: {summary['completed']}/{summary['total_tasks']} tasks")
            
        except Exception as e:
            logger.exception(f"Error editing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to edit chapter {chapter_number}[/red]")
    
    def _build_character_context(self) -> str:
        """Build character context string for editor."""
        try:
            characters = self.project_knowledge_base.characters
            if not characters:
                return "No characters defined"
            
            context_parts = []
            for name, char in characters.items():
                role = getattr(char, 'role', '')
                traits = getattr(char, 'personality_traits', [])
                if isinstance(traits, list):
                    traits_str = ', '.join(traits) if traits else 'No traits'
                else:
                    traits_str = str(traits)
                context_parts.append(f"- {name} ({role}): {traits_str}")
            
            return "\n".join(context_parts)
        except Exception as e:
            logger.error(f"Error building character context: {e}")
            return "Error loading characters"
    
    def _build_worldbuilding_context(self) -> str:
        """Build worldbuilding context string for editor."""
        try:
            worldbuilding = self.project_knowledge_base.worldbuilding
            if not worldbuilding:
                return "No worldbuilding defined"
            
            # Worldbuilding is an object, convert to string representation
            context_parts = []
            
            # Get all attributes from the worldbuilding object
            if hasattr(worldbuilding, '__dict__'):
                for key, value in worldbuilding.__dict__.items():
                    if not key.startswith('_') and value:
                        if isinstance(value, str):
                            context_parts.append(f"- {key}: {value}")
                        elif isinstance(value, list):
                            context_parts.append(f"- {key}: {', '.join(str(v) for v in value)}")
                        else:
                            context_parts.append(f"- {key}: {str(value)}")
            
            return "\n".join(context_parts) if context_parts else "No worldbuilding defined"
        except Exception as e:
            logger.error(f"Error building worldbuilding context: {e}")
            return "Error loading worldbuilding"

    def write_and_review_chapter_ai_mode(self, chapter_number: int) -> str:
        """AI-mode enhanced write-review-edit workflow with backups.
        
        Args:
            chapter_number: The chapter number to process
            
        Returns:
            str: "next" to continue to next chapter, "finish" to complete
        """
        # Write initial chapter
        console.print(f"[bold cyan]✍️ Writing Chapter {chapter_number}...[/bold cyan]")
        self.write_chapter(chapter_number)
        
        # Initial review
        self.review_chapter(chapter_number)

        # Check if auto-pass mode is enabled
        auto_mode = getattr(self.project_knowledge_base, 'auto_review_mode', False)
        auto_passes = getattr(self.project_knowledge_base, 'auto_review_passes', 0)
        
        if auto_mode and auto_passes > 0:
            # AUTO MODE: Run configured number of passes automatically
            console.print(f"\n[bold cyan]🤖 Auto-Review Mode: {auto_passes} passes[/bold cyan]")
            
            for pass_num in range(1, auto_passes + 1):
                console.print(f"\n[yellow]➡️  Pass {pass_num} of {auto_passes}[/yellow]")
                
                # Apply edits (backup is created automatically by the system)
                console.print(f"[cyan]✏️  Editing...[/cyan]")
                self.edit_chapter(chapter_number)
                
                # Review the edited version
                console.print(f"[cyan]🔍 Reviewing...[/cyan]")
                self.review_chapter(chapter_number)
                
                console.print(f"[green]✓ Pass {pass_num} complete[/green]")
            
            console.print(f"\n[bold green]✅ All {auto_passes} passes complete![/bold green]")
            
            # Determine if this is the last chapter
            total_chapters = len(self.project_knowledge_base.chapters) if self.project_knowledge_base.chapters else 1
            is_last_chapter = chapter_number >= total_chapters
            
            return "finish" if is_last_chapter else "next"

        # Determine if this is the last chapter
        total_chapters = len(self.project_knowledge_base.chapters) if self.project_knowledge_base.chapters else 1
        is_last_chapter = chapter_number >= total_chapters

        # Interactive loop for AI mode
        while True:
            console.print("[bold yellow]What would you like to do next?[/bold yellow]")
            console.print("1. Apply review fixes")
            console.print("2. Restore a backup")
            console.print(f"3. {'Finish book' if is_last_chapter else 'Write next chapter'}")
            
            choice = typer.prompt("Enter choice").strip()

            if choice == "1":
                # Create backup before editing
                chapter_path = self.get_chapter_path(chapter_number)
                backup_path = self.backup_manager.create_backup(chapter_path)
                
                if backup_path:
                    console.print(f"[blue]Backup created: {Path(backup_path).name}[/blue]")
                
                # Apply edits
                self.edit_chapter(chapter_number)
                
                # Review the edited version
                self.review_chapter(chapter_number)
                continue

            elif choice == "2":
                # List and restore backups
                backups = self.backup_manager.list_backups(chapter_number)
                
                if not backups:
                    console.print("[red]No backups available.[/red]")
                    continue
                
                console.print("[bold]Available backups:[/bold]")
                for i, backup in enumerate(backups, 1):
                    console.print(f"{i}. {backup.name}")
                
                try:
                    idx = int(typer.prompt("Which backup to restore?"))
                    selected_backup = backups[idx - 1]
                    
                    if self.backup_manager.restore_backup(selected_backup, chapter_number):
                        console.print(f"[green]✓ Restored {selected_backup.name}[/green]")
                        # Review the restored version
                        self.review_chapter(chapter_number)
                    else:
                        console.print("[red]Failed to restore backup.[/red]")
                        
                except (ValueError, IndexError):
                    console.print("[red]Invalid choice.[/red]")
                    
                continue

            elif choice == "3":
                return "finish" if is_last_chapter else "next"

            else:
                console.print("[red]Invalid selection.[/red]")

    def write_and_review_chapter_human_mode(self, chapter_number: int) -> str:
        """Human-mode write and review workflow (original behavior).
        
        Args:
            chapter_number: The chapter number to process
            
        Returns:
            str: "next" to continue
        """
        self.write_chapter(chapter_number)
        self.review_chapter(chapter_number)
        return "next"

    def write_and_review_chapter(self, chapter_number: int) -> str:
        """Main entry point for write and review workflow.
        
        Delegates to AI or Human mode based on project preferences.
        
        Args:
            chapter_number: The chapter number to process
            
        Returns:
            str: "next" or "finish"
        """
        review_preference = self.project_knowledge_base.review_preference.lower().strip()
        is_ai_mode = "ai" in review_preference

        if is_ai_mode:
            return self.write_and_review_chapter_ai_mode(chapter_number)
        else:
            return self.write_and_review_chapter_human_mode(chapter_number)
