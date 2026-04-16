from __future__ import annotations

from pathlib import Path

from context_weave.fixture_catalog import fixture_root
from context_weave.skill_catalog import project_root


def test_project_root_prefers_configured_root(monkeypatch, tmp_path: Path) -> None:
    configured_root = tmp_path / "context-weave"
    (configured_root / "skills").mkdir(parents=True)
    (configured_root / "examples").mkdir(parents=True)
    monkeypatch.setenv("CONTEXT_WEAVE_PROJECT_ROOT", str(configured_root))

    assert project_root() == configured_root.resolve()


def test_fixture_root_uses_source_repo_when_installed_from_venv(monkeypatch, tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    installed_file = workspace_root / "context-skills" / ".venv" / "lib" / "python3.12" / "site-packages" / "context_weave" / "skill_catalog.py"
    source_repo = workspace_root / "context-weave"
    (source_repo / "skills").mkdir(parents=True)
    (source_repo / "examples" / "minimal").mkdir(parents=True)
    installed_file.parent.mkdir(parents=True)
    installed_file.write_text("", encoding="utf-8")
    monkeypatch.delenv("CONTEXT_WEAVE_PROJECT_ROOT", raising=False)
    monkeypatch.setattr("context_weave.skill_catalog.__file__", str(installed_file))

    assert project_root() == source_repo.resolve()
    assert fixture_root() == (source_repo / "examples" / "minimal").resolve()
