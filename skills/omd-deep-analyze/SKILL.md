---
name: omd-deep-analyze
description: "Deep-analyze: multi-angle, evidence-backed analysis of code, architecture, or a problem. Use when the user says deep-analyze / 深度分析 / 分析一下 / 为什么这样 / 值得吗, and wants thorough reasoning, not a quick fix."
---

# oh-my-dsh · Deep-analyze 深度分析

对一段代码、一个架构决策或一个问题做**多角度、带证据**的深入分析，而不是给一个速修补丁。对应 OMC 的 `deep-analyze` 提示词触发模式。

## 何时用

- 用户要「为什么」「值不值」「有什么隐患」，而不是「改成什么」。
- 涉及架构/安全/性能/可维护性等多维权衡，单一视角会偏。

## 分析纪律

1. **扎根证据**：先 `read`/`grep` 把相关代码与历史读透，结论必须落到具体文件/行。
2. **多角度并行**：用 `subagent` 并行从不同视角分析——架构、安全、性能、可测试性、数据流——每个子代理返回结构化发现。
3. **显式权衡**：对每个候选方案列「利/弊/代价/风险」，别只给一个答案。
4. **给建议**：以「若目标是 X，建议 Y」收口，并标出证据强度（确证/推测）。

## 与其它模式的关系

- 分析产出「为什么与权衡」，要落地成方案再转 `omd-plan`。
- 需求本身没问清先 `omd-deep-interview`；代码在哪没摸清先 `omd-deepsearch`。
- 只想「推理决策、不查代码」的纯思考用 `omd-ultrathink`；要看代码证据用本模式。

## 收尾：HUD

用 `omd-hud` 输出分析结构：视角清单 + 每视角关键发现 + 方案权衡表。让「从哪些角度看了、各自结论、怎么取舍」一眼可见。

## 反模式

- 别只给结论不给证据（file:line / 引用）。
- 别只从单一视角（比如只谈安全）下结论。
- 别把「分析」做成「直接改」——本模式产出判断，不产出补丁。
