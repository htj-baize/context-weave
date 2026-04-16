# Changelog

All notable changes to `ContextWeave` should be recorded in this file.

The format is intentionally simple:

- Added
- Changed
- Fixed
- Breaking

## 0.1.0

### Added

- first public product shell for `ContextWeave`
- skill families:
  - `context.*`
  - `target.*`
  - `operate.*`
- stable CLI entrypoints:
  - `cw`
  - `context-weave`
  - `./scripts/cw`
- product docs, contract docs, and skill references
- repo-local bootstrap, build, and dist-check scripts
- doctor validation for docs, scripts, skill surfaces, and registry alignment
- stable minimal example assets under `examples/minimal/`
- a composition reference covering standard multi-step seams
- fixture registry surface with stable fixture ids and CLI discovery
- a second standard target fixture that intentionally leaves one required input unsatisfied for upper-layer validation scenarios

### Changed

- bootstrap policy was reduced to the minimum supported strategy:
  - use `PYTHON_BIN` if explicitly provided
  - otherwise discover `python3.12` then `python3.11` from the user shell environment
  - create a repo-local `.venv`
- packaging metadata was normalized for current setuptools validation
- public contract docs now distinguish stable fields from additive extension slots
- CLI success responses now use a uniform `status + result + meta` envelope

### Fixed

- `scripts/check-dist` now passes the project root correctly to its embedded Python checker
- `doctor` link validation no longer crashes on root-level markdown files such as `README.md`
- `build` now completes through artifact verification for both wheel and sdist
- CLI failure responses now expose a formal error taxonomy with stable error codes

### Breaking

- none
