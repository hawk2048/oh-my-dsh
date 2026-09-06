---
name: omd-autopilot
description: "Autopilot: one lead agent (you) drives a single objective to verified completion across goal rounds, delegating via subagents and tracking with todo_write. Use for end-to-end autonomous feature work with minimal ceremony, or when the user says autopilot/自动驾驶/自主执行/自动驾驶式."
---

# oh-my-dsh · Autopilot 自动驾驶

一个主控代理（你）把一个目标从模糊一路推到「已验证完成」。对应 OMC 的 Autopilot 模式：**单领导、自主执行、持续到底**。

## 何时用

- 用户给了一个明确的最终目标："搭一个 REST API""重构认证模块"。
- 不想走 Team 的完整五阶段仪式，但目标要真正跑完、验证过。
- 用户说"autopilot""自动驾驶""自主执行""一路做完"。

## 核心：goal 工具循环

Autopilot 的地基是 DSH 的 goal 工具——一个**跨多轮持续到完成**的目标，不是单轮内做完。

```
create_goal(objective)  →  [每一轮]  todo_write 推进  →  subagent 委托  →  update_goal 推进  →  完成
```

1. **建目标**：`create_goal(objective, { max_goal_rounds })`。objective 写成"可验收的完成目标"，不是任务描述——"通过 npm test 的认证模块重构"优于"重构认证"。
2. **拆计划**：立刻用 `todo_write` 列出实现步骤，每步一条；并行步骤可同时 `in_progress`。
3. **每轮推进**：本轮该做的做（`subagent` 委托独立子任务、读代码、改文件），做完就把对应 todo 置 `completed`，用 `update_goal` 保持目标推进。
4. **持续到完成**：跨轮继续，别在单轮里硬塞。每个长目标都属于 goal 工具，不属于一次回答。
5. **委托**：能独立、能并行的子任务用 `subagent`（后台并行），不要把上下文全烧在主控里。
6. **收尾**：只有「验证通过、验收标准满足」才 `update_goal complete`；用 `get_goal` 读当前 revision 再更新。

## 目标状态纪律

- `complete`：目标**真正达成**才标。别因为"做完了主要部分"就提前标。
- `blocked`：**同一阻塞条件持续至少 3 个 goal 轮**才标，并在 `blocked_reason` 里写明具体条件。"难/不确定/还有活"不算 blocked。
- 目标在会话恢复或 fork 后会解除武装：用户说"继续/接着做"时用 `update_goal resume` 重新武装。

## 与 Team / Ralph 的边界

- **Team**：多子系统、要分阶段规格。Autopilot 是单领导直推，不搞 prd 仪式。
- **Ralph**：要"每个完成都必须验证、不许静默半成品"的强验证循环，或用户明说 fresh-agent 迭代。
- Autopilot 内部可以顺手并行 `subagent`，但主控权始终在你这一个代理手里。

## 收尾：HUD

每轮结束按 `omd-hud` 输出内联仪表盘：目标 + 轮次 + todo 进度 + 子代理状态。让用户始终看到"现在到哪了、还差什么"。

## 反模式

- 别在单轮里试图一次做完整个目标——goal 工具就是为"跨轮持续"设计的。
- 别把 goal 用在琐碎的单轮任务上。
- 别静默交付半成品——收尾前必须验证。
