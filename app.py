import os
from flask import Flask, request, jsonify, render_template_string
from google import genai

# Initialize the Flask app
app = Flask(__name__)
client = genai.Client()

# Simple HTML template for the front end
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini Chatbot</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; }
        #chatbox { height: 300px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll; }
        .message { margin-bottom: 10px; }
        .user { color: blue; }
        .bot { color: green; }
    </style>
</head>
<body>
    <h1>Gemini Chatbot</h1>
    <div id="chatbox"></div>
    <input type="text" id="user_input" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        function sendMessage() {
            const input = document.getElementById('user_input');
            const message = input.value;
            if (!message) return;

            // Add user message to chatbox
            const chatbox = document.getElementById('chatbox');
            chatbox.innerHTML += `<div class="message user">You: ${message}</div>`;
            input.value = '';

            // Send message to the Flask backend API
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Add bot message to chatbox
                chatbox.innerHTML += `<div class="message bot">Bot: ${data.response}</div>`;
                chatbox.scrollTop = chatbox.scrollHeight; // Scroll to bottom
            });
        }
    </script>
</body>
</html>
"""

# The main web page route
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# The API endpoint that handles the AI interaction
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        # We need a way to manage chat history globally or use a simple generate_content for now
        # For simplicity in this basic Flask app, we'll use a single-turn interaction
        # If you want true multi-turn, you need session management (more complex)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app locally for testing
    # It will run on 127.0.0.1
    app.run(debug=True)
