import requests
import json
import os

# Configuration
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY_HERE"  # Replace with your actual key
OUTPUT_DIR = "generated_novels"

def generate_chapter(book_title, genre, chapter_number, chapter_title, chapter_summary, language="English"):
    """Generate a single chapter using OpenRouter/Claude"""
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    book_dir = os.path.join(OUTPUT_DIR, book_title.replace(" ", "_"))
    os.makedirs(book_dir, exist_ok=True)
    
    # Prepare the prompt
    prompt = f"""Write Chapter {chapter_number}: {chapter_title} for the {genre} novel '{book_title}'.

Chapter Summary: {chapter_summary}

Instructions:
- Write in {language}
- Aim for 3000-4000 words
- Use vivid, cinematic descriptions
- Show don't tell
- Include dialogue and action
- End with a hook for the next chapter
- Match the tone and pacing of a professional {genre} novel

Write the complete chapter now:"""

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Shakespeare AI Novel Generator"
    }
    
    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8000,
        "temperature": 0.7
    }
    
    print(f"Generating Chapter {chapter_number}: {chapter_title}...")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        chapter_content = result['choices'][0]['message']['content']
        
        # Save to file
        filename = os.path.join(book_dir, f"chapter_{chapter_number}.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Chapter {chapter_number}: {chapter_title}\n\n")
            f.write(chapter_content)
        
        print(f"✅ Chapter {chapter_number} saved to: {filename}")
        print(f"📊 Word count: ~{len(chapter_content.split())} words")
        return chapter_content
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Example: Generate Chapter 1
    generate_chapter(
        book_title="The Moscow Protocol",
        genre="Spy Thriller",
        chapter_number=1,
        chapter_title="The Dead Drop",
        chapter_summary="MI6 agent discovers a compromised asset in Moscow. Must retrieve critical intelligence before the FSB closes in.",
        language="English"
    )
    
    print("\n✨ Done! Check the 'generated_novels' folder for your chapter.")
