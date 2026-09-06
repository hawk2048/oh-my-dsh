---
name: omd-ultragoal
description: "Ultragoal: a durable multi-goal workflow — split one big outcome into multiple sub-goals, checkpoint each to workspace artifacts, and keep a ledger so progress survives turns and sessions. Use when the user asks to ultragoal/持久目标/多目标/长期目标/带台账推进."
---

# oh-my-dsh · Ultragoal 持久多目标

把一个**大结果**拆成多个子目标，逐个推进，每个子目标都写 checkpoint 工件 + 记台账，保证进度**跨轮、跨会话可恢复可审计**。对应 OMC 的 `ultragoal`。

## 何时用

- 目标太大、要跨很多轮、不能一次做完，且要能"接着上次继续"。
- 用户说"ultragoal""持久目标""多目标""长期目标""带台账""可恢复地推进"。

## 拆解 + checkpoint + 台账

```
create_goal(总目标) → 拆子目标(各有验收标准) → [实现子目标 → 验证 → 写checkpoint] × N → 全部完成
```

1. **总目标**：`create_goal` 写总 objective（可验收）。
2. **拆子目标**：用 `todo_write` 列出子目标，每个子目标一条、带验收标准，可并行的并行推进。
3. **每个子目标闭环**：实现 → 验证（对照该子目标的验收标准）→ **写 checkpoint 工件**：把进度、证据、产物路径写进工作区文件。
4. **台账**：维护一个 ledger 文件（如 `ULTRA_GOAL.md`），持续记录「子目标状态 / 完成证据 / 下一步 / 阻塞」，跨轮、跨会话都能据此恢复。
5. **收尾**：全部子目标完成 + 验证通过 → `update_goal complete`。

## 工件约定

- checkpoint：每个子目标完成后，落一个带验收证据的工件（测试输出、产物文件路径、结论）。
- ledger：单一事实源，会话恢复后先读它，再继续——别只靠记忆。

## 与其它模式的关系

- `autopilot` = 单领导直推一个目标到底；`ultragoal` = 多子目标 + 显式 checkpoint/台账，强调**持久与可恢复**。
- 每个子目标内部仍可走 `execute` → `review` → `verify`。
- 需要"每个完成都必须验证、不许半成品"时，叠加 `ralph` 的强验证纪律。

## 收尾：HUD

用 `omd-hud` 输出：子目标进度表（状态/验收/checkpoint）+ 台账状态。让"哪些子目标完成、哪些还欠证据"可见。

## 反模式

- 别把大目标一次硬做——先拆子目标。
- 别不写 checkpoint 就指望跨轮恢复——工件是恢复的唯一依据。
- 别在子目标没验证时就标完成。
