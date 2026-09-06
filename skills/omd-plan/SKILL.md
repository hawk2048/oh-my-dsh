---
name: omd-plan
description: "Plan: explore first with non-mutating reads/search/static analysis, then produce a concrete implementation plan (task breakdown with dependencies + acceptance criteria + file-level changes). No implementation. Use as the first stage of the plan→execute→review→verify pipeline, or when the user asks to plan/规划/方案/计划/怎么实现."
---

# oh-my-dsh · Plan 规划

先探明现状，再产出一份**可执行、可验收**的实现计划；此阶段**不写代码**。对应 OMC 的 `plan` 工作流（Tier-0 流水线第一段：`plan → execute → review → verify`）。

## 何时用

- 任务还没拆清楚，或横跨多文件/多模块。
- 用户说"规划""方案""计划""先想清楚怎么做""plan"。
- 作为流水线的起点：规划完交给 `execute`。

## 探索优先（不动手）

先用**非变更**手段把现状摸清，再谈怎么做：

- `read` / `grep` / `glob` 读代码、搜符号、列文件；
- `web_search` / `web_fetch` 查官方文档（用 SDK/框架/API 前必查）；
- 大范围探索可并行 `subagent`：每个子代理负责一个子系统/一个疑问，返回结构化结论。

原则：计划必须**扎根在真实仓库**，不要凭空假设接口或路径。

## 产出计划

计划至少包含三块：

| 块 | 内容 |
|----|------|
| 任务分解 | 编号任务，标明依赖关系（哪些可并行） |
| 验收标准 | 每个任务怎么算"做完"（测试/命令/观察点） |
| 落地位置 | 每个任务改哪些文件、用什么既有模式 |

把计划写成正文（markdown）。若当前处于 plan mode，用 `exit_plan_mode` 提交计划等待确认；否则把计划留在回答里，等用户确认后再进入 `execute`。

## 与其它阶段的关系

- `plan` 管"拆什么、怎么验收"；`deep-interview` 管"需求本身还没问清"——需求模糊先 `deep-interview`，需求清楚了才 `plan`。
- 别在这里实现：`plan` 的产出是"做什么"，`execute` 才做。

## 收尾：HUD

用 `omd-hud` 输出计划概览：任务清单表（依赖/验收列）+ 阶段进度条。让"要做什么、依赖谁、怎么算完"一眼可见。

## 反模式

- 别跳过探索直接写计划——没读代码的计划是猜的。
- 别把 `plan` 和 `deep-interview` 混用：一个管需求，一个管实现方案。
- 别在 plan 阶段改文件（非变更探索除外）。
