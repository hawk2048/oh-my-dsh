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

# Merge-copy: add/overwrite the files this repo ships and touch nothing else.
Copy-Item (Join-Path $src 'agent.cordis.yml') $dst -Force
Copy-Item (Join-Path $src 'preset.yml') $dst -Force

# Copy the CONTENTS of skills/ and commands/, never those directories themselves.
# `Copy-Item <src>\skills <dst>\skills -Recurse` into a directory that already
# exists copies the whole tree INSIDE it, producing <dst>\skills\skills and
# leaving the real skill files at their old version -- an upgrade that reports
# success while shipping nothing. Enumerate the children and copy those.
foreach ($d in @('skills', 'commands')) {
  $srcDir = Join-Path $src $d
  if (-not (Test-Path $srcDir -PathType Container)) { continue }
  $dstDir = Join-Path $dst $d
  New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
  $children = Get-ChildItem -Path $srcDir -Force
  if ($children) {
    Copy-Item -Path $children.FullName -Destination $dstDir -Recurse -Force
  }
}

Write-Host "installed oh-my-dsh preset to $dst"

# Report -- never delete -- a duplicate tree that an older version of this script
# nested. Those files are not what the preset loads, so they are dead weight.
foreach ($d in @('skills', 'commands')) {
  $nested = Join-Path $dst (Join-Path $d $d)
  if (Test-Path $nested -PathType Container) {
    Write-Host "  WARNING duplicate tree from an older installer: $nested"
    Write-Host "          nothing loads it; delete it after you have checked it."
  }
}

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
