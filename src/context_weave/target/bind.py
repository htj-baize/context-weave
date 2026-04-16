from __future__ import annotations

from context_weave.context.helpers import normalize_context
from context_weave.contracts.target import TargetBinding, serialize_target_binding
from context_weave.target.helpers import normalize_target


def bind_target(context: dict[str, object], target: dict[str, object]) -> dict[str, object]:
    normalized_context = normalize_context(context)
    normalized_target = normalize_target(target)
    available = normalized_context.payload
    projected_keys = normalized_target.required_inputs + [
        item for item in normalized_target.optional_inputs if item not in normalized_target.required_inputs
    ]
    projected_payload = {key: available[key] for key in projected_keys if key in available}
    missing_required_inputs = [key for key in normalized_target.required_inputs if key not in available]
    satisfied_inputs = [key for key in normalized_target.required_inputs if key in available]
    satisfied_inputs.extend(
        [key for key in normalized_target.optional_inputs if key in available and key not in satisfied_inputs]
    )
    binding = TargetBinding(
        binding_kind="target_binding",
        context_id=normalized_context.context_id,
        target_id=normalized_target.target_id,
        target_version=normalized_target.target_version,
        satisfied_inputs=satisfied_inputs,
        missing_required_inputs=missing_required_inputs,
        projected_payload=projected_payload,
        extensions={
            "schema_ref": normalized_target.schema_ref,
        },
    )
    return {
        "binding": serialize_target_binding(binding),
        "binding_summary": {
            "schema_ref": normalized_target.schema_ref,
            "missing_required_count": len(missing_required_inputs),
            "projected_key_count": len(projected_payload),
            "ready": len(missing_required_inputs) == 0,
        },
    }
