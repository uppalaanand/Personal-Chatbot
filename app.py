from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_input = data.get("message")
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = chat.send_message(user_input)
        return jsonify({'reply': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
