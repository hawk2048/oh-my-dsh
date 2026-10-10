#!/usr/bin/env node
// Platform-neutral entry point for `pnpm test`.
//
// `sh tests/install.test.sh` alone needs a POSIX shell on PATH, which a plain
// Windows install of Git for Windows does not provide -- the documented
// `pnpm test` then dies with "'sh' is not recognized". This runner finds a
// shell that works, runs the Windows guard when a PowerShell exists, and says
// so when a guard is skipped.
//
//   tests/skill-path.test.mjs bundle skill-root guard: the customSkillDirs
//                            expression in cordis.patch.yml must resolve to the
//                            INSTALLED package, not to a path relative to baseUrl
//   tests/install.test.sh    portable (sh) guard for install.sh
//   tests/install.test.ps1   Windows guard for install.ps1, where the nesting
//                            bug lived: `Copy-Item <src>\skills <dst>\skills
//                            -Recurse` into an existing directory copies the
//                            tree INSIDE it, so the real skills stayed stale.
//
// Every child runs with stdio 'inherit' or 'ignore' on purpose: piped stdio is
// blocked in a confined DSH sandbox.

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = dirname(here);
const isWindows = process.platform === 'win32';
let failed = false;

/** Run a command that is expected to work; a non-zero exit fails the suite. */
function run(label, cmd, args, cwd) {
  const result = spawnSync(cmd, args, { stdio: 'inherit', cwd });
  if (result.error) {
    console.log(`  FAIL  ${label}: ${result.error.message}`);
    failed = true;
    return;
  }
  if (result.status !== 0) failed = true;
}

/** True when `cmd -c "exit 0"` works, i.e. the command exists. */
function available(cmd, probeArgs) {
  const result = spawnSync(cmd, probeArgs, { stdio: 'ignore' });
  return !result.error && result.status === 0;
}

const shCandidates = isWindows
  ? [
      'sh',
      'bash',
      `${process.env.ProgramFiles ?? 'C:\\Program Files'}\\Git\\bin\\sh.exe`,
      `${process.env['ProgramFiles(x86)'] ?? 'C:\\Program Files (x86)'}\\Git\\bin\\sh.exe`,
    ]
  : ['sh'];

let ranShellGuard = false;
for (const sh of shCandidates) {
  if (!sh.includes('\\') || existsSync(sh)) {
    if (available(sh, ['-c', 'exit 0'])) {
      // A relative path with the repository as cwd: Windows also resolves `sh`
      // to a WSL/MSYS shell, which cannot open a `D:\...` argument.
      run('install.test.sh', sh, ['tests/install.test.sh'], repoRoot);
      ranShellGuard = true;
      break;
    }
  }
}
if (!ranShellGuard) {
  console.log('  skip  install.test.sh (no sh/bash on this machine)');
}

const psCandidates = isWindows ? ['pwsh', 'powershell'] : ['pwsh'];
let ranWindowsGuard = false;
for (const ps of psCandidates) {
  if (!available(ps, ['-NoProfile', '-Command', 'exit 0'])) continue;
  run('install.test.ps1', ps, [
    '-NoProfile',
    '-ExecutionPolicy',
    'Bypass',
    '-File',
    join(here, 'install.test.ps1'),
  ]);
  ranWindowsGuard = true;
  break;
}
if (!ranWindowsGuard) {
  console.log('  skip  install.test.ps1 (no pwsh/powershell on this machine)');
}

// The bundle skill root is resolved at boot by the host, and a wrong path
// fails silently -- so guard it here, where a plain node run is portable.
run('skill-path.test.mjs', process.execPath, [join(here, 'skill-path.test.mjs')], repoRoot);

process.exit(failed ? 1 : 0);
