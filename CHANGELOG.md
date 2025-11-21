# Changelog

All notable changes to Shakespeare AI (formerly Libriscribe) are documented here.

## [Unreleased] - 2025-11-20

### Fixed

#### Chapter Count Generation
- **Flexible chapter counts**: AI now generates variable chapter counts within defined ranges instead of always forcing the maximum
  - Short Stories: 1-3 chapters (previously always 2)
  - Novellas: 5-8 chapters (previously always 8)
  - Novels: 15-30 chapters (previously always 20, capped at max)
- **Substring matching**: Fixed book length detection to handle formatted strings like "Short Story (1-3 chapters)"
- **Updated max limits**: Increased Novel maximum from 20 to 30 chapters to support longer works

#### PDF Generation
- **Fixed PDF truncation**: Removed LLM-based formatting that was causing content to be cut off due to token limits
- **Multi-page support**: Books now generate complete PDFs with all chapters, not just the first page
- **Unicode handling**: Added text sanitization to handle special characters (em dashes, smart quotes, etc.) that caused encoding errors

#### Core Functionality
- **KeyError 'language'**: Fixed missing language parameter in formatting prompts
- **AttributeError fixes**: Resolved duplicate Pydantic field definitions and syntax errors in ProjectManagerAgent
- **Pydantic validation**: Made `worldbuilding` field optional to support existing project files
- **Import errors**: Added missing `import re` and `import logging` statements

#### UI/UX
- **Advanced Mode menu**: Fixed unexpected program exit by removing premature `break` statements
- **Menu navigation**: Restored proper `typer.prompt` logic for menu interactions

### Changed
- Increased maximum chapter limits to better match real-world book lengths
- Improved LLM prompts to encourage natural story pacing

### Technical Details
**Files Modified:**
- `src/libriscribe/agents/outliner.py` - Chapter count logic and prompts
- `src/libriscribe/agents/project_manager.py` - PDF generation and formatting
- `src/libriscribe/knowledge_base.py` - Pydantic model fixes
- `src/libriscribe/utils/llm_client.py` - Import fixes
- `src/libriscribe/main.py` - Menu navigation fixes

---

## About This Fork

This is a fork of [guerra2fernando/libriscribe](https://github.com/guerra2fernando/libriscribe) with significant bug fixes and improvements focused on chapter generation flexibility and PDF output reliability.
