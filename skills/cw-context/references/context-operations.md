# CW Context Reference v0.1

## Purpose

This document is the operator-facing reference for the `cw-context` skill family.

It complements:

- [ContextWeave Root Skill](../../context-weave/SKILL.md)
- [CW Context Skill](../SKILL.md)

with concrete input/output and command-level examples.

## Shared CLI Rules

### Commands

```bash
cw list
cw doctor --project-root .
cw describe context.build
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

## `context.read`

- description:
  - Read an existing standard context asset from a file reference.
- required_inputs:
  - `context_ref`
- expected_outputs:
  - `context`
  - `context_metadata`

```bash
cw run context.read --context-ref /abs/path/to/context.json
cw run context.read --context-ref /abs/path/to/context.snapshot.json
```

`context_metadata.source_kind` values:

- `raw_context`
- `snapshot_wrapper`

## `context.build`

- description:
  - Build a standard context from a declared source state.
- required_inputs:
  - `source_kind`
  - `source_ref`
- optional_inputs:
  - `build_profile`
- expected_outputs:
  - `context`
  - `build_summary`

```bash
cw run context.build --source-kind source_state --source-ref /abs/path/to/input.json --build-profile starter
```

## `context.merge`

- description:
  - Merge multiple contexts into a single context.
- required_inputs:
  - `contexts`
- optional_inputs:
  - `merge_policy`
- expected_outputs:
  - `context`
  - `merge_summary`

Supported merge policies:

- `override_right`
- `override_left`
- `shallow_union`

```bash
cw run context.merge --contexts @/abs/path/to/contexts.json --merge-policy override_right
```

## `context.slice`

- description:
  - Slice a task-specific sub-context from a full context.
- required_inputs:
  - `context`
  - `slice_profile`
- expected_outputs:
  - `context`
  - `slice_summary`

Supported slice profiles:

- `task_focus`
- `source_focus`
- `trace_focus`

```bash
cw run context.slice --context @/abs/path/to/context.json --slice-profile task_focus
```

## `context.snapshot`

- description:
  - Persist a context as a recoverable snapshot artifact.
- required_inputs:
  - `context`
- optional_inputs:
  - `output_path`
  - `label`
- expected_outputs:
  - `snapshot_ref`
  - `snapshot_metadata`

```bash
cw run context.snapshot --context @/abs/path/to/context.json --output-path /abs/path/to/context.snapshot.json --label round_1
```

## `context.trace`

- description:
  - Read lineage and provenance information from a context.
- required_inputs:
  - `context`
- expected_outputs:
  - `trace`
  - `lineage_summary`

```bash
cw run context.trace --context @/abs/path/to/context.json
```

## Stable Examples

- [Minimal Context](../../../examples/minimal/context.json)
- [Composition Reference](../../../docs/composition-reference.md)
