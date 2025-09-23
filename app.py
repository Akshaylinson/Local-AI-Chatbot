# app.py
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

from flask import Flask, render_template, request, jsonify
from model import ChatModel

# Configure basic logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("local-chatbot")

app = Flask(__name__)

# Initialize ChatModel using LMSTUDIO_MODEL env var if provided
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", None)
chat_model = ChatModel(MODEL_NAME)

@app.route("/")
def index():
    """Render the chat UI (templates/index.html)."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Accepts JSON: { "message": "...", "session_id": "optional" }
    Returns JSON: { "reply": "..." } or { "error": "..." }
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"error": "No message provided."}), 400

    logger.info("Received message for session %s: %s", session_id, message[:200])
    try:
        reply = chat_model.get_reply(message, session_id=session_id)
        logger.info("Reply (len=%d) for session %s", len(reply), session_id)
        return jsonify({"reply": reply})
    except Exception as exc:
        logger.exception("Error generating reply for session %s", session_id)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """
    Clears server-side in-memory session history for the provided session_id.
    Accepts JSON: { "session_id": "default" }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default")
    try:
        ok = chat_model.reset_session(session_id=session_id)
        return jsonify({"status": "ok", "message": f"session {session_id} reset", "result": ok})
    except Exception as exc:
        logger.exception("Error resetting session %s", session_id)
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_flag = os.getenv("FLASK_DEBUG", "True").lower() in ("1", "true", "yes")
    logger.info("Starting Flask app on port %s (debug=%s)", port, debug_flag)
    app.run(host="0.0.0.0", port=port, debug=debug_flag)
