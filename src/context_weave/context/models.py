from __future__ import annotations

from typing import Any

from context_weave.contracts.context import (
    SourceRef,
    StandardContext,
    serialize_standard_context,
)
from context_weave.context.helpers import make_context_id, make_trace, make_transform


def make_context(
    *,
    scope: str,
    payload: dict[str, Any],
    context_id: str = "",
    context_version: str = "v1",
    source_kind: str = "",
    source_ref: str = "",
    transform_kind: str = "build",
    transform_notes: str = "",
    derived_from: list[str] | None = None,
) -> StandardContext:
    trace = make_trace(
        source_refs=[SourceRef(source_kind=source_kind, source_ref=source_ref)] if source_kind or source_ref else [],
        derived_from=derived_from or [],
        transforms=[make_transform(transform_kind, transform_notes)],
    )
    return StandardContext(
        context_kind="standard_context",
        context_id=context_id or make_context_id(),
        context_version=context_version,
        scope=scope,
        payload=payload,
        trace=trace,
    )


def serialize_context(context: StandardContext) -> dict[str, Any]:
    return serialize_standard_context(context)
