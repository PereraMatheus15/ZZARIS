"""Testes unitários para os módulos de memória."""
from memory.long_term import LongTermMemory
from memory.short_term import ShortTermMemory


def test_short_term_memory():
    memory = ShortTermMemory()
    memory.add("pergunta", "resposta")
    assert memory.recall("pergunta") == "resposta"


def test_long_term_memory():
    memory = LongTermMemory()
    memory.add_fact("fato", "valor")
    assert memory.recall("fato") == "valor"
