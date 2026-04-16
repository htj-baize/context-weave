# Operation Report Contract

## Purpose

`validation_report` 和 `route_decision` 是 `operate.*` family 的标准结果对象。

它们负责：

- 表达 binding 是否可执行
- 表达下一步建议路由
- 保持和执行层解耦

## Validation Report Shape

```json
{
  "report_kind": "validation_report",
  "context_id": "ctx_xxx",
  "target_id": "tgt_xxx",
  "ready": true,
  "missing_required_inputs": [],
  "satisfied_inputs": ["title"],
  "warnings": [],
  "extensions": {}
}
```

## Route Decision Shape

```json
{
  "decision_kind": "route_decision",
  "context_id": "ctx_xxx",
  "target_id": "tgt_xxx",
  "route_name": "ready_for_prepare",
  "next_skill": "operate.prepare",
  "reason": "binding already satisfies required target inputs",
  "extensions": {}
}
```

## Stability Rule

Stable `validation_report` fields:

- `report_kind`
- `context_id`
- `target_id`
- `ready`
- `missing_required_inputs`
- `satisfied_inputs`
- `warnings`
- `extensions`

Stable `route_decision` fields:

- `decision_kind`
- `context_id`
- `target_id`
- `route_name`
- `next_skill`
- `reason`
- `extensions`
