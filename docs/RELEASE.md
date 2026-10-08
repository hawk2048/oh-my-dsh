# 发布 oh-my-dsh

oh-my-dsh 用两种形态分发：**组合包（bundle）** 是主要安装路径（`dsh plugin add`），
**agent preset** 是可选的全量会话（按会话选择）。二者都来自本仓库，一起打 tag、一起发布。

## 对齐 OMC：git tag 即发布，用户不手动下载压缩包

OMC 的安装只有两条路，**都不涉及「下载压缩包」**：

| OMC | oh-my-dsh 等价 |
|-----|---------------|
| Claude Code 插件市场 `/plugin marketplace add <git-url>` + `/plugin install`（git clone） | `dsh plugin add github:hawk2048/oh-my-dsh`（git 拉取） |
| `npm i -g oh-my-claude-sisyphus`（npm） | `dsh plugin add @hawk2048/oh-my-dsh` |

所以 oh-my-dsh 也一样：**git tag 就是 release**，用户敲一条命令，由 pnpm 拉取，全程不碰压缩包。

## 前置

- 已发布到 GitHub（公开仓库，加 `dsh-plugin` topic）。
- 本地有 `dsh` CLI 与 `pnpm`（`dsh plugin` 底层转发给 pnpm）。
- 改动了 `skills/`、`commands/` 或 `cordis.patch.yml` 后，记得 bump `package.json` 的 `version`。

## 本地验证（每次发布前）

```sh
# 0. 安装脚本的回归测试（非破坏性安装契约：不删 preset 目录、保留本地文件、覆盖前备份、
#    重跑原地刷新而不是把 skills/ 嵌套成 skills/skills）；有 PowerShell 时一并跑 Windows 侧守卫
pnpm test

# 1. 语法自检命令模块
node --check commands/omd-commands.mjs

# 2. 打一个本地 tarball，装进临时 profile，验证层与加载（tarball 只用于本地自测，不是用户安装方式）
pnpm pack
dsh plugin --profile omdtest add ./oh-my-dsh-<version>.tgz
dsh --profile omdtest --dump-config   # 应看到 command-omd 与 skill-filesystem(customSkillDirs)
dsh --profile omdtest                 # 应能启动、无 duplicate / provider 冲突
dsh plugin --profile omdtest remove @hawk2048/oh-my-dsh
```

## 发布步骤

1. 提交并打 tag（**这就是 release**，`dsh plugin add` 可用 `github:...@<tag>` 锁定版本）：
   ```sh
   git tag v0.1.0
   git push origin v0.1.0
   ```
2. 发布到 npm：`pnpm publish --access public` —— 等价 OMC 的 `npm i -g oh-my-claude-sisyphus`，装的是 `dsh plugin add @hawk2048/oh-my-dsh`。
   **注意 registry**：若本机 `npm config get registry` 指向 `https://registry.npmmirror.com`（国内只读镜像），
   直接 `publish` 会打到镜像上并失败。发布必须显式指定官方源，且先登录：
   ```sh
   npm whoami --registry https://registry.npmjs.org   # 需先 npm login --registry https://registry.npmjs.org
   npm publish --access public --registry https://registry.npmjs.org
   ```
3. （可选）在 GitHub Release 挂 `pnpm pack` 出的 `.tgz`，仅供离线/内网分发；不是必需，也不是默认安装方式。

## 安装方式（写进 README 与 release 说明）

**组合包（主要，等价 OMC 的 `/plugin install`）：**

```sh
# git 源码安装（等价 OMC 插件市场；纯 JS/Markdown，无需构建授权）
dsh plugin --profile web add github:hawk2048/oh-my-dsh

# npm 安装（等价 OMC 的 npm i -g）
dsh plugin --profile web add @hawk2048/oh-my-dsh
```

装完后重启 profile，13 条 `/omd-*` 命令与 30 个 skill 即全局可用。

**agent preset（可选，按会话选择，含 persona 与编排工具集）：**

```sh
# Windows
.\install.ps1
# macOS / Linux
./install.sh
```

安装器是**非破坏性**的：它从不删除 preset 目录。你自己加的东西（例如本地写的 skill）升级后仍在；
若某个随仓库发布的文件会覆盖你本地改过的同名文件（例如 `agent.cordis.yml` 里加了本地配置），
会先备份成 `<name>.bak-<时间戳>` 再覆盖。重复运行安全可逆。脚本结束时会列出「保留了哪些不随仓库发布的文件」。

或直接解压到 `$DSH_HOME/.agent-presets/oh-my-dsh/`。新建会话后在 preset 选择器里选「oh-my-dsh 编排」。

## 登记到社区

- 给仓库加 GitHub topic：`dsh-plugin`。
- 提 PR 收录进 [awesome-dsh-plugin](https://awesome-dsh-plugin.com)。

## 注意事项

- git 安装拉取源码，本仓库是纯 JS + YAML + Markdown、零构建，故不需要 `prepare` 脚本，用户也无需 `allowBuilds` 授权。
- 发布 npm 时，在 CI 里 `pnpm pack` 出产物再 `pnpm publish --access public`（或用 `dsh plugin add @hawk2048/oh-my-dsh` 直接装 npm 包）。
