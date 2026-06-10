"""Console interativo simples para o ZZARIS."""
from core.brain import Brain
from training.dataset import load_examples
from training.trainer import Trainer
from config import EXAMPLES_FILE, MEMORY_FILE
from interface.commands import CommandParser


class ConsoleInterface:
    """Interface de linha de comando para conversar com o ZZARIS."""

    def __init__(self) -> None:
        self.brain = Brain()
        self.parser = CommandParser()
        self.examples = load_examples(EXAMPLES_FILE)

    def run(self) -> None:
        print("ZZARIS - Zero Zone Artificial Reasoning and Intelligence System")
        print("Digite 'help' para ver comandos. Ctrl+C para sair.")
        while True:
            try:
                command = input("ZZARIS> ")
                name, args = self.parser.parse(command)
                output = self.parser.execute(name, args, self)
                if output == "exit":
                    print("Encerrando ZZARIS. Até logo!")
                    break
                print(output)
            except KeyboardInterrupt:
                print("\nSessão finalizada pelo usuário.")
                break
            except Exception as error:
                print(f"Erro: {error}")

    def train_model(self, args: list[str]) -> str:
        epochs = int(args[0]) if args else 500
        trainer = Trainer(self.brain.network, self.examples)
        trainer.train(epochs=epochs)
        return f"Treinamento concluído com {epochs} épocas."

    def remember_fact(self, args: list[str]) -> str:
        if len(args) < 2:
            return "Uso: remember <chave> <valor>"
        key = args[0].lower()
        value = " ".join(args[1:])
        self.brain.learn_fact(key, value)
        return f"Fato aprendido: {key} -> {value}"

    def show_memory(self) -> str:
        if not self.brain.long_term.data:
            return "Memória de longo prazo está vazia."
        return "\n".join(f"{k}: {v}" for k, v in self.brain.long_term.data.items())

    def status(self) -> str:
        return (
            f"Versão: {self.brain.network.activation_name}\n"
            f"Camadas: {self.brain.network.layer_sizes}\n"
            f"Exemplos carregados: {len(self.examples)}\n"
            f"Memória longa: {len(self.brain.long_term.data)} itens"
        )

    def handle_prompt(self, prompt: str) -> str:
        if prompt.strip().lower().startswith("remember:"):
            parts = prompt.split(":", 1)
            if len(parts) == 2:
                key_value = parts[1].strip().split("=", 1)
                if len(key_value) == 2:
                    self.brain.learn_fact(key_value[0].strip().lower(), key_value[1].strip())
                    return "Fato adicionado à memória de longo prazo."
        return self.brain.respond(prompt)
