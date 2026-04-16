from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

STANDARD_TARGET_REQUIRED_FIELDS = [
    "target_kind",
    "target_id",
    "target_version",
    "schema_ref",
    "required_inputs",
    "optional_inputs",
    "constraints",
]

STANDARD_TARGET_STABLE_FIELDS = STANDARD_TARGET_REQUIRED_FIELDS + ["extensions"]
TARGET_BINDING_REQUIRED_FIELDS = [
    "binding_kind",
    "context_id",
    "target_id",
    "target_version",
    "satisfied_inputs",
    "missing_required_inputs",
    "projected_payload",
]
TARGET_BINDING_STABLE_FIELDS = TARGET_BINDING_REQUIRED_FIELDS + ["extensions"]


@dataclass
class StandardTarget:
    target_kind: str
    target_id: str
    target_version: str
    schema_ref: str
    required_inputs: list[str] = field(default_factory=list)
    optional_inputs: list[str] = field(default_factory=list)
    constraints: dict[str, Any] = field(default_factory=dict)
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass
class TargetBinding:
    binding_kind: str
    context_id: str
    target_id: str
    target_version: str
    satisfied_inputs: list[str] = field(default_factory=list)
    missing_required_inputs: list[str] = field(default_factory=list)
    projected_payload: dict[str, Any] = field(default_factory=dict)
    extensions: dict[str, Any] = field(default_factory=dict)


def serialize_standard_target(target: StandardTarget) -> dict[str, Any]:
    return asdict(target)


def serialize_target_binding(binding: TargetBinding) -> dict[str, Any]:
    return asdict(binding)
