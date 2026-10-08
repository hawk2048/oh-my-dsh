# Regression guard for the PowerShell preset installer (install.ps1).
#
# Mirrors tests/install.test.sh on the platform where the nesting bug lived:
# `Copy-Item <src>\skills <dst>\skills -Recurse` into an EXISTING directory
# copies the whole tree inside it, so a re-run produced <preset>\skills\skills
# and left the real skill files on the old version while reporting success.
#
# Run from the repository root:  pwsh -File tests/install.test.ps1

$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('omd-install-test-' + [guid]::NewGuid().ToString('N'))
$homeDir = Join-Path $tmp 'home'
$preset = Join-Path $homeDir '.agent-presets/oh-my-dsh'
$fails = 0

function Pass($m) { Write-Host "  ok   $m" }
function Fail($m) { Write-Host "  FAIL $m"; $script:fails++ }
function Expect-File($p, $m) { if (Test-Path $p -PathType Leaf) { Pass $m } else { Fail $m } }
function Expect-NoDir($p, $m) { if (Test-Path $p -PathType Container) { Fail $m } else { Pass $m } }
function Expect-Same($a, $b, $m) {
  if ((Get-FileHash $a).Hash -eq (Get-FileHash $b).Hash) { Pass $m } else { Fail $m }
}
function Expect-Contains($needle, $path, $m) {
  if (Select-String -Path $path -SimpleMatch -Pattern $needle -Quiet) { Pass $m } else { Fail $m }
}
function Invoke-Installer($log) {
  try { & (Join-Path $repo 'install.ps1') *> $log; return $true }
  catch { Add-Content -Path $log -Value $_; return $false }
}

foreach ($sub in @('skills/my-local-skill', 'skills')) {
  New-Item -ItemType Directory -Force -Path (Join-Path $preset $sub) | Out-Null
}
Set-Content -Path (Join-Path $preset 'skills/my-local-skill/SKILL.md') -Value 'mine'
$localSkill = Join-Path $preset 'skills/my-local-skill/SKILL.md'
Copy-Item (Join-Path $repo 'agent.cordis.yml') (Join-Path $preset 'agent.cordis.yml') -Force
Add-Content -Path (Join-Path $preset 'agent.cordis.yml') -Value '# MY-LOCAL-CONFIG'

$env:DSH_HOME = $homeDir

try {
  Write-Host '[1] behaviour: install over a preset that already has local content'
  if (Invoke-Installer "$tmp/run1.log") { Pass 'install.ps1 exits 0' } else { Fail 'install.ps1 failed' }
  Expect-File $localSkill 'local-only skill preserved'
  Expect-File (Join-Path $preset 'skills/omd-pyramid/SKILL.md') 'shipped skill installed'
  Expect-Same (Join-Path $repo 'skills/omd-pyramid/SKILL.md') (Join-Path $preset 'skills/omd-pyramid/SKILL.md') `
    'installed skill content is the shipped content'
  Expect-Contains 'my-local-skill' "$tmp/run1.log" 'run reports the preserved file'
  $backup = Get-ChildItem (Join-Path $preset 'agent.cordis.yml.bak-*')
  if ($backup) {
    Pass 'local config was backed up before being overwritten'
    Expect-Contains 'MY-LOCAL-CONFIG' $backup[0].FullName 'backup keeps the local content'
  }
  else { Fail 'no backup of the locally modified agent.cordis.yml' }
  Expect-Same (Join-Path $repo 'agent.cordis.yml') (Join-Path $preset 'agent.cordis.yml') `
    'shipped agent.cordis.yml is the installed one'

  Write-Host '[2] behaviour: re-running is idempotent and does not nest the trees'
  if (Invoke-Installer "$tmp/run2.log") { Pass 'second run exits 0' } else { Fail 'second run failed' }
  if ((Get-ChildItem (Join-Path $preset 'agent.cordis.yml.bak-*')).Count -eq 1) {
    Pass 'still exactly 1 backup'
  }
  else { Fail 'backup count changed on re-run' }
  Expect-File $localSkill 'local-only skill still preserved'
  Expect-NoDir (Join-Path $preset 'skills/skills') 're-run does not nest skills/skills'
  Expect-NoDir (Join-Path $preset 'commands/commands') 're-run does not nest commands/commands'

  Write-Host '[3] behaviour: a re-run refreshes a shipped file in place'
  Add-Content -Path (Join-Path $preset 'skills/omd-plan/SKILL.md') -Value '# LOCAL-EDIT'
  Add-Content -Path (Join-Path $preset 'commands/omd-commands.mjs') -Value '// LOCAL-EDIT'
  if (Invoke-Installer "$tmp/run3.log") { Pass 'third run exits 0' } else { Fail 'third run failed' }
  Expect-Same (Join-Path $repo 'skills/omd-plan/SKILL.md') (Join-Path $preset 'skills/omd-plan/SKILL.md') `
    'shipped skill replaces the drifted local copy'
  Expect-Same (Join-Path $repo 'commands/omd-commands.mjs') (Join-Path $preset 'commands/omd-commands.mjs') `
    'shipped command module replaces the drifted local copy'
  $skillBackup = Get-ChildItem (Join-Path $preset 'skills/omd-plan/SKILL.md.bak-*')
  if ($skillBackup) {
    Pass 'drifted shipped skill was backed up'
    Expect-Contains 'LOCAL-EDIT' $skillBackup[0].FullName 'skill backup keeps the local content'
  }
  else { Fail 'no backup of the drifted shipped skill' }
}
finally {
  Remove-Item Env:DSH_HOME -ErrorAction SilentlyContinue
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

Write-Host ''
if ($fails -eq 0) {
  Write-Host '=== install tests passed ==='
  exit 0
}
Write-Host "=== $fails install test(s) FAILED ==="
exit 1
