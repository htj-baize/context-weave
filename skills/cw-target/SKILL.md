---
name: cw-target
description: Specialized skill family for target/schema-facing operations built on top of ContextWeave.
---

# CW Target

description

- specialized skill family for target and schema-facing operations built on top of ContextWeave

when_to_use

- a workflow needs explicit target schema selection
- a workflow needs target-bound context shaping

when_not_to_use

- the task only needs generic context lifecycle operations
- the task is about execution of already prepared payloads

required_inputs

- target-specific inputs defined by the selected `target.*` skill

expected_outputs

- target descriptors
- target-bound context views

side_effects

- none

related_skills

- `context-weave`
- `cw-context`
- `cw-operate`

reference_docs

- [Skill Spec](../../docs/skill-spec.md)
- [Standard Target Contract](../../docs/standard-target-contract.md)
- [Target Binding Contract](../../docs/target-binding-contract.md)
- [Target Operations](./references/target-operations.md)
