# LibriScribe N8N Workflows - Import Instructions

## Summary
I've successfully created the 6 missing LibriScribe agents for your N8N installation:

### ✅ Created Workflow Files:
1. `scene_generator_workflow.json` - Scene Generator
2. `scene_outliner_workflow.json` - Scene Outliner  
3. `fact_checker_workflow.json` - Fact Checker
4. `researcher_workflow.json` - Researcher
5. `worldbuilding_workflow.json` - Worldbuilding
6. `plagiarism_checker_workflow.json` - Plagiarism Checker

### 📋 Current Status:
- **Existing workflows:** 8/13 (already in N8N)
- **New workflows:** 6/13 (JSON files ready to import)
- **Total when complete:** 13/13 LibriScribe agents

## How to Import these Workflows

### Method 1: Import via N8N UI (Recommended)
1. Open your N8N instance at http://localhost:5678
2. Login with your credentials
3. For each JSON file:
   - Click "+" to create a new workflow
   - Click the "⚙️" menu in the top right
   - Select "Import from file"
   - Choose the JSON file
   - Click "Import"
   - Save the workflow

### Method 2: Copy/Paste Import
1. Open N8N and create a new workflow
2. Open one of the JSON files in a text editor
3. Copy the entire contents
4. In N8N, click the "⚙️" menu → "Import from clipboard"
5. Paste the JSON content
6. Click "Import"

## Workflow Structure
Each workflow follows the same pattern as your existing ones:
- **Webhook** (POST trigger with unique path)
- **AI Agent** (with LibriScribe system prompts from YAML templates)
- **OpenRouter Chat Model** (Claude Sonnet 4.5)
- **Credentials** (uses your existing OpenRouter account)

## Expected Input Parameters

### Scene Generator
- `scene_number`, `chapter_number`, `book_title`
- `scene_outline`, `scene_purpose`, `scene_characters`
- `scene_setting`, `language`

### Scene Outliner
- `chapter_number`, `genre`, `chapter_context`
- `chapter_summary`, `language`

### Fact Checker
- `genre`, `content_to_check`, `language`

### Researcher
- `genre`, `query`, `project_context`, `language`

### Worldbuilding
- `category`, `genre`, `project_context`
- `worldbuilding_aspects`, `language`

### Plagiarism Checker
- `genre`, `content_to_analyze`, `language`

## Next Steps
1. Import all 6 workflows using the instructions above
2. Test each workflow with sample data
3. Activate the workflows you want to use
4. Your complete LibriScribe system will be ready!

## Notes
- All workflows use your existing OpenRouter credentials
- Each has a unique webhook path for API calls
- System prompts are based on your LibriScribe YAML templates
- All workflows are set to inactive by default after import
