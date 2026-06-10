"""Gerencia conjuntos de dados de treinamento para o ZZARIS."""
import json
from typing import Any


def load_examples(path: str) -> list[tuple[list[float], list[float]]]:
    """Carrega exemplos de treinamento de um arquivo JSON."""
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    examples = []
    for case in payload.get("examples", []):
        inputs = [float(value) for value in case.get("inputs", [])]
        outputs = [float(value) for value in case.get("outputs", [])]
        examples.append((inputs, outputs))
    return examples


def save_examples(path: str, examples: list[dict[str, Any]]) -> None:
    """Salva exemplos em formato JSON para referência futura."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"examples": examples}, handle, indent=2, ensure_ascii=False)
