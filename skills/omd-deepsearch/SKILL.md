---
name: omd-deepsearch
description: "Deepsearch: locate implementations, call sites, definitions, and data flow inside the local codebase. Use when the user says deepsearch / 找一下 / 代码在哪 / 定位 / 谁调用了 / 哪里实现的, or asks where something lives rather than how to do it."
---

# oh-my-dsh · Deepsearch 代码库聚焦检索

在**本地仓库**里做证据驱动的检索：定位实现、调用点、定义、数据流。对应 OMC 的 `deepsearch` 提示词触发模式。

## 何时用

- 问题答案是「代码在哪里/谁调用了/哪里实现的」，而不是「该怎么做」。
- 要追一条调用链、一个符号的定义与引用、一个配置项的生效位置。

## 检索纪律

- **本地优先**：`grep`（按符号/正则搜内容）、`glob`（按路径模式找文件）、`read`（读上下文）。代码库问题先用它们，别一上来 `web_search`。
- **给证据**：每个结论带 `file:line`（或文件 + 关键片段），让用户能直接点过去核。
- **追到底**：从调用点沿定义→引用→实现追完整链，别停在第一处匹配。
- **广撒网再收口**：范围不明时并行 `subagent`，每个子代理负责一个模块/一条链路，返回带行号的结论，主代理汇总。

## 与其它模式的关系

- 只想「找到」就只返回定位结果；找到后要「改」就转 `omd-plan` 或 `omd-execute`。
- 要理解「为什么这么设计」而不仅是「在哪」，转 `omd-deep-analyze`。
- 框架/API 的**外部**语义仍用 `web_search`/`web_fetch` 查官方文档，别猜。

## 收尾：HUD

用 `omd-hud` 输出检索结果：命中清单表（符号/文件/行号/角色：定义|调用|实现）。让「找到了什么、每条证据在哪」一眼可见。

## 反模式

- 别对代码库问题直接 `web_search`——那是外部信息，不是本项目事实。
- 别返回没有 `file:line` 的模糊结论。
- 别在找到第一处匹配就停，确认它是唯一/权威的那一处。
