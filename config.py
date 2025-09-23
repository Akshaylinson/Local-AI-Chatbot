
import os
from dataclasses import dataclass

@dataclass
class Config:
    MODEL_NAME: str = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
    DEVICE: str = os.getenv("DEVICE", "auto")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "150"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))
    TOP_K: int = int(os.getenv("TOP_K", "50"))
    PORT: int = int(os.getenv("PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Session settings
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour

config = Config()
