# Arquitetura ZZARIS

ZZARIS foi projetado como um sistema modular de inteligência artificial que separa responsabilidades em camadas claras.

## Componentes principais

- `main.py` - Ponto de entrada do aplicativo.
- `config.py` - Configuração global do sistema, caminhos e parâmetros.
- `core/` - Núcleo da IA com neurônios, rede neural, funções de ativação, aprendizado e cérebro.
- `memory/` - Memória de curto e longo prazo com persistência JSON.
- `training/` - Dataset e treinador para aprendizado supervisionado.
- `interface/` - Interface de console e comandos de interação.
- `data/` - Armazenamento JSON para conhecimento, memória e logs.

## Fluxo de funcionamento

1. `main.py` inicializa `ConsoleInterface`.
2. `ConsoleInterface` instancia `Brain` e carrega exemplos de treino.
3. `Brain` carrega conhecimento estático e memória persistente.
4. A rede neural processa entradas numéricas e a memória responde a conhecimentos salvos.
5. Logs são gravados em `data/logs.json`.

## Princípios de design

- **SOLID**: cada módulo tem responsabilidade única.
- **Modularidade**: os pacotes podem ser expandidos separadamente.
- **Extensibilidade**: suporte para novas camadas, NLP, visão e controle de dispositivos.
