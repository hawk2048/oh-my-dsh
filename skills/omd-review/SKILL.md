---
name: omd-review
description: "Review: a separate review pass that evaluates the implementation — never self-approve in the same context. Route to a reviewer subagent (subagent_fork or subagent), read the diffs, produce an issues list. Use as the review stage of plan→execute→review→verify, or when the user asks to review/评审/审查/code review."
---

# oh-my-dsh · Review 评审

对刚写完的实现做一轮**独立**评审，产出缺陷清单。对应 OMC 的 `review` 工作流（Tier-0 流水线第三段：`plan → execute → review → verify`）。

## 何时用

- `execute` 刚产出改动，需要独立把关。
- 用户说"评审""审查""review""帮我看看写得对不对"。

## 核心：独立评审，绝不自我背书

**写和评必须是两趟分开的活**——不要在同一个上下文里既当作者又当评审。做法：

- 用 `subagent` 或 `subagent_fork` 派一个**评审代理**，让它独立读改动（`subagent_fork` 继承本会话已完成内容，适合评审刚写的改动）。
- 让评审代理读 diff / 改动文件，对照**计划里的验收标准**逐条核。
- 产出结构化 `issues` 清单：每条含位置、问题、严重度、建议改法。

评审要点：正确性、边界/异常、安全、与既有模式的一致性、有无 `test.skip`/`.only`、TODO 占位、桩实现这类"假完成"痕迹。

## 产出与流转

评审结果只有两种去向：

1. **无问题** → 进入 `verify`（测试/构建验证）。
2. **有问题** → 把 issues 回给 `execute` 修，修完再评；严重缺陷优先。

## 与其它阶段的关系

- `review` 看的是"写对没有"，`verify` 看的是"跑通没有、验收没有"——两者不互相替代。
- 别用评审代理去实现，也别让实现代理自我评审。

## 收尾：HUD

用 `omd-hud` 输出评审结果：issues 表（位置/严重度/状态）+ 通过/缺陷计数。让"还有几个问题没修"可见。

## 反模式

- 别自我评审（同一个代理写完就宣布"没问题"）。
- 别把评审做成"看起来没问题"的模糊结论——要落到具体缺陷或明确通过。
- 别跳过评审直接宣布完成。
