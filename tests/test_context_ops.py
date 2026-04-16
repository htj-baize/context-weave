from context_weave.context.build import build_context
from context_weave.context.merge import merge_contexts
from context_weave.context.read import read_context
from context_weave.context.slice import slice_context
from context_weave.context.trace import trace_context
from context_weave.errors import ValidationError
import json
from pathlib import Path


def test_build_context_generates_nonempty_context_id_and_timestamp() -> None:
    payload = build_context("source_state", "/tmp/source.json", "starter")
    context = payload["context"]
    assert context["context_id"].startswith("ctx_")
    assert context["trace"]["transforms"][0]["kind"] == "build"
    assert context["trace"]["transforms"][0]["timestamp"]


def test_merge_contexts_generates_derived_from_ids() -> None:
    left = build_context("source_state", "/tmp/a.json", "left")["context"]
    right = build_context("source_state", "/tmp/b.json", "right")["context"]
    merged = merge_contexts([left, right], "override_right")["context"]
    assert merged["scope"] == "mixed"
    assert len(merged["trace"]["derived_from"]) == 2
    assert merged["trace"]["transforms"][0]["notes"] == "override_right"


def test_merge_contexts_supports_override_left_policy() -> None:
    left = build_context("source_state", "/tmp/a.json", "left")["context"]
    right = build_context("source_state", "/tmp/b.json", "right")["context"]
    merged = merge_contexts([left, right], "override_left")["context"]
    assert merged["payload"]["build_profile"] == "left"


def test_slice_context_uses_task_slice_scope() -> None:
    source = build_context("source_state", "/tmp/source.json", "starter")["context"]
    sliced = slice_context(source, "task_focus")["context"]
    assert sliced["scope"] == "task_slice"
    assert sliced["trace"]["derived_from"] == [source["context_id"]]


def test_slice_context_validates_profile() -> None:
    source = build_context("source_state", "/tmp/source.json", "starter")["context"]
    sliced = slice_context(source, "trace_focus")["context"]
    assert sliced["payload"]["slice_profile"] == "trace_focus"


def test_trace_context_reports_transform_count() -> None:
    source = build_context("source_state", "/tmp/source.json", "starter")["context"]
    traced = trace_context(source)
    assert traced["lineage_summary"]["context_id"] == source["context_id"]
    assert traced["lineage_summary"]["transform_count"] == 1


def test_read_context_supports_snapshot_wrapper(tmp_path: Path) -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    target = tmp_path / "context.snapshot.json"
    target.write_text(json.dumps({"context": context}, ensure_ascii=False, indent=2), encoding="utf-8")
    loaded = read_context(str(target))
    assert loaded["context"]["context_kind"] == "standard_context"
    assert loaded["context_metadata"]["source_kind"] == "snapshot_wrapper"


def test_merge_contexts_rejects_unknown_policy() -> None:
    left = build_context("source_state", "/tmp/a.json", "left")["context"]
    try:
        merge_contexts([left], "unknown_policy")
    except ValidationError as error:
        assert error.code == "validation_error"
    else:
        raise AssertionError("expected ValidationError")


def test_slice_context_rejects_unknown_profile() -> None:
    source = build_context("source_state", "/tmp/source.json", "starter")["context"]
    try:
        slice_context(source, "unknown_profile")
    except ValidationError as error:
        assert error.code == "validation_error"
    else:
        raise AssertionError("expected ValidationError")
