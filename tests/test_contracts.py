from context_weave.contracts.context import (
    STANDARD_CONTEXT_STABLE_FIELDS,
    ContextTrace,
    SourceRef,
    StandardContext,
    TransformRecord,
    serialize_standard_context,
)
from context_weave.contracts.snapshot import (
    ContextSnapshotMetadata,
    ContextSnapshotRef,
    serialize_context_snapshot,
)
from context_weave.contracts.operate import (
    OPERATION_REQUEST_STABLE_FIELDS,
    ROUTE_DECISION_STABLE_FIELDS,
    VALIDATION_REPORT_STABLE_FIELDS,
    OperationRequest,
    RouteDecision,
    ValidationReport,
    serialize_operation_request,
    serialize_route_decision,
    serialize_validation_report,
)
from context_weave.contracts.target import (
    STANDARD_TARGET_STABLE_FIELDS,
    TARGET_BINDING_STABLE_FIELDS,
    StandardTarget,
    TargetBinding,
    serialize_standard_target,
    serialize_target_binding,
)
from context_weave.contracts.trace import serialize_context_trace


def test_standard_context_serializes_to_expected_shape() -> None:
    payload = serialize_standard_context(
        StandardContext(
            context_kind="standard_context",
            context_id="ctx_001",
            context_version="v1",
            scope="source_state",
            payload={"foo": "bar"},
            trace=ContextTrace(
                source_refs=[SourceRef(source_kind="source_state", source_ref="/tmp/input.json")],
                derived_from=[],
                transforms=[TransformRecord(kind="build")],
            ),
            extensions={"profile": "starter"},
        )
    )

    assert payload["context_kind"] == "standard_context"
    assert payload["context_id"] == "ctx_001"
    assert payload["trace"]["source_refs"][0]["source_kind"] == "source_state"
    assert payload["extensions"]["profile"] == "starter"
    assert sorted(payload.keys()) == sorted(STANDARD_CONTEXT_STABLE_FIELDS)


def test_context_trace_serializes_to_expected_shape() -> None:
    payload = serialize_context_trace(
        ContextTrace(
            source_refs=[SourceRef(source_kind="source_state", source_ref="abc")],
            derived_from=["ctx_prev"],
            transforms=[TransformRecord(kind="merge", notes="override_right")],
        )
    )

    assert payload["derived_from"] == ["ctx_prev"]
    assert payload["transforms"][0]["kind"] == "merge"


def test_context_snapshot_serializes_to_expected_shape() -> None:
    payload = serialize_context_snapshot(
        ContextSnapshotRef(
            snapshot_ref="/tmp/context.snapshot.json",
            snapshot_metadata=ContextSnapshotMetadata(
                context_id="ctx_001",
                label="round_1",
                created_at="2026-01-01T00:00:00+00:00",
            ),
        )
    )

    assert payload["snapshot_ref"] == "/tmp/context.snapshot.json"
    assert payload["snapshot_metadata"]["context_id"] == "ctx_001"


def test_standard_target_serializes_to_expected_shape() -> None:
    payload = serialize_standard_target(
        StandardTarget(
            target_kind="standard_target",
            target_id="tgt_001",
            target_version="v1",
            schema_ref="demo.schema.v1",
            required_inputs=["title", "summary"],
            optional_inputs=["tone"],
            constraints={"max_items": 3},
            extensions={"channel": "demo"},
        )
    )

    assert payload["target_kind"] == "standard_target"
    assert payload["target_id"] == "tgt_001"
    assert payload["required_inputs"] == ["title", "summary"]
    assert payload["extensions"]["channel"] == "demo"
    assert sorted(payload.keys()) == sorted(STANDARD_TARGET_STABLE_FIELDS)


def test_target_binding_serializes_to_expected_shape() -> None:
    payload = serialize_target_binding(
        TargetBinding(
            binding_kind="target_binding",
            context_id="ctx_001",
            target_id="tgt_001",
            target_version="v1",
            satisfied_inputs=["title"],
            missing_required_inputs=["summary"],
            projected_payload={"title": "Demo"},
            extensions={"schema_ref": "demo.schema.v1"},
        )
    )

    assert payload["binding_kind"] == "target_binding"
    assert payload["context_id"] == "ctx_001"
    assert payload["missing_required_inputs"] == ["summary"]
    assert payload["extensions"]["schema_ref"] == "demo.schema.v1"
    assert sorted(payload.keys()) == sorted(TARGET_BINDING_STABLE_FIELDS)


def test_validation_report_serializes_to_expected_shape() -> None:
    payload = serialize_validation_report(
        ValidationReport(
            report_kind="validation_report",
            context_id="ctx_001",
            target_id="tgt_001",
            ready=True,
            missing_required_inputs=[],
            satisfied_inputs=["title"],
            warnings=[],
            extensions={"projected_key_count": 1},
        )
    )

    assert payload["report_kind"] == "validation_report"
    assert payload["ready"] is True
    assert payload["extensions"]["projected_key_count"] == 1
    assert sorted(payload.keys()) == sorted(VALIDATION_REPORT_STABLE_FIELDS)


def test_operation_request_serializes_to_expected_shape() -> None:
    payload = serialize_operation_request(
        OperationRequest(
            request_kind="operation_request",
            operation_id="op_001",
            operation_kind="apply",
            context_id="ctx_001",
            target_id="tgt_001",
            payload={"title": "Demo"},
            extensions={"target_version": "v1"},
        )
    )

    assert payload["request_kind"] == "operation_request"
    assert payload["operation_id"] == "op_001"
    assert payload["extensions"]["target_version"] == "v1"
    assert sorted(payload.keys()) == sorted(OPERATION_REQUEST_STABLE_FIELDS)


def test_route_decision_serializes_to_expected_shape() -> None:
    payload = serialize_route_decision(
        RouteDecision(
            decision_kind="route_decision",
            context_id="ctx_001",
            target_id="tgt_001",
            route_name="ready_for_prepare",
            next_skill="operate.prepare",
            reason="binding already satisfies required target inputs",
            extensions={"satisfied_inputs": ["title"]},
        )
    )

    assert payload["decision_kind"] == "route_decision"
    assert payload["next_skill"] == "operate.prepare"
    assert payload["extensions"]["satisfied_inputs"] == ["title"]
    assert sorted(payload.keys()) == sorted(ROUTE_DECISION_STABLE_FIELDS)
