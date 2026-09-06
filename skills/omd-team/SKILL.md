---
name: omd-team
description: "Team multi-agent orchestration: run a staged pipeline (team-plan → team-prd → team-exec → team-verify → team-fix loop) as a DSH workflow script with subagent fan-out. Use when the user asks for team orchestration, a multi-agent pipeline, or a feature spanning several subsystems (team/团队/多智能体流水线)."
---

# oh-my-dsh · Team 分阶段流水线

把一个大任务拆成五个阶段的流水线，每个阶段由专门的子代理负责，阶段之间像流水线一样传递产物。对应 OMC 的 Team 模式。

## 何时用

- 需求横跨多个子系统（后端 + 前端 + 测试 + 文档）。
- 用户说"团队""team""多智能体""流水线""pipeline"。
- 任务有清晰的阶段依赖：先规划，再出规格，再实现，再验证，再修复。

## 五阶段模型

```
team-plan → team-prd → team-exec → team-verify → team-fix (loop)
```

| 阶段 | 产出 | 责任人 |
|------|------|--------|
| plan | 任务分解：子系统、依赖、验收标准 | 规划代理 |
| prd | 精确规格：接口、schema、数据流、边界 | 规格代理 |
| exec | 各子系统的实现 | 多个执行代理（并行） |
| verify | 测试、评审、与验收标准逐条对照 | 验证代理 |
| fix | 修复验证发现的缺陷，循环直到全绿 | 修复代理 |

## 用 workflow 工具驱动

`workflow` 是团队流水线的首选载体：一个 JS 脚本编排多个子代理，支持 `pipeline`（无阶段屏障的流水线）和 `parallel`（屏障）。每个阶段用一个子代理，产物用结构化 JSON 在阶段间传递。

```js
// workflow 脚本骨架（meta 走参数，不是代码）
const plan = await agent(
  `你是规划代理。把任务拆成带依赖和验收标准的任务清单。任务：${args.task}`,
  { label: 'team-plan', phase: 'plan', schema: { type: 'object', properties: {
    tasks: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, title: { type: 'string' },
      dependsOn: { type: 'array', items: { type: 'string' } },
      acceptance: { type: 'string' } },
      required: ['id','title','acceptance'] } } } } }
);

const prd = await agent(
  `你是规格代理。基于这份任务清单产出精确实现规格（接口/schema/边界）。\n${JSON.stringify(plan)}`,
  { label: 'team-prd', phase: 'prd' }
);

// exec：按依赖并行执行，无屏障
const results = await pipeline(plan.tasks, async (prev, task) => {
  return await agent(
    `你是执行代理。按规格实现任务 #${task.id}「${task.title}」。\n规格：${prd}\n前序产物：${JSON.stringify(prev)}`,
    { label: `exec-${task.id}`, phase: 'exec' }
  );
});

// verify：对照验收标准逐条验证
const verdict = await agent(
  `你是验证代理。对照验收标准验证实现，返回每个任务的通过/缺陷清单。\n实现：${JSON.stringify(results)}\n验收标准：${JSON.stringify(plan.tasks)}`,
  { label: 'team-verify', phase: 'verify' }
);

// fix loop：只要还有缺陷就继续修，上限 3 轮
let fixing = verdict;
for (let round = 0; round < 3 && fixing.openIssues.length; round++) {
  fixing = await agent(
    `你是修复代理。修复这些缺陷并重新验证。\n${JSON.stringify(fixing.openIssues)}`,
    { label: `team-fix-${round}`, phase: 'fix' }
  );
}

return { plan, prd, results, final: fixing };
```

要点：

- `meta` 的 `phases` 声明 `[{title:'plan'},{title:'prd'},{title:'exec'},{title:'verify'},{title:'fix'}]`，进度条按阶段推进。
- `agent()` 的 `schema` 用「对象根 + type/properties/required/items」约束子代理返回结构化 JSON；不写 `schema` 则拿到纯文本。
- `pipeline(items, ...stages)` 让每个任务独立流过各阶段、阶段间无屏障；`parallel(thunks)` 用于必须集齐全部结果才能继续的屏障。
- 脚本里没有文件系统/网络/计时器，只有 `agent`/`pipeline`/`parallel`/`phase`/`log`/`args` —— 所有实际工作由子代理完成，脚本只负责编排。

## 不用 workflow 时（轻量版）

任务不大、阶段不复杂时，直接在主会话里手动走五阶段：用 `subagent` 依次委托 plan → prd → exec（多个 `subagent` 在同一轮并行启动）→ verify → fix，产物在主会话里自己串联。

## 收尾：HUD

每个阶段结束后，按 `omd-hud` 输出一段内联 `dsh-ui` 仪表盘：阶段状态表 + 进度条 + 下一个动作。别等全跑完才汇报。

## 反模式

- 别把 plan 和 prd 合并成一个代理：plan 管"拆什么"，prd 管"怎么做对"。
- exec 之间如果有依赖，用 `pipeline` 传前序产物，而不是让它们各自重读仓库。
- fix loop 必须有上限和"全绿"判据，否则无限循环。
