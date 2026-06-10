"""Módulo de aprendizado com funções de custo e utilitários de treino."""
from typing import List


def mean_squared_error(outputs: List[float], targets: List[float]) -> float:
    """Calcula o erro quadrático médio para previsão e alvo."""
    return sum((o - t) ** 2 for o, t in zip(outputs, targets)) / len(outputs)


def normalize_vector(values: List[float]) -> List[float]:
    """Normaliza um vetor em escala 0-1 para exemplos simples."""
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [0.0 for _ in values]
    return [(value - minimum) / (maximum - minimum) for value in values]
