from __future__ import annotations

from typing import Any

from context_weave.context.helpers import normalize_context
from context_weave.contracts.trace import serialize_context_trace


def trace_context(context: dict[str, Any]) -> dict[str, object]:
    normalized = normalize_context(context)
    trace = serialize_context_trace(normalized.trace)
    return {
        "trace": trace,
        "lineage_summary": {
            "context_id": normalized.context_id,
            "derived_from_count": len(trace.get("derived_from", [])),
            "transform_count": len(trace.get("transforms", [])),
        },
    }
