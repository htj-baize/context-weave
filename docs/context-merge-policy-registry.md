# Context Merge Policy Registry v0.1

## Purpose

This registry defines the allowed merge policy identifiers for `context.merge`.

## Policies

### `override_right`

- description:
  - Later contexts overwrite earlier payload keys.

### `override_left`

- description:
  - Earlier contexts keep precedence over later payload keys.

### `shallow_union`

- description:
  - Merge top-level keys without recursive deep merge behavior.

## Current Support

The current implementation supports:

- `override_right`
- `override_left`
- `shallow_union`

