# ContextWeave

`ContextWeave` 是一个独立的、可发布的 context management skill product。

它不以任何外部场景或外部执行方式为中心语义，而以：

- `context`
- `target`
- `structured operation`

作为产品边界。

## Product Surface

`ContextWeave` 当前提供三层最小产品骨架：

- `context.*`
- `target.*`
- `operate.*`

这三层共同组成：

- context lifecycle
- target surface
- structured operation preparation

## First Slice

- 定义独立产品壳
- 定义第一批 `context.*` skills
- 提供稳定的 `skills/ + registry + CLI`

## Current Skills

- `context.read`
- `context.build`
- `context.merge`
- `context.slice`
- `context.snapshot`
- `context.trace`
- `target.read`
- `target.build`
- `target.bind`
- `operate.validate`
- `operate.prepare`
- `operate.route`

## Quickstart

运行环境：

- `Python 3.11+`

第一次使用：

```bash
cd /path/to/context-weave
./scripts/bootstrap
./scripts/cw doctor --project-root .
./scripts/cw list
```

`./scripts/bootstrap` 会直接使用用户 shell 环境里可见的 `python3.12` / `python3.11`。
如果你想显式指定解释器，可以设置 `PYTHON_BIN=/abs/path/to/python`。

如果你只是想确认产品面是否可用，最小验证是：

```bash
./scripts/cw doctor --project-root .
```

如果你要验证开发者交付链路，再运行：

```bash
./.venv/bin/python -m pytest -q
./scripts/build
```

命令入口：

```bash
./scripts/cw list
./scripts/cw doctor --project-root .
./scripts/cw describe context.build
./scripts/cw run context.build --source-kind source_package --source-ref /abs/path --build-profile starter
```

一个最小链路示例：

```bash
./scripts/cw run context.build --source-kind source_state --source-ref /tmp/source.json --build-profile starter
./scripts/cw run target.build --schema-ref demo.schema.v1 --required-inputs '["title"]'
./scripts/cw run target.bind --context @/tmp/context.json --target @/tmp/target.json
./scripts/cw run operate.validate --binding @/tmp/binding.json
```

## Release Surface

当前对外稳定暴露的是：

- skill ids
- CLI entrypoints
- 文档里明确写出的 contract

当前版本阶段：

- `0.x`

版本规则入口：

- [Versioning Policy](./docs/versioning-policy.md)
- [Changelog](./CHANGELOG.md)
- [Result And Error Taxonomy](./docs/result-and-error-taxonomy.md)
- [Composition Reference](./docs/composition-reference.md)
- [Fixture Registry](./docs/fixture-registry.md)

## Product Navigation

正式文档入口：

- [Product Vision Spec](./docs/product-vision-spec.md)
- [Architecture](./docs/architecture.md)
- [Versioning Policy](./docs/versioning-policy.md)
- [Standard Context Contract](./docs/standard-context-contract.md)
- [Standard Target Contract](./docs/standard-target-contract.md)
- [Context Trace Contract](./docs/context-trace-contract.md)
- [Context Snapshot Contract](./docs/context-snapshot-contract.md)
- [Target Binding Contract](./docs/target-binding-contract.md)
- [Operation Request Contract](./docs/operation-request-contract.md)
- [Operation Report Contract](./docs/operation-report-contract.md)
- [Result And Error Taxonomy](./docs/result-and-error-taxonomy.md)
- [Context Merge Policy Registry](./docs/context-merge-policy-registry.md)
- [Context Slice Profile Registry](./docs/context-slice-profile-registry.md)
- [Skill Spec](./docs/skill-spec.md)
- [Capability Map](./docs/capability-map.md)
- [Installation And Release](./docs/installation-and-release.md)
- [Composition Reference](./docs/composition-reference.md)
- [Fixture Registry](./docs/fixture-registry.md)
- [Changelog](./CHANGELOG.md)

技能入口：

- [ContextWeave Root Skill](./skills/context-weave/SKILL.md)
- [CW Context Skill](./skills/cw-context/SKILL.md)
- [CW Context Operations](./skills/cw-context/references/context-operations.md)
- [CW Target Skill](./skills/cw-target/SKILL.md)
- [CW Target Operations](./skills/cw-target/references/target-operations.md)
- [CW Operate Skill](./skills/cw-operate/SKILL.md)
- [CW Operate Operations](./skills/cw-operate/references/operate-operations.md)

## Product Boundary

- 对外提供稳定的 `skills/ + registry + CLI`
- 不内置具体领域语义
- 不内置外部执行逻辑
- 不把上层决策逻辑写进基座
