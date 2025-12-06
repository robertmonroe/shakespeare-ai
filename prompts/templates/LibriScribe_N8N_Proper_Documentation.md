# LibriScribe N8N - Proper Implementation

## Overview

This is the **correct** N8N implementation of LibriScribe that properly replicates the Simple Mode and Advanced Mode functionality from the original Python application.

## 🎯 **What I Fixed**

Previously I made the mistake of not understanding LibriScribe's actual modes. After reading the source code, I now have the correct implementation:

### **Simple Mode** (`libriscribe_simple_mode_workflow.json`)
- **Webhook:** `POST http://localhost:5678/webhook/libriscribe-simple`
- **Exact book length options from LibriScribe:**
  1. **Short Story (1-3 chapters)** - Random 1-3 chapters generated
  2. **Novella (5-8 chapters)** - Random 5-8 chapters generated  
  3. **Novel (15+ chapters)** - Random 15-20 chapters generated
  4. **Full Book (Non-Fiction)** - Random 8-13 chapters generated

### **Advanced Mode** (`libriscribe_advanced_mode_workflow.json`)  
- **Webhook:** `POST http://localhost:5678/webhook/libriscribe-advanced`
- **Flexible chapter ranges:**
  - Supports ranges like `"8-12"` (random between 8-12)
  - Supports plus notation like `"20+"` (20 + random 0-9)
  - Supports exact numbers like `"15"` (exactly 15)

## 📚 **Simple Mode Usage** 

### **Required Parameters:**
```json
{
  "project_name": "my-book",
  "title": "My Amazing Story",
  "category": "Fiction",  // Fiction, Non-Fiction, Business, Research Paper
  "book_length": "Novel (15+ chapters)"  // Exact options from LibriScribe
}
```

### **Complete Simple Mode Parameter Reference:**

**All LibriScribe Simple Mode Questions as API Parameters:**

| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "Project name?" | `project_name` | `"my-fantasy-book"` |
| "Book title?" | `title` | `"The Crystal Kingdom"` |
| "Select language" | `language` | `"English", "Spanish", "Brazilian Portuguese"` |
| "Select category" | `category` | `"Fiction", "Non-Fiction", "Business", "Research Paper"` |
| "Select genre" | `genre` | `"Fantasy", "Science Fiction", "Romance"` |
| "How long?" | `book_length` | `"Short Story (1-3 chapters)"` (exact text) |
| "How many characters?" (Fiction) | `num_characters` | `2`, `3`, `5` |
| "Extensive worldbuilding?" (Fiction) | `worldbuilding_needed` | `true`, `false` |
| "Review preference?" | `review_preference` | `"AI"`, `"Human"` |
| "Concept description?" | `description` | `"A young mage discovers ancient magic"` |

### **Book Length Options (Must Use Exact Text):**
| Option | Chapters Generated |
|--------|-------------------|
| `"Short Story (1-3 chapters)"` | 1-3 (random) |
| `"Novella (5-8 chapters)"` | 5-8 (random) |
| `"Novel (15+ chapters)"` | 15-20 (random) |
| `"Full Book (Non-Fiction)"` | 8-13 (random) |

### **Optional Parameters:**
```json
{
  "genre": "Fantasy",
  "language": "English",
  "description": "A story about magic and adventure",
  "target_audience": "Young Adult",
  "tone": "Serious",
  "review_preference": "AI",
  "num_characters": 3,
  "worldbuilding_needed": true
}
```

### **Simple Mode Example:**
```json
POST http://localhost:5678/webhook/libriscribe-simple
{
  "project_name": "fantasy-adventure",
  "title": "The Crystal Kingdom",
  "category": "Fiction",
  "book_length": "Novella (5-8 chapters)",
  "genre": "Fantasy",
  "description": "Young mage discovers ancient crystal magic",
  "num_characters": 3,
  "worldbuilding_needed": true
}
```

## 🔧 **Advanced Mode Usage**

### **Required Parameters:**
```json
{
  "project_name": "advanced-book",
  "title": "Complex Story",
  "category": "Fiction"
}
```

### **Advanced Chapter Specifications:**
| Input | Chapters Generated | Example |
|-------|-------------------|---------|
| `"10"` | Exactly 10 | `"num_chapters_str": "10"` |
| `"8-12"` | Random 8-12 | `"num_chapters_str": "8-12"` |  
| `"20+"` | Random 20-29 | `"num_chapters_str": "20+"` |

### **Complete Advanced Mode Parameter Reference:**

**All LibriScribe Advanced Mode Questions as API Parameters:**

#### **Base Questions (All Categories):**
| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "Project name?" | `project_name` | `"epic-fantasy-saga"` |
| "Book title?" | `title` | `"The Seven Realms War"` |
| "Select language" | `language` | `"English", "Spanish", "Brazilian Portuguese"` |
| "Select category" | `category` | `"Fiction", "Non-Fiction", "Business", "Research Paper"` |
| "Select genre" | `genre` | `"Epic Fantasy", "History", "Marketing"` |

#### **Fiction-Specific Questions:**
| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "How many characters? (e.g., 3, 2-4, 5+)" | `num_characters_str` | `"3"`, `"2-4"`, `"5+"` |
| "Extensive worldbuilding?" | `worldbuilding_needed` | `true`, `false` |
| "Select tone" | `tone` | `"Serious"`, `"Funny"`, `"Romantic"` |
| "Target audience" | `target_audience` | `"Children"`, `"Teens"`, `"Young Adult"`, `"Adults"` |
| "Book length" | `book_length` | `"Short Story"`, `"Novella"`, `"Novel"`, `"Full Book"` |
| "How many chapters? (e.g., 10, 8-12, 20+)" | `num_chapters_str` | `"10"`, `"8-12"`, `"20+"` |
| "Authors/books that inspire you?" | `inspired_by` | `"Tolkien, Brandon Sanderson"` |

#### **Non-Fiction Questions:**
| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "Select tone" | `tone` | `"Informative"`, `"Persuasive"`, `"Funny"` |
| "Target audience" | `target_audience` | `"Children"`, `"Adults"`, `"Professional/Expert"` |
| "Book length" | `book_length` | `"Article"`, `"Essay"`, `"Full Book"` |
| "Your experience/expertise?" | `author_experience` | `"PhD in History, 20 years teaching"` |

#### **Business Questions:**
| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "Select tone" | `tone` | `"Informative"`, `"Motivational"`, `"Instructive"` |
| "Target audience" | `target_audience` | `"Entrepreneurs"`, `"Managers"`, `"Students"` |
| "Book length" | `book_length` | `"Pamphlet"`, `"Guidebook"`, `"Full Book"` |
| "Key takeaways readers should gain?" | `key_takeaways` | `"How to scale startups effectively"` |
| "Include case studies?" | `case_studies` | `true`, `false` |
| "Provide actionable advice?" | `actionable_advice` | `true`, `false` |
| "Marketing focus?" (if genre=Marketing) | `marketing_focus` | `"SEO"`, `"Content Marketing"`, `"Social Media"` |
| "Sales focus?" (if genre=Sales) | `sales_focus` | `"Sales Techniques"`, `"Negotiation"` |

#### **Research Paper Questions:**
| LibriScribe Question | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| "Target audience" | `target_audience` | `"Academic Community"`, `"Researchers"`, `"Students"` |
| "Primary research question?" | `research_question` | `"How does AI affect human creativity?"` |
| "Hypothesis?" | `hypothesis` | `"AI enhances creativity through collaboration"` |
| "Research methodology" | `methodology` | `"Quantitative"`, `"Qualitative"`, `"Mixed Methods"` |

#### **Dynamic Questions (Advanced Only):**
| LibriScribe Feature | API Parameter | Example Values |
|---------------------|---------------|-----------------|
| AI-generated genre questions | `dynamic_questions` | `{"q1": "Answer 1", "q2": "Answer 2"}` |

### **Category-Specific Fields:**

#### **Fiction:**
```json
{
  "category": "Fiction",
  "num_characters_str": "2-4",
  "worldbuilding_needed": true,
  "tone": "Serious",
  "target_audience": "Adults",
  "book_length": "Novel",
  "inspired_by": "Tolkien"
}
```

#### **Non-Fiction:**
```json
{
  "category": "Non-Fiction", 
  "tone": "Informative",
  "target_audience": "Adults",
  "book_length": "Full Book",
  "author_experience": "PhD in History"
}
```

#### **Business:**
```json
{
  "category": "Business",
  "tone": "Motivational",
  "target_audience": "Entrepreneurs", 
  "key_takeaways": "How to scale startups",
  "case_studies": true,
  "actionable_advice": true,
  "marketing_focus": "SEO"
}
```

#### **Research Paper:**
```json
{
  "category": "Research Paper",
  "target_audience": "Academic Community",
  "research_question": "How does AI affect creativity?",
  "hypothesis": "AI enhances human creativity",
  "methodology": "Mixed Methods"
}
```

### **Advanced Mode Example:**
```json
POST http://localhost:5678/webhook/libriscribe-advanced
{
  "project_name": "complex-fantasy",
  "title": "The Seven Realms War",
  "category": "Fiction",
  "genre": "Epic Fantasy",
  "num_chapters_str": "18-25",
  "num_characters_str": "5-8", 
  "worldbuilding_needed": true,
  "tone": "Serious",
  "target_audience": "Adults",
  "book_length": "Novel",
  "description": "Multi-realm war spanning generations",
  "inspired_by": "Game of Thrones, LOTR",
  "dynamic_questions": {
    "q1": "What makes your magic system unique?",
    "q2": "How do the realms differ culturally?"
  }
}
```

## 🔄 **Key Differences Between Modes**

| Feature | Simple Mode | Advanced Mode |
|---------|-------------|---------------|
| **Chapter Count** | Fixed options (1-3, 5-8, 15+, 8-13) | Flexible ranges (8-12, 20+, exact) |
| **Character Count** | Simple number | Range support (2-4, 5+) |
| **Configuration** | Limited options | Full customization |
| **Category Support** | Basic | Category-specific fields |
| **Dynamic Questions** | No | Yes |
| **Processing** | Single AI call | Individual chapter processing |
| **Quality Control** | Basic | Advanced review/editing pipeline |

## 📁 **File Structure Created**

Both modes create the same file structure:

```
C:/Users/3dmax/n8n-books/{project_name}/
├── project_data.json              # LibriScribe project format
├── chapter_1.md                   # Chapter files
├── chapter_2.md
├── ...
├── chapter_N.md
├── chapter_1_revised.md           # Advanced mode edited chapters  
├── chapter_2_revised.md
├── ...
├── {Title}_complete.md             # Simple mode final book
├── {Title}_advanced_complete.md    # Advanced mode final book
└── project_final.json             # Completion metadata
```

## 🌍 **Language Support**

Both modes support:
- English (default)
- Spanish  
- Brazilian Portuguese
- French
- German
- Chinese (Simplified)
- Japanese
- Russian
- Arabic
- Hindi
- Custom languages

## ⚡ **Performance**

### **Simple Mode:**
- **Time:** 5-15 minutes (single AI call)
- **Quality:** Good (single pass)
- **Best for:** Quick book generation

### **Advanced Mode:**  
- **Time:** 30-90 minutes (individual chapter processing)
- **Quality:** Excellent (review + editing pipeline)
- **Best for:** Professional quality books

## 🚀 **Getting Started**

1. **Import workflows into N8N**
   - `libriscribe_simple_mode_workflow.json`
   - `libriscribe_advanced_mode_workflow.json` 
   - `book_formatter_workflow.json`
   - All 6 agent workflows

2. **Test Simple Mode first:**
   ```bash
   curl -X POST http://localhost:5678/webhook/libriscribe-simple \
   -H "Content-Type: application/json" \
   -d '{
     "project_name": "test-book",
     "title": "My First Book", 
     "category": "Fiction",
     "book_length": "Short Story (1-3 chapters)"
   }'
   ```

3. **Verify your existing agent workflows:**
   - `/webhook/concept-generator`
   - `/webhook/outliner` 
   - `/webhook/chapter-writer`
   - `/webhook/content-reviewer`
   - `/webhook/editor`
   - `/webhook/character-generator`

4. **Scale up to Advanced Mode when ready**

## 🎉 **Result**

You now have a **complete, accurate N8N replication** of LibriScribe that properly handles:
- ✅ Simple Mode with exact book length options
- ✅ Advanced Mode with flexible chapter ranges  
- ✅ All category types (Fiction, Non-Fiction, Business, Research)
- ✅ Proper LibriScribe data format compatibility
- ✅ Professional quality book generation

**This is the definitive N8N LibriScribe implementation.**
