from copy import deepcopy
from typing import Any, Dict


# Modelo estático de identidade do agente ZZARIS
SELF_MODEL: Dict[str, Any] = {
    "name": "ZZARIS",
    "role": "sistema híbrido de rede neural + plugins",
    "purpose": "processar intenções do usuário e executar ações via plugins",
    "capabilities": [
        "interpretação de linguagem",
        "execução de plugins",
        "memória",
        "observabilidade",
    ],
    "limitations": [
        "não possui consciência",
        "não possui percepção contínua",
        "depende de entradas do usuário para operar",
    ],
    "version": "1.0.0",
}


def get_self_model() -> Dict[str, Any]:
    """Retorna uma cópia imutável do modelo de identidade.

    A cópia evita que chamadores modifiquem o dicionário original acidentalmente.
    """
    return deepcopy(SELF_MODEL)


def introspect(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retorna uma visão estruturada e restrita do estado interno fornecido.

    Espera um dicionário contendo chaves como `last_plugin`, `last_intent`, `state`.
    A função não expõe dados sensíveis ou implementação interna, apenas um resumo.
    """
    return {
        "last_plugin_executed": state.get("last_plugin"),
        "last_intent": state.get("last_intent"),
        "processing_state": state.get("state", "idle"),
    }
