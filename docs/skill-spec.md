# ContextWeave Skill Spec

## Skill Families

### `target.read`

- description:
  - Read an existing standard target asset.

### `target.build`

- description:
  - Build a standard target descriptor from schema-facing inputs.

### `target.bind`

- description:
  - Project a context onto a declared target surface.

### `operate.validate`

- description:
  - Validate whether a target binding is ready for downstream operation.

### `operate.prepare`

- description:
  - Prepare a neutral operation request from a ready target binding.

### `operate.route`

- description:
  - Route a target binding to the next appropriate skill step.

### `context.read`

- description:
  - Read an existing standard context asset.

### `context.build`

- description:
  - Build a standard context from a source state.

### `context.merge`

- description:
  - Merge multiple contexts into a single context.

### `context.slice`

- description:
  - Slice a task-specific sub-context from a full context.

### `context.snapshot`

- description:
  - Persist a context as a recoverable snapshot.

### `context.trace`

- description:
  - Read lineage and provenance information from a context.

## Shared Output Contract

All `context.*` skills should converge on:

- `context_kind`
- `context_id`
- `context_version`
- `scope`
- `payload`
- `trace`

Formal references:

- [Standard Context Contract](./standard-context-contract.md)
- [Standard Target Contract](./standard-target-contract.md)
- [Context Trace Contract](./context-trace-contract.md)
- [Context Snapshot Contract](./context-snapshot-contract.md)
- [Target Binding Contract](./target-binding-contract.md)
- [Operation Request Contract](./operation-request-contract.md)
- [Operation Report Contract](./operation-report-contract.md)
- [Result And Error Taxonomy](./result-and-error-taxonomy.md)
- [Context Merge Policy Registry](./context-merge-policy-registry.md)
- [Context Slice Profile Registry](./context-slice-profile-registry.md)
- [CW Context Operations](../skills/cw-context/references/context-operations.md)
- [CW Target Operations](../skills/cw-target/references/target-operations.md)
- [CW Operate Operations](../skills/cw-operate/references/operate-operations.md)
- [Installation And Release](./installation-and-release.md)
