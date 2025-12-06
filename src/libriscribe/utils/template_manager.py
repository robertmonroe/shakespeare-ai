# src/libriscribe/utils/template_manager.py

import shutil
import json
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from rich.console import Console

console = Console()


class TemplateManager:
    """Manages project templates for reusability."""
    
    def __init__(self, base_dir: Path):
        """Initialize template manager.
        
        Args:
            base_dir: Base directory for Libriscribe (contains 'projects' folder)
        """
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Files to include in templates (structure only, no content)
        self.template_files = [
            "characters.json",
            "world.json",
            "outline.md",
            "scenes.json",
            "project_data.json"
        ]
        
        # Files to exclude (generated content)
        self.exclude_patterns = [
            "chapter_*.md",
            "reviews/*",
            "backups/*",
            "*.log"
        ]
    
    def save_template(self, project_name: str, template_name: str, description: str = "") -> bool:
        """Save a project as a reusable template.
        
        Args:
            project_name: Name of the source project
            template_name: Name for the template
            description: Optional description of the template
            
        Returns:
            bool: True if successful
        """
        try:
            source_dir = self.base_dir / "projects" / project_name
            if not source_dir.exists():
                console.print(f"[red]❌ Project '{project_name}' not found[/red]")
                return False
            
            # Create template directory
            template_dir = self.templates_dir / template_name
            template_dir.mkdir(exist_ok=True)
            
            # Copy template files
            copied_files = []
            for filename in self.template_files:
                source_file = source_dir / filename
                if source_file.exists():
                    dest_file = template_dir / filename
                    shutil.copy2(source_file, dest_file)
                    copied_files.append(filename)
            
            # Create template metadata
            metadata = {
                "name": template_name,
                "description": description,
                "created_from": project_name,
                "created_at": datetime.now().isoformat(),
                "files": copied_files,
                "libriscribe_version": "2.1.0"
            }
            
            metadata_file = template_dir / "template_info.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            console.print(f"[green]✅ Template '{template_name}' created successfully![/green]")
            console.print(f"[dim]Saved {len(copied_files)} files[/dim]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error creating template: {e}[/red]")
            return False
    
    def load_template(self, template_name: str, new_project_name: str) -> bool:
        """Create a new project from a template.
        
        Args:
            template_name: Name of the template to use
            new_project_name: Name for the new project
            
        Returns:
            bool: True if successful
        """
        try:
            template_dir = self.templates_dir / template_name
            if not template_dir.exists():
                console.print(f"[red]❌ Template '{template_name}' not found[/red]")
                return False
            
            # Create new project directory
            new_project_dir = self.base_dir / "projects" / new_project_name
            if new_project_dir.exists():
                console.print(f"[red]❌ Project '{new_project_name}' already exists[/red]")
                return False
            
            new_project_dir.mkdir(parents=True)
            
            # Copy template files
            copied_files = []
            for filename in self.template_files:
                source_file = template_dir / filename
                if source_file.exists():
                    dest_file = new_project_dir / filename
                    shutil.copy2(source_file, dest_file)
                    copied_files.append(filename)
                    
                    # Update project_data.json with new project name
                    if filename == "project_data.json":
                        self._update_project_data(dest_file, new_project_name, new_project_dir)
            
            # Create required subdirectories
            (new_project_dir / "reviews").mkdir(exist_ok=True)
            (new_project_dir / "backups").mkdir(exist_ok=True)
            
            console.print(f"[green]✅ Project '{new_project_name}' created from template![/green]")
            console.print(f"[dim]Copied {len(copied_files)} files[/dim]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error loading template: {e}[/red]")
            return False
    
    def list_templates(self) -> List[Dict]:
        """List all available templates.
        
        Returns:
            List of template metadata dictionaries
        """
        templates = []
        
        if not self.templates_dir.exists():
            return templates
        
        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir():
                metadata_file = template_dir / "template_info.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            templates.append(metadata)
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not read template '{template_dir.name}': {e}[/yellow]")
        
        return templates
    
    def delete_template(self, template_name: str) -> bool:
        """Delete a template.
        
        Args:
            template_name: Name of the template to delete
            
        Returns:
            bool: True if successful
        """
        try:
            template_dir = self.templates_dir / template_name
            if not template_dir.exists():
                console.print(f"[red]❌ Template '{template_name}' not found[/red]")
                return False
            
            shutil.rmtree(template_dir)
            console.print(f"[green]✅ Template '{template_name}' deleted[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error deleting template: {e}[/red]")
            return False
    
    def _update_project_data(self, project_data_file: Path, new_name: str, new_dir: Path):
        """Update project_data.json with new project information.
        
        Args:
            project_data_file: Path to project_data.json
            new_name: New project name
            new_dir: New project directory
        """
        try:
            with open(project_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update project-specific fields
            if isinstance(data, dict):
                data['title'] = new_name
                data['project_dir'] = str(new_dir)
                
                # Clear auto-chapter mode (user should set this per project)
                if 'auto_chapter_mode' in data:
                    data['auto_chapter_mode'] = False
            
            with open(project_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not update project_data.json: {e}[/yellow]")
    
    def export_template(self, template_name: str, export_path: Optional[Path] = None) -> bool:
        """Export a template as a ZIP file for sharing.
        
        Args:
            template_name: Name of the template to export
            export_path: Optional path for the ZIP file (default: templates/{name}.zip)
            
        Returns:
            bool: True if successful
        """
        try:
            import zipfile
            
            template_dir = self.templates_dir / template_name
            if not template_dir.exists():
                console.print(f"[red]❌ Template '{template_name}' not found[/red]")
                return False
            
            # Default export path
            if export_path is None:
                export_path = self.templates_dir / f"{template_name}.zip"
            else:
                export_path = Path(export_path)
            
            # Create ZIP file
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in template_dir.rglob('*'):
                    if file.is_file():
                        arcname = file.relative_to(template_dir)
                        zipf.write(file, arcname)
            
            console.print(f"[green]✅ Template exported to: {export_path}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error exporting template: {e}[/red]")
            return False
    
    def import_template(self, zip_path: Path, template_name: Optional[str] = None) -> bool:
        """Import a template from a ZIP file.
        
        Args:
            zip_path: Path to the ZIP file
            template_name: Optional name for the imported template (default: from metadata)
            
        Returns:
            bool: True if successful
        """
        try:
            import zipfile
            
            zip_path = Path(zip_path)
            if not zip_path.exists():
                console.print(f"[red]❌ ZIP file not found: {zip_path}[/red]")
                return False
            
            # Extract to temporary location first
            import tempfile
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract ZIP
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                # Read metadata to get template name
                metadata_file = temp_path / "template_info.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        if template_name is None:
                            template_name = metadata.get('name', zip_path.stem)
                else:
                    if template_name is None:
                        template_name = zip_path.stem
                
                # Create template directory
                template_dir = self.templates_dir / template_name
                if template_dir.exists():
                    console.print(f"[yellow]⚠️  Template '{template_name}' already exists[/yellow]")
                    overwrite = input("Overwrite? (y/n): ").lower()
                    if overwrite != 'y':
                        console.print("[yellow]Import cancelled[/yellow]")
                        return False
                    shutil.rmtree(template_dir)
                
                # Copy extracted files to template directory
                shutil.copytree(temp_path, template_dir)
            
            console.print(f"[green]✅ Template '{template_name}' imported successfully![/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error importing template: {e}[/red]")
            return False
