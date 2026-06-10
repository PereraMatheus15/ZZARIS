# API ZZARIS

## core.neuron.NeuralNetwork

- `__init__(layer_sizes, activation)` - cria uma rede multicamada.
- `feedforward(inputs)` - calcula a saída da rede.
- `predict(inputs)` - retorna a previsão para uma entrada.
- `train(training_data, epochs, learning_rate)` - ajusta pesos com aprendizado supervisionado.

## core.brain.Brain

- `respond(prompt)` - responde a prompts de texto e usa memória.
- `remember_short(key, value)` - salva contexto temporário.
- `remember_long(key, value)` - grava memória persistente.
- `save_memory()` - salva a memória no disco.

## interface.console.ConsoleInterface

- `run()` - inicia a interface de linha de comando.
- `train_model(args)` - treina a rede usando exemplos padrão.
- `remember_fact(args)` - registra um fato na memória de longo prazo.
- `show_memory()` - exibe fatos gravados.
- `status()` - mostra o estado atual do sistema.
