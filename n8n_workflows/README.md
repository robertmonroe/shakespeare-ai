# Libriscribe N8N Workflows - Complete Guide

## Overview

This folder contains N8N workflows that replicate the entire Libriscribe novel generation system using Claude 3.5 Sonnet via OpenRouter.

---

## Workflow Files

### 01 - Outline Generator
**File:** `01_outline_generator.json`

**Purpose:** Generate a complete 20-chapter outline from a book concept

**Inputs:**
- Book title
- Genre
- Concept/premise
- Target chapter count
- Language

**Outputs:**
- `{book_title}/outline.md` - Complete chapter-by-chapter outline

**Usage:**
1. Import into N8N
2. Configure OpenRouter credential
3. Edit "Book Input Parameters" node with your book details
4. Execute workflow
5. Review generated outline in output folder

---

### 02 - Single Chapter Generator
**File:** `02_single_chapter_generator.json`

**Purpose:** Generate a single chapter with full control

**Inputs:**
- Book title
- Genre
- Chapter number
- Chapter title
- Chapter summary
- Language
- Target word count

**Outputs:**
- `{book_title}/chapter_{number}.md` - Complete chapter with word count

**Usage:**
1. Import into N8N
2. Configure OpenRouter credential
3. Edit "Chapter Input Parameters" with chapter details
4. Execute workflow
5. Chapter saved automatically

**Features:**
- Word count tracking
- Professional formatting
- Customizable length (default: 3500 words)

---

### 03 - Batch Chapter Generator
**File:** `03_batch_chapter_generator.json`

**Purpose:** Generate ALL chapters automatically from outline

**Inputs:**
- Book title (must match outline filename)
- Genre
- Start chapter (default: 1)
- End chapter (default: 20)
- Language

**Requirements:**
- Must have outline file from Workflow 01

**Outputs:**
- `{book_title}/chapter_1.md` through `chapter_20.md`

**Usage:**
1. Run Workflow 01 first to generate outline
2. Import Workflow 03 into N8N
3. Configure OpenRouter credential
4. Edit "Batch Input Parameters"
5. Execute workflow
6. Wait ~2-3 hours for all 20 chapters (5 sec delay between chapters)

**Features:**
- Automatic outline parsing
- Rate limiting (5 second delay between chapters)
- Generates 3000-4000 words per chapter
- Saves each chapter automatically

**Cost Estimate:**
- ~$2-5 for complete 20-chapter novel (60k-80k words)

---

### 04 - Content Reviewer
**File:** `04_content_reviewer.json`

**Purpose:** Review chapters for plot holes, character issues, and writing quality

**Inputs:**
- Book title
- Chapter number
- Genre

**Outputs:**
- `{book_title}/reviews/chapter_{number}_review.md` - Detailed review

**Review Categories:**
1. **Critical Issues** - Must fix (plot holes, major errors)
2. **Moderate Issues** - Should fix (pacing, character development)
3. **Minor Suggestions** - Optional improvements
4. **Strengths** - What works well

**Usage:**
1. Generate chapter first (Workflow 02 or 03)
2. Import Workflow 04
3. Configure OpenRouter credential
4. Set chapter number to review
5. Execute workflow
6. Review feedback in reviews folder

---

## Setup Instructions

### Prerequisites
1. **N8N installed and running** (http://localhost:5678)
2. **OpenRouter API key** (get from https://openrouter.ai/)
3. **OpenRouter credits** (~$5 recommended for testing)

### Initial Setup

#### Step 1: Create OpenRouter Credential
1. In N8N, go to **Credentials** (sidebar)
2. Click **Add Credential**
3. Search for **"Header Auth"**
4. Configure:
   - **Name:** `OpenRouter API`
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer YOUR_OPENROUTER_API_KEY`
5. Click **Save**

#### Step 2: Import Workflows
1. In N8N, click **Workflows** → **Import from File**
2. Import each workflow JSON file
3. For each workflow:
   - Open the HTTP Request node
   - Select your "OpenRouter API" credential
   - Save the workflow

#### Step 3: Test Setup
1. Open **Workflow 01 - Outline Generator**
2. Click **Execute Workflow**
3. Check output folder for `outline.md`
4. If successful, you're ready!

---

## Complete Novel Generation Workflow

### Phase 1: Generate Outline
1. Run **Workflow 01** with your book concept
2. Review the generated outline
3. Edit if needed (manually adjust chapter summaries)

### Phase 2: Generate All Chapters
1. Run **Workflow 03** (Batch Chapter Generator)
2. Wait 2-3 hours for completion
3. You'll have 20 complete chapters (60k-80k words)

### Phase 3: Review & Edit (Optional)
1. Run **Workflow 04** on each chapter
2. Review feedback
3. Manually edit chapters or create an editor workflow

### Phase 4: Compile Book (Manual for now)
1. Concatenate all chapters
2. Add title page
3. Export to PDF/EPUB using Calibre or similar

---

## Customization Guide

### Change Model
In any HTTP Request node, change:
```json
"model": "anthropic/claude-3.5-sonnet"
```

**Alternative models:**
- `anthropic/claude-3-opus` - More creative, slower
- `anthropic/claude-3-haiku` - Faster, cheaper
- `openai/gpt-4-turbo` - GPT-4 alternative

### Adjust Word Count
In Chapter Generator nodes, change:
```json
"target_words": "3500"
```

Or modify the prompt:
```
"Target word count: 5000 words"
```

### Change Temperature
Higher = more creative, Lower = more focused

```json
"temperature": 0.7  // Default
"temperature": 0.9  // More creative
"temperature": 0.5  // More consistent
```

### Modify Genre Prompts
Edit the prompt in HTTP Request nodes to match your genre:
- Replace "Spy Thriller" with "Romance", "Fantasy", etc.
- Adjust writing requirements
- Change tone and style instructions

---

## Troubleshooting

### Error: "Unauthorized" (401)
- Check OpenRouter API key is correct
- Verify "Bearer " prefix in credential
- Check credits at https://openrouter.ai/credits

### Error: "Model not found"
- Verify model name: `anthropic/claude-3.5-sonnet`
- Check available models at https://openrouter.ai/models

### Chapters are too short
- Increase `max_tokens` (try 16000)
- Add "Write at least 4000 words" to prompt
- Lower temperature to 0.6

### Outline parsing fails (Workflow 03)
- Check outline format matches expected pattern
- Ensure outline has "Chapter X: Title\nSummary: ..." format
- Manually verify outline.md file

### Rate limit errors
- Increase wait time in Workflow 03 (change 5000ms to 10000ms)
- Upgrade OpenRouter plan
- Run fewer chapters at once

---

## Cost Breakdown

**Per Chapter (3500 words):**
- Input: ~500 tokens (prompt)
- Output: ~5000 tokens (chapter)
- Cost: ~$0.10-0.25 per chapter

**Full Novel (20 chapters):**
- Total: ~$2-5 for complete book
- Outline: ~$0.50
- Reviews: ~$0.50 per chapter reviewed

**Comparison:**
- Libriscribe Python: Same cost (uses same API)
- Direct Anthropic API: Slightly more expensive
- Human ghostwriter: $5,000-50,000

---

## Advanced Features (Coming Soon)

### Planned Workflows:
- **05 - Editor Agent** - Auto-fix issues from reviews
- **06 - Book Compiler** - Combine chapters into final book
- **07 - Character Consistency Checker** - Track character details
- **08 - World Building Manager** - Maintain setting details

---

## Comparison: N8N vs Libriscribe Python

| Feature | N8N Workflows | Libriscribe Python |
|---------|--------------|-------------------|
| **Setup** | Visual, no coding | Command-line |
| **Flexibility** | Drag-and-drop editing | Code editing |
| **Monitoring** | Built-in execution logs | Terminal output |
| **Scheduling** | Built-in cron triggers | External scheduler needed |
| **Cost** | Same (OpenRouter) | Same (OpenRouter) |
| **Speed** | Same | Same |
| **Learning Curve** | Easier (visual) | Harder (Python) |
| **Customization** | Limited to nodes | Unlimited (code) |

**Recommendation:**
- Use **N8N** for quick setup and visual workflow management
- Use **Libriscribe Python** for advanced customization and integration

---

## Support & Resources

- **OpenRouter Docs:** https://openrouter.ai/docs
- **N8N Community:** https://community.n8n.io/
- **Claude API Docs:** https://docs.anthropic.com/
- **Libriscribe GitHub:** https://github.com/guerra2fernando/libriscribe

---

## Quick Start Checklist

- [ ] N8N installed and running
- [ ] OpenRouter API key obtained
- [ ] OpenRouter credential created in N8N
- [ ] Workflow 01 imported and tested
- [ ] Workflow 02 imported and tested
- [ ] Workflow 03 imported (for batch generation)
- [ ] Workflow 04 imported (for reviews)
- [ ] Output folder created
- [ ] First outline generated
- [ ] First chapter generated
- [ ] Ready to generate full novel!

---

**You're now ready to generate professional-quality novels using N8N and Claude 3.5 Sonnet!** 🚀📚
