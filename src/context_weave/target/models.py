from __future__ import annotations

from typing import Any

from context_weave.contracts.target import StandardTarget, serialize_standard_target
from context_weave.target.helpers import make_target_id


def make_target(
    *,
    schema_ref: str,
    required_inputs: list[str] | None = None,
    optional_inputs: list[str] | None = None,
    constraints: dict[str, Any] | None = None,
    target_id: str = "",
    target_version: str = "v1",
) -> StandardTarget:
    return StandardTarget(
        target_kind="standard_target",
        target_id=target_id or make_target_id(),
        target_version=target_version,
        schema_ref=schema_ref,
        required_inputs=required_inputs or [],
        optional_inputs=optional_inputs or [],
        constraints=constraints or {},
    )


def serialize_target(target: StandardTarget) -> dict[str, Any]:
    return serialize_standard_target(target)
