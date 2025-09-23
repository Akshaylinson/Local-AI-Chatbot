.

📚 Local AI Chatbot (Flask + LM Studio)

A lightweight web-based chatbot built with Python (Flask) and powered by LM Studio, which allows running large language models locally without relying on external cloud APIs.

This project demonstrates how to integrate a web UI with a local LLM backend via LM Studio’s OpenAI-compatible REST API. It is designed for developers, researchers, and hobbyists who want to experiment with local AI chatbots in a controlled environment.

🚀 Features

Local-first AI: No external API calls — your data never leaves your machine.

Flask-powered backend: Simple, extensible Python server with REST endpoints.

Bootstrap-based UI: Clean and responsive chat interface in templates/index.html.

Session management: Maintains per-user chat history (in-memory).

Configurable: Easily change model, server base URL, or parameters via .env.

Lightweight stack: Only Flask, requests, and python-dotenv are required.

Reset sessions: Clear chat history per user with /api/reset.

🏗️ Tech Stack

Backend: Python 3.9+ with Flask

Frontend: HTML (Bootstrap, inline JS)

LLM Runtime: LM Studio
 — local server mode

Deployment: Works locally or on LAN; can be containerized or run behind Nginx

📂 Project Structure
local-chatbot/
├── .venv/                 # Python virtual environment
├── .env                   # Environment variables (ignored in Git)
├── app.py                 # Flask server entrypoint
├── model.py               # ChatModel wrapper (LM Studio HTTP API)
├── templates/
│   └── index.html         # Chat UI (Bootstrap + JS)
├── static/                # Optional assets (CSS/JS if separated)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

⚙️ Setup Instructions
1. Clone repository
git clone https://github.com/your-username/local-chatbot.git
cd local-chatbot

2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\Activate.ps1 # Windows PowerShell

3. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt


Example requirements.txt:

Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0

4. Configure environment

Create .env in the project root:

LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=llama-3.2-3b-instruct
LMSTUDIO_TIMEOUT=60
LMSTUDIO_MAX_HISTORY=12
PORT=5000
FLASK_DEBUG=True

5. Start LM Studio server

Open LM Studio → Developer → Start Local Server

Or use CLI:

lms server start --port 1234


Confirm with curl:

curl -X POST "http://localhost:1234/v1/chat/completions" \
 -H "Content-Type: application/json" \
 -d '{"model":"llama-3.2-3b-instruct","messages":[{"role":"user","content":"Hello!"}]}'

6. Run the Flask app
python app.py


Visit: http://127.0.0.1:5000

🖥️ API Endpoints
GET /

Returns the web-based chat UI.

POST /api/chat

Send a user message to the model.
Request JSON:

{
  "message": "Explain AI in simple terms",
  "session_id": "demo"
}


Response JSON:

{
  "reply": "AI is like teaching a computer to learn from examples..."
}

POST /api/reset

Clear history for a given session.
Request JSON:

{ "session_id": "demo" }


Response JSON:

{ "status": "ok", "message": "session demo reset" }

🐞 Troubleshooting
Issue	Solution
Import "flask" could not be resolved	Ensure .venv is selected in VS Code: Ctrl+Shift+P → Python: Select Interpreter
Connection refused to localhost:1234	Start LM Studio local server (Developer → Start Local Server)
Unexpected response shape	Check LMSTUDIO_MODEL in .env matches the model ID in LM Studio
Memory error (torch/transformers)	Remove unused HF code: pip uninstall torch transformers (not needed for LM Studio mode)
🔮 Future Enhancements

Streaming responses: Stream tokens to the UI with SSE/WebSockets.

Persistent storage: Save chat history to SQLite or Redis instead of memory.

Multi-user support: Unique session management per user ID.

Deployment: Containerize with Docker, serve with Gunicorn + Nginx.

Plugins: Extend with tools (search, DB queries) via LM Studio function-calling.

🤝 Contributing

Contributions welcome!

Fork this repo

Create a feature branch

Submit a pull request with clear commit messages
