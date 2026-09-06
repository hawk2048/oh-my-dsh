// oh-my-dsh 斜杠命令生产者。
// 注册 plan/execute/review/verify/team/autopilot/ralph/deep-interview/ralplan/research/autoresearch/ultragoal 十二条人类命令。
// 每条 handler 把任务作为一条用户消息提交给模型（唤醒模型并让它加载对应
// omd-* skill），然后返回一条直接 UI 确认（不进入模型请求）。
//
// 说明：本文件作为 preset 内置插件被 Loader 以 ESM 方式加载；为避免依赖
// harness 内部包（本地 preset 目录无法走 node_modules 向上解析），这里手工
// 构造 UserMessage，而不是 import createUserMessage。

export const name = 'omd-commands'
export const inject = ['commands']

let seq = 0
function messageId() {
  seq += 1
  return 'omd-' + Date.now().toString(36) + '-' + seq.toString(36) + '-' + Math.random().toString(36).slice(2, 10)
}

function userMessage(text) {
  return {
    role: 'user',
    source: { kind: 'user' },
    content: [{ type: 'text', text }],
    id: messageId(),
  }
}

const MODES = [
  {
    name: 'omd-plan',
    description: '规划：先探索，产出带依赖与验收标准的实现计划（不写代码）',
    hint: '<任务>',
    label: '规划',
    skill: 'omd-plan',
    build: (t) => `请加载 omd-plan skill，对以下任务先探索再产出带依赖与验收标准的实现计划（不写代码），并用 HUD 输出计划概览：${t}`,
  },
  {
    name: 'omd-execute',
    description: '执行：按计划实现，多文件改动委托并行子代理，琐碎改动直接做',
    hint: '<任务>',
    label: '执行',
    skill: 'omd-execute',
    build: (t) => `请加载 omd-execute skill，按已确认的计划实现以下任务（多文件改动委托并行 subagent，琐碎改动直接做），并用 HUD 输出进度：${t}`,
  },
  {
    name: 'omd-review',
    description: '评审：独立评审改动，产出缺陷清单（不自我背书）',
    hint: '<任务>',
    label: '评审',
    skill: 'omd-review',
    build: (t) => `请加载 omd-review skill，对以下改动作独立评审（用评审 subagent 产出 issues 清单，不自我背书），并用 HUD 输出评审结果：${t}`,
  },
  {
    name: 'omd-verify',
    description: '验证：跑测试/构建，对照验收标准收集证据，失败则迭代',
    hint: '<任务>',
    label: '验证',
    skill: 'omd-verify',
    build: (t) => `请加载 omd-verify skill，对以下任务跑测试/构建并对照验收标准收集证据（失败则回 execute/review 迭代），并用 HUD 输出验证结果：${t}`,
  },
  {
    name: 'omd-team',
    description: '团队分阶段流水线（规划→规格→实现→验证→修复）',
    hint: '<任务>',
    label: '团队流水线',
    skill: 'omd-team',
    build: (t) => `请加载 omd-team skill，用 Team 分阶段流水线编排完成以下任务，各阶段用 HUD 输出进度：${t}`,
  },
  {
    name: 'omd-autopilot',
    description: '自动驾驶：单个主控代理把目标持续做到已验证完成',
    hint: '<目标>',
    label: '自动驾驶',
    skill: 'omd-autopilot',
    build: (t) => `请加载 omd-autopilot skill，用 Autopilot 模式把以下目标持续做到已验证完成，并用 HUD 输出进度：${t}`,
  },
  {
    name: 'omd-ralph',
    description: '拉夫持久验证循环：完整完成并验证到全绿，不留静默半成品',
    hint: '<目标>',
    label: '拉夫循环',
    skill: 'omd-ralph',
    build: (t) => `请加载 omd-ralph skill，用 Ralph 持久验证循环完成以下目标直到全绿，并用 HUD 输出进度：${t}`,
  },
  {
    name: 'omd-deep-interview',
    description: '深度访谈：写代码前用苏格拉底式追问澄清需求',
    hint: '<主题>',
    label: '深度访谈',
    skill: 'omd-deep-interview',
    build: (t) => `请加载 omd-deep-interview skill，对以下想法做深度访谈澄清需求，先收敛出规格再动手：${t}`,
  },
  {
    name: 'omd-ralplan',
    description: '共识规划：多视角并行规划 + 结构化审议，收敛出共识计划',
    hint: '<描述>',
    label: '共识规划',
    skill: 'omd-ralplan',
    build: (t) => `请加载 omd-ralplan skill，对以下描述做多视角并行规划 + 结构化审议，收敛出共识计划，并用 HUD 输出草案/分歧/裁决概览：${t}`,
  },
  {
    name: 'omd-research',
    description: '调研：查证一个开放问题，返回有来源依据的结论',
    hint: '<问题>',
    label: '调研',
    skill: 'omd-research',
    build: (t) => `请加载 omd-research skill，对以下问题做有据调研（并行研究子代理 + 每条结论标注来源），并用 HUD 输出调研结论与来源：${t}`,
  },
  {
    name: 'omd-autoresearch',
    description: '自动调研改进：评估器驱动的有界改进循环，持续改进到达标',
    hint: '<任务>',
    label: '自动调研',
    skill: 'omd-autoresearch',
    build: (t) => `请加载 omd-autoresearch skill，对以下任务做评估器驱动的有界改进循环直到达标，并用 HUD 输出轮次/评分/差距：${t}`,
  },
  {
    name: 'omd-ultragoal',
    description: '持久多目标：拆解多子目标，带 checkpoint 工件与台账，可恢复可审计',
    hint: '<目标>',
    label: '持久目标',
    skill: 'omd-ultragoal',
    build: (t) => `请加载 omd-ultragoal skill，把以下大目标拆成多子目标、带 checkpoint 工件与台账持续推进，并用 HUD 输出子目标进度：${t}`,
  },
]

export function apply(ctx) {
  for (const mode of MODES) {
    ctx.commands.register({
      name: mode.name,
      description: mode.description,
      input: { hint: mode.hint },
      handler: (invocation) => {
        const task = (invocation.rawInput || '').trim()
        if (!task) return { kind: 'error', text: `用法：/${mode.name} ${mode.hint}` }
        invocation.agent.followup(userMessage(mode.build(task)))
        return { kind: 'success', text: `${mode.label}已启动：${task}` }
      },
    })
  }
}
