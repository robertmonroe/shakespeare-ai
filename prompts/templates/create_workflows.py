import requests
import json
import uuid

# N8N API configuration
N8N_URL = "http://localhost:5678"
USERNAME = "cgartandweb@gmail.com"
PASSWORD = "MyN8N1@#17"

def create_workflow(name, system_message, input_text):
    """Create a new N8N workflow"""
    webhook_id = str(uuid.uuid4())
    
    workflow_data = {
        "name": name,
        "active": False,
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": webhook_id,
                    "options": {}
                },
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2.1,
                "position": [0, 0],
                "id": f"webhook-{webhook_id[:8]}",
                "name": "Webhook",
                "webhookId": webhook_id
            },
            {
                "parameters": {
                    "promptType": "define",
                    "text": input_text,
                    "options": {
                        "systemMessage": system_message
                    }
                },
                "type": "@n8n/n8n-nodes-langchain.agent",
                "typeVersion": 3,
                "position": [208, 0],
                "id": f"agent-{webhook_id[:8]}",
                "name": "AI Agent"
            },
            {
                "parameters": {
                    "model": "anthropic/claude-sonnet-4.5",
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
                "typeVersion": 1,
                "position": [80, 208],
                "id": f"model-{webhook_id[:8]}",
                "name": "OpenRouter Chat Model",
                "credentials": {
                    "openRouterApi": {
                        "id": "N8GwdEqLBJAYPzWp",
                        "name": "OpenRouter account"
                    }
                }
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "AI Agent",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "OpenRouter Chat Model": {
                "ai_languageModel": [
                    [
                        {
                            "node": "AI Agent",
                            "type": "ai_languageModel",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "executionOrder": "v1"
        }
    }
    
    try:
        response = requests.post(
            f"{N8N_URL}/rest/workflows",
            json=workflow_data,
            auth=(USERNAME, PASSWORD),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print(f"✅ Successfully created: {name}")
            return response.json()
        else:
            print(f"❌ Failed to create {name}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating {name}: {e}")
        return None

# Define the workflows to create
workflows = [
    {
        "name": "Book Creation - Scene Generator",
        "system_message": """Write Scene {scene_number} for Chapter {chapter_number} of "{book_title}".

Scene outline: {scene_outline}
Scene purpose: {scene_purpose}
Characters involved: {scene_characters}
Setting: {scene_setting}

Write engaging scene content that:
- Advances the plot meaningfully
- Develops characters through action/dialogue
- Maintains consistent tone and pacing
- Connects smoothly with adjacent scenes

Focus on showing rather than telling.
Language: {language}""",
        "input_text": """=Scene Number: {{ $json.body.scene_number }}
Chapter Number: {{ $json.body.chapter_number }}
Book Title: {{ $json.body.book_title }}
Scene Outline: {{ $json.body.scene_outline }}
Scene Purpose: {{ $json.body.scene_purpose }}
Characters: {{ $json.body.scene_characters }}
Setting: {{ $json.body.scene_setting }}
Language: {{ $json.body.language }}"""
    },
    {
        "name": "Book Creation - Scene Outliner",
        "system_message": """Create detailed scene outlines for Chapter {chapter_number} of this {genre} story.

Chapter context: {chapter_context}
Chapter summary: {chapter_summary}

For each scene, provide:
- Scene purpose and goals
- Key events and conflicts
- Character interactions
- Emotional beats and tension
- Setting and atmosphere
- Transition to next scene

Generate 3-5 scenes that create a compelling chapter flow.
Language: {language}""",
        "input_text": """=Chapter Number: {{ $json.body.chapter_number }}
Genre: {{ $json.body.genre }}
Chapter Context: {{ $json.body.chapter_context }}
Chapter Summary: {{ $json.body.chapter_summary }}
Language: {{ $json.body.language }}"""
    },
    {
        "name": "Book Creation - Fact Checker",
        "system_message": """Fact-check the following content from a {genre} book for accuracy and consistency.

Content to verify:
{content_to_check}

Check for:
- Historical accuracy (dates, events, people)
- Technical correctness (science, technology, procedures)
- Geographic accuracy (locations, distances, climate)
- Cultural authenticity (customs, languages, traditions)
- Internal story consistency (previously established facts)
- Logical plausibility within the story world

Report any inaccuracies found and suggest corrections.
Note any areas requiring additional research.
Language: {language}""",
        "input_text": """=Genre: {{ $json.body.genre }}
Content to Check: {{ $json.body.content_to_check }}
Language: {{ $json.body.language }}"""
    },
    {
        "name": "Book Creation - Researcher",
        "system_message": """Research the following topic for a {genre} writing project.

Research query: {query}
Project context: {project_context}

Provide:
- Key facts and information
- Relevant details for storytelling
- Historical or technical accuracy notes
- Interesting angles or perspectives
- Sources for further research

Focus on information that enhances authenticity and depth.
Language: {language}""",
        "input_text": """=Genre: {{ $json.body.genre }}
Query: {{ $json.body.query }}
Project Context: {{ $json.body.project_context }}
Language: {{ $json.body.language }}"""
    },
    {
        "name": "Book Creation - Worldbuilding",
        "system_message": """Create detailed worldbuilding for this {category} {genre} project.

Project context: {project_context}
Required elements: {worldbuilding_aspects}

Generate comprehensive details for:
- Geography and locations
- Culture and society
- History and timeline
- Rules and laws
- Technology level
- Key organizations

Output in JSON format with structured worldbuilding data.
Language: {language}""",
        "input_text": """=Category: {{ $json.body.category }}
Genre: {{ $json.body.genre }}
Project Context: {{ $json.body.project_context }}
Worldbuilding Aspects: {{ $json.body.worldbuilding_aspects }}
Language: {{ $json.body.language }}"""
    },
    {
        "name": "Book Creation - Plagiarism Checker",
        "system_message": """Check this {genre} content for potential originality concerns and similarity to well-known works.

Content to analyze:
{content_to_analyze}

Evaluate for:
- Similarity to famous {genre} works or popular stories
- Overused tropes or clichéd elements
- Distinctive phrases that might echo other works
- Plot elements that closely mirror existing stories
- Character archetypes that are too derivative
- Unique elements that enhance originality

Provide a summary of originality assessment and suggestions for enhancing uniqueness.
Flag any specific concerns that require attention.
Language: {language}""",
        "input_text": """=Genre: {{ $json.body.genre }}
Content to Analyze: {{ $json.body.content_to_analyze }}
Language: {{ $json.body.language }}"""
    }
]

# Create all workflows
print("Creating LibriScribe N8N workflows...")
print("=" * 50)

created_workflows = []
for workflow in workflows:
    result = create_workflow(
        workflow["name"],
        workflow["system_message"],
        workflow["input_text"]
    )
    if result:
        created_workflows.append(result)

print("=" * 50)
print(f"Successfully created {len(created_workflows)} out of {len(workflows)} workflows")
