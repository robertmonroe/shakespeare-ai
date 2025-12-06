# Git Commit for v2.1.0

## Commit Message:
feat: v2.1.0 - Critical Context Integration \u0026 Backup Fixes

BREAKING CHANGES:
- Chapter writer and reviewer now require full character/world context
- .gitignore updated to allow AI editing of project files

CRITICAL FIXES:
- Chapter writer now uses full character descriptions from characters.json
- Reviewer now uses full character/world context, preventing false positives
- Automatic backups now work in all edit modes
- JSON parsing handles invalid escape sequences from LLM
- Task feedback shows actual actions applied

This release fixes the #1 source of inconsistencies (missing context) and
prevents data loss with automatic backups.

Files changed:
- src/libriscribe/agents/chapter_writer.py
- src/libriscribe/agents/chapter_flow/review_manager.py
- src/libriscribe/agents/chapter_flow/chapter_flow_manager.py
- src/libriscribe/agents/decision_agent.py
- src/libriscribe/agents/task_based_editor.py
- src/libriscribe/utils/prompts_context.py
- .gitignore
- CHANGELOG.md

## Git Commands:
git add .
git commit -m \"feat: v2.1.0 - Critical Context Integration \u0026 Backup Fixes\"
git tag v2.1.0
git push origin main
git push origin v2.1.0

## Release Notes:
Shakespeare AI v2.1.0 - Production Ready

This release completes the integration of characters.json and world.json
into the writing and review pipelines, eliminating inconsistencies and
false positives. Combined with automatic backups, the system is now
production-ready for professional use.

Key improvements:
- Writers get full character context (no more made-up descriptions)
- Reviewers understand context (no more false errors)
- Automatic backups prevent data loss
- Better error handling and feedback

Status: PRODUCTION READY
