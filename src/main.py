"""Entrypoint CLI mínimo para validar el motor."""
from __future__ import annotations
from rauli_core.app import RauliCoreApp

def main() -> None:
    app = RauliCoreApp()
    print(app.health())

if __name__ == "__main__":
    main()
