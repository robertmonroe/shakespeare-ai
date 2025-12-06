# test_file_scanner.py
# Quick test to verify ProjectFileScanner can see all project files

from pathlib import Path
from src.libriscribe.agents.autonomous.project_file_scanner import ProjectFileScanner

# Test with a real project
project_dir = Path("projects/pig 10")  # Change to your project

if project_dir.exists():
    print(f"Testing ProjectFileScanner on: {project_dir}\n")
    
    scanner = ProjectFileScanner(project_dir)
    files = scanner.scan_project()
    
    print(f"✓ Found {len(files)} files:\n")
    
    for filename, content in files.items():
        print(f"  • {filename} ({len(content)} chars)")
    
    print("\nFile types found:")
    json_files = [f for f in files.keys() if f.endswith('.json')]
    md_files = [f for f in files.keys() if f.endswith('.md')]
    
    print(f"  • JSON files: {len(json_files)}")
    print(f"  • Markdown files: {len(md_files)}")
    
    print("\nSample content from characters.json:")
    if 'characters.json' in files:
        print(files['characters.json'][:500])
    
else:
    print(f"Project not found: {project_dir}")
    print("\nAvailable projects:")
    for p in Path("projects").iterdir():
        if p.is_dir():
            print(f"  • {p.name}")
