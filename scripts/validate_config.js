#!/usr/bin/env node
const fs = require('fs');
const vm = require('vm');

const args = process.argv.slice(2);
const allowPartial = args.includes('--allow-partial');
const file = args.find((a) => !a.startsWith('--')) || 'config.js';

if (!fs.existsSync(file)) {
  console.error(`Missing ${file}`);
  process.exit(1);
}

const src = fs.readFileSync(file, 'utf8');
const sandbox = { window: {} };
vm.createContext(sandbox);

try {
  vm.runInContext(src, sandbox, { timeout: 1000 });
} catch (err) {
  console.error('Config parse error:', err.message);
  process.exit(1);
}

const cfg = sandbox.window.ACOUSTIC_GUARD_CONFIG;
if (!cfg) {
  console.error('window.ACOUSTIC_GUARD_CONFIG is missing');
  process.exit(1);
}

const required = [
  { ok: !!cfg.tomtomApiKey, key: 'tomtomApiKey' },
  { ok: !!(cfg.firebase && cfg.firebase.apiKey && cfg.firebase.projectId), key: 'firebase.apiKey + firebase.projectId' },
  { ok: Number.isFinite(Number(cfg.edgeNodeCount)), key: 'edgeNodeCount (number)' }
];

const missing = required.filter((r) => !r.ok).map((r) => r.key);

const optionalChecks = [];
if (!(cfg.yamnet && (cfg.yamnet.localUrl || cfg.yamnet.remoteUrl))) {
  optionalChecks.push('yamnet.localUrl or yamnet.remoteUrl (optional)');
}
if (missing.length) {
  if (allowPartial) {
    console.warn('Partial config mode: missing optional-for-now fields:');
    missing.forEach((m) => console.warn(`- ${m}`));
    process.exit(0);
  }
  console.error('Missing/incomplete fields:');
  missing.forEach((m) => console.error(`- ${m}`));
  process.exit(2);
}

if (optionalChecks.length) {
  console.warn('Optional fields not set:');
  optionalChecks.forEach((m) => console.warn(`- ${m}`));
}

console.log('Config validation passed.');
