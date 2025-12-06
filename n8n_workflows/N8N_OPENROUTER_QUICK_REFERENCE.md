# N8N + OpenRouter Quick Reference Guide
## For AI Book Generator Tutorial

This guide helps you adapt any N8N tutorial that uses Anthropic/Claude directly to work with **OpenRouter** instead.

---

## Why Use OpenRouter?

- ✅ Access Claude AND other models (GPT-4, Gemini, etc.)
- ✅ One API key for multiple providers
- ✅ Often cheaper than direct API access
- ✅ Built-in rate limiting and fallbacks

---

## HTTP Request Node Configuration for OpenRouter

### Basic Settings
```
Method: POST
URL: https://openrouter.ai/api/v1/chat/completions
```

### Authentication
**Option 1: Using Header Auth Credential**
1. Authentication: `Generic Credential Type`
2. Generic Auth Type: `Header Auth`
3. Create credential:
   - Name: `OpenRouter API`
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_OPENROUTER_API_KEY`

**Option 2: Manual Header (Simpler)**
1. Authentication: `None`
2. Add header manually (see Headers section below)

### Headers
Toggle **Send Headers** to ON, then add:

**Required Headers:**
```
Name: Authorization
Value: Bearer YOUR_OPENROUTER_API_KEY

Name: Content-Type
Value: application/json

Name: HTTP-Referer
Value: http://localhost:5678
```

**Optional but Recommended:**
```
Name: X-Title
Value: Shakespeare AI Novel Generator
```

### Body Configuration
```
Send Body: ON
Body Content Type: JSON
Specify Body: Using JSON
```

**JSON Body Template:**
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": "YOUR_PROMPT_HERE"
    }
  ],
  "max_tokens": 8000,
  "temperature": 0.7
}
```

---

## Available Models on OpenRouter

### Claude Models (Anthropic)
```
anthropic/claude-3.5-sonnet          ← Best for novels (recommended)
anthropic/claude-3-opus              ← Most creative
anthropic/claude-3-sonnet            ← Balanced
anthropic/claude-3-haiku             ← Fastest/cheapest
```

### Alternative Models
```
openai/gpt-4-turbo                   ← GPT-4 alternative
openai/gpt-4o                        ← Latest GPT-4
google/gemini-pro-1.5                ← Google's model
meta-llama/llama-3.1-70b-instruct    ← Open source option
```

---

## Common Prompts for Novel Generation

### Generate Chapter Outline
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [{
    "role": "user",
    "content": "Create a detailed outline for a 20-chapter spy thriller novel titled 'The Moscow Protocol'. Include chapter titles and 2-3 sentence summaries for each chapter."
  }],
  "max_tokens": 4000,
  "temperature": 0.7
}
```

### Generate Single Chapter
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [{
    "role": "user",
    "content": "Write Chapter 1: The Dead Drop for the spy thriller 'The Moscow Protocol'. Write 3000-4000 words with vivid descriptions, dialogue, and action. End with a cliffhanger."
  }],
  "max_tokens": 8000,
  "temperature": 0.7
}
```

### Review Chapter for Issues
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [{
    "role": "user",
    "content": "Review this chapter for plot holes, inconsistencies, pacing issues, and character development problems:\n\n[CHAPTER_CONTENT_HERE]"
  }],
  "max_tokens": 2000,
  "temperature": 0.3
}
```

### Edit Chapter Based on Review
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [{
    "role": "user",
    "content": "Fix ALL issues in this chapter based on the review feedback:\n\nREVIEW:\n[REVIEW_FEEDBACK]\n\nCHAPTER:\n[CHAPTER_CONTENT]\n\nReturn the complete revised chapter."
  }],
  "max_tokens": 8000,
  "temperature": 0.5
}
```

---

## Extracting Response Data

OpenRouter returns responses in this format:
```json
{
  "choices": [
    {
      "message": {
        "content": "THE GENERATED TEXT IS HERE"
      }
    }
  ]
}
```

**To extract the generated text in N8N:**
- Use expression: `{{ $json.choices[0].message.content }}`

---

## Temperature Settings Guide

```
0.1 - 0.3  → Very focused, consistent (good for editing/fixing)
0.5 - 0.7  → Balanced creativity (good for chapter writing)
0.8 - 1.0  → Very creative (good for brainstorming/outlines)
```

---

## Token Limits

**Max tokens per request:**
- Claude 3.5 Sonnet: Up to 200k input, 8k output (via OpenRouter)
- Recommended for chapters: 8000 tokens = ~6000 words

**Cost estimation (approximate):**
- Claude 3.5 Sonnet: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- Generating 20 chapters (3000 words each): ~$2-5 total

---

## Troubleshooting

### Error: "Unauthorized" or 401
- Check your OpenRouter API key is correct
- Ensure "Bearer " is before the key
- Verify key has credits at openrouter.ai/credits

### Error: "Model not found"
- Check model name spelling
- Use format: `provider/model-name`
- List of models: https://openrouter.ai/models

### Response is too short
- Increase `max_tokens` (try 12000 or 16000)
- Add "Write at least 3000 words" to your prompt
- Lower temperature slightly (0.5-0.6)

### Response is cut off mid-sentence
- Increase `max_tokens`
- OpenRouter may have hit the model's limit
- Try splitting into smaller chunks

### Rate limit errors
- OpenRouter has built-in rate limiting
- Wait 60 seconds and retry
- Or upgrade your OpenRouter plan

---

## Differences from Direct Anthropic API

| Feature | Anthropic Direct | OpenRouter |
|---------|-----------------|------------|
| **Endpoint** | `api.anthropic.com/v1/messages` | `openrouter.ai/api/v1/chat/completions` |
| **Auth Header** | `x-api-key` | `Authorization: Bearer` |
| **Request Format** | Anthropic-specific | OpenAI-compatible |
| **Model Name** | `claude-3-5-sonnet-20241022` | `anthropic/claude-3.5-sonnet` |
| **Response Format** | Anthropic format | OpenAI format |

---

## Complete Working Example

**HTTP Request Node Settings:**
```
Method: POST
URL: https://openrouter.ai/api/v1/chat/completions
Authentication: None

Headers:
  Authorization: Bearer sk-or-v1-YOUR_KEY_HERE
  Content-Type: application/json
  HTTP-Referer: http://localhost:5678

Body (JSON):
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": "Write a 500-word opening scene for a spy thriller set in Moscow."
    }
  ],
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Extract Response:**
- Add "Set" node after HTTP Request
- Expression: `{{ $json.choices[0].message.content }}`
- This gives you the generated text

---

## Next Steps

1. **Test with simple prompt** - Generate a 500-word scene
2. **Build chapter generator** - Use the chapter prompt template
3. **Add file saving** - Use "Write Binary File" node
4. **Create loop** - Generate multiple chapters automatically
5. **Add review/edit** - Chain multiple HTTP requests

---

## Resources

- OpenRouter Dashboard: https://openrouter.ai/
- Model Pricing: https://openrouter.ai/models
- API Docs: https://openrouter.ai/docs
- N8N Community: https://community.n8n.io/

---

**Good luck building your novel generator! 🚀**
