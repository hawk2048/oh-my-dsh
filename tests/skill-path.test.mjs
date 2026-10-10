#!/usr/bin/env node
// Regression guard for the skill root declared in cordis.patch.yml.
//
// That row adds this package's skills/ to the host skill-filesystem through
// customSkillDirs. It used to locate them relative to `baseUrl`:
//
//   !!js "process.getBuiltinModule('node:url').fileURLToPath(new URL('skills/', baseUrl))"
//
// DeepSeek Harness anchors `baseUrl` at the PROFILE directory, not at the
// package directory -- see the comment above prepareProfile() in the dsh
// bundle: "the Loader needs a real include root to anchor baseUrl at the
// profile directory". So the expression produced <profile>/skills, a path
// that does not exist. A missing skill root is not an error: the scanner
// silently finds zero skills, the catalog shows no omd-* entries, and the
// skill tool answers "unknown or no longer available". Nothing complains,
// which is why this shipped unnoticed.
//
// The fix resolves the root FROM THE PACKAGE instead: createRequire(baseUrl)
// uses the profile only as a lookup anchor -- an input to node's resolver,
// never a directory we assume anything lives in -- and require.resolve()
// answers where the package actually is, under a plain or a pnpm
// node_modules layout alike. This mirrors what DSH itself does for the same
// field in its own preset patch.
//
// Guards:
//   [1] source: the row still overrides by id, still sets disabled: false,
//       still uses customSkillDirs (additive over the default roots)
//   [2] behaviour: evaluating the real expression against a fake profile
//       install yields a directory holding exactly the shipped skills, and the
//       package is found in the profile's node_modules rather than a decoy one
//       level up
//   [3] regression: the skills are located through the module resolver, so the
//       old baseUrl-relative spelling cannot silently come back
//   [4] layout: a pnpm node_modules (public entry is a symlink into .pnpm)
//       still resolves to a directory that holds the skills
//   [5] exports: the bare specifier is resolvable while <name>/package.json is
//       not, so the fix must keep using the former
//
// Assertions are counted, never thrown: a guard that stops at the first
// failure hides the rest of the damage it is meant to describe.

import {
  cpSync, existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, rmSync, symlinkSync, writeFileSync,
} from 'node:fs'
import { dirname, join, resolve as resolvePath } from 'node:path'
import { tmpdir } from 'node:os'
import { fileURLToPath, pathToFileURL } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const repoRoot = dirname(here)
const patch = readFileSync(join(repoRoot, 'cordis.patch.yml'), 'utf8')
const pkg = JSON.parse(readFileSync(join(repoRoot, 'package.json'), 'utf8'))
const PKG_NAME = pkg.name

let fails = 0
const pass = (msg) => console.log('  ok   ' + msg)
const fail = (msg) => { console.log('  FAIL ' + msg); fails += 1 }
const expect = (cond, msg) => (cond ? pass(msg) : fail(msg))

/** Slice of the patch file belonging to one entry id. */
function rowOf(text, id) {
  const start = text.indexOf('- id: ' + id)
  if (start < 0) return undefined
  const rest = text.slice(start)
  const next = rest.slice(1).search(/^\- id: /m)
  return next < 0 ? rest : rest.slice(0, next + 1)
}

/** The raw source behind the first `!!js` scalar of a block. */
function jsExprOf(block) {
  const m = block.match(/-\s*!!js\s+(.*)/)
  if (!m) return undefined
  let expr = m[1].trim()
  const q = expr[0]
  if ((q === '"' || q === "'") && expr.endsWith(q)) expr = expr.slice(1, -1)
  return expr
}

/**
 * The evaluator DeepSeek Harness applies to `!!js` scalars, copied from
 * cordis-plugin-loader/src/config/utils.ts. A new-Function body is sloppy
 * mode even when this file is a module, so `with` is legal exactly as there.
 */
const evaluate = new Function('ctx', 'expr', 'with (ctx) { return eval(expr) }')

const row = rowOf(patch, 'skill-filesystem')
const expr = row ? jsExprOf(row) : undefined

console.log('[1] source: the bundle row keeps its shape')
if (!row) {
  fail('cordis.patch.yml has no "- id: skill-filesystem" row')
} else {
  expect(/disabled:\s*false/.test(row),
    'the row sets disabled: false (the Web app ships the host row disabled)')
  expect(/customSkillDirs:/.test(row), 'the row supplies customSkillDirs')
  expect(!/^name:/m.test(row),
    'the row overrides by id and does not rename the plugin (one filesystem provider)')
  expect(!/\nskillDirs:/.test(row),
    'the row does not replace the default roots (customSkillDirs is additive)')
  expect(typeof expr === 'string' && expr.length > 0, 'a !!js expression was found')
}

console.log('')
console.log('[2] behaviour: the expression finds the shipped skills from a profile install')
if (typeof expr === 'string') {
  const opens = (expr.match(/[([{]/g) || []).length
  const closes = (expr.match(/[\])}]/g) || []).length
  expect(opens === closes,
    'the expression is complete on one line (' + opens + ' open / ' + closes + ' close)')

  const sandbox = join(tmpdir(), 'omd-skill-path-' + process.pid)
  const profile = join(sandbox, 'profiles', 'web')
  const installed = join(profile, 'node_modules', ...PKG_NAME.split('/'))
  const decoy = join(sandbox, 'profiles', 'node_modules', ...PKG_NAME.split('/'))
  try {
    rmSync(sandbox, { recursive: true, force: true })
    mkdirSync(dirname(installed), { recursive: true })
    cpSync(repoRoot, installed, { recursive: true, filter: (src) => !src.includes('/.git') })

    // A same-named package one level up. A resolver allowed to walk upward
    // would pick this one, so it is planted empty to make the choice visible.
    mkdirSync(join(decoy, 'skills', 'decoy-skill'), { recursive: true })
    writeFileSync(join(decoy, 'package.json'), JSON.stringify({
      name: PKG_NAME, version: '0.0.0-decoy', type: 'module', main: 'index.js',
      exports: { '.': './index.js' },
    }))
    writeFileSync(join(decoy, 'index.js'), 'export {}')

    // Exactly what dsh sets: the profile directory as a file URL, trailing slash.
    const baseUrl = new URL('.', pathToFileURL(join(profile, 'cordis.include.yml'))).href
    const ctx = { baseUrl, get: () => undefined }

    let value
    try {
      value = evaluate(ctx, expr)
      expect(typeof value === 'string', 'the expression evaluated to a string (got ' + typeof value + ')')
    } catch (error) {
      fail('the expression threw: ' + (error && error.message))
    }

    if (typeof value === 'string') {
      console.log('       resolved root: ' + value.replace(sandbox, '<sandbox>'))
      expect(existsSync(value), 'the resolved root exists on disk')
      const real = (x) => { try { return realpathSync(x) } catch { return resolvePath(x) } }
      expect(!real(value).startsWith(real(join(profile, 'skills')) + '/'),
        'the root is not the profile directory (that path does not exist in a real install)')
      expect(real(value).startsWith(real(installed) + '/'),
        'the root is inside the installed package, not the decoy one level up')

      const namesUnder = (dir) => (existsSync(dir)
        ? readdirSync(dir, { withFileTypes: true })
            .filter((e) => e.isDirectory() && existsSync(join(dir, e.name, 'SKILL.md')))
            .map((e) => e.name).sort()
        : [])
      const shipped = namesUnder(join(repoRoot, 'skills'))
      expect(shipped.length > 0, 'the repository ships at least one skill (found ' + shipped.length + ')')
      const found = namesUnder(value)
      expect(found.length === shipped.length && found.every((n, i) => n === shipped[i]),
        'every shipped skill is discoverable (' + found.length + ' found / ' + shipped.length + ' shipped)')
      expect(!found.includes('decoy-skill'), 'the decoy package contributes no skills')
    }
  } finally {
    rmSync(sandbox, { recursive: true, force: true })
  }
}

console.log('')
console.log('[3] regression: skills must not be located relative to baseUrl')
// The rule is about behaviour, not spelling: the root must not be a path that
// only exists because the profile happened to be named a certain way. Guard 1
// is that the expression asks the module resolver where the package is.
{
  const usesResolver = /createRequire\([^)]*\)\s*\.\s*resolve/.test(expr || '')
  expect(usesResolver, 'the expression asks node\'s resolver where the package is (createRequire(...).resolve(...))')
  // And guard against the old spelling returning verbatim.
  expect(!/new URL\(\s*'skills\/'\s*,\s*baseUrl\s*\)/.test(expr || ''),
    'the expression is not the old new URL(\'skills/\', baseUrl) form')
}

console.log('')
console.log('[4] layout: a pnpm node_modules resolves through the symlink too')
// dsh installs bundles with pnpm, where the public node_modules entry is a
// symlink into node_modules/.pnpm/<name>@<ver>/node_modules/<name>. The root
// must still land on a directory that actually holds the skills.
{
  const sandbox = join(tmpdir(), 'omd-skill-path-pnpm-' + process.pid)
  const storePkg = join(sandbox, 'node_modules', '.pnpm',
    PKG_NAME.replace('/', '+') + '@9.9.9', 'node_modules', ...PKG_NAME.split('/'))
  const publicPkg = join(sandbox, 'node_modules', ...PKG_NAME.split('/'))
  try {
    rmSync(sandbox, { recursive: true, force: true })
    mkdirSync(join(storePkg, 'skills', 'omd-plan'), { recursive: true })
    writeFileSync(join(storePkg, 'skills', 'omd-plan', 'SKILL.md'), '# omd-plan\n')
    writeFileSync(join(storePkg, 'package.json'), JSON.stringify({
      name: PKG_NAME, version: '9.9.9', type: 'module', main: 'index.js',
      exports: { '.': './index.js' },
    }))
    writeFileSync(join(storePkg, 'index.js'), 'export {}')
    mkdirSync(dirname(publicPkg), { recursive: true })
    symlinkSync(storePkg, publicPkg, 'dir')

    const baseUrl = new URL('.', pathToFileURL(join(sandbox, 'cordis.include.yml'))).href
    let value
    try {
      value = evaluate({ baseUrl, get: () => undefined }, expr || '')
      expect(existsSync(value), 'the pnpm store path resolves and exists')
      const n = readdirSync(value).filter((d) => existsSync(join(value, d, 'SKILL.md'))).length
      expect(n === 1, 'the resolved root holds the skills of the installed package (' + n + '/1)')
    } catch (error) {
      fail('the expression threw under a pnpm layout: ' + (error && error.message))
    }
  } finally {
    rmSync(sandbox, { recursive: true, force: true })
  }
}

console.log('')
console.log('[5] exports: the bare specifier is the resolvable one')
{
  const keys = Object.keys(pkg.exports || {})
  const exposesPkgJson = keys.includes('./package.json')
  if (exposesPkgJson) {
    pass('package.json exports ./package.json, so the subpath is resolvable')
  } else {
    expect(!expr || !/resolve\(\s*['\"][^'\"]*\/package\.json['\"]\s*\)/.test(expr),
      'the expression does not resolve <name>/package.json (not exported -> ERR_PACKAGE_PATH_NOT_EXPORTED)')
  }
  expect(!!expr && new RegExp('resolve\\(\s*[\"\']' + PKG_NAME.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[\"\']\s*\\)').test(expr),
    'the expression resolves the bare package specifier, which the "." export provides')
}

console.log('')
if (fails) {
  console.log('skill-path guard FAILED (' + fails + ')')
  process.exit(1)
}
console.log('skill-path guard passed')
