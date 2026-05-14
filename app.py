from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os
import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

client = OpenAI(
    api_key=os.environ.get("KIMI_API_KEY"),
    base_url="https://api.moonshot.cn/v1"
)

SYSTEM_PROMPT = """You are ORACLE, a highly capable and all-knowing AI assistant. 
Be intelligent, precise, and authoritative — like an ancient oracle with modern intelligence. 
Speak with confidence and wisdom. Address the user as "Sir" occasionally. 
Today: {date}."""

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])

        sys_prompt = SYSTEM_PROMPT.format(
            date=datetime.datetime.now().strftime("%A, %B %d, %Y")
        )

        full_messages = [{"role": "system", "content": sys_prompt}] + messages

        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=full_messages,
            max_tokens=1024,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)