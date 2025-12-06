# LibriScribe Architecture Documentation

**Version:** 2.0 (Post-Refactoring)  
**Last Updated:** 2025-11-22

---

## 🏗️ System Architecture Overview

LibriScribe uses a **multi-agent architecture** where specialized AI agents handle different aspects of book creation. The system is orchestrated by the `ProjectManagerAgent`, which delegates tasks to specialized agents.

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (CLI)                     │
│                      main.py (Typer)                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   ProjectManagerAgent                        │
│  • Orchestrates all agents                                   │
│  • Manages project lifecycle                                 │
│  • Handles data persistence                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│ Creative     │  │ Chapter Flow     │  │ Quality      │
│ Agents       │  │ Management       │  │ Assurance    │
└──────────────┘  └──────────────────┘  └──────────────┘
```

---

## 🎭 Agent System

### Core Agents

#### 1. **ProjectManagerAgent** (`project_manager.py`)
**Role:** Main orchestrator and coordinator

**Responsibilities:**
- Initialize and manage projects
- Coordinate all other agents
- Handle data persistence (save/load project data)
- Manage chapter flow delegation
- Format final manuscripts

**Key Methods:**
```python
initialize_llm_client(llm_provider: str)
initialize_project_with_data(project_data: ProjectKnowledgeBase)
save_project_data()
load_project_data(project_name: str)
write_and_review_chapter(chapter_number: int)
format_book(output_path: str)
```

---

### Creative Agents

#### 2. **ConceptGeneratorAgent** (`concept_generator.py`)
**Role:** Generate book concepts from user ideas

**Input:** Basic idea, genre, category  
**Output:** Detailed concept with themes, target audience, unique selling points

#### 3. **OutlinerAgent** (`outliner.py`)
**Role:** Create chapter-by-chapter outlines

**Input:** Book concept, desired chapter count  
**Output:** Structured outline with chapter summaries

#### 4. **CharacterGeneratorAgent** (`character_generator.py`)
**Role:** Develop character profiles

**Input:** Book concept, number of characters  
**Output:** Detailed character profiles (background, personality, motivations, arcs)

#### 5. **WorldbuildingAgent** (`worldbuilding.py`)
**Role:** Create rich world details

**Input:** Book concept, category (fiction/non-fiction/business/research)  
**Output:** Category-specific worldbuilding (geography, culture, history, etc.)

---

### Writing Agents

#### 6. **ChapterWriterAgent** (`chapter_writer.py`)
**Role:** Write chapter drafts

**Input:** Outline, characters, worldbuilding, chapter number  
**Output:** Complete chapter draft in markdown

#### 7. **EditorAgent** (`editor.py`)
**Role:** Refine and improve chapters

**Input:** Chapter content, review feedback  
**Output:** Revised chapter with improvements

**Key Features:**
- Preserves scene titles
- Applies review feedback
- Extracts and maintains structure

---

### Quality Assurance Agents

#### 8. **ContentReviewerAgent** (`content_reviewer.py`)
**Role:** Review chapters for quality issues

**Input:** Chapter text  
**Output:** Structured review with actionable feedback

**Checks:**
- Internal consistency
- Clarity
- Plot holes
- Redundancy
- Flow and transitions

#### 9. **StyleEditorAgent** (`style_editor.py`)
**Role:** Polish writing style

**Input:** Chapter content  
**Output:** Style-improved version

#### 10. **PlagiarismCheckerAgent** (`plagiarism_checker.py`)
**Role:** Detect potential plagiarism

#### 11. **FactCheckerAgent** (`fact_checker.py`)
**Role:** Verify factual claims (non-fiction)

---

## 🔄 Chapter Flow Management System

### Architecture

```
ChapterFlowManager
    ├── BackupManager
    │   ├── create_backup()
    │   ├── list_backups()
    │   ├── restore_backup()
    │   └── get_backup_count()
    │
    ├── ReviewManager
    │   ├── review_chapter()
    │   ├── _extract_actionable()
    │   └── load_review()
    │
    └── Workflow Methods
        ├── write_chapter()
        ├── review_chapter()
        ├── edit_chapter()
        ├── write_and_review_chapter_ai_mode()
        └── write_and_review_chapter_human_mode()
```

### BackupManager (`backup_manager.py`)

**Purpose:** Manage chapter backups and restoration

**Key Features:**
- Numbered backup system (`chapter_1_backup_1.md`, `chapter_1_backup_2.md`, etc.)
- List all backups for a chapter
- Restore any previous version
- Automatic backup directory creation

**Storage Location:** `projects/{project_name}/backups/`

**Methods:**
```python
create_backup(chapter_path: Path) -> str
list_backups(chapter_number: int) -> List[Path]
restore_backup(backup_path: Path, chapter_number: int) -> bool
get_backup_count(chapter_number: int) -> int
```

---

### ReviewManager (`review_manager.py`)

**Purpose:** Manage AI-powered chapter reviews

**Key Features:**
- Generate comprehensive reviews using LLM
- Extract actionable feedback
- Save reviews to dedicated directory
- Load previous reviews

**Storage Location:** `projects/{project_name}/reviews/`

**Methods:**
```python
review_chapter(chapter_number: int, chapter_text: str) -> Dict[str, Any]
_extract_actionable(review_md: str) -> str
load_review(chapter_number: int) -> Optional[str]
```

**Review Structure:**
```markdown
# Chapter Review

## Consistency Issues
- Issue 1
- Issue 2

## Clarity Problems
- Problem 1

## Plot Holes
- Hole 1

## Actionable Fixes
1. Fix X
2. Improve Y
3. Clarify Z
```

---

### ChapterFlowManager (`chapter_flow_manager.py`)

**Purpose:** Orchestrate the complete chapter workflow

**Modes:**

#### AI Mode (Interactive)
```
1. Write Chapter
2. Review Chapter
3. Interactive Loop:
   ┌─────────────────────────────────┐
   │ User Choice:                    │
   │ 1. Apply Fixes                  │
   │    → Create Backup              │
   │    → Edit Chapter               │
   │    → Review Again               │
   │                                 │
   │ 2. Restore Backup               │
   │    → Select Backup              │
   │    → Restore                    │
   │    → Review                     │
   │                                 │
   │ 3. Continue/Finish              │
   │    → Next Chapter or Done       │
   └─────────────────────────────────┘
```

#### Human Mode (Simple)
```
1. Write Chapter
2. Review Chapter
3. Continue to Next Chapter
```

**Methods:**
```python
write_chapter(chapter_number: int)
review_chapter(chapter_number: int) -> Dict[str, Any]
edit_chapter(chapter_number: int)
write_and_review_chapter_ai_mode(chapter_number: int) -> str
write_and_review_chapter_human_mode(chapter_number: int) -> str
write_and_review_chapter(chapter_number: int) -> str
```

---

## 💾 Data Models

### ProjectKnowledgeBase (`knowledge_base.py`)

**Purpose:** Central data structure for project information

**Key Fields:**
```python
project_name: str
title: str
genre: str
category: str  # fiction, non-fiction, business, research paper
language: str
description: str
num_chapters: int
review_preference: str  # "AI" or "Human"
worldbuilding_needed: bool

# Generated content
concept: Dict
outline: Dict
characters: List[Dict]
worldbuilding: Optional[Worldbuilding]

# Metadata
project_dir: Path
```

**Methods:**
```python
save_to_file(file_path: str)
load_from_file(file_path: str) -> ProjectKnowledgeBase
clean_worldbuilding_for_category()
```

---

### Worldbuilding Model

**Category-Specific Fields:**

**Fiction:**
- geography, culture_and_society, history, rules_and_laws
- technology_level, magic_system, key_locations
- important_organizations, flora_and_fauna, languages
- religions_and_beliefs, economy, conflicts

**Non-Fiction:**
- setting_context, key_figures, major_events
- underlying_causes, consequences, relevant_data
- different_perspectives, key_concepts

**Business:**
- industry_overview, target_audience, market_analysis
- business_model, marketing_and_sales_strategy
- operations, financial_projections, management_team
- legal_and_regulatory_environment, risks_and_challenges
- opportunities_for_growth

**Research Paper:**
- introduction, literature_review, methodology
- results, discussion, conclusion
- references, appendices

---

## 🔌 LLM Integration

### LLMClient (`utils/llm_client.py`)

**Purpose:** Unified interface for multiple LLM providers

**Supported Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude (Claude 3 family)
- Google Gemini
- DeepSeek
- Mistral AI

**Key Methods:**
```python
generate_text(prompt: str, max_tokens: int) -> str
generate_content(prompt: str, max_tokens: int) -> str
```

**Configuration:**
- API keys stored in `.env` file
- Provider selected at initialization
- Automatic retry logic
- Error handling

---

## 📁 File System Organization

### Project Directory Structure
```
projects/
└── {project_name}/
    ├── project_data.json          # Project metadata
    ├── outline.md                 # Book outline
    ├── characters.json            # Character profiles
    ├── world.json                 # Worldbuilding
    ├── chapter_1.md               # Original chapters
    ├── chapter_2.md
    ├── chapter_1_revised.md       # Edited chapters
    ├── chapter_2_revised.md
    ├── backups/                   # Chapter backups
    │   ├── chapter_1_backup_1.md
    │   ├── chapter_1_backup_2.md
    │   └── chapter_2_backup_1.md
    ├── reviews/                   # Chapter reviews
    │   ├── chapter_1_review.md
    │   └── chapter_2_review.md
    └── research_results.md        # Research findings
```

---

## 🔄 Data Flow

### Chapter Creation Flow

```
User Request
    ↓
ProjectManager.write_and_review_chapter(N)
    ↓
ChapterFlowManager.write_and_review_chapter(N)
    ↓
┌─────────────────────────────────────┐
│ Check review_preference             │
│ • AI Mode → Interactive Loop        │
│ • Human Mode → Simple Flow          │
└─────────────────────────────────────┘
    ↓
Write Chapter
    ↓
ChapterWriterAgent.execute()
    ↓
Review Chapter
    ↓
ReviewManager.review_chapter()
    ↓
ContentReviewerAgent.execute()
    ↓
[AI Mode Only] Interactive Loop
    ↓
User Choice → Edit/Backup/Continue
    ↓
Save & Continue
```

---

## 🧪 Testing Strategy

### Unit Tests
- Test individual agents in isolation
- Mock LLM responses
- Test data models

### Integration Tests
- Test agent interactions
- Test workflow completion
- Test file operations

### Manual Testing
- Full book creation workflow
- Edge cases (empty chapters, errors)
- Different LLM providers

---

## 🔒 Security Considerations

### API Key Management
- Store in `.env` file (not committed)
- Use environment variables
- Never log API keys

### File System
- Validate file paths
- Sanitize user input
- Prevent directory traversal

### LLM Safety
- Implement rate limiting
- Monitor costs
- Validate LLM outputs

---

## 📊 Performance Considerations

### Optimization Strategies
- Cache LLM responses where appropriate
- Batch operations when possible
- Lazy load large files
- Stream long outputs

### Scalability
- Modular design allows horizontal scaling
- Each agent can run independently
- Future: Async/parallel agent execution

---

## 🔮 Future Architecture Plans

### Planned Enhancements
1. **Event-Driven Architecture**
   - Implement event bus
   - Decouple agents further
   - Enable real-time updates

2. **Microservices**
   - Split agents into services
   - RESTful API
   - GraphQL interface

3. **Database Integration**
   - Replace JSON with database
   - Vector store for semantic search
   - Proper versioning

4. **Caching Layer**
   - Redis for session data
   - LLM response caching
   - Reduce API costs

5. **Queue System**
   - Background job processing
   - Long-running tasks
   - Better error recovery

---

## 📝 Design Patterns Used

### Patterns
- **Strategy Pattern:** LLMClient supports multiple providers
- **Template Method:** Agent base class defines workflow
- **Facade Pattern:** ProjectManager simplifies complex operations
- **Repository Pattern:** File-based data persistence
- **Manager Pattern:** Specialized managers for backups and reviews

---

## 🤝 Contributing to Architecture

### Guidelines
1. Maintain separation of concerns
2. Use absolute imports
3. Add type hints
4. Document public APIs
5. Write tests for new components
6. Follow existing patterns

### Adding New Agents
1. Inherit from `Agent` base class
2. Implement `execute()` method
3. Register in `ProjectManagerAgent`
4. Add to documentation

---

*This architecture documentation should be updated with each significant change to the system design.*
