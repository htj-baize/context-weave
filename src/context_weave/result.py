from __future__ import annotations

from typing import Any


def ok_result(result: dict[str, Any], **meta: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "ok",
        "result": result,
    }
    if meta:
        payload["meta"] = meta
    return payload

