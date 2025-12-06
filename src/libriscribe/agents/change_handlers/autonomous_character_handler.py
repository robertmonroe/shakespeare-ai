# src/libriscribe/agents/change_handlers/autonomous_character_handler.py

import logging
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from libriscribe.agents.autonomous.project_file_scanner import ProjectFileScanner
from libriscribe.agents.autonomous.change_analyzer import ChangeAnalyzer
from libriscribe.agents.autonomous.autonomous_executor import AutonomousExecutor
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class AutonomousCharacterHandler:
    """
    Autonomous handler for character changes.
    
    Uses LLM to analyze and update ALL project files for complete consistency.
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base: ProjectKnowledgeBase):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
        
        # Initialize autonomous components
        self.scanner = ProjectFileScanner(project_dir)
        self.analyzer = ChangeAnalyzer(llm_client)
        self.executor = AutonomousExecutor(llm_client, project_dir)
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute autonomous character change across all project files.
        
        Args:
            intent: Parsed intent
            impact: Impact analysis
            
        Returns:
            Dict with execution results
        """
        try:
            character_name = intent.get("character")
            user_command = intent.get("raw_command", f"Change character {character_name}")
            
            # Step 1: Scan all project files
            console.print("   [cyan]📂[/cyan] Scanning project files...")
            project_files = self.scanner.scan_project()
            
            if not project_files:
                return {"success": False, "error": "No project files found"}
            
            console.print(f"   [green]✓[/green] Found {len(project_files)} files")
            
            # Step 2: Analyze what needs changing
            console.print("   [cyan]🔍[/cyan] Analyzing changes...")
            change_plan = self.analyzer.analyze_change(
                user_command,
                project_files,
                character_name
            )
            
            if not change_plan:
                return {"success": False, "error": "No changes identified"}
            
            console.print(f"   [green]✓[/green] {len(change_plan)} files need updates")
            
            # Step 3: Execute changes
            console.print("   [cyan]✏️[/cyan] Applying changes...")
            results = self.executor.execute_changes(change_plan, project_files)
            
            if results["success"]:
                console.print(f"   [green]✓[/green] Updated {len(results['files_updated'])} files")
            
            # Add review recommendations
            results["review_recommended"] = results.get("files_updated", [])[:5]
            
            return results
            
        except Exception as e:
            logger.exception(f"Error in autonomous character handler: {e}")
            return {"success": False, "error": str(e)}
