"""Vision service (adapter). Evita imports rotos y centraliza la visión en el core."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from ..ops.logging import get_logger

log = get_logger("rauli.vision")

@dataclass
class VisionResult:
    ok: bool
    message: str = ""
    data: Optional[dict[str, Any]] = None

class VisionService:
    def __init__(self) -> None:
        log.info("VisionService inicializado (adapter)")
        self._driver = None

    def try_load_experiments_driver(self) -> bool:
        """
        Carga opcional del driver legacy desde experiments/ (si existe en runtime local).
        NOTA: experiments NO es paquete importable por defecto; esto evita dependencia dura.
        """
        return False

    def analyze(self, image_path: str) -> VisionResult:
        # Adapter base (no rompe): devuelve resultado controlado.
        log.info("Vision analyze: %s", image_path)
        return VisionResult(ok=False, message="Vision driver no conectado aún", data={"image_path": image_path})
