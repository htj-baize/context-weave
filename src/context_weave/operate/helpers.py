from __future__ import annotations

from typing import Any

from context_weave.contracts.target import TargetBinding
from context_weave.errors import ValidationError


def normalize_binding(raw: dict[str, Any]) -> TargetBinding:
    if not isinstance(raw, dict):
        raise ValidationError("binding payload must be an object")
    binding = TargetBinding(
        binding_kind=str(raw.get("binding_kind", "target_binding")),
        context_id=str(raw.get("context_id", "")),
        target_id=str(raw.get("target_id", "")),
        target_version=str(raw.get("target_version", "v1")),
        satisfied_inputs=[str(item) for item in raw.get("satisfied_inputs", [])] if isinstance(raw.get("satisfied_inputs", []), list) else [],
        missing_required_inputs=[str(item) for item in raw.get("missing_required_inputs", [])] if isinstance(raw.get("missing_required_inputs", []), list) else [],
        projected_payload=dict(raw.get("projected_payload", {})) if isinstance(raw.get("projected_payload", {}), dict) else {},
        extensions=dict(raw.get("extensions", {})) if isinstance(raw.get("extensions", {}), dict) else {},
    )
    if binding.binding_kind != "target_binding":
        raise ValidationError("unsupported binding_kind", binding_kind=binding.binding_kind)
    if not binding.context_id:
        raise ValidationError("context_id must be non-empty")
    if not binding.target_id:
        raise ValidationError("target_id must be non-empty")
    return binding
