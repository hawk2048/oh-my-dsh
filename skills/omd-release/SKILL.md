---
name: omd-release
description: "Release: walk the repo's release process — version bump, changelog, tests, tag, build — and produce a release checklist. Use when the user says release / 发布 / 发版 / 打 tag / 打版本 / changelog."
---

# oh-my-dsh · Release 发布

按仓库既有惯例走一遍发版流程，产出**可核对清单**。对应 OMC 的 `release` 工具 skill。

## 何时用

- 用户要发版本、打 tag、出 changelog、准备发布产物。
- 需要把「改完了」推进到「可交付」。

## 发布纪律

1. **摸清惯例**：先 `read`/`grep` 看仓库有没有 CI、`CHANGELOG`、版本规则（semver?）、发布脚本。有 `.omc/RELEASE_RULE.md` 或 `docs/RELEASE.md` 先读它。
2. **前置检查**：测试全绿、无未提交变更、依赖/构建通过（`pwsh`/`bash` 跑真实命令）。
3. **版本号**：按语义化版本 bump（major/minor/patch），改到该改的地方（package.json 等）。
4. **changelog**：按「新增/变更/修复/移除」归类写清改动。
5. **tag 与产物**：打 tag，出构建产物（如 `pnpm pack` 出 `.tgz`）。

## 与其它模式的关系

- 发布前用 `omd-review` 复核改动，用 `omd-verify` 确认达标。
- oh-my-dsh 自身的发布流程见 `docs/RELEASE.md`——本 skill 是通用发布纪律，二者不冲突。

## 收尾：HUD

用 `omd-hud` 输出发布清单：`table`（检查项/状态/结果）+ `steps`（版本→changelog→tag→产物）。让「哪步做了、哪步待办、产物在哪」一眼可见。

## 反模式

- 别跳过前置测试就发版。
- 别在没看仓库惯例的情况下凭空定版本/格式。
- 别把「打了 tag」当成「发完了」——产物和说明都要落到位。
