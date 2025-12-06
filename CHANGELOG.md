# 🎭 Shakespeare AI - Changelog

All notable changes to Shakespeare AI will be documented in this file.

*Forked from [Libriscribe](https://github.com/guerra2fernando/libriscribe) by Fernando Guerra*

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-12-06

### Added - Style Presets & Story Structures System

- **Style Presets** - Reusable writing style configurations
  - `Spy Maker` - Fleming prose + modern elite world (Max Monroe style)
  - `Epic Romance` - Titanic + Star Wars emotional velocity
  - `Sci-Fi Horror` - Alien + The Thing atmosphere
  - `Creature Feature` - Jaws/cryptid horror (for Chupacabra, etc.)
  - `Literary Epic` - Dune + McCarthy atmospheric prose
  - `Thriller Pace` - Lee Child short-sentence velocity
  - `Cozy Mystery` - Agatha Christie warmth
  - `Dark Fantasy` - Abercrombie grimdark with heart

- **Story Structures** - Plot beat frameworks for outlining
  - `Hero's Journey` - Campbell/Vogler 12-beat monomyth
  - `Save the Cat` - Blake Snyder's 15-beat commercial structure
  - `Three-Act Structure` - Classic dramatic framework
  - `Seven-Point` - Dan Wells' tight plotting system
  - `Fichtean Curve` - Crisis-to-crisis thriller pacing
  - `Kishotenketsu` - Japanese 4-act twist-based structure

- **Preset Manager** (`src/libriscribe/presets/`)
  - `PresetManager` class for loading/saving/applying style presets
  - `StructureManager` class for story structure templates
  - Custom preset support (save to `~/.libriscribe/presets/`)
  - Integration with prompts_context.py for automatic style injection

### Changed

- **prompts_context.py** - Added preset integration helpers
  - `get_style_guide_from_preset()` - Load style from preset name
  - `get_pacing_from_preset()` - Load pacing instructions from preset
  - `get_prose_rules_from_preset()` - Load prose rules from preset

### Files Added

- `src/libriscribe/presets/__init__.py`
- `src/libriscribe/presets/preset_manager.py`
- `src/libriscribe/presets/default_presets.py`
- `src/libriscribe/presets/story_structures.py`

---

## [2.2.0] - 2024-12-06

### Added - Quality & Consistency Improvements

- **Style Guide System** - New pacing and tone control throughout the pipeline
  - Added `inspired_by` field to specify style influences (e.g., "Titanic, Star Wars")
  - Added `pacing_preference` field ("fast", "slow", "balanced")
  - SCENE_PROMPT and EDITOR_PROMPT now include style guide instructions
  - Automatic pacing detection based on inspired_by (Titanic = fast, Dune = slow)

- **Enhanced Content Reviewer** - Now checks character and world consistency
  - Loads character descriptions from characters.json to verify consistency
  - Loads worldbuilding from world.json for setting verification
  - Loads chapter outline to verify plot adherence
  - New review categories: Character Consistency, Worldbuilding Consistency, Pacing & Flow, Prose Quality, Emotional Beats
  - Catches issues like incorrect skin/hair color that were previously missed

- **Previous Chapter Context** - Scene writer now knows what came before
  - Added previous_chapter_summary to SCENE_PROMPT for chapter-to-chapter continuity
  - Added previous_scenes context within chapters (each scene knows prior scenes)
  - Prevents character knowledge inconsistencies and timeline breaks

- **Character Appearance Field** - Explicit visual description field
  - Added `appearance` field to Character model separate from physical_description
  - Character appearances now displayed prominently in prompts
  - Reduces description drift across chapters

- **Show Don't Tell Instructions** - Built-in prose quality guidance
  - SCENE_PROMPT includes explicit "show don't tell" instructions
  - Limits internal monologue to critical moments
  - Encourages sensory details and action-based emotion

### Changed

- **Increased Scene Token Limit** - Raised from 2000 to 4000 tokens per scene
  - Allows richer, more detailed scenes
  - Especially important for emotional/romantic scenes

- **Enhanced Editor Context** - Editor now receives style_guide
  - Edits respect project pacing preferences
  - Better character appearance consistency checking

- **Safer Worldbuilding Access** - Fixed dict/object handling in chapter_writer
  - Now handles both dict and Worldbuilding object correctly
  - Added hasattr checks for safer field access

### Fixed

- **Review Missing Context** - Critical fix for reviewer false positives
  - Reviewer now has full character, world, and outline context
  - No more flagging correct descriptions as errors

- **Scene Isolation Issue** - Scenes now aware of previous scenes
  - Previously each scene written without chapter context
  - Now maintains emotional and plot continuity within chapters

## [2.1.0] - 2024-12-05


### Added
- **Full Context Integration** - Chapter writer and reviewer now use complete character & world data
  - Character descriptions, personality, role, backstory from characters.json
  - World details (geography, culture, locations) from world.json
  - Chapter outline context for better consistency checking
  
- **Automatic Backup System** - Backups created before every chapter edit
  - Works in both manual and auto-review modes
  - Prevents data loss from editing errors
  
### Fixed
- **CRITICAL: Chapter Writer Context** - Now receives full character descriptions and world details
  - Previously only received character names, causing inconsistencies
  - Added `_build_character_context()` and `_build_world_context()` methods
  - Updated SCENE_PROMPT with `{character_details}` and `{world_details}` fields
  
- **CRITICAL: Reviewer Context** - Now receives full character and world data
  - Previously only received character names, causing false positives
  - Added context-aware instructions to prevent flagging correct descriptions
  - Added dialogue vs. narrative distinction (nicknames aren't description errors)
  
- **JSON Parsing Errors** - Fixed invalid escape sequence handling
  - LLM sometimes returns JSON with invalid escapes (e.g., `\e`)
  - Added regex sanitization before parsing
  
- **Task Feedback Display** - Now shows what action was applied
  - Previously only showed generic "Task completed"
  - Falls back to action description if no detailed summary
  
- **Backup System** - Now works in auto-review mode
  - Previously only created backups in manual edit mode
  - Added backup creation to `edit_chapter()` method

### Changed
- Disabled `projects/` in `.gitignore` for better AI assistant integration
- Enhanced review prompt with critical instructions about context
- Enhanced scene prompt with character and world details

## [2.0.0] - 2024-12-04

### Added
- **Director Agent** - Natural language creative control interface
  - `IntentParser` for command interpretation
  - `ImpactAnalyzer` for change scope estimation
  - User confirmation before applying changes
  
- **Autonomous Project-Wide Modifier** - Complete consistency across all files
  - `ProjectFileScanner` - Reads all project files
  - `ChangeAnalyzer` - LLM-powered change analysis
  - `AutonomousExecutor` - Applies coordinated updates
  
- **Change Handlers**
  - `AutonomousCharacterHandler` - Character attribute changes
  - `GrammarCorrectionHandler` - Simple find/replace
  - `PronounFixerHandler` - Context-aware pronoun fixing
  - `ReportAnalyzerHandler` - Editorial report analysis
  
- **Universal Report Analyzer**
  - Support for TXT, MD, RTF, DOCX, PDF formats
  - Vision analysis for DOCX embedded images
  - Vision analysis for PDF charts/graphs (via Poppler)
  - Generates actionable editorial plans
  
- **Document Reading**
  - `DocumentReader` utility for universal format support
  - Gemini Vision integration for image analysis
  - Poppler integration for PDF image extraction
  
- **Vision Support in LLM Client**
  - `generate_content_with_image()` method
  - Gemini 2.0 Flash Exp for vision tasks
  
- **Director Mode Menu** - New menu option in main interface

### Changed
- `CharacterGenderHandler` replaced with `AutonomousCharacterHandler`
- Updated all change handlers to use autonomous system
- Enhanced `ImpactAnalyzer` with new intent types

### Fixed
- Project-wide consistency issues (outline.md, scenes.json, worldbuilding.json now updated)
- Character changes now affect ALL relevant files

### Documentation
- Comprehensive MEMORY.md with complete project state
- Updated README.md with new features
- Implementation plans for Execute Action Plan
- Walkthroughs for major features

## [1.0.0] - 2024-11-XX

### Added
- Initial release
- Core writing system
- Chapter generation
- Multi-pass review & editing
- Character & world management
- Outline-driven development
- Chat interface

---

## [Unreleased]

### Planned for v2.1
- Execute Action Plan handler
- Refine Action Plan capability
- Preview mode for changes
- Undo/redo functionality

### Planned for v2.2
- Plot modification commands
- Worldbuilding change commands
- Tone/style adjustments
- Enhanced consistency verification

### Planned for v3.0
- EditScribe integration
- Multi-user collaboration
- Version control
- Quality metrics dashboard
