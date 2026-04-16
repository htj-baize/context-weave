# Composition Reference

## Purpose

This document captures the smallest stable multi-step compositions built on top of `ContextWeave`.

It is the bridge between single-skill references and upper-layer orchestration.

## Example Assets

Stable example assets live under:

- [examples/minimal/context.source.json](../examples/minimal/context.source.json)
- [examples/minimal/context.json](../examples/minimal/context.json)
- [examples/minimal/target.json](../examples/minimal/target.json)
- [examples/minimal/binding.ready.json](../examples/minimal/binding.ready.json)
- [examples/minimal/binding.needs-input.json](../examples/minimal/binding.needs-input.json)

Registry entry:

- [Fixture Registry](./fixture-registry.md)

## Composition A

`context.build -> target.build -> target.bind -> operate.validate`

Use this composition when you want to confirm a context can satisfy a declared target surface.

```bash
cw run context.build --source-kind source_state --source-ref ./examples/minimal/context.source.json --build-profile starter
cw run target.build --schema-ref demo.schema.v1 --required-inputs '["title","summary"]' --optional-inputs '["tone"]'
cw run target.bind --context @./examples/minimal/context.json --target @./examples/minimal/target.json
cw run operate.validate --binding @./examples/minimal/binding.ready.json
```

Expected outcome:

- `operate.validate` returns `status: ok`
- `result.report.ready` is `true`

## Composition B

`context.read -> context.slice -> target.bind -> operate.route`

Use this composition when you need to decide the next step without directly preparing execution.

```bash
cw run context.read --context-ref ./examples/minimal/context.json
cw run context.slice --context @./examples/minimal/context.json --slice-profile task_focus
cw run target.bind --context @./examples/minimal/context.json --target @./examples/minimal/target.json
cw run operate.route --binding @./examples/minimal/binding.needs-input.json
```

Expected outcome:

- `operate.route` returns `status: ok`
- `result.decision.route_name` is either:
  - `ready_for_prepare`
  - `needs_input`

## Composition Rule

Stable composition seams are:

- `context`
- `target`
- `binding`
- `report`
- `request`
- `decision`

Upper-layer systems should compose through these objects rather than by inspecting internal helper modules.
