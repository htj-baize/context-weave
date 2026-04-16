# Installation And Release

## Runtime Requirement

- Python `3.11+`

## Local Editable Install

```bash
cd /path/to/context-weave
./scripts/bootstrap
```

After install, the CLI entrypoints are:

- `cw`
- `context-weave`
- `./scripts/cw`

`./scripts/bootstrap` will:

- prefer `python3.12`, then `python3.11`
- use interpreters discoverable from the user's shell environment
- create `.venv/`
- install `setuptools>=68` and `wheel` into `.venv`
- install `-e .[dev]`
- leave the stable repo-local command at `./scripts/cw`

You may override interpreter discovery with:

```bash
PYTHON_BIN=/abs/path/to/python3.12 ./scripts/bootstrap
```

## Local Validation

```bash
cd /path/to/context-weave
./scripts/cw doctor --project-root .
./.venv/bin/python -m pytest -q
```

## Build Distribution Artifacts

```bash
cd /path/to/context-weave
./scripts/bootstrap
./scripts/build
```

Expected outputs:

- `dist/*.whl`
- `dist/*.tar.gz`

`./scripts/build` will:

- install `build` into the repo-local `.venv`
- run `python -m build --no-isolation`
- run `./scripts/check-dist`

You may also run artifact verification separately:

```bash
cd /path/to/context-weave
./scripts/check-dist
```

## Release Checklist

1. Run `./scripts/cw doctor --project-root .`
2. Run `./.venv/bin/python -m pytest -q`
3. Verify `README.md` still matches the current skill surface
4. Verify `docs/versioning-policy.md` still matches the current release rule
5. Update `CHANGELOG.md`
6. Verify every skill family still has:
   - `SKILL.md`
   - `references/`
7. Build the package with `./scripts/build`
8. Publish the generated `dist/*` artifacts through the chosen package channel

## Validation Boundary

Current repository validation covers:

- `./scripts/cw doctor --project-root .`
- `./.venv/bin/python -m pytest -q`
- `./scripts/build`
- `./scripts/check-dist`

Current machine-level observation during authoring:

- the active shell default `python3` was `3.9.6`
- a valid `python3.12` interpreter was still discoverable through explicit interpreter discovery

So the repository bootstrap path is now aligned with the real machine state:

- default shell Python may be too old
- bootstrap will rely on the user's shell environment unless `PYTHON_BIN` is explicitly provided

## Packaging Boundary

`ContextWeave` publishes:

- Python package under `src/context_weave`
- CLI entrypoints
- `docs/`
- `skills/`

It does not publish:

- external workflow executors
- domain-specific adapters
- runtime-specific integrations

## Release Documentation

Before publishing any version, the release-facing documents should be aligned:

- [Versioning Policy](./versioning-policy.md)
- [Skill Spec](./skill-spec.md)
- [Result And Error Taxonomy](./result-and-error-taxonomy.md)
- [Composition Reference](./composition-reference.md)
- [Fixture Registry](./fixture-registry.md)
- [Changelog](../CHANGELOG.md)
