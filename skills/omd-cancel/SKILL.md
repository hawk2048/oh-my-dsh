---
name: omd-cancel
description: "取消：干净地停止进行中的编排模式——暂停目标轮次、中断后台子代理、终止任务——并留下干净的检查点。触发词：cancel / 停止 / 停下 / 取消 / 别跑了 / stop / abort。"
---

# oh-my-dsh · Cancel 取消进行中模式

干净地停掉正在跑的编排，留下可恢复的检查点。对应 OMC 的 `cancel` skill（触发词 stop/cancel/abort）。

## 何时用

- 用户说「停」「取消」「别跑了」。
- 一个 autopilot/ralph/team/ultragoal 跑偏了，需要中断。

## 取消纪律

1. **盘点**：先搞清楚现在有什么在跑——`goal`（`get_goal` 查当前目标）、后台 `subagent`（`list_agents`）、后台 `job`（`job_list`）。
2. **停目标**：`update_goal` 用 `pause`（或 `blocked`）停掉跨轮目标，别让它继续自动续轮。
3. **停子代理/任务**：对还在跑的子代理 `interrupt_agent`，对后台命令 `job_kill`。
4. **留检查点**：用 `remember` 或写文件记下「进行到哪、下一步从哪续」，别让进度白费。
5. **报告**：说清停了什么、还留着什么、怎么恢复。

## 与其它模式的关系

- 取消不是删除：用 `cordis_stop`/`update_goal pause` 保留定义与进度，别 `undefine`/`complete` 式永久清掉（除非用户明确要删）。
- 取消后要重来，从检查点接续；方向都变了就先 `omd-plan` 重新规划。

## 收尾：HUD

用 `omd-hud` 输出取消结果：`table`（对象/动作/结果）+ `callout`（恢复方式）。让「停了什么、怎么续」一眼可见。

## 反模式

- 别只说「已停止」却不真正调停对应机制——goal 会继续续轮、子代理会继续跑。
- 别把取消做成不可逆删除。
- 别不留检查点就停，否则前功尽弃。
