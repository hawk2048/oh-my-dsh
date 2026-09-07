---
name: omd-hud
description: "HUD：把编排进度渲染成内联 dsh-ui 仪表盘——统计卡片、进度条、时间线与子代理状态表。用于实时展示任意 oh-my-dsh 模式的进度（plan/execute/review/verify/team/autopilot/ralph/deep-interview/ralplan/research/autoresearch/ultragoal/tdd/deepsearch/deep-analyze/ultrathink/ai-slop-cleaner/debug/release/remember/cancel/minimal-code-discipline/external-context/visual-verdict/skillify/wiki/help/doctor）。"
---

# oh-my-dsh · HUD 实时进度仪表盘

把编排进度渲染成内联 `dsh-ui` 仪表盘，嵌在回答正文里。对应 OMC 的 HUD 状态栏。渲染语法见 `genui` skill——本节只讲编排场景该怎么摆。

## 何时用

任何 oh-my-dsh 模式跑起来后，**每个阶段/每轮结束**都输出一段 HUD，让用户一眼看到：目标、进度、子代理状态、下一步。别等全跑完才汇报。

## 仪表盘骨架

一个 HUD 块由「标题 + stat 概览 + 进度 + 子代理状态表 + 下一步」组成：

```dsh-ui
{"title":"Autopilot · 重构认证模块","gap":14,"items":[
  {"type":"row","wrap":true,"items":[
    {"type":"stat","label":"目标轮次","value":"3 / 6"},
    {"type":"stat","label":"子代理","value":"2 运行中"},
    {"type":"stat","label":"通过 / 缺陷","value":"14 / 2"}
  ]},
  {"type":"progress","label":"整体进度","value":62},
  {"type":"table","columns":["代理","任务","状态"],
   "rows":[["team-plan","拆解任务","done"],["exec-auth","实现认证","running"],["exec-ui","实现界面","queued"]]},
  {"type":"callout","tone":"info","title":"下一步","content":"等待 exec-auth 完成后进入 verify 阶段"}
]}
```

## 每个模式用什么组件

| 模式 | 推荐组件 |
|------|---------|
| Plan | `table`（任务/依赖/验收）+ `steps`（流水线位置） |
| Execute | `progress`（todo 进度）+ `table`（子代理状态） |
| Review | `table`（issues：位置/严重度/状态）+ `stat`（通过/缺陷） |
| Verify | `table`（验收标准逐条通过/失败）+ `stat`（通过计数） |
| Team | `steps`（五阶段）+ `table`（阶段→状态）+ `progress` |
| Autopilot | `stat`（轮次/进度）+ `progress` + `todo` 进度 |
| Ralph | `stat`（通过/缺陷/轮次）+ `timeline`（fix loop 轨迹） |
| Deep Interview | `keyvalue`/`table`（维度→已澄清/待澄清）+ `progress`（澄清度） |
| Ralplan | `table`（草案/分歧/裁决）+ `stat`（已裁决/未决） |
| Research | `table`（结论/证据/来源）+ `stat`（来源计数） |
| Autoresearch | `stat`（轮次/评分）+ `table`（差距清单） |
| Ultragoal | `table`（子目标→状态/checkpoint）+ `progress` |
| TDD | `steps`（红绿重构）+ `table`（用例→状态） |
| Deepsearch | `table`（符号/文件/行号/角色） |
| Deep-analyze | `table`（视角/发现）+ `table`（方案权衡） |
| Ultrathink | `table`（方案对比）+ `list`（风险） |
| AI-slop-cleaner | `table`（删除条目/前后字数） |
| Doctor | `table`（检查项/状态/证据） |
| Debug | `timeline`（复现→定位→修复→验证）+ `table`（根因/修复/回归） |
| Release | `table`（检查项/状态）+ `steps`（版本→changelog→tag→产物） |
| Remember | `table`（标签/摘要/类型）+ `keyvalue`（记忆文件路径） |
| Cancel | `table`（对象/动作/结果）+ `callout`（恢复方式） |
| Minimal-code-discipline | `table`（文件/改动/必要性）+ `stat`（净增删行） |
| External-context | `table`（来源/关键事实）+ `list`（引用 URL） |
| Visual-verdict | `table`（维度/期望/实际/通过?）+ `stat`（通过/失败） |
| Skillify | `keyvalue`（新 skill/路径）+ `table`（步骤/触发词） |
| Wiki | `table`（页面/增改/要点）+ `keyvalue`（知识库路径） |
| Help | `table`（分类/技能/用途）+ `table`（命令→模式） |

## 常用组件速查（详见 genui）

- `stat`: `{"type":"stat","label":"…","value":"…","delta":"+12%"}`（`-` 开头自动红、`+` 绿）
- `progress`: `{"type":"progress","label":"…","value":62}`
- `table`: `{"type":"table","columns":[…],"rows":[[…]]}`
- `steps` / `timeline`: 流程与轨迹
- `badge` / `callout`: 状态徽标与提示
- `mermaid`: 阶段流程图/依赖图

## 纪律

- HUD 是**进度快照**，不是最终总结——每个阶段/每轮都更新，状态要真实（运行中的写 running，别虚报 done）。
- 状态词统一：`done` / `running` / `queued` / `failed`。
- HUD 块照常穿插在文字前后，组件就是回答的一部分，不是单独的工具调用。
- 别在 HUD 里塞巨量数据——只放「决策所需」的关键指标。
