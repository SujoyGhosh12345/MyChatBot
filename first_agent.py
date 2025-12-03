import os
from google import genai
from google.genai import types

try:
    client = genai.Client()
    print("Client initialized successfully.")

    config = types.GenerateContentConfig(
        system_instruction="You are a friendly and helpful coding assistant."
    )
    prompt = "What is the fastest way to learn Python loops?"

    # --- CHANGE THIS LINE TO 2.5 FLASH ---
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config,
    )
    # ------------------------------------

    print("\nAI Response:")
    print(response.text)

except Exception as e:
    print(f"\nAn error occurred: {e}")
    # The API key part of the error is resolved!
