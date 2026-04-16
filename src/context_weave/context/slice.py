from __future__ import annotations

from typing import Any

from context_weave.context.helpers import normalize_context
from context_weave.context.models import make_context, serialize_context
from context_weave.context.policies import validate_slice_profile


def slice_context(context: dict[str, Any], slice_profile: str) -> dict[str, object]:
    normalized = normalize_context(context)
    resolved_profile = validate_slice_profile(slice_profile)
    payload = normalized.payload
    sliced = make_context(
        scope="task_slice",
        payload={
            "slice_profile": resolved_profile,
            "source_payload": payload,
        },
        transform_kind="slice",
        transform_notes=resolved_profile,
        derived_from=[normalized.context_id],
    )
    return {
        "context": serialize_context(sliced),
        "slice_summary": {
            "slice_profile": resolved_profile,
        },
    }
