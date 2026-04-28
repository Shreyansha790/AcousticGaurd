# Edge Node Emulator Bridge

This folder adds a backend/edge deployment path for AcousticGuard.

It simulates field edge devices (Raspberry Pi / MCU gateway equivalents) that publish:
- node heartbeats (`edge_nodes/*`)
- siren detections (`detections/*`)

into Firebase Realtime Database.

## Quick Start

1. Install dependencies:

```bash
pip install -r edge_node/requirements.txt
```

2. Run the bridge:

```bash
python edge_node/edge_sensor_bridge.py \
  --service-account "C:/path/to/service-account.json" \
  --database-url "https://your-project-default-rtdb.firebaseio.com"
```

Optional tuning:

```bash
python edge_node/edge_sensor_bridge.py \
  --service-account "C:/path/to/service-account.json" \
  --database-url "https://your-project-default-rtdb.firebaseio.com" \
  --interval-sec 6 \
  --emit-probability 0.35
```

## Why This Exists

Judges asked for a credible path beyond browser-only simulation.
This bridge demonstrates how deployed edge sensors can stream live telemetry into the same operational dashboard architecture.
