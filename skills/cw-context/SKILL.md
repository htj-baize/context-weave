---
name: cw-context
description: Specialized skill for standard context operations including build, read, merge, slice, snapshot, and trace.
---

# CW Context

description

- specialized skill for standard context operations

when_to_use

- a workflow needs a standard context
- multiple sources must be merged
- a full context must be narrowed into a task-specific sub-context

when_not_to_use

- the task is directly about result policy
- the task is only about applying already validated payloads

required_inputs

- source-specific inputs depending on the selected `context.*` operation

expected_outputs

- standard context objects
- merge/slice/build metadata
- snapshot or trace metadata

side_effects

- `context.snapshot` writes a snapshot artifact
- other `context.*` operations are read-only

related_skills

- `context-weave`

reference_docs

- [Context Operations](./references/context-operations.md)
