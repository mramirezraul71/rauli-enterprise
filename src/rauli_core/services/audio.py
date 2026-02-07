"""Audio service (adapter). No rompe: stub estable para integrar TTS luego."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from ..ops.logging import get_logger

log = get_logger("rauli.audio")

@dataclass
class AudioResult:
    ok: bool
    message: str = ""
    data: Optional[dict[str, Any]] = None

class AudioService:
    def __init__(self) -> None:
        log.info("AudioService inicializado (adapter)")
        self._driver = None

    def synthesize(self, text: str) -> AudioResult:
        log.info("Audio synthesize (stub): %s", (text or "")[:80])
        return AudioResult(ok=False, message="Audio driver no conectado aún", data={"text_preview": (text or "")[:120]})
