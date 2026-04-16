from __future__ import annotations

from pathlib import Path

from context_weave.skill_catalog import project_root


def fixture_root() -> Path:
    return project_root() / "examples" / "minimal"


FIXTURE_REGISTRY = {
    "minimal.context.source": {
        "summary": "Minimal source-state input example.",
        "kind": "source_state",
        "path": str(fixture_root() / "context.source.json"),
        "related_contract": "source_state",
    },
    "minimal.context": {
        "summary": "Minimal standard context example.",
        "kind": "standard_context",
        "path": str(fixture_root() / "context.json"),
        "related_contract": "standard_context",
    },
    "minimal.target": {
        "summary": "Minimal standard target example.",
        "kind": "standard_target",
        "path": str(fixture_root() / "target.json"),
        "related_contract": "standard_target",
    },
    "minimal.target.needs_input": {
        "summary": "Standard target example that requires an input absent from the minimal context.",
        "kind": "standard_target",
        "path": str(fixture_root() / "target.needs-input.json"),
        "related_contract": "standard_target",
    },
    "minimal.binding.ready": {
        "summary": "Minimal ready binding example.",
        "kind": "target_binding",
        "path": str(fixture_root() / "binding.ready.json"),
        "related_contract": "target_binding",
    },
    "minimal.binding.needs_input": {
        "summary": "Minimal binding example with missing required inputs.",
        "kind": "target_binding",
        "path": str(fixture_root() / "binding.needs-input.json"),
        "related_contract": "target_binding",
    },
}
