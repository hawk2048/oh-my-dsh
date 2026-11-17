---
name: omd-autopilot
description: "自动驾驶：一个主控代理（你）跨目标轮次把单一目标持续做到已验证完成，用 Agent 子代理委派并以 TaskCreate 跟踪。适合低仪式感的端到端自主功能开发；触发词：autopilot / 自动驾驶 / 自主执行 / 自动驾驶式。"
---

# oh-my-workbuddy · Autopilot 自动驾驶

> **WorkBuddy 提示**：本文含 DSH 原生工具调用（goal/cancel/hud/ralph），仅作方法论参考。实际执行请跳到文末「WorkBuddy 适配」段。


一个主控代理（你）把一个目标从模糊一路推到「已验证完成」。对应 OMC 的 Autopilot 模式：**单领导、自主执行、持续到底**。

## 何时用

- 用户给了一个明确的最终目标："搭一个 REST API""重构认证模块"。
- 不想走 Team 的完整五阶段仪式，但目标要真正跑完、验证过。
- 用户说"autopilot""自动驾驶""自主执行""一路做完"。

## 核心：goal 工具循环

Autopilot 的地基是「跨多轮持续到完成的目标」——WorkBuddy 用 TaskCreate + Agent(resume) 实现。下方 DSH goal 段落仅作方法论参考，实际执行请看文末「WorkBuddy 适配」。

```
create_goal(objective)  →  [每一轮]  todo_write 推进  →  subagent 委托  →  update_goal 推进  →  完成
```

1. **建目标**：`create_goal(objective, { max_goal_rounds })`。objective 写成"可验收的完成目标"，不是任务描述——"通过 npm test 的认证模块重构"优于"重构认证"。
2. **拆计划**：立刻用 `TaskCreate/TaskUpdate` 列出实现步骤，每步一条；并行步骤可同时 `in_progress`。
3. **每轮推进**：本轮该做的做（`Agent` 工具 委托独立子任务、读代码、改文件），做完就把对应 todo 置 `completed`，用 `update_goal` 保持目标推进。
4. **持续到完成**：跨轮继续，别在单轮里硬塞。每个长目标都属于 goal 工具，不属于一次回答。
5. **委托**：能独立、能并行的子任务用 `Agent` 工具（后台并行），不要把上下文全烧在主控里。
6. **收尾**：只有「验证通过、验收标准满足」才 `update_goal complete`；用 `get_goal` 读当前 revision 再更新。

## 目标状态纪律

- `complete`：目标**真正达成**才标。别因为"做完了主要部分"就提前标。
- `blocked`：**同一阻塞条件持续至少 3 个 goal 轮**才标，并在 `blocked_reason` 里写明具体条件。"难/不确定/还有活"不算 blocked。
- 目标在会话恢复或 fork 后会解除武装：用户说"继续/接着做"时用 `update_goal resume` 重新武装。

## 与 Team / Ralph 的边界

- **Team**：多子系统、要分阶段规格。Autopilot 是单领导直推，不搞 prd 仪式。
- **Ralph**：要"每个完成都必须验证、不许静默半成品"的强验证循环，或用户明说 fresh-agent 迭代。
- Autopilot 内部可以顺手并行 `Agent` 工具，但主控权始终在你这一个代理手里。

## 收尾：HUD

每轮结束按 `omd-hud` 输出内联仪表盘：目标 + 轮次 + todo 进度 + 子代理状态。让用户始终看到"现在到哪了、还差什么"。

## 反模式

- 别在单轮里试图一次做完整个目标——goal 工具就是为"跨轮持续"设计的。
- 别把 goal 用在琐碎的单轮任务上。
- 别静默交付半成品——收尾前必须验证。


## WorkBuddy 适配（自动驾驶）— 已实测可行

WorkBuddy 无原生 `goal` 工具，但四个核心语义都有承接（2026-11-17 实测验证）。按以下流程执行：

### 建目标（对应 create_goal）

`TaskCreate` 建一条主任务，objective 写成**可验收的完成状态**——"通过 npm test 的认证重构"优于"重构认证"。
同时把 objective、验收标准、进度约定写进工作区文件（如 `AUTOPILOT.md`），这是跨轮的长期记忆。

### 拆计划（对应 todo_write）

`TaskCreate` 列出实现步骤，依赖关系用 `addBlockedBy`/`addBlocks`；互不依赖的步骤可同时 `in_progress`。

### 每轮推进（对应 goal 自动续轮）

- 用 `Agent` 启动后台子任务完成本轮工作。**它返回时会给出 `Task ID (for resume)`——务必记下这个 ID**。
- 下一轮用 `Agent(resume=<上轮 ID>)` 从上次 transcript 继续，不丢上下文。
  - 实测证据：启动 agent 写 `ROUND=1`，resume 同一 ID 后写 `ROUND=2`，文件内容确实从 1 变成 2。
- 2 个以上互不依赖的子任务，同一轮并行启动多个 `Agent`（`run_in_background=true`），别串行等。
- 每轮结束用 `TaskUpdate` 更新状态；跨轮继续，别在单轮硬塞完整目标。

### 验证与收尾（对应 update_goal complete）

- 派一个独立 `Agent` 作验证代理，对照 `AUTOPILOT.md` 的验收标准，只输出"通过"或"具体缺陷清单"，不接受模糊结论。
- 有缺陷 → 修复 → 再验；`completed` 只在验证全绿后标。
- `blocked` 需同一阻塞持续 ≥3 轮，并在任务描述里写明具体阻塞原因（"难/不确定"不算）。

### 跨会话自动续轮（对应 goal 的持久性，此处更强）

- 若目标需要跨天/跨会话自动推进：用 `automation_update` 创建定时任务，prompt 写明"读取 AUTOPILOT.md，resume 上轮 agent ID，推进一轮并更新进度"。
- 这是 DSH goal 做不到的——它的 target 会话恢复后会解除武装；WorkBuddy 的定时任务可真正跨会话自动触发。
- 新会话手动恢复时：`TaskList` 找未完成任务 → 读 `AUTOPILOT.md` 拿上轮 agent ID → `Agent(resume)` 继续。

### 已知缺口

- WorkBuddy **没有"同一会话内自动无限续轮"**——每轮需要你（主控）主动调一次 `Agent(resume)` 或定时任务触发。
- DSH 的 fresh-agent（每轮换全新代理）在 WorkBuddy 里是"同一个 agent 续跑"；若要完全 fresh，就不传 resume、改为从 `AUTOPILOT.md` 读全部上下文启动新 agent。

### 反模式（实测补充）

- 别只建 TaskCreate 就以为 goal 建好了——必须把验收标准写进工作区文件，否则 resume 后代理不知道"完成"长什么样。
- 别忘记记下 agent 返回的 `Task ID (for resume)`，丢了就只能 fresh 启动、丢失上下文。
