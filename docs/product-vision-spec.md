# ContextWeave Product Vision Spec

## Purpose

`ContextWeave` 存在的目的不是直接生成结果数据，也不是承载某个具体工作流。

它存在的目的，是为任意上层 skill 系统提供一个稳定的 `context management substrate`，让后续的：

- operate
- apply
- route

都建立在同一套正式的 context contract 之上。

换句话说：

`ContextWeave` 的核心使命是把“临时上下文拼接”升级为“正式的、可复用的、可追踪的 context 资产体系”。

## Vision

`ContextWeave` 的长期愿景是成为一个独立发布、独立安装、独立演化的 skill product：

- 它不依赖某个单一业务项目的页面或宿主
- 它不以某个具体业务对象作为中心语义
- 它不把外部执行方式差异写进产品核心
- 它专注于 `context lifecycle + structured context operations`
- 它在第二层提供 neutral 的 `target surface`，但不承担执行逻辑

## Core Product Thesis

`ContextWeave` 的核心判断是：

1. 小 skill 之所以无法稳定组合，通常不是因为缺少结果操作，而是因为缺少统一的 context
2. 上层的 operate / apply / route，如果没有统一 context contract，最终一定会重新耦合
3. 只有先把 context 资产化、标准化、可追踪化，后续所有高层能力才会真正可组合

因此：

`ContextWeave` 的第一优先级永远是 context，而不是业务结果。

## Product Boundary

### In Scope

`ContextWeave` 应负责：

- 标准 context contract
- context build / read / merge / slice / snapshot / trace
- context-related skill docs
- skill registry
- stable CLI surface
- top-level skill docs for agent-facing consumption

### Out of Scope

`ContextWeave` 不应负责：

- specific business semantics
- result-generation strategy
- selection strategy
- external execution strategy
- presentation layer concerns

这些能力未来可以建立在 `ContextWeave` 之上，但不应该写进 `ContextWeave` 内部。

## Design Principles

### 1. Context First

任何新能力进入 `ContextWeave` 前，都要先回答：

- 它是不是在管理 context？
- 它是不是在操作 context lifecycle？
- 它是不是在维护 context contract？

如果不是，就默认不属于 `ContextWeave`。

### 2. Neutral Product Core

`ContextWeave` 不以任何特定业务对象或表现层名词作为产品主语义。

它应该保持 neutral，只围绕 context 自身建模。

### 3. Structured, Not Prompt-Shaped

`ContextWeave` 输出的核心资产应当是结构化对象，而不是 prompt text。

prompt 可以建立在 context 上，但 prompt 不应成为产品 contract。

### 4. Traceable By Default

任意 context 都应该可以回答：

- 从哪里来
- 由哪些输入构成
- 经过了哪些 transform
- 当前版本是什么

没有 trace 的 context，不算完整产品资产。

### 5. Composable Above, Minimal Below

`ContextWeave` 本身应保持小而稳。

它的目标不是把所有能力做进来，而是提供足够稳的底座，让上层系统自由组合。

## First Success Criteria

第一阶段成功，不以“能生成多少业务内容”为标准，而以这些标准为准：

1. `context.*` family 有清晰、稳定的 contract
2. `list / describe / run` 已经能作为独立产品入口工作
3. skill docs、registry、CLI 三者一致
4. context 可以被读取、构建、合并、裁剪、快照、追踪
5. 后续扩展时，不需要回写产品中心语义

## Failure Modes To Avoid

后续演化中，以下情况视为偏航：

1. 把外部业务逻辑写进 `ContextWeave`
2. 把外部执行逻辑直接写进 `context.*` skills
3. 把某个外部系统的命名体系变成产品命名体系
4. 为了某个单一业务场景，破坏通用 context contract
5. 把 `ContextWeave` 做成“什么都做”的 orchestration 杂物箱

## Evolution Rule

以后任何新能力进入 `ContextWeave` 前，都应该先通过这三个问题：

1. 这是不是 context lifecycle 的一部分？
2. 这是不是为上层 skill 提供稳定底座，而不是代替上层决策？
3. 这项能力如果迁出到上层系统，会不会更合理？

只要有一个问题答案偏向“更适合在上层”，就不应进入 `ContextWeave`。
