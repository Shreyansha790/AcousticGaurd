# How to get Firebase Web App config and YAMNet URL

This is the exact way to collect the remaining values safely.

## 1) Firebase Web App config (public client config, not admin key)

### Console method (fastest)
1. Open Firebase Console → your project.
2. Click **Project settings** (gear icon).
3. In **Your apps**, select your **Web app** (create one first if missing).
4. In **SDK setup and configuration**, choose **Config**.
5. Copy these fields:
   - `apiKey`
   - `authDomain`
   - `projectId`
   - `databaseURL` (optional)
   - `storageBucket`
   - `messagingSenderId`
   - `appId`
   - `measurementId` (optional)

### CLI method (optional)
If you use Firebase CLI, run:

```bash
firebase apps:list
firebase apps:sdkconfig WEB <YOUR_FIREBASE_WEB_APP_ID>
```

Then copy the same fields from the printed config.

## 2) YAMNet URL (optional for current milestone)

Use one of these only if you want real model checks now:

- `yamnet.localUrl` (recommended for demos): host model files locally/CDN you control.
- `yamnet.remoteUrl`: use the default remote URL from `config.example.js` if you want quick setup.

Current default in this repo:

```text
https://tfhub.dev/google/tfjs-model/yamnet/tfjs/1/default/1/model.json
```

## 3) What to send me
Paste this block with real values:

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

## Safety
- Do **not** send service-account JSON/private keys.
- Only send the web app config object above.


For a strict step-by-step YAMNet flow, see `YAMNET_SETUP_EXACT_PROCESS.md`.
