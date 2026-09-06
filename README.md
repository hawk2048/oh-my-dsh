# oh-my-dsh

[![npm version](https://img.shields.io/npm/v/@hawk2048/oh-my-dsh?color=cb3837)](https://www.npmjs.com/package/@hawk2048/oh-my-dsh)
[![GitHub stars](https://img.shields.io/github/stars/hawk2048/oh-my-dsh?style=flat&color=yellow)](https://github.com/hawk2048/oh-my-dsh/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![dsh-plugin](https://img.shields.io/badge/dsh-plugin-orange)](https://github.com/topics/dsh-plugin)

**A multi-agent orchestration layer for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH)** — ports [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)'s orchestration modes onto DSH's native primitives (`workflow` / `subagent` / `ralph` / `goal`).

> Two ways to trigger: **natural language** (29 skills, auto-loaded by the agent) + **slash commands** (12 `/omd-*` commands). Start a session, orchestration is ready.

[中文](README.zh.md)

## Quick Start

One command installs all 29 skills + 12 `/omd-*` commands (the OMC plugin-marketplace equivalent):

```sh
dsh plugin --profile web add github:hawk2048/oh-my-dsh
```

Or from npm (the `npm i -g` equivalent):

```sh
dsh plugin --profile web add @hawk2048/oh-my-dsh
```

Restart the profile, type `/omd` to see command candidates, or use natural language ("plan this", "autopilot, build a REST API").

## Requirements

- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh` CLI)
- [pnpm](https://pnpm.io) — `dsh plugin` forwards to pnpm

## Why oh-my-dsh

- **Zero configuration** — one `dsh plugin add` installs everything; the bundle self-registers, no setup wizard.
- **Team-first orchestration** — Team is the canonical staged pipeline (`team-plan → team-prd → team-exec → team-verify → team-fix`), built on DSH's native `workflow`.
- **Natural language interface** — describe what you want; the 29 `omd-*` skills auto-load, nothing to memorize.
- **Automatic parallelization** — complex tasks fan out across parallel `subagent`s.
- **Persistent execution** — Ralph / Autopilot / Ultragoal keep going until verified complete (native `ralph` loops + `goal` cross-turn objectives).
- **Zero runtime overhead** — adds no new host tools or runtime, just skills over DSH's native primitives, so you keep DSH's own model routing and sandbox.
- **Learn from experience** — `omd-skillify` extracts reusable skills; `omd-remember` persists durable notes across sessions.
- **Real-time visibility** — the inline HUD renders live `dsh-ui` progress dashboards.

## OMC correspondence

Aligned to OMC **v5.3.0** (the `plan → execute → review → verify` pipeline + retained modes):

| OMC workflow | oh-my-dsh skill | DSH primitive |
|-----------|-----------------|--------------|
| Plan | [`omd-plan`](skills/omd-plan/SKILL.md) | read-only exploration + parallel `subagent` |
| Execute | [`omd-execute`](skills/omd-execute/SKILL.md) | parallel `subagent` + `todo_write` |
| Review | [`omd-review`](skills/omd-review/SKILL.md) | `subagent_fork` independent review |
| Verify | [`omd-verify`](skills/omd-verify/SKILL.md) | `pwsh`/`bash` tests + `subagent` re-check |
| Team | [`omd-team`](skills/omd-team/SKILL.md) | `workflow` + `subagent` |
| Autopilot | [`omd-autopilot`](skills/omd-autopilot/SKILL.md) | `goal` + `todo` + `subagent` |
| Ralph | [`omd-ralph`](skills/omd-ralph/SKILL.md) | `ralph` + `goal` verify loop |
| Deep Interview | [`omd-deep-interview`](skills/omd-deep-interview/SKILL.md) | `ask_user_question` |
| Ralplan | [`omd-ralplan`](skills/omd-ralplan/SKILL.md) | parallel `subagent` drafts + arbitration |
| Research | [`omd-research`](skills/omd-research/SKILL.md) | `web_search`/`web_fetch` + parallel `subagent` |
| Autoresearch | [`omd-autoresearch`](skills/omd-autoresearch/SKILL.md) | `goal` + evaluator loop |
| Ultragoal | [`omd-ultragoal`](skills/omd-ultragoal/SKILL.md) | `goal` + `todo_write` + checkpoint artifacts |
| HUD | [`omd-hud`](skills/omd-hud/SKILL.md) | inline `dsh-ui` dashboard (genui) |

**Prompt-trigger + utility skills** (natural-language only, no slash command):

| OMC trigger | oh-my-dsh skill | DSH primitive |
|----------|-----------------|--------------|
| tdd | [`omd-tdd`](skills/omd-tdd/SKILL.md) | `pwsh`/`bash` tests + red-green-refactor |
| deepsearch | [`omd-deepsearch`](skills/omd-deepsearch/SKILL.md) | `grep`/`glob`/`read` local lookup |
| deep-analyze | [`omd-deep-analyze`](skills/omd-deep-analyze/SKILL.md) | parallel `subagent` multi-angle |
| ultrathink | [`omd-ultrathink`](skills/omd-ultrathink/SKILL.md) | pure reasoning (no tools first) |
| ai-slop-cleaner | [`omd-ai-slop-cleaner`](skills/omd-ai-slop-cleaner/SKILL.md) | `review`/`edit` tightening |
| omc-doctor | [`omd-doctor`](skills/omd-doctor/SKILL.md) | install/mount diagnostics |
| debug | [`omd-debug`](skills/omd-debug/SKILL.md) | reproduce→isolate→fix→regress |
| release | [`omd-release`](skills/omd-release/SKILL.md) | git + tests + changelog + tag |
| remember | [`omd-remember`](skills/omd-remember/SKILL.md) | workspace memory file |
| cancel | [`omd-cancel`](skills/omd-cancel/SKILL.md) | goal pause + `interrupt_agent` + `job_kill` |
| minimal-code-discipline | [`omd-minimal-code-discipline`](skills/omd-minimal-code-discipline/SKILL.md) | YAGNI ladder |
| external-context | [`omd-external-context`](skills/omd-external-context/SKILL.md) | `web_fetch`/`read` |
| visual-verdict | [`omd-visual-verdict`](skills/omd-visual-verdict/SKILL.md) | `read_image` comparison |
| skillify | [`omd-skillify`](skills/omd-skillify/SKILL.md) | write `SKILL.md` |
| wiki | [`omd-wiki`](skills/omd-wiki/SKILL.md) | workspace markdown |
| omc-help | [`omd-help`](skills/omd-help/SKILL.md) | live skill/command index |

> **`ultrawork` is retired** — OMC removed it in 5.0.0 (along with `ultraqa`/`swarm`/`pipeline`); oh-my-dsh removed it too, folding its "maximum parallel fan-out" into `execute`/`team`/`ralph`.

Key difference: OMC's HUD is a CLI status line, while oh-my-dsh's HUD is an **inline `dsh-ui` dashboard in the reply** (stat/progress/timeline/table), because DSH's Web GUI already renders structured UI.

## Directory structure

```
oh-my-dsh/
├── package.json              # dsh.bundle manifest (bundle install entry)
├── cordis.patch.yml          # bundle patch layer (global commands + skills)
├── index.js                  # bundle module entry
├── agent.cordis.yml          # agent preset composition (= standard + persona + skills + commands)
├── preset.yml                # preset display metadata
├── install.ps1 / install.sh  # preset manual install scripts
├── LICENSE
├── commands/
│   └── omd-commands.mjs      # slash-command producer (ESM plugin)
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

## Install / usage

Two forms — pick one (bundle for global, preset for per-session).

**Form A: bundle (primary, the OMC plugin-marketplace equivalent)** — installs the `/omd-*` commands and 29 skills globally, visible to every session in the profile:

```sh
# git source (pure JS/Markdown, zero build, no allowBuilds needed; pin with @<tag>)
dsh plugin --profile web add github:hawk2048/oh-my-dsh

# or npm (the npm i -g equivalent)
dsh plugin --profile web add @hawk2048/oh-my-dsh
```

Restart the profile. One command, pulled by pnpm — no manual tarball download.

**Form B: agent preset (optional, per-session)** — full session with persona and the orchestration toolkit:

```sh
# Windows
.\install.ps1
# macOS / Linux
./install.sh
```

Then create a session and pick the "oh-my-dsh 编排" preset (or set it as `agent-presets.default`). See [docs/RELEASE.md](docs/RELEASE.md).

## Usage (in-session)

Two equivalent ways:

**Way 1: natural language** (the agent auto-loads the matching skill)

- `plan how to implement X` → `omd-plan`
- `execute the plan` → `omd-execute`
- `review my changes` → `omd-review`
- `verify — tests must pass` → `omd-verify`
- `team, build a task-management app` → `omd-team`
- `autopilot: build a REST API` → `omd-autopilot`
- `ralph the auth refactor until green` → `omd-ralph`
- `deep interview me — I want to build X` → `omd-deep-interview`
- `ralplan this architecture decision` → `omd-ralplan`
- `research X best practices, with sources` → `omd-research`
- `autoresearch this report to passing` → `omd-autoresearch`
- `ultragoal: break this long goal into subgoals` → `omd-ultragoal`
- `tdd: failing test first` → `omd-tdd`
- `deepsearch: who calls this function` → `omd-deepsearch`
- `deep-analyze this architecture` → `omd-deep-analyze`
- `ultrathink before acting` → `omd-ultrathink`
- `strip the AI slop` → `omd-ai-slop-cleaner`
- `self-check the install` → `omd-doctor`
- `debug this error` → `omd-debug`
- `release v1.2 with changelog` → `omd-release`
- `remember this decision` → `omd-remember`
- `stop the running autopilot` → `omd-cancel`
- `minimal change, no over-engineering` → `omd-minimal-code-discipline`
- `read this issue/link` → `omd-external-context`
- `compare these screenshots` → `omd-visual-verdict`
- `turn this flow into a skill` → `omd-skillify`
- `write this to the wiki` → `omd-wiki`
- `what can omd do` → `omd-help`

**Way 2: slash commands** (type `/omd` for candidates)

| Command | Equivalent skill |
|------|-----------|
| `/omd-plan <task>` | `omd-plan` |
| `/omd-execute <task>` | `omd-execute` |
| `/omd-review <task>` | `omd-review` |
| `/omd-verify <task>` | `omd-verify` |
| `/omd-team <task>` | `omd-team` |
| `/omd-autopilot <goal>` | `omd-autopilot` |
| `/omd-ralph <goal>` | `omd-ralph` |
| `/omd-deep-interview <topic>` | `omd-deep-interview` |
| `/omd-ralplan <desc>` | `omd-ralplan` |
| `/omd-research <question>` | `omd-research` |
| `/omd-autoresearch <task>` | `omd-autoresearch` |
| `/omd-ultragoal <goal>` | `omd-ultragoal` |

The agent loads the matching skill, runs that mode, and reports progress via the HUD.

## Why skills + bundle/preset, not new tools

DSH's native multi-agent primitives (`workflow` pipelines/parallel, `subagent` fan-out, `ralph` fresh-agent loops, `goal` cross-turn objectives) **already cover OMC's orchestration semantics**. oh-my-dsh therefore adds no new host tools or runtime — it distills "which primitive to use, when, how to orchestrate, and how to close out" into reusable skills.

Distribution reuses DSH's native mechanisms: `cordis.patch.yml` + the `dsh.bundle` manifest make `dsh plugin add` install a **bundle** (global commands + skills), and `agent.cordis.yml` makes it an **agent preset** (per-session persona + commands + skills). The slash-command `commands/omd-commands.mjs` is an ESM plugin that injects DSH's built-in `commands` registry — zero runtime risk, survives DSH upgrades.

## Extending

- **Add a mode**: add `skills/omd-xxx/SKILL.md` (YAML frontmatter with `name` + `description`).
- **Add a command**: append an entry to the `MODES` array in `commands/omd-commands.mjs`.
- **Change the persona**: edit the `persona` row at the top of `agent.cordis.yml`.
- **Make a skill global**: use the bundle (`dsh plugin add`) or copy `skills/*` to `${DSH_HOME}/skills/`.

## License

MIT. Inspired by [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode).
