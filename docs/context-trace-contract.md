# Context Trace Contract v0.1

## Purpose

`trace` records where a context came from and how it evolved.

Every `standard_context` must carry trace information.

## Required Fields

- `source_refs`
- `derived_from`
- `transforms`

## Minimal Shape

```json
{
  "source_refs": [
    {
      "source_kind": "source_state",
      "source_ref": "/abs/path/or/opaque/ref"
    }
  ],
  "derived_from": [],
  "transforms": [
    {
      "kind": "build",
      "timestamp": "",
      "notes": ""
    }
  ]
}
```

## Source Ref Rules

### `source_kind`

- must be a non-empty string
- describes the kind of source, not the full semantics

### `source_ref`

- may be a path, opaque id, or external reference string

## Transform Rules

### `kind`

- must be a non-empty string
- examples:
  - `build`
  - `merge`
  - `slice`
  - `normalize`
  - `snapshot`

### `timestamp`

- optional
- recommended format: ISO 8601 string

### `notes`

- optional
- used for policy labels or human-readable hints

