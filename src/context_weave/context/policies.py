from __future__ import annotations

from context_weave.errors import ValidationError


MERGE_POLICY_REGISTRY: dict[str, str] = {
    "override_right": "Later contexts overwrite earlier payload keys.",
    "override_left": "Earlier contexts keep precedence over later payload keys.",
    "shallow_union": "Merge top-level keys without recursive deep merge behavior.",
}


SLICE_PROFILE_REGISTRY: dict[str, str] = {
    "task_focus": "Generic task-focused sub-context.",
    "source_focus": "Preserve source payload emphasis for downstream operations.",
    "trace_focus": "Preserve trace-facing details for inspection workflows.",
}


def validate_merge_policy(policy: str) -> str:
    normalized = str(policy).strip() or "override_right"
    if normalized not in MERGE_POLICY_REGISTRY:
        raise ValidationError("unsupported merge policy", merge_policy=normalized)
    return normalized


def validate_slice_profile(profile: str) -> str:
    normalized = str(profile).strip() or "task_focus"
    if normalized not in SLICE_PROFILE_REGISTRY:
        raise ValidationError("unsupported slice profile", slice_profile=normalized)
    return normalized
