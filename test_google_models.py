import google.generativeai as genai
from pathlib import Path

# Load .env file
env_file = Path(r"c:\Users\3dmax\Libriscribe\.env")
env_vars = {}
for line in env_file.read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        env_vars[key.strip()] = value.strip()

api_key = env_vars.get('GOOGLE_AI_STUDIO_API_KEY')
if not api_key:
    print("ERROR: GOOGLE_AI_STUDIO_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

# Test different model names
models_to_test = [
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-2.0-flash-exp",
]

print("Testing Google AI Studio models...\n")

for model_name in models_to_test:
    try:
        print(f"Testing: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content("Say 'OK' if this works")
        print(f"✅ WORKS! Response: {response.text[:50]}")
        print(f"\n✅ USE THIS MODEL: {model_name}")
        break  # Stop at first working model
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ Model not found")
        else:
            print(f"❌ Error: {error_msg[:80]}")

print("\nDone!")
