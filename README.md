# ZZARIS

Zero Zone Artificial Reasoning and Intelligence System

## Visão geral

ZZARIS é um projeto de IA modular e expansível criado em Python, com uma rede neural simples implementada manualmente.
A primeira versão não utiliza bibliotecas de IA como TensorFlow ou PyTorch.

## Estrutura do projeto

- `main.py` - ponto de entrada da aplicação.
- `config.py` - configurações e caminhos de dados.
- `core/` - neurônios, rede neural, funções de ativação, aprendizado e cérebro.
- `memory/` - memória de curto e longo prazo com persistência JSON.
- `training/` - dataset e treinador para aprendizado supervisionado.
- `interface/` - console interativo e comandos.
- `data/` - conhecimento, memória e logs.
- `tests/` - testes unitários básicos.
- `docs/` - documentação da arquitetura e roadmap.

## Como usar

1. Abra a pasta do projeto.
2. Execute no terminal:

```bash
python main.py
```

3. Use comandos como `help`, `train 500`, `remember chave valor`, `memory` e `status`.

## Roadmap inicial

- ZZARIS v0.1 → neurônios básicos
- ZZARIS v0.2 → memória persistente
- ZZARIS v0.3 → aprendizado contínuo
- ZZARIS v0.4 → processamento de linguagem
- ZZARIS v0.5 → assistente inteligente
- ZZARIS v1.0 → núcleo cognitivo modular completo

## Testes

Execute:

```bash
pytest
```
