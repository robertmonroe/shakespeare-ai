# src/libriscribe/agents/autonomous/project_file_scanner.py

import logging
from pathlib import Path
from typing import Dict, List
import json

logger = logging.getLogger(__name__)


class ProjectFileScanner:
    """
    Scans and reads all project files for autonomous modification.
    
    Returns complete project state as dict of {filename: content}.
    """
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
    
    def scan_project(self) -> Dict[str, str]:
        """
        Scan all project files and return their contents.
        
        Returns:
            Dict mapping filename to file content
        """
        files = {}
        
        try:
            # Scan JSON metadata files
            files.update(self._scan_json_files())
            
            # Scan markdown files
            files.update(self._scan_markdown_files())
            
            # Scan chapters
            files.update(self._scan_chapters())
            
            logger.info(f"Scanned {len(files)} project files")
            return files
            
        except Exception as e:
            logger.exception(f"Error scanning project: {e}")
            return {}
    
    def _scan_json_files(self) -> Dict[str, str]:
        """Scan JSON metadata files."""
        files = {}
        json_files = [
            "characters.json",
            "scenes.json",
            "worldbuilding.json",
            "project_data.json"
        ]
        
        for filename in json_files:
            file_path = self.project_dir / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    files[filename] = content
                except Exception as e:
                    logger.warning(f"Could not read {filename}: {e}")
        
        return files
    
    def _scan_markdown_files(self) -> Dict[str, str]:
        """Scan markdown files."""
        files = {}
        md_files = [
            "outline.md",
            "manuscript.md",
            "manuscript_original.md"
        ]
        
        for filename in md_files:
            file_path = self.project_dir / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    files[filename] = content
                except Exception as e:
                    logger.warning(f"Could not read {filename}: {e}")
        
        return files
    
    def _scan_chapters(self) -> Dict[str, str]:
        """Scan all chapter files."""
        files = {}
        
        chapter_files = sorted(self.project_dir.glob("chapter_*.md"))
        
        for chapter_path in chapter_files:
            try:
                content = chapter_path.read_text(encoding='utf-8')
                files[chapter_path.name] = content
            except Exception as e:
                logger.warning(f"Could not read {chapter_path.name}: {e}")
        
        return files
    
    def get_file_list(self) -> List[str]:
        """Get list of all scanned files."""
        return list(self.scan_project().keys())
