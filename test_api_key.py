"""
Test if the OpenAI API key in .env is working.
Run: python test_api_key.py
"""

import os
import sys

# Load .env manually (no dotenv dependency needed)
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

print(f"API Key found: {api_key[:12]}...{api_key[-4:]}")
print("Testing connection to OpenAI...\n")

try:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'API key is working!'"}],
        max_tokens=20,
    )

    print("✅ API key is VALID and working!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model: {response.model}")
    print(f"Usage: {response.usage}")

except Exception as e:
    print(f"❌ API key test FAILED: {e}")
    sys.exit(1)
