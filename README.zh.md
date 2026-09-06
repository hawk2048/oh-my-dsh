# oh-my-dsh

[![npm version](https://img.shields.io/npm/v/@hawk2048/oh-my-dsh?color=cb3837)](https://www.npmjs.com/package/@hawk2048/oh-my-dsh)
[![GitHub stars](https://img.shields.io/github/stars/hawk2048/oh-my-dsh?style=flat&color=yellow)](https://github.com/hawk2048/oh-my-dsh/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![dsh-plugin](https://img.shields.io/badge/dsh-plugin-orange)](https://github.com/topics/dsh-plugin)

**面向 DeepSeek Harness (DSH) 的多智能体编排层** —— 把 [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 的编排模式，映射到 DSH 原生原语（`workflow` / `subagent` / `ralph` / `goal`）之上。

> 两种触发方式：**自然语言**（29 个随 preset 打包的编排 skill，代理自动加载）+ **斜杠命令**（12 条，敲 `/omd` 即弹出候选）。启动一次会话，编排能力就位。

[English](README.md) | 中文

## 快速开始

一条命令装好全部 29 个 skill + 12 条 `/omd-*` 命令（等价 OMC 的插件市场安装）：

```sh
dsh plugin --profile web add github:hawk2048/oh-my-dsh
```

或从 npm 安装（等价 OMC 的 npm i -g）：

```sh
dsh plugin --profile web add @hawk2048/oh-my-dsh
```

装完重启 profile，敲 `/omd` 弹出命令候选；或直接用自然语言（「先规划一下」「autopilot 搭个 API」）触发对应 skill。

## 要求

- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（`dsh` CLI）
- [pnpm](https://pnpm.io)（`dsh plugin` 底层转发给 pnpm）

## 为什么用 oh-my-dsh

- **零配置**——一条 `dsh plugin add` 装好全部；bundle 自注册，无需安装向导。
- **Team 优先编排**——Team 是标准分阶段流水线（`team-plan → team-prd → team-exec → team-verify → team-fix`），构建在 DSH 原生 `workflow` 上。
- **自然语言交互**——说清需求即可，29 个 `omd-*` skill 自动加载，无需记命令。
- **自动并行**——复杂任务扇出到并行 `subagent`。
- **持久执行**——Ralph / Autopilot / Ultragoal 不达验证完成不罢休（原生 `ralph` 循环 + `goal` 跨轮目标）。
- **零运行时开销**——不引入新宿主工具或运行时，只是 DSH 原生原语之上的 skill，保留 DSH 自己的模型路由与沙箱。
- **从经验中学习**——`omd-skillify` 提取可复用 skill；`omd-remember` 跨会话持久记忆。
- **实时可见**——内联 HUD 渲染实时 `dsh-ui` 进度仪表盘。

## 与 oh-my-claudecode 的对应关系

对齐 OMC **v5.3.0** 的命令面（核心流水线 `plan → execute → review → verify` + 保留模式）：

| OMC 工作流 | oh-my-dsh skill | DSH 原生载体 |
|-----------|-----------------|--------------|
| Plan（规划） | [`omd-plan`](skills/omd-plan/SKILL.md) | 只读探索 + `subagent` 并行调研 |
| Execute（执行） | [`omd-execute`](skills/omd-execute/SKILL.md) | `subagent` 并行 + `todo_write` |
| Review（评审） | [`omd-review`](skills/omd-review/SKILL.md) | `subagent_fork` 独立评审 |
| Verify（验证） | [`omd-verify`](skills/omd-verify/SKILL.md) | `pwsh`/`bash` 测试 + `subagent` 复核 |
| Team（分阶段流水线） | [`omd-team`](skills/omd-team/SKILL.md) | `workflow` + `subagent` |
| Autopilot（自动驾驶） | [`omd-autopilot`](skills/omd-autopilot/SKILL.md) | `goal` + `todo` + `subagent` |
| Ralph（持久验证循环） | [`omd-ralph`](skills/omd-ralph/SKILL.md) | `ralph` + `goal` 验证循环 |
| Deep Interview（需求澄清） | [`omd-deep-interview`](skills/omd-deep-interview/SKILL.md) | `ask_user_question` |
| Ralplan（共识规划） | [`omd-ralplan`](skills/omd-ralplan/SKILL.md) | 并行 `subagent` 草案 + 仲裁收敛 |
| Research（有据调研） | [`omd-research`](skills/omd-research/SKILL.md) | `web_search`/`web_fetch` + 并行 `subagent` |
| Autoresearch（评估驱动改进） | [`omd-autoresearch`](skills/omd-autoresearch/SKILL.md) | `goal` + 评估子代理循环 |
| Ultragoal（持久多目标） | [`omd-ultragoal`](skills/omd-ultragoal/SKILL.md) | `goal` + `todo_write` + checkpoint 工件 |
| HUD（状态栏） | [`omd-hud`](skills/omd-hud/SKILL.md) | `dsh-ui` 内联仪表盘（genui） |

**提示词触发 + 工具 skill**（自然语言触发，无独立斜杠命令）：

| OMC 触发 | oh-my-dsh skill | DSH 原生载体 |
|----------|-----------------|--------------|
| tdd（测试驱动） | [`omd-tdd`](skills/omd-tdd/SKILL.md) | `pwsh`/`bash` 测试 + red-green-refactor |
| deepsearch（代码检索） | [`omd-deepsearch`](skills/omd-deepsearch/SKILL.md) | `grep`/`glob`/`read` 本地定位 |
| deep-analyze（深度分析） | [`omd-deep-analyze`](skills/omd-deep-analyze/SKILL.md) | 并行 `subagent` 多视角 |
| ultrathink（深度推理） | [`omd-ultrathink`](skills/omd-ultrathink/SKILL.md) | 纯推理（先不动工具） |
| ai-slop-cleaner（去废话） | [`omd-ai-slop-cleaner`](skills/omd-ai-slop-cleaner/SKILL.md) | `review`/`edit` 精简 |
| omc-doctor（自检） | [`omd-doctor`](skills/omd-doctor/SKILL.md) | 安装/挂载诊断 |
| debug（调试） | [`omd-debug`](skills/omd-debug/SKILL.md) | 复现→定位→最小修复→回归 |
| release（发布） | [`omd-release`](skills/omd-release/SKILL.md) | git + 测试 + changelog + tag |
| remember（跨会话记忆） | [`omd-remember`](skills/omd-remember/SKILL.md) | 工作区记忆文件 |
| cancel（取消模式） | [`omd-cancel`](skills/omd-cancel/SKILL.md) | goal pause + interrupt_agent + job_kill |
| minimal-code-discipline（最小改动） | [`omd-minimal-code-discipline`](skills/omd-minimal-code-discipline/SKILL.md) | YAGNI 阶梯 |
| external-context（外部上下文） | [`omd-external-context`](skills/omd-external-context/SKILL.md) | `web_fetch`/`read` |
| visual-verdict（视觉 QA） | [`omd-visual-verdict`](skills/omd-visual-verdict/SKILL.md) | `read_image` 对比 |
| skillify（提取 skill） | [`omd-skillify`](skills/omd-skillify/SKILL.md) | 写 `SKILL.md` |
| wiki（知识库） | [`omd-wiki`](skills/omd-wiki/SKILL.md) | 工作区 markdown |
| omc-help（使用指南） | [`omd-help`](skills/omd-help/SKILL.md) | 实时列 skill/命令索引 |

> **`ultrawork` 已退役**：OMC 在 5.0.0 删除了 `ultrawork`（以及 `ultraqa`/`swarm`/`pipeline` 等），oh-my-dsh 同步移除；其"最大并行扇出"能力已并入 `execute`/`team`/`ralph` 的内部并行纪律。

关键差异：OMC 的 HUD 是 CLI 状态栏，而 oh-my-dsh 的 HUD 是**内联在回答正文里的 `dsh-ui` 仪表盘**（stat/progress/timeline/table），因为 DSH 的 Web GUI 本身就在渲染结构化 UI。

## 目录结构

```
oh-my-dsh/
├── package.json              # dsh.bundle manifest（组合包安装入口）
├── cordis.patch.yml          # 组合包 patch 层（全局命令 + 全局 skill 挂载）
├── index.js                  # 组合包模块入口
├── agent.cordis.yml          # agent preset 组合文件（= standard + persona + skill + 命令）
├── preset.yml                # preset 显示元数据
├── install.ps1 / install.sh  # preset 手动安装脚本
├── LICENSE
├── commands/
│   └── omd-commands.mjs    # 斜杠命令生产者（ESM 插件）
├── skills/
│   ├── omd-plan/SKILL.md
│   ├── omd-execute/SKILL.md
│   ├── omd-review/SKILL.md
│   ├── omd-verify/SKILL.md
│   ├── omd-team/SKILL.md
│   ├── omd-autopilot/SKILL.md
│   ├── omd-ralph/SKILL.md
│   ├── omd-deep-interview/SKILL.md
│   ├── omd-ralplan/SKILL.md
│   ├── omd-research/SKILL.md
│   ├── omd-autoresearch/SKILL.md
│   ├── omd-ultragoal/SKILL.md
│   ├── omd-tdd/SKILL.md
│   ├── omd-deepsearch/SKILL.md
│   ├── omd-deep-analyze/SKILL.md
│   ├── omd-ultrathink/SKILL.md
│   ├── omd-ai-slop-cleaner/SKILL.md
│   ├── omd-doctor/SKILL.md
│   ├── omd-debug/SKILL.md
│   ├── omd-release/SKILL.md
│   ├── omd-remember/SKILL.md
│   ├── omd-cancel/SKILL.md
│   ├── omd-minimal-code-discipline/SKILL.md
│   ├── omd-external-context/SKILL.md
│   ├── omd-visual-verdict/SKILL.md
│   ├── omd-skillify/SKILL.md
│   ├── omd-wiki/SKILL.md
│   ├── omd-help/SKILL.md
│   └── omd-hud/SKILL.md
└── docs/
    ├── ARCHITECTURE.md
    └── RELEASE.md
```

## 安装 / 使用

两种安装方式，**任选其一即可**（bundle 装全局、preset 按会话选）。

**方式 A：组合包 bundle（主要，等价 OMC 的插件市场安装）** —— 全局装好 `/omd-*` 命令与 29 个 skill，profile 里所有会话可见：

```sh
# git 源码安装（纯 JS/Markdown，零构建，无需 allowBuilds 授权；用 @<tag> 可锁定版本）
dsh plugin --profile web add github:hawk2048/oh-my-dsh

# 或从 npm 安装（等价 OMC 的 npm i -g）
dsh plugin --profile web add @hawk2048/oh-my-dsh
```

装完重启 profile 即可。用户全程只敲一条命令，由 pnpm 拉取，**不手动下载压缩包**。

**方式 B：agent preset（可选，按会话选择）** —— 含 persona 与编排工具集的全量会话：

```sh
# Windows
.\install.ps1
# macOS / Linux
./install.sh
```

然后在 DSH 里**新建会话时选择 "oh-my-dsh 编排"** preset（或把它设为 `agent-presets.default`）。详见 [docs/RELEASE.md](docs/RELEASE.md)。

## 怎么用（会话内）

两种方式，效果一样：

**方式一：自然语言**（代理自动加载对应 skill）

- `先规划一下怎么实现 X` → `omd-plan`
- `按计划实现` → `omd-execute`
- `评审一下刚才的改动` → `omd-review`
- `验证一下，测试要全绿` → `omd-verify`
- `用 team 做一个任务管理应用` → `omd-team`
- `autopilot：搭一个 REST API` → `omd-autopilot`
- `ralph 重构认证，必须测试全绿` → `omd-ralph`
- `先深度访谈，我想做个 xx` → `omd-deep-interview`
- `ralplan：多角度论证一下这个架构选型` → `omd-ralplan`
- `调研一下 X 的最佳实践，要带来源` → `omd-research`
- `autoresearch：把这份报告打磨到达标` → `omd-autoresearch`
- `ultragoal：这个长期目标拆成子目标推进` → `omd-ultragoal`
- `tdd：先写失败测试再实现` → `omd-tdd`
- `deepsearch：定位谁调用了这个函数` → `omd-deepsearch`
- `deep-analyze：深度分析一下这块架构` → `omd-deep-analyze`
- `ultrathink：想清楚再动手` → `omd-ultrathink`
- `去 AI 废话，精简这段` → `omd-ai-slop-cleaner`
- `自检一下 oh-my-dsh 装好没` → `omd-doctor`
- `debug：排查这个报错` → `omd-debug`
- `发布 v1.2，写 changelog` → `omd-release`
- `记住这个决定，下个会话还要用` → `omd-remember`
- `停掉正在跑的 autopilot` → `omd-cancel`
- `最小改动，别过度设计` → `omd-minimal-code-discipline`
- `看下这个 issue/链接` → `omd-external-context`
- `对比这两张截图` → `omd-visual-verdict`
- `把这段流程沉淀成 skill` → `omd-skillify`
- `记到知识库/更新文档` → `omd-wiki`
- `omd 能做什么 / 有哪些命令` → `omd-help`

**方式二：斜杠命令**（在输入框敲 `/omd` 弹出候选）

| 命令 | 等价 skill |
|------|-----------|
| `/omd-plan <任务>` | `omd-plan` |
| `/omd-execute <任务>` | `omd-execute` |
| `/omd-review <任务>` | `omd-review` |
| `/omd-verify <任务>` | `omd-verify` |
| `/omd-team <任务>` | `omd-team` |
| `/omd-autopilot <目标>` | `omd-autopilot` |
| `/omd-ralph <目标>` | `omd-ralph` |
| `/omd-deep-interview <主题>` | `omd-deep-interview` |
| `/omd-ralplan <描述>` | `omd-ralplan` |
| `/omd-research <问题>` | `omd-research` |
| `/omd-autoresearch <任务>` | `omd-autoresearch` |
| `/omd-ultragoal <目标>` | `omd-ultragoal` |

代理会加载对应的 skill，按该模式编排，并用 HUD 实时汇报进度。

## 为什么是 skill + bundle/preset，而不是新工具

DSH 的原生多智能体原语（`workflow` 的流水线/并行、`subagent` 的扇出、`ralph` 的 fresh-agent 循环、`goal` 的跨轮目标）**已经覆盖了 OMC 的编排语义**。oh-my-dsh 因此不引入新的宿主工具或运行时，而是把「什么时候用哪个原语、怎么编排、怎么收尾」沉淀成可复用的 skill。

分发也复用 DSH 原生机制：`cordis.patch.yml` + `package.json` 的 `dsh.bundle` manifest 让 `dsh plugin add` 装成**组合包**（全局命令 + 全局 skill），`agent.cordis.yml` 让它作为**agent preset** 按会话挂载（persona + 命令 + skill）。斜杠命令的 `commands/omd-commands.mjs` 是一个 ESM 插件，注入 DSH 自带的 `commands` 服务注册命令——零运行时风险，升级 DSH 不受影响。

## 扩展

- **加模式**：在 `skills/` 下新增 `omd-xxx/SKILL.md`（YAML frontmatter 写 `name` + `description`）。
- **加命令**：在 `commands/omd-commands.mjs` 的 `MODES` 数组里追加一条。
- **改 persona**：编辑 `agent.cordis.yml` 顶部的 `persona` 行。
- **把 skill 做成全局**：走 bundle（`dsh plugin add`），见上文方式 A；或把 `skills/*` 复制到 `${DSH_HOME}/skills/`。

## 许可

MIT。灵感来自 [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)。
