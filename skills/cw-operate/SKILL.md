---
name: cw-operate
description: Specialized skill family for structured operations that consume target bindings without executing external side effects.
---

# CW Operate

description

- specialized skill family for structured operations such as validate, prepare, and route

when_to_use

- a workflow already has context and target information
- the next step is to validate, route, or apply structured payloads

when_not_to_use

- the task still needs core context build or merge work
- the task is only about target/schema discovery

required_inputs

- operation-specific inputs defined by the selected `operate.*` skill

expected_outputs

- operation results
- validation or apply summaries

side_effects

- none in the current first slice

related_skills

- `context-weave`
- `cw-context`
- `cw-target`

reference_docs

- [Skill Spec](../../docs/skill-spec.md)
- [Operation Request Contract](../../docs/operation-request-contract.md)
- [Operation Report Contract](../../docs/operation-report-contract.md)
- [CW Context Operations](../cw-context/references/context-operations.md)
- [CW Target Operations](../cw-target/references/target-operations.md)
- [CW Operate Operations](./references/operate-operations.md)
