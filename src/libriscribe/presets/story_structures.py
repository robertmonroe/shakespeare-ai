# src/libriscribe/presets/story_structures.py
"""
Story Structure Presets for Shakespeare AI

Define plot beat frameworks: Hero's Journey, Save the Cat, Three-Act, etc.
These are used for outlining and chapter planning.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class StoryBeat:
    """A single beat in a story structure."""
    name: str
    description: str
    percentage: float  # Where in the story this occurs (0-100)
    chapter_hint: str = ""  # Suggested chapter range
    key_elements: List[str] = field(default_factory=list)


@dataclass 
class StoryStructure:
    """A complete story structure framework."""
    name: str
    description: str
    beats: List[StoryBeat]
    total_chapters_suggestion: str = "20-30"
    best_for: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryStructure":
        beats = [StoryBeat(**b) for b in data.pop("beats", [])]
        return cls(beats=beats, **data)
    
    def get_beat_at_percentage(self, pct: float) -> Optional[StoryBeat]:
        """Get the story beat closest to a given percentage."""
        closest = None
        min_dist = float('inf')
        for beat in self.beats:
            dist = abs(beat.percentage - pct)
            if dist < min_dist:
                min_dist = dist
                closest = beat
        return closest
    
    def get_outline_template(self, num_chapters: int = 25) -> str:
        """Generate an outline template based on this structure."""
        lines = [f"# {self.name} Outline Template\n"]
        lines.append(f"Target: {num_chapters} chapters\n")
        
        for beat in self.beats:
            chapter_num = max(1, int(beat.percentage / 100 * num_chapters))
            lines.append(f"\n## {beat.name} (Chapter ~{chapter_num}, {beat.percentage}%)")
            lines.append(f"_{beat.description}_\n")
            if beat.key_elements:
                for elem in beat.key_elements:
                    lines.append(f"- {elem}")
        
        return "\n".join(lines)


# ============================================================================
#  HERO'S JOURNEY (Joseph Campbell / Christopher Vogler)
# ============================================================================
HEROS_JOURNEY = StoryStructure(
    name="Hero's Journey",
    description="The classic monomyth structure: ordinary world, call to adventure, trials, transformation, return. Used by Star Wars, The Matrix, Harry Potter.",
    
    total_chapters_suggestion="20-30",
    best_for=["epic fantasy", "adventure", "coming of age", "science fiction", "mythology"],
    
    beats=[
        StoryBeat(
            name="Ordinary World",
            description="Establish the hero's normal life, their flaws, and what's missing. Show what they'll eventually leave behind.",
            percentage=0,
            chapter_hint="1-2",
            key_elements=[
                "Hero's everyday life and routine",
                "Their flaw or wound that needs healing",
                "Relationships that ground them",
                "Hints of the larger world/problem"
            ]
        ),
        StoryBeat(
            name="Call to Adventure",
            description="Something disrupts the ordinary world. The hero is presented with a challenge or opportunity.",
            percentage=10,
            chapter_hint="2-3",
            key_elements=[
                "Inciting incident that changes everything",
                "The problem/opportunity that demands response",
                "Stakes are introduced"
            ]
        ),
        StoryBeat(
            name="Refusal of the Call",
            description="The hero hesitates, doubts, or outright refuses. Fear of the unknown holds them back.",
            percentage=15,
            chapter_hint="3-4",
            key_elements=[
                "Hero's fear or reluctance",
                "What they'd have to sacrifice",
                "Pressure to maintain status quo"
            ]
        ),
        StoryBeat(
            name="Meeting the Mentor",
            description="A wise figure provides guidance, training, or a gift that will help the hero on their journey.",
            percentage=20,
            chapter_hint="4-5",
            key_elements=[
                "Mentor character introduction",
                "Training or wisdom shared",
                "Gift or tool for the journey",
                "Encouragement to accept the call"
            ]
        ),
        StoryBeat(
            name="Crossing the Threshold",
            description="The hero commits to the journey, leaving the ordinary world behind. There's no going back.",
            percentage=25,
            chapter_hint="5-6",
            key_elements=[
                "Point of no return",
                "Entering the special world",
                "Old life left behind",
                "First challenge in new world"
            ]
        ),
        StoryBeat(
            name="Tests, Allies, Enemies",
            description="The hero navigates the special world, making friends, facing enemies, and learning the rules.",
            percentage=35,
            chapter_hint="7-10",
            key_elements=[
                "New allies join the quest",
                "Enemies and obstacles appear",
                "Hero learns the rules of special world",
                "Skills tested and developed"
            ]
        ),
        StoryBeat(
            name="Approach to the Inmost Cave",
            description="The hero prepares for the major challenge. Tension builds as they near the heart of danger.",
            percentage=50,
            chapter_hint="11-13",
            key_elements=[
                "Preparation for the ordeal",
                "Team dynamics tested",
                "Doubts and fears resurface",
                "Final approach to the center"
            ]
        ),
        StoryBeat(
            name="The Ordeal",
            description="The hero faces their greatest challenge, often a near-death experience or confrontation with their deepest fear.",
            percentage=55,
            chapter_hint="14-15",
            key_elements=[
                "Greatest challenge/crisis",
                "Death and rebirth (literal or symbolic)",
                "Confronting deepest fear",
                "Moment of apparent defeat"
            ]
        ),
        StoryBeat(
            name="Reward (Seizing the Sword)",
            description="Having survived the ordeal, the hero claims their reward: knowledge, power, or the object of their quest.",
            percentage=60,
            chapter_hint="15-16",
            key_elements=[
                "Claiming the treasure/knowledge",
                "Celebration or moment of triumph",
                "New understanding gained",
                "Hero transformed by ordeal"
            ]
        ),
        StoryBeat(
            name="The Road Back",
            description="The hero begins the journey home, but the adventure isn't over. New dangers pursue them.",
            percentage=70,
            chapter_hint="17-19",
            key_elements=[
                "Decision to return",
                "Chase or pursuit",
                "Stakes raised again",
                "Motivation to complete journey"
            ]
        ),
        StoryBeat(
            name="Resurrection",
            description="The final, most dangerous challenge. The hero must use everything they've learned. A climactic battle or test.",
            percentage=85,
            chapter_hint="20-22",
            key_elements=[
                "Final confrontation",
                "Hero applies all lessons learned",
                "Sacrifice may be required",
                "Climactic battle/test"
            ]
        ),
        StoryBeat(
            name="Return with the Elixir",
            description="The hero returns home transformed, bringing something valuable to share with their world.",
            percentage=95,
            chapter_hint="23-25",
            key_elements=[
                "Hero returns home changed",
                "Gift/knowledge shared with world",
                "New equilibrium established",
                "Character arc completed"
            ]
        )
    ]
)


# ============================================================================
#  SAVE THE CAT (Blake Snyder)
# ============================================================================
SAVE_THE_CAT = StoryStructure(
    name="Save the Cat",
    description="Blake Snyder's 15-beat story structure, originally for screenwriting but widely used for novels. Precise, commercial, emotionally satisfying.",
    
    total_chapters_suggestion="15-25",
    best_for=["commercial fiction", "romance", "thriller", "young adult", "any genre"],
    
    beats=[
        StoryBeat(
            name="Opening Image",
            description="A visual that represents the hero's starting point. This will contrast with the final image.",
            percentage=0,
            chapter_hint="1",
            key_elements=[
                "Snapshot of hero's world 'before'",
                "Tone established",
                "Visual metaphor for theme"
            ]
        ),
        StoryBeat(
            name="Theme Stated",
            description="Someone states the theme to the hero, often without them realizing its importance. The lesson they'll learn.",
            percentage=5,
            chapter_hint="1",
            key_elements=[
                "Theme spoken aloud (subtly)",
                "Hero doesn't understand yet",
                "Sets up character arc"
            ]
        ),
        StoryBeat(
            name="Set-Up",
            description="Establish the hero's world, their flaws, and what needs to change. Plant seeds for later.",
            percentage=10,
            chapter_hint="1-2",
            key_elements=[
                "Hero's world and status quo",
                "Their flaw/want/need",
                "Supporting cast introduced",
                "Things that will pay off later"
            ]
        ),
        StoryBeat(
            name="Catalyst",
            description="The inciting incident. Something happens that will change everything.",
            percentage=12,
            chapter_hint="2-3",
            key_elements=[
                "Life-changing event",
                "Can't be ignored",
                "Sets the story in motion"
            ]
        ),
        StoryBeat(
            name="Debate",
            description="The hero debates whether to accept the challenge. Should I go? Can I do this?",
            percentage=15,
            chapter_hint="3-4",
            key_elements=[
                "Hero's hesitation",
                "Weighing options",
                "What's at stake",
                "Last chance to turn back"
            ]
        ),
        StoryBeat(
            name="Break into Two",
            description="The hero makes a choice and enters Act Two, the 'upside-down world' where things are different.",
            percentage=25,
            chapter_hint="5-6",
            key_elements=[
                "Active choice by hero",
                "Crossing into new world",
                "Old world left behind",
                "New rules apply"
            ]
        ),
        StoryBeat(
            name="B Story",
            description="The secondary story begins, often a love interest or friendship that carries the theme.",
            percentage=27,
            chapter_hint="6-7",
            key_elements=[
                "New character(s) introduced",
                "Often the love interest",
                "Carries the theme",
                "Will help hero learn lesson"
            ]
        ),
        StoryBeat(
            name="Fun and Games",
            description="The 'promise of the premise.' The most entertaining section where the concept delivers.",
            percentage=35,
            chapter_hint="7-11",
            key_elements=[
                "Deliver what the audience came for",
                "Hero in the new world",
                "Exploration and discovery",
                "Things seem to go well (or amusingly wrong)"
            ]
        ),
        StoryBeat(
            name="Midpoint",
            description="A major shift. Either a false victory or false defeat. Stakes are raised. Everything changes.",
            percentage=50,
            chapter_hint="12-13",
            key_elements=[
                "False victory OR false defeat",
                "Stakes raised dramatically",
                "Clock starts ticking",
                "From 'wants' to 'needs'"
            ]
        ),
        StoryBeat(
            name="Bad Guys Close In",
            description="Things get harder. External and internal pressure mounts. The team fractures.",
            percentage=60,
            chapter_hint="14-16",
            key_elements=[
                "Villains regroup and attack",
                "Internal conflicts surface",
                "Team/relationships fracture",
                "Hero's flaws cause problems"
            ]
        ),
        StoryBeat(
            name="All Is Lost",
            description="The lowest point. The hero experiences their greatest defeat. Often a 'death' (literal or symbolic).",
            percentage=75,
            chapter_hint="17-18",
            key_elements=[
                "Lowest moment",
                "Death of mentor/ally or hope",
                "Hero at rock bottom",
                "The 'whiff of death'"
            ]
        ),
        StoryBeat(
            name="Dark Night of the Soul",
            description="The hero mourns, reflects, and finds the strength to continue. The moment before breakthrough.",
            percentage=78,
            chapter_hint="18-19",
            key_elements=[
                "Hero processes defeat",
                "Mourning what was lost",
                "Finding inner strength",
                "Hint of solution emerges"
            ]
        ),
        StoryBeat(
            name="Break into Three",
            description="The hero has an epiphany. They combine what they learned with a new plan. Time for the finale.",
            percentage=80,
            chapter_hint="19-20",
            key_elements=[
                "A and B stories combine",
                "Hero sees the truth",
                "New plan formed",
                "Theme understood"
            ]
        ),
        StoryBeat(
            name="Finale",
            description="The hero executes the plan, confronts the villain, and proves they've changed.",
            percentage=90,
            chapter_hint="20-23",
            key_elements=[
                "Execute the new plan",
                "Confront antagonist",
                "High tower surprise",
                "Dig deep down to win",
                "Prove the transformation"
            ]
        ),
        StoryBeat(
            name="Final Image",
            description="A visual that shows the hero's transformation. Mirrors but contrasts with the opening image.",
            percentage=100,
            chapter_hint="24-25",
            key_elements=[
                "Hero's new world",
                "Proof of change",
                "Mirrors opening image",
                "Resolution and satisfaction"
            ]
        )
    ]
)


# ============================================================================
#  THREE-ACT STRUCTURE (Classic)
# ============================================================================
THREE_ACT = StoryStructure(
    name="Three-Act Structure",
    description="The fundamental Western dramatic structure. Setup, confrontation, resolution. Simple, flexible, universal.",
    
    total_chapters_suggestion="15-30",
    best_for=["any genre", "beginning writers", "flexible storytelling"],
    
    beats=[
        StoryBeat(
            name="Act One: Setup",
            description="Introduce the world, characters, and conflict. End with the hero committed to action.",
            percentage=0,
            chapter_hint="1-7 (25% of story)",
            key_elements=[
                "Ordinary world established",
                "Protagonist introduced with flaw",
                "Inciting incident occurs",
                "Stakes established",
                "First plot point: hero commits"
            ]
        ),
        StoryBeat(
            name="First Plot Point",
            description="The event that locks the hero into the story. After this, there's no going back.",
            percentage=25,
            chapter_hint="6-7",
            key_elements=[
                "Point of no return",
                "Hero fully committed",
                "Goal clarified",
                "Antagonist force revealed"
            ]
        ),
        StoryBeat(
            name="Act Two: Confrontation",
            description="The hero pursues their goal, facing escalating obstacles. The longest act.",
            percentage=30,
            chapter_hint="8-18 (50% of story)",
            key_elements=[
                "Rising action and obstacles",
                "Allies and enemies",
                "Subplots develop",
                "Hero tested and learns"
            ]
        ),
        StoryBeat(
            name="Midpoint",
            description="A major reversal or revelation that changes everything. False victory or false defeat.",
            percentage=50,
            chapter_hint="12-14",
            key_elements=[
                "Major reversal",
                "Stakes raised",
                "New information revealed",
                "Shift in direction"
            ]
        ),
        StoryBeat(
            name="Second Plot Point",
            description="The final push toward climax. Hero gets the key to defeating the antagonist.",
            percentage=75,
            chapter_hint="18-20",
            key_elements=[
                "Final piece of puzzle",
                "Hero at lowest point then rises",
                "Path to climax clear",
                "Final confrontation set up"
            ]
        ),
        StoryBeat(
            name="Act Three: Resolution",
            description="The climax and its aftermath. Hero confronts antagonist, resolves conflict, shows change.",
            percentage=80,
            chapter_hint="19-25 (25% of story)",
            key_elements=[
                "Climactic confrontation",
                "Hero uses lessons learned",
                "Antagonist defeated",
                "Subplots resolved",
                "New equilibrium"
            ]
        )
    ]
)


# ============================================================================
#  SEVEN-POINT STORY STRUCTURE (Dan Wells)
# ============================================================================
SEVEN_POINT = StoryStructure(
    name="Seven-Point Structure",
    description="Dan Wells' simplified structure. Start with the end, work backward. Hook → Plot Turn 1 → Pinch 1 → Midpoint → Pinch 2 → Plot Turn 2 → Resolution.",
    
    total_chapters_suggestion="15-25",
    best_for=["plotters", "genre fiction", "tight pacing"],
    
    beats=[
        StoryBeat(
            name="Hook",
            description="The opposite of the resolution. Show the hero at their starting point.",
            percentage=0,
            chapter_hint="1-2",
            key_elements=[
                "Hero in their 'before' state",
                "Opposite of where they'll end",
                "Hook the reader's interest"
            ]
        ),
        StoryBeat(
            name="Plot Turn 1",
            description="The call to adventure. The world changes and the hero must respond.",
            percentage=15,
            chapter_hint="3-5",
            key_elements=[
                "World changes",
                "Introduce the conflict",
                "Set hero on path"
            ]
        ),
        StoryBeat(
            name="Pinch Point 1",
            description="Apply pressure. The villain/antagonist shows their power. Things get harder.",
            percentage=30,
            chapter_hint="7-9",
            key_elements=[
                "Antagonist pressure",
                "Force hero to action",
                "Raise stakes"
            ]
        ),
        StoryBeat(
            name="Midpoint",
            description="The hero moves from reaction to action. They take charge of their destiny.",
            percentage=50,
            chapter_hint="12-14",
            key_elements=[
                "Hero stops running",
                "From reactive to proactive",
                "Major revelation or change",
                "Commit fully to goal"
            ]
        ),
        StoryBeat(
            name="Pinch Point 2",
            description="Apply maximum pressure. The villain seems unbeatable. Darkest moment.",
            percentage=70,
            chapter_hint="17-19",
            key_elements=[
                "Maximum antagonist power",
                "Lowest point for hero",
                "All seems lost",
                "Force final change"
            ]
        ),
        StoryBeat(
            name="Plot Turn 2",
            description="The hero gets or discovers what they need to win. The final piece.",
            percentage=80,
            chapter_hint="19-21",
            key_elements=[
                "Power to win obtained",
                "Final piece of puzzle",
                "Hero fully transformed",
                "Ready for climax"
            ]
        ),
        StoryBeat(
            name="Resolution",
            description="The climax and ending. The hero achieves their goal and shows transformation.",
            percentage=90,
            chapter_hint="22-25",
            key_elements=[
                "Climactic confrontation",
                "Hero uses new power/knowledge",
                "Goal achieved (or meaningful failure)",
                "Show transformation"
            ]
        )
    ]
)


# ============================================================================
#  FICHTEAN CURVE (Crisis to Crisis)
# ============================================================================
FICHTEAN_CURVE = StoryStructure(
    name="Fichtean Curve",
    description="Start in the middle of action. Crisis after crisis builds to climax. Minimal setup, maximum tension. Great for thrillers.",
    
    total_chapters_suggestion="15-25",
    best_for=["thriller", "horror", "action", "fast-paced stories"],
    
    beats=[
        StoryBeat(
            name="In Medias Res",
            description="Start in the middle of action. The story begins at a crisis point.",
            percentage=0,
            chapter_hint="1",
            key_elements=[
                "Begin with conflict/action",
                "Hook immediately",
                "Backstory later",
                "Establish stakes fast"
            ]
        ),
        StoryBeat(
            name="First Crisis",
            description="The first major challenge. Raises stakes and questions.",
            percentage=15,
            chapter_hint="3-5",
            key_elements=[
                "First major obstacle",
                "Tensions rise",
                "Character revealed through action"
            ]
        ),
        StoryBeat(
            name="Rising Crisis 1",
            description="Each crisis bigger than the last. Momentum builds.",
            percentage=30,
            chapter_hint="7-9",
            key_elements=[
                "Escalating tension",
                "Stakes increase",
                "New complications"
            ]
        ),
        StoryBeat(
            name="Rising Crisis 2",
            description="Another crisis, worse than before. The pressure is relentless.",
            percentage=45,
            chapter_hint="11-13",
            key_elements=[
                "Even higher stakes",
                "Character tested further",
                "No relief"
            ]
        ),
        StoryBeat(
            name="Rising Crisis 3",
            description="The penultimate crisis. Nearly unbearable tension. Everything at stake.",
            percentage=65,
            chapter_hint="15-18",
            key_elements=[
                "Maximum tension before climax",
                "All seems lost",
                "Final preparation"
            ]
        ),
        StoryBeat(
            name="Climax",
            description="The ultimate crisis. Everything resolves in an explosive confrontation.",
            percentage=85,
            chapter_hint="20-23",
            key_elements=[
                "Maximum stakes",
                "Final confrontation",
                "All threads converge"
            ]
        ),
        StoryBeat(
            name="Falling Action",
            description="Brief resolution after the climax. Catch breath, show new normal.",
            percentage=95,
            chapter_hint="24-25",
            key_elements=[
                "Aftermath",
                "New equilibrium",
                "Brief and satisfying"
            ]
        )
    ]
)


# ============================================================================
#  KISHOTENKETSU (Four-Act, No Conflict Required)
# ============================================================================
KISHOTENKETSU = StoryStructure(
    name="Kishotenketsu",
    description="Japanese/Chinese four-act structure. Introduction, development, twist, conclusion. Conflict optional. Great for slice-of-life, mystery reveals.",
    
    total_chapters_suggestion="12-20",
    best_for=["literary fiction", "slice of life", "mystery", "quiet stories", "twist endings"],
    
    beats=[
        StoryBeat(
            name="Ki (Introduction)",
            description="Introduce the world and characters. Establish the status quo.",
            percentage=0,
            chapter_hint="1-5 (25%)",
            key_elements=[
                "World and characters introduced",
                "Status quo established",
                "Tone set",
                "No conflict required yet"
            ]
        ),
        StoryBeat(
            name="Sho (Development)",
            description="Develop the characters and world. Deepen understanding. Build toward the twist.",
            percentage=25,
            chapter_hint="6-10 (25%)",
            key_elements=[
                "Deepen characterization",
                "Expand the world",
                "Develop themes",
                "Plant seeds for twist"
            ]
        ),
        StoryBeat(
            name="Ten (Twist)",
            description="The twist or turn. A revelation that recontextualizes everything. The surprise.",
            percentage=50,
            chapter_hint="11-15 (25%)",
            key_elements=[
                "Major twist or revelation",
                "Recontextualizes story",
                "The 'aha' moment",
                "Tension peaks here"
            ]
        ),
        StoryBeat(
            name="Ketsu (Conclusion)",
            description="Reconcile the twist with everything before. Bring harmony. Conclude with new understanding.",
            percentage=75,
            chapter_hint="16-20 (25%)",
            key_elements=[
                "Reconcile twist with earlier content",
                "New equilibrium",
                "Thematic resolution",
                "Satisfying conclusion"
            ]
        )
    ]
)


# ============================================================================
#  STORY STRUCTURE COLLECTION
# ============================================================================
STORY_STRUCTURES = [
    HEROS_JOURNEY,
    SAVE_THE_CAT,
    THREE_ACT,
    SEVEN_POINT,
    FICHTEAN_CURVE,
    KISHOTENKETSU
]


class StructureManager:
    """Manages story structure presets."""
    
    def __init__(self, structures_dir: Optional[Path] = None):
        if structures_dir is None:
            structures_dir = Path.home() / ".libriscribe" / "structures"
        
        self.structures_dir = Path(structures_dir)
        self.structures_dir.mkdir(parents=True, exist_ok=True)
        
        # Load built-in structures
        self.structures: Dict[str, StoryStructure] = {s.name: s for s in STORY_STRUCTURES}
        
        # Load custom structures
        self._load_custom_structures()
    
    def _load_custom_structures(self):
        """Load custom structures from directory."""
        for struct_file in self.structures_dir.glob("*.json"):
            try:
                with open(struct_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    struct = StoryStructure.from_dict(data)
                    self.structures[struct.name] = struct
            except Exception as e:
                print(f"Warning: Could not load structure {struct_file}: {e}")
    
    def list_structures(self) -> List[str]:
        """List all available structure names."""
        return list(self.structures.keys())
    
    def get_structure(self, name: str) -> Optional[StoryStructure]:
        """Get a structure by name."""
        return self.structures.get(name)
    
    def display_structures(self):
        """Display all available structures."""
        print("\n=== Available Story Structures ===\n")
        
        for name, struct in self.structures.items():
            print(f"**{name}**")
            print(f"  {struct.description}")
            print(f"  Best for: {', '.join(struct.best_for)}")
            print(f"  Beats: {len(struct.beats)}")
            print()
