"""Ponto de entrada principal para iniciar o ZZARIS no terminal."""
from interface.console import ConsoleInterface


def main() -> None:
    console = ConsoleInterface()
    console.run()


if __name__ == "__main__":
    main()
