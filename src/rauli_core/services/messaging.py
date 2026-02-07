"""Messaging service (adapter). Unifica WhatsApp/Telegram/Email sin dependencias duras."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from ..ops.logging import get_logger

log = get_logger("rauli.messaging")

@dataclass
class MessageResult:
    ok: bool
    message: str = ""
    data: Optional[dict[str, Any]] = None

class MessagingService:
    def __init__(self) -> None:
        log.info("MessagingService inicializado (adapter)")
        self._driver = None

    def send(self, to: str, text: str) -> MessageResult:
        log.info("Messaging send (stub) -> %s", to)
        return MessageResult(ok=False, message="Messaging driver no conectado aún", data={"to": to, "text_preview": (text or "")[:160]})
