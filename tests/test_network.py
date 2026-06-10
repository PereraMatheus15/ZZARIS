"""Testes unitários para a rede neural."""
from core.network import NeuralNetwork


def test_network_forward_shape():
    network = NeuralNetwork([2, 2, 1])
    output = network.predict([0.0, 1.0])
    assert isinstance(output, list)
    assert len(output) == 1
