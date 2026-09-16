#!/usr/bin/env sh
# Regression guard for the preset installer.
#
# The install scripts used to `rm -rf` the preset directory, which silently
# destroyed anything the user had added there (a locally written skill, local
# edits to agent.cordis.yml). This test pins the non-destructive contract:
#
#   1. the scripts never delete the preset directory (source-level check)
#   2. a file the repo does not ship survives an install
#   3. a shipped file that would overwrite a locally modified copy is backed up
#      first, and the backup keeps the local content
#   4. the shipped version is what ends up installed
#   5. re-running is idempotent (no second backup)
#
# Every assertion is written so a failure is REPORTED and counted, never
# allowed to abort the run — a guard that stops at the first failure hides the
# rest of the damage it is supposed to describe.

set -u

REPO="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

HOMEDIR="$TMP/home"
PRESET="$HOMEDIR/.agent-presets/oh-my-dsh"
fails=0

pass() { echo "  ok   $1"; }
fail() { echo "  FAIL $1"; fails=$((fails + 1)); }

expect_file() { if [ -f "$1" ]; then pass "$2"; else fail "$2"; fi; }
expect_contains() {
  if grep -q -- "$1" "$2" 2>/dev/null; then pass "$3"; else fail "$3"; fi
}
expect_absent() {
  if grep -qE -- "$1" "$2" 2>/dev/null; then fail "$3"; else pass "$3"; fi
}
expect_same() { if cmp -s "$1" "$2"; then pass "$3"; else fail "$3"; fi; }
expect_count() {
  n="$(ls $1 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$n" = "$2" ]; then pass "$3"; else fail "$3 (got $n, want $2)"; fi
}
run_installer() {
  if DSH_HOME="$HOMEDIR" sh "$REPO/install.sh" >"$1" 2>&1; then return 0; else return 1; fi
}

echo "[1] source-level: the preset directory is never deleted"
expect_absent 'rm[[:space:]]+-rf[[:space:]]+"?\$DST' "$REPO/install.sh" \
  "install.sh does not remove \$DST"
expect_absent 'Remove-Item[[:space:]]+\$dst' "$REPO/install.ps1" \
  "install.ps1 does not remove \$dst"

echo "[2] behaviour: install over a preset that already has local content"
mkdir -p "$PRESET/skills/my-local-skill"
echo "mine" >"$PRESET/skills/my-local-skill/SKILL.md"
cp "$REPO/agent.cordis.yml" "$PRESET/agent.cordis.yml"
echo "# MY-LOCAL-CONFIG" >>"$PRESET/agent.cordis.yml"
LOCAL_SKILL="$PRESET/skills/my-local-skill/SKILL.md"

if run_installer "$TMP/run1.log"; then pass "install.sh exits 0"; else fail "install.sh exits non-zero"; fi

expect_file "$LOCAL_SKILL" "local-only skill preserved"
expect_file "$PRESET/skills/omd-pyramid/SKILL.md" "shipped skill installed"
expect_contains "my-local-skill" "$TMP/run1.log" "run reports the preserved file"

BACKUP="$(ls "$PRESET"/agent.cordis.yml.bak-* 2>/dev/null | head -1 || true)"
if [ -n "$BACKUP" ]; then
  pass "local config was backed up before being overwritten"
  expect_contains "MY-LOCAL-CONFIG" "$BACKUP" "backup keeps the local content"
else
  fail "no backup of the locally modified agent.cordis.yml"
fi
expect_same "$REPO/agent.cordis.yml" "$PRESET/agent.cordis.yml" \
  "shipped agent.cordis.yml is the installed one"

echo "[3] behaviour: re-running is idempotent"
if run_installer "$TMP/run2.log"; then pass "second run exits 0"; else fail "second run exits non-zero"; fi
expect_count "$PRESET/agent.cordis.yml.bak-*" 1 "still exactly 1 backup"
expect_file "$LOCAL_SKILL" "local-only skill still preserved"

echo
if [ "$fails" -eq 0 ]; then
  echo "=== install tests passed ==="
  exit 0
fi
echo "=== $fails install test(s) FAILED ==="
exit 1
