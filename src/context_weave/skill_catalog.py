from __future__ import annotations

import os
from pathlib import Path


def _configured_root() -> Path | None:
    raw_value = os.environ.get("CONTEXT_WEAVE_PROJECT_ROOT")
    if not raw_value:
        return None
    candidate = Path(raw_value).expanduser().resolve()
    if (candidate / "skills").is_dir() and (candidate / "examples").is_dir():
        return candidate
    return None


def _source_root() -> Path | None:
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / "skills").is_dir() and (ancestor / "examples").is_dir():
            return ancestor
    for ancestor in current.parents:
        sibling = ancestor / "context-weave"
        if (sibling / "skills").is_dir() and (sibling / "examples").is_dir():
            return sibling.resolve()
    return None


def project_root() -> Path:
    return _configured_root() or _source_root() or Path(__file__).resolve().parents[2]


def skill_doc_path(skill_name: str) -> str:
    return str(project_root() / "skills" / skill_name / "SKILL.md")
