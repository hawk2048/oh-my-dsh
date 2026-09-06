---
name: omd-minimal-code-discipline
description: "Minimal-code-discipline: make the smallest correct diff — existence-first, reuse before writing, shortest correct change. Use when the user says minimal / 最小改动 / YAGNI / 别过度设计 / 只改必要的 / 能复用就复用."
---

# oh-my-dsh · Minimal-code-discipline 最小改动纪律

用**最短的正确 diff** 达成目标：先确认已有，能复用就复用，不写投机抽象。对应 OMC 的 `minimal-code-discipline`（YAGNI-ladder 写作时纪律）。

## 何时用

- 用户要求「最小改动」「别过度设计」「只改必要的」。
- 任何改代码的场景，作为默认写作纪律兜底。

## 纪律阶梯

1. **存在优先**：动手前先 `grep`/`glob` 确认有没有现成实现、工具函数、约定——已存在的就不写。
2. **复用优先**：能调已有函数/类型/配置就别重写。
3. **最短正确 diff**：只改达成目标必须改的那几行，不顺手重构、不格式化无关代码。
4. **YAGNI**：不为「以后可能要」提前抽象；需要时再提炼，提炼要有第二个使用点作依据。

## 与其它模式的关系

- `omd-execute` 的实现阶段应默认套用本纪律，避免 diff 膨胀。
- `omd-review` 要专门盯「超出必要范围的改动」。
- 与 `omd-ai-slop-cleaner` 互补：一个管「改得少」，一个管「写得干净」。

## 收尾：HUD

用 `omd-hud` 输出改动范围：`table`（文件/改动/是否必要/能否更小）+ `stat`（净增删行数）。让「改了多少、为什么不能再小」一眼可见。

## 反模式

- 别为了「整洁」顺手改与目标无关的代码。
- 别在没有第二个使用点时就抽象出通用层。
- 别把「最小」当成「偷懒跳过必要处理」——正确性优先于行数。
