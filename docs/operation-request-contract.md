# Operation Request Contract

## Purpose

`operation_request` 是由 `operate.prepare` 生成的中间执行请求。

它的职责是：

- 承载已准备好的 target-bound payload
- 给外部执行器或上层 workflow 一个稳定请求封装
- 不在此层直接执行任何外部动作

## Canonical Shape

```json
{
  "request_kind": "operation_request",
  "operation_id": "op_xxx",
  "operation_kind": "apply",
  "context_id": "ctx_xxx",
  "target_id": "tgt_xxx",
  "payload": {
    "title": "Demo"
  },
  "extensions": {}
}
```

## Field Rules

- `request_kind`
  - fixed value: `operation_request`
- `operation_id`
  - non-empty request identifier
- `operation_kind`
  - non-empty downstream operation label
- `context_id`
  - source context identifier
- `target_id`
  - source target identifier
- `payload`
  - structured operation payload object
- `extensions`
  - additive non-breaking metadata slot
