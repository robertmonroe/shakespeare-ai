# 🎭 Shakespeare AI - Project Memory & Context

**Last Updated:** 2025-12-06  
**Project Owner:** Robert Monroe  
**Repository:** https://github.com/robertmonroe/shakespeare-ai
**Current Version:** 2.3.0
**Forked From:** [Libriscribe](https://github.com/guerra2fernando/libriscribe) by Fernando Guerra

---

## 🎯 Project Overview

**Shakespeare AI** is an AI-powered book writing assistant that uses a sophisticated multi-agent system to help authors create complete books from concept to final manuscript. Each AI agent specializes in specific tasks (concept generation, outlining, character development, worldbuilding, chapter writing, editing, etc.).

### Core Technology Stack
- **Language:** Python 3.8+
- **AI/LLM Integration:** Multi-provider support (OpenAI, Anthropic Claude, Google Gemini, DeepSeek, Mistral)
- **Architecture:** Multi-agent system with specialized agents
- **CLI Framework:** Typer
- **UI Library:** Rich (for terminal UI)
- **PDF Generation:** FPDF
- **File Formats:** Markdown, JSON, PDF

---

## 📂 Project Structure

```
libriscribe/
├── src/libriscribe/
│   ├── agents/                    # AI agent implementations
│   │   ├── project_manager.py     # Main orchestrator
│   │   ├── chapter_flow/          # Chapter workflow management
│   │   │   ├── __init__.py
│   │   │   ├── chapter_flow_manager.py
│   │   │   ├── backup_manager.py
│   │   │   └── review_manager.py
│   │   ├── concept_generator.py
│   │   ├── outliner.py
│   │   ├── character_generator.py
│   │   ├── worldbuilding.py
│   │   ├── chapter_writer.py
│   │   ├── editor.py
│   │   ├── content_reviewer.py
│   │   ├── style_editor.py
│   │   ├── plagiarism_checker.py
│   │   └── fact_checker.py
│   ├── presets/                   # Style & Structure Presets (NEW v2.3.0)
│   │   ├── __init__.py
│   │   ├── preset_manager.py      # PresetManager class
│   │   ├── default_presets.py     # 8 built-in style presets
│   │   └── story_structures.py    # 6 story structure frameworks
│   ├── knowledge_base.py          # Project data models
│   ├── settings.py                # Configuration
│   ├── main.py                    # CLI entry point
│   └── utils/
│       ├── llm_client.py          # Multi-LLM abstraction
│       ├── file_utils.py
│       └── prompts_context.py
├── projects/                      # User-created book projects
├── prompts/                       # LLM prompt templates
├── docs/                          # Documentation
├── n8n_workflows/                 # N8N automation workflows
└── requirements.txt
```

---

## 🔄 Recent Major Changes (Dec 2025)

### v2.3.0 - Style Presets & Story Structures System
**Date:** 2025-12-06  
**Status:** ✅ Complete

#### What Changed:
Added a comprehensive presets system for controlling writing style and story structure:

1. **Style Presets** (HOW to write):
   - `Spy Maker` - Fleming prose + modern elite world (Max Monroe)
   - `Epic Romance` - Titanic + Star Wars emotional velocity
   - `Sci-Fi Horror` - Alien + The Thing atmosphere
   - `Creature Feature` - Jaws/cryptid horror
   - `Literary Epic` - Dune + McCarthy atmospheric prose
   - `Thriller Pace` - Lee Child short-sentence velocity
   - `Cozy Mystery` - Agatha Christie warmth
   - `Dark Fantasy` - Abercrombie grimdark

2. **Story Structures** (WHAT to write):
   - `Hero's Journey` - Campbell/Vogler 12-beat monomyth
   - `Save the Cat` - Blake Snyder's 15-beat commercial structure
   - `Three-Act Structure` - Classic dramatic framework
   - `Seven-Point` - Dan Wells' tight plotting
   - `Fichtean Curve` - Crisis-to-crisis thriller pacing
   - `Kishotenketsu` - Japanese 4-act twist-based

#### Benefits:
- ✅ Consistent writing style across projects
- ✅ Easy to switch between genres/styles
- ✅ Story beat guidance for outlining
- ✅ Custom presets can be saved
- ✅ Automatic style injection into prompts

---

### v2.2.0 - Quality & Consistency Improvements  
**Date:** 2025-12-06  
**Status:** ✅ Complete

### 🔧 In Progress
- [ ] N8N workflow integration
- [ ] Web-based UI

---

## 🚀 Roadmap (From ROADMAP.md)

### High Priority
- [ ] Model Performance Benchmarking
- [ ] Automatic Model Fallback System
- [ ] Cost Optimization Engine
- [ ] Vector Database Support (ChromaDB, MongoDB, Pinecone, Weaviate)
- [ ] Advanced Search (Semantic, Hybrid, Cross-Reference)

### Medium Priority
- [ ] Authentication & Authorization (Cerbos)
- [ ] User Management System
- [ ] RESTful API Development
- [ ] GraphQL Interface
- [ ] WebSocket Support

### Future Vision
- [ ] Modern React Frontend
- [ ] Real-time Collaboration
- [ ] Character Relationship Graphs
- [ ] Plot Timeline Visualization
- [ ] World Map Generation
- [ ] Story Arc Visualization

---

## 🔑 Key Workflows

### Chapter Writing Workflow

#### AI Mode (Interactive):
1. Write chapter using `ChapterWriterAgent`
2. Review chapter using `ReviewManager`
3. User chooses:
   - Apply fixes → Create backup → Edit with `EditorAgent` → Review again
   - Restore backup → Select from numbered backups → Review
   - Continue to next chapter or finish

#### Human Mode (Simple):
1. Write chapter
2. Review chapter
3. Continue to next chapter

### Backup System
- Numbered backups: `chapter_1_backup_1.md`, `chapter_1_backup_2.md`, etc.
- Stored in `projects/{project_name}/backups/`
- Can restore any previous version

### Review System
- Reviews saved to `projects/{project_name}/reviews/chapter_N_review.md`
- Extracts actionable feedback
- Provides structured markdown reports

---

## 💡 Design Decisions

### Why Multi-Agent Architecture?
- **Specialization:** Each agent focuses on one task (writing, editing, reviewing)
- **Modularity:** Easy to swap or upgrade individual agents
- **Flexibility:** Can use different LLMs for different tasks
- **Maintainability:** Clear separation of concerns

### Why Modular Chapter Flow?
- **Testability:** Each manager can be tested independently
- **Reusability:** Backup and review logic can be used elsewhere
- **Clarity:** Easier to understand what each component does
- **Extensibility:** Easy to add new features (e.g., version control, collaboration)

### Why Support Multiple LLMs?
- **Cost Optimization:** Use cheaper models for simple tasks
- **Quality:** Use best model for each specific task
- **Availability:** Fallback if one provider is down
- **Experimentation:** Compare outputs from different models

---

## 🐛 Known Issues & Limitations

### Current Limitations
- No real-time collaboration
- No web UI (CLI only)
- Limited version control (basic backup system)
- No cloud sync
- Manual review process

### Technical Debt
- Some agents still need refactoring
- Test coverage needs improvement
- Documentation could be more comprehensive
- Error handling could be more robust

---

## 📝 Development Notes

### Testing
- Use `python -m py_compile` to verify syntax
- Test script: `test_refactor.py` for architecture verification
- Manual testing required for full workflows

### Code Style
- Use absolute imports: `from libriscribe.agents.chapter_flow import BackupManager`
- Type hints where possible
- Docstrings for all public methods
- Rich console for user-facing output
- Logging for debugging

### File Naming Conventions
- Agents: `{task}_agent.py` or `{task}.py`
- Managers: `{domain}_manager.py`
- Utils: `{purpose}_utils.py`
- Generated files: `chapter_{N}.md`, `chapter_{N}_revised.md`

---

## 🔗 Important Links

- **Documentation:** https://guerra2fernando.github.io/libriscribe/
- **GitHub:** https://github.com/guerra2fernando/libriscribe
- **Issues:** https://github.com/guerra2fernando/libriscribe/issues
- **Wiki:** https://github.com/guerra2fernando/libriscribe/wiki
- **Support:** https://buymeacoffee.com/guerra2fernando

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📊 Project Stats

- **License:** MIT
- **Python Version:** 3.8+
- **Active Development:** Yes
- **Community:** Growing
- **Status:** Beta

---

## 💭 Future Ideas & Considerations

### Potential Enhancements
- [ ] Git integration for version control
- [ ] Cloud storage sync (Google Drive, Dropbox)
- [ ] Collaborative editing
- [ ] Mobile app
- [ ] Voice-to-text integration
- [ ] Multi-language support
- [ ] Template library
- [ ] Publishing integrations (Amazon KDP, etc.)
- [ ] Analytics dashboard
- [ ] AI-powered plot analysis

### Community Requests
- Track feature requests in GitHub Issues
- Prioritize based on user feedback
- Consider sponsorship for premium features

---

## 📞 Contact & Support

- **Creator:** Fernando Guerra
- **Co-Creator:** Lenxys
- **Email:** Via GitHub Issues
- **Support:** Buy Me a Coffee

---

*This file serves as a living document and should be updated with each major change or milestone.*
