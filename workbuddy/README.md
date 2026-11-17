# oh-my-workbuddy · WorkBuddy 适配层

把 oh-my-dsh 的 30+ 个 `omd-*` 编排 skill 迁移到 [WorkBuddy](https://www.workbuddy.cn/) 用户级技能目录。
同一套 OMC 编排模式，映射到底层宿主工具——DSH 版用 `workflow`/`subagent`/`goal`，WorkBuddy 版用 `Agent`/`TaskCreate`/`automation`。

> 本目录是 `oh-my-dsh` 仓库的**适配分支**，不是独立项目。核心方法论与 `../skills/` 同源，
> 只改工具名与宿主专属段落。omd 核心 skill 更新时，适配层应同步跟进。

## 为什么放在同一仓库

- **版本同步**：omd 的模式定义（plan/execute/review/verify/team/autopilot/ralph…）改了，两个宿主一起改，一个 commit。
- **同源保证**：映射表与核心 skill 一一对应，不会出现"DSH 版有、WorkBuddy 版漏了"的分叉。
- WorkBuddy 没有 DSH 的 `dsh plugin add github:` 一键安装机制，所以本目录的价值是**版本控制 + 备份 + 分发源**，不是即装即用。

## 安装

WorkBuddy 会把 `~/.workbuddy/skills/` 下的每个子目录识别为技能。把本目录的 `skills/` 内容复制过去即可：

```bash
# Windows（Git Bash）
cp -r workbuddy/skills/omd-* "$HOME/.workbuddy/skills/"

# 或用 install 脚本（自动定位目标目录）
bash workbuddy/install.sh
```

复制后重启 WorkBuddy 会话，说触发词即可自动加载（如「先规划一下」「autopilot 搭个 API」「把这段整理成金字塔结构」）。

**无需重启验证**：实测复制后 `skill_management list` 立即识别到全部 skill。

## 工具映射（omd → WorkBuddy）

| DSH 原语 | WorkBuddy | 状态 |
|---|---|---|
| `subagent` / `subagent_fork` | `Agent` 工具 | ✅ |
| `workflow` 流水线 | `TaskCreate` + `Agent` 并行 | ✅ |
| `todo_write` | `TaskCreate/TaskUpdate` | ✅ |
| `read`/`grep`/`glob` | `Read/Grep/Glob` | ✅ |
| `web_search`/`web_fetch` | `WebSearch/WebFetch` | ✅ |
| `ask_user_question` | `AskUserQuestion` | ✅ |
| `ralph` / `goal` | `Agent(resume=<Task ID>)` + 工作区文件 + `TaskCreate` | ✅ 已实测 |
| 跨会话目标持久 | `automation_update` 定时任务（比 DSH goal 更强，可跨天） | ✅ |
| `dsh-ui` HUD | `show_widget` 可视化 | ✅ |
| `/omd-*` 斜杠命令 | 无对应，改用 description 触发词 | ❌ 无法 1:1 |

## 实测记录（2026-11-17）

- **Agent resume 续跑**：启动后台 agent 写 `ROUND=1` → 完成后 `Agent(resume=<返回的 Task ID>)` 续跑写 `ROUND=2` → 文件内容确实从 1 变 2。证明 autopilot/ralph 的跨轮机制可用。
- **技能识别**：31 个 `omd-*` skill + 1 个 suite 入口复制到 `~/.workbuddy/skills/` 后，`skill_management list` 全部识别、无需重启。

## 已知缺口

1. **无同会话自动无限续轮**：WorkBuddy 每轮需主控主动调 `Agent(resume)` 或定时任务触发；DSH goal 是后台自己跑到底。
2. **无自定义斜杠命令**：靠 description 触发词，不能敲 `/omd-plan`。
3. **fresh-agent 语义差异**：resume 是同一 agent 续跑；要完全 fresh 就不传 resume、从工作区文件读上下文启动新 agent。

## 目录结构

```
workbuddy/
├── README.md          # 本文件
├── install.sh         # 安装脚本
├── SKILL.md           # suite 入口（含 31 个子 skill 索引 + 映射表）
└── skills/
    ├── omd-plan/SKILL.md
    ├── omd-execute/SKILL.md
    └── ...（共 31 个）
```

## 许可

MIT，与原仓库一致。
