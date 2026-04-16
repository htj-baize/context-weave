from __future__ import annotations

from context_weave.operate.helpers import normalize_binding
from context_weave.operate.models import build_route_decision


def route_operation(binding: dict[str, object]) -> dict[str, object]:
    normalized = normalize_binding(binding)
    if normalized.missing_required_inputs:
        decision = build_route_decision(
            context_id=normalized.context_id,
            target_id=normalized.target_id,
            route_name="needs_input",
            next_skill="context.build",
            reason="binding is missing required target inputs",
            extensions={
                "missing_required_inputs": normalized.missing_required_inputs,
            },
        )
    else:
        decision = build_route_decision(
            context_id=normalized.context_id,
            target_id=normalized.target_id,
            route_name="ready_for_prepare",
            next_skill="operate.prepare",
            reason="binding already satisfies required target inputs",
            extensions={
                "satisfied_inputs": normalized.satisfied_inputs,
            },
        )
    return {
        "decision": decision,
        "route_summary": {
            "route_name": decision["route_name"],
            "next_skill": decision["next_skill"],
        },
    }
