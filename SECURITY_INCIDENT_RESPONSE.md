# Security incident response (Firebase service account key exposed)

A **Firebase service account private key** was shared in chat. Treat it as compromised.

## Immediate actions (do now)
1. **Revoke/disable the exposed service account key** in Google Cloud IAM.
2. **Create a new key only if absolutely required** (prefer Workload Identity where possible).
3. **Rotate any dependent credentials** and redeploy backend services using new auth.
4. **Audit logs** for suspicious usage on this service account.

## Important clarification
- The JSON shared is a **server/admin credential**.
- It must **never** be embedded in `index.html`/frontend `config.js`.
- For frontend Firebase usage, we only need the public web config fields (`apiKey`, `authDomain`, `projectId`, etc.).

## What to send to continue frontend setup safely
Send only this public web config (non-secret by design):

```js
window.ACOUSTIC_GUARD_CONFIG = {
  edgeNodeCount: 2,
  firebase: {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: ""
  },
  tomtomApiKey: "",
  yamnet: {
    localUrl: "",
    remoteUrl: "",
    timeoutMs: 12000
  }
};
```

## Repository hardening applied
- Added `.gitignore` entries for `config.js`, `.env*`, and service-account JSON patterns.
