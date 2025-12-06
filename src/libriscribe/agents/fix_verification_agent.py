"""
Fix Verification Agent - Grades editor's work on applying review fixes

This agent verifies that the editor correctly applied each actionable fix
from the previous review, providing itemized Pass/Fail grading with specific
feedback for continuous improvement.
"""

import logging
from typing import Dict, Any, List
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class FixVerificationAgent(Agent):
    """Verifies and grades editor's application of review fixes."""

    def __init__(self, llm_client: LLMClient):
        super().__init__("FixVerificationAgent", llm_client)

    def execute(
        self,
        previous_fixes: List[str],
        original_chapter: str,
        edited_chapter: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Verify that each fix from previous review was applied correctly.
        
        Args:
            previous_fixes: List of actionable fixes from previous review
            original_chapter: Chapter text before editing
            edited_chapter: Chapter text after editing
            
        Returns:
            Dict containing:
                - verification_report: Full markdown report
                - passed_fixes: List of fix numbers that passed
                - failed_fixes: List of fix numbers that failed
                - pass_rate: Percentage of fixes that passed
                - failed_fix_details: Specific feedback for failed fixes
        """
        console.print(f"🔍 [cyan]Verifying fix application...[/cyan]")
        
        # Build verification prompt
        prompt = self._build_verification_prompt(
            previous_fixes,
            original_chapter,
            edited_chapter
        )
        
        # Get verification from LLM
        verification_output = self.llm_client.generate_content(
            prompt,
            max_tokens=4000,
            temperature=0.3  # Lower temp for consistent grading
        )
        
        # Parse verification results
        results = self._parse_verification_results(verification_output)
        
        # Display summary
        self._display_summary(results)
        
        return results

    def _build_verification_prompt(
        self,
        previous_fixes: List[str],
        original_chapter: str,
        edited_chapter: str
    ) -> str:
        """Build the verification prompt for the LLM."""
        
        # Format fixes list
        fixes_list = "\n".join([
            f"{i+1}. {fix}" for i, fix in enumerate(previous_fixes)
        ])
        
        prompt = f"""
You are a quality control reviewer grading an editor's work.

The editor was given these ACTIONABLE FIXES from the previous review:

{fixes_list}

ORIGINAL CHAPTER (before editing):
{original_chapter[:2000]}... [truncated for brevity]

EDITED CHAPTER (after editing):
{edited_chapter[:2000]}... [truncated for brevity]

Your task: For EACH fix listed above, determine if it was applied correctly.

For each fix, provide:

#### Fix #[N]: [Fix Description]
**Status**: ✅ PASS or ❌ FAIL

**What Editor Did Well** (if PASS or partial):
- [Specific things done correctly]

**What Editor Failed to Fix** (if FAIL):
- [Specific things still wrong or missing]

**Required Action for Next Pass** (if FAIL):
- [Exact steps to complete the fix]
- [Provide specific examples if applicable]

**Grade**: [Excellent/Good/Partial/Minimal/Failed]

---

After grading all fixes, provide:

## Summary

**Pass Rate**: X/Y (Z%)

**Passed Fixes**: [List fix numbers]

**Failed Fixes**: [List fix numbers with brief reason]

**Priority for Next Pass**:
1. 🔴 CRITICAL: [Most important failed fixes]
2. 🟡 HIGH: [Important failed fixes]
3. 🟢 MEDIUM: [Minor failed fixes]

Be specific and constructive. Provide concrete examples for failed fixes.
"""
        return prompt

    def _parse_verification_results(self, verification_output: str) -> Dict[str, Any]:
        """Parse the verification output into structured data."""
        
        # Extract pass/fail status for each fix
        passed_fixes = []
        failed_fixes = []
        
        lines = verification_output.split('\n')
        current_fix_num = None
        
        for line in lines:
            # Look for fix numbers
            if line.startswith('#### Fix #'):
                try:
                    current_fix_num = int(line.split('#')[1].split(':')[0])
                except:
                    pass
            
            # Look for status
            if '**Status**:' in line and current_fix_num:
                if '✅ PASS' in line:
                    passed_fixes.append(current_fix_num)
                elif '❌ FAIL' in line:
                    failed_fixes.append(current_fix_num)
                current_fix_num = None
        
        # Calculate pass rate
        total_fixes = len(passed_fixes) + len(failed_fixes)
        pass_rate = (len(passed_fixes) / total_fixes * 100) if total_fixes > 0 else 0
        
        # Extract failed fix details for feedback
        failed_fix_details = self._extract_failed_fix_details(
            verification_output,
            failed_fixes
        )
        
        return {
            'verification_report': verification_output,
            'passed_fixes': passed_fixes,
            'failed_fixes': failed_fixes,
            'pass_rate': pass_rate,
            'failed_fix_details': failed_fix_details,
            'total_fixes': total_fixes
        }

    def _extract_failed_fix_details(
        self,
        verification_output: str,
        failed_fixes: List[int]
    ) -> List[Dict[str, str]]:
        """Extract detailed feedback for failed fixes."""
        
        details = []
        
        for fix_num in failed_fixes:
            # Find the section for this fix
            fix_marker = f"#### Fix #{fix_num}:"
            if fix_marker in verification_output:
                # Extract the section (simplified - would need better parsing)
                start = verification_output.find(fix_marker)
                end = verification_output.find("#### Fix #", start + 1)
                if end == -1:
                    end = verification_output.find("## Summary", start)
                
                section = verification_output[start:end] if end != -1 else verification_output[start:]
                
                # Extract required action
                required_action = ""
                if "**Required Action" in section:
                    action_start = section.find("**Required Action")
                    action_end = section.find("**Grade:", action_start)
                    if action_end != -1:
                        required_action = section[action_start:action_end].strip()
                
                details.append({
                    'fix_number': fix_num,
                    'section': section,
                    'required_action': required_action
                })
        
        return details

    def _display_summary(self, results: Dict[str, Any]):
        """Display verification summary to console."""
        
        pass_rate = results['pass_rate']
        passed = len(results['passed_fixes'])
        failed = len(results['failed_fixes'])
        total = results['total_fixes']
        
        console.print("\n" + "="*80)
        console.print(f"[bold cyan]📊 FIX VERIFICATION RESULTS[/bold cyan]")
        console.print("="*80)
        
        # Pass rate with color coding
        if pass_rate >= 90:
            color = "green"
            grade = "Excellent"
        elif pass_rate >= 75:
            color = "cyan"
            grade = "Good"
        elif pass_rate >= 60:
            color = "yellow"
            grade = "Acceptable"
        else:
            color = "red"
            grade = "Needs Improvement"
        
        console.print(f"\n[bold {color}]Pass Rate: {passed}/{total} ({pass_rate:.1f}%) - {grade}[/bold {color}]")
        
        if passed > 0:
            console.print(f"\n[green]✅ PASSED ({passed}):[/green]")
            for fix_num in results['passed_fixes']:
                console.print(f"  • Fix #{fix_num}")
        
        if failed > 0:
            console.print(f"\n[red]❌ FAILED ({failed}):[/red]")
            for fix_num in results['failed_fixes']:
                console.print(f"  • Fix #{fix_num}")
        
        console.print("\n" + "="*80 + "\n")
