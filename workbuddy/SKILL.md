---
name: oh-my-workbuddy
description: "多智能体编排层：把 oh-my-dsh 的 30 个 omd skill 迁移到 WorkBuddy。核心流水线 Plan→Execute→Review→Verify，加 Team/Autopilot/Ralph/Deep-Interview/Ralplan/Research/Autoresearch/Ultragoal，以及表达纪律（pyramid/plain-writing/ai-slop-cleaner）与工具 skill。触发词：编排 / 规划 / 执行 / 评审 / 验证 / team / autopilot / ralph / 金字塔 / 说人话 / 深度访谈 / 调研 / omd。"
---

# oh-my-workbuddy

> 由 hawk2048 的 [oh-my-dsh](https://github.com/hawk2048/oh-my-dsh) 迁移而来。30 个子 skill 沿用 `omd-*` 命名与触发词，工具调用已映射到 WorkBuddy 环境。

## 使用方式

直接说触发词即可，例如「先规划一下」「autopilot 搭个 API」「把这段整理成金字塔结构」。每个子 skill 会按 description 自动触发。

## 核心流水线

```
plan → execute → review → verify
```

## 30 个子 skill

| skill | 说明 |
|---|---|
| [omd-ai-slop-cleaner](omd-ai-slop-cleaner/SKILL.md) | 去AI味：清除代码或文本里 AI 生成的废话、套话、冗余注释与含糊表述。触发词：ai-slop / 去废话 / 精简 / 去水 / 太啰嗦 … |
| [omd-autopilot](omd-autopilot/SKILL.md) | 自动驾驶：一个主控代理（你）跨目标轮次把单一目标持续做到已验证完成，用子代理委派并以 todo_write 跟踪。适合低仪式感的端到端自主功… |
| [omd-autoresearch](omd-autoresearch/SKILL.md) | 自动调研改进：有界的评估器驱动改进循环——先定额度、分节落笔、一节一闸、独立打分、定点改到达标。产出调研报告/行业研究/方案对比时用它，也用… |
| [omd-cancel](omd-cancel/SKILL.md) | 取消：干净地停止进行中的编排模式——暂停目标轮次、中断后台子代理、终止任务——并留下干净的检查点。触发词：cancel / 停止 / 停下 … |
| [omd-debug](omd-debug/SKILL.md) | 调试：复现失败，用证据定位根因，最小化修复，并用回归测试锁定。触发词：debug / 调试 / 报错 / 崩溃 / 为什么失败 / 修 bu… |
| [omd-deep-analyze](omd-deep-analyze/SKILL.md) | 深度分析：对代码、架构或问题做多角度、有证据支撑的分析。需要透彻推理而不是快速修补时使用；触发词：deep-analyze / 深度分析 /… |
| [omd-deep-interview](omd-deep-interview/SKILL.md) | 深度访谈：写代码前用苏格拉底式追问澄清需求——用 ask_user_question 在加权维度上收敛模糊想法。需求模糊或有歧义时使用；触发… |
| [omd-deepsearch](omd-deepsearch/SKILL.md) | 代码库聚焦检索：定位本地代码库中的实现、调用点、定义与数据流。问「东西在哪」而非「怎么做」时使用；触发词：deepsearch / 找一下 … |
| [omd-doctor](omd-doctor/SKILL.md) | 自检诊断：检查 oh-my-dsh 装得对不对——核对技能目录、/omd-* 斜杠命令与 preset/bundle 挂载——并诊断某个模式… |
| [omd-execute](omd-execute/SKILL.md) | 执行：按已确认的计划实现——多文件改动/重构/调试交给执行子代理（后台并行），琐碎改动直接做，用 todo_write 跟踪。作为 plan… |
| [omd-external-context](omd-external-context/SKILL.md) | 外部上下文：从仓库之外拉取上下文——URL、文档、issue、包 README——在推理或编辑前先做摘要。用户给出 URL/issue/文档… |
| [omd-help](omd-help/SKILL.md) | 帮助：展示 oh-my-dsh 菜单——全部 omd-* 技能与 /omd-* 命令，按分类分组并说明各自触发方式。触发词：help / 帮… |
| [omd-hud](omd-hud/SKILL.md) | HUD：把编排进度渲染成内联 dsh-ui 仪表盘——统计卡片、进度条、时间线与子代理状态表。用于实时展示任意 oh-my-dsh 模式的进… |
| [omd-minimal-code-discipline](omd-minimal-code-discipline/SKILL.md) | 最小改动纪律：做最小而正确的改动——先确认存在、能复用就不新写、最短的正确修改。触发词：minimal / 最小改动 / YAGNI / 别… |
| [omd-plain-writing](omd-plain-writing/SKILL.md) | 说人话：生成期的写作纪律——落笔前先定具体事实，不写对偶拔高句、自我更正、生造借代与两字缩写，报告先给结论；输出前过八条自查。触发词：说人话… |
| [omd-plan](omd-plan/SKILL.md) | 规划：先用只读方式探索（读/搜索/静态分析），再产出具体的实现计划（带依赖的任务拆解 + 验收标准 + 文件级改动）。不写代码。作为 pla… |
| [omd-pyramid](omd-pyramid/SKILL.md) | 金字塔结构化表达：把回答/汇报/方案/文档按 Minto 金字塔重组——结论先行、以上统下、归类分组(MECE)、逻辑递进，用 SCQA 开… |
| [omd-ralph](omd-ralph/SKILL.md) | 拉夫：持久验证/修复循环，不留静默半成品。显式全新代理迭代用原生 ralph 工具，否则用手动 goal+verify 循环。任务必须完整完… |
| [omd-ralplan](omd-ralplan/SKILL.md) | 共识规划：多视角并行规划——派出多个独立规划子代理从不同角度切入，再运行结构化审议裁决分歧，收敛为一份共识计划。适合高风险或需求模糊、需要多… |
| [omd-release](omd-release/SKILL.md) | 发布：走完仓库的发布流程——版本号、changelog、测试、打 tag、构建——并产出发布检查清单。触发词：release / 发布 / … |
| [omd-remember](omd-remember/SKILL.md) | 记住：把持久化的笔记、决策与事实写入工作区记忆文件，让它们在压缩和后续会话中留存。触发词：remember / 记住 / 记下来 / 别忘 … |
| [omd-research](omd-research/SKILL.md) | 调研：查证开放问题并返回有据结论——每条结论都有来源背书。并行派出研究子代理（web_search/web_fetch + 仓库文档），再综… |
| [omd-review](omd-review/SKILL.md) | 评审：独立的评审环节，评估实现——绝不在同一上下文里自我背书。交给评审子代理（subagent_fork 或 subagent）、读 dif… |
| [omd-skillify](omd-skillify/SKILL.md) | 技能化：把当前会话里可复用的流程提炼成新的可复用 SKILL.md。触发词：skillify / 把这段流程存成 skill / 沉淀成技能… |
| [omd-tdd](omd-tdd/SKILL.md) | 测试驱动开发：先写会失败的测试，再做最小实现，然后重构（红-绿-重构）。触发词：tdd / 测试驱动 / 先写测试 / red-green … |
| [omd-team](omd-team/SKILL.md) | 团队多智能体编排：运行分阶段流水线（team-plan → team-prd → team-exec → team-verify → tea… |
| [omd-ultragoal](omd-ultragoal/SKILL.md) | 持久目标：持久的多目标工作流——把一个大成果拆成多个子目标，各自 checkpoint 到工作区工件，并维护台账让进度跨回合、跨会话存活。触… |
| [omd-ultrathink](omd-ultrathink/SKILL.md) | 深度思考：行动前穷举边界情况、权衡备选方案、预演失败模式。触发词：ultrathink / 深度思考 / 想清楚 / 多想想 / 别急着动手… |
| [omd-verify](omd-verify/SKILL.md) | 验证：宣称完成前先验证——跑测试/构建、对照验收标准、收集证据（小规模内联，大规模/安全走子代理），失败则迭代。作为 plan→execut… |
| [omd-visual-verdict](omd-visual-verdict/SKILL.md) | 视觉裁决：把截图或渲染输出与参考对照，给出结构化的通过/失败裁决与具体差异。触发词：visual-verdict / 对比截图 / 看下 U… |
| [omd-wiki](omd-wiki/SKILL.md) | 知识库：维护工作区里的轻量 markdown 知识库——创建、更新、交叉链接页面，并让它们与代码保持一致。触发词：wiki / 记到知识库 … |

## 工具映射（omd → WorkBuddy）

| DSH 原语 | WorkBuddy |
|---|---|
| `subagent` / `subagent_fork` | `Agent` 工具 |
| `workflow` 流水线 | `TaskCreate` + `Agent` 并行 |
| `todo_write` | `TaskCreate/TaskUpdate` |
| `ralph` / `goal` | `Agent(resume)` + 工作区文件 + `TaskCreate` |
| `dsh-ui` HUD | `show_widget` 可视化 |
| `/omd-*` 斜杠命令 | 无对应，改用自然语言触发 |
