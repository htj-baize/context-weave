from __future__ import annotations

from typing import Any

from context_weave.context.helpers import normalize_context
from context_weave.context.models import make_context, serialize_context
from context_weave.context.policies import validate_merge_policy


def merge_contexts(contexts: list[dict[str, Any]], merge_policy: str = "override_right") -> dict[str, object]:
    resolved_policy = validate_merge_policy(merge_policy)
    merged_payload: dict[str, Any] = {}
    merged_ids: list[str] = []
    normalized_contexts = [normalize_context(item) for item in contexts]
    ordered_contexts = normalized_contexts if resolved_policy != "override_left" else list(reversed(normalized_contexts))
    for context in ordered_contexts:
        merged_ids.append(context.context_id)
        merged_payload.update(context.payload)
    if resolved_policy == "shallow_union":
        merged_ids = [item.context_id for item in normalized_contexts]
    merged = make_context(
        scope="mixed",
        payload=merged_payload,
        transform_kind="merge",
        transform_notes=resolved_policy,
        derived_from=merged_ids,
    )
    return {
        "context": serialize_context(merged),
        "merge_summary": {
            "merge_policy": resolved_policy,
            "input_count": len(contexts),
        },
    }
