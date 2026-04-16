# Context Snapshot Contract v0.1

## Purpose

`context snapshot` is a persistence-facing wrapper for a saved context artifact.

It allows workflows to recover, review, replay, or inspect prior context states.

## Required Fields

- `snapshot_ref`
- `snapshot_metadata`

## Minimal Shape

```json
{
  "snapshot_ref": "/abs/path/to/context.snapshot.json",
  "snapshot_metadata": {
    "context_id": "ctx_build_001",
    "label": "build_round_1",
    "created_at": ""
  }
}
```

## Field Rules

### `snapshot_ref`

- must be a non-empty string
- should point to the persisted snapshot artifact

### `snapshot_metadata.context_id`

- must match the saved context identifier

### `snapshot_metadata.label`

- optional
- can be used for workflow-friendly labels

### `snapshot_metadata.created_at`

- optional
- recommended format: ISO 8601 string

