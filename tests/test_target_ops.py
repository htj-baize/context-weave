from pathlib import Path
import json

from context_weave.context.build import build_context
from context_weave.errors import ValidationError
from context_weave.target.bind import bind_target
from context_weave.target.build import build_target
from context_weave.target.read import read_target


def test_build_target_generates_nonempty_target_id() -> None:
    payload = build_target("demo.schema.v1", ["title", "summary"], ["tone"], {"max_items": 3})
    target = payload["target"]
    assert target["target_id"].startswith("tgt_")
    assert target["schema_ref"] == "demo.schema.v1"


def test_bind_target_projects_payload_and_reports_missing_required() -> None:
    context = build_context("source_state", "/tmp/source.json", "starter")["context"]
    context["payload"].update({"title": "Demo", "tone": "quiet"})
    target = build_target("demo.schema.v1", ["title", "summary"], ["tone"])["target"]
    binding = bind_target(context, target)
    assert binding["binding"]["projected_payload"]["title"] == "Demo"
    assert binding["binding"]["projected_payload"]["tone"] == "quiet"
    assert binding["binding"]["missing_required_inputs"] == ["summary"]
    assert binding["binding_summary"]["ready"] is False


def test_read_target_supports_wrapper_payload(tmp_path: Path) -> None:
    target = build_target("demo.schema.v1", ["title"], ["tone"])["target"]
    target_path = tmp_path / "target.wrapper.json"
    target_path.write_text(json.dumps({"target": target}, ensure_ascii=False, indent=2), encoding="utf-8")
    loaded = read_target(str(target_path))
    assert loaded["target"]["target_kind"] == "standard_target"
    assert loaded["target_metadata"]["source_kind"] == "wrapper"


def test_build_target_rejects_overlapping_inputs() -> None:
    try:
        build_target("demo.schema.v1", ["title"], ["title"])
    except ValidationError as error:
        assert error.code == "validation_error"
    else:
        raise AssertionError("expected ValidationError")
