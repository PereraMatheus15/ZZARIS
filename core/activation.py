"""Funções de ativação para os neurônios artificiais."""
import math
from typing import Callable


def sigmoid(x: float) -> float:
    """Retorna o valor da função Sigmoid para x."""
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x: float) -> float:
    """Derivada da função Sigmoid em x."""
    sx = sigmoid(x)
    return sx * (1.0 - sx)


def relu(x: float) -> float:
    """Retorna o valor da função ReLU para x."""
    return max(0.0, x)


def relu_derivative(x: float) -> float:
    """Derivada da função ReLU em x."""
    return 1.0 if x > 0 else 0.0


def step(x: float) -> float:
    """Retorna 1.0 se x for não negativo, caso contrário 0.0."""
    return 1.0 if x >= 0.0 else 0.0


def step_derivative(x: float) -> float:
    """Derivada aproximada da função Step."""
    return 1.0 if x == 0.0 else 0.0


def resolve_activation(name: str) -> tuple[Callable[[float], float], Callable[[float], float]]:
    """Resolve strings para funções de ativação e derivadas."""
    name = name.lower()
    if name == "sigmoid":
        return sigmoid, sigmoid_derivative
    if name == "relu":
        return relu, relu_derivative
    if name == "step":
        return step, step_derivative
    return sigmoid, sigmoid_derivative
