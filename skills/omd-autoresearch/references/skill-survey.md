# 外部报告类 Skill 调研结论（哪个能强化 omd-autoresearch）

调研时间：2026-11-03。方法：GitHub API + raw 原文直读（web 搜索通道当时不可用）。
可信度标注：**已核** = 读到 SKILL.md/README 原文；**仅元数据** = 只核到仓库存在、star、描述；**未找到** = 在可访问来源里没定位到，不臆测其机制。

---

## 一、六个指定技能

### 1. huashu-report（花叔报告）· 已核

`github.com/alchaincyf/huashu-report` · MIT · 484★（2026-11-04 复核）· 作者 alchaincyf
规范取自 42 份顶级机构报告 PDF 的反向拆解（Stanford HAI、McKinsey、BCG、OpenAI、Anthropic、PwC、World Bank）。

工作流：三问定原型 → 建数据表 → 写正文 → 补机制与文献定位 → 做图 → 逐页自检。

可迁移机制：

- **每个百分比必须带分母 N**，没有 N 的百分比视为不可用。
- **图表标题写结论**，不写主题（研报型例外）。
- **预先反驳自己四段式**：列替代解释 → 各自怎么排除 → 诚实说没排除掉的 → 主动降级结论。
- **删除判据**：「把这句话删掉，读者对结论的判断会不会改变？不变就是工作日志，删。」
- **附录 ≤ 正文 10%**，附录是来源表，不是数据表转印。
- **数据源行**：区分「谁采的数」和「谁做的图」。
- **「太干」的正解是补机制层与文献定位层**；加形容词、换口语化都不管用。

它没解决的：口语化、逐句改写的机械规则（它靠原型选型与删除判据治「读不下去」）。

### 2. deep-research-plus-skills · 已核（影响面小）

`github.com/Asaceoo/deep-research-plus-skills` · MIT · 1★ · 作者 Asaceoo
编排层，把 4 个调研子技能串成流水线。社区验证为零，机制可抄，别当权威。

可执行面（复核补记）：`scripts/drp.py` 为 89.8 KB 的五阶段闸门，`validate_json.py` 两处，`tests/` 下 8 个 pytest 文件，`checklists/` 带通过样本。

可迁移机制：

- **闸门外置成脚本退出码**：`gate --stage outline|confirm|results|review|report`，0 通过 / 1 违规。
- **大纲强制至少 1 条反方条目**（竞品反对、已知缺陷、失效场景），否则拦下。
- **来源数下限是公式**：档位基数 + 反方加权，只搜一次就落盘会被判违规。
- **引用是硬字段**：完整 URL + 日期 + 来源类型枚举，裸域名判 0。
- **承重引用开页核对**：链接能打开不算数，要确认内容支撑结论。
- **单源标 `single-source`，社区来源支撑决策级结论标 `high-risk`。**
- **固定六章骨架，缺章不合格**；复杂度分档（light 档不产出完整报告）。

### 3. industry-research · 已核（同名歧义多）

`github.com/geekjourneyx/industry-research` · MIT · 33★ · 作者 geekjourneyx
同名/近名仓库另有 5 个以上（`hehe-industry-research-skill-pack` 315★、`PerryLink/dsh-industry-research` 215★、`luopan` 390★ 等），若指的是别的版本需回退确认。

核心信条：**搜索结果只是线索，不是证据。**

可执行面（复核补记）：`scripts/validate_report.py` 校验分档必需章节、引用数、置信度与工作区必需文件；另有 Go CLI 与其单元测试、`evals/evals.json`。


可迁移机制：

- **四层证据分层，禁止越级**：搜索结果 → 来源材料 → 推理（显式标注）→ 结论（置信度匹配证据质量）。
- **A/B/C 证据级 + 5 个独立证据家族三角验证**；同一家族的多个信号只算一个。
- **证据 schema 必填**：来源类型枚举、核实状态（仅检索到 / 已开页 / 已交叉）、独立性说明。
- **时效规则**：>180 天视为陈旧，不能单独支撑当前判断。
- **反证三问**：什么证据能证明它错？查过没有？没找到是因为结论硬，还是数据拿不到？
- **诚实空手离场**：找不到反证就标 `DATA_INSUFFICIENT_FOR_BEAR_CASE`，禁止编造风险。
- **篇幅三联表**：深度级别 × 目标字数 × 章节强制性。

### 4. research-copilot · 已核

`github.com/ptt-22/research-copilot`（3★；另有 `tririver/arc` 114★ 等相近项，未逐一验证）
手动触发型深度调研：先定研究边界 → 读 report-framework → 多源采集 → 证据账本 → 交叉验证 → 结构化报告，默认出 MD/HTML/DOCX/PDF 四份。

可迁移机制：

- **来源编号制 `[S3]`**，正文引用即回指，和本技能的 `evidence.md` 同构。
- **来源四级 A/B/C/D**，C 级只能证明「有人这样反馈」，不能证明客观事实。
- **主张级缺口标注**：`单一来源` / `未充分交叉验证` / `来源冲突` / `未找到一手来源`。
- **转载不算多源**：多篇转同一原始报道按一个来源计。
- **默认深度**：≥20 个候选来源，最终引用 12–25 个高质量来源。

### 5. Xiaobai-Research · 未找到

在 GitHub 仓库搜索、中文关键词组合（小白 调研 skill / Xiaobai research）里都没有定位到同名项目。
可能是本地自制、付费社群内部分发或已改名。**本技能不采用任何未核实的「小白向机制」描述**——需要用户提供路径或链接后再补。

### 6. fxbaogao-deep-research · 已核

`github.com/fxbaogao/fxbaogao-deep-research` · 10★ · 作者 fxbaogao（发现报告）
方法叫「先想后搜」：明确研究边界 → MECE 拆子问题 → 按子问题定向搜研报 → 筛选核心研报精读 → 整理成事实卡片 → 对比推导 → 结构化结论。

可迁移机制：

- **子问题先行**：先出问题清单再检索，避免「搜到哪算哪」。
- **中间产物模板化**：问题拆解 / 资料来源 / 事实卡片 / 对比框架 / 推导过程 / 终稿六件套，正文之前先有卡片。
- **研报精读 playbook**：把长报告拆成可复用的抽取规则。

---

## 二、其他更值得抄的（本次调研新增）

### 2.0 书面 / 口语表达类，单独立一条

`github.com/op7418/Humanizer-zh` · 21880 星 · MIT · 已核（仓库元数据，未读规则正文）
Humanizer 的汉化版，目标是消除中文文本里的 AI 痕迹。同类的还有 `MrGeDiao/shuorenhua`（2435 星）与英文原版 `blader/humanizer`（64268 星），三家分工不同：

| 项目 | 覆盖 | 缺什么 |
|---|---|---|
| blader/humanizer | 英文 AI 写作特征，按强度分级 | 中文句式与黑话 |
| Humanizer-zh | 中文 AI 痕迹，汉化后的规则集 | 未覆盖工程词外泄 |
| shuorenhua | 中文黑话 + 可脚本化指标 + 标定方法 | 需要自备语料 |

**要不要为「书面 / 口语表达」单独做一个 omd 技能？判断：不单独做。** 现有三处已经覆盖，再加一处会互相打架——写作时的用词规则在 `report-style.md`，事后清理在 `omd-ai-slop-cleaner`，外部机制来自上表三家。真正缺的那一层是语域问题：工具内部词混进给读者的正文（`报警项`、`判死`、`小疤`）。这一层不属于「表达技能」，已经补进 `report-style.md` 的「语域：三类词别混用」和 `report_lint.py` 的工程词检查。

| 项目 | 规模 | 抄什么 |
|---|---|---|
| `blader/humanizer` | 64k★ MIT 已核 | 模式**按强度排序**：强信号单次即改，弱信号同段凑够才改；工作流固定「标 tell → 起草 → 复检」；结论是「结构习惯比词表更持久」 |
| `MrGeDiao/shuorenhua` | 2.4k★ MIT 已核 | **可脚本化的判定从 judge 手里拿走**（句长离散度、破折号密度、留存率）；阈值必须在自己语料上标定；设误杀率门禁 |
| `Weizhena/Deep-Research-skills` | 2.5k★ MIT 已核 | 调研编译成两个机器可读契约（大纲 + 字段），每条产出过 `validate_json.py` 才算完成，不确定值填「[不确定]」并登记 |
| `tonyazhuuki/deep-research-skill` | 32★ MIT 已核 | 证据评鉴拆两根轴（因果是否成立 / 强度与适用性），置信度不足自动追加一轮深挖（≤2 轮），引用由脚本真去查库 |
| `ruanyf/document-style-guide` | 13k★ 已核（许可证未核到） | 中文句长/段长/标题层级的硬数字：单句 >40 字不可接受，段落 ≤7 行，尽量避免四级标题 |
| `Leonxlnx/unlazy` | 4.3k★ 仅元数据 | 给每个叶子节点分配完整时间预算，用结构对抗提前收尾 |

采购判据（本次调研得出）：合格的调研技能至少有 ①机器可校验的产物 schema 或校验脚本 ②不确定如何标注的协议 ③人工审批闸门 ④有阈值的评分表。四条缺两条，基本是提示词空话。

---

## 三、采纳了什么，没采纳什么

| 机制 | 来源 | 采纳 | 落在哪 |
|---|---|---|---|
| 篇幅档位（brief/standard/comprehensive）| industry-research、deep-research-plus | ✅ | SKILL.md 第 0 步 |
| 证据编号 + 来源分级 + 去重 + 时效 | research-copilot、industry-research | ✅ | `report-rules.md` §1–3 |
| 反证四段式 + 诚实空手离场 | huashu-report、industry-research | ✅ | `report-rules.md` §4 |
| 承重引用开页核对 | deep-research-plus | ✅ | `report-rules.md` §3 |
| 六章骨架 + 缺章不合格 | deep-research-plus | ✅ | `report-rules.md` §5 |
| 大纲必须含反方条目，否则拦下 | deep-research-plus | ✅ | `SKILL.md` 第 3 步结构闸 + `report-rules.md` §4 |
| 来源数下限按档位定 | deep-research-plus、research-copilot | ✅ | `SKILL.md` 第 0 步（brief 3 / standard 6 / comprehensive 12） |
| 补「机制层 + 文献定位层」治太干 | huashu-report | ✅ | `rubric.md` D2 与 `SKILL.md` 报告硬规则 |
| 百分比必须带分母 N | huashu-report | ✅ | `report-rules.md` §3、§6；`rubric.md` D1 |
| 引用即硬字段（URL+日期+类型，裸域名不算） | deep-research-plus | ✅ | `report-rules.md` §1 证据表字段 |
| 单源 / 社区来源显式标注 | deep-research-plus、research-copilot | ✅ | `report-rules.md` §3 缺口标注 |
| 标题层级（一级下不跳三级、少用四级） | ruanyf | ✅ | `report_lint.py` 标题跳级判死 + `report-style.md` 排版表 |
| 删除判据 + 附录 ≤10% | huashu-report | ✅ | `report-rules.md` §6 |
| 图表标题写结论 + 数据源行 | huashu-report | ✅ | `report-rules.md` §6 |
| 分级处置（强信号即改 / 弱信号凑够 / 只报警）| blader/humanizer、shuorenhua | ✅ | `report-style.md` 分级处置 |
| 对偶句密度判死 + 豁免额度 | shuorenhua、ruanyf | ✅ | `report-style.md` T1-1 |
| 句长/段长/破折号硬阈值 | ruanyf、shuorenhua | ✅ | `report_lint.py` |
| 连词密度不设全局阈值 | shuorenhua 实测反例 | ✅（反向采纳）| `report-style.md` T3 |
| 机器闸门脚本化 | deep-research-plus、shuorenhua | ✅ | `report_lint.py` |
| 闸门外置成 CLI 退出码全流程 | deep-research-plus | ❌ | 依赖外部脚本，DSH 内无对应能力；改用 lint 退出码做单点闸 |
| 契约文件 + validate_json 全流程 | Weizhena | ❌ | 与 omd-research 子代理分工重复，收益低于复杂度 |
| 红队/蓝队/仲裁四角色 | industry-research | ❌ | 单份报告成本过高；已用「反证段 + 评估者」覆盖 |
| 研报精读 playbook | fxbaogao | ❌ | 依赖发现报告站点 API，非通用 |
| 四种格式同源导出 | research-copilot | ❌ | 交付格式另有 office-* 技能负责 |

## 四、结论

能强化 `omd-autoresearch` 的是四类机制，不是四个 skill：

1. **篇幅与骨架先定**（industry-research、deep-research-plus）→ 治「太长」。
2. **证据编号与来源分级**（research-copilot、industry-research、huashu）→ 治「不可信」。
3. **反证层与机制层**（huashu、industry-research）→ 治「太干」，这是最反直觉的一条：加一层解释，比加形容词有效。
4. **机器闸门 + 分级处置**（shuorenhua、blader、ruanyf）→ 治「AI 腔」，且不会误杀正常文本。

Xiaobai-Research 未核实，未采纳。若有具体来源，把它补进 `report-style.md` 的误杀防护表即可。
