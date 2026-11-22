---
name: omd-help
description: "帮助：展示 oh-my-dsh 菜单——全部 omd-* 技能与 /omd-* 命令，按分类分组并说明各自触发方式。触发词：help / 帮助 / omd 能做什么 / 有哪些命令 / 有什么模式 / usage。"
---

# oh-my-dsh · Help 使用索引

把 oh-my-dsh 的完整能力面展示给用户：所有 skill + 所有斜杠命令 + 触发方式。对应 OMC 的 `omc-help`（Usage guide）。

## 何时用

- 用户问「omd 能做什么」「有哪些模式/命令」「help」。
- 会话开始或用户想要能力总览时。

## 展示纪律

1. **列实时清单**：用 `glob` 列 `skills/*/SKILL.md`，读每个的 frontmatter `name` + `description` 首句，别凭记忆硬背——清单会随版本变。
2. **分类呈现**：编排流水线（plan/execute/review/verify/team/autopilot/ralph/deep-interview/ralplan/research/autoresearch/ultragoal/cancel/hud）/ 表达与推理纪律（pyramid/plain-writing/deep-analyze/ultrathink/ai-slop-cleaner/first-principles/contradictions/challenge）/ 工程纪律（tdd/deepsearch/debug/release/minimal-code-discipline/observe）/ 事后与留痕（postmortem/decision-record）/ 工具 skill（remember/external-context/visual-verdict/skillify/wiki/doctor/help），每类给「技能名 + 一句话用途」。
3. **命令面**：20 条 `/omd-*` 斜杠命令（plan/execute/review/verify/team/autopilot/ralph/deep-interview/ralplan/research/autoresearch/ultragoal/pyramid/plain + first-principles/contradictions/challenge/postmortem/decision-record/observe）。说明两者区别：**斜杠命令 = 直接进对应模式；自然语言 = 说清需求自动触发对应 skill**。
4. **给入口**：按用户目标指路——「要规划」→ `omd-plan`，「多人拆任务」→ `omd-team`，「修 bug」→ `omd-debug`，「发版」→ `omd-release`，「讲不清楚/要写汇报」→ `omd-pyramid`；「拆惯性/从事实重建」→ `omd-first-principles`，「问题太多先抓重点」→ `omd-contradictions`，「方案采纳前挑毛病」→ `omd-challenge`，「白干了要复盘」→ `omd-postmortem`，「记下为什么这么定」→ `omd-decision-record`，「查实际在跑什么」→ `omd-observe`。

## 与其它模式的关系

- 用户说不清要哪个模式时，先用本 skill 给总览，再按目标推荐具体模式。
- 装坏了/不生效 → `omd-doctor`；要把新流程沉淀 → `omd-skillify`。

## 收尾：HUD

用 `omd-hud` 输出能力总览：`table`（分类/技能/用途）+ `table`（命令→模式）。让「有什么、怎么触发」一眼可见。

## 反模式

- 别凭记忆硬背技能清单——用 `glob` 实时列，版本会变。
- 别只列名字不给「怎么触发」——每条都带触发方式。
- 别把 help 写成 README 全文——只给决策所需的索引。
