# src/libriscribe/presets/default_presets.py
"""
Default Style Presets for Shakespeare AI

Built-in presets for various genres and styles.
"""

from .preset_manager import StylePreset


# ============================================================================
#  SPY MAKER - Max Monroe Style (Fleming prose, modern exclusive world)
# ============================================================================
SPY_MAKER = StylePreset(
    name="Spy Maker",
    description="Fleming's prose elegance + Sicario's brutal realism. Modern world: billionaire nightclubs, yacht parties, exotic supercars, beautiful dangerous women, and the brutal cost of the spy game.",
    
    inspired_by="Ian Fleming (prose style ONLY), Sicario, Mission: Impossible, John Wick",
    
    pacing_preference="fast",
    pacing_instruction="""**SPY MAKER PACING - ELEGANT VELOCITY:**

OPENING STYLE (The Caviar Rule):
- Open with a sensory luxury detail that establishes the modern elite world
- Introduce mystery/threat immediately in the first paragraph  
- Move from comfort to danger in three sentences or less
- The mundane becomes sinister: an unordered drink, a familiar face in the wrong place

SCENE PACING:
- Luxuriate in ONE sensory detail (the champagne, her perfume, the weapon's weight), then MOVE
- During action: short sentences, visceral verbs, no adjectives
- Tradecraft shown naturally, never lectures
- Dialogue loaded with subtext; what's NOT said matters more
- Every scene ends with a hook or revelation
- CLIFFHANGERS are essential - the reader MUST turn the page""",
    
    tone="Dangerous elegance, understated menace, world-weary sophistication, sexual tension",
    
    prose_style="""FLEMING'S PROSE STYLE IN A MODERN EXCLUSIVE WORLD:

THE MODERN ELITE PLAYGROUND:
- Exclusive billionaire nightclubs, rooftop parties, mega-yacht gatherings
- Racing speedboats off Monaco, exotic supercars (Maserati MC20, McLaren 720S, Lamborghini)
- High-stakes poker in private rooms, cryptocurrency deals, tech billionaire intrigue
- Modern locations: Dubai penthouses, Singapore marinas, Mykonos beach clubs, Monaco Grand Prix
- Bond-inspired luxury: Brioni suits, Omega watches, fine champagne, Beluga caviar - the good life
- Specific sensory details: the growl of a twin-turbo engine, champagne bubbles, designer perfume

WOMEN AND SEDUCTION:
- Beautiful, dangerous women - they have agendas, they seduce AND are seduced
- Sex and attraction written with heat but not vulgarity - tension, anticipation, consequence
- The femme fatale is smart, motivated, and possibly the most dangerous person in the room

VIOLENCE WITH WEIGHT (Sicario's influence):
- Violence has consequences. Characters are morally compromised.
- The protagonist is competent but not invincible. He makes mistakes. People die.
- Max's signature: SIG Sauer P365, Maserati MC20 - NOT Bond's Aston Martin or PPK
- Betrayal is constant - allies become enemies, lovers have hidden agendas

PROSE MECHANICS:
- Clean, muscular, precise. No purple passages.
- Settings tactile and specific - taste the vodka, feel the silk, smell gunpowder
- Interior life shown through what he NOTICES, not what he thinks
- Modern tech (encrypted phones, drones, facial recognition) integrated naturally

DO NOT USE: Aston Martin, Walther PPK, tuxedos, or any James Bond clichés.""",
    
    dialogue_style="""Dialogue is sparse and loaded with subtext.
Characters rarely say what they mean. Double meanings abound.
Seduction happens in conversation - verbal foreplay before physical.
Intelligence professionals speak in euphemisms and codes.
Antagonists are articulate and believe they're right.
NO exposition dumps - information earned through tension.
A glance says more than a speech. A touch is a promise or a threat.""",
    
    internal_monologue="minimal",
    sensory_detail="high",
    
    action_style="""Action is fast, brutal, and clinical.
SPY VS SPY: The opponent is equally skilled. Every encounter could go either way.
Use short, punchy sentences. Active verbs only.
Violence has weight and consequence - no cartoon heroics.
Modern weapons and tactics - the protagonist knows his craft.
Geography is clear - the reader should be able to draw the room.
Aftermath matters: wounds hurt, guilt lingers, adrenaline crashes.
Speed and machines: racing boats, supercars, helicopters - modern thrills.""",
    
    genre_hints=["espionage", "thriller", "political", "action", "romance", "seduction"],
    
    prose_rules=[
        "Open with sensory luxury that establishes the MODERN elite world",
        "Billionaire nightclubs, yacht parties, exotic supercars - young, exclusive, dangerous",
        "Beautiful dangerous women - seduction is a weapon used by AND against the hero",
        "Never explain emotions - show through action and sensory detail",
        "Luxury and danger coexist: champagne before a kill, blood on silk sheets",
        "BETRAYAL is constant - trust no one, especially the beautiful ones",
        "CLIFFHANGERS end every chapter - the reader must turn the page",
        "SPY VS SPY - antagonists are equally skilled and intelligent",
        "Modern realistic tech and weapons - no cartoon gadgets, no magic solutions",
        "Tradecraft shown, not explained. Trust the reader's intelligence",
        "Villains believe they are heroes. Give them dignity and intelligence",
        "Every mission costs something - innocence, love, pieces of his soul",
        "Write action cinematically: short shots, clear geography, visceral impact",
        "MAX'S SIGNATURE: SIG Sauer P365 and Maserati MC20 - avoid Aston Martin and PPK (those are Bond's)",
        "MYSTERY layers - questions raised, answers delayed, revelations earned"
    ],
    
    scene_length="800-1200 words",
    chapter_length="3000-4500 words"
)


# ============================================================================
#  EPIC ROMANCE - Titanic meets Star Wars
# ============================================================================
EPIC_ROMANCE = StylePreset(
    name="Epic Romance",
    description="Sweeping romantic epic: Titanic's heart-pounding love story with Star Wars-scale stakes",
    
    inspired_by="Titanic, Star Wars, Outlander, The Notebook, Romeo and Juliet",
    
    pacing_preference="fast",
    pacing_instruction="""**EPIC ROMANCE PACING - EMOTIONAL VELOCITY:**
- Open scenes with action, sensory immersion, or emotional stakes
- The love story is the SPINE - every scene advances the romance
- Use 'Titanic tempo': fast-moving plot that PAUSES for key emotional beats
- Internal monologue earned in pivotal moments (first sight, first touch, sacrifice)
- External conflict drives the lovers together, not apart
- Joy before tragedy - build happiness before shattering it
- Every scene should make the reader FEEL something""",
    
    tone="Sweeping, passionate, emotionally intense, epic scale",
    
    prose_style="""Write like Cameron directed Titanic: grand, romantic, but never slow.
The romance is SHOWN through action and gesture, not told through reflection.
Sensory details heighten emotional moments: the scent of him, the heat of her touch.
Stakes are galactic but the story is intimate - two hearts against the universe.
Use Cameron's technique: humor and lightness before devastation.""",
    
    dialogue_style="""Dialogue reveals character and builds chemistry.
Lovers speak differently to each other than to others.
Banter shows attraction. Vulnerability shows depth.
The forbidden aspect adds tension to every conversation.
Key lines become memorable: 'I'm the king of the world' moments.""",
    
    internal_monologue="moderate",  # Allowed for pivotal emotional moments
    sensory_detail="high",
    
    action_style="""Action serves the love story, not the other way around.
Danger brings lovers together. Near-death intensifies connection.
Fight scenes show character: protectiveness, sacrifice, courage.
Physical peril mirrors emotional peril.
The hero/heroine's competence is attractive.""",
    
    genre_hints=["romance", "epic", "science fiction", "adventure", "fantasy"],
    
    prose_rules=[
        "The love story is the spine - every scene advances the romance",
        "Physical chemistry is SHOWN: lingering looks, accidental touches, breath catching",
        "Build joy before tragedy - 'I'm flying, Jack' moments before the iceberg",
        "Internal reflection ONLY at pivotal moments (first sight, revelation, sacrifice)",
        "Forbidden love adds delicious tension - make the obstacles real",
        "Character appearances matter - describe what attracts them to each other",
        "Grand settings enhance romance: starfields, ancient temples, crashing waves",
        "Secondary characters highlight the central romance by contrast",
        "Time pressure intensifies romance - they don't have forever",
        "The ending earns its emotion through everything that came before"
    ],
    
    scene_length="800-1500 words",
    chapter_length="4000-6000 words"
)


# ============================================================================
#  LITERARY FICTION - Dune meets Blood Meridian
# ============================================================================
LITERARY_EPIC = StylePreset(
    name="Literary Epic",
    description="Atmospheric literary fiction: Dune's world-building depth with McCarthy's prose intensity",
    
    inspired_by="Dune, Blood Meridian, The Name of the Wind, Gormenghast",
    
    pacing_preference="slow",
    pacing_instruction="""**LITERARY EPIC PACING - ATMOSPHERIC WEIGHT:**
- Let scenes breathe. Build atmosphere before action.
- Internal monologue is currency - spend it on philosophy and revelation
- Description creates mood: landscape as character
- Dialogue sparse but heavy with meaning
- Time passes in poetic montage when necessary
- Build dread through accumulated detail, not explicit threat""",
    
    tone="Philosophical, atmospheric, morally complex, mythic",
    
    prose_style="""Write like Herbert and McCarthy had a child.
Sentences can be long, complex, beautiful. But each word earns its place.
Nature and landscape are characters. Weather has meaning.
Violence is operatic and horrifying, never casual.
Ideas and themes are embedded in action, never lectured.""",
    
    dialogue_style="""Dialogue is sparse and weighted with meaning.
Characters speak formally or poetically when appropriate.
Philosophical debates occur in action, not in sitting rooms.
Power dynamics expressed through how characters address each other.""",
    
    internal_monologue="heavy",
    sensory_detail="high",
    
    action_style="""Action is mythic and operatic.
Violence has consequences that reverberate.
Combat described through poetic imagery.
The physical landscape participates in conflict.""",
    
    genre_hints=["literary fiction", "epic fantasy", "science fiction", "western"],
    
    prose_rules=[
        "Every scene builds atmosphere before action",
        "Nature and landscape are active characters",
        "Philosophical themes embedded in action, never lectures",
        "Violence is mythic, consequential, never casual",
        "Internal monologue explores character philosophy",
        "Dialogue weighted with subtext and meaning",
        "Time can expand and contract poetically",
        "Imagery recurs with variation - motifs bind the narrative"
    ],
    
    scene_length="1200-2000 words",
    chapter_length="5000-8000 words"
)


# ============================================================================
#  THRILLER PACE - Lee Child meets Michael Connelly
# ============================================================================
THRILLER_PACE = StylePreset(
    name="Thriller Pace",
    description="Pure thriller velocity: Lee Child's short sentences with Connelly's procedural depth",
    
    inspired_by="Lee Child (Jack Reacher), Michael Connelly, Dennis Lehane, Gillian Flynn",
    
    pacing_preference="fast",
    pacing_instruction="""**THRILLER PACING - RELENTLESS MOMENTUM:**
- Short chapters. Often 2-4 pages.
- End every chapter on a hook
- Short paragraphs. Often one sentence.
- Present tense creates immediacy (optional)
- Information revealed in drips, never dumps
- Clock always ticking - deadlines drive the plot""",
    
    tone="Tense, propulsive, street-smart, noir-inflected",
    
    prose_style="""Write like Child: Subject. Verb. Period. Short sentences that punch.
But with Connelly's eye for procedural detail that creates authenticity.
Observation is character. What the protagonist notices reveals who they are.
Blue-collar poetry. Working-class wisdom. Street philosophy.""",
    
    dialogue_style="""Dialogue is clipped and real. People interrupt each other.
Lies are common. The reader should sense them before the protagonist.
Interrogations are power struggles. Who asks the questions controls the room.
Wisecracks only if character earns them.""",
    
    internal_monologue="minimal",
    sensory_detail="moderate",
    
    action_style="""Action is concrete and physical. Geography matters.
Every punch lands. Every shot has consequence.
The protagonist takes damage. Bodies break.
Violence solves problems and creates new ones.""",
    
    genre_hints=["thriller", "crime", "mystery", "noir"],
    
    prose_rules=[
        "Short sentences during action. Long sentences between.",
        "End chapters on hooks. Always.",
        "Clocks tick. Deadlines loom. Urgency is constant.",
        "Procedural details create authenticity",
        "Observation reveals character",
        "Violence has physical consequence",
        "Information dripped, never dumped",
        "Short chapters keep pages turning"
    ],
    
    scene_length="600-1000 words",
    chapter_length="2000-3500 words"
)


# ============================================================================
#  COZY MYSTERY - Lighthearted and charming
# ============================================================================
COZY_MYSTERY = StylePreset(
    name="Cozy Mystery",
    description="Charming, lighthearted mystery: clever puzzles in delightful settings",
    
    inspired_by="Agatha Christie, Alexander McCall Smith, Richard Osman",
    
    pacing_preference="balanced",
    pacing_instruction="""**COZY MYSTERY PACING - GENTLE ENGAGEMENT:**
- Let readers enjoy the setting and characters
- Clues planted fairly - the reader could solve it
- Humor woven throughout, not in clumps
- Character relationships matter as much as mystery
- Comfortable but not boring - intrigue maintains interest""",
    
    tone="Warm, witty, charming, lighthearted but clever",
    
    prose_style="""Write with warmth and wit. The narrator is a friend, not a lecturer.
Settings should be inviting, even when danger lurks.
Food, tea, and domestic details add comfort.
Death may occur but gore does not.""",
    
    dialogue_style="""Dialogue is charming and reveals character.
Wit is valued. Banter is encouraged.
Suspects are interesting people, not cardboard villains.
Amateur sleuths ask clever questions.""",
    
    internal_monologue="moderate",
    sensory_detail="moderate",
    
    action_style="""Minimal violence, no graphic descriptions.
Chase scenes can be comedic.
Danger exists but isn't overwhelming.
The protagonist outthinks, not outfights.""",
    
    genre_hints=["cozy mystery", "amateur sleuth", "small town"],
    
    prose_rules=[
        "Violence off-page or minimal",
        "Food and comfort details welcome",
        "Wit and warmth in equal measure",
        "Clues planted fairly",
        "Community and relationships matter",
        "Settings should be cozy and appealing"
    ],
    
    scene_length="1000-1500 words",
    chapter_length="3000-4500 words"
)


# ============================================================================
#  DARK FANTASY - Grimdark with heart
# ============================================================================
DARK_FANTASY = StylePreset(
    name="Dark Fantasy",
    description="Grimdark fantasy: Joe Abercrombie's cynicism with genuine emotional stakes",
    
    inspired_by="Joe Abercrombie (First Law), Mark Lawrence, Robin Hobb",
    
    pacing_preference="balanced",
    pacing_instruction="""**DARK FANTASY PACING - SHADOW AND LIGHT:**
- Action scenes brutal and kinetic
- Quiet scenes build character depth
- Cynicism punctuated by unexpected tenderness
- Dark humor throughout - characters cope through jokes
- Battle chapters fast; aftermath chapters slow""",
    
    tone="Cynical but not nihilistic, darkly humorous, morally gray, visceral",
    
    prose_style="""Write like Abercrombie: wry, cynical, but with a beating heart beneath.
Violence is ugly and has consequence. Glory is a lie.
Characters are flawed but readers root for them anyway.
Dark humor is survival. Tenderness is rare and precious.""",
    
    dialogue_style="""Dialogue is wry and realistic. Medieval formality unnecessary.
Characters swear, joke, and lie. They have distinct voices.
Villains have points. Heroes make mistakes.
Banter between unlikely companions.""",
    
    internal_monologue="moderate",
    sensory_detail="high",
    
    action_style="""Combat is ugly, desperate, terrifying.
There are no clean victories.
Fear is constant. Survival is victory.
The aftermath matters: wounds fester, minds break.""",
    
    genre_hints=["dark fantasy", "grimdark", "epic fantasy"],
    
    prose_rules=[
        "Violence has weight and consequence",
        "Heroes are flawed; villains are human",
        "Dark humor is survival mechanism",
        "Tenderness rare but powerful",
        "No clean victories",
        "Cynicism and hope in tension"
    ],
    
    scene_length="800-1500 words",
    chapter_length="4000-6000 words"
)


# ============================================================================
#  SCI-FI HORROR - Alien meets The Thing
# ============================================================================
SCI_FI_HORROR = StylePreset(
    name="Sci-Fi Horror",
    description="Scientific terror: Alien's claustrophobic dread + The Thing's paranoid horror. For creature features, cosmic horror, and science gone wrong.",
    
    inspired_by="Alien, The Thing, Annihilation, Event Horizon, Jurassic Park, The Mist",
    
    pacing_preference="balanced",
    pacing_instruction="""**SCI-FI HORROR PACING - DREAD AND RELEASE:**

THE BUILD:
- Start with normalcy, then introduce the WRONGNESS
- Escalate slowly at first, then accelerate
- False safety moments before horror strikes
- Let tension build through what characters DON'T see

THE HORROR:
- Brief, intense horror sequences followed by aftermath
- Show the cost: bodies, trauma, resources depleting
- The creature/threat should be rarely seen fully at first
- Each encounter should be worse than the last

RHYTHM:
- Quiet dread → investigation → glimpse of horror → aftermath → worse dread
- Chapter endings: either cliffhanger OR false calm before the storm""",
    
    tone="Creeping dread, scientific wonder turned nightmare, survival desperation, paranoid tension",
    
    prose_style="""TERROR WITH BRAINS:

ATMOSPHERE:
- Isolation is key: remote locations, no escape, no help coming
- Environment becomes hostile: darkness, cold, confined spaces
- Technology fails when needed most
- Nature/science is indifferent to human survival

THE CREATURE/THREAT:
- Less is more: glimpses, sounds, evidence of its passage
- Make it WEIRD - unsettling wrongness, not just dangerous
- It has rules (scientific or cosmic) that characters must figure out
- Each reveal should deepen the horror, not diminish it

SCIENTIFIC GROUNDING:
- Characters think scientifically, try to understand the threat
- Real science terminology used correctly
- The horror comes from WHAT the science reveals
- Rational characters making rational choices that still fail

VISCERAL HORROR:
- Body horror: transformation, infection, consumption
- Sensory details: sounds, smells, textures of wrongness
- Death is ugly, messy, terrifying
- Survivors are traumatized, not heroic""",
    
    dialogue_style="""Dialogue is tense, clipped, desperate.
Characters argue under stress - conflict reveals character.
Scientific explanations delivered with growing horror.
Someone always wants to do the wrong thing.
Final girl/survivor earns their survival through intelligence.
Silence speaks louder than words in horror.""",
    
    internal_monologue="moderate",
    sensory_detail="high",
    
    action_style="""Horror action is SURVIVAL, not combat.
The creature is almost always faster, stronger, deadlier.
Running, hiding, desperate improvisation.
Geography matters: where are the exits, what can be used as weapon?
Violence against the creature rarely works as expected.
Human vs human conflict under stress: who breaks, who betrays?""",
    
    genre_hints=["horror", "science fiction", "thriller", "creature feature", "survival"],
    
    prose_rules=[
        "Isolation is essential - no cavalry coming, limited resources",
        "The creature/threat is WRONG - unsettling, not just dangerous",
        "Less is more - glimpses before full reveal",
        "Science explains but doesn't comfort - knowledge brings horror",
        "Body horror: transformation, infection, consumption",
        "Characters make SMART choices that still fail",
        "Trust breaks down - paranoia and suspicion",
        "Environment is hostile - darkness, cold, confined spaces",
        "Death is ugly and terrifying - not heroic",
        "Survivors earn survival through intelligence, not luck",
        "Each encounter WORSE than the last - escalating horror",
        "False safety before horror strikes - let readers breathe, then strike"
    ],
    
    scene_length="1000-1500 words",
    chapter_length="3500-5000 words"
)


# ============================================================================
#  CREATURE FEATURE - Monster Horror (Chupacabra, Cryptids, etc.)
# ============================================================================
CREATURE_FEATURE = StylePreset(
    name="Creature Feature",
    description="Monster horror: cryptids, creatures, and things that hunt in the dark. Jaws meets folklore. For Chupacabra, werewolves, and unknown predators.",
    
    inspired_by="Jaws, Tremors, The Descent, Dog Soldiers, Predator, folklore and cryptid legends",
    
    pacing_preference="fast",
    pacing_instruction="""**CREATURE FEATURE PACING - HUNT AND HUNTED:**

ACT ONE: THE MYSTERY
- Strange deaths, mutilated animals, missing people
- Locals dismiss, outsider investigates
- First glimpse of the creature - brief, terrifying
- Disbelief gives way to dawning horror

ACT TWO: THE SIEGE
- Characters trapped with the creature(s)
- Dwindling numbers, escalating stakes
- Learn the creature's rules: what attracts it, what hurts it
- Failed attempts to escape or fight back

ACT THREE: THE HUNT
- Roles reverse: hunted becomes hunter
- Use what was learned to fight back
- Final confrontation: personal, visceral, costly
- Survival, not victory - the creature may return""",
    
    tone="Primal fear, survival instinct, folklore dread, visceral terror",
    
    prose_style="""MONSTER IN THE DARK:

THE CREATURE:
- Root in real folklore/cryptid legends when possible
- Give it rules: feeding patterns, weaknesses, behaviors
- Show its intelligence or cunning
- Physical descriptions that feel WRONG: too many limbs, wrong proportions

SETTING AS CHARACTER:
- Remote location: swamps, forests, deserts, mountains
- Local culture and legends foreshadow the truth
- Environment helps or hinders both prey and predator
- Night is when it hunts

THE HUNT:
- Creature is apex predator - humans are prey
- Track the creature, learn its patterns
- Small victories before major confrontation
- Creature has personality: cunning, rage, hunger

GORE AND BODY HORROR:
- Show the aftermath of attacks
- Physical cost on survivors
- The creature's biology is horrifying
- Death scenes are memorable and terrifying""",
    
    dialogue_style="""Dialogue reveals character under extreme stress.
Locals know more than they admit - folklore as warning.
Arguments about what to do, who to trust.
Gallows humor from some, breakdown from others.
The expert/outsider explains what they're facing.
Final survivor speaks in trauma.""",
    
    internal_monologue="minimal",
    sensory_detail="high",
    
    action_style="""Action is primal: run, hide, fight, die.
The creature is FAST - you don't outrun it.
Improvised weapons, desperate tactics.
Geography of the kill: where it hunts, where it can't reach.
Character deaths should be shocking and visceral.
Final fight is personal and brutal.""",
    
    genre_hints=["horror", "creature feature", "thriller", "survival", "folklore"],
    
    prose_rules=[
        "The creature is rooted in folklore/legend - give it history",
        "Remote location, isolated characters, no help coming",
        "Show its intelligence - this is a predator, not mindless",
        "Physical descriptions emphasize WRONGNESS",
        "Gore serves the horror - aftermath of attacks",
        "Characters figure out the creature's rules",
        "Night is when it hunts - darkness is danger",
        "Local legends foreshadow the truth",
        "Death scenes are memorable and terrifying",
        "Survival is earned through cunning, not strength",
        "The creature may return - horror doesn't end clean"
    ],
    
    scene_length="800-1200 words",
    chapter_length="3000-4500 words"
)


# ============================================================================
#  PRESET COLLECTION
# ============================================================================
PRESETS = [
    SPY_MAKER,
    EPIC_ROMANCE,
    LITERARY_EPIC,
    THRILLER_PACE,
    COZY_MYSTERY,
    DARK_FANTASY,
    SCI_FI_HORROR,
    CREATURE_FEATURE
]
