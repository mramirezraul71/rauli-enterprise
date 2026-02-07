"""Config estable del motor RAULI (sin secretos dentro del repo)."""
from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class RauliConfig:
    log_level: str = os.getenv("RAULI_LOG_LEVEL", "INFO")
    env: str = os.getenv("RAULI_ENV", "local")
    # Endpoints/keys: siempre por entorno (.env fuera del repo o variables)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
