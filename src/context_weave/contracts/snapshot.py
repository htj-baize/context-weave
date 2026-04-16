from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ContextSnapshotMetadata:
    context_id: str
    label: str = ""
    created_at: str = ""


@dataclass
class ContextSnapshotRef:
    snapshot_ref: str
    snapshot_metadata: ContextSnapshotMetadata


def serialize_context_snapshot(snapshot: ContextSnapshotRef) -> dict[str, Any]:
    return asdict(snapshot)
