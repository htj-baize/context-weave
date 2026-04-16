# ContextWeave Versioning Policy

## Current Stage

`ContextWeave` is currently in the `0.x` stage.

This means the product surface is real and intended for external consumption, but controlled evolution is still allowed.

## Versioning Rule

`ContextWeave` follows semantic versioning with an explicit `0.x` interpretation:

- `patch`:
  - documentation-only fixes
  - internal implementation fixes
  - bug fixes that do not change public contracts
- `minor`:
  - additive skill surface changes
  - additive CLI flags
  - additive fields in output contracts that do not break existing consumers
- `major`:
  - breaking changes to public skill ids
  - breaking changes to CLI invocation shape
  - breaking changes to documented output contracts
  - removal or rename of published product surface

## Public Surface

The following are considered public product surface:

- published skill ids such as `context.build`
- documented CLI entrypoints:
  - `cw`
  - `context-weave`
  - `./scripts/cw`
- documented request and output contract shapes
- documented skill-family navigation and references

## Breaking Change Rule

The following changes must be treated as breaking:

- renaming an existing skill id
- removing an existing skill id
- changing the meaning of an existing skill id in a non-compatible way
- changing required CLI arguments for an existing command
- removing a documented output field
- changing the semantic meaning of a documented output field

## Additive Change Rule

The following changes are allowed in `0.x` minor releases:

- adding a new skill id
- adding optional CLI flags
- adding optional output fields
- adding new docs and references
- adding new internal modules without changing public contracts

## Changelog Rule

Every released version must record:

- added
- changed
- fixed
- breaking

If there is no breaking change, the `breaking` section should explicitly say `none`.

## Release Gate

Before a new version is considered releasable:

1. `./scripts/cw doctor --project-root .` must pass
2. `./.venv/bin/python -m pytest -q` must pass
3. `./scripts/build` must pass
4. any public-surface change must be reflected in:
   - `README.md`
   - `docs/skill-spec.md`
   - `CHANGELOG.md`
