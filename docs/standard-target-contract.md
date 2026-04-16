# Standard Target Contract

## Purpose

`standard_target` 用来描述一个下游结构化操作期望消费的输入表面。

它不负责执行，也不负责生成结果，只负责声明：

- 目标 schema 是什么
- 哪些输入是必需的
- 哪些输入是可选的
- 当前 target 自身约束是什么

## Canonical Shape

```json
{
  "target_kind": "standard_target",
  "target_id": "tgt_xxx",
  "target_version": "v1",
  "schema_ref": "demo.schema.v1",
  "required_inputs": ["title", "summary"],
  "optional_inputs": ["tone", "tags"],
  "constraints": {
    "max_items": 3
  },
  "extensions": {}
}
```

## Field Rules

- `target_kind`
  - 当前固定为 `standard_target`
- `target_id`
  - 非空字符串
- `target_version`
  - target contract 版本，默认 `v1`
- `schema_ref`
  - 非空字符串，用于标识下游目标 schema
- `required_inputs`
  - 必需字段列表
- `optional_inputs`
  - 可选字段列表
- `constraints`
  - target 自身约束对象
- `extensions`
  - additive non-breaking metadata slot

## Validation Rules

- `required_inputs` 和 `optional_inputs` 必须是字符串列表
- 两者不能重叠
- `schema_ref` 必须非空
- `target_kind` 必须是 `standard_target`

## Stability Rule

Stable fields:

- `target_kind`
- `target_id`
- `target_version`
- `schema_ref`
- `required_inputs`
- `optional_inputs`
- `constraints`
- `extensions`
