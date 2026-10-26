#!/usr/bin/env node
// Contract guard for the shipped agent preset's persona row.
//
// DSH's prompt assembler interpolates `{{name}}` inside a section's text and
// throws on any name the assembling layer did not register — only `provider`
// and `model` today. The persona row lands in the `deployment:persona-prefix`
// section, so a persona that references anything else (the removed `cwd`
// variable being the one that bit us) fails assembly for every turn of that
// preset, with:
//
//   unknown prompt variable "{{cwd}}" in section "deployment:persona-prefix";
//   registered variables: provider, model
//
// The row's schema also requires `prefix:`. The older `text:` key is dropped by
// the schema, and the then-missing required `prefix` fails the mount instead.
//
// Zero dependencies on purpose: this repository ships pure JS/Markdown and
// pulls in no YAML parser, so the file is checked textually. Every assertion is
// reported rather than aborting on the first failure.

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const presetPath = join(repoRoot, 'agent.cordis.yml');
const text = readFileSync(presetPath, 'utf8');
const lines = text.split(/\r?\n/);

/** Prompt variables the assembling layer registers; anything else throws. */
const REGISTERED_VARIABLES = new Set(['provider', 'model']);

let failed = 0;
function check(label, ok, detail) {
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}`);
  if (!ok) {
    failed++;
    if (detail) console.log(`        ${detail}`);
  }
}

// 1. The persona row itself is present and is the row this contract is about.
const personaRow = lines.findIndex((line) => /^\s*-\s*id:\s*persona\s*$/.test(line));
check('persona row is present', personaRow !== -1);
check(
  'persona row mounts @deepseek-ai/dsh-persona',
  personaRow !== -1 && /^\s*name:\s*'@deepseek-ai\/dsh-persona'\s*$/.test(lines[personaRow + 1] ?? '')
);

// 2. It configures `prefix:` — the key the row's schema requires today.
check(
  'persona row uses the prefix: key',
  /^ {4}prefix:\s*[>|]/m.test(text),
  'the row\'s schema requires `prefix`; a preset without it fails to mount'
);
check(
  'persona row carries no legacy text: key',
  !/^ {4}text:\s*[>|]/m.test(text),
  '`text:` is dropped by the row\'s schema, leaving the required `prefix` missing'
);

// 3. Only registered variables may be referenced. Comments are not interpolated,
//    so they are skipped — a comment may legitimately name the removed variable.
const offenders = [];
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (/^\s*#/.test(line)) continue;
  for (const match of line.matchAll(/\{\{([^{}]*)\}\}/g)) {
    const name = match[1];
    if (!REGISTERED_VARIABLES.has(name)) offenders.push({ line: i + 1, name, text: line.trim() });
  }
}
check(
  'every prompt variable is registered',
  offenders.length === 0,
  offenders
    .map(
      (o) =>
        `line ${o.line}: {{${o.name}}}${
          o.name === 'cwd'
            ? ' — the working directory is injected as its own runtime-context section, not a variable'
            : ''
        }`
    )
    .join('\n        ')
);

console.log(`\npreset-contract: ${failed === 0 ? 'ok' : `${failed} failed`} (${presetPath})`);
process.exit(failed === 0 ? 0 : 1);
