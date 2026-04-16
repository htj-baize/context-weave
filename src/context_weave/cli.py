from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from context_weave.doctor import run_doctor
from context_weave.errors import ContextWeaveError, InternalError, InvalidArgumentError
from context_weave.fixture_catalog import FIXTURE_REGISTRY
from context_weave.registry import REGISTRY
from context_weave.result import ok_result


def _parse_value(value: str) -> Any:
    if value.startswith("@"):
        path = Path(value[1:])
        if not path.exists():
            raise InvalidArgumentError("argument file does not exist", path=str(path))
        text = path.read_text(encoding="utf-8")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    if value.startswith("{") or value.startswith("["):
        return json.loads(value)
    return value


def _parse_kv_pairs(items: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    index = 0
    while index < len(items):
        token = items[index]
        if not token.startswith("--"):
            raise InvalidArgumentError("unexpected token", token=token)
        key = token[2:].replace("-", "_")
        if index + 1 >= len(items):
            raise InvalidArgumentError("missing value for argument", token=token)
        value = items[index + 1]
        parsed[key] = _parse_value(value)
        index += 2
    return parsed


def _build_call_kwargs(arg_names: list[str], raw_kwargs: dict[str, Any]) -> dict[str, Any]:
    return {name: raw_kwargs[name] for name in arg_names if name in raw_kwargs}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cw")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list")

    fixtures_parser = subparsers.add_parser("fixtures")
    fixtures_subparsers = fixtures_parser.add_subparsers(dest="fixtures_command", required=True)
    fixtures_subparsers.add_parser("list")
    fixtures_describe_parser = fixtures_subparsers.add_parser("describe")
    fixtures_describe_parser.add_argument("fixture_id")

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--project-root", default=".")

    describe_parser = subparsers.add_parser("describe")
    describe_parser.add_argument("skill_id")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("skill_id")
    run_parser.add_argument("args", nargs=argparse.REMAINDER)

    parsed = parser.parse_args(argv)

    if parsed.command == "list":
        payload = ok_result(
            {
                "items": [{"skill_id": key, "summary": value["summary"]} for key, value in REGISTRY.items()],
            },
            command="list",
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if parsed.command == "fixtures":
        if parsed.fixtures_command == "list":
            payload = ok_result(
                {
                    "items": [
                        {
                            "fixture_id": key,
                            "summary": value["summary"],
                            "kind": value["kind"],
                            "path": value["path"],
                        }
                        for key, value in FIXTURE_REGISTRY.items()
                    ],
                },
                command="fixtures.list",
            )
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        entry = FIXTURE_REGISTRY.get(parsed.fixture_id)
        if entry is None:
            payload = InvalidArgumentError("unknown fixture_id", fixture_id=parsed.fixture_id).to_payload()
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 1
        print(
            json.dumps(
                ok_result(
                    {
                        "fixture_id": parsed.fixture_id,
                        **entry,
                    },
                    command="fixtures.describe",
                    fixture_id=parsed.fixture_id,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if parsed.command == "doctor":
        result = run_doctor(parsed.project_root)
        exit_code = 0 if result["doctor_status"] == "ok" else 1
        if exit_code == 0:
            print(json.dumps(ok_result(result, command="doctor"), ensure_ascii=False, indent=2))
        else:
            print(
                json.dumps(
                    {
                        "status": "error",
                        "error": {
                            "code": "doctor_failed",
                            "message": "doctor checks failed",
                            "details": {
                                "failed_count": result["failed_count"],
                            },
                            "retryable": False,
                        },
                        "result": result,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        return exit_code

    if parsed.command == "describe":
        entry = REGISTRY.get(parsed.skill_id)
        if entry is None:
            payload = InvalidArgumentError("unknown skill_id", skill_id=parsed.skill_id).to_payload()
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 1
        entry = REGISTRY[parsed.skill_id]
        print(
            json.dumps(
                ok_result(
                    {
                        "skill_id": parsed.skill_id,
                        "summary": entry["summary"],
                        "description": entry["description"],
                        "when_to_use": entry["when_to_use"],
                        "when_not_to_use": entry["when_not_to_use"],
                        "args": entry["args"],
                        "expected_outputs": entry["expected_outputs"],
                        "side_effects": entry["side_effects"],
                        "skill_doc": entry["skill_doc"],
                    },
                    command="describe",
                    skill_id=parsed.skill_id,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        entry = REGISTRY[parsed.skill_id]
        kwargs = _parse_kv_pairs(parsed.args)
        result = entry["callable"](**_build_call_kwargs(entry["args"], kwargs))
        print(json.dumps(ok_result(result, command="run", skill_id=parsed.skill_id), ensure_ascii=False, indent=2))
        return 0
    except KeyError:
        payload = InvalidArgumentError("unknown skill_id", skill_id=getattr(parsed, "skill_id", "")).to_payload()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    except ContextWeaveError as error:
        print(json.dumps(error.to_payload(), ensure_ascii=False, indent=2))
        return 1
    except Exception as error:
        payload = InternalError("internal error", exception_type=type(error).__name__)
        print(json.dumps(payload.to_payload(), ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
