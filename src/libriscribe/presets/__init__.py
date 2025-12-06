# src/libriscribe/presets/__init__.py
"""
Shakespeare AI Style Presets and Story Structures

Load and apply:
- Writing style presets (pacing, tone, prose style)
- Story structure frameworks (Hero's Journey, Save the Cat, etc.)
"""

from .preset_manager import PresetManager, StylePreset
from .default_presets import PRESETS
from .story_structures import StructureManager, StoryStructure, StoryBeat, STORY_STRUCTURES

__all__ = [
    'PresetManager', 'StylePreset', 'PRESETS',
    'StructureManager', 'StoryStructure', 'StoryBeat', 'STORY_STRUCTURES'
]

