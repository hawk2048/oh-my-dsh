# oh-my-dsh 架构说明

## 平面决策：为什么这一切都在一个 agent preset 里

DSH 的能力 = `cordis.yml` 里的插件行。两个平面：

- **宿主组合（Host）**：注册表本身（`tools`/`systemPrompt`/`agents`/`agent-loop`/`sessions`）、跨会话的持久化/沙箱/模型路由/子代理注册表。
- **Agent preset**：单会话对注册表的贡献——工具、persona、提示段、压缩策略。

oh-my-dsh **不发布任何服务**，也不引入宿主运行时。它只做两件事：

1. **persona**（`dsh-persona` 行）告诉代理存在这套编排词汇；
2. **skill 打包**（`skill-filesystem` 行的 `customSkillDirs`）把 29 个 `omd-*` skill 挂进该 preset 的 skill 目录层。

所以整件事是一个 agent preset，而不是宿主改动或动态插件。这是它"零运行时风险"的根本原因。

## skill 如何随 preset 打包

`agent.cordis.yml` 里的 skill 行：

```yaml
- id: skill-filesystem
  name: '@deepseek-ai/dsh-skill-filesystem'
  config:
    customSkillDirs:
      - !!js "process.getBuiltinModule('node:url').fileURLToPath(new URL('skills/', baseUrl))"
```

- `baseUrl` 是 Loader 上下文中**该 preset 自己的目录**，所以 `skills/` 永远解析到 preset 安装处的 `skills/` 目录。
- 这与 DSH 自带 `cordis` preset 打包 `editing-cordis-compositions` 的方式**完全一致**（已证明可用的模板）。
- skill 注册表分层：该 preset 的 `skill-filesystem` 只往**本 preset 那一层**注册，无需 isolate realm；代理的合并目录仍包含部署全局注册的 skill（仓库插件）。

## 编排模式 → 原生原语映射

| omd 模式 | 原语 | 为什么这个原语 |
|-----------|------|----------------|
| Plan | 只读探索（read/grep/glob/web_search）+ 并行 `subagent` 调研 | 先扎根真实仓库再定方案 |
| Execute | `subagent`/`subagent_fork` 并行扇出 + `todo_write` | 子代理天然并行，后台自动回传 |
| Review | `subagent_fork` 独立评审 | 继承上下文但不共用作者立场，写评分离 |
| Verify | `pwsh`/`bash` 测试 + `subagent` 复核 | 用真实命令/证据证明达标 |
| Team | `workflow`（`pipeline`/`parallel`/`phase`） | 原生就支持多阶段、结构化产物传递、进度分组 |
| Autopilot | `goal`（`create_goal`/`update_goal`）+ `todo_write` + `subagent` | goal 是"跨轮持续到完成"的原生目标机制 |
| Ralph | `ralph`（fresh-agent 循环）或 `goal`+验证代理手动循环 | DSH 原生 `ralph` = fresh-agent + 共享工作区记忆 |
| Deep Interview | `ask_user_question`（多问题/选项/多选） | 原生结构化提问，答案按 id 回传 |
| Ralplan | 并行 `subagent` 草案 + 仲裁 `subagent` 收敛 | 多视角独立出草案，再显式裁决分歧 |
| Research | `web_search`/`web_fetch` + 并行 `subagent` | 每条结论带来源，可交叉验证 |
| Autoresearch | `goal` + 评估子代理循环 | 评估驱动、有界改进、达标退出 |
| Ultragoal | `goal` + `todo_write` + checkpoint 工件 | 多子目标 + 台账，跨轮跨会话可恢复 |
| TDD | `pwsh`/`bash` 测试 + `todo_write` | red-green-refactor 由真实命令驱动 |
| Deepsearch | `grep`/`glob`/`read` | 代码库问题本地定位，证据带 file:line |
| Deep-analyze | 并行 `subagent` 多视角 | 架构/安全/性能分开看，显式权衡 |
| Ultrathink | 纯推理（先不调工具） | 边界/备选/失败模式想透再动手 |
| AI-slop-cleaner | `review` + `edit` 精简 | 删水分保语义 |
| Doctor | 只读诊断（glob/grep/read） | 自检 skill/命令/挂载 |
| Debug | `pwsh`/`bash` 复现 + `read`/`grep` 定位 | 复现→定位→最小修复→回归 |
| Release | git + 测试 + `pnpm pack` | 版本→changelog→tag→产物 |
| Remember | 工作区记忆文件 | 跨轮跨会话存续 |
| Cancel | `update_goal` pause + `interrupt_agent` + `job_kill` | 干净停掉在跑模式 |
| Minimal-code-discipline | 纯纪律（YAGNI 阶梯） | 最小正确 diff |
| External-context | `web_fetch`/`read` | 仓库外上下文拉取 |
| Visual-verdict | `read_image` 对比 | 视觉 QA 结构化判定 |
| Skillify | 写 `SKILL.md` | 从会话沉淀可复用 skill |
| Wiki | 工作区 markdown | 知识库维护 |
| Help | `glob`/`read` 实时列清单 | 能力索引（技能/命令总览） |
| HUD | `dsh-ui` 围栏（genui） | 内联结构化 UI，无需 Client 插件 |

## 为什么 HUD 用 genui 而不是 Client Cordis 插件

OMC 的 HUD 是 CLI 状态栏。DSH 是 Web GUI，且已有 `genui` skill 渲染内联 `dsh-ui` 组件。用 `dsh-ui` 实现 HUD：

- 零审批、零 Client 插件、只在本 preset 生效（skill 驱动的行为约定）；
- 仪表盘就是回答的一部分，随每次阶段完成自然更新；
- 若未来要**常驻状态栏**（真正的 HUD statusline），那才需要 Client Cordis 插件往 Slot 注册 UI——那是本项目的可选增量，不是当前范围。

## 斜杠命令如何随 preset 打包

`/omd-plan` `/omd-execute` `/omd-review` `/omd-verify` `/omd-team` `/omd-autopilot` `/omd-ralph` `/omd-deep-interview` `/omd-ralplan` `/omd-research` `/omd-autoresearch` `/omd-ultragoal` 由 `commands/omd-commands.mjs` 提供，是一个随 preset 打包的 ESM 插件：

这 12 条之外，其余 17 个 skill（`hud`、`tdd`、`deepsearch`、`deep-analyze`、`ultrathink`、`ai-slop-cleaner`、`doctor`、`debug`、`release`、`remember`、`cancel`、`minimal-code-discipline`、`external-context`、`visual-verdict`、`skillify`、`wiki`、`help`）是**纯自然语言触发的 skill**（无斜杠命令），靠 skill 的 `description` 写清触发词，由模型自动加载。

- 组合里用**相对路径**引用：`name: './commands/omd-commands.mjs'`。Loader 的 `classifyRowSpecifier` 把 `.` 前缀归类为 `preset`，按 preset 自身目录（`baseUrl`）解析——所以命令生产者随 preset 走，装到哪都找得到。
- 插件 `inject: ['commands']`，复用 DSH 自带的命令注册表（与内置 `/goal` 的 `command-goal` 同一机制），**不引入新服务**。
- 每个命令的 handler 把任务作为一条用户消息提交给模型（`invocation.agent.followup({ role:'user', source:{kind:'user'}, content:[{type:'text',text}], id })`，语义 = `send(message, "next-turn", true)`，即唤醒模型进入下一轮），再返回一条直接 UI 确认（不进入模型请求）。
- **刻意不 import** `createUserMessage`：本地 preset 目录无法走 node_modules 向上解析到 harness 的 `@deepseek-ai/dsh-llm`（overlay 解析器只覆盖 profile/loader 入口模块），因此手工构造等价的 UserMessage（role/source/content/id 四个字段与 `createUserMessage` 产出一致）。

## 不变式 / 纪律

- preset **不发布服务**，所以没有 isolate realm 的坑（所有工具行都是纯消费者，挂宿主注册表）。
- `delegation` 组保留 `isolate: workflowEngine`，与 `standard` 一致——`workflows` 服务只被代理读，必须私有到每个会话。
- 不改宿主动画、不改沙箱/审批、不装可选 provider（codex/claude-code 行保持 `disabled`）。
- skill 是"行为约定"：它们教代理如何用原生工具编排，而不是替代这些工具。

## 从 standard 到 oh-my-dsh 的 diff

| 位置 | standard | oh-my-dsh |
|------|----------|-----------|
| `persona` 文本 | 一行身份 | 身份 + 编排词汇说明 |
| `skill-filesystem` | 无 config（默认本地发现） | `customSkillDirs` 指向 preset 的 `skills/` |
| `command-omd` | （不存在） | 相对路径挂载 `./commands/omd-commands.mjs`，注册 12 条斜杠命令 |
| 其余全部行 | — | **逐字节一致** |
