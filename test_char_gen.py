#!/usr/bin/env python3
"""
Test character generation with cache clearing
"""
import sys
import importlib

# Clear all libriscribe modules from cache
modules_to_remove = [key for key in sys.modules.keys() if key.startswith('libriscribe')]
for module in modules_to_remove:
    del sys.modules[module]

# Now import fresh
sys.path.insert(0, 'src')

from libriscribe.agents.project_manager import ProjectManagerAgent
from libriscribe.agents.character_generator import CharacterGeneratorAgent
from rich.console import Console

console = Console()

# Load the project
console.print("\n[cyan]Loading Inanna 4 project (with cache cleared)...[/cyan]")
project_manager = ProjectManagerAgent(llm_client=None)

try:
    project_manager.load_project_data("Inanna 4")
    
    # Get the LLM provider from project data
    llm_provider = project_manager.project_knowledge_base.llm_provider
    console.print(f"[green]Project loaded! Using {llm_provider}[/green]")
    
    # Initialize LLM client
    project_manager.initialize_llm_client(llm_provider)
    
    # Regenerate characters
    console.print("\n[cyan]👥 Testing character generation with fixed code...[/cyan]")
    
    char_gen = CharacterGeneratorAgent(project_manager.llm_client)
    char_gen.execute(project_manager.project_knowledge_base)
    
    # Save the updated project
    project_manager.save_project_data()
    
    console.print("\n[green]Test complete! Check the logs and characters.json[/green]")
    
except Exception as e:
    console.print(f"[red]❌ Error: {e}[/red]")
    import traceback
    traceback.print_exc()
