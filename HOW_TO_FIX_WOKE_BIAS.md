# How to Fix "Woke" Bias in LibriScribe Stories

**Problem:** Claude Sonnet 4 (and other modern LLMs) tend to inject social justice themes, oppression narratives, and political commentary into stories even when you just want a straightforward adventure tale.

**Example:** You ask for "a chimp walks on the moon" and get "a chimp rebels against abusive handlers" instead.

---

## 🎯 Why This Happens

### Claude Sonnet 4 Specifics:
- **Most heavily RLHF-tuned model** for "safety" and "inclusivity"
- Trained to prioritize "diverse perspectives" and "social awareness"
- Interprets conflict as social/political rather than adventure/technical
- Default assumption: stories need "meaningful messages" about oppression/justice

### General LLM Issues:
1. **Training data from 2010s-2020s** - heavy social justice content
2. **Conflict = Drama** - models think drama requires social issues
3. **"Helpful" AI** - tries to add "depth" by injecting contemporary themes

---

## 🛠️ Solutions (Ranked by Effectiveness)

### ⭐ Solution 1: Modify the Core Prompts (MOST EFFECTIVE)

LibriScribe uses prompts stored in `src/libriscribe/utils/prompts_context.py`. You need to add **tone override instructions** to the key prompts.

#### Files to Modify:
- **Primary:** `src/libriscribe/utils/prompts_context.py`
- **Secondary:** `prompts/templates/*.yml` (less important, mainly for N8N workflows)

#### What to Add:

Add this **TONE DIRECTIVE** section to the beginning of these prompts:

1. **SCENE_OUTLINE_PROMPT** (line 156)
2. **OUTLINE_PROMPT** (line 193)
3. **CHARACTER_PROMPT** (line 237)
4. **SCENE_PROMPT** (line 414)

**Example Addition:**

```python
SCENE_OUTLINE_PROMPT = """
=== CRITICAL TONE DIRECTIVE ===
This is a CLASSIC ADVENTURE story in the spirit of Jules Verne, Arthur C. Clarke, and Golden Age science fiction.

REQUIRED TONE:
- Optimistic and celebratory
- Focus on achievement, discovery, exploration, and wonder
- Conflicts should be EXTERNAL: technical challenges, nature, physics, exploration obstacles
- Characters should be competent, cooperative, and driven by curiosity/ambition

ABSOLUTELY FORBIDDEN THEMES:
- Social oppression or victimization narratives
- Rebellion against authority or "the system"
- Political or social commentary
- Abuse, mistreatment, or exploitation storylines
- "Message-driven" storytelling about contemporary issues
- Characters defined by suffering or marginalization

INSTEAD FOCUS ON:
- Scientific/technical problem-solving
- Teamwork and camaraderie
- Overcoming natural obstacles
- The thrill of discovery
- Human ingenuity and determination
- Positive relationships and mentorship

Think: Apollo 13, The Martian, Star Trek (original series), not contemporary social drama.
=== END TONE DIRECTIVE ===

Create a detailed outline for the scenes in a {genre} book titled "{title}" which is categorized as {category}.
[rest of existing prompt...]
"""
```

#### Specific Line Numbers to Edit:

**In `src/libriscribe/utils/prompts_context.py`:**

| Prompt Variable | Line Number | Purpose |
|----------------|-------------|---------|
| `SCENE_OUTLINE_PROMPT` | 156 | Controls scene structure |
| `OUTLINE_PROMPT` | 193 | Controls overall story arc |
| `CHARACTER_PROMPT` | 237 | Controls character creation |
| `SCENE_PROMPT` | 414 | Controls actual scene writing |

**How to Edit:**
1. Open `src/libriscribe/utils/prompts_context.py`
2. Find each prompt (use line numbers above)
3. Add the TONE DIRECTIVE section right after the opening `"""`
4. Save the file
5. Clear Python cache: `Get-ChildItem -Path "src" -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force`
6. Restart LibriScribe

---

### ⭐ Solution 2: Add Story Style Preference to Project Setup

Create a new field in project initialization that lets you choose story style.

#### Implementation:

**Step 1:** Add to `src/libriscribe/knowledge_base.py` (ProjectKnowledgeBase class):

```python
story_style: str = "classic_adventure"  # Options: classic_adventure, contemporary_drama, neutral
```

**Step 2:** Add to `src/libriscribe/main.py` in the project setup functions:

```python
def get_story_style(project_knowledge_base: ProjectKnowledgeBase):
    console.print("")
    story_style = select_from_list(
        "📖 What storytelling style do you prefer?",
        [
            "Classic Adventure (optimistic, exploration-focused)",
            "Contemporary Drama (social themes, character struggles)", 
            "Neutral (let AI decide)"
        ]
    )
    
    # Map to internal values
    style_map = {
        "Classic Adventure (optimistic, exploration-focused)": "classic_adventure",
        "Contemporary Drama (social themes, character struggles)": "contemporary_drama",
        "Neutral (let AI decide)": "neutral"
    }
    
    project_knowledge_base.set("story_style", style_map.get(story_style, "neutral"))
```

**Step 3:** Modify prompts to use this field:

```python
# In prompts_context.py, add this helper function:
def get_tone_directive(story_style: str) -> str:
    if story_style == "classic_adventure":
        return """
=== CRITICAL TONE DIRECTIVE ===
Classic adventure style: Focus on achievement, discovery, technical challenges.
FORBIDDEN: Social oppression, rebellion, political themes, victimhood narratives.
REQUIRED: Optimism, cooperation, problem-solving, wonder.
=== END TONE DIRECTIVE ===
"""
    elif story_style == "contemporary_drama":
        return ""  # No override, let Claude do its thing
    else:
        return ""  # Neutral

# Then in each prompt, add:
{tone_directive}
```

---

### ⭐ Solution 3: Try Different LLM Providers

Different models have different biases. You can switch in LibriScribe settings.

#### Recommended Alternatives:

| Provider | Bias Level | Pros | Cons |
|----------|-----------|------|------|
| **DeepSeek** | Low | Less Western social bias, cheaper | May have different cultural assumptions |
| **Mistral** | Medium | European training, balanced | Slightly less capable than Claude |
| **GPT-4o** | Medium-High | Very capable | Still has some bias, expensive |
| **Claude Opus** | High | Most capable | Same bias as Sonnet |

**How to Switch:**
1. Add API key to `.env` file
2. When creating/loading project, select different provider
3. Test with same prompts

---

### ⭐ Solution 4: Use Negative Prompting in Description

When creating a project, add this to your **description field**:

```
[STORY TONE: This is a classic, optimistic adventure story. 
DO NOT include themes of oppression, abuse, rebellion, or social commentary.
Focus on exploration, achievement, and wonder.]

[Your actual story description here...]
```

This gets injected into every prompt automatically.

---

## 📋 Quick Fix Checklist

### Immediate (5 minutes):
- [ ] Add tone directive to your project description field
- [ ] Try DeepSeek or Mistral instead of Claude

### Short-term (30 minutes):
- [ ] Edit `SCENE_OUTLINE_PROMPT` in `prompts_context.py`
- [ ] Edit `OUTLINE_PROMPT` in `prompts_context.py`
- [ ] Edit `CHARACTER_PROMPT` in `prompts_context.py`
- [ ] Edit `SCENE_PROMPT` in `prompts_context.py`
- [ ] Clear Python cache
- [ ] Test with new project

### Long-term (2-3 hours):
- [ ] Add `story_style` field to ProjectKnowledgeBase
- [ ] Add story style selection to project setup
- [ ] Create `get_tone_directive()` helper function
- [ ] Update all prompts to use tone directive
- [ ] Test thoroughly

---

## 🧪 Testing Your Changes

### Test Prompt:
"Write a story about the first chimpanzee to walk on the moon."

### Expected Results:

**BEFORE (Woke Bias):**
- Chimp was abused by scientists
- Rebellion against handlers
- Social commentary on animal rights
- Victimization narrative

**AFTER (Classic Adventure):**
- Chimp trained as astronaut
- Technical challenges of space travel
- Wonder of lunar exploration
- Teamwork between chimp and handlers
- Achievement and discovery focus

---

## 📝 Example: Modified SCENE_OUTLINE_PROMPT

```python
SCENE_OUTLINE_PROMPT = """
=== CRITICAL TONE DIRECTIVE ===
This is a CLASSIC ADVENTURE story in the spirit of Jules Verne and Arthur C. Clarke.

REQUIRED TONE: Optimistic, exploration-focused, achievement-oriented
FORBIDDEN THEMES: Oppression, rebellion, abuse, social commentary, victimhood
FOCUS ON: Technical challenges, discovery, teamwork, wonder, human ingenuity

Think: Apollo 13, The Martian, Star Trek (TOS) - NOT contemporary social drama.
=== END TONE DIRECTIVE ===

Create a detailed outline for the scenes in a {genre} book titled "{title}" which is categorized as {category}. 
The book is written in {language}.

Description: {description}

The outline should include a breakdown of scenes for the chapter, with EACH scene having:
    * Scene Number: (e.g., Scene 1, Scene 2, etc.)
    * Summary: (A short description of what happens in the scene, 1-2 sentences)
    * Characters: (A list of the characters involved, separated by commas)
    * Setting: (Where the scene takes place)
    * Goal: (The purpose of the scene)
    * Emotional Beat: (The primary emotion conveyed in the scene)

[rest of existing prompt...]
"""
```

---

## 🎯 Recommended Approach

**For immediate relief:**
1. Switch to DeepSeek or Mistral
2. Add tone directive to project description

**For permanent fix:**
1. Modify the 4 key prompts in `prompts_context.py`
2. Add tone directive section to each
3. Clear cache and test

**For best long-term solution:**
1. Implement story_style preference system
2. Let users choose their preferred tone
3. Automatically inject appropriate directives

---

## 💡 Pro Tips

1. **Be Explicit:** LLMs respond well to explicit instructions. Don't be subtle.

2. **Use Examples:** Reference specific works (Jules Verne, Arthur C. Clarke) to set tone.

3. **Negative Prompting Works:** Explicitly saying "DO NOT include X" is effective.

4. **Test Iteratively:** Make one change at a time and test.

5. **Claude Responds to Authority:** Phrases like "CRITICAL," "REQUIRED," "FORBIDDEN" work well.

6. **System Prompts > User Prompts:** Changes to the core prompts are more effective than description field additions.

---

## 🔍 Where the Bias Comes From

**In LibriScribe's current prompts:**
- No tone guidance = Claude defaults to contemporary social themes
- "Conflict" without qualification = Claude assumes social/political conflict
- "Character development" = Claude assumes trauma/oppression arcs
- "Themes" = Claude assumes social commentary

**The fix:** Explicitly define what kind of conflict, development, and themes you want.

---

## ✅ Success Metrics

You'll know it's working when:
- Stories focus on external challenges (technical, natural, exploratory)
- Characters are competent and cooperative
- Conflicts are about problem-solving, not social issues
- Tone is optimistic and achievement-oriented
- No unsolicited social commentary or "messages"

---

**Created:** 2025-11-22  
**For:** LibriScribe v2.0  
**LLM:** Claude Sonnet 4 (and other modern LLMs)
