from __future__ import annotations

from context_weave.context.models import make_context, serialize_context


def build_context(source_kind: str, source_ref: str, build_profile: str = "") -> dict[str, object]:
    context = make_context(
        scope=source_kind,
        payload={
            "source_kind": source_kind,
            "source_ref": source_ref,
            "build_profile": build_profile,
        },
        source_kind=source_kind,
        source_ref=source_ref,
        transform_kind="build",
    )
    return {
        "context": serialize_context(context),
        "build_summary": {
            "source_kind": source_kind,
            "source_ref": source_ref,
            "build_profile": build_profile,
        },
    }
