import os
from google import genai

client = genai.Client()
# Create a new chat session linked to the 'gemini-2.5-flash' model
chat = client.chats.create(model="gemini-2.5-flash")

print("Chatbot initialized. Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    # Send the user's message and get a response
    response = chat.send_message(user_input)
    print(f"Bot: {response.text}")
    # The 'chat' object automatically remembers previous turns
