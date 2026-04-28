# Suggestion Response Matrix (implemented)

This file maps reviewer suggestions to concrete implementation in the current prototype.

## 1) No backend / edge hardware
- **Status:** Addressed as transparent readiness + adapter contract.
- **What changed:** Added **Infra Readiness Checks** panel and `edgeNodeCount` support in config so judges can see whether real edge deployment exists.
- **Production next step:** connect a real heartbeat endpoint from edge devices and replace declaration-based status with live status.

## 2) Firebase config missing / offline fallback only
- **Status:** Addressed.
- **What changed:** Added config-based sync mode switch (`firebase` vs `local`) and explicit readiness display. If cloud adapter is unavailable, app still persists safely via localStorage.

## 3) TomTom key not bundled
- **Status:** Addressed.
- **What changed:** Added TomTom live ETA adapter path. If API call fails or key is absent, route generation automatically falls back to deterministic synthetic ETA.

## 4) YAMNet load reliability
- **Status:** Addressed.
- **What changed:** Added AI adapter mode (`yamnet` vs `simulated`) with timeout-based health check against model URL and deterministic fallback trigger if unavailable.

## 5) Export PDF still stubbed
- **Status:** Fixed.
- **What changed:** Implemented working **Export PDF Report** via generated print report window (browser Save as PDF).

## Config contract for demos
Load this before app script:

```html
<script src="config.js"></script>
```

Use this template (see `config.example.js`):

```js
window.ACOUSTIC_GUARD_CONFIG = {
  edgeNodeCount: 2,
  firebase: { apiKey: '***', projectId: '***' },
  tomtomApiKey: '***',
  yamnet: { localUrl: '', remoteUrl: 'https://.../model.json', timeoutMs: 12000 }
};
```

Without this config, the app remains runnable in deterministic fallback mode.
