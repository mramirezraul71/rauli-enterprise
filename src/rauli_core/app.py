"""RAULI CORE Engine - Orquestador principal (estable)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any

from .config import RauliConfig
from .ops.logging import get_logger

from .services.vision import VisionService, VisionResult
from .services.audio import AudioService, AudioResult
from .services.messaging import MessagingService, MessageResult

log = get_logger("rauli.core")

@dataclass
class CoreStatus:
    ok: bool
    message: str = ""
    data: Optional[dict[str, Any]] = None

class RauliCoreApp:
    def __init__(self, config: Optional[RauliConfig] = None) -> None:
        self.config = config or RauliConfig()
        log.info("RAULI CORE inicializando | env=%s", self.config.env)

        # Adapters (stubs seguros)
        self.vision = VisionService()
        self.audio = AudioService()
        self.messaging = MessagingService()

    def health(self) -> CoreStatus:
        return CoreStatus(ok=True, message="RAULI CORE engine OK", data={"env": self.config.env})

    def analyze_image(self, image_path: str) -> VisionResult:
        return self.vision.analyze(image_path)

    def speak(self, text: str) -> AudioResult:
        return self.audio.synthesize(text)

    def notify(self, to: str, text: str) -> MessageResult:
        return self.messaging.send(to=to, text=text)
