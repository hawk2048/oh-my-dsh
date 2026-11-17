#!/usr/bin/env bash
# oh-my-workbuddy 安装脚本：把适配层 skill 复制到 WorkBuddy 用户级技能目录。
# 用法：bash workbuddy/install.sh [目标目录]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/skills"
DST="${1:-$HOME/.workbuddy/skills}"

if [ ! -d "$SRC" ]; then
  echo "错误：找不到 $SRC" >&2
  exit 1
fi

mkdir -p "$DST"
count=0
for d in "$SRC"/omd-*; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  cp -r "$d" "$DST/"
  count=$((count + 1))
done

# suite 入口
cp "$SCRIPT_DIR/SKILL.md" "$DST/oh-my-workbuddy-SKILL.md.tmp" 2>/dev/null || true
mkdir -p "$DST/oh-my-workbuddy"
cp "$SCRIPT_DIR/SKILL.md" "$DST/oh-my-workbuddy/SKILL.md"
rm -f "$DST/oh-my-workbuddy-SKILL.md.tmp"

echo "已安装 $count 个 omd skill + 1 个 suite 入口 → $DST"
echo "重启 WorkBuddy 会话后，用触发词即可（如「先规划一下」「autopilot 搭个 API」）。"
