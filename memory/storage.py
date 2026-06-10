"""Operações de E/S para armazenamento JSON do ZZARIS."""
import json
from typing import Any


def load_json(path: str) -> Any:
    """Carrega um arquivo JSON de disco."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: str, data: Any) -> None:
    """Salva um objeto Python em formato JSON."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
