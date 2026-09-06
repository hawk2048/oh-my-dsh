---
name: omd-remember
description: "Remember: persist durable notes, decisions, and facts to a workspace memory file so they survive compaction and later sessions. Use when the user says remember / 记住 / 记下来 / 别忘 / 存个备忘 / 记录这个决定."
---

# oh-my-dsh · Remember 跨会话记忆

把**该跨轮/跨会话存续**的信息落到工作区记忆文件，避免被压缩或新会话冲掉。对应 OMC 的 `remember` / `note` 工具 skill。

## 何时用

- 用户说「记住这个」「别忘」「记一下这个决定/约定/事实」。
- 有需要在后续会话继续用到的决策、约定、环境事实。

## 记忆纪律

1. **落盘**：写到工作区里的记忆文件（如 `OMD_MEMORY.md` 或 `.omd/memory.md`），别只留在对话里——对话会被压缩。
2. **结构化**：每条含「标签 + 内容 + 日期 + 为什么重要」，便于检索。
3. **区分**：事实（环境/路径/账号无关的约定）vs 决策（为什么这么选）vs 待办（后续要做的）。
4. **取用**：新会话开头或遇到「之前说过……」时，先 `read` 记忆文件再答。

## 与其它模式的关系

- `remember` 存的是「跨会话事实」，`omd-wiki` 存的是「成体系的知识」——单条零散事实用 remember，成页文档用 wiki。
- 记忆文件本身也要遵守 `omd-minimal-code-discipline`：只记值得记的，别堆噪音。

## 收尾：HUD

用 `omd-hud` 输出记忆摘要：`table`（标签/内容摘要/类型/日期）+ `keyvalue`（记忆文件路径）。让「记了什么、存哪了」一眼可见。

## 反模式

- 别把记忆只留在对话正文——不落盘就丢。
- 别把大段代码/文档当「记忆」塞进去——那该进 wiki 或仓库文件。
- 别重复记已经存在的条目，先查再写。
