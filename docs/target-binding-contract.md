# Target Binding Contract

## Purpose

`target_binding` 用来表示：

- 一个 context
- 针对某个 target
- 投影出来的输入视图

它的作用是给后续 `operate.*` 提供稳定的中间层，而不是直接执行结果动作。

## Canonical Shape

```json
{
  "binding_kind": "target_binding",
  "context_id": "ctx_xxx",
  "target_id": "tgt_xxx",
  "target_version": "v1",
  "satisfied_inputs": ["title", "summary"],
  "missing_required_inputs": ["tone"],
  "projected_payload": {
    "title": "Demo",
    "summary": "Short text"
  },
  "extensions": {}
}
```

## Field Rules

- `binding_kind`
  - 当前固定为 `target_binding`
- `context_id`
  - 来源 context 标识
- `target_id`
  - 对应 target 标识
- `target_version`
  - 对应 target 版本
- `satisfied_inputs`
  - 已在 context payload 中满足的字段
- `missing_required_inputs`
  - 未满足的必需字段
- `projected_payload`
  - 从 context payload 中按 target 输入表面投影得到的对象
- `extensions`
  - additive non-breaking metadata slot

## Stability Rule

Stable fields:

- `binding_kind`
- `context_id`
- `target_id`
- `target_version`
- `satisfied_inputs`
- `missing_required_inputs`
- `projected_payload`
- `extensions`
