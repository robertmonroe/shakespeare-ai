# src/libriscribe/agents/task_based_editor.py

from typing import List, Dict, Any
from libriscribe.agents.agent_base import Agent
from libriscribe.utils.llm_client import LLMClient
from rich.console import Console
import logging

console = Console()
logger = logging.getLogger(__name__)


class TaskBasedEditor(Agent):
    """Applies specific tasks to chapter with self-confirmation."""
    
    def __init__(self, llm_client: LLMClient):
        super().__init__("TaskBasedEditor", llm_client)
    
    def execute(
        self,
        chapter_text: str,
        task_list: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply tasks to chapter.
        
        Args:
            chapter_text: Current chapter content
            task_list: List of specific tasks from Decision Agent
            context: Character/worldbuilding context
            
        Returns:
            {
                'edited_chapter': str,
                'completion_summary': Dict
            }
        """
        if not task_list:
            console.print("[yellow]⚠️  No tasks to apply[/yellow]")
            return {
                'edited_chapter': chapter_text,
                'completion_summary': {
                    'total_tasks': 0,
                    'completed': 0,
                    'failed': 0,
                    'tasks': []
                }
            }
        
        current_chapter = chapter_text
        completed_tasks = []
        
        console.print(f"\n[bold cyan]✏️  Applying {len(task_list)} tasks...[/bold cyan]\n")
        
        # Group tasks by category
        tasks_by_category = {}
        for task in task_list:
            category = task.get('category', 'Other')
            if category not in tasks_by_category:
                tasks_by_category[category] = []
            tasks_by_category[category].append(task)
        
        # Apply tasks grouped by category
        for category, tasks in tasks_by_category.items():
            console.print(f"\n[bold yellow]📂 {category} ({len(tasks)} tasks)[/bold yellow]")
            console.print(f"[dim]{'='*60}[/dim]\n")
            
            for task in tasks:
                # Validate task format
                required_fields = ['id', 'description', 'action', 'find_text', 'expected_outcome']
                missing_fields = [f for f in required_fields if f not in task]
                
                if missing_fields:
                    console.print(f"[red]❌ Task #{task.get('id', '?')} has invalid format![/red]")
                    console.print(f"[red]   Missing fields: {', '.join(missing_fields)}[/red]")
                    console.print(f"[yellow]   Skipping this task...[/yellow]\n")
                    failed_tasks.append({
                        'task': task,
                        'error': f"Missing required fields: {', '.join(missing_fields)}"
                    })
                    continue
                
                console.print(f"[yellow]⏳ Task #{task['id']}: {task['description']}[/yellow]")
                console.print(f"   [dim]Action: {task.get('action', 'N/A')}[/dim]")
                console.print(f"   [dim]Context: {task.get('context', 'N/A')}[/dim]")
                console.print(f"   [dim]Expected: {task['expected_outcome']}[/dim]")
                
                # Apply task
                result = self._apply_single_task(current_chapter, task, context)
                
                if result['success']:
                    current_chapter = result['edited_text']
                    console.print(f"[green]✅ Task #{task['id']} COMPLETE[/green]")
                    
                    # Show detailed feedback
                    if result['summary'] and result['summary'] != "Task completed":
                        console.print(f"   [dim]{result['summary']}[/dim]\n")
                    else:
                        # Show what action was taken if no detailed summary
                        action_desc = task.get('action', 'modified')
                        find_text = task.get('find_text', '')
                        if find_text:
                            console.print(f"   [dim]Applied '{action_desc}' to: {find_text[:50]}...[/dim]\n")
                        else:
                            console.print(f"   [dim]Applied: {action_desc}[/dim]\n")
                    
                    completed_tasks.append({
                        'task_id': task['id'],
                        'category': category,
                        'status': 'completed',
                        'summary': result['summary']
                    })
                else:
                    console.print(f"[red]❌ Task #{task['id']} FAILED[/red]")
                    console.print(f"   [red]{result['error']}[/red]\n")
                    
                    completed_tasks.append({
                        'task_id': task['id'],
                        'category': category,
                        'status': 'failed',
                        'error': result['error']
                    })
        
        # Self-check all tasks
        console.print("[cyan]🔍 Self-checking all tasks...[/cyan]")
        self_check = self._self_check_all_tasks(task_list, completed_tasks)
        
        console.print(f"[green]✅ {self_check['completed_count']}/{len(task_list)} tasks completed successfully[/green]")
        if self_check['failed_count'] > 0:
            console.print(f"[yellow]⚠️  {self_check['failed_count']} tasks failed[/yellow]")
        console.print()
        
        return {
            'edited_chapter': current_chapter,
            'completion_summary': {
                'total_tasks': len(task_list),
                'completed': self_check['completed_count'],
                'failed': self_check['failed_count'],
                'success_rate': self_check['success_rate'],
                'tasks': completed_tasks
            }
        }
    
    def _apply_single_task(
        self,
        chapter_text: str,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a single specific task using LLM."""
        
        # Build task application prompt
        prompt = self._build_task_prompt(chapter_text, task, context)
        
        try:
            # Apply task with LLM
            response = self.llm_client.generate_content(prompt, max_tokens=12000, temperature=0.5)
            
            # Extract edited chapter
            edited_text = self._extract_chapter(response)
            
            # Extract summary
            summary = self._extract_summary(response)
            
            # Verify outcome achieved
            outcome_achieved = self._extract_outcome(response)
            
            if not outcome_achieved:
                logger.warning(f"Task {task['id']} may not have achieved expected outcome")
            
            return {
                'success': True,
                'edited_text': edited_text,
                'summary': summary,
                'outcome_achieved': outcome_achieved,
                'error': None
            }
            
        except Exception as e:
            logger.exception(f"Error applying task {task.get('id', '?')}: {e}")
            return {
                'success': False,
                'edited_text': chapter_text,
                'summary': None,
                'outcome_achieved': False,
                'error': str(e)
            }
    
    def _build_task_prompt(
        self,
        chapter_text: str,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Build prompt for applying a specific task."""
        
        example_section = ""
        if task.get('example'):
            example_section = f"\n**Example of Desired Change**:\n{task['example']}\n"
        
        return f"""
You are an expert editor applying a specific task to a chapter.

**Task Details**:
- ID: {task['id']}
- Description: {task['description']}
- Action: {task.get('action', 'N/A')}
- Context: {task.get('context', 'N/A')}
- Expected Outcome: {task['expected_outcome']}
- Priority: {task.get('priority', 'medium')}
{example_section}
**Context for Consistency**:
- Characters: {context.get('characters', 'N/A')}
- Worldbuilding: {context.get('worldbuilding', 'N/A')}

**Current Chapter**:
{chapter_text}

**CRITICAL INSTRUCTIONS**:
1. **ONLY edit the specified context**: {task.get('context', 'the relevant section')}
2. **DO NOT change anything else** in the chapter
3. Follow the task description and action type EXACTLY
4. Use the example (if provided) as a guide for the style/format
5. Achieve the "Expected Outcome" precisely
6. Maintain consistency with character and worldbuilding context
7. Preserve all scene titles and chapter structure
8. Return the COMPLETE chapter with ONLY the specified section modified

**Output Format**:
Provide the complete edited chapter in a markdown code block.

```markdown
[COMPLETE CHAPTER WITH ONLY THE TARGET SECTION MODIFIED]
```

**Summary**: [Brief description of what you changed in the target section]
**Outcome Achieved**: [Yes/No - brief explanation]
"""
    
    def _extract_chapter(self, response: str) -> str:
        """Extract edited chapter from LLM response."""
        try:
            if "```markdown" in response:
                start = response.find("```markdown") + 11
                end = response.find("```", start)
                if end == -1:
                    # No closing backticks, take rest of response
                    return response[start:].strip()
                return response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                # Skip language identifier if present
                newline = response.find("\n", start)
                if newline != -1 and newline < start + 20:
                    start = newline + 1
                end = response.find("```", start)
                if end == -1:
                    return response[start:].strip()
                return response[start:end].strip()
            else:
                # No code blocks, try to extract chapter content
                # Look for chapter heading
                if response.startswith("#"):
                    return response.strip()
                # Otherwise return as-is
                return response.strip()
        except Exception as e:
            logger.error(f"Error extracting chapter: {e}")
            return response.strip()
    
    def _extract_summary(self, response: str) -> str:
        """Extract summary of changes from response."""
        try:
            if "**Summary**:" in response:
                summary_start = response.find("**Summary**:") + 12
                summary_end = response.find("\n**", summary_start)
                if summary_end == -1:
                    summary_end = response.find("\n", summary_start)
                if summary_end == -1:
                    summary_end = len(response)
                return response[summary_start:summary_end].strip()
            return "Task completed"
        except Exception as e:
            logger.error(f"Error extracting summary: {e}")
            return "Task completed"
    
    def _extract_outcome(self, response: str) -> bool:
        """Extract whether expected outcome was achieved."""
        try:
            if "**Outcome Achieved**:" in response:
                outcome_start = response.find("**Outcome Achieved**:") + 21
                outcome_text = response[outcome_start:outcome_start+100].lower()
                return "yes" in outcome_text
            # If not explicitly stated, assume success
            return True
        except Exception as e:
            logger.error(f"Error extracting outcome: {e}")
            return True
    
    def _self_check_all_tasks(
        self,
        task_list: List[Dict],
        completed_tasks: List[Dict]
    ) -> Dict[str, Any]:
        """Self-check that all tasks were completed."""
        completed_count = sum(1 for t in completed_tasks if t['status'] == 'completed')
        failed_count = sum(1 for t in completed_tasks if t['status'] == 'failed')
        
        success_rate = completed_count / len(task_list) if task_list else 0
        
        return {
            'completed_count': completed_count,
            'failed_count': failed_count,
            'success_rate': success_rate
        }
