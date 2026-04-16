---
name: context-weave
description: Root routing skill for ContextWeave. Use when the task is about context modeling, context lifecycle, or choosing a context-related skill.
---

# ContextWeave

description

- root routing skill for ContextWeave

when_to_use

- the task is about context modeling
- the task is about context lifecycle
- the task needs routing into a context-related skill

when_not_to_use

- the task is specific business logic
- the task is selection policy
- the task is external execution logic

required_inputs

- none

expected_outputs

- routing guidance

side_effects

- none

related_skills

- `cw-context`
- `cw-target`
- `cw-operate`

reference_docs

- [CW Context Operations](../cw-context/references/context-operations.md)
- [CW Target Operations](../cw-target/references/target-operations.md)
