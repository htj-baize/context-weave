from __future__ import annotations

from pathlib import Path
import json

from context_weave.context.helpers import normalize_context
from context_weave.context.models import serialize_context
from context_weave.errors import InvalidArgumentError, NotFoundError


def read_context(context_ref: str) -> dict[str, object]:
    path = Path(context_ref)
    if not path.exists():
        raise NotFoundError("context reference does not exist", context_ref=context_ref)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise InvalidArgumentError("context reference did not contain valid JSON", context_ref=context_ref) from error
    context_payload = payload.get("context", payload) if isinstance(payload, dict) else payload
    normalized = normalize_context(context_payload)
    return {
        "context": serialize_context(normalized),
        "context_metadata": {
            "context_ref": str(path),
            "source_kind": "snapshot_wrapper" if isinstance(payload, dict) and "context" in payload else "raw_context",
        },
    }
