#!/usr/bin/env node
const url = process.env.YAMNET_REMOTE_URL || process.argv[2];
const timeoutMs = Number(process.env.YAMNET_TIMEOUT_MS || 12000);

if (!url) {
  console.error('Usage: YAMNET_REMOTE_URL=<model.json url> node scripts/check_yamnet_url.js');
  process.exit(1);
}

const controller = new AbortController();
const t = setTimeout(() => controller.abort(), timeoutMs);

fetch(url, { method: 'HEAD', signal: controller.signal, cache: 'no-store' })
  .then((res) => {
    clearTimeout(t);
    if (!res.ok) {
      console.error(`YAMNet URL not reachable: HTTP ${res.status}`);
      process.exit(2);
    }
    console.log('YAMNet URL reachable:', url);
  })
  .catch((err) => {
    clearTimeout(t);
    console.error('YAMNet check failed:', err.message);
    process.exit(3);
  });
