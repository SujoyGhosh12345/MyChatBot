import os
from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)
client = genai.Client()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini Chatbot</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 600px; 
            margin: auto; 
            padding: 20px; 
            background-color: #f4f4f4;
            display: flex;
            flex-direction: column;
            min-height: 100vh; /* Ensures footer is at bottom of viewport */
        }
        h1 { margin-bottom: 0; }
        #chatbox { 
            height: 400px; 
            border: 1px solid #ccc; 
            padding: 15px; 
            overflow-y: scroll; 
            background-color: #fff;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            flex-grow: 1; /* Allows chatbox to expand */
        }
        .message { 
            padding: 10px 15px; 
            border-radius: 18px; 
            max-width: 80%; 
            word-wrap: break-word;
        }
        .user { 
            align-self: flex-end; 
            background-color: #007bff; 
            color: white; 
        }
        .bot { 
            align-self: flex-start; 
            background-color: #e9e9eb; 
            color: black; 
        }
        #input-area {
            display: flex;
            gap: 10px;
            margin-bottom: 20px; /* Space above footer */
        }
        #user_input {
            flex-grow: 1;
            padding: 10px;
            border-radius: 18px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #28a745;
            color: white;
            border-radius: 18px;
            cursor: pointer;
        }
        /* New Footer Style */
        .footer {
            margin-top: auto; /* Pushes the footer to the bottom */
            text-align: center;
            padding-top: 15px;
            border-top: 1px solid #ccc;
            font-size: 0.8em;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Welcome to my first chatbot</h1>
    <div id="chatbox"></div>
    <div id="input-area">
        <input type="text" id="user_input" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <!-- NEW FOOTER SECTION -->
    <div class="footer">
        Developed by: **Sujoy Ghosh** <br>
        Role: *Software Engineer*
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user_input');
            const message = input.value;
            if (!message) return;

            const chatbox = document.getElementById('chatbox');
            chatbox.innerHTML += `<div class="message user">You: ${message}</div>`;
            input.value = '';

            const thinking = document.createElement('div');
            thinking.classList.add('message', 'bot', 'thinking');
            thinking.innerText = 'Typing...';
            chatbox.appendChild(thinking);
            chatbox.scrollTop = chatbox.scrollHeight;

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                chatbox.removeChild(thinking);
                chatbox.innerHTML += `<div class="message bot">${data.response}</div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
