# Install oh-my-dsh as an agent preset (per-session composition) under
# $DSH_HOME/.agent-presets/oh-my-dsh. Run from a checkout of this repository.
# This is the "manual preset" path; the primary install is `dsh plugin add`.

$ErrorActionPreference = 'Stop'

$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME '.dsh' }
$dst = Join-Path $dshHome '.agent-presets\oh-my-dsh'

Remove-Item $dst -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $dst | Out-Null

Copy-Item (Join-Path $src 'agent.cordis.yml') $dst -Force
Copy-Item (Join-Path $src 'preset.yml') $dst -Force
Copy-Item (Join-Path $src 'skills') (Join-Path $dst 'skills') -Recurse -Force
Copy-Item (Join-Path $src 'commands') (Join-Path $dst 'commands') -Recurse -Force

Write-Host "installed oh-my-dsh preset to $dst"
Write-Host "start a new session and select 'oh-my-dsh' from the preset picker."
