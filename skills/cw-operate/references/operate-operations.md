# CW Operate Reference v0.1

## Purpose

This document is the operator-facing reference for the `cw-operate` skill family.

It complements:

- [ContextWeave Root Skill](../../context-weave/SKILL.md)
- [CW Operate Skill](../SKILL.md)

with concrete input/output and command-level examples.

## Shared CLI Rules

### Success Surface

All CLI success responses return:

```json
{
  "status": "ok",
  "result": {},
  "meta": {}
}
```

### Error Surface

All CLI errors return:

```json
{
  "status": "error",
  "error": {
    "code": "invalid_argument|not_found|validation_error|contract_error|internal_error",
    "message": "...",
    "details": {},
    "retryable": false
  }
}
```

## `operate.validate`

- description:
  - Validate whether a target binding is ready for downstream operation.
- required_inputs:
  - `binding`
- expected_outputs:
  - `report`
  - `validation_summary`

```bash
cw run operate.validate --binding @/abs/path/to/binding.json
```

## `operate.prepare`

- description:
  - Prepare a neutral operation request from a ready target binding.
- required_inputs:
  - `binding`
- optional_inputs:
  - `operation_kind`
- expected_outputs:
  - `request`
  - `request_summary`

```bash
cw run operate.prepare --binding @/abs/path/to/binding.json --operation-kind apply
```

## `operate.route`

- description:
  - Route a target binding to the next appropriate skill step.
- required_inputs:
  - `binding`
- expected_outputs:
  - `decision`
  - `route_summary`

```bash
cw run operate.route --binding @/abs/path/to/binding.json
```

## Stable Examples

- [Ready Binding](../../../examples/minimal/binding.ready.json)
- [Needs Input Binding](../../../examples/minimal/binding.needs-input.json)
- [Composition Reference](../../../docs/composition-reference.md)
