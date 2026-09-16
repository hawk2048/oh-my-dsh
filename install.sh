#!/usr/bin/env sh
# Install oh-my-dsh as an agent preset (per-session composition) under
# $DSH_HOME/.agent-presets/oh-my-dsh. Run from a checkout of this repository.
# This is the "manual preset" path; the primary install is `dsh plugin add`.
#
# NON-DESTRUCTIVE by design: the preset directory is never deleted. Your own
# additions survive an upgrade:
#   - files this repo does not ship (e.g. a locally written skill) are left alone;
#   - a shipped file that WOULD overwrite a locally modified copy is backed up
#     first as <name>.bak-<timestamp>; only then is the shipped version copied.
# Re-running this script is therefore safe, and reversible.

set -eu

SRC="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
DST="$DSH_HOME/.agent-presets/oh-my-dsh"
STAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$DST"

# Back up $1 (relative to the preset root) when the local copy differs from ours.
backup_if_differs() {
  rel="$1"
  if [ -f "$DST/$rel" ] && [ -f "$SRC/$rel" ] && ! cmp -s "$SRC/$rel" "$DST/$rel"; then
    cp -p "$DST/$rel" "$DST/$rel.bak-$STAMP"
    echo "  backed up local $rel -> $rel.bak-$STAMP"
  fi
}

backup_if_differs agent.cordis.yml
backup_if_differs preset.yml

for d in skills commands; do
  [ -d "$SRC/$d" ] || continue
  find "$SRC/$d" -type f -print | while IFS= read -r f; do
    backup_if_differs "${f#"$SRC"/}"
  done
done

# Merge-copy: cp -R adds/overwrites the files we ship and touches nothing else.
cp "$SRC/agent.cordis.yml" "$SRC/preset.yml" "$DST/"
cp -R "$SRC/skills" "$SRC/commands" "$DST/"

echo "installed oh-my-dsh preset to $DST"

# Report what the upgrade left alone, so nothing local disappears silently.
LIST_DIR="$(mktemp -d)"
trap 'rm -rf "$LIST_DIR"' EXIT
find "$DST" -type f ! -name '*.bak-*' | sed "s|^$DST/||" | sort >"$LIST_DIR/installed"
{
  echo agent.cordis.yml
  echo preset.yml
  for d in skills commands; do
    [ -d "$SRC/$d" ] && find "$SRC/$d" -type f | sed "s|^$SRC/||"
  done
} | sort >"$LIST_DIR/shipped"
PRESERVED="$(comm -23 "$LIST_DIR/installed" "$LIST_DIR/shipped")"
if [ -n "$PRESERVED" ]; then
  echo "preserved files that this repo does not ship (left untouched):"
  echo "$PRESERVED" | sed 's/^/  /'
fi

echo "start a new session and select 'oh-my-dsh' from the preset picker."
