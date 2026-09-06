---
name: omd-debug
description: "Debug: reproduce the failure, isolate the cause with evidence, fix minimally, and lock it with a regression test. Use when the user says debug / 调试 / 报错 / 崩溃 / 为什么失败 / 修 bug / 排查."
---

# oh-my-dsh · Debug 结构化调试

按「复现 → 定位 → 最小修复 → 回归验证」排查故障，每一步都留证据。对应 OMC 的 `debug` 工具 skill。

## 何时用

- 有报错/崩溃/异常行为，需要找出根因并修掉。
- 用户说「修一下」「为什么失败」「排查这个 bug」。

## 调试纪律

1. **复现**：先用 `pwsh`/`bash` 拿到**确切的**报错信息（命令 + 完整 stderr + 退出码），别凭记忆。
2. **定位**：二分缩小范围——`read` 读相关代码、`grep` 追调用链、加日志/断点式打印，把根因锁定到具体 file:line。
3. **最小修复**：只改必要的，别顺手重构（配合 `omd-minimal-code-discipline`）。
4. **回归验证**：补/跑一条测试证明修好了，再确认没引入新问题。

## 与其它模式的关系

- 定位「在哪里」用 `omd-deepsearch`；理解「为什么这么设计」用 `omd-deep-analyze`；`debug` 专注「为什么坏了 + 修好」。
- 修完交给 `omd-review` 复核；需要反复验证的交给 `omd-verify`。

## 收尾：HUD

用 `omd-hud` 输出排查轨迹：`timeline`（复现→定位→修复→验证）+ `table`（根因/文件:行/修复/回归测试）。让「坏了什么、改了什么、怎么证明好了」一眼可见。

## 反模式

- 别没复现就改——那是猜，不是 debug。
- 别只看第一处报错就下结论，追到根因。
- 别修完不验证就宣称「已修好」。
