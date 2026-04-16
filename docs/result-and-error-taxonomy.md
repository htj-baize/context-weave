# Result And Error Taxonomy

## Purpose

`ContextWeave` exposes a stable CLI-facing envelope for both success and failure.

This taxonomy exists so upper-layer agents and workflows do not need to infer result shape from command-specific payloads.

## Success Envelope

All successful CLI commands should return:

```json
{
  "status": "ok",
  "result": {},
  "meta": {}
}
```

## Error Envelope

All failed CLI commands should return:

```json
{
  "status": "error",
  "error": {
    "code": "invalid_argument",
    "message": "human-readable explanation",
    "details": {},
    "retryable": false
  }
}
```

Some command failures may also include a `result` field when partial diagnostic output is useful, for example `doctor`.

## Error Codes

Supported top-level error codes:

- `invalid_argument`
  - malformed or missing CLI input
- `not_found`
  - referenced file or asset does not exist
- `validation_error`
  - payload shape is structurally invalid for the expected contract
- `contract_error`
  - a formally documented contract rule is violated
- `doctor_failed`
  - repository validation completed but at least one check failed
- `internal_error`
  - unexpected unclassified failure

## Contract Rule

- `status`
  - stable top-level field
- `result`
  - stable top-level field for successful execution
- `error`
  - stable top-level field for failed execution
- `meta`
  - optional stable top-level field for successful execution metadata

No consumer should depend on undocumented top-level fields outside this envelope.
