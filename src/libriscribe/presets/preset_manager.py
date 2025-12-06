# src/libriscribe/presets/preset_manager.py
"""
Style Preset Management for Libriscribe

Allows loading, saving, and applying style presets to projects.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from rich.console import Console

console = Console()


@dataclass
class StylePreset:
    """Defines a complete writing style preset."""
    
    # Core identification
    name: str
    description: str
    
    # Style inspirations
    inspired_by: str = ""  # Authors, books, movies: "Ian Fleming, Sicario, The Bourne Identity"
    
    # Pacing control
    pacing_preference: str = "balanced"  # fast, slow, balanced
    pacing_instruction: str = ""  # Detailed pacing guidance
    
    # Tone and voice
    tone: str = ""  # e.g., "Elegant, dangerous, sophisticated"
    prose_style: str = ""  # Detailed prose style description
    
    # Dialogue guidelines
    dialogue_style: str = ""  # How characters should speak
    
    # Action/Description balance
    internal_monologue: str = "moderate"  # minimal, moderate, heavy
    sensory_detail: str = "high"  # minimal, moderate, high
    action_style: str = ""  # How to write action scenes
    
    # Genre-specific
    genre_hints: List[str] = field(default_factory=list)
    
    # Additional prose rules
    prose_rules: List[str] = field(default_factory=list)
    
    # Formatting preferences
    scene_length: str = "800-1500 words"
    chapter_length: str = "3000-5000 words"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StylePreset":
        """Create from dictionary."""
        return cls(**data)
    
    def get_style_guide(self) -> str:
        """Generate style guide string for prompts."""
        parts = []
        
        if self.inspired_by:
            parts.append(f"- **Style Inspiration**: {self.inspired_by}")
        if self.pacing_preference:
            parts.append(f"- **Pacing**: {self.pacing_preference}")
        if self.tone:
            parts.append(f"- **Tone**: {self.tone}")
        if self.prose_style:
            parts.append(f"- **Prose Style**: {self.prose_style}")
        if self.dialogue_style:
            parts.append(f"- **Dialogue**: {self.dialogue_style}")
        if self.action_style:
            parts.append(f"- **Action Scenes**: {self.action_style}")
        if self.internal_monologue:
            parts.append(f"- **Internal Monologue**: {self.internal_monologue}")
        if self.sensory_detail:
            parts.append(f"- **Sensory Detail**: {self.sensory_detail}")
        
        return "\n".join(parts) if parts else "No specific style guide."
    
    def get_pacing_instruction(self) -> str:
        """Get detailed pacing instruction."""
        if self.pacing_instruction:
            return self.pacing_instruction
        
        # Generate from pacing_preference if not explicit
        pacing = self.pacing_preference.lower()
        
        if pacing == "fast":
            return """**FAST-PACED STYLE:**
- Open scenes with action or immediate tension
- Keep internal monologue to 1-2 sentences at a time
- Use short, punchy sentences during action
- Move quickly through transitions
- Dialogue should be snappy and purposeful
- Cut unnecessary description - every word earns its place"""
        
        elif pacing == "slow":
            return """**LITERARY/ATMOSPHERIC STYLE:**
- Allow space for internal reflection
- Build atmosphere through detailed description
- Explore character psychology deeply
- Use longer, flowing sentences
- Let emotional moments breathe"""
        
        else:
            return """**BALANCED STYLE:**
- Mix action with reflection
- Use internal monologue strategically
- Vary sentence length for rhythm
- Match pace to scene requirements"""
    
    def get_prose_rules(self) -> str:
        """Get prose rules as formatted string."""
        if not self.prose_rules:
            return ""
        
        rules = ["**PROSE RULES:**"]
        for i, rule in enumerate(self.prose_rules, 1):
            rules.append(f"{i}. {rule}")
        return "\n".join(rules)


class PresetManager:
    """Manages loading, saving, and applying style presets."""
    
    def __init__(self, presets_dir: Optional[Path] = None):
        """Initialize preset manager.
        
        Args:
            presets_dir: Directory for custom presets. 
                        Defaults to ~/.libriscribe/presets/
        """
        if presets_dir is None:
            presets_dir = Path.home() / ".libriscribe" / "presets"
        
        self.presets_dir = Path(presets_dir)
        self.presets_dir.mkdir(parents=True, exist_ok=True)
        
        # Load built-in presets
        from .default_presets import PRESETS
        self.presets: Dict[str, StylePreset] = {p.name: p for p in PRESETS}
        
        # Load custom presets
        self._load_custom_presets()
    
    def _load_custom_presets(self):
        """Load custom presets from presets directory."""
        for preset_file in self.presets_dir.glob("*.json"):
            try:
                with open(preset_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    preset = StylePreset.from_dict(data)
                    self.presets[preset.name] = preset
                    console.print(f"[dim]Loaded custom preset: {preset.name}[/dim]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load preset {preset_file}: {e}[/yellow]")
    
    def list_presets(self) -> List[str]:
        """List all available preset names."""
        return list(self.presets.keys())
    
    def get_preset(self, name: str) -> Optional[StylePreset]:
        """Get a preset by name."""
        return self.presets.get(name)
    
    def save_preset(self, preset: StylePreset, custom: bool = True):
        """Save a preset.
        
        Args:
            preset: The preset to save
            custom: If True, save to user's custom presets dir
        """
        if custom:
            filepath = self.presets_dir / f"{preset.name.lower().replace(' ', '_')}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(preset.to_dict(), f, indent=2)
            console.print(f"[green]Saved preset '{preset.name}' to {filepath}[/green]")
        
        self.presets[preset.name] = preset
    
    def apply_to_project(self, preset_name: str, project_knowledge_base) -> bool:
        """Apply a preset to a project knowledge base.
        
        Args:
            preset_name: Name of preset to apply
            project_knowledge_base: The project to modify
            
        Returns:
            True if successful
        """
        preset = self.get_preset(preset_name)
        if not preset:
            console.print(f"[red]Preset '{preset_name}' not found![/red]")
            return False
        
        # Apply preset fields to project
        if preset.inspired_by:
            project_knowledge_base.inspired_by = preset.inspired_by
        if preset.pacing_preference:
            project_knowledge_base.pacing_preference = preset.pacing_preference
        if preset.tone:
            project_knowledge_base.tone = preset.tone
        
        console.print(f"[green]Applied preset '{preset_name}' to project[/green]")
        return True
    
    def display_presets(self):
        """Display all available presets."""
        console.print("\n[bold cyan]Available Style Presets:[/bold cyan]\n")
        
        for name, preset in self.presets.items():
            console.print(f"[bold]{name}[/bold]")
            console.print(f"  [dim]{preset.description}[/dim]")
            if preset.inspired_by:
                console.print(f"  [cyan]Inspired by:[/cyan] {preset.inspired_by}")
            if preset.pacing_preference:
                console.print(f"  [cyan]Pacing:[/cyan] {preset.pacing_preference}")
            console.print()
