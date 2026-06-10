"""Definição de neurônio artificial básico."""
import random
from typing import Callable


class Neuron:
    """Representa um neurônio artificial com pesos, bias e função de ativação."""

    def __init__(
        self,
        input_size: int,
        activation: Callable[[float], float],
        activation_derivative: Callable[[float], float],
    ) -> None:
        self.weights: list[float] = [random.uniform(-1.0, 1.0) for _ in range(input_size)]
        self.bias: float = random.uniform(-1.0, 1.0)
        self.activation = activation
        self.activation_derivative = activation_derivative
        self.last_input: list[float] = []
        self.last_z: float = 0.0

    def forward(self, inputs: list[float]) -> float:
        """Computa a saída do neurônio para um conjunto de entradas."""
        self.last_input = inputs
        self.last_z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
        return self.activation(self.last_z)

    def update_weights(self, gradient: float, learning_rate: float) -> None:
        """Ajusta pesos e bias com base no gradiente calculado."""
        for index, value in enumerate(self.last_input):
            self.weights[index] += learning_rate * gradient * value
        self.bias += learning_rate * gradient

    def to_dict(self) -> dict:
        """Serializa o neurônio para JSON."""
        return {
            "weights": self.weights,
            "bias": self.bias,
        }

    def load_dict(self, data: dict) -> None:
        """Carrega o estado do neurônio a partir de um dicionário."""
        self.weights = data.get("weights", self.weights)
        self.bias = data.get("bias", self.bias)
