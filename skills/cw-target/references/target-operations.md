# CW Target Reference v0.1

## Purpose

This document is the operator-facing reference for the `cw-target` skill family.

It complements:

- [ContextWeave Root Skill](../../context-weave/SKILL.md)
- [CW Target Skill](../SKILL.md)

with concrete input/output and command-level examples.

## Shared CLI Rules

### Commands

```bash
cw list
cw doctor --project-root .
cw describe target.build
cw run <skill_id> ...
```

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

### File Input

Any argument value may use `@/abs/path/to/file` syntax.

Behavior:

- if the file contains JSON, it is decoded as structured input
- otherwise it is passed as raw text

## `target.read`

- description:
  - Read an existing standard target asset from a file reference.
- required_inputs:
  - `target_ref`
- expected_outputs:
  - `target`
  - `target_metadata`

```bash
cw run target.read --target-ref /abs/path/to/target.json
cw run target.read --target-ref /abs/path/to/target.wrapper.json
```

## `target.build`

- description:
  - Build a standard target descriptor from schema-facing inputs.
- required_inputs:
  - `schema_ref`
- optional_inputs:
  - `required_inputs`
  - `optional_inputs`
  - `constraints`
- expected_outputs:
  - `target`
  - `build_summary`

```bash
cw run target.build --schema-ref demo.schema.v1 --required-inputs '[\"title\",\"summary\"]' --optional-inputs '[\"tone\"]' --constraints '{\"max_items\":3}'
```

## `target.bind`

- description:
  - Project a context onto a declared target surface.
- required_inputs:
  - `context`
  - `target`
- expected_outputs:
  - `binding`
  - `binding_summary`

```bash
cw run target.bind --context @/abs/path/to/context.json --target @/abs/path/to/target.json
```

## Stable Examples

- [Minimal Target](../../../examples/minimal/target.json)
- [Composition Reference](../../../docs/composition-reference.md)
