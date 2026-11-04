#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_lint.py — 报告文字体检器（omd-autoresearch 附带的机器闸门）

只查**下限**：水词、AI 腔、句式骨架、密度、篇幅。
不判断观点对不对、逻辑通不通、数据真不真——那些交给评估子代理与人。

用法：
    python report_lint.py 报告.md                 # 整篇
    python report_lint.py 节.md --scale 0.6 --quiet  # 节级（短文本放宽密度阈值）
    python report_lint.py 报告.md --json          # 机器可读

退出码：0 = 通过（可含 warning）；1 = 有「判死」项。

阈值来源：ruanyf/document-style-guide（句长/段长/标题层级）、
MrGeDiao/shuorenhua hard_metrics（层次化判定 + 误杀防护思路）、
blader/humanizer（结构信号优先于词表）。
阈值未经本地语料标定，一律按「判死 / 报警」两档处置：报警只报数，不判负。
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------- 判死项

JUDGE_BANNED = {
    # 用户点名禁用，权重最高。逗号可有可无：中文里「不是A而是B」常常不加逗号，
    # 早期版本强制标点，导致这类变体全部漏检。
    "对偶转折句": [
        r"不是[^。，；！？\n]{2,24}[，,]?\s*而是",
        r"不是[^。，；！？\n]{2,24}[，,]?\s*是(?!的)",  # 省略「而」的变体：不是需求问题，是回本期问题
        r"并非[^。，；！？\n]{2,24}[，,]?\s*而是",
        r"与其说[^。，；！？\n]{2,24}[，,]?\s*不如",
        r"不在于[^。，；！？\n]{2,24}[，,]?\s*而在于",
        r"不(仅仅|只是|单)[^。，；！？\n]{2,24}[，,]?\s*更是",
        r"真正的[^。，；！？\n]{0,12}不是[^。，；！？\n]{2,20}[，,]?\s*(而)?是",
    ],
    "自我更正元叙述": [
        r"前面(说|提|写)错",
        r"之前(说|提|写)错",
        r"前面(提到|说|提|写|给)的[^。，\n]{0,24}(有误|不对|错了|有问题|是错的|站不住)",
        r"之前(提到|说|提|写|给)的[^。，\n]{0,24}(有误|不对|错了|有问题|是错的)",
        r"我(们)?(前面|刚才|上一条|上面)(说|提|写)的[^。\n]{0,12}(不对|有误|错了)",
        r"(纠正|更正|修正|勘误)一下",
        r"说错了",
        r"(正确|准确)的说法(应该)?是",
        r"重新说一遍",
        r"前面(那个|这|的)?(说法|结论|判断)[^。\n]{0,12}(不成立|要改|得改)",
    ],
    "生造黑话": [
        r"钉死", r"焊死", r"锁死", r"打死", r"拉齐", r"对齐颗粒度",
        r"抓手", r"闭环", r"赋能", r"沉淀", r"打通", r"水位", r"心智",
        r"体感", r"链路", r"势能", r"降维打击", r"组合拳", r"颗粒度",
        r"顶层设计", r"兜底", r"压实", r"收口", r"砍一刀", r"补一刀",
        # 比喻化生造：拿伤口、搏斗、烹饪比喻软件问题，正常人不会这么说
        r"小疤", r"打穿", r"啃下(了)?", r"拧巴", r"裸写", r"裸奔",
        r"缝补", r"硬掰", r"贴脸", r"焊在",
    ],
}

# 工程词外泄：工具输出与流程内部词，不该出现在给读者看的正文里。
# 判定分两档——纯行话直接判死，权衡用词只提示（对外报告可换，内部文档随意）。
TOOL_LEAK_JUDGE = [r"报警项", r"判死", r"判负", r"落盘", r"跑通", r"卡闸", r"fail\s*掉", r"打了个补丁",
                   r"机器判", r"人判", r"判据", r"口径", r"档位", r"编号制", r"自检"]
TOOL_LEAK_WARN = [r"闸门", r"拆轮", r"打标", r"跑一遍", r"收口", r"字段", r"条目"]

# 比喻与借代：拿别的东西指代报告里的概念。对外报告里直接说做了什么。
# 机器判比喻并不可靠，这里只收高频、且几乎不会作字面用的几个，命中只提示。
METAPHOR_WARN = [r"骨架", r"双轴", r"全家桶", r"台账", r"三角验证", r"抓手",
                 r"闭环", r"链路", r"小疤", r"打穿", r"地基", r"桥梁",
                 r"钥匙", r"落地生根", r"痛点"]

# 误杀防护：命中上下文白名单则计数作废（同音/同形但语义正常的用法）
FALSE_POSITIVE_GUARD = [
    r"闭环(控制|反馈|系统)", r"协同编辑", r"消防联动", r"用户洞察",
    r"颗粒度(测试|分析|采样)", r"链路(层|协议)", r"赋能(函数|接口)",
    # 字面义：这些词在行业报告里是正常表达，不是黑话
    r"(地下|河道|水库|海域|上游|中游)水位", r"水位[^，。\n]{0,8}(米|较|下降|上升|监测|站|线)",
    r"体感(温度|气温|温度计)", r"资金沉淀", r"化学沉淀", r"泥沙沉淀",
    r"沉淀(物|池|法|剂)", r"打通(最后一公里|隧道|电话)",
    r"心智(模型|发育|障碍)", r"势能(转化|守恒|势能面)",
]

# ---------------------------------------------------------------- 提示项

WARN_TICS = {
    "空转连接": ["值得注意的是", "值得一提的是", "需要指出的是", "不可否认的是",
             "不难发现", "不容忽视", "众所周知", "由此可见", "综上所述",
             "总而言之", "总的来说", "总体来看", "简而言之", "归根结底",
             "不言而喻", "换句话说", "也就是说", "具体来说", "更重要的是"],
    "开场套话": ["在当今", "随着.*的(不断|快速)(发展|推进)", "在这个.*的时代",
             "让我们一起来", "接下来我将", "深入探讨", "不得不说", "诚然"],
    "伪深刻": ["本质上是", "核心在于", "关键在于", "真正的问题在于",
            "从某种意义上", "某种程度上", "可以说", "这背后的逻辑",
            "标志着.*(新时代|新阶段)", "范式转移"],
    "拔高渲染": ["意义深远", "意义非凡", "前所未有", "史无前例", "毋庸置疑",
             "至关重要", "举足轻重", "令人瞩目", "值得深思", "发人深省",
             "发挥着关键作用", "颠覆性"],
    "客服腔": ["让我们一起", "我们可以看到", "希望.*对(你|您)有帮助",
            "如果(你|您)(还)?有(任何)?(其他)?(问题|疑问)", "祝(你|您).*愉快",
            "好问题", "你说得很对", "让我来为你", "要不要我"],
    "正能量收尾": ["让我们拭目以待", "未来可期", "积极拥抱", "只有.*才能.*未来"],
    "无源引用": ["研究表明", "数据显示", "有专家指出", "业内人士认为",
             "据报道", "观察人士", "有分析认为"],
    "程度副词堆砌": ["非常(重要|关键|显著)", "极大(地)?(提升|改善)",
               "显著(地)?(提升|改善)", "全方位", "深层次", "系统性地"],
}

NOMINALIZATION = [r"(进行|实现|完成|开展|起到|具有)(了)?(一)?(个|次)?[^。，\n]{0,6}(优化|提升|改进|调整|分析|管理|建设|部署)"]

# 阈值（--scale 只作用于 per_1000 类密度）
THRESHOLDS = {
    "sentence_hard": 60,        # 单句 > 60 字：判死
    "sentence_warn": 40,        # 单句 40–60 字：报警（ruanyf：>40 不可接受）
    "para_hard": 300,           # 单段 > 300 字：判死（≈7 行 × 43 字，行宽按手机估）
    "para_warn": 200,           # 单段 200–300：报警
    "dash_para_hard": 4,        # 单段 —— 数 ≥4：判死
    "dash_para_warn": 2,        # 单段 —— 数 ≥2：报警
    "bold_per_1000": 8,         # 加粗密度上限
    "tics_per_1000": 8,         # AI 腔词密度上限
    "numbers_per_1000": 6,      # 数字密度下限（低于=空话多）
    "visuals_per_1000": 1.2,    # 表格/图/清单密度下限（低于=枯燥）
}

SENT_SPLIT = re.compile(r"[。！？；\n]+")
CN_CHAR = re.compile(r"[\u4e00-\u9fff]")
NUM = re.compile(r"\d+(?:\.\d+)?%?|\d+\.\d+|"
                 r"[一二三四五六七八九十百千万亿]+(?:个|家|元|万|亿|%|年|月|倍|人|页|天)")
VISUAL_LINE = re.compile(r"^\s*(\||\s*[-*+]\s|\d+\.\s|>\s|```|!\[)")


def strip_code(text: str) -> str:
    """去掉围栏代码与行内代码：规则文档里的反例通常放在这两种容器里，不该被判违规。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]+`", "", text)


def struck_out(text: str, start: int, end: int) -> bool:
    """上下文白名单：命中即不计数。"""
    ctx = text[max(0, start - 8): end + 8]
    return any(re.search(p, ctx) for p in FALSE_POSITIVE_GUARD)


def parallelism_allowed(n: int) -> int:
    """对偶句豁免额度（含术语定义 1 处 + 论证骨架 1 处）。"""
    if n < 300:
        return 1
    if n < 1000:
        return 2
    return max(2, n // 300)


def is_quoted_pattern(text: str, start: int, end: int) -> bool:
    """命中处在「引用某个句式」而不是「使用某个句式」。

    例子：标题里写「（真正的…不是…而是…）」是在给句式命名，
    正文里写「真正的瓶颈不是产能，而是渠道库存」才是使用。
    判据：命中片段含省略号、紧挨中文引号/括号、或落在 Markdown 引用块里。
    """
    frag = text[start:end]
    if "…" in frag or "..." in frag:
        return True
    before = text[max(0, start - 2):start]
    after = text[end:end + 2]
    openers = "「『【（(“‘《〈"
    closers = "」』】）)”’》〉"
    if any(c in openers for c in before) or any(c in closers for c in after):
        return True
    line_start = text.rfind("\n", 0, start) + 1
    if text[line_start:line_start + 2].lstrip().startswith(">"):
        return True
    return False


def is_factual_correction(frag: str) -> bool:
    """两侧都带数字的「不是 X，而是 Y」是在更正数据，不是拔高句式。

    例：「不是 12GWh，而是 18GWh」应当放行；「不是技术升级，而是重构」应当拦下。
    """
    return len(re.findall(r"\d", frag)) >= 2


def find_dual_spans(text: str):
    """找出所有对偶转折句，并按字符区间合并重叠命中。

    多条正则会命中同一句话（例如「真正的瓶颈不是产能而是渠道」会同时被
    「不是…而是…」和「真正的…不是…是…」匹配），不合并就会把一句话算成三处，
    把合法的单次对比误判成超标。合并后一句话只算一处。
    """
    spans = []
    for pat in JUDGE_BANNED["对偶转折句"]:
        for m in re.finditer(pat, text):
            if struck_out(text, m.start(), m.end()):
                continue
            if is_quoted_pattern(text, m.start(), m.end()):
                continue
            if is_factual_correction(m.group(0)):
                continue
            spans.append((m.start(), m.end(), m.group(0)[:26]))
    spans.sort(key=lambda x: (x[0], -x[1]))
    merged = []
    for s, e, t in spans:
        if merged and s < merged[-1][1]:  # 有重叠 → 合并
            ps, pe, pt = merged[-1]
            merged[-1] = (ps, max(pe, e), pt if len(pt) >= len(t) else t)
        else:
            merged.append((s, e, t))
    return merged


def main() -> int:
    try:  # Windows 控制台默认 GBK，中文会乱码
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0,
                    help="密度阈值缩放，节级检查建议 0.6（只影响密度类阈值，不影响禁句/句长/段长）")
    ap.add_argument("--strict", action="store_true",
                    help="严格模式：数字密度、图表密度、AI 腔密度、加粗密度不达标也判死。"
                         "写报告的语言闸用它；改别人的稿子、做体检时不用。")
    ap.add_argument("--doc", action="store_true",
                    help="文档模式：跳过 AI 腔/加粗密度。用于检查技能文档自身——"
                         "规则表必须引用禁词，密度指标对它无意义。")
    args = ap.parse_args()

    raw = open(args.path, encoding="utf-8").read()
    text = strip_code(raw)
    n = len(CN_CHAR.findall(text)) or 1
    per1000 = 1000.0 / n

    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    body = [p for p in paras if not VISUAL_LINE.match(p) and not p.startswith("#")]
    body = body or paras
    para_lens = [len(CN_CHAR.findall(p)) for p in body]

    sentences = [s for s in SENT_SPLIT.split(text) if CN_CHAR.search(s)]
    sent_lens = [len(CN_CHAR.findall(s)) for s in sentences]

    fails, warns, metrics = [], [], {}

    # ---- 判死：点名禁句
    ban_detail = {}
    for label, pats in JUDGE_BANNED.items():
        if label == "对偶转折句":
            continue  # 单独按区间合并计数，见 dual_spans()
        hits = []
        for pat in pats:
            for m in re.finditer(pat, text):
                if struck_out(text, m.start(), m.end()):
                    continue
                hits.append(m.group(0)[:26])
        ban_detail[label] = hits

    dual_spans = find_dual_spans(text)
    ban_detail["对偶转折句"] = [t for _, _, t in dual_spans]
    ban_total = sum(len(v) for v in ban_detail.values())
    metrics["禁句总数"] = ban_total
    metrics["对偶句豁免额度"] = parallelism_allowed(n)

    dual = len(dual_spans)
    if dual > metrics["对偶句豁免额度"]:
        fails.append({
            "rule": "对偶转折句超限",
            "value": f"{dual} 处（额度 {metrics['对偶句豁免额度']}）",
            "samples": ban_detail["对偶转折句"][:3],
            "fix": "删掉否定半句，只留成立的那个判断；术语定义与论证骨架各留 1 处额度。",
        })
    if ban_detail["自我更正元叙述"]:
        fails.append({
            "rule": "报告正文出现自我更正",
            "value": f"{len(ban_detail['自我更正元叙述'])} 处",
            "samples": ban_detail["自我更正元叙述"][:3],
            "fix": "直接给正确版本，不叙述修正过程；确需记录就单开「修订记录」小节。",
        })
    if ban_detail["生造黑话"]:
        fails.append({
            "rule": "生造黑话",
            "value": f"{len(ban_detail['生造黑话'])} 处",
            "samples": ban_detail["生造黑话"][:4],
            "fix": "换成人话：钉死→确定下来，拉齐→统一口径，抓手→着手点，小疤→小问题。",
        })

    # ---- 工程词外泄（--doc 模式跳过：规则文档本来就要讨论这些词）
    if not args.doc:
        def leaks_of(pats):
            hits = []
            for p in pats:
                for m in re.finditer(p, text):
                    if is_quoted_pattern(text, m.start(), m.end()):
                        continue  # 引用他人的原话不改写
                    hits.append(m.group(0))
            return hits

        leaks = leaks_of(TOOL_LEAK_JUDGE)
        if leaks:
            fails.append({
                "rule": "工程词外泄",
                "value": f"{len(leaks)} 处",
                "samples": leaks[:4],
                "fix": "换成读者词：报警项→需要留意的地方，判死→不合格，落盘→存成文件，"
                       "跑通→验证通过。术语只在讨论工具本身时出现。",
            })
        soft = leaks_of(TOOL_LEAK_WARN)
        if soft:
            warns.append({"rule": "工程味偏重", "value": f"{len(soft)} 处",
                          "samples": soft[:4],
                          "fix": "对外报告可换成「检查项 / 关卡 / 一轮」这类日常说法。"})
        meta = [m.group(0) for p in METAPHOR_WARN for m in re.finditer(p, text)]
        if meta:
            warns.append({"rule": "出现比喻或借代", "value": f"{len(meta)} 处",
                          "samples": meta[:4],
                          "fix": "直接说做了什么：骨架→结构，台账→清单，抓手→着手点，"
                                 "打穿→彻底解决。对外报告里不用比喻。"})

    # ---- 判死：标题层级（一级标题下不得直接出现三级；不鼓励四级及以下）
    heads = [(len(m.group(1)), m.group(2).strip())
             for m in re.finditer(r"^(#{1,6})\s+(.+)$", raw, flags=re.M)]
    if heads:
        deepest = max(lv for lv, _ in heads)
        prev_level = 0
        jumped = False
        for lv, _ in heads:
            if lv > prev_level + 1 and lv >= 3:
                jumped = True
            prev_level = lv
        if jumped:
            fails.append({
                "rule": "标题层级跳级",
                "value": "一级标题下直接出现三级（或更深）",
                "fix": "补一级下的二级标题，或把该节降为二级。",
            })
        if deepest >= 4:
            warns.append({"rule": "出现四级及以下标题",
                          "value": f"最深 {deepest} 级",
                          "fix": "并列内容改用项目列表，少用四级标题。"})

    # ---- 判死：句长 / 段长 / 破折号
    long_sents = [x for x in sent_lens if x > THRESHOLDS["sentence_hard"]]
    if long_sents:
        fails.append({
            "rule": "超长句",
            "value": f"{len(long_sents)} 句 > {THRESHOLDS['sentence_hard']} 字（最长 {max(long_sents)}）",
            "fix": "拆句：一句只装一个意思，超过 40 字就找句号的位置。",
        })

    if para_lens and max(para_lens) > THRESHOLDS["para_hard"]:
        fails.append({
            "rule": "超长段",
            "value": f"最长 {max(para_lens)} 字 > {THRESHOLDS['para_hard']}",
            "fix": "拆段或删铺垫：一段一个主张，段首句就是主张。",
        })

    # 「——」由两个「—」组成，直接相加会把一处破折号算成三处
    def dash_count(p: str) -> int:
        pairs = p.count("——")
        return pairs + max(0, p.count("—") - 2 * pairs)

    dash_by_para = [dash_count(p) for p in body]
    if dash_by_para and max(dash_by_para) >= THRESHOLDS["dash_para_hard"]:
        fails.append({
            "rule": "破折号滥用",
            "value": f"单段最多 {max(dash_by_para)} 处",
            "fix": "破折号换句号/冒号/括号，或直接断句。",
        })

    # ---- 报警：AI 腔词
    tic_total = 0
    for label, pats in WARN_TICS.items():
        hits = []
        for pat in pats:
            for m in re.finditer(pat, text):
                hits.append(m.group(0)[:18])
        tic_total += len(hits)
        metrics[f"腔:{label}"] = len(hits)
        if hits:
            warns.append({
                "rule": f"AI腔/{label}",
                "value": f"{len(hits)} 处",
                "samples": hits[:4],
                "fix": "删连接词直接接事实，或把形容词换成数字。",
            })

    # ---- 报警：句长/段长/破折号轻档
    mid_sents = [x for x in sent_lens if THRESHOLDS["sentence_warn"] < x <= THRESHOLDS["sentence_hard"]]
    if mid_sents:
        warns.append({"rule": "偏长句", "value": f"{len(mid_sents)} 句 40–60 字",
                      "fix": "拆成两句，或删掉句中的解释性从句。"})
    if para_lens and max(para_lens) > THRESHOLDS["para_warn"] >= 0:
        over = [x for x in para_lens if x > THRESHOLDS["para_warn"]]
        if over and max(para_lens) <= THRESHOLDS["para_hard"]:
            warns.append({"rule": "偏长段", "value": f"{len(over)} 段 200–300 字",
                          "fix": "拆段，手机一屏读不完的段落读者会跳过。"})
    if dash_by_para and THRESHOLDS["dash_para_warn"] <= max(dash_by_para) < THRESHOLDS["dash_para_hard"]:
        warns.append({"rule": "破折号偏多", "value": f"单段最多 {max(dash_by_para)} 处",
                      "fix": "一段最多保留一处真正承担插入的破折号。"})

    nom = sum(len(re.findall(p, text)) for p in NOMINALIZATION)
    metrics["名词化"] = nom

    # ---- 密度
    metrics["中文字数"] = n
    metrics["段落数"] = len(body)
    metrics["平均段长"] = round(sum(para_lens) / max(len(para_lens), 1), 1)
    metrics["最长段"] = max(para_lens) if para_lens else 0
    metrics["平均句长"] = round(sum(sent_lens) / max(len(sent_lens), 1), 1)
    metrics["最长句"] = max(sent_lens) if sent_lens else 0
    metrics["破折号峰值/段"] = max(dash_by_para) if dash_by_para else 0
    metrics["加粗/千字"] = round(len(re.findall(r"\*\*[^*]+\*\*", text)) * per1000, 2)
    metrics["AI腔/千字"] = round(tic_total * per1000, 2)
    # 引用编号（[S07]）里的数字不算数据，否则一份通篇回指编号的稿子会轻易过数字密度
    text_for_numbers = re.sub(r"\[S\d+\]", " ", text)
    metrics["数字/千字"] = round(len(NUM.findall(text_for_numbers)) * per1000, 2)
    # 表格与列表按「块」计：一张六行表算一处，一组列表算一处
    visuals, prev_kind = 0, None
    for line in raw.splitlines():
        m = VISUAL_LINE.match(line)
        kind = None
        if m:
            kind = "table" if line.lstrip().startswith("|") else "list"
        if kind and kind != prev_kind:
            visuals += 1
        prev_kind = kind
    metrics["图表清单数"] = visuals
    metrics["图表/千字"] = round(visuals * per1000, 2)

    def warn_density(key, limit, lower_bad, label, fix, min_chars=0, mode="upper"):
        """密度类阈值默认只报警；--strict 时升级为判死。

        --scale 的方向：上限型（越少越好，如 AI 腔、加粗）用 limit/scale，
        下限型（越多越好，如数字、图表）用 limit*scale。这样 --scale 0.6
        对短节是「放宽」而不是「收紧」——短文本的密度天然抖动大。
        """
        if n < min_chars:
            return
        v = metrics[key]
        lim = limit / s if mode == "upper" else limit * s
        bad = v < lim if lower_bad else v > lim
        if not bad:
            return
        item = {"rule": label, "value": v, "limit": round(lim, 2), "fix": fix}
        (fails if args.strict else warns).append(item)

    s = args.scale
    if not args.doc:  # 规则文档要列举禁词与反例，密度类指标对它没有意义
        warn_density("AI腔/千字", THRESHOLDS["tics_per_1000"], False,
                     "AI 腔词密度超标", "按上面每类的 fix 逐条改。", mode="upper")
        warn_density("加粗/千字", THRESHOLDS["bold_per_1000"], False,
                     "加粗过多", "只加粗结论和数字，一段最多一处。", mode="upper")
    warn_density("数字/千字", THRESHOLDS["numbers_per_1000"], True,
                 "数字密度过低（空话多）", "每个论断补数字/时间/金额/人名；补不出的论断删掉。",
                 mode="lower")
    # 短节不判图表密度：200 字的节不该被要求塞一张表
    warn_density("图表/千字", THRESHOLDS["visuals_per_1000"], True,
                 "表格清单过少（枯燥）", "并列 ≥3 项一律表格化；每 800 字至少一处表格或清单。",
                 min_chars=400, mode="lower")

    passed = not fails
    out = {"file": args.path, "passed": passed, "metrics": metrics,
           "fails": fails, "warns": warns}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.quiet:
        print("PASS" if passed else "FAIL")
        for f in fails:
            print(f"  ✗ {f['rule']}: {f['value']}  样例 {f.get('samples', '')}")
            print(f"      改法：{f['fix']}")
        for w in warns:
            print(f"  ⚠ {w['rule']}: {w['value']}")
    else:
        print(f"== {args.path} ==")
        print(f"字数 {n} / 段 {len(body)} / 图表清单 {visuals} | "
              f"平均段长 {metrics['平均段长']} 最长段 {metrics['最长段']} | "
              f"平均句长 {metrics['平均句长']} 最长句 {metrics['最长句']}")
        print(f"数字 {metrics['数字/千字']}/千字 · AI腔 {metrics['AI腔/千字']}/千字 · "
              f"禁句 {ban_total} 处（对偶额度 {metrics['对偶句豁免额度']}）")
        for f in fails:
            print(f"  ✗ [判死] {f['rule']}: {f['value']}  样例 {f.get('samples', '')}")
            print(f"           改法：{f['fix']}")
        for w in warns:
            print(f"  ⚠ [报警] {w['rule']}: {w['value']} → {w['fix']}")
        print("结论：", "PASS" if passed else "FAIL")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
