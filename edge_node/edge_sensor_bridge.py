"""
AcousticGuard Edge Sensor Bridge (demo emulator)

Purpose:
- Simulate deployed edge nodes (Raspberry Pi / microcontroller gateway behavior)
- Publish heartbeat + siren events into Firebase Realtime Database
- Give judges a credible "Phase 2 edge deployment path" beyond browser-only logic
"""

from __future__ import annotations

import argparse
import random
import time
from datetime import datetime, timezone
from typing import Dict, List

import firebase_admin
from firebase_admin import credentials, db


EDGE_NODES: List[Dict[str, object]] = [
    {"id": "EDGE_001", "name": "Hotel Service Gate", "lat": 12.9714, "lng": 77.5948},
    {"id": "EDGE_002", "name": "Mall Atrium West", "lat": 12.9758, "lng": 77.6052},
    {"id": "EDGE_003", "name": "Arena South Stand", "lat": 12.9778, "lng": 77.5997},
    {"id": "EDGE_004", "name": "Resort Reception", "lat": 12.9487, "lng": 77.5861},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_firebase(service_account_path: str, database_url: str) -> None:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})


def emit_heartbeat(node: Dict[str, object]) -> None:
    ref = db.reference(f"edge_nodes/{node['id']}")
    ref.update(
        {
            "name": node["name"],
            "lat": node["lat"],
            "lng": node["lng"],
            "status": "online",
            "source": "edge_emulator",
            "last_ping": now_iso(),
        }
    )


def emit_detection(node: Dict[str, object], confidence: float) -> None:
    det_ref = db.reference("detections").push()
    det_ref.set(
        {
            "intersection_id": node["id"],
            "intersection_name": node["name"],
            "lat": node["lat"],
            "lng": node["lng"],
            "confidence": round(confidence, 2),
            "status": "active",
            "source": "edge_emulator",
            "timestamp": now_iso(),
        }
    )


def loop(interval_sec: float, emit_probability: float) -> None:
    print("Edge bridge running. Ctrl+C to stop.")
    while True:
        for node in EDGE_NODES:
            emit_heartbeat(node)

            if random.random() < emit_probability:
                conf = random.uniform(0.85, 0.98)
                emit_detection(node, conf)
                print(f"[{now_iso()}] detection emitted: {node['id']} @ {conf:.2f}")
            else:
                print(f"[{now_iso()}] heartbeat: {node['id']}")

        time.sleep(interval_sec)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AcousticGuard edge node emulator bridge")
    parser.add_argument(
        "--service-account",
        required=True,
        help="Path to Firebase service account JSON",
    )
    parser.add_argument(
        "--database-url",
        required=True,
        help="Realtime Database URL (e.g. https://your-project-default-rtdb.firebaseio.com)",
    )
    parser.add_argument(
        "--interval-sec",
        type=float,
        default=6.0,
        help="Heartbeat interval for each sweep",
    )
    parser.add_argument(
        "--emit-probability",
        type=float,
        default=0.35,
        help="Probability of generating a siren event per node each interval (0..1)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    init_firebase(args.service_account, args.database_url)
    loop(interval_sec=args.interval_sec, emit_probability=args.emit_probability)


if __name__ == "__main__":
    main()
