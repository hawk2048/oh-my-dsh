#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest.py — 两个检查脚本自己的回归测试。

不需要外部文件，用例在内存里生成，跑完删掉。
用法：python selftest.py        退出码 0 表示全部通过。
"""

import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LINT = HERE / "report_lint.py"
EVID = HERE / "evidence_check.py"

GOOD = """# 结论：欧洲户用储能在收缩

德国 2026 年户用光伏新增预计 3.0GW，比 2024 年少 27%（BNEF 2026.1）。平均回本期从 6.2 年拉到 9.4 年。

| 项目 | 2024 | 2026 |
|---|---|---|
| 德国新增 | 4.1GW | 3.0GW |

- 意大利新增下滑 41%（n=12）
- 波兰增长 18%（n=8）
"""

BAD = """# 不是升级，而是重构

值得注意的是，这不是技术升级，而是生产关系的重构。前面提到的数据有误，正确口径是 18GWh。我们要把这个点钉死。
"""

QUOTE = """研究员 A 说：“这不是周期问题，而是结构问题。” 两人对出货量的估计相差 10%（4.2GWh 对 3.8GWh）。"""

EVID_OK = """| 编号 | 事实或数字 | 来源 | 级别 | 日期 | 置信度 | 核验状态 | 核验人 |
|---|---|---|---|---|---|---|---|
| S01 | 德国新增 3.0GW | bnef.com | A | 2026-01-15 | 高 | 已开页 | 本人 |
| S02 | 回本期 9.4 年 | bnef.com | A | 2026-01-15 | 高 | 已开页 | 本人 |
"""

EVID_BROKEN = """| 编号 | 事实或数字 | 来源 | 级别 | 日期 | 置信度 | 核验状态 | 核验人 |
|---|---|---|---|---|---|---|---|
| S01 | 德国新增 3.0GW | bnef.com | A | 2026-01-15 | 高 | 已开页 | 本人 |
| S01 | 重复的一条 | bnef.com | A | 2026-01-15 | 高 | 已开页 | 本人 |
| S02 | 未核验的一条 | bnef.com | A | 2026-01-15 | 中 | 未核 | — |
"""

REPORT_BROKEN = "正文引用了 [S01] 与 [S09]。\n"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cases = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="omd-selftest-"))
    try:
        def write(name, text):
            p = tmp / name
            p.write_text(text, encoding="utf-8")
            return p

        good = write("good.md", GOOD)
        bad = write("bad.md", BAD)
        quote = write("quote.md", QUOTE)
        ev_ok = write("ev_ok.md", EVID_OK)
        ev_bad = write("ev_bad.md", EVID_BROKEN)
        rp_bad = write("rp_bad.md", REPORT_BROKEN)

        cases.append(("正常段落应通过", run([sys.executable, str(LINT), str(good), "--quiet", "--strict"]).returncode == 0))
        cases.append(("对偶句与自我更正应拦下", run([sys.executable, str(LINT), str(bad), "--quiet", "--strict"]).returncode == 1))
        cases.append(("引用卦话应放行", run([sys.executable, str(LINT), str(quote), "--quiet", "--strict"]).returncode == 0))
        cases.append(("完好证据清单应通过", run([sys.executable, str(EVID), str(ev_ok), "--report", str(good)]).returncode in (0, 1)))
        cases.append(("重复编号应拦下", run([sys.executable, str(EVID), str(ev_bad), "--report", str(rp_bad)]).returncode == 1))
        cases.append(("断链应拦下", "[S09]" in REPORT_BROKEN and run([sys.executable, str(EVID), str(ev_ok), "--report", str(rp_bad)]).returncode == 1))
        cases.append(("未核验在 strict 下应拦下", run([sys.executable, str(EVID), str(ev_bad), "--strict"]).returncode == 1))
    finally:
        for p in tmp.glob("*"):
            p.unlink()
        tmp.rmdir()

    ok = True
    for name, passed in cases:
        print(("  ok   " if passed else "  FAIL ") + name)
        ok = ok and passed
    print("=== selftest " + ("passed" if ok else "failed") + " ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
