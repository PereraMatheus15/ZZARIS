"""Memória persistente do ZZARIS baseada em armazenamento JSON."""
from typing import Any

from memory.storage import save_json


class LongTermMemory:
    """Modelo de memória de longo prazo confiável e persistente."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = data or {}

    def add_fact(self, key: str, value: Any) -> None:
        self.data[key] = value

    def recall(self, key: str) -> Any:
        return self.data.get(key)

    def save(self, path: str) -> None:
        save_json(path, self.data)
