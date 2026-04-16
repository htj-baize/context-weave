from context_weave.cli import main
import json
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_list_runs() -> None:
    assert main(["list"]) == 0


def test_cli_describe_runs() -> None:
    assert main(["describe", "context.build"]) == 0
    assert main(["describe", "target.build"]) == 0
    assert main(["describe", "operate.validate"]) == 0


def test_cli_doctor_runs() -> None:
    assert main(["doctor", "--project-root", str(PROJECT_ROOT)]) == 0


def test_cli_run_returns_error_code_for_unknown_skill() -> None:
    assert main(["run", "unknown.skill"]) == 1


def test_cli_supports_file_argument_input(tmp_path: Path) -> None:
    target = tmp_path / "context.json"
    target.write_text(
        json.dumps(
            {
                "context_kind": "standard_context",
                "context_id": "ctx_file",
                "context_version": "v1",
                "scope": "source_state",
                "payload": {},
                "trace": {"source_refs": [], "derived_from": [], "transforms": []},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    assert main(["run", "context.trace", "--context", f"@{target}"]) == 0


def test_cli_list_returns_status_ok() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["list"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert "result" in payload
    assert payload["meta"]["command"] == "list"


def test_cli_run_returns_status_ok() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["run", "context.build", "--source-kind", "source_state", "--source-ref", "/tmp/x.json"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert "result" in payload
    assert payload["meta"]["skill_id"] == "context.build"


def test_cli_run_target_build_returns_status_ok() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(
            [
                "run",
                "target.build",
                "--schema-ref",
                "demo.schema.v1",
                "--required-inputs",
                "[\"title\",\"summary\"]",
                "--optional-inputs",
                "[\"tone\"]",
            ]
        )
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert "result" in payload


def test_cli_run_operate_validate_returns_status_ok() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(
            [
                "run",
                "operate.validate",
                "--binding",
                "{\"binding_kind\":\"target_binding\",\"context_id\":\"ctx_1\",\"target_id\":\"tgt_1\",\"target_version\":\"v1\",\"satisfied_inputs\":[\"title\"],\"missing_required_inputs\":[],\"projected_payload\":{\"title\":\"Demo\"}}",
            ]
        )
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert "result" in payload


def test_cli_describe_returns_result_envelope() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["describe", "context.build"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert payload["result"]["skill_id"] == "context.build"


def test_cli_error_payload_contains_error_taxonomy() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["run", "unknown.skill"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 1
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "invalid_argument"
    assert payload["error"]["retryable"] is False


def test_cli_fixtures_list_returns_status_ok() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["fixtures", "list"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert payload["result"]["items"]
    assert payload["meta"]["command"] == "fixtures.list"


def test_cli_fixtures_describe_returns_fixture() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["fixtures", "describe", "minimal.context"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert payload["result"]["fixture_id"] == "minimal.context"
    assert payload["result"]["kind"] == "standard_context"


def test_cli_fixtures_describe_returns_not_ready_target_fixture() -> None:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["fixtures", "describe", "minimal.target.needs_input"])
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0
    assert payload["status"] == "ok"
    assert payload["result"]["fixture_id"] == "minimal.target.needs_input"
    assert payload["result"]["kind"] == "standard_target"
