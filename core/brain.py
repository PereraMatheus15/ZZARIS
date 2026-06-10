"""Núcleo cognitivo do ZZARIS que une rede neural, memória e lógica de conversa."""
import json
import os
from datetime import datetime
from typing import Any

from .network import NeuralNetwork
from ..memory.short_term import ShortTermMemory
from ..memory.long_term import LongTermMemory
from ..memory.storage import save_json, load_json
from ..config import KNOWLEDGE_FILE, MEMORY_FILE, LOG_FILE, VERSION


class Brain:
    """Coordena a inteligência artificial, memória e histórico de aprendizado."""

    def __init__(self, network: NeuralNetwork | None = None) -> None:
        self.network = network or NeuralNetwork([2, 4, 1])
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(self._load_long_term())
        self.knowledge = self._load_knowledge()
        self._log("INFO", f"ZZARIS Brain iniciado v{VERSION}")

    def _load_knowledge(self) -> dict[str, Any]:
        if not os.path.exists(KNOWLEDGE_FILE):
            return {}
        return load_json(KNOWLEDGE_FILE)

    def _load_long_term(self) -> dict[str, Any]:
        if not os.path.exists(MEMORY_FILE):
            return {}
        return load_json(MEMORY_FILE)

    def _log(self, level: str, message: str) -> None:
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
        }
        try:
            logs = []
            if os.path.exists(LOG_FILE):
                logs = load_json(LOG_FILE)
            logs.append(payload)
            save_json(LOG_FILE, logs)
        except Exception:
            pass

    def remember_short(self, key: str, value: Any) -> None:
        self.short_term.add(key, value)
        self._log("DEBUG", f"Memória de curto prazo atualizada: {key}")

    def remember_long(self, key: str, value: Any) -> None:
        self.long_term.add_fact(key, value)
        self.long_term.save(MEMORY_FILE)
        self._log("DEBUG", f"Memória de longo prazo armazenada: {key}")

    def respond(self, prompt: str) -> str:
        self._log("INFO", f"Recebido prompt: {prompt}")
        prompt_key = prompt.strip().lower()
        if prompt_key in self.knowledge:
            response = self.knowledge[prompt_key]
            self._log("INFO", f"Resposta proveniente de conhecimento: {prompt_key}")
            return response

        if prompt_key in self.long_term.data:
            return f"Lembro que {self.long_term.data[prompt_key]}"

        if self.network and prompt_key.replace(" ", "").isdigit():
            inputs = [float(d) for d in prompt_key if d.isdigit()][:2]
            prediction = self.network.predict(inputs)
            return f"Previsão de rede neural: {prediction[0]:.3f}"

        return "Ainda estou aprendendo. Por favor, forneça uma explicação ou use comandos específicos."

    def learn_fact(self, key: str, value: str) -> None:
        self.remember_long(key.lower(), value)
        self._log("INFO", f"Aprendido novo fato: {key}")

    def save_memory(self) -> None:
        self.long_term.save(MEMORY_FILE)
        self._log("INFO", "Memória persistente salva.")
