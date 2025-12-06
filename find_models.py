import google.generativeai as genai
from pathlib import Path

# Load API key
env_file = Path(r"c:\Users\3dmax\Libriscribe\.env")
env_vars = {}
for line in env_file.read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        env_vars[key.strip()] = value.strip()

api_key = env_vars.get('GOOGLE_AI_STUDIO_API_KEY')
genai.configure(api_key=api_key)

# Test various model names
models_to_test = [
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash-exp",
]

print("Finding working Google AI models...\n")

working_models = []
for model_name in models_to_test:
    try:
        print(f"Testing: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content("Say 'OK'")
        print(f"✅ WORKS!")
        working_models.append(model_name)
    except Exception as e:
        if "404" in str(e):
            print(f"❌ Not found")
        else:
            print(f"❌ Error")

print(f"\n✅ Working models: {working_models}")
print(f"\nRecommendation:")
print(f"  Production: {working_models[0] if working_models else 'None found'}")
print(f"  Test: {working_models[-1] if len(working_models) > 1 else working_models[0] if working_models else 'None found'}")
