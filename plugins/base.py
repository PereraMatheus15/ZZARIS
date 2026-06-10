from typing import Any


class BasePlugin:
    """Classe base para plugins de habilidade.

    Plugins devem herdar desta classe e sobrescrever `name`, `can_handle` e `execute`.
    """

    @property
    def name(self) -> str:
        return "BasePlugin"

    def can_handle(self, prompt: str) -> float:
        """Retorna um score (0.0-1.0) indicando quão apropriado o plugin é para lidar com o `prompt`.

        Valor padrão 0.0 (não lida).
        """
        return 0.0

    def execute(self, prompt: str) -> str:
        """Executa a ação do plugin e retorna a resposta como string.

        Valor padrão: string vazia.
        """
        return ""
