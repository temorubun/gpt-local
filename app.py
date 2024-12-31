from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatGPT UI</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #1E1E1E;
                color: #FFFFFF;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                width: 100%;
                max-width: 600px;
                background-color: #2D2D2D;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .header h1 {
                font-size: 24px;
            }
            .chat-box {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
                background-color: #1E1E1E;
            }
            .chat {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .message {
                max-width: 80%;
                padding: 10px;
                border-radius: 10px;
                word-wrap: break-word;
            }
            .message.user {
                align-self: flex-end;
                background-color: #007BFF;
                color: white;
            }
            .message.gpt {
                align-self: flex-start;
                background-color: #333;
                color: white;
            }
            .input-area {
                display: flex;
                gap: 10px;
            }
            .input-area textarea {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #444;
                border-radius: 8px;
                background-color: #333;
                color: #FFF;
            }
            .input-area button {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background-color: #007BFF;
                color: white;
                cursor: pointer;
            }
            .input-area button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>What can I help with?</h1>
            </div>
            <div class="chat-box" id="chat-box">
                <div class="chat" id="chat"></div>
            </div>
            <div class="input-area">
                <textarea id="user-input" placeholder="Message ChatGPT" onkeydown="handleEnter(event)"></textarea>
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            async function sendMessage() {
                const userInput = document.getElementById('user-input').value;
                if (!userInput) return;

                const chat = document.getElementById('chat');
                const userMessage = document.createElement('div');
                userMessage.className = 'message user';
                userMessage.textContent = userInput;
                chat.appendChild(userMessage);

                document.getElementById('user-input').value = '';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userInput })
                });

                const data = await response.json();
                const gptMessage = document.createElement('div');
                gptMessage.className = 'message gpt';
                gptMessage.textContent = data.reply || `Error: ${data.error}`;
                chat.appendChild(gptMessage);

                chat.scrollTop = chat.scrollHeight;
            }

            function handleEnter(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
