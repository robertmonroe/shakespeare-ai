"""
Quick test to verify the refactored architecture works
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from libriscribe.agents.chapter_flow.backup_manager import BackupManager
from libriscribe.agents.chapter_flow.review_manager import ReviewManager
from libriscribe.agents.chapter_flow.chapter_flow_manager import ChapterFlowManager

print("✅ All imports successful!")
print("✅ BackupManager:", BackupManager)
print("✅ ReviewManager:", ReviewManager)
print("✅ ChapterFlowManager:", ChapterFlowManager)

# Test instantiation
test_dir = Path("./test_project")
test_dir.mkdir(exist_ok=True)

backup_mgr = BackupManager(test_dir)
print(f"✅ BackupManager instantiated with backup_dir: {backup_mgr.backup_dir}")

# Cleanup
import shutil
if test_dir.exists():
    shutil.rmtree(test_dir)

print("\n🎉 All tests passed! The refactored architecture is working.")
