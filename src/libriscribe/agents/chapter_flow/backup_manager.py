# src/libriscribe/agents/chapter_flow/backup_manager.py

import shutil
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class BackupManager:
    """Manages backup creation and restoration for chapter files."""

    def __init__(self, project_dir: Path):
        """Initialize the backup manager.
        
        Args:
            project_dir: The project directory path
        """
        self.project_dir = Path(project_dir)
        self.backup_dir = self.project_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        logger.info(f"BackupManager initialized for {project_dir}")

    def create_backup(self, chapter_path: Path) -> str:
        """Create a numbered backup of a chapter file.
        
        Args:
            chapter_path: Path to the chapter file to backup
            
        Returns:
            str: Path to the created backup file
        """
        try:
            chapter_path = Path(chapter_path)
            if not chapter_path.exists():
                logger.warning(f"Chapter file does not exist: {chapter_path}")
                return ""

            # Find next backup number
            existing_backups = list(self.backup_dir.glob(f"{chapter_path.stem}_backup_*.md"))
            next_num = len(existing_backups) + 1
            
            backup_path = self.backup_dir / f"{chapter_path.stem}_backup_{next_num}.md"
            shutil.copy2(chapter_path, backup_path)
            
            logger.info(f"Created backup: {backup_path.name}")
            return str(backup_path)
            
        except Exception as e:
            logger.exception(f"Error creating backup for {chapter_path}: {e}")
            return ""

    def list_backups(self, chapter_number: int) -> List[Path]:
        """List all backups for a specific chapter.
        
        Args:
            chapter_number: The chapter number
            
        Returns:
            List[Path]: Sorted list of backup file paths
        """
        pattern = f"chapter_{chapter_number}_backup_*.md"
        backups = sorted(
            self.backup_dir.glob(pattern),
            key=lambda x: int(x.stem.split("_")[-1])
        )
        return backups

    def restore_backup(self, backup_path: Path, chapter_number: int) -> bool:
        """Restore a backup to the main chapter file.
        
        Args:
            backup_path: Path to the backup file
            chapter_number: The chapter number to restore to
            
        Returns:
            bool: True if restoration was successful
        """
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                logger.error(f"Backup file does not exist: {backup_path}")
                return False

            chapter_path = self.project_dir / f"chapter_{chapter_number}.md"
            shutil.copy2(backup_path, chapter_path)
            
            logger.info(f"Restored backup {backup_path.name} to {chapter_path.name}")
            return True
            
        except Exception as e:
            logger.exception(f"Error restoring backup {backup_path}: {e}")
            return False

    def get_backup_count(self, chapter_number: int) -> int:
        """Get the number of backups for a chapter.
        
        Args:
            chapter_number: The chapter number
            
        Returns:
            int: Number of backups
        """
        return len(self.list_backups(chapter_number))
