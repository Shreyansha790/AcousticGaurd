# Integration keys required from you

Perfect — share these values and I will do all updates + commits for you.

## 1) Firebase (required for multi-device sync)

> ⚠️ Do **not** share Firebase service-account JSON/private keys here. Share only Firebase Web App config fields.
Please send:
- `firebase.apiKey`
- `firebase.authDomain` (optional but recommended)
- `firebase.projectId`
- `firebase.databaseURL` (optional)
- `firebase.storageBucket` (optional)
- `firebase.messagingSenderId` (optional)
- `firebase.appId` (optional)
- `firebase.measurementId` (optional)

## 2) TomTom (required for live traffic ETA)
Please send:
- `tomtomApiKey`

## 3) YAMNet / model hosting (optional enhancement)
You can skip this for now; app uses deterministic fallback mode.

If you want it later, send at least one:
- `yamnet.localUrl`
- OR `yamnet.remoteUrl`

Optional:
- `yamnet.timeoutMs` (default: `12000`)

## 4) Edge node declaration (for readiness panel)
Please send:
- `edgeNodeCount` (number)

---

## Copy-paste format (fill and send)

```js
window.ACOUSTIC_GUARD_CONFIG = {
  edgeNodeCount: 2,

  firebase: {
    apiKey: "",
    authDomain: "",
    projectId: "",
    databaseURL: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
  },

  tomtomApiKey: "",

  yamnet: {
    localUrl: "",
    remoteUrl: "",
    timeoutMs: 12000
  }
};
```

Once you send this, I will:
1. create/update `config.js`,
2. validate wiring,
3. run checks,
4. commit everything.


## Intake status
- ✅ TomTom API key received (stored locally only; never committed).
- ✅ Firebase Web App config received (will be written to local `config.js`, never committed).
- ✅ YAMNet intentionally deferred (low impact for current demo).


## Quick progress mode
If only some keys are available right now, validate in partial mode:

```bash
node scripts/validate_config.js config.js --allow-partial
```

This keeps development unblocked while remaining fields are pending.


For step-by-step collection instructions, see `KEYS_SETUP_GUIDE.md`.
