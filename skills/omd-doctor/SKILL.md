---
name: omd-doctor
description: "自检诊断：检查 oh-my-dsh 装得对不对——核对技能目录、/omd-* 斜杠命令与 preset/bundle 挂载——并诊断某个模式为什么没生效。触发词：doctor / 自检 / 诊断 / 为什么没生效 / 检查一下安装 / omd 有问题。"
---

# oh-my-dsh · Doctor 自检诊断

检查 oh-my-dsh 装得对不对、为什么某个模式没生效，并尽量当场修。对应 OMC 的 `omc-doctor`。

## 何时用

- `/omd-*` 命令不出现、敲了没反应。
- 某个模式（plan/team/autopilot/…）没按预期触发。
- 用户问「oh-my-dsh 装好了吗 / 为什么没生效」。

## 诊断清单

按顺序查，每项给「OK / 异常 + 证据」：

1. **skill 目录**：确认 `skills/` 下有一整套 `omd-*` 目录（29+ 个：编排 + 触发 + 工具 + HUD）。可用 `glob` 列 `skills/*/SKILL.md`。
2. **斜杠命令**：确认命令面有 12 条 `/omd-*`（bundle 装进 `commands` 注册表，preset 经 `commands/omd-commands.mjs`）。让用户在输入框敲 `/omd` 看候选是否弹出。
3. **挂载/组合**：preset 形态看 `~/.dsh/.agent-presets/oh-my-dsh/` 是否有 `agent.cordis.yml` + `skills/` + `commands/`；bundle 形态看 `dsh --profile <name> --dump-config` 是否有 `command-omd` 与 `skill-filesystem(customSkillDirs)` 行。
4. **生效范围**：bundle = 全局；preset = 仅所选会话。若只装了 preset，换别的 preset 会话自然看不到 `/omd-*`。

## 修复建议

- skill 缺失 → 重跑安装（bundle：`dsh plugin add …`；preset：`install.ps1`/`install.sh`）。
- 命令不出现 → 新开会话或重启 profile，让组合层重新加载。
- 组合行缺 → 查 `cordis.patch.yml` / `agent.cordis.yml` 是否有对应行，bump 版本重装。

## 收尾：HUD

用 `omd-hud` 输出诊断结果：检查项状态表（OK/异常/证据/建议）。让「哪一环断了、怎么修」一眼可见。

## 反模式

- 别只看结论——每项诊断都要给证据（文件/行/命令输出）。
- 别在没确认安装形态（bundle 还是 preset）前乱猜。
- 修完要让用户重开会话/重启 profile 再验证，别宣称「已好」却未复测。
