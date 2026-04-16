from __future__ import annotations

import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from context_weave.cli import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = PROJECT_ROOT / "examples" / "minimal"


def _run_cli(args: list[str]) -> dict[str, object]:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(args)
    payload = json.loads(buffer.getvalue())
    assert exit_code == 0, payload
    return payload


def test_ready_composition_reference_assets_work() -> None:
    context_payload = _run_cli(["run", "context.read", "--context-ref", str(EXAMPLES_ROOT / "context.json")])
    target_payload = _run_cli(["run", "target.read", "--target-ref", str(EXAMPLES_ROOT / "target.json")])
    binding_payload = _run_cli(
        [
            "run",
            "target.bind",
            "--context",
            f"@{EXAMPLES_ROOT / 'context.json'}",
            "--target",
            f"@{EXAMPLES_ROOT / 'target.json'}",
        ]
    )
    validate_payload = _run_cli(
        [
            "run",
            "operate.validate",
            "--binding",
            f"@{EXAMPLES_ROOT / 'binding.ready.json'}",
        ]
    )

    assert context_payload["result"]["context"]["context_id"] == "ctx_demo_001"
    assert target_payload["result"]["target"]["target_id"] == "tgt_demo_001"
    assert binding_payload["result"]["binding"]["missing_required_inputs"] == []
    assert validate_payload["result"]["report"]["ready"] is True


def test_needs_input_composition_reference_assets_route_to_context_build() -> None:
    route_payload = _run_cli(
        [
            "run",
            "operate.route",
            "--binding",
            f"@{EXAMPLES_ROOT / 'binding.needs-input.json'}",
        ]
    )

    assert route_payload["result"]["decision"]["route_name"] == "needs_input"
    assert route_payload["result"]["decision"]["next_skill"] == "context.build"
