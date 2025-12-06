# N8N Novel Generator - Setup Guide

## Step 1: Add OpenRouter Credentials to N8N

1. Open N8N at `http://localhost:5678`
2. Click your profile icon (top right) → **Settings**
3. Go to **Credentials** → **Add Credential**
4. Search for "**HTTP Header Auth**"
5. Fill in:
   - **Name**: `OpenRouter API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_OPENROUTER_API_KEY`
   - Replace `YOUR_OPENROUTER_API_KEY` with your actual key
6. Click **Save**

## Step 2: Import the Workflow

1. In N8N, click **Workflows** (left sidebar)
2. Click **Add Workflow** → **Import from File**
3. Select: `C:\Users\3dmax\Libriscribe\n8n_workflows\chapter_generator.json`
4. The workflow will load with 5 nodes:
   - Manual Trigger
   - Chapter Input
   - Call OpenRouter (Claude)
   - Extract Chapter Text
   - Save Chapter to File

## Step 3: Connect Your Credentials

1. Click on the **"Call OpenRouter (Claude)"** node
2. Under **Credentials**, select **OpenRouter API** (the one you just created)
3. Click **Save** on the node

## Step 4: Test the Workflow

1. Click the **"Chapter Input"** node
2. Modify the values if you want:
   - `book_title`: Your novel title
   - `genre`: Spy Thriller, Mystery, Romance, etc.
   - `chapter_number`: 1, 2, 3...
   - `chapter_title`: Chapter title
   - `chapter_summary`: What happens in this chapter
3. Click **Execute Workflow** (top right)
4. Watch it run! It will:
   - Send your prompt to Claude via OpenRouter
   - Extract the generated chapter
   - Save to: `C:\Users\3dmax\Libriscribe\The_Moscow_Protocol\chapter_1.md`

## Step 5: Customize for Your Novels

### Change the Save Location
Edit the **"Save Chapter to File"** node:
- Current: Saves to Libriscribe folder
- Change `fileName` to your preferred path, e.g.:
  ```
  C:/Users/3dmax/Novels/{{ $json.book_title }}/chapter_{{ $json.chapter_number }}.md
  ```

### Adjust Claude Settings
Edit the **"Call OpenRouter (Claude)"** node:
- **Model**: Change `anthropic/claude-3.5-sonnet` to other models:
  - `anthropic/claude-3-opus` (more creative)
  - `anthropic/claude-3-haiku` (faster, cheaper)
  - `openai/gpt-4-turbo` (alternative)
- **Temperature**: 0.7 (balanced), 0.9 (creative), 0.3 (focused)
- **Max Tokens**: 8000 (current), increase for longer chapters

### Generate Multiple Chapters
To generate all 20 chapters:
1. Add a **"Loop Over Items"** node before Chapter Input
2. Feed it a list of chapter numbers (1-20)
3. Add chapter summaries for each
4. The workflow will run 20 times automatically

## What This Workflow Does

```
[Manual Trigger] 
    ↓
[Chapter Input] ← You set: title, genre, chapter #, summary
    ↓
[Call OpenRouter] ← Sends prompt to Claude via OpenRouter API
    ↓
[Extract Text] ← Pulls the chapter content from API response
    ↓
[Save to File] ← Writes chapter_X.md to your folder
```

## Next Steps

Once this works, we can build:
- **Outline Generator** workflow (creates 20-chapter outline)
- **Review Agent** workflow (checks for plot holes, inconsistencies)
- **Edit Agent** workflow (fixes issues found by reviewer)
- **Full Novel Pipeline** (outline → generate → review → edit → compile)

## Troubleshooting

**Error: "Unauthorized"**
- Check your OpenRouter API key is correct
- Make sure you added "Bearer " before the key

**Error: "File not found"**
- Create the folder first: `mkdir C:\Users\3dmax\Novels`
- Or change the save path in the workflow

**Chapter is too short**
- Increase `max_tokens` to 12000 or 16000
- Adjust the prompt to request more words

**Want to use Anthropic directly instead of OpenRouter?**
- Change URL to: `https://api.anthropic.com/v1/messages`
- Change headers to use `x-api-key` instead of `Authorization`
- Adjust the request body format (Anthropic uses different structure)

---

Ready to test? Import the workflow and let me know if you hit any issues!
