# YAMNet setup — exact process

Use this exact flow to finish YAMNet for AcousticGuard.

> Skip for now if you want faster delivery; the app already works with deterministic fallback.

## Option A (fastest, recommended now): remote URL

1. Use this URL:

```text
https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json
```

2. Put it in your local config as `yamnet.remoteUrl`:

```js
yamnet: {
  localUrl: "",
  remoteUrl: "https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json",
  timeoutMs: 12000
}
```

3. Pre-check reachability:

```bash
YAMNET_REMOTE_URL="https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json" \
node scripts/check_yamnet_url.js
```

4. Validate config in partial-safe mode:

```bash
node scripts/validate_config.js config.js --allow-partial
```

5. Run app and click **Run AI Check** in dashboard.

---

## Option B (best demo reliability): local-hosted model URL

Use a stable URL you control (CDN/static host) that serves `model.json` and its referenced shard files.

Then set:

```js
yamnet: {
  localUrl: "https://<your-domain>/models/yamnet/model.json",
  remoteUrl: "",
  timeoutMs: 12000
}
```

Pre-check with the same command:

```bash
YAMNET_REMOTE_URL="https://<your-domain>/models/yamnet/model.json" node scripts/check_yamnet_url.js
```

---

## What to send me now
Send only this YAMNet block and I’ll wire the rest:

```js
yamnet: {
  localUrl: "",
  remoteUrl: "https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json",
  timeoutMs: 12000
}
```
