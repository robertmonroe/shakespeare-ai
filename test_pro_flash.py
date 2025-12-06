import google.generativeai as genai
from pathlib import Path

# Load API key from .env
env_file = Path(r"c:\Users\3dmax\Libriscribe\.env")
env_vars = {}
for line in env_file.read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        env_vars[key.strip()] = value.strip()

api_key = env_vars.get('GOOGLE_AI_STUDIO_API_KEY')
genai.configure(api_key=api_key)

# Test both models
models_to_test = [
    ("gemini-1.5-pro-002", "Production (Pro)"),
    ("gemini-1.5-flash-002", "Test (Flash)"),
]

print("Testing Google AI Studio models for Production/Test modes...\n")

for model_name, mode in models_to_test:
    try:
        print(f"Testing {mode}: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content("Say 'OK'")
        print(f"✅ WORKS!")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ Model not found")
        else:
            print(f"❌ Error: {error_msg[:80]}")

print("\nDone!")
