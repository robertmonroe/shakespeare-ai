# Quick template management script
# Usage: python manage_templates.py [command] [args]

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from libriscribe.utils.template_manager import TemplateManager
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    base_dir = Path(__file__).parent
    manager = TemplateManager(base_dir)
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "save":
        if len(sys.argv) < 4:
            console.print("[red]Usage: python manage_templates.py save <project_name> <template_name> [description][/red]")
            return
        
        project_name = sys.argv[2]
        template_name = sys.argv[3]
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        
        manager.save_template(project_name, template_name, description)
    
    elif command == "load":
        if len(sys.argv) < 4:
            console.print("[red]Usage: python manage_templates.py load <template_name> <new_project_name>[/red]")
            return
        
        template_name = sys.argv[2]
        new_project_name = sys.argv[3]
        
        manager.load_template(template_name, new_project_name)
    
    elif command == "list":
        templates = manager.list_templates()
        
        if not templates:
            console.print("[yellow]No templates found[/yellow]")
            return
        
        table = Table(title="Available Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Created From", style="green")
        table.add_column("Created At", style="dim")
        
        for template in templates:
            table.add_row(
                template.get('name', 'Unknown'),
                template.get('description', ''),
                template.get('created_from', 'Unknown'),
                template.get('created_at', '')[:10]
            )
        
        console.print(table)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            console.print("[red]Usage: python manage_templates.py delete <template_name>[/red]")
            return
        
        template_name = sys.argv[2]
        manager.delete_template(template_name)
    
    elif command == "export":
        if len(sys.argv) < 3:
            console.print("[red]Usage: python manage_templates.py export <template_name> [output_path][/red]")
            return
        
        template_name = sys.argv[2]
        output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
        
        manager.export_template(template_name, output_path)
    
    elif command == "import":
        if len(sys.argv) < 3:
            console.print("[red]Usage: python manage_templates.py import <zip_file> [template_name][/red]")
            return
        
        zip_file = Path(sys.argv[2])
        template_name = sys.argv[3] if len(sys.argv) > 3 else None
        
        manager.import_template(zip_file, template_name)
    
    else:
        show_help()

def show_help():
    console.print("""
[bold cyan]Libriscribe Template Manager[/bold cyan]

[bold]Commands:[/bold]
  save <project> <template> [desc]  - Save project as template
  load <template> <new_project>     - Create project from template
  list                              - List all templates
  delete <template>                 - Delete a template
  export <template> [path]          - Export template as ZIP file
  import <zip_file> [name]          - Import template from ZIP file

[bold]Examples:[/bold]
  python manage_templates.py save "Inanna 4" "scifi_template" "Sci-fi novel template"
  python manage_templates.py load "scifi_template" "Inanna 5"
  python manage_templates.py list
  python manage_templates.py delete "old_template"
  python manage_templates.py export "scifi_template" "my_template.zip"
  python manage_templates.py import "downloaded_template.zip" "new_template"

[bold]What gets saved:[/bold]
  ✓ characters.json
  ✓ world.json
  ✓ outline.md
  ✓ scenes.json
  ✓ project_data.json
  
[bold]What gets excluded:[/bold]
  ✗ Chapter files (chapter_*.md)
  ✗ Reviews
  ✗ Backups

[bold]Sharing Templates:[/bold]
  1. Export your template to a ZIP file
  2. Share the ZIP file with others
  3. They import it to use your character/world setup
""")

if __name__ == "__main__":
    main()
