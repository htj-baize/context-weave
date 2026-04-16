from __future__ import annotations

import re
from pathlib import Path

from context_weave.fixture_catalog import FIXTURE_REGISTRY
from context_weave.registry import REGISTRY


REQUIRED_DOCS = [
    "docs/product-vision-spec.md",
    "docs/architecture.md",
    "docs/versioning-policy.md",
    "docs/standard-context-contract.md",
    "docs/standard-target-contract.md",
    "docs/context-trace-contract.md",
    "docs/context-snapshot-contract.md",
    "docs/target-binding-contract.md",
    "docs/operation-request-contract.md",
    "docs/operation-report-contract.md",
    "docs/result-and-error-taxonomy.md",
    "docs/context-merge-policy-registry.md",
    "docs/context-slice-profile-registry.md",
    "docs/skill-spec.md",
    "docs/installation-and-release.md",
    "docs/composition-reference.md",
    "docs/fixture-registry.md",
    "CHANGELOG.md",
]

REQUIRED_SCRIPTS = [
    "scripts/bootstrap",
    "scripts/cw",
    "scripts/build",
    "scripts/check-dist",
]

SKILL_FAMILIES = [
    "context-weave",
    "cw-context",
    "cw-target",
    "cw-operate",
]

ROOT_SKILL_FAMILY = "context-weave"

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_SPEC_FAMILY_RE = re.compile(r"^### `([^`]+)`", re.MULTILINE)
REQUIRED_SKILL_FIELDS = [
    "description",
    "when_to_use",
    "when_not_to_use",
    "required_inputs",
    "expected_outputs",
    "side_effects",
    "related_skills",
    "reference_docs",
]
REQUIRED_REGISTRY_FIELDS = [
    "summary",
    "description",
    "when_to_use",
    "when_not_to_use",
    "args",
    "expected_outputs",
    "side_effects",
    "skill_doc",
    "callable",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _check_exists(checks: list[dict[str, object]], label: str, path: Path) -> None:
    checks.append(
        {
            "check": label,
            "status": "ok" if path.exists() else "error",
            "path": str(path),
        }
    )


def _check_markdown_links(checks: list[dict[str, object]], label_prefix: str, path: Path) -> None:
    text = _read_text(path)
    try:
        display_path = path.relative_to(path.parents[2] if "skills" in path.parts else path.parent)
    except ValueError:
        display_path = path.name
    for ref in MARKDOWN_LINK_RE.findall(text):
        if "://" in ref or ref.startswith("#") or ref.startswith("mailto:"):
            continue
        target = (path.parent / ref).resolve()
        checks.append(
            {
                "check": f"{label_prefix}:{display_path}:{ref}",
                "status": "ok" if target.exists() else "error",
                "path": str(target),
            }
        )


def _check_skill_family_surface(checks: list[dict[str, object]], root: Path, family: str) -> None:
    family_root = root / "skills" / family
    skill_doc = family_root / "SKILL.md"
    _check_exists(checks, f"skill_surface_exists:skills/{family}/SKILL.md", skill_doc)
    references_dir = family_root / "references"
    if family != ROOT_SKILL_FAMILY:
        _check_exists(checks, f"skill_references_dir_exists:skills/{family}/references", references_dir)
        reference_files = sorted(references_dir.glob("*.md")) if references_dir.exists() else []
        checks.append(
            {
                "check": f"skill_reference_files_present:skills/{family}",
                "status": "ok" if reference_files else "error",
                "path": str(references_dir),
                "count": len(reference_files),
            }
        )
    else:
        checks.append(
            {
                "check": f"skill_references_dir_optional:skills/{family}/references",
                "status": "ok",
                "path": str(references_dir),
            }
        )

    text = _read_text(skill_doc)
    missing_sections = [field for field in REQUIRED_SKILL_FIELDS if field not in text]
    checks.append(
        {
            "check": f"skill_doc_sections:{family}",
            "status": "ok" if not missing_sections else "error",
            "missing_sections": missing_sections,
            "path": str(skill_doc),
        }
    )
    if skill_doc.exists():
        _check_markdown_links(checks, "skill_link_exists", skill_doc)
    if references_dir.exists():
        for ref_file in sorted(references_dir.glob("*.md")):
            _check_markdown_links(checks, "reference_link_exists", ref_file)


def _extract_skill_spec_ids(path: Path) -> list[str]:
    text = _read_text(path)
    return SKILL_SPEC_FAMILY_RE.findall(text)


def run_doctor(project_root: str | Path) -> dict[str, object]:
    root = Path(project_root)
    checks: list[dict[str, object]] = []

    for relative_path in REQUIRED_DOCS:
        _check_exists(checks, f"doc_exists:{relative_path}", root / relative_path)

    for relative_path in REQUIRED_SCRIPTS:
        _check_exists(checks, f"script_exists:{relative_path}", root / relative_path)

    readme_path = root / "README.md"
    _check_exists(checks, "readme_exists:README.md", readme_path)
    if readme_path.exists():
        _check_markdown_links(checks, "readme_link_exists", readme_path)

    for relative_path in REQUIRED_DOCS:
        doc_path = root / relative_path
        if doc_path.exists():
            _check_markdown_links(checks, "doc_link_exists", doc_path)

    for family in SKILL_FAMILIES:
        _check_skill_family_surface(checks, root, family)

    for fixture_id, entry in FIXTURE_REGISTRY.items():
        path = Path(str(entry["path"]))
        checks.append(
            {
                "check": f"fixture_exists:{fixture_id}",
                "status": "ok" if path.exists() else "error",
                "path": str(path),
            }
        )

    for skill_id, entry in REGISTRY.items():
        missing_fields = [field for field in REQUIRED_REGISTRY_FIELDS if field not in entry]
        checks.append(
            {
                "check": f"registry_fields:{skill_id}",
                "status": "ok" if not missing_fields else "error",
                "missing_fields": missing_fields,
            }
        )
        skill_doc = Path(str(entry.get("skill_doc", "")))
        checks.append(
            {
                "check": f"skill_doc_exists:{skill_id}",
                "status": "ok" if skill_doc.exists() else "error",
                "path": str(skill_doc),
            }
        )

    spec_skill_ids = _extract_skill_spec_ids(root / "docs/skill-spec.md")
    registry_skill_ids = sorted(REGISTRY.keys())
    missing_from_spec = [item for item in registry_skill_ids if item not in spec_skill_ids]
    missing_from_registry = [item for item in spec_skill_ids if item not in registry_skill_ids]
    checks.append(
        {
            "check": "skill_spec_registry_alignment",
            "status": "ok" if not missing_from_spec and not missing_from_registry else "error",
            "missing_from_spec": missing_from_spec,
            "missing_from_registry": missing_from_registry,
        }
    )

    failed = [item for item in checks if item["status"] != "ok"]
    return {
        "doctor_status": "ok" if not failed else "error",
        "project_root": str(root),
        "check_count": len(checks),
        "failed_count": len(failed),
        "checks": checks,
    }
