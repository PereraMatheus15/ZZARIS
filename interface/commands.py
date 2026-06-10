"""Comandos da interface de terminal do ZZARIS."""
from typing import Any


class CommandParser:
    """Interpreta comandos de texto simples para controlar a IA."""

    def parse(self, command: str) -> tuple[str, list[str]]:
        text = command.strip()
        if not text:
            return "empty", []
        parts = text.split()
        name = parts[0].lower()
        args = parts[1:]
        return name, args

    def execute(self, name: str, args: list[str], context: Any) -> str:
        if name in {"help", "?"}:
            return self.help_text()
        if name == "exit":
            return "exit"
        if name == "train":
            return context.train_model(args)
        if name == "remember":
            return context.remember_fact(args)
        if name == "memory":
            return context.show_memory()
        if name == "status":
            return context.status()
        return context.handle_prompt(" ".join([name] + args))

    def help_text(self) -> str:
        return (
            "ZZARIS comandos:\n"
            "  help               - mostrar esta ajuda\n"
            "  exit               - encerrar a sessão\n"
            "  train <epochs>     - treinar o núcleo com o dataset padrão\n"
            "  remember <chave> <valor> - aprender um fato para longo prazo\n"
            "  memory             - exibir memória de longo prazo\n"
            "  status             - exibir estado atual do sistema\n"
            "  qualquer outra entrada será usada como prompt de conversa"
        )
