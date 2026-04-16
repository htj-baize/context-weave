from __future__ import annotations

from typing import Any

from context_weave.target.helpers import normalize_target
from context_weave.target.models import make_target, serialize_target


def build_target(
    schema_ref: str,
    required_inputs: list[str] | None = None,
    optional_inputs: list[str] | None = None,
    constraints: dict[str, Any] | None = None,
) -> dict[str, object]:
    target = make_target(
        schema_ref=schema_ref,
        required_inputs=required_inputs,
        optional_inputs=optional_inputs,
        constraints=constraints,
    )
    normalized = normalize_target(serialize_target(target))
    serialized = serialize_target(normalized)
    return {
        "target": serialized,
        "build_summary": {
            "schema_ref": normalized.schema_ref,
            "required_input_count": len(normalized.required_inputs),
            "optional_input_count": len(normalized.optional_inputs),
            "constraint_key_count": len(normalized.constraints),
        },
    }
