from context_weave.context.build import build_context
from context_weave.errors import ValidationError
from context_weave.operate.prepare import prepare_operation
from context_weave.operate.route import route_operation
from context_weave.operate.validate import validate_operation
from context_weave.target.bind import bind_target
from context_weave.target.build import build_target


def test_validate_operation_reports_ready_binding() -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    context["payload"].update({"title": "Demo"})
    target = build_target("demo.schema.v1", ["title"], [])["target"]
    binding = bind_target(context, target)["binding"]
    result = validate_operation(binding)
    assert result["report"]["ready"] is True
    assert result["validation_summary"]["missing_required_count"] == 0


def test_prepare_operation_builds_request_for_ready_binding() -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    context["payload"].update({"title": "Demo"})
    target = build_target("demo.schema.v1", ["title"], [])["target"]
    binding = bind_target(context, target)["binding"]
    result = prepare_operation(binding, "apply")
    assert result["request"]["request_kind"] == "operation_request"
    assert result["request"]["payload"]["title"] == "Demo"


def test_route_operation_reports_missing_input_route() -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    target = build_target("demo.schema.v1", ["title"], [])["target"]
    binding = bind_target(context, target)["binding"]
    result = route_operation(binding)
    assert result["decision"]["route_name"] == "needs_input"
    assert result["decision"]["next_skill"] == "context.build"


def test_prepare_operation_rejects_unready_binding() -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    target = build_target("demo.schema.v1", ["title"], [])["target"]
    binding = bind_target(context, target)["binding"]
    try:
        prepare_operation(binding, "apply")
    except ValidationError as error:
        assert error.code == "validation_error"
    else:
        raise AssertionError("expected ValidationError")
