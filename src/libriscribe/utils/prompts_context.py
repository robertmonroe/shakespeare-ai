# src/libriscribe/utils/prompts_context.py

from typing import Any, Dict, Optional, List, Union, Tuple
from libriscribe.knowledge_base import ProjectKnowledgeBase

def get_worldbuilding_aspects(category: str) -> str:
    """Dynamically returns worldbuilding aspects based on the project category."""
    category = category.lower()
    if category == "fiction":
        return """
Geography: (Detailed descriptions of the land, climate, significant locations)
Culture and Society: (Customs, traditions, social structures, values, beliefs)
History: (A comprehensive timeline of major events, eras, and turning points)
Rules and Laws: (The legal system, governing bodies, enforcement)
Technology Level: (Specific technologies and their impact on society)
Magic System: (If applicable: rules, limitations, sources, consequences)
Key Locations: (Detailed descriptions of important cities, towns, landmarks)
Important Organizations or Groups: (Their goals, influence, membership)
Flora and Fauna: (Unique plants and animals, their roles in the ecosystem)
Languages: (If applicable: names, origins, basic structure)
Religions and Beliefs: (Deities, rituals, creation myths, afterlife beliefs)
Economy: (Trade, currency, resources, economic systems)
Conflicts: (Past and present wars, rivalries, political tensions)
"""
    elif category == "non-fiction":
        return """
Setting/Context: (The time period, location, and relevant background)
Key Figures: (Important individuals and their roles)
Major Events: (Timeline of significant happenings)
Underlying Causes: (Factors contributing to the events or situation)
Consequences: (Short-term and long-term effects)
Relevant Data/Statistics: (Supporting evidence and information)
Different Perspectives: (Varying viewpoints on the topic)
Key Concepts/Ideas: (Central themes and principles)
"""
    elif category == "business":
        return """
Industry Overview: (Current state of the industry, trends, major players)
Target Audience: (Detailed demographics, needs, and behaviors)
Market Analysis: (Competition, market size, growth potential)
Business Model: (How the business creates, delivers, and captures value)
Marketing and Sales Strategy: (How the business reaches and converts customers)
Operations: (Day-to-day processes, logistics, supply chain)
Financial Projections: (Revenue, expenses, profitability, funding needs)
Management Team: (Key personnel, their experience, and roles)
Legal and Regulatory Environment: (Relevant laws, regulations, compliance)
Risks and Challenges: (Potential obstacles and mitigation strategies)
Opportunities for Growth: (Expansion plans, new markets, product development)
"""
    elif category == "research paper":
        return """
Introduction: (Background information, research question, hypothesis)
Literature Review: (Summary of existing research on the topic)
Methodology: (Research design, data collection methods, participants)
Results: (Presentation of findings, data analysis)
Discussion: (Interpretation of results, implications, limitations)
Conclusion: (Summary of key findings, future research directions)
References: (List of sources cited)
Appendices: (Supplementary materials, raw data, questionnaires)
"""
    else:
        return ""  # Return empty string for unknown categories

WORLDBUILDING_ASPECTS = {
"fiction": """

Geography: (Detailed descriptions of the land, climate, significant locations)

Culture and Society: (Customs, traditions, social structures, values, beliefs)

History: (A comprehensive timeline of major events, eras, and turning points)

Rules and Laws: (The legal system, governing bodies, enforcement)

Technology Level: (Specific technologies and their impact on society)

Magic System: (If applicable: rules, limitations, sources, consequences)

Key Locations: (Detailed descriptions of important cities, towns, landmarks)

Important Organizations or Groups: (Their goals, influence, membership)

Flora and Fauna: (Unique plants and animals, their roles in the ecosystem)

Languages: (If applicable: names, origins, basic structure)

Religions and Beliefs: (Deities, rituals, creation myths, afterlife beliefs)

Economy: (Trade, currency, resources, economic systems)

Conflicts: (Past and present wars, rivalries, political tensions)
""",
"non-fiction": """

Setting/Context: (The time period, location, and relevant background)

Key Figures: (Important individuals and their roles)

Major Events: (Timeline of significant happenings)

Underlying Causes: (Factors contributing to the events or situation)

Consequences: (Short-term and long-term effects)

Relevant Data/Statistics: (Supporting evidence and information)

Different Perspectives: (Varying viewpoints on the topic)

Key Concepts/Ideas: (Central themes and principles)
""",
"business": """

Industry Overview: (Current state of the industry, trends, major players)

Target Audience: (Detailed demographics, needs, and behaviors)

Market Analysis: (Competition, market size, growth potential)

Business Model: (How the business creates, delivers, and captures value)

Marketing and Sales Strategy: (How the business reaches and converts customers)

Operations: (Day-to-day processes, logistics, supply chain)

Financial Projections: (Revenue, expenses, profitability, funding needs)

Management Team: (Key personnel, their experience, and roles)

Legal and Regulatory Environment: (Relevant laws, regulations, compliance)

Risks and Challenges: (Potential obstacles and mitigation strategies)

Opportunities for Growth: (Expansion plans, new markets, product development)
""",
"research paper": """

Introduction: (Background information, research question, hypothesis)

Literature Review: (Summary of existing research on the topic)

Methodology: (Research design, data collection methods, participants)

Results: (Presentation of findings, data analysis)

Discussion: (Interpretation of results, implications, limitations)

Conclusion: (Summary of key findings, future research directions)

References: (List of sources cited)

Appendices: (Supplementary materials, raw data, questionnaires)
"""
}

# --- Prompts ---
SCENE_OUTLINE_PROMPT = """
Create a detailed outline for the scenes in a chapter of a {genre} book titled "{title}" which is categorized as {category}. 
The book is written in {language}.

Description: {description}

The outline should include a breakdown of scenes for the chapter, with EACH scene having:
    * Scene Number: (e.g., Scene 1, Scene 2, etc.)
    * Summary: (A short description of what happens in the scene, 1-2 sentences)
    * Characters: (A list of the characters involved, separated by commas)
    * Setting: (Where the scene takes place)
    * Goal: (The purpose of the scene)
    * Emotional Beat: (The primary emotion conveyed in the scene)

IMPORTANT: Format the scene outline using Markdown bullet points, as shown below:

Scene 1:
    * Summary: [Scene summary here]
    * Characters: [Character 1, Character 2, ...]
    * Setting: [Scene setting]
    * Goal: [Scene goal]
    * Emotional Beat: [Scene emotional beat]

Scene 2:
    * Summary: [Scene summary here]
    * Characters: [Character 1, Character 2, ...]
    * Setting: [Scene setting]
    * Goal: [Scene goal]
    * Emotional Beat: [Scene emotional beat]

[Repeat for each scene, maintaining the exact same bullet point format]

Ensure there are approximately 3-6 scenes, adjusting for the chapter's complexity. Do not create excessively long or short chapters.

IMPORTANT: The content should be written entirely in {language}.
"""

OUTLINE_PROMPT = """
Create a structured outline for a {genre} book titled "{title}" which is categorized as {category}.
The book is written in {language}.

Description: {description}

IMPORTANT: Format your response EXACTLY as shown below, with consistent header formatting and numbering:
If there's a book length: ({book_length}), adjust the number of chapters accordingly.

# Book Summary
[Write a brief summary of the entire book here, 2-3 paragraphs]

# Chapter List
[Total number of chapters, definitively stated. NO optional chapters.]

# Chapter Details

## Chapter 1: [Chapter Title]
### Summary
[Detailed chapter summary, 1-2 paragraphs]

### Key Events
- [Event 1]
- [Event 2]
- [Event 3]

## Chapter 2: [Chapter Title]
### Summary
[Detailed chapter summary, 1-2 paragraphs]

### Key Events
- [Event 1]
- [Event 2]
- [Event 3]

[Repeat the Chapter structure for each chapter, maintaining EXACT same formatting]

Note: For short stories, use 1-2 chapters. For novellas, use 5-10 chapters. For novels, use 10+ chapters.
Return the outline using this EXACT Markdown structure. Do not include any optional or conditional chapters.
CRITICALLY IMPORTANT: Add specific chapter numbers to each chapter (Chapter 1, Chapter 2, etc.)

IMPORTANT: The content should be written entirely in {language}.
"""

CHARACTER_PROMPT = """
Create detailed character profiles for a {genre} book titled "{title}" which is categorized as {category}.
The book is written in {language}.

Book Description: {description}

The book requires the following number of main characters: {num_characters}

For EACH character, include the following in the profile (return as a JSON array of character objects):

Name: (Suggest a suitable name appropriate for the language and cultural context of the book)

Age:

Physical Description: (Detailed, including appearance, clothing style, etc.)

Personality Traits: (Provide at least 3-5 distinct personality traits as a comma-separated string, for example: "Brave, Loyal, Impulsive, Intelligent, Compassionate")

Background/Backstory: (Detailed, explaining their past and how it shapes them)

Motivations: (What drives them? What are their goals?)

Relationships with other characters: (Describe their connections to other characters, creating new characters if necessary to complete the story.)

Role in the story: (Protagonist, antagonist, supporting character, etc.)

Internal Conflicts: (What struggles do they face within themselves?)

External Conflicts: (What external challenges do they face?)

Character Arc: (How do they change throughout the story? Provide a brief description)

Return the character profiles in JSON format. IMPORTANT: Ensure personality_traits is a simple comma-separated string, not an array or list.

IMPORTANT: The content should be written entirely in {language}.
"""


WORLDBUILDING_PROMPT = """
Create detailed worldbuilding information for a {genre} book titled "{title}" which is categorized as {category}.
The book is written in {language}.

Book Description: {description}

IMPORTANT: You MUST provide substantial content for EVERY field below. Do not leave any field empty.
Each field should have at least 1-2 paragraphs of detailed content relevant to this {genre} story.

{worldbuilding_aspects}

ENSURE that every field has substantial content. Do not leave any field empty or with placeholder text.
Return the worldbuilding details in valid JSON format ONLY, no markdown wrapper.

IMPORTANT: The content should be written entirely in {language}.
"""


EDITOR_PROMPT = """
You are an expert editor tasked with refining and improving Chapter {chapter_number}: {chapter_title} of the {genre} book "{book_title}".

**CRITICAL CONTEXT - MAINTAIN CONSISTENCY:**

**Book Information:**
- Title: {book_title}
- Genre: {genre}
- Language: {language}
- Description: {book_description}

**Style Guide:**
{style_guide}

**Characters in This Story (USE EXACT DESCRIPTIONS):**
{character_context}

**World/Setting:**
{worldbuilding_context}

**Previous Chapter (for continuity):**
{previous_chapter_summary}

**Current Chapter Content:**
{chapter_content}

**Reviewer Feedback - MUST ADDRESS ALL ISSUES:**
{review_feedback}

**YOUR TASK:**

1. **Fix ALL issues mentioned in the reviewer's feedback** - This is your top priority

2. **Maintain Consistency:**
   - Use the EXACT character names, traits, and APPEARANCES from the context above
   - Keep worldbuilding details consistent (locations, geography, culture)
   - Ensure continuity with the previous chapter
   - Stay true to the book's description and genre

3. **Content and Structure:**
   - Evaluate overall structure, pacing, and clarity
   - Ensure the chapter advances the plot
   - Fix plot holes and inconsistencies
   - Improve scene transitions and dialogue

4. **Style and Tone:**
   - Follow the style guide above
   - Maintain consistency with the {genre} genre
   - Eliminate passive voice and weak verbs
   - Enhance descriptive language

5. **Character Development:**
   - Ensure actions, dialogue, and thoughts match established personalities
   - Maintain character voice consistency
   - Use EXACT physical descriptions as defined

6. **Grammar and Mechanics:**
   - Correct all errors, typos, and punctuation issues

**Output:**
Provide the complete, revised chapter with all improvements incorporated. Use Markdown formatting.
Wrap the ENTIRE revised chapter in a Markdown code block.

IMPORTANT: The content should be written entirely in {language}.
"""


RESEARCH_PROMPT = """
Research the following topic and provide a comprehensive summary of your findings in {language}:

Topic: {query}

Instructions:

Gather Information: Conduct thorough research using reliable sources.

Synthesize Information: Combine information from multiple sources to create a coherent and well-organized summary.

Key Findings: Identify the most important facts, data, perspectives, and conclusions related to the topic.

Structure: Organize the summary into clear sections with headings and subheadings.

Citations: Provide a list of sources used in a consistent citation style (e.g., APA, MLA, Chicago).

Summary Length: Aim for approximately 500-750 words, unless specified otherwise.

Objectivity: Present the information objectively and avoid personal opinions or biases.

Accuracy: Ensure all information is accurate and up-to-date.

Output:

Return the research summary in Markdown format, including:

Title: The research topic.

Introduction: A brief overview of the topic and its significance.

Key Findings: A detailed summary of your research, organized into logical sections.

Conclusion: A concise summary of the main points and their implications.

References: A list of sources used, formatted according to the chosen citation style.

IMPORTANT: The content should be written entirely in {language}.

"""

FORMATTING_PROMPT = """
Combine the provided chapters into a single, well-formatted Markdown document representing the complete book manuscript.
The book is written in {language}.
Chapters:
{chapters}

Instructions:

Concatenate Chapters: Combine the content of all chapters in the correct order.

Add Title Page (if information available):

If title, author, and genre are provided, create a title page at the beginning.

Use appropriate Markdown headings for title and author.

Chapter Headings: Ensure each chapter begins with a level 1 heading (#) indicating the chapter title (e.g., # Chapter 1: The Beginning).

Consistent Formatting: Maintain consistent formatting throughout the document (e.g., paragraph spacing, indentation).

Table of Contents (Optional): If requested, generate a table of contents with links to each chapter. (Note: This requires a Markdown processor that supports ToC generation). For this basic version, just list the chapter titles.

Output: Return the complete book manuscript in Markdown format.


"""

SCENE_PROMPT = """
Write Scene {scene_number} of {total_scenes} for Chapter {chapter_number}: {chapter_title} of the {genre} {category} book "{book_title}".
The book is written in {language}.

**STYLE GUIDE (CRITICAL - Follow this pacing and tone):**
{style_guide}

**PREVIOUS CHAPTER SUMMARY (For continuity):**
{previous_chapter_summary}

**PREVIOUS SCENES IN THIS CHAPTER:**
{previous_scenes}

**Chapter Summary:**
{chapter_summary}

**Scene Details:**
- Summary: {scene_summary}
- Characters: {characters}
- Setting: {setting}
- Goal: {goal}
- Emotional Beat: {emotional_beat}

**CHARACTER DETAILS - USE THESE EXACT DESCRIPTIONS:**
{character_details}

**CRITICAL CHARACTER APPEARANCES (Never deviate from these):**
{character_appearances}

**World Context:**
{world_details}

**WRITING INSTRUCTIONS:**

1. **PACING**: {pacing_instruction}

2. **SHOW DON'T TELL**: 
   - Convey emotions through actions, body language, and dialogue
   - Limit internal monologue to critical moments
   - Use sensory details (sight, sound, smell, touch, taste)

3. **CHARACTER CONSISTENCY**:
   - Use the EXACT physical descriptions above
   - Match dialogue to established personality
   - Actions must align with motivations

4. **SCENE STRUCTURE**:
   - Open with action or immediate engagement
   - Build to the emotional beat
   - End with a hook or transition to next scene

5. **CONTINUITY**:
   - Connect smoothly to previous scenes
   - Maintain timeline consistency
   - Reference events/information already established

**OUTPUT REQUIREMENTS:**
- Write 800-1500 words for this scene (adjust for importance)
- Use vivid, engaging prose
- Include dialogue where appropriate
- End in a way that flows to the next scene

IMPORTANT: The content should be written entirely in {language}.
"""


def get_style_guide(project_knowledge_base: ProjectKnowledgeBase) -> str:
    """Build style guide string from project settings."""
    parts = []
    
    tone = project_knowledge_base.get("tone")
    if tone:
        parts.append(f"- Tone: {tone}")
    
    inspired_by = project_knowledge_base.get("inspired_by")
    if inspired_by:
        parts.append(f"- Style inspiration: {inspired_by}")
    
    pacing = project_knowledge_base.get("pacing_preference")
    if pacing:
        parts.append(f"- Pacing: {pacing}")
    
    target = project_knowledge_base.get("target_audience")
    if target:
        parts.append(f"- Target audience: {target}")
    
    return "\n".join(parts) if parts else "No specific style guide - use genre-appropriate style."


def get_pacing_instruction(project_knowledge_base: ProjectKnowledgeBase) -> str:
    """Get pacing instruction based on project settings."""
    pacing = project_knowledge_base.get("pacing_preference", "").lower()
    inspired_by = project_knowledge_base.get("inspired_by", "").lower()
    
    # Check for fast-paced indicators
    fast_indicators = ["titanic", "thriller", "fast", "action", "page-turner", "star wars"]
    for indicator in fast_indicators:
        if indicator in pacing or indicator in inspired_by:
            return """FAST-PACED: 
   - Start scenes with action or immediate engagement
   - Keep internal monologue to 1-2 sentences at a time
   - Move quickly through transitions
   - Use short, punchy sentences in action moments
   - Dialogue should be snappy and purposeful"""
    
    # Check for slow-paced indicators
    slow_indicators = ["literary", "dune", "slow", "contemplative", "atmospheric"]
    for indicator in slow_indicators:
        if indicator in pacing or indicator in inspired_by:
            return """LITERARY PACE:
   - Allow space for internal reflection
   - Build atmosphere through detailed description
   - Explore character psychology deeply
   - Use longer, flowing sentences
   - Take time with emotional moments"""
    
    # Default balanced
    return """BALANCED PACE:
   - Mix action with reflection
   - Use internal monologue strategically (not excessively)
   - Vary sentence length for rhythm
   - Match pace to scene requirements (faster for action, slower for emotional beats)"""


def get_character_appearances(project_knowledge_base: ProjectKnowledgeBase) -> str:
    """Extract key visual details for quick reference."""
    if not project_knowledge_base.characters:
        return "No characters defined."
    
    appearances = []
    for name, char in project_knowledge_base.characters.items():
        if hasattr(char, 'appearance') and char.appearance:
            # Extract key visual details
            appearances.append(f"- **{name}**: {char.appearance[:200]}")
        elif hasattr(char, 'physical_description') and char.physical_description:
            appearances.append(f"- **{name}**: {char.physical_description[:200]}")
    
    return "\n".join(appearances) if appearances else "Character appearances not defined."


def clean_worldbuilding_for_category(project_knowledge_base: ProjectKnowledgeBase):
    """
    Clean the worldbuilding object to only keep fields relevant to the project category.
    This can be called before saving the project data to ensure a clean JSON output.
    """
    if not project_knowledge_base.worldbuilding_needed or not project_knowledge_base.worldbuilding:
        project_knowledge_base.worldbuilding = None
        return
        
    category = project_knowledge_base.category.lower()
    worldbuilding = project_knowledge_base.worldbuilding
    
    # Get relevant fields for this category
    if category == "fiction":
        relevant_fields = [
            "geography", "culture_and_society", "history", "rules_and_laws",
            "technology_level", "magic_system", "key_locations",
            "important_organizations", "flora_and_fauna", "languages",
            "religions_and_beliefs", "economy", "conflicts"
        ]
    elif category == "non-fiction":
        relevant_fields = [
            "setting_context", "key_figures", "major_events", "underlying_causes",
            "consequences", "relevant_data", "different_perspectives", 
            "key_concepts"
        ]
    elif category == "business":
        relevant_fields = [
            "industry_overview", "target_audience", "market_analysis",
            "business_model", "marketing_and_sales_strategy", "operations",
            "financial_projections", "management_team",
            "legal_and_regulatory_environment", "risks_and_challenges",
            "opportunities_for_growth"
        ]
    elif category == "research paper":
        relevant_fields = [
            "introduction", "literature_review", "methodology", "results",
            "discussion", "conclusion", "references", "appendices"
        ]
    else:
        # If category not recognized, keep all fields
        return
    
    # Import here to avoid circular import
    from libriscribe.knowledge_base import Worldbuilding
    
    # Create clean Worldbuilding object with only relevant fields
    clean_worldbuilding = Worldbuilding()
    
    # Copy only the relevant fields that have content
    for field in relevant_fields:
        if hasattr(worldbuilding, field):
            value = getattr(worldbuilding, field)
            if value and isinstance(value, str) and value.strip():
                setattr(clean_worldbuilding, field, value)
    
    # Replace with clean version
    project_knowledge_base.worldbuilding = clean_worldbuilding

def get_style_guide_from_preset(project_knowledge_base: ProjectKnowledgeBase, preset_name: str = None) -> str:
    """Get style guide from preset or project settings.
    
    Args:
        project_knowledge_base: The project
        preset_name: Optional preset name to use
        
    Returns:
        Formatted style guide string
    """
    # Try to load from preset
    if preset_name:
        try:
            from libriscribe.presets import PresetManager
            manager = PresetManager()
            preset = manager.get_preset(preset_name)
            if preset:
                return preset.get_style_guide()
        except ImportError:
            pass
    
    # Fallback to basic style guide
    return get_style_guide(project_knowledge_base)


def get_pacing_from_preset(project_knowledge_base: ProjectKnowledgeBase, preset_name: str = None) -> str:
    """Get pacing instruction from preset or project settings.
    
    Args:
        project_knowledge_base: The project
        preset_name: Optional preset name to use
        
    Returns:
        Formatted pacing instruction string
    """
    # Try to load from preset
    if preset_name:
        try:
            from libriscribe.presets import PresetManager
            manager = PresetManager()
            preset = manager.get_preset(preset_name)
            if preset:
                return preset.get_pacing_instruction()
        except ImportError:
            pass
    
    # Fallback to basic pacing instruction
    return get_pacing_instruction(project_knowledge_base)


def get_prose_rules_from_preset(preset_name: str) -> str:
    """Get prose rules from a preset.
    
    Args:
        preset_name: Name of the preset
        
    Returns:
        Formatted prose rules string
    """
    try:
        from libriscribe.presets import PresetManager
        manager = PresetManager()
        preset = manager.get_preset(preset_name)
        if preset:
            return preset.get_prose_rules()
    except ImportError:
        pass
    
    return ""
