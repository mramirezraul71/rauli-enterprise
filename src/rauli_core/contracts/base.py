"""Contracts base del motor RAULI (interfaces estables)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol, Optional

@dataclass(frozen=True)
class ServiceResult:
    ok: bool
    message: str = ""
    data: Optional[dict[str, Any]] = None

class VisionContract(Protocol):
    def analyze(self, image_path: str) -> ServiceResult: ...

class AudioContract(Protocol):
    def synthesize(self, text: str) -> ServiceResult: ...

class MessagingContract(Protocol):
    def send(self, to: str, text: str) -> ServiceResult: ...
