# LibriScribe N8N - Complete Book Creation System

## Overview

This is a complete N8N-based book creation system that replicates the LibriScribe Python application functionality. The system uses modular workflows that work together to create full-length books automatically.

## System Architecture

### 🧠 Core Component: **Orchestrator Workflow**
- **File:** `libriscribe_orchestrator_workflow.json`
- **Webhook:** `http://localhost:5678/webhook/libriscribe-orchestrator` 
- **Function:** Main coordinator that manages the entire book creation process
- **Flow:** Project Setup → Concept → Outline → Chapters → Review → Edit → Format → Complete

### 📚 Individual AI Agent Workflows (13 Total)

#### ✅ **Already Created (6 workflows):**
1. **Scene Generator** - `scene_generator_workflow.json`
2. **Scene Outliner** - `scene_outliner_workflow.json`  
3. **Fact Checker** - `fact_checker_workflow.json`
4. **Researcher** - `researcher_workflow.json`
5. **Worldbuilding** - `worldbuilding_workflow.json`
6. **Plagiarism Checker** - `plagiarism_checker_workflow.json`

#### 🔧 **Need from Your Existing N8N (7 workflows):**
7. **Concept Generator** - Webhook: `/webhook/concept-generator`
8. **Character Generator** - Webhook: `/webhook/character-generator`
9. **Outliner** - Webhook: `/webhook/outliner`
10. **Chapter Writer** - Webhook: `/webhook/chapter-writer`
11. **Content Reviewer** - Webhook: `/webhook/content-reviewer`
12. **Style Editor** - Webhook: `/webhook/style-editor`
13. **Editor** - Webhook: `/webhook/editor`

### 🎨 **Formatting System:**
- **Book Formatter** - `book_formatter_workflow.json`
- **Webhook:** `http://localhost:5678/webhook/book-formatter`
- **Function:** Assembles all chapters into final book with title page and table of contents

## Complete Installation Steps

### 1. Import All Workflow Files
Import these JSON files through N8N UI (+ → Import from File):

```
- libriscribe_orchestrator_workflow.json (Main coordinator)
- book_formatter_workflow.json (Book assembly)
- scene_generator_workflow.json (Scene writing)
- scene_outliner_workflow.json (Scene planning)
- fact_checker_workflow.json (Fact verification)
- researcher_workflow.json (Research tool)
- worldbuilding_workflow.json (World creation)
- plagiarism_checker_workflow.json (Content checking)
```

### 2. Verify Existing Agent Webhooks
Ensure these webhook paths exist in your N8N:
- `/webhook/concept-generator`
- `/webhook/character-generator`
- `/webhook/outliner`
- `/webhook/chapter-writer`
- `/webhook/content-reviewer`
- `/webhook/style-editor`
- `/webhook/editor`

### 3. Test Individual Agents
Test each agent workflow individually before using the orchestrator.

## How to Use the System

### Method 1: Complete Book Creation (Recommended)

**Endpoint:** `POST http://localhost:5678/webhook/libriscribe-orchestrator`

**Payload:**
```json
{
  "project_name": "my-sci-fi-book",
  "title": "Journey to Alpha Centauri",
  "genre": "Science Fiction",
  "language": "English",
  "num_chapters": 15,
  "user_input": "A story about space exploration and first contact with aliens",
  "category": "fiction",
  "worldbuilding_needed": true,
  "review_preference": "AI"
}
```

**What Happens:**
1. Creates project directory: `C:/Users/3dmax/n8n-books/my-sci-fi-book/`
2. Generates concept using AI
3. Creates detailed outline with specified number of chapters
4. Writes all chapters
5. Reviews each chapter for content issues
6. Automatically edits chapters (if review_preference = "AI")
7. Formats complete book with title page and table of contents
8. Saves final book as: `Journey_to_Alpha_Centauri_complete.md`

**Response:**
```json
{
  "status": "success",
  "message": "Book creation completed successfully!",
  "project_name": "my-sci-fi-book",
  "title": "Journey to Alpha Centauri",
  "chapters_completed": 15,
  "book_file": "C:/Users/3dmax/n8n-books/my-sci-fi-book/Journey_to_Alpha_Centauri_complete.md",
  "word_count": 45000,
  "completed_at": "2024-11-20T18:30:00.000Z"
}
```

### Method 2: Individual Agent Usage

You can call any agent individually:

**Scene Generator:**
```json
POST http://localhost:5678/webhook/scene-generator-webhook
{
  "scene_number": 1,
  "chapter_number": 3,
  "book_title": "My Book",
  "scene_outline": "The protagonist discovers the alien artifact",
  "scene_purpose": "Introduce the main conflict",
  "scene_characters": "Sarah (protagonist), Dr. Martinez (mentor)",
  "scene_setting": "Underground laboratory",
  "language": "English"
}
```

**Fact Checker:**
```json
POST http://localhost:5678/webhook/fact-checker-webhook
{
  "genre": "Historical Fiction",
  "content_to_check": "Napoleon was defeated at Waterloo in 1815 by the British forces",
  "language": "English"
}
```

## File Structure Created

```
C:/Users/3dmax/n8n-books/
└── {project_name}/
    ├── project_data.json          # Project configuration
    ├── chapter_1.md               # Original chapters
    ├── chapter_2.md
    ├── ...
    ├── chapter_1_edited.md        # AI-edited chapters
    ├── chapter_2_edited.md
    ├── ...
    ├── project_final.json         # Final completion data
    └── {Title}_complete.md         # Final formatted book
```

## System Features

### ✅ **Complete Automation**
- One API call creates entire book
- Handles 15+ chapters automatically
- Saves all files with proper organization

### ✅ **Quality Control**
- Content review for each chapter
- Automatic editing if review_preference = "AI"
- Fact checking and plagiarism detection available

### ✅ **Modular Design**
- Use individual agents as needed
- Combine agents in custom workflows
- Each agent is independent and reusable

### ✅ **Multi-language Support**
- English and Brazilian Portuguese built-in
- Easy to add more languages

### ✅ **Professional Output**
- Formatted with title page
- Automatic table of contents
- Word count and statistics
- Ready for publishing

## Configuration Options

### Required Parameters:
- `project_name` - Unique identifier for the project
- `title` - Book title
- `genre` - Book genre (affects AI prompts)

### Optional Parameters:
- `language` - "English" (default) or "Brazilian Portuguese"
- `num_chapters` - Number of chapters (you can set ANY number: 1, 5, 10, 20, 50, etc. Default: 15)
- `user_input` - Additional story guidance
- `category` - "fiction" (default), "non-fiction", "business"
- `worldbuilding_needed` - true/false for fantasy/sci-fi
- `review_preference` - "AI" (auto-edit) or "Human" (manual review)

## Performance Notes

### Estimated Processing Time:
- **Setup & Concept:** ~30 seconds
- **Outline Generation:** ~1 minute  
- **Chapter Writing:** ~2-3 minutes per chapter
- **Review & Editing:** ~1 minute per chapter
- **Book Formatting:** ~30 seconds

**Total for 15-chapter book:** ~45-75 minutes

### Output Quality:
- **Word Count:** ~40,000-60,000 words (typical novel length)
- **Chapter Length:** ~2,500-4,000 words per chapter
- **Consistency:** High (AI maintains style and continuity)

## Troubleshooting

### Common Issues:

**"Workflow not found" errors:**
- Ensure all agent workflows are imported and active
- Check webhook paths match exactly

**"Directory creation failed":**
- Ensure N8N has write permissions to `C:/Users/3dmax/n8n-books/`
- Check disk space availability

**"Timeout" errors:**
- Large books may take time - consider reducing chapters
- Check OpenRouter/Claude API limits

**"Missing content" in chapters:**
- Verify Chapter Writer workflow is properly configured
- Check Claude API key is valid in OpenRouter credentials

## Next Steps

1. **Import all workflow JSON files**
2. **Test with a simple 3-chapter book first**
3. **Verify your existing 7 agent workflows**
4. **Run complete book creation**
5. **Customize prompts as needed**

## API Integration Examples

### Python Integration:
```python
import requests

response = requests.post(
    'http://localhost:5678/webhook/libriscribe-orchestrator',
    json={
        'project_name': 'test-book',
        'title': 'My First AI Book',
        'genre': 'Fantasy',
        'num_chapters': 5,
        'user_input': 'A young wizard discovers ancient magic'
    }
)

print(response.json())
```

### JavaScript/Node.js Integration:
```javascript
const response = await fetch('http://localhost:5678/webhook/libriscribe-orchestrator', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    project_name: 'test-book',
    title: 'My First AI Book',
    genre: 'Fantasy',
    num_chapters: 5,
    user_input: 'A young wizard discovers ancient magic'
  })
});

const result = await response.json();
console.log(result);
```

---

🎉 **Your complete N8N LibriScribe system is ready!** 

This replaces the Python application entirely and runs everything through N8N workflows.
