# Edge Node Emulator Bridge

This folder is the deployable backend half of AcousticGuard. It simulates a
fleet of acoustic edge nodes (Raspberry Pi / ESP32-class gateways) and streams
telemetry into Firebase Realtime Database — the same paths the browser
dashboard subscribes to.

## What it publishes

- `edge_nodes/{id}` — per-node heartbeat: status, battery, RSSI, firmware,
  last-ping timestamp, lat/lng, venue type, zone.
- `detections/{auto-id}` — acoustic detection events: YAMNet-style label,
  confidence, source venue, affected zone.

## Run modes

### 1. Local laptop (judge demo)

```bash
pip install -r edge_node/requirements.txt

python edge_node/edge_sensor_bridge.py \
  --service-account "C:/path/to/service-account.json" \
  --database-url "https://acousticguard-default-rtdb.firebaseio.com"
```

### 2. Dry run (no Firebase, prints JSON)

Use this for CI, offline demos, or when you don't have a service-account on
the laptop you're presenting on:

```bash
python edge_node/edge_sensor_bridge.py --dry-run
```

### 3. Cloud Run / Cloud Functions

A `Dockerfile` is included. Build and deploy with the gcloud CLI:

```bash
cd edge_node

# Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/acousticguard-edge

# Deploy as a long-running Cloud Run job
gcloud run jobs deploy acousticguard-edge \
  --image gcr.io/$PROJECT_ID/acousticguard-edge \
  --set-env-vars FIREBASE_DATABASE_URL=https://acousticguard-default-rtdb.firebaseio.com \
  --service-account=acousticguard-edge@$PROJECT_ID.iam.gserviceaccount.com \
  --region=asia-south1
```

The script auto-discovers `GOOGLE_APPLICATION_CREDENTIALS` and
`FIREBASE_DATABASE_URL` from the environment, so no flags are needed in a
container.

## Tuning

```bash
python edge_node/edge_sensor_bridge.py \
  --service-account "..." --database-url "..." \
  --interval-sec 6 \
  --emit-probability 0.35
```

- `--interval-sec` — how often each node heartbeats (default 6s).
- `--emit-probability` — chance of emitting a siren/medical event per node per
  sweep (default 0.35, i.e. ~4 events / sweep across 12 nodes).

## Why this matters for the judges

The browser dashboard alone could be dismissed as "all simulated in JS." This
bridge is the proof that:

1. The data model already supports non-browser ingestion.
2. The deployment story is real — Dockerfile, env-var configuration, Cloud
   Run job target.
3. Replacing the emulator with real Raspberry Pi devices is a ~one-day swap:
   the same JSON shape, the same Firebase paths.

## Phase 2 production swap

Replace `build_detection()` with a microphone capture loop calling YAMNet
locally on the Pi (TF-Lite) and writing the same payload shape. Everything
downstream — dashboard, conflict arbitration, hospital routing — keeps
working without changes.
