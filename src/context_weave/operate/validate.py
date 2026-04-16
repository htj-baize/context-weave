from __future__ import annotations

from context_weave.operate.helpers import normalize_binding
from context_weave.operate.models import build_validation_report


def validate_operation(binding: dict[str, object]) -> dict[str, object]:
    normalized = normalize_binding(binding)
    ready = len(normalized.missing_required_inputs) == 0
    warnings: list[str] = []
    if not normalized.projected_payload:
        warnings.append("projected_payload is empty")
    report = build_validation_report(
        context_id=normalized.context_id,
        target_id=normalized.target_id,
        ready=ready,
        missing_required_inputs=normalized.missing_required_inputs,
        satisfied_inputs=normalized.satisfied_inputs,
        warnings=warnings,
        extensions={
            "projected_key_count": len(normalized.projected_payload),
        },
    )
    return {
        "report": report,
        "validation_summary": {
            "ready": ready,
            "missing_required_count": len(normalized.missing_required_inputs),
            "warning_count": len(warnings),
        },
    }
