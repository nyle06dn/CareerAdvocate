import google.generativeai as genai

# Use one of the keys from your AI Studio dashboard
genai.configure(api_key="YOUR_COPIED_API_KEY")

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")