"""
AcousticGuard Edge Sensor Bridge.

Simulates a fleet of in-venue acoustic edge nodes (Raspberry Pi / ESP32-class
gateways) and publishes their heartbeats + acoustic detections into Firebase
Realtime Database. The browser dashboard subscribes to the same paths, so
everything the bridge writes shows up live in the operator UI.

Designed to run in three modes:
  1. Local laptop (default) - point at any service-account JSON.
  2. Cloud Run / Cloud Functions container - read service-account from
     GOOGLE_APPLICATION_CREDENTIALS, database URL from FIREBASE_DATABASE_URL.
  3. --dry-run - prints telemetry to stdout, no Firebase writes. Useful for
     CI, smoke testing, and offline judge demos.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass(frozen=True)
class EdgeNode:
    id: str
    name: str
    venue_type: str
    lat: float
    lng: float
    zone: str


EDGE_NODES: List[EdgeNode] = [
    EdgeNode("EDGE_001", "Orion Grand Hotel - Service Gate", "hotel",   12.9714, 77.5948, "Service Gate"),
    EdgeNode("EDGE_002", "Orion Grand Hotel - Banquet Hall", "hotel",   12.9716, 77.5946, "Banquet Hall"),
    EdgeNode("EDGE_003", "Orion Grand Hotel - Lobby",        "hotel",   12.9715, 77.5944, "Lobby"),
    EdgeNode("EDGE_004", "Nexus City Mall - Atrium West",    "mall",    12.9758, 77.6052, "Atrium"),
    EdgeNode("EDGE_005", "Nexus City Mall - Food Court",     "mall",    12.9760, 77.6049, "Food Court"),
    EdgeNode("EDGE_006", "Nexus City Mall - Loading Bay",    "mall",    12.9757, 77.6055, "Loading Bay"),
    EdgeNode("EDGE_007", "Bengaluru Arena - South Stand",    "stadium", 12.9778, 77.5997, "South Stand"),
    EdgeNode("EDGE_008", "Bengaluru Arena - VIP Entry",      "stadium", 12.9781, 77.5994, "VIP Entry"),
    EdgeNode("EDGE_009", "Bengaluru Arena - Concourse A",    "stadium", 12.9779, 77.5999, "Concourse A"),
    EdgeNode("EDGE_010", "Lakeview Resort - Reception",      "resort",  12.9487, 77.5861, "Reception"),
    EdgeNode("EDGE_011", "Lakeview Resort - Pool Deck",      "resort",  12.9488, 77.5860, "Pool Deck"),
    EdgeNode("EDGE_012", "Lakeview Resort - Service Road",   "resort",  12.9485, 77.5863, "Service Road"),
]

DETECTION_LABELS = [
    ("ambulance siren", 0.91, 0.98),
    ("fire alarm",      0.88, 0.96),
    ("smoke detector",  0.84, 0.94),
    ("crowd panic",     0.78, 0.91),
    ("glass break",     0.82, 0.95),
    ("medical distress",0.86, 0.97),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def battery_drift(node_id: str, ts: float) -> int:
    """Cheap deterministic battery curve so dashboards see plausible values."""
    seed = sum(ord(c) for c in node_id)
    return max(8, 100 - int((ts / 60 + seed) % 92))


def signal_rssi(node_id: str, ts: float) -> int:
    seed = sum(ord(c) for c in node_id) * 7
    return -45 - int((ts / 7 + seed) % 38)


class Sink:
    """Abstract write target (Firebase or stdout)."""

    def heartbeat(self, payload: Dict) -> None: ...
    def detection(self, payload: Dict) -> None: ...


class FirebaseSink(Sink):
    def __init__(self, service_account_path: str, database_url: str) -> None:
        import firebase_admin
        from firebase_admin import credentials, db

        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {"databaseURL": database_url})
        self._db = db

    def heartbeat(self, payload: Dict) -> None:
        ref = self._db.reference(f"edge_nodes/{payload['id']}")
        ref.update(payload)

    def detection(self, payload: Dict) -> None:
        ref = self._db.reference("detections").push()
        ref.set(payload)


class DryRunSink(Sink):
    def heartbeat(self, payload: Dict) -> None:
        sys.stdout.write(json.dumps({"kind": "heartbeat", **payload}) + "\n")
        sys.stdout.flush()

    def detection(self, payload: Dict) -> None:
        sys.stdout.write(json.dumps({"kind": "detection", **payload}) + "\n")
        sys.stdout.flush()


def build_heartbeat(node: EdgeNode) -> Dict:
    ts = time.time()
    return {
        "id": node.id,
        "name": node.name,
        "venue_type": node.venue_type,
        "zone": node.zone,
        "lat": node.lat,
        "lng": node.lng,
        "status": "online",
        "source": "edge_emulator",
        "battery_pct": battery_drift(node.id, ts),
        "signal_rssi": signal_rssi(node.id, ts),
        "firmware": "acg-edge/0.4.2",
        "last_ping": now_iso(),
    }


def build_detection(node: EdgeNode) -> Dict:
    label, lo, hi = random.choice(DETECTION_LABELS)
    confidence = round(random.uniform(lo, hi), 3)
    return {
        "intersection_id": node.id,
        "intersection_name": node.name,
        "venue_type": node.venue_type,
        "affected_zone": node.zone,
        "lat": node.lat,
        "lng": node.lng,
        "confidence": confidence,
        "yamnet_label": label,
        "status": "active",
        "source": "edge_emulator",
        "timestamp": now_iso(),
    }


def loop(sink: Sink, interval_sec: float, emit_probability: float) -> None:
    print(f"[edge-bridge] {len(EDGE_NODES)} simulated nodes, interval={interval_sec}s, p(detection)={emit_probability}")
    print("[edge-bridge] Ctrl+C to stop")

    def _shutdown(*_):
        print("\n[edge-bridge] shutting down")
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    while True:
        for node in EDGE_NODES:
            sink.heartbeat(build_heartbeat(node))
            if random.random() < emit_probability:
                payload = build_detection(node)
                sink.detection(payload)
                print(f"[{payload['timestamp']}] {node.id} detect={payload['yamnet_label']} conf={payload['confidence']:.2f}")
            else:
                print(f"[{now_iso()}] {node.id} heartbeat ok")
        time.sleep(interval_sec)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AcousticGuard edge node emulator bridge")
    parser.add_argument(
        "--service-account",
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help="Path to Firebase service account JSON (or GOOGLE_APPLICATION_CREDENTIALS env)",
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("FIREBASE_DATABASE_URL"),
        help="Realtime Database URL (or FIREBASE_DATABASE_URL env)",
    )
    parser.add_argument("--interval-sec", type=float, default=6.0, help="Heartbeat sweep interval")
    parser.add_argument("--emit-probability", type=float, default=0.35, help="Per-node detection probability per sweep")
    parser.add_argument("--dry-run", action="store_true", help="Print telemetry to stdout instead of Firebase")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.dry_run:
        sink: Sink = DryRunSink()
    else:
        if not args.service_account or not args.database_url:
            sys.exit("error: --service-account and --database-url are required (or set env vars). Use --dry-run for offline mode.")
        sink = FirebaseSink(args.service_account, args.database_url)
    loop(sink, args.interval_sec, args.emit_probability)


if __name__ == "__main__":
    main()
