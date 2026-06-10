"""Armazenamento de curto prazo para manter o contexto de conversas recentes."""
from typing import Any


class ShortTermMemory:
    """Modelo simples de memória de curto prazo, temporal e de sessão."""

    def __init__(self) -> None:
        self.memory: dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        self.memory[key] = value

    def recall(self, key: str) -> Any:
        return self.memory.get(key)

    def clear(self) -> None:
        self.memory.clear()

    def items(self) -> list[tuple[str, Any]]:
        return list(self.memory.items())
