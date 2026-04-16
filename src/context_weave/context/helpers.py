from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from context_weave.contracts.context import ContextTrace, SourceRef, StandardContext, TransformRecord
from context_weave.errors import ValidationError


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_context_id(prefix: str = "ctx") -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def make_transform(kind: str, notes: str = "") -> TransformRecord:
    return TransformRecord(kind=kind, timestamp=now_utc_iso(), notes=notes)


def make_trace(
    *,
    source_refs: list[SourceRef] | None = None,
    derived_from: list[str] | None = None,
    transforms: list[TransformRecord] | None = None,
) -> ContextTrace:
    return ContextTrace(
        source_refs=source_refs or [],
        derived_from=derived_from or [],
        transforms=transforms or [],
    )


def normalize_context(raw: dict[str, Any]) -> StandardContext:
    if not isinstance(raw, dict):
        raise ValidationError("context payload must be an object")
    trace_raw = raw.get("trace", {})
    source_refs = []
    for item in trace_raw.get("source_refs", []) if isinstance(trace_raw, dict) else []:
        if isinstance(item, dict):
            source_refs.append(
                SourceRef(
                    source_kind=str(item.get("source_kind", "")),
                    source_ref=str(item.get("source_ref", "")),
                )
            )
    transforms = []
    for item in trace_raw.get("transforms", []) if isinstance(trace_raw, dict) else []:
        if isinstance(item, dict):
            transforms.append(
                TransformRecord(
                    kind=str(item.get("kind", "")),
                    timestamp=str(item.get("timestamp", "")),
                    notes=str(item.get("notes", "")),
                )
            )
    trace = make_trace(
        source_refs=source_refs,
        derived_from=[str(item) for item in trace_raw.get("derived_from", [])] if isinstance(trace_raw, dict) else [],
        transforms=transforms,
    )
    context = StandardContext(
        context_kind=str(raw.get("context_kind", "standard_context")),
        context_id=str(raw.get("context_id", "")),
        context_version=str(raw.get("context_version", "v1")),
        scope=str(raw.get("scope", "")),
        payload=dict(raw.get("payload", {})) if isinstance(raw.get("payload", {}), dict) else {},
        trace=trace,
        extensions=dict(raw.get("extensions", {})) if isinstance(raw.get("extensions", {}), dict) else {},
    )
    if context.context_kind != "standard_context":
        raise ValidationError("unsupported context_kind", context_kind=context.context_kind)
    if not context.context_id:
        raise ValidationError("context_id must be non-empty")
    if not context.scope:
        raise ValidationError("scope must be non-empty")
    return context
