# Fixture Registry

## Purpose

`ContextWeave` publishes a small set of stable example assets as a fixture registry.

This registry exists so upper-layer systems can reference documented example assets without hardcoding ad hoc file paths.

## Current Fixture IDs

- `minimal.context.source`
- `minimal.context`
- `minimal.target`
- `minimal.target.needs_input`
- `minimal.binding.ready`
- `minimal.binding.needs_input`

## CLI Surface

List fixtures:

```bash
cw fixtures list
```

Describe a fixture:

```bash
cw fixtures describe minimal.context
```

## Registry Rule

Each fixture entry should provide:

- `fixture_id`
- `summary`
- `kind`
- `path`
- `related_contract`

## Intended Use

Use the fixture registry for:

- documentation examples
- integration tests
- consumer adapter bring-up
- smoke validation of composition seams

Do not treat fixture IDs as production runtime assets.
