from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

from context_weave.context.helpers import normalize_context
from context_weave.contracts.snapshot import (
    ContextSnapshotMetadata,
    ContextSnapshotRef,
    serialize_context_snapshot,
)


def snapshot_context(context: dict[str, object], output_path: str = "", label: str = "") -> dict[str, object]:
    normalized = normalize_context(context)
    target = Path(output_path) if output_path else Path(".tmp/context.snapshot.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"context": context}, ensure_ascii=False, indent=2), encoding="utf-8")
    snapshot = ContextSnapshotRef(
        snapshot_ref=str(target),
        snapshot_metadata=ContextSnapshotMetadata(
            context_id=normalized.context_id,
            label=label,
            created_at=datetime.now(timezone.utc).isoformat(),
        ),
    )
    return serialize_context_snapshot(snapshot)
