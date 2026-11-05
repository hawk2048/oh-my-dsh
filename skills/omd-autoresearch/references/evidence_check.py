#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""evidence_check.py — 证据清单与正文的一致性检查（omd-autoresearch 附带）

查四件事：
  1. 编号有没有重复
  2. 正文引用的编号，清单里有没有（断链）
  3. 清单里有没有条目从未被正文引用（闲置）
  4. 还没有核验过的条目有哪些（--strict 时视为不合格）

用法：
    python evidence_check.py evidence.md --report REPORT.md
    python evidence_check.py evidence.md --report REPORT.md --strict --json

退出码：0 通过；1 有不合格项。
"""

import argparse
import json
import re
import sys

CITE = re.compile(r"\[(S\d+)\]")
HEAD_ALIASES = {
    "编号": "id", "id": "id",
    "事实或数字": "fact", "事实": "fact", "内容": "fact",
    "来源": "source",
    "级别": "level", "来源类型": "level",
    "日期": "date",
    "置信度": "confidence",
    "核验状态": "status", "核验": "status",
    "核验人": "checker", "核验者": "checker",
}
VERIFIED = {"已开页", "已交叉", "已核", "verified", "checked"}


def parse_table(text: str):
    """取文件里第一张表（连续以 | 开头的行）。返回 (headers, rows)。

    只取一张：文件后面可能还有别的表（比如机制登记），混进来会串行。
    """
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith("|")), None)
    if start is None:
        return [], []
    block = []
    for ln in lines[start:]:
        if not ln.strip().startswith("|"):
            break
        block.append(ln.strip())
    if not block:
        return [], []
    header = [c.strip() for c in block[0].strip("|").split("|")]
    keys = [HEAD_ALIASES.get(h, h) for h in header]
    body = []
    for ln in block[1:]:
        if re.fullmatch(r"\|[\s:\-|]+\|", ln):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        body.append(dict(zip(keys, cells)))
    return keys, body


def citations(text: str):
    """正文里引用的编号。行内代码与引号里的内容不算：那通常是在讲别人的编号规则。"""
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = re.sub(r"「[^」\n]*」|“[^”\n]*”", " ", text)
    return set(CITE.findall(text))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("evidence")
    ap.add_argument("--report", default="", help="正文文件，用来查断链与闲置")
    ap.add_argument("--strict", action="store_true", help="未核验的条目也判不合格")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ev_text = open(args.evidence, encoding="utf-8").read()
    keys, rows = parse_table(ev_text)

    ids = [r.get("id", "") for r in rows if r.get("id")]
    dup = sorted({i for i in ids if ids.count(i) > 1})

    report_ids = set()
    if args.report:
        report_text = open(args.report, encoding="utf-8").read()
        report_ids = citations(report_text)

    missing = sorted(report_ids - set(ids))
    unused = sorted(set(ids) - report_ids) if args.report else []

    statuses = {}
    pending = []
    if "status" in keys:
        for r in rows:
            st = r.get("status", "").strip()
            statuses[st or "(空)"] = statuses.get(st or "(空)", 0) + 1
            if st not in VERIFIED:
                pending.append(r.get("id", ""))

    fails, warns = [], []
    if dup:
        fails.append({"rule": "编号重复", "value": dup,
                      "fix": "同一编号只能登记一条，重复的改号或合并。"})
    if missing:
        fails.append({"rule": "正文引用了清单里没有的编号", "value": missing,
                      "fix": "补进证据清单，或删掉正文里这条引用。"})
    if keys and "status" not in keys:
        warns.append({"rule": "清单没有核验状态列", "value": "全部条目",
                      "fix": "加「核验状态」与「核验人」两列，写清谁核过、核到什么程度。"})
    if pending:
        msg = {"rule": "未核验的条目", "value": pending,
               "fix": "打开原始来源核对，把状态改成已开页或已交叉；核不了的降级或删掉。"}
        (fails if args.strict else warns).append(msg)
    if unused:
        warns.append({"rule": "登记了但正文没用", "value": unused[:10],
                      "fix": "用上它，或在清单里标明仅登记、不参与结论。"})

    passed = not fails
    out = {"evidence": args.evidence, "report": args.report or None,
           "passed": passed, "entries": len(rows),
           "statuses": statuses, "fails": fails, "warns": warns}

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"证据 {len(rows)} 条" + (f" · 正文引用 {len(report_ids)} 个编号" if args.report else ""))
        if statuses:
            print("核验状态：" + " · ".join(f"{k} {v}" for k, v in sorted(statuses.items())))
        for f in fails:
            print(f"  ✗ {f['rule']}: {f['value']}")
            print(f"      改法：{f['fix']}")
        for w in warns:
            print(f"  ⚠ {w['rule']}: {w['value']}")
        print("结论：", "PASS" if passed else "FAIL")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
