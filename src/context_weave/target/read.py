from __future__ import annotations

import json
from pathlib import Path

from context_weave.errors import InvalidArgumentError, NotFoundError
from context_weave.target.helpers import normalize_target
from context_weave.target.models import serialize_target


def read_target(target_ref: str) -> dict[str, object]:
    path = Path(target_ref)
    if not path.exists():
        raise NotFoundError("target reference does not exist", target_ref=target_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise InvalidArgumentError("target reference did not contain valid JSON", target_ref=target_ref) from error
    target_payload = payload.get("target", payload) if isinstance(payload, dict) else payload
    normalized = normalize_target(target_payload)
    return {
        "target": serialize_target(normalized),
        "target_metadata": {
            "target_ref": str(path),
            "source_kind": "wrapper" if isinstance(payload, dict) and "target" in payload else "raw_target",
        },
    }
