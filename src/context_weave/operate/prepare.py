from __future__ import annotations

from context_weave.errors import ValidationError
from context_weave.operate.helpers import normalize_binding
from context_weave.operate.models import build_operation_request


def prepare_operation(binding: dict[str, object], operation_kind: str = "apply") -> dict[str, object]:
    normalized = normalize_binding(binding)
    resolved_kind = str(operation_kind).strip() or "apply"
    if normalized.missing_required_inputs:
        raise ValidationError(
            "binding is not ready for operation request",
            operation_kind=resolved_kind,
            missing_required_inputs=normalized.missing_required_inputs,
        )
    request = build_operation_request(
        operation_kind=resolved_kind,
        context_id=normalized.context_id,
        target_id=normalized.target_id,
        payload=normalized.projected_payload,
        extensions={
            "target_version": normalized.target_version,
        },
    )
    return {
        "request": request,
        "request_summary": {
            "operation_kind": resolved_kind,
            "payload_key_count": len(normalized.projected_payload),
        },
    }
