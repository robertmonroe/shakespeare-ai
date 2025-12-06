#!/usr/bin/env python3
"""
Regenerate character profiles and worldbuilding for Inanna 4 project
"""
import sys
sys.path.insert(0, 'src')

from libriscribe.agents.project_manager import ProjectManagerAgent
from libriscribe.agents.character_generator import CharacterGeneratorAgent
from libriscribe.agents.worldbuilding import WorldbuildingAgent
from libriscribe.utils.llm_client import LLMClient
from rich.console import Console

console = Console()

# Load the project
console.print("\n[cyan]Loading Inanna 4 project...[/cyan]")
project_manager = ProjectManagerAgent(llm_client=None)

try:
    project_manager.load_project_data("Inanna 4")
    
    # Get the LLM provider from project data
    llm_provider = project_manager.project_knowledge_base.llm_provider
    console.print(f"[green]✓ Project loaded! Using {llm_provider}[/green]")
    
    # Initialize LLM client
    project_manager.initialize_llm_client(llm_provider)
    
    # Regenerate characters
    console.print("\n[cyan]👥 Regenerating character profiles...[/cyan]")
    console.print("[yellow]Making sure Inanna is beautiful and Tarzan is hot AF! 🔥[/yellow]\n")
    
    char_gen = CharacterGeneratorAgent(project_manager.llm_client)
    char_gen.execute(project_manager.project_knowledge_base)
    
    console.print("\n[cyan]🗺️ Regenerating worldbuilding...[/cyan]")
    world_gen = WorldbuildingAgent(project_manager.llm_client)
    world_gen.execute(project_manager.project_knowledge_base)
    
    # Save the updated project
    project_manager.save_project_data()
    
    console.print("\n[green]✅ Done! Character profiles and worldbuilding regenerated![/green]")
    console.print("[yellow]Check projects/Inanna 4/characters.json and worldbuilding.json[/yellow]")
    
except FileNotFoundError:
    console.print("[red]❌ Project 'Inanna 4' not found![/red]")
    console.print("[yellow]Available projects:[/yellow]")
    import os
    projects = [d for d in os.listdir("projects") if os.path.isdir(os.path.join("projects", d))]
    for p in projects:
        console.print(f"  - {p}")
except Exception as e:
    console.print(f"[red]❌ Error: {e}[/red]")
    import traceback
    traceback.print_exc()
