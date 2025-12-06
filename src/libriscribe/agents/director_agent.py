# src/libriscribe/agents/director_agent.py

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console

from libriscribe.agents.agent_base import Agent
from libriscribe.agents.intent_parser import IntentParser
from libriscribe.agents.impact_analyzer import ImpactAnalyzer
from libriscribe.agents.change_handlers.character_gender_handler import CharacterGenderHandler
from libriscribe.agents.change_handlers.grammar_correction_handler import GrammarCorrectionHandler
from libriscribe.agents.change_handlers.pronoun_fixer_handler import PronounFixerHandler
from libriscribe.agents.change_handlers.autonomous_character_handler import AutonomousCharacterHandler
from libriscribe.agents.change_handlers.report_analyzer_handler import ReportAnalyzerHandler
from libriscribe.agents.change_handlers.execute_action_plan_handler import ExecuteActionPlanHandler
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class DirectorAgent(Agent):
    """
    Director Agent - Natural language interface for creative control.
    
    Interprets user commands like "Make M a man" and orchestrates
    changes across the entire project.
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base: ProjectKnowledgeBase):
        super().__init__("DirectorAgent", llm_client)
        self.project_dir = project_dir
        self.project_knowledge_base = project_knowledge_base
        
        # Initialize sub-components
        self.intent_parser = IntentParser(llm_client)
        self.impact_analyzer = ImpactAnalyzer(project_dir)
        
        # Initialize change handlers
        self.handlers = {
            "character_gender": AutonomousCharacterHandler(llm_client, project_dir, project_knowledge_base),  # Use autonomous for gender changes
            "character_attribute": AutonomousCharacterHandler(llm_client, project_dir, project_knowledge_base),  # New: any character attribute
            "grammar_correction": GrammarCorrectionHandler(llm_client, project_dir, project_knowledge_base),
            "pronoun_fix": PronounFixerHandler(llm_client, project_dir, project_knowledge_base),
            "analyze_reports": ReportAnalyzerHandler(llm_client, project_dir, project_knowledge_base),  # New: analyze editorial reports
            "execute_action_plan": ExecuteActionPlanHandler(llm_client, project_dir, project_knowledge_base)  # New: execute action plan
        }
        
        logger.info("DirectorAgent initialized")
    
    def execute(self, user_command: str) -> Dict[str, Any]:
        """
        Execute a natural language creative direction.
        
        Args:
            user_command: Natural language command (e.g., "Make M a man")
            
        Returns:
            Dict with execution results
        """
        try:
            console.print(f"\n[bold cyan]🎬 Director Mode[/bold cyan]")
            console.print(f"[dim]Command: {user_command}[/dim]\n")
            
            # Step 1: Parse intent
            console.print("[cyan]🔍 Analyzing request...[/cyan]")
            intent = self.intent_parser.parse(user_command)
            
            if not intent or intent.get("type") == "unknown":
                console.print("[red]❌ Could not understand command[/red]")
                return {"success": False, "error": "Unknown command"}
            
            console.print(f"[green]✓ Identified: {intent['type']}[/green]")
            
            # Step 2: Analyze impact
            console.print("\n[cyan]📊 Analyzing impact...[/cyan]")
            impact = self.impact_analyzer.analyze(intent)
            
            # Display impact report
            self._display_impact(impact)
            
            # Step 3: Confirm with user
            if not self._confirm_changes(impact):
                console.print("[yellow]⚠️  Changes cancelled[/yellow]")
                return {"success": False, "cancelled": True}
            
            # Step 4: Execute changes
            console.print("\n[cyan]🚀 Executing changes...[/cyan]")
            handler = self.handlers.get(intent["type"])
            
            if not handler:
                console.print(f"[red]❌ No handler for {intent['type']}[/red]")
                return {"success": False, "error": f"Unsupported change type: {intent['type']}"}
            
            result = handler.execute(intent, impact)
            
            # Step 5: Report completion
            if result.get("success"):
                console.print("\n[bold green]✅ Changes complete![/bold green]")
                self._display_completion(result)
            else:
                console.print(f"\n[red]❌ Changes failed: {result.get('error')}[/red]")
            
            return result
            
        except Exception as e:
            logger.exception(f"Error executing director command: {e}")
            console.print(f"[red]❌ Error: {e}[/red]")
            return {"success": False, "error": str(e)}
    
    def _display_impact(self, impact: Dict[str, Any]):
        """Display impact analysis to user."""
        console.print(f"   [cyan]•[/cyan] {impact.get('affected_chapters', 0)} chapters affected")
        console.print(f"   [cyan]•[/cyan] {impact.get('changes_count', 0)} changes to make")
        
        if impact.get('regenerations'):
            console.print(f"   [cyan]•[/cyan] {len(impact['regenerations'])} scenes to regenerate")
        
        if impact.get('estimated_time_minutes'):
            console.print(f"   [cyan]•[/cyan] Estimated time: {impact['estimated_time_minutes']} minutes")
        
        if impact.get('estimated_cost_usd'):
            console.print(f"   [cyan]•[/cyan] Estimated cost: ${impact['estimated_cost_usd']:.2f}")
    
    def _confirm_changes(self, impact: Dict[str, Any]) -> bool:
        """Ask user to confirm changes."""
        import typer
        response = typer.prompt("\n💰 Proceed with changes? [Y/n]", default="Y")
        return response.lower() in ['y', 'yes', '']
    
    def _display_completion(self, result: Dict[str, Any]):
        """Display completion report."""
        if result.get('changes_applied'):
            console.print(f"\n[green]✓ Applied {result['changes_applied']} changes[/green]")
        
        if result.get('chapters_updated'):
            console.print(f"[green]✓ Updated {len(result['chapters_updated'])} chapters[/green]")
        
        if result.get('review_recommended'):
            console.print("\n[yellow]📝 Review recommended:[/yellow]")
            for chapter in result['review_recommended']:
                console.print(f"   [yellow]•[/yellow] Chapter {chapter}")
