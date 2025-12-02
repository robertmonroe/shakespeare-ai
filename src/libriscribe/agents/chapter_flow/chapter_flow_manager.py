# src/libriscribe/agents/chapter_flow/chapter_flow_manager.py

import logging
from pathlib import Path
from typing import Dict, Any, Optional

import typer
from rich.console import Console

from libriscribe.agents.chapter_flow.backup_manager import BackupManager
from libriscribe.agents.chapter_flow.review_manager import ReviewManager
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
        """Edit a chapter using the editor agent.
        
        Args:
            chapter_number: The chapter number to edit
        """
        try:
            # EditorAgent will print its own status message
            self.agents["editor"].execute(
                project_knowledge_base=self.project_knowledge_base,
                chapter_number=chapter_number
            )
            
            logger.info(f"Chapter {chapter_number} edited successfully")
            
        except Exception as e:
            logger.exception(f"Error editing chapter {chapter_number}: {e}")
            console.print(f"[red]ERROR: Failed to edit chapter {chapter_number}[/red]")

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
