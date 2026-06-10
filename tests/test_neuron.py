"""Testes unitários para o neurônio artificial básico."""
from core.activation import sigmoid
from core.neuron import Neuron


def test_neuron_forward():
    neuron = Neuron(2, sigmoid, lambda x: x)
    neuron.weights = [0.5, -0.5]
    neuron.bias = 0.0
    output = neuron.forward([1.0, 1.0])
    assert 0.0 < output < 1.0
