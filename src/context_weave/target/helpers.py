from __future__ import annotations

from typing import Any
from uuid import uuid4

from context_weave.contracts.target import StandardTarget
from context_weave.errors import ValidationError


def make_target_id(prefix: str = "tgt") -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _normalize_string_list(raw: Any, field_name: str) -> list[str]:
    if raw in ("", None):
        return []
    if not isinstance(raw, list):
        raise ValidationError(f"{field_name} must be a list", field_name=field_name)
    items = [str(item).strip() for item in raw if str(item).strip()]
    if len(items) != len(set(items)):
        raise ValidationError(f"{field_name} contains duplicates", field_name=field_name)
    return items


def normalize_target(raw: dict[str, Any]) -> StandardTarget:
    if not isinstance(raw, dict):
        raise ValidationError("target payload must be an object")
    target = StandardTarget(
        target_kind=str(raw.get("target_kind", "standard_target")),
        target_id=str(raw.get("target_id", "")),
        target_version=str(raw.get("target_version", "v1")),
        schema_ref=str(raw.get("schema_ref", "")),
        required_inputs=_normalize_string_list(raw.get("required_inputs", []), "required_inputs"),
        optional_inputs=_normalize_string_list(raw.get("optional_inputs", []), "optional_inputs"),
        constraints=dict(raw.get("constraints", {})) if isinstance(raw.get("constraints", {}), dict) else {},
        extensions=dict(raw.get("extensions", {})) if isinstance(raw.get("extensions", {}), dict) else {},
    )
    if target.target_kind != "standard_target":
        raise ValidationError("unsupported target_kind", target_kind=target.target_kind)
    if not target.target_id:
        raise ValidationError("target_id must be non-empty")
    if not target.schema_ref:
        raise ValidationError("schema_ref must be non-empty")
    overlap = set(target.required_inputs).intersection(target.optional_inputs)
    if overlap:
        raise ValidationError("required_inputs and optional_inputs must not overlap", overlap=sorted(overlap))
    return target
