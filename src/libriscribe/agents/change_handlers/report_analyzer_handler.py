# src/libriscribe/agents/change_handlers/report_analyzer_handler.py

import logging
from pathlib import Path
from typing import Dict, Any, List

from rich.console import Console
from libriscribe.utils.llm_client import LLMClient
from libriscribe.utils.document_reader import DocumentReader

console = Console()
logger = logging.getLogger(__name__)


class ReportAnalyzerHandler:
    """
    Analyzes editorial reports from any source (AutoCrit, ProWritingAid, etc.)
    and creates action plans and task lists.
    
    Supports: TXT, MD, RTF, DOCX, PDF
    """
    
    def __init__(self, llm_client: LLMClient, project_dir: Path, project_knowledge_base):
        self.llm_client = llm_client
        self.project_dir = Path(project_dir)
        self.project_knowledge_base = project_knowledge_base
        self.doc_reader = DocumentReader()
    
    def execute(self, intent: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze reports and create action plan.
        
        Args:
            intent: Parsed intent with folder path
            impact: Impact analysis
            
        Returns:
            Dict with execution results
        """
        try:
            folder_path = intent.get("folder_path", "reports")
            report_folder = self.project_dir / folder_path
            
            # Read all documents in folder
            console.print(f"   [cyan]📂[/cyan] Reading reports from {folder_path}...")
            reports = self.doc_reader.read_folder(report_folder)
            
            if not reports:
                return {"success": False, "error": f"No reports found in {folder_path}"}
            
            console.print(f"   [green]✓[/green] Found {len(reports)} report(s)")
            
            # Analyze reports with LLM
            console.print("   [cyan]🔍[/cyan] Analyzing reports...")
            analysis = self._analyze_reports(reports)
            
            if not analysis:
                return {"success": False, "error": "Failed to analyze reports"}
            
            # Create action plan
            console.print("   [cyan]📋[/cyan] Creating action plan...")
            action_plan = self._create_action_plan(analysis)
            
            # Save action plan
            plan_path = self.project_dir / "editorial_action_plan.md"
            plan_path.write_text(action_plan, encoding='utf-8')
            
            console.print(f"   [green]✓[/green] Action plan saved to editorial_action_plan.md")
            
            return {
                "success": True,
                "reports_analyzed": len(reports),
                "action_plan_path": str(plan_path),
                "review_recommended": ["editorial_action_plan.md"]
            }
            
        except Exception as e:
            logger.exception(f"Error analyzing reports: {e}")
            return {"success": False, "error": str(e)}
    
    def _analyze_reports(self, reports: Dict[str, str]) -> Dict[str, Any]:
        """Use LLM to analyze all reports and extract findings."""
        
        # Combine all reports
        combined_reports = "\n\n---\n\n".join([
            f"**{filename}**\n\n{content}"
            for filename, content in reports.items()
        ])
        
        prompt = f"""Analyze these editorial reports and extract key findings.

Reports:
{combined_reports[:15000]}  # Limit to avoid token overflow

Extract:
1. **Major Issues** - Critical problems that need fixing
2. **Minor Issues** - Small improvements
3. **Strengths** - What's working well
4. **Recommendations** - Specific actions to take

Output as JSON:
{{
  "major_issues": ["issue 1", "issue 2", ...],
  "minor_issues": ["issue 1", "issue 2", ...],
  "strengths": ["strength 1", "strength 2", ...],
  "recommendations": ["rec 1", "rec 2", ...]
}}
"""
        
        try:
            response = self.llm_client.generate_content(prompt, max_tokens=2000, temperature=0.1)
            
            # Extract JSON
            import json
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start >= 0 and end > start:
                return json.loads(response[start:end])
            
            return None
            
        except Exception as e:
            logger.exception(f"Error analyzing reports: {e}")
            return None
    
    def _create_action_plan(self, analysis: Dict[str, Any]) -> str:
        """Create a markdown action plan from analysis."""
        
        plan = "# Editorial Action Plan\n\n"
        plan += "*Generated from editorial reports*\n\n"
        plan += "---\n\n"
        
        # Major Issues
        plan += "## 🔴 Major Issues (High Priority)\n\n"
        for i, issue in enumerate(analysis.get("major_issues", []), 1):
            plan += f"{i}. {issue}\n"
        plan += "\n"
        
        # Minor Issues
        plan += "## 🟡 Minor Issues (Medium Priority)\n\n"
        for i, issue in enumerate(analysis.get("minor_issues", []), 1):
            plan += f"{i}. {issue}\n"
        plan += "\n"
        
        # Strengths
        plan += "## ✅ Strengths\n\n"
        for i, strength in enumerate(analysis.get("strengths", []), 1):
            plan += f"{i}. {strength}\n"
        plan += "\n"
        
        # Recommendations
        plan += "## 📝 Recommended Actions\n\n"
        for i, rec in enumerate(analysis.get("recommendations", []), 1):
            plan += f"- [ ] {rec}\n"
        plan += "\n"
        
        plan += "---\n\n"
        plan += "*Use Director Mode to apply these changes to your manuscript.*\n"
        
        return plan
