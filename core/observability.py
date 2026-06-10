import os
import json
from datetime import datetime
from typing import Any


LOG_FOLDER = "logs"
LOG_FILENAME_PATTERN = "zzaris_{date}.jsonl"


def _ensure_log_folder() -> None:
    try:
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER, exist_ok=True)
    except Exception:
        pass


def _safe_json_dumps(payload: dict[str, Any]) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False)
    except TypeError:
        safe_payload = {k: (json.dumps(v, ensure_ascii=False) if not isinstance(v, (str, int, float, bool, type(None))) else v)
                        for k, v in payload.items()}
        return json.dumps(safe_payload, ensure_ascii=False)


def log_event(event_type: str, data: dict[str, Any]) -> None:
    """Registra um evento estruturado em JSON Lines de forma resiliente.

    O arquivo é criado em logs/zzaris_YYYY-MM-DD.jsonl e o logger nunca deve romper o fluxo.
    """
    try:
        _ensure_log_folder()
        timestamp = datetime.utcnow().isoformat() + "Z"
        event_record = {
            "timestamp": timestamp,
            "event": event_type,
            "input": data.get("input"),
            "plugin": data.get("plugin"),
            "confidence_score": data.get("confidence_score"),
            "latency_ms": data.get("latency_ms"),
            "result": data.get("result"),
            "metadata": data.get("metadata", {}),
        }
        filename = os.path.join(LOG_FOLDER, LOG_FILENAME_PATTERN.format(date=datetime.utcnow().strftime("%Y-%m-%d")))
        line = _safe_json_dumps(event_record)
        with open(filename, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        pass
