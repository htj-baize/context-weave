# Standard Context Contract v0.1

## Purpose

`standard_context` 是 `ContextWeave` 的核心资产类型。

它用于承载一个可被后续 structured operations 消费的正式 context 对象。

## Required Fields

- `context_kind`
  - fixed value: `standard_context`
- `context_id`
  - stable identifier for the context object
- `context_version`
  - current contract version
- `scope`
  - high-level scope label for the context
- `payload`
  - structured context payload
- `trace`
  - lineage and provenance data

## Minimal Shape

```json
{
  "context_kind": "standard_context",
  "context_id": "ctx_build_001",
  "context_version": "v1",
  "scope": "source_state",
  "payload": {},
  "trace": {
    "source_refs": [],
    "derived_from": [],
    "transforms": []
  }
}
```

## Field Rules

### `context_id`

- must be a non-empty string
- should be stable enough for downstream tracing

### `context_version`

- first public version is `v1`
- breaking shape changes must increment version

### `scope`

- should describe the scope, not the business meaning
- examples:
  - `source_state`
  - `runtime_state`
  - `mixed`
  - `task_slice`

### `payload`

- must be an object
- must remain structured and machine-readable
- prompt text must not become the contract surface

### `trace`

- must follow `context trace contract`

### `extensions`

- optional object
- reserved for additive non-breaking metadata
- consumers must not require undocumented extension keys

## Stability Rule

Stable fields:

- `context_kind`
- `context_id`
- `context_version`
- `scope`
- `payload`
- `trace`
- `extensions`

Only `extensions` is open for additive contract growth without changing the core shape.
