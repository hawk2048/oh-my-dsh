---
name: omd-ultrathink
description: "Ultrathink: before acting, exhaustively enumerate edge cases, weigh alternatives, and rehearse failure modes. Use when the user says ultrathink / 深度思考 / 想清楚 / 多想想 / 别急着动手 / 三思, and wants deep reasoning before any tool use."
---

# oh-my-dsh · Ultrathink 深度推理

动手前把问题想透：穷举边界、权衡备选、预演失败，**先想清楚再调用工具**。对应 OMC 的 `ultrathink` 提示词触发模式。

## 何时用

- 决策影响大或不可逆，值得慢下来想清楚。
- 用户明确说「先想清楚/别急着动手/多权衡」。

## 推理纪律

1. **定义问题**：先用一句话写清目标与约束（要什么、不要什么、边界在哪）。
2. **枚举方案**：列出可行的候选，不急着锁第一个。
3. **穷举边界**：极端输入、空值、并发、失败、回滚、向后兼容……
4. **预演失败**：每个方案最坏会怎样？什么信号说明它错了？
5. **决策**：按目标给一个主选 + 一个备选，说明为什么。

关键：**这段推理写在回答正文里**，先不刷工具。想清楚后，要执行再转 `omd-plan` / `omd-execute`。

## 与其它模式的关系

- `ultrathink` 是纯推理，不查代码；要看证据用 `omd-deep-analyze`。
- 推理结论要落地成步骤转 `omd-plan`；要直接开干转 `omd-execute`。
- 需求没问清用 `omd-deep-interview`，别在假设上 long 推理。

## 收尾：HUD

用 `omd-hud` 输出决策摘要：方案对比表 + 风险清单 + 主选/备选。让「想过什么、选了谁、为什么」一眼可见。

## 反模式

- 别在没想清楚前就开始 `write`/`edit`——那是边做边猜。
- 别只列一个方案就下结论，至少给备选。
- 别把 ultrathink 拖成无限空想：想清楚一轮就产出决策，需要证据就转 deep-analyze。
