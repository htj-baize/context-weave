from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

VALIDATION_REPORT_REQUIRED_FIELDS = [
    "report_kind",
    "context_id",
    "target_id",
    "ready",
    "missing_required_inputs",
    "satisfied_inputs",
    "warnings",
]
VALIDATION_REPORT_STABLE_FIELDS = VALIDATION_REPORT_REQUIRED_FIELDS + ["extensions"]
OPERATION_REQUEST_REQUIRED_FIELDS = [
    "request_kind",
    "operation_id",
    "operation_kind",
    "context_id",
    "target_id",
    "payload",
]
OPERATION_REQUEST_STABLE_FIELDS = OPERATION_REQUEST_REQUIRED_FIELDS + ["extensions"]
ROUTE_DECISION_REQUIRED_FIELDS = [
    "decision_kind",
    "context_id",
    "target_id",
    "route_name",
    "next_skill",
    "reason",
]
ROUTE_DECISION_STABLE_FIELDS = ROUTE_DECISION_REQUIRED_FIELDS + ["extensions"]


@dataclass
class ValidationReport:
    report_kind: str
    context_id: str
    target_id: str
    ready: bool
    missing_required_inputs: list[str] = field(default_factory=list)
    satisfied_inputs: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationRequest:
    request_kind: str
    operation_id: str
    operation_kind: str
    context_id: str
    target_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteDecision:
    decision_kind: str
    context_id: str
    target_id: str
    route_name: str
    next_skill: str
    reason: str
    extensions: dict[str, Any] = field(default_factory=dict)


def serialize_validation_report(report: ValidationReport) -> dict[str, Any]:
    return asdict(report)


def serialize_operation_request(request: OperationRequest) -> dict[str, Any]:
    return asdict(request)


def serialize_route_decision(decision: RouteDecision) -> dict[str, Any]:
    return asdict(decision)
