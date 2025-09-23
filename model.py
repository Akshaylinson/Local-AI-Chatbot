# model.py  - LM Studio HTTP wrapper (Option A)
import os
import threading
import requests
from typing import Optional, List, Dict

LM_BASE = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
LM_MODEL = os.getenv("LMSTUDIO_MODEL", "llama-3.2-3b-instruct")
LM_API_KEY = os.getenv("LMSTUDIO_API_KEY", None)
DEFAULT_TIMEOUT = float(os.getenv("LMSTUDIO_TIMEOUT", "60"))
MAX_HISTORY_MESSAGES = int(os.getenv("LMSTUDIO_MAX_HISTORY", "12"))

_histories: Dict[str, List[Dict[str, str]]] = {}
_lock = threading.Lock()
_session = requests.Session()

class ChatModel:
    def __init__(self, model_name: Optional[str] = None):
        self.base = LM_BASE
        self.model = model_name or LM_MODEL
        self.url = f"{self.base}/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        if LM_API_KEY:
            self.headers["Authorization"] = f"Bearer {LM_API_KEY}"

    def get_reply(self, user_text: str, session_id: str = "default",
                  temperature: float = 0.7, max_tokens: int = 256) -> str:
        # append user msg to in-memory history
        with _lock:
            hist = _histories.get(session_id, [])
            hist.append({"role": "user", "content": user_text})
            # build payload using messages
            payload = {
                "model": self.model,
                "messages": hist,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

        # call LM Studio
        try:
            resp = _session.post(self.url, json=payload, headers=self.headers, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise RuntimeError(f"LM Studio request failed: {e}") from e

        # parse response (OpenAI-like shape)
        try:
            assistant_text = data["choices"][0]["message"]["content"].strip()
        except Exception:
            # fallback if shape differs
            if "choices" in data and len(data["choices"]) and "text" in data["choices"][0]:
                assistant_text = data["choices"][0]["text"].strip()
            else:
                raise RuntimeError(f"Unexpected LM Studio response shape: {data}")

        # save assistant reply in history (trim)
        with _lock:
            hist = _histories.get(session_id, [])
            hist.append({"role": "assistant", "content": assistant_text})
            _histories[session_id] = hist[-MAX_HISTORY_MESSAGES:]

        return assistant_text

    def reset_session(self, session_id: str = "default"):
        with _lock:
            if session_id in _histories:
                del _histories[session_id]
        return True

