# Install oh-my-dsh as an agent preset (per-session composition) under
# $DSH_HOME\.agent-presets\oh-my-dsh. Run from a checkout of this repository.
# This is the "manual preset" path; the primary install is `dsh plugin add`.
#
# NON-DESTRUCTIVE by design: the preset directory is never deleted. Your own
# additions survive an upgrade:
#   - files this repo does not ship (e.g. a locally written skill) are left alone;
#   - a shipped file that WOULD overwrite a locally modified copy is backed up
#     first as <name>.bak-<timestamp>; only then is the shipped version copied.
# Re-running this script is therefore safe, and reversible.

$ErrorActionPreference = 'Stop'

$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME '.dsh' }
$dst = Join-Path $dshHome '.agent-presets\oh-my-dsh'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

New-Item -ItemType Directory -Force -Path $dst | Out-Null

# Every file this repo ships, relative to the checkout root.
$shipped = New-Object System.Collections.Generic.List[string]
$shipped.Add('agent.cordis.yml')
$shipped.Add('preset.yml')
foreach ($d in @('skills', 'commands')) {
  $root = Join-Path $src $d
  if (Test-Path $root) {
    Get-ChildItem -Path $root -Recurse -File | ForEach-Object {
      $shipped.Add($_.FullName.Substring($src.Length + 1))
    }
  }
}

function Backup-IfDiffers {
  param([string]$Rel)
  $destPath = Join-Path $dst $Rel
  $srcPath = Join-Path $src $Rel
  if (-not (Test-Path $destPath -PathType Leaf)) { return }
  if (-not (Test-Path $srcPath -PathType Leaf)) { return }
  $localHash = (Get-FileHash -Path $destPath -Algorithm SHA256).Hash
  $shippedHash = (Get-FileHash -Path $srcPath -Algorithm SHA256).Hash
  if ($localHash -ne $shippedHash) {
    Copy-Item -Path $destPath -Destination "$destPath.bak-$stamp" -Force
    Write-Host "  backed up local $Rel -> $Rel.bak-$stamp"
  }
}

foreach ($rel in $shipped) { Backup-IfDiffers -Rel $rel }

# Merge-copy: Copy-Item adds/overwrites the files we ship and touches nothing else.
Copy-Item (Join-Path $src 'agent.cordis.yml') $dst -Force
Copy-Item (Join-Path $src 'preset.yml') $dst -Force
Copy-Item (Join-Path $src 'skills') (Join-Path $dst 'skills') -Recurse -Force
Copy-Item (Join-Path $src 'commands') (Join-Path $dst 'commands') -Recurse -Force

Write-Host "installed oh-my-dsh preset to $dst"

# Report what the upgrade left alone, so nothing local disappears silently.
$installed = Get-ChildItem -Path $dst -Recurse -File |
  Where-Object { $_.Name -notmatch '\.bak-\d{8}-\d{6}$' } |
  ForEach-Object { $_.FullName.Substring($dst.Length + 1) }
$preserved = $installed | Where-Object { -not $shipped.Contains($_) }
if ($preserved) {
  Write-Host "preserved files that this repo does not ship (left untouched):"
  $preserved | ForEach-Object { Write-Host "  $_" }
}

Write-Host "start a new session and select 'oh-my-dsh' from the preset picker."
