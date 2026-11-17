---
name: omd-ralph
description: "拉夫：持久验证/修复循环，不留静默半成品。显式全新代理迭代用 Agent(resume)，否则用 TaskCreate+verify 循环。任务必须完整完成并验证时使用；触发词：ralph / 拉夫 / verify-fix / 必须做完。"
---

# oh-my-workbuddy · Ralph 持久验证循环

> **WorkBuddy 提示**：本文含 DSH 原生工具调用（goal/cancel/hud/ralph），仅作方法论参考。实际执行请跳到文末「WorkBuddy 适配」段。


目标必须**完整完成并验证过**，绝不允许静默的半成品。对应 OMC 的 Ralph 模式。原 DSH 版分两条路。WorkBuddy 无原生 ralph 工具，请直接看文末「WorkBuddy 适配」段执行。下方 DSH 原生段落仅作方法论参考。

## 何时用

- 用户说"ralph""拉夫""一定要做完""不许半途""fresh-agent 迭代"。
- 任务有硬验收标准，必须验证到全绿。
- 普通的"做一下就完"不要用 Ralph——它重。

## 路线 A：原生 ralph 工具

（DSH 参考）原版在用户明确要求 fresh-agent 迭代时调 ralph 工具：

```
ralph(objective, { maxRounds })
```

语义（和 goal 不同，务必分清）：

- 每一轮开一个**全新子代理**，不继承任何对话种子。
- **共享工作区是唯一长期记忆**——子代理通过读/写文件在轮次间传递上下文。
- 只有一份**有界结构化报告**跨轮传递，其余什么都不带。
- 返回：某个 worker 报告完成、或报告具体阻塞、或达到轮次上限。
- 完成与阻塞是**worker 的自述报告，不是独立评估**——最后你要自己核验工作区里的真实产物。

用 Ralph 时，你的职责是：写一个**不可变、可验收的 objective**；把验收标准和进度约定写进工作区文件（如 `RALPH.md`）让每轮子代理读到；循环结束后独立检查产物是否真达标。

## 路线 B：手动 verify/fix 循环（原生 ralph 之外的默认）

用户没明说要 fresh-agent 迭代、但任务必须验证到全绿时，用 goal + 验证代理手动循环：

```
1. create_goal(objective)           # 持久目标
2. 实现（主控 or subagent 委托）
3. verify：subagent 验证代理对照验收标准产出"通过/缺陷清单"
4. fix：有缺陷就修，回到第 3 步
5. 全绿 → update_goal complete；同一阻塞 ≥3 轮 → update_goal blocked
```

验证代理的提示词要**硬性**：逐条对照验收标准，只允许"通过"或"具体缺陷"，不允许"看起来没问题"这类模糊结论。

## 与其它模式的关系

- Ralph **包含并行**：执行和验证阶段内部照常并行 `Agent` 工具（`execute` 的并行能力），只是外面多套一层"必须验证到全绿"。
- Ralph 强调**不许静默半成品**；Autopilot 强调**单领导持续到底**。两者常叠加。
- Ralph 的 verify/fix 循环，本质是把 `plan→execute→review→verify` 里的 `verify` 阶段反复执行到全绿。

## 收尾：HUD

每轮 verify/fix 后按 `omd-hud` 输出仪表盘：轮次、通过/缺陷计数、fix loop 次数。让"还剩几个缺陷"始终可见。

## 反模式

- 别把 Ralph 用在琐碎任务上。
- 别把 worker 的"完成报告"当最终结论——你要亲自核验工作区。
- fix loop 必须设上限，且必须有"全绿"这个明确退出条件。


## WorkBuddy 适配（持久验证循环）

WorkBuddy 无原生 `ralph` 工具，用以下组合实现同等语义：

- **手动 verify/fix 循环**：`TaskCreate` 建目标 → 实现 → `Agent` 派验证代理（对照验收标准，只输出"通过/具体缺陷"）→ 有缺陷就修 → 循环到全绿。
- **fresh-agent 迭代**：用 `Agent` 的 `resume=<上轮返回的 Task ID>` 从上次 transcript 继续（2026-11-17 实测：ROUND1→ROUND2 续跑成功）。要求完全全新上下文时不传 resume、派生新 agent，把**验收标准与进度写进工作区文件**（如 `RALPH.md`），让每轮子代理读文件对齐——共享工作区是唯一长期记忆。
- **关键**：每轮 Agent 返回时会给出 `Task ID (for resume)`，务必记录；丢了就无法续跑只能用工作区文件 fresh 启动。
- **退出条件**：全绿，或同一阻塞 ≥3 轮。每轮 verify 后用可视化组件汇报：轮次、通过/缺陷数、fix loop 次数。
- **重要**：worker 的"完成报告"是自述，主控必须亲自核验工作区真实产物。
