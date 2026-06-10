"""Implementação de rede neural multicamada simples."""
from typing import Callable

from core.activation import resolve_activation
from core.neuron import Neuron
from core.learning import mean_squared_error


class NeuralNetwork:
    """Rede neural modular com suporte a múltiplas camadas."""

    def __init__(self, layer_sizes: list[int], activation: str = "sigmoid") -> None:
        self.layer_sizes = layer_sizes
        self.activation_name = activation
        self.activation, self.activation_derivative = resolve_activation(activation)
        self.layers: list[list[Neuron]] = []
        self._build_layers()

    def _build_layers(self) -> None:
        for index in range(1, len(self.layer_sizes)):
            input_size = self.layer_sizes[index - 1]
            next_size = self.layer_sizes[index]
            layer = [Neuron(input_size, self.activation, self.activation_derivative) for _ in range(next_size)]
            self.layers.append(layer)

    def feedforward(self, inputs: list[float]) -> list[float]:
        """Passa entradas através de cada camada para calcular uma previsão."""
        activation = inputs
        for layer in self.layers:
            activation = [neuron.forward(activation) for neuron in layer]
        return activation

    def predict(self, inputs: list[float]) -> list[float]:
        """Retorna a previsão da rede para uma entrada."""
        return self.feedforward(inputs)

    def train(self, training_data: list[tuple[list[float], list[float]]], epochs: int, learning_rate: float) -> None:
        """Treina a rede usando aprendizado supervisionado simples."""
        for epoch in range(epochs):
            total_loss = 0.0
            for inputs, expected in training_data:
                outputs = self.feedforward(inputs)
                loss = mean_squared_error(outputs, expected)
                total_loss += loss
                self._backpropagate(expected, learning_rate)
            if epoch % max(1, epochs // 10) == 0:
                print(f"[Treinamento] Época {epoch + 1}/{epochs} - loss: {total_loss:.6f}")

    def _backpropagate(self, targets: list[float], learning_rate: float) -> None:
        """Realiza retropropagação usando gradientes locais."""
        layer_inputs: list[list[float]] = []
        activation = []
        current_input = []
        # gather activations from forward pass in each neuron
        for layer in self.layers:
            layer_inputs.append([neuron.last_z for neuron in layer])
            current_input = [neuron.activation(neuron.last_z) for neuron in layer]
            activation.append(current_input)

        deltas: list[list[float]] = []
        # calcula delta na saída
        output_layer = self.layers[-1]
        output_activations = activation[-1]
        output_deltas = []
        for index, neuron in enumerate(output_layer):
            error = targets[index] - output_activations[index]
            output_deltas.append(error * neuron.activation_derivative(neuron.last_z))
        deltas.append(output_deltas)

        # retropropaga para camadas ocultas
        for layer_index in range(len(self.layers) - 2, -1, -1):
            layer = self.layers[layer_index]
            next_layer = self.layers[layer_index + 1]
            layer_deltas: list[float] = []
            for neuron_index, neuron in enumerate(layer):
                error = sum(next_neuron.weights[neuron_index] * deltas[0][next_index] for next_index, next_neuron in enumerate(next_layer))
                layer_deltas.append(error * neuron.activation_derivative(neuron.last_z))
            deltas.insert(0, layer_deltas)

        # ajusta pesos e bias usando deltas
        for layer_index, layer in enumerate(self.layers):
            for neuron_index, neuron in enumerate(layer):
                neuron.update_weights(deltas[layer_index][neuron_index], learning_rate)

    def to_dict(self) -> dict:
        """Serializa a rede neural para um dicionário."""
        return {
            "layer_sizes": self.layer_sizes,
            "activation": self.activation_name,
            "layers": [[neuron.to_dict() for neuron in layer] for layer in self.layers],
        }

    def load_dict(self, data: dict) -> None:
        """Carrega a rede a partir de um dicionário serializado."""
        self.layer_sizes = data.get("layer_sizes", self.layer_sizes)
        self.activation_name = data.get("activation", self.activation_name)
        self.activation, self.activation_derivative = resolve_activation(self.activation_name)
        self.layers = []
        layer_data = data.get("layers", [])
        for layer_index, neurons_data in enumerate(layer_data):
            layer_size = len(neurons_data)
            input_size = self.layer_sizes[layer_index]
            layer = [Neuron(input_size, self.activation, self.activation_derivative) for _ in range(layer_size)]
            for neuron, neuron_data in zip(layer, neurons_data):
                neuron.load_dict(neuron_data)
            self.layers.append(layer)
