---
name: omd-deep-interview
description: "Deep Interview: Socratic requirement clarification before any code — converge a vague idea across weighted dimensions using ask_user_question. Use when requirements are vague/ambiguous, or the user says deep-interview/深度访谈/先澄清需求/需求访谈."
---

# oh-my-dsh · Deep Interview 需求澄清

在写任何代码之前，用苏格拉底式追问把模糊想法收敛成可执行的规格。对应 OMC 的 Deep Interview 模式。

## 何时用

- 需求模糊："我想做个任务管理应用"。
- 用户对设计摇摆、想被引导着想清楚。
- 用户说"deep-interview""深度访谈""先澄清""访谈"。
- 不要在有明确规格的任务上做访谈——那是浪费时间。

## 澄清维度（加权）

| 维度 | 要问清的问题 | 权重 |
|------|------------|------|
| 目标 | 最终要解决谁的什么问题？成功长什么样？ | 高 |
| 范围 | 包含什么、**明确不包含**什么（non-goals）？ | 高 |
| 约束 | 技术栈、性能、安全、合规、时间/成本硬约束？ | 高 |
| 验收 | 怎么判断"做完了"？可度量的标准是什么？ | 高 |
| 优先级 | 若只能先做一件，先做什么？哪些可砍？ | 中 |
| 数据 | 数据从哪来？格式、量级、敏感度？ | 中 |
| 风险 | 最可能翻车的地方？边界和失败模式？ | 低 |

## 提问纪律（用 ask_user_question）

- 每轮最多 2–4 个问题，每个问题给 2–4 个候选选项（可多选），并说明每个选项的取舍。
- 问题必须**收敛**：问完一轮，维度就从"未知"变"已知"，别原地打转。
- 只问**你无法通过检查代码库得到**的用户决策；能在仓库里查出来的事实不要拿去问。
- 问题要具体，不要"你想要什么？"这种空泛问法——给候选方向。
- 每个问题带一个稳定 `id`，答案会原样回传。

```js
ask_user_question({ questions: [
  { id: 'scope', header: '范围', question: '第一版要覆盖哪些？',
    options: [
      { label: 'MVP：仅核心闭环', description: '最快验证价值，其余后续迭代' },
      { label: '含协作与权限', description: '复杂度明显上升，工期翻倍' }
    ] },
  { id: 'acceptance', header: '验收', question: '怎么算"做完"？',
    options: [
      { label: '可演示的端到端闭环', description: 'happy path 全通即可' },
      { label: '测试覆盖 + CI 全绿', description: '质量门槛更高' }
    ] }
] })
```

## 流程

1. 先扫一眼仓库/现状（`glob`/`read`/`grep`），把"能查出来的事实"和"必须问用户的决策"分开。
2. 按权重从高到低，每轮问 2–4 个问题。
3. 每轮结束，把已确定的点回写成一份"需求快照"（简短），让用户确认没跑偏。
4. 所有高权重维度都清晰后，输出最终规格：目标 / 范围 / 非目标 / 约束 / 验收标准 / 优先级 / 数据 / 风险。
5. **拿到规格才开始动手**——之前的任何对话都只是澄清，不是开工许可。

## 收尾

最终规格用 `dsh-ui` 的 `keyvalue`/`table` 呈现（见 `omd-hud`），并明确说"以下规格确认后即开始实现"。

## 反模式

- 别一次甩 10 个问题。
- 别问能靠读仓库回答的问题。
- 别把用户"嗯/可以"当成完整需求确认——关键维度没问清就继续问。
