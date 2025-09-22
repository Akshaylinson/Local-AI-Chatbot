# model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import threading


# Keep a simple in-memory conversation history per session
_conversations = {}
_lock = threading.Lock()


class ChatModel:
def __init__(self, model_name='microsoft/DialoGPT-small', device=None):
self.model_name = model_name
self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Loading model {model_name} on {self.device} ...")
self.tokenizer = AutoTokenizer.from_pretrained(model_name)
self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
print("Model loaded.")


def get_reply(self, user_text, session_id='default', max_length=1000):
# Use a lock to avoid concurrent generation clashes
with _lock:
# prepare input
new_input_ids = self.tokenizer.encode(user_text + self.tokenizer.eos_token, return_tensors='pt').to(self.device)


# append to history
history = _conversations.get(session_id)
if history is None:
bot_input_ids = new_input_ids
else:
bot_input_ids = torch.cat([history, new_input_ids], dim=-1)


# generate
chat_history_ids = self.model.generate(
bot_input_ids,
max_length=bot_input_ids.shape[-1] + 50,
pad_token_id=self.tokenizer.eos_token_id,
do_sample=True,
top_k=50,
top_p=0.95,
temperature=0.7,
)


# store history
_conversations[session_id] = chat_history_ids


# decode only the newly generated tokens
response_ids = chat_history_ids[:, bot_input_ids.shape[-1]:][0]
reply = self.tokenizer.decode(response_ids, skip_special_tokens=True)
return reply


def reset_session(self, session_id='default'):
if session_id in _conversations:
del _conversations[session_id]
