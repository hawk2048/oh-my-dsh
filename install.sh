#!/usr/bin/env sh
# Install oh-my-dsh as an agent preset (per-session composition) under
# $DSH_HOME/.agent-presets/oh-my-dsh. Run from a checkout of this repository.
# This is the "manual preset" path; the primary install is `dsh plugin add`.

set -eu

SRC="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
DST="$DSH_HOME/.agent-presets/oh-my-dsh"

rm -rf "$DST"
mkdir -p "$DST"

cp "$SRC/agent.cordis.yml" "$SRC/preset.yml" "$DST/"
cp -R "$SRC/skills" "$SRC/commands" "$DST/"

echo "installed oh-my-dsh preset to $DST"
echo "start a new session and select 'oh-my-dsh' from the preset picker."
