from datetime import datetime
from plugins.base import BasePlugin


class TempoPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Relógio Interno"

    def can_handle(self, prompt: str) -> float:
        if not prompt:
            return 0.0
        text = prompt.lower()
        keywords = [
            "que horas sao",
            "que horas são",
            "hora atual",
            "me diga a hora",
            "qual a hora",
        ]
        for kw in keywords:
            if kw in text:
                return 1.0
        return 0.0

    def execute(self, prompt: str) -> str:
        agora = datetime.now().strftime("%H:%M")
        return f"Meu relógio interno indica que agora são exatamente {agora}."
