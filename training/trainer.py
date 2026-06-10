"""Treinador supervisionado simples para o ZZARIS."""
from typing import List

from core.network import NeuralNetwork
from memory.storage import save_json


class Trainer:
    """Executa ciclos de treinamento e avalia a rede neural."""

    def __init__(self, network: NeuralNetwork, examples: list[tuple[list[float], list[float]]]) -> None:
        self.network = network
        self.examples = examples

    # ALTERAÇÃO: Épocas aumentadas para 10000 e taxa de aprendizado reduzida para 0.1
    def train(self, epochs: int = 10000, learning_rate: float = 0.1) -> None:
        """Treina a rede neural usando exemplos rotulados."""
        self.network.train(self.examples, epochs, learning_rate)

    def evaluate(self) -> list[tuple[list[float], list[float], list[float]]]:
        """Avalia a rede nos exemplos e retorna previsões."""
        results = []
        for inputs, outputs in self.examples:
            prediction = self.network.predict(inputs)
            results.append((inputs, outputs, prediction))
        return results

    def save_progress(self, path: str) -> None:
        """Persistência opcional do estado da rede."""
        save_json(path, self.network.to_dict())