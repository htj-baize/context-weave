from context_weave.doctor import run_doctor
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_doctor_reports_ok_for_current_project() -> None:
    payload = run_doctor(PROJECT_ROOT)
    assert payload["doctor_status"] == "ok"
    assert payload["failed_count"] == 0


def test_doctor_checks_skill_spec_registry_alignment() -> None:
    payload = run_doctor(PROJECT_ROOT)
    alignment_checks = [item for item in payload["checks"] if item["check"] == "skill_spec_registry_alignment"]
    assert len(alignment_checks) == 1
    assert alignment_checks[0]["status"] == "ok"


def test_doctor_checks_skill_reference_directories() -> None:
    payload = run_doctor(PROJECT_ROOT)
    reference_checks = [
        item
        for item in payload["checks"]
        if item["check"].startswith("skill_references_dir_exists:skills/cw-")
    ]
    assert len(reference_checks) >= 3
    assert all(item["status"] == "ok" for item in reference_checks)


def test_doctor_checks_markdown_links() -> None:
    payload = run_doctor(PROJECT_ROOT)
    link_checks = [item for item in payload["checks"] if ":./" in item["check"] or ":../" in item["check"]]
    assert link_checks
    assert all(item["status"] == "ok" for item in link_checks)


def test_doctor_checks_required_scripts() -> None:
    payload = run_doctor(PROJECT_ROOT)
    script_checks = [item for item in payload["checks"] if item["check"].startswith("script_exists:")]
    assert len(script_checks) == 4
    assert all(item["status"] == "ok" for item in script_checks)


def test_doctor_checks_registered_fixtures() -> None:
    payload = run_doctor(PROJECT_ROOT)
    fixture_checks = [item for item in payload["checks"] if item["check"].startswith("fixture_exists:")]
    assert len(fixture_checks) >= 6
    assert all(item["status"] == "ok" for item in fixture_checks)
