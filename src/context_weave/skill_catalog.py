from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def skill_doc_path(skill_name: str) -> str:
    return str(project_root() / "skills" / skill_name / "SKILL.md")
