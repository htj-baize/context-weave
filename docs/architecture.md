# ContextWeave Architecture

## Position

`ContextWeave` 是一个独立产品，不承载具体外部场景的业务语义。

产品目的和边界以：

- [Product Vision Spec](./product-vision-spec.md)

作为最高优先级约束。

它的职责是：

1. 统一 `context` 的表达
2. 提供围绕 `context` 的稳定 skill surface
3. 为上层的结构化操作提供共用底座

## First Slice

第一版只定义 `context family`：

- `context.read`
- `context.build`
- `context.merge`
- `context.slice`
- `context.snapshot`
- `context.trace`

## Layers

### `contracts/`

定义标准 context、snapshot、trace contract。

当前正式 contract 文档：

- [Standard Context Contract](./standard-context-contract.md)
- [Standard Target Contract](./standard-target-contract.md)
- [Context Trace Contract](./context-trace-contract.md)
- [Context Snapshot Contract](./context-snapshot-contract.md)
- [Target Binding Contract](./target-binding-contract.md)
- [Operation Request Contract](./operation-request-contract.md)
- [Operation Report Contract](./operation-report-contract.md)
- [Context Merge Policy Registry](./context-merge-policy-registry.md)
- [Context Slice Profile Registry](./context-slice-profile-registry.md)

### `context/`

实现 context 相关的纯操作。

### `target/`

实现 target 相关的纯操作，包括 target build、read 和 context-to-target bind。

### `operate/`

实现 operate 相关的纯操作，包括 validate、prepare 和 route。

### `registry.py`

定义 skill id、参数和 summary 的统一映射。

### `cli.py`

提供 `list / describe / run` 命令入口。

### `skills/`

承载产品级、top-level 的 agent-facing skill docs，并作为 `SKILL.md` 的单一事实来源。

### `docs/`

承载 spec、contract、architecture 和 release-facing product docs。

## Non-Goals

第一版不做：

- 具体领域逻辑
- 外部执行逻辑
- 上层决策逻辑
- 结果生成逻辑
