# app.py
import os
from flask import Flask, render_template, request, jsonify
from model import ChatModel


app = Flask(__name__)


# Load model once at startup
MODEL_NAME = os.getenv('MODEL_NAME', 'microsoft/DialoGPT-small')
chat_model = ChatModel(MODEL_NAME)


@app.route('/')
def index():
return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def api_chat():
data = request.json or {}
message = data.get('message', '')
if not message:
return jsonify({'error': 'No message provided.'}), 400


# Provide a simple session-based conversation ID
session_id = data.get('session_id', 'default')


try:
reply = chat_model.get_reply(message, session_id=session_id)
return jsonify({'reply': reply})
except Exception as e:
return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)
