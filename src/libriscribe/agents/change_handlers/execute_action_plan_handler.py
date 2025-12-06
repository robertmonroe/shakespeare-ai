# src/libriscribe/agents/change_handlers/execute_action_plan_handler.py

import logging
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from libriscribe.agents.autonomous.action_plan_parser import ActionPlanParser
from libriscribe.agents.autonomous.recommendation_interpreter import RecommendationInterpreter
from libriscribe.agents.change_handlers.autonomous_character_handler import AutonomousCharacterHandler
from libriscribe.knowledge_base import ProjectKnowledgeBase
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class ExecuteActionPlanHandler:
    """
    Executes all recommendations in editorial_action_plan.md.
    
    Reads the action plan, interprets each recommendation,
    and applies changes using the Autonomous Modifier.
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base: ProjectKnowledgeBase):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
        
        # Initialize components
        self.parser = ActionPlanParser()
        self.interpreter = RecommendationInterpreter(llm_client)
        self.autonomous_handler = AutonomousCharacterHandler(llm_client, project_dir, project_knowledge_base)
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all recommendations in the action plan.
        
        Args:
            intent: Parsed intent
            impact: Impact analysis
            
        Returns:
            Dict with execution results
        """
        try:
            plan_path = self.project_dir / "editorial_action_plan.md"
            
            if not plan_path.exists():
                return {"success": False, "error": "No action plan found. Run 'analyze reports' first."}
            
            # Parse action plan
            console.print("   [cyan]📋[/cyan] Reading action plan...")
            recommendations = self.parser.parse_action_plan(plan_path)
            
            if not recommendations:
                return {"success": False, "error": "No recommendations found in action plan"}
            
            # Filter out completed items
            pending = [r for r in recommendations if not r["completed"]]
            
            if not pending:
                return {"success": True, "message": "All recommendations already completed!"}
            
            console.print(f"   [green]✓[/green] Found {len(pending)} pending recommendation(s)")
            
            # Execute each recommendation
            results = {
                "success": True,
                "total_recommendations": len(pending),
                "completed": 0,
                "failed": 0,
                "files_updated": set(),
                "errors": []
            }
            
            for i, rec in enumerate(pending, 1):
                console.print(f"\n   [cyan]📋[/cyan] Recommendation {i}/{len(pending)}: {rec['text'][:60]}...")
                
                try:
                    # Interpret recommendation
                    console.print(f"      [cyan]🔍[/cyan] Interpreting...")
                    interpretation = self.interpreter.interpret_recommendation(rec["text"])
                    
                    console.print(f"      [green]✓[/green] Command: {interpretation['command'][:50]}...")
                    
                    # Execute using autonomous handler
                    console.print(f"      [cyan]⚙️[/cyan] Executing...")
                    
                    exec_intent = {
                        "type": "character_attribute",  # Use autonomous handler
                        "raw_command": interpretation["command"]
                    }
                    
                    exec_result = self.autonomous_handler.execute(exec_intent, {})
                    
                    if exec_result.get("success"):
                        # Mark as complete
                        self.parser.mark_as_complete(plan_path, rec["id"])
                        
                        results["completed"] += 1
                        if "files_updated" in exec_result:
                            results["files_updated"].update(exec_result["files_updated"])
                        
                        console.print(f"      [green]✅[/green] Recommendation {i} complete")
                    else:
                        results["failed"] += 1
                        error_msg = exec_result.get("error", "Unknown error")
                        results["errors"].append(f"Rec {i}: {error_msg}")
                        console.print(f"      [red]❌[/red] Failed: {error_msg}")
                
                except Exception as e:
                    logger.exception(f"Error executing recommendation {i}: {e}")
                    results["failed"] += 1
                    results["errors"].append(f"Rec {i}: {str(e)}")
                    console.print(f"      [red]❌[/red] Error: {str(e)}")
            
            # Summary
            results["files_updated"] = list(results["files_updated"])
            results["success"] = results["failed"] == 0
            
            return results
            
        except Exception as e:
            logger.exception(f"Error executing action plan: {e}")
            return {"success": False, "error": str(e)}
