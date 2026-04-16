from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

STANDARD_CONTEXT_REQUIRED_FIELDS = [
    "context_kind",
    "context_id",
    "context_version",
    "scope",
    "payload",
    "trace",
]

STANDARD_CONTEXT_STABLE_FIELDS = STANDARD_CONTEXT_REQUIRED_FIELDS + ["extensions"]


@dataclass
class SourceRef:
    source_kind: str
    source_ref: str


@dataclass
class TransformRecord:
    kind: str
    timestamp: str = ""
    notes: str = ""


@dataclass
class ContextTrace:
    source_refs: list[SourceRef] = field(default_factory=list)
    derived_from: list[str] = field(default_factory=list)
    transforms: list[TransformRecord] = field(default_factory=list)


@dataclass
class StandardContext:
    context_kind: str
    context_id: str
    context_version: str
    scope: str
    payload: dict[str, Any]
    trace: ContextTrace
    extensions: dict[str, Any] = field(default_factory=dict)


def serialize_standard_context(context: StandardContext) -> dict[str, Any]:
    return asdict(context)
