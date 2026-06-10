"""Núcleo cognitivo do ZZARIS que une rede neural, memória, lógica de conversa e plugins."""

import os
import math
import re
import importlib
import inspect
from datetime import datetime
from typing import Any, Callable, List
from collections import Counter

from core.network import NeuralNetwork
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.storage import save_json, load_json
from plugins.base import BasePlugin
from config import KNOWLEDGE_FILE, MEMORY_FILE, LOG_FILE, VERSION


class Brain:
    """Coordena a inteligência artificial, memória, histórico de aprendizado e plugins."""

    def __init__(self, network: NeuralNetwork | None = None) -> None:
        self.network = network or NeuralNetwork([2, 4, 1])
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(self._load_long_term())
        self.knowledge = self._load_knowledge()
        
        self.similarity_threshold = 0.3 

        self.plugins: List[BasePlugin] = []
        self._load_plugins()

        self._log("INFO", f"ZZARIS Brain iniciado v{VERSION}")

    # --- Sistema de Plugins Dinâmicos ---
    def _load_plugins(self) -> None:
        """Escaneia a pasta /plugins e instancia todas as classes filhas de BasePlugin."""
        folder = "plugins"
        if not os.path.exists(folder):
            os.makedirs(folder)
            return

        for filename in os.listdir(folder):
            if filename.endswith(".py") and filename != "base.py" and not filename.startswith("__"):
                module_name = f"plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    importlib.reload(module) 
                    
                    for _, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                            self.plugins.append(obj())
                            self._log("INFO", f"Plugin carregado com sucesso: [{obj().name}]")
                except Exception as e:
                    self._log("ERROR", f"Falha ao carregar plugin {filename}: {e}")

    # --- Utilitários de Memória ---
    def remember_short(self, key: str, value: Any) -> None:
        """Salva um dado na memória de curto prazo."""
        self.short_term.add(key, value)
        self._log("DEBUG", f"Memória de curto prazo atualizada: {key}")

    # --- Utilitários Matemáticos ---
    def _get_cosine_similarity(self, str1: str, str2: str) -> float:
        vec1 = Counter(re.findall(r'\w+', str1.lower()))
        vec2 = Counter(re.findall(r'\w+', str2.lower()))
        
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return float(numerator) / denominator if denominator else 0.0

    # --- Persistência e Logs ---
    def _load_knowledge(self) -> dict[str, Any]:
        return load_json(KNOWLEDGE_FILE) if os.path.exists(KNOWLEDGE_FILE) else {}

    def _load_long_term(self) -> dict[str, Any]:
        return load_json(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else {}

    def _log(self, level: str, message: str) -> None:
        payload = {"timestamp": datetime.utcnow().isoformat() + "Z", "level": level, "message": message}
        try:
            logs = load_json(LOG_FILE) if os.path.exists(LOG_FILE) else []
            logs.append(payload)
            save_json(LOG_FILE, logs)
        except Exception: pass

    # --- Handlers de Resposta ---
    def _handle_continuation(self, prompt_key: str) -> str | None:
        if prompt_key in ["continue", "continue falando", "me fale mais", "continue sobre isso"]:
            topic = self.short_term.recall("last_topic")
            if topic and topic in self.knowledge:
                more_info = self.knowledge[topic].get("more_info")
                return more_info if more_info else self.knowledge[topic].get("response", "")
        return None

    def _handle_learning(self, prompt_text: str, prompt_key: str) -> str | None:
        patterns = {
            "nome": r"meu nome é (.*)",
            "cidade": r"eu moro em (.*)",
            "projeto": r"meu projeto é (.*)"
        }
        for key, pattern in patterns.items():
            # CORREÇÃO: Procura no prompt_text original com IGNORECASE para preservar Maiúsculas/Minúsculas
            match = re.search(pattern, prompt_text, re.IGNORECASE)
            if match:
                value = match.group(1).strip(" .!?")
                self.long_term.add_fact(key, value)
                self.long_term.save(MEMORY_FILE)
                
                # CORREÇÃO: Mapeamento de respostas exatas para respeitar a gramática dos testes
                responses = {
                    "nome": f"Entendido. Vou lembrar que seu nome é {value}.",
                    "cidade": f"Entendido. Vou lembrar que você mora em {value}.",
                    "projeto": f"Entendido. Vou lembrar que seu projeto é {value}."
                }
                return responses[key]
        return None

    def _handle_memory_retrieval(self, prompt_key: str) -> str | None:
        queries = {
            "nome": ["qual é meu nome", "qual meu nome", "quem sou eu"],
            "cidade": ["onde eu moro", "onde moro"],
            "projeto": ["qual é meu projeto", "qual meu projeto"]
        }
        for key, phrases in queries.items():
            if any(phrase in prompt_key for phrase in phrases):
                saved = self.long_term.recall(key)
                if not saved:
                    return f"Ainda não sei seu {key}."
                
                # CORREÇÃO: Retornos customizados e idênticos aos assertions dos testes
                responses = {
                    "nome": f"Seu nome é {saved}.",
                    "cidade": f"Você mora em {saved}.",
                    "projeto": f"Seu projeto é {saved}."
                }
                return responses[key]
        return None

    def _handle_knowledge_lookup(self, prompt_key: str) -> str | None:
        best_score = 0
        best_response = None
        best_topic = None

        for topic, data in self.knowledge.items():
            if not isinstance(data, dict): continue
            
            for keyword in data.get("keywords", []):
                score = self._get_cosine_similarity(prompt_key, keyword)
                if score > best_score:
                    best_score = score
                    best_response = data.get("response")
                    best_topic = topic

        if best_score >= self.similarity_threshold:
            self.remember_short("last_topic", best_topic)
            return best_response
        return None

    # --- Orquestrador Principal ---
    def respond(self, prompt: str) -> str:
        prompt_text = prompt.strip()
        prompt_key = prompt_text.lower().strip("?!.,;:")

        # 1. VALIDAÇÃO DE PLUGINS DINÂMICOS
        best_plugin = None
        best_score = 0.0

        for plugin in self.plugins:
            score = plugin.can_handle(prompt_key)
            if score > best_score:
                best_score = score
                best_plugin = plugin

        if best_plugin and best_score >= 0.5:
            self._log("DEBUG", f"Prompt interceptado pelo plugin: {best_plugin.name} (Confiança: {best_score})")
            return best_plugin.execute(prompt_key)

        # 2. HANDLERS COGNITIVOS PADRÃO
        handlers: List[Callable] = [
            lambda p: self._handle_continuation(prompt_key),
            lambda p: self._handle_learning(prompt_text, prompt_key),
            lambda p: self._handle_memory_retrieval(prompt_key),
            lambda p: self._handle_knowledge_lookup(prompt_key)
        ]

        for handler in handlers:
            result = handler(prompt_key)
            if result: 
                return result

        # 3. FALLBACK NEURAL (Cálculos Matemáticos)
        if self.network and prompt_key.replace(" ", "").isdigit():
            inputs = [float(d) for d in prompt_key if d.isdigit()][:2]
            if len(inputs) == 2:
                return f"Previsão de rede neural: {self.network.predict(inputs)[0]:.3f}"

        # CORREÇÃO: Adicionada a palavra "específicos" exigida pelo test_brain_knowledge_no_match
        return "Ainda estou aprendendo. Por favor, forneça uma explicação ou use comandos específicos."