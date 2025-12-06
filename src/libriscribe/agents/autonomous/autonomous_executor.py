# src/libriscribe/agents/autonomous/autonomous_executor.py

import logging
from pathlib import Path
from typing import Dict, List, Any

from rich.console import Console
from libriscribe.utils.llm_client import LLMClient

console = Console()
logger = logging.getLogger(__name__)


class AutonomousExecutor:
    """
    Executes changes across all project files using LLM guidance.
    
    For each file in the change plan, uses LLM to make the changes.
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
    
    def execute_changes(
        self,
        change_plan: Dict[str, List[str]],
        project_files: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Execute changes across all files.
        
        Args:
            change_plan: Dict of {filename: [changes to make]}
            project_files: Dict of {filename: current content}
            
        Returns:
            Dict with execution results
        """
        results = {
            "success": True,
            "files_updated": [],
            "changes_applied": 0,
            "errors": []
        }
        
        total_files = len(change_plan)
        
        for i, (filename, changes) in enumerate(change_plan.items(), 1):
            console.print(f"   [cyan]✓[/cyan] Updating {filename} ({i}/{total_files})")
            
            try:
                current_content = project_files.get(filename, "")
                
                if not current_content:
                    logger.warning(f"File {filename} not found in project files")
                    continue
                
                # Use LLM to make the changes
                updated_content = self._apply_changes_to_file(
                    filename,
                    current_content,
                    changes
                )
                
                if updated_content and updated_content != current_content:
                    # Write updated file
                    file_path = self.project_dir / filename
                    file_path.write_text(updated_content, encoding='utf-8')
                    
                    results["files_updated"].append(filename)
                    results["changes_applied"] += len(changes)
                    
                    logger.info(f"Updated {filename} with {len(changes)} changes")
                
            except Exception as e:
                logger.exception(f"Error updating {filename}: {e}")
                results["errors"].append(f"{filename}: {str(e)}")
                results["success"] = False
        
        return results
    
    def _apply_changes_to_file(
        self,
        filename: str,
        current_content: str,
        changes: List[str]
    ) -> str:
        """
        Use LLM to apply changes to a file.
        
        Args:
            filename: Name of the file
            current_content: Current file content
            changes: List of changes to make
            
        Returns:
            Updated file content
        """
        changes_text = "\n".join([f"{i+1}. {change}" for i, change in enumerate(changes)])
        
        prompt = f"""Update this file by making the specified changes.

File: {filename}

Current content:
{current_content}

Changes to make:
{changes_text}

Return the COMPLETE updated file content with all changes applied.
Output ONLY the file content, no explanations.
"""
        
        try:
            updated_content = self.llm_client.generate_content(
                prompt,
                max_tokens=8000,
                temperature=0.1
            )
            
            return updated_content.strip()
            
        except Exception as e:
            logger.exception(f"Error applying changes to {filename}: {e}")
            return current_content
