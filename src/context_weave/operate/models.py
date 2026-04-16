from __future__ import annotations

from uuid import uuid4

from context_weave.contracts.operate import (
    OperationRequest,
    RouteDecision,
    ValidationReport,
    serialize_operation_request,
    serialize_route_decision,
    serialize_validation_report,
)


def make_operation_id(prefix: str = "op") -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def build_validation_report(
    *,
    context_id: str,
    target_id: str,
    ready: bool,
    missing_required_inputs: list[str],
    satisfied_inputs: list[str],
    warnings: list[str] | None = None,
    extensions: dict[str, object] | None = None,
) -> dict[str, object]:
    return serialize_validation_report(
        ValidationReport(
            report_kind="validation_report",
            context_id=context_id,
            target_id=target_id,
            ready=ready,
            missing_required_inputs=missing_required_inputs,
            satisfied_inputs=satisfied_inputs,
            warnings=warnings or [],
            extensions=extensions or {},
        )
    )


def build_operation_request(
    *,
    operation_kind: str,
    context_id: str,
    target_id: str,
    payload: dict[str, object],
    extensions: dict[str, object] | None = None,
) -> dict[str, object]:
    return serialize_operation_request(
        OperationRequest(
            request_kind="operation_request",
            operation_id=make_operation_id(),
            operation_kind=operation_kind,
            context_id=context_id,
            target_id=target_id,
            payload=payload,
            extensions=extensions or {},
        )
    )


def build_route_decision(
    *,
    context_id: str,
    target_id: str,
    route_name: str,
    next_skill: str,
    reason: str,
    extensions: dict[str, object] | None = None,
) -> dict[str, object]:
    return serialize_route_decision(
        RouteDecision(
            decision_kind="route_decision",
            context_id=context_id,
            target_id=target_id,
            route_name=route_name,
            next_skill=next_skill,
            reason=reason,
            extensions=extensions or {},
        )
    )
