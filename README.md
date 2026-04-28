# AcousticGuard.ai

AcousticGuard.ai is a hospitality crisis-response command dashboard for hotels, malls, stadiums, resorts, and large venues. It detects emergency signals, coordinates venue staff, routes responders with live traffic context, and generates a crisis report for rapid emergency response.

The prototype is built for the Google Solution Challenge rapid crisis response theme. It connects distressed guests, venue staff, on-site security, medical teams, hospitals, and ambulance responders in one operational dashboard.

## Current Build Status (April 28, 2026)

This repository is currently a **working hackathon demo build** with:

- Hospitality-first command workflow (hotel/mall/stadium/resort)
- Venue crisis scenarios (medical, fire, security, evacuation)
- Medical crisis routing anchored from **venue origin to nearest/best hospital**
- TomTom-backed road geometry rendering for live ambulance route visualization
- Multi-ambulance conflict arbitration with deterministic replay mode
- Resilient live-mic inference pipeline:
  - Primary: TensorFlow.js + YAMNet
  - Fallback: in-browser heuristic classifier when model/CDN fails
- Firebase Realtime Database integration plus local fallback when Firebase/network is unavailable
- Edge-node emulator bridge (`edge_node/`) to demonstrate non-browser telemetry ingestion path

## How It Fits The Challenge

Hospitality venues face fast-moving incidents where information is often fragmented between guests, front desk, security, floor managers, and emergency services. AcousticGuard.ai addresses this by:

- Detecting or triggering crisis events in a live command view
- Synchronizing staff tasks across front desk, security, medical, and floor teams
- Showing guest-safe zones, affected zones, and responder entry gates
- Routing ambulances/hospitals with TomTom traffic-aware ETA logic
- Preserving a crisis timeline and post-incident report for accountability

## Core Features

- `Venue Crisis Mode`:
  - Hotel, mall, stadium, and resort profiles
  - Medical, fire, security, and evacuation scenario presets
  - Affected zone, safe zone, and responder gate tracking

- `Hospitality Command Panel`:
  - Guest safety progress
  - Staff task dispatch board
  - Responder bridge with TomTom/fallback traffic source
  - Crisis timeline for judge-visible explainability

- `Real AI Audio Detection`:
  - Live mic capture in browser
  - TensorFlow.js + YAMNet-based sound classification
  - YAMNet prefetch + cached label fallback for weak demo networks
  - Auto-fallback classifier to prevent pipeline breakage if YAMNet cannot load
  - Siren/noise confidence scoring with decision trace

- `Emergency Corridor Activation`:
  - Automatic route activation on high-confidence siren or medical-crisis events
  - Medical crisis path starts from selected hospitality venue and resolves to nearest hospital
  - Exact road-path geometry from TomTom Routing API for map visualization
  - Animated corridor rendering on Leaflet map
  - Signal node sequencing visualization (kept minimal in venue-medical flow to avoid map clutter)

- `Multi-Ambulance Arbitration`:
  - Conflict-first responder demo flow
  - Priority scoring based on urgency, ETA window, overlap risk, and traffic density
  - Winner and rerouted path logic
  - Deterministic replay mode for judging/demo consistency

- `Live Traffic Integration (TomTom)`:
  - Real-time traffic flow sampling from TomTom Flow Segment API
  - Traffic multipliers applied to ETA and conflict arbitration
  - Dynamic congestion visualization in route rendering and node table
  - Safe synthetic fallback when live traffic API is unavailable

- `Hospitality Crisis Analytics & Report`:
  - Detection volume charts
  - Confidence distribution
  - Response time saved
  - Staff tasks, guest-safe-zone progress, responder gate, and crisis narrative
  - Export-to-PDF action (printable report view)

## Tech Stack

- `Frontend`: HTML, CSS, JavaScript (single-page architecture)
- `AI`: TensorFlow.js, YAMNet
- `Map`: Leaflet.js + dark basemap
- `Traffic`: TomTom Flow Segment API with fallback simulation
- `Charts`: Chart.js
- `Backend/Data`: Firebase Realtime Database with local in-memory fallback

## Project Structure

- `index.html`: Single source of truth for the full prototype app
- `.gitignore`: Local artifact exclusions
- `PROJECT_UNDERSTANDING.md`: Full project understanding and implementation status document
- `runtime-config.js`: Runtime secrets/config override stub (safe defaults)
- `firebase-config.example.json`: Example Firebase web config template
- `edge_node/`: Edge telemetry emulator bridge (Python + Firebase Admin SDK)

## Runtime Configuration

### Firebase

The repo ships with a working Firebase web SDK config bundled directly in `index.html`. This is the demo project's *public* web key — Firebase web keys are designed to be embedded in client code; the security boundary is enforced by Realtime Database rules + API-key restrictions in the Cloud Console, not by hiding the object. Anyone cloning the repo gets multi-device sync working out of the box.

To point at your own Firebase project instead, override in any of these ways (highest priority first):

1. `window.__ACOUSTICGUARD_FIREBASE_CONFIG = { ... }` in `runtime-config.js`.
2. Drop a `firebase-config.json` next to `index.html` (gitignored).
3. Set the bundled config in `index.html`.

### TomTom (live traffic + routing geometry)

The app falls back to a deterministic synthetic traffic model if no key is provided, so the UI is always populated. To switch to live TomTom data, choose one:

1. `window.__ACOUSTICGUARD_TOMTOM_KEY = "YOUR_KEY"` in `runtime-config.js` (recommended for local demo).
2. Append `?tomtomKey=YOUR_KEY` to the URL once — it's persisted in `localStorage` from then on.
3. `localStorage.setItem('acousticguard.tomtom.key', 'YOUR_KEY')` in DevTools.

Get a free key at https://developer.tomtom.com (Routing API + Traffic Flow API).

The top-bar `Live Traffic:` badge tells you which mode the UI is in: `TomTom` (live) or `Fallback` (synthetic).

## Edge Backend (Cloud Run-deployable)

The `edge_node/` folder is the deployable backend half of AcousticGuard — a 12-node simulated edge fleet that publishes heartbeats + detections into the same Firebase paths the dashboard reads. Three run modes:

```bash
# 1. Local laptop demo
pip install -r edge_node/requirements.txt
python edge_node/edge_sensor_bridge.py \
  --service-account "C:/path/to/service-account.json" \
  --database-url "https://acousticguard-default-rtdb.firebaseio.com"

# 2. Offline / dry-run (no Firebase, prints JSON to stdout)
python edge_node/edge_sensor_bridge.py --dry-run

# 3. Cloud Run job (Dockerfile in edge_node/)
gcloud builds submit edge_node --tag gcr.io/$PROJECT_ID/acousticguard-edge
gcloud run jobs deploy acousticguard-edge \
  --image gcr.io/$PROJECT_ID/acousticguard-edge \
  --set-env-vars FIREBASE_DATABASE_URL=https://acousticguard-default-rtdb.firebaseio.com \
  --service-account=acousticguard-edge@$PROJECT_ID.iam.gserviceaccount.com \
  --region=asia-south1
```

Replacing the emulator with real Raspberry Pi devices is a one-day swap: same JSON shape, same Firebase paths, dashboard untouched. See [edge_node/README.md](./edge_node/README.md).

## Running Locally

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/index.html`.

A service worker (`sw.js`) caches the YAMNet model, TF.js, Leaflet, Chart.js, and basemap tiles after the first successful load — the demo stays usable on a flaky judge-room network.

## Demo Flow

1. Select `Hotel` in Venue Mode.
2. Run `Medical Crisis` — show guest safety, staff tasks, responder gate, crisis timeline, ambulance route on map.
3. Trigger `Conflict` to demonstrate multi-ambulance arbitration.
4. Use `Replay` for deterministic rerun (judge-friendly).
5. Enable `LIVE MIC` and play a siren / talk into the mic to show the YAMNet decision tree.
6. Switch to `Hospitality Crisis Analytics` → `Generate Crisis Report` → `Export PDF`.

## Resilience

| Component       | Live mode                              | Fallback path                                                  |
|-----------------|----------------------------------------|----------------------------------------------------------------|
| Firebase RTDB   | Bundled web config (works out of box)  | In-memory store, "LOCAL MODE" badge in topbar                  |
| YAMNet model    | TF.js + TFHub model, prefetched, SW-cached | Heuristic RMS/ZCR/spike classifier, `AI Engine: Fallback` badge |
| TomTom traffic  | Flow Segment + Routing API             | Deterministic per-node synthetic multipliers, `Fallback` badge |
| Mic permission  | `getUserMedia` siren/noise inference   | Manual `🚨 Siren` / `🚗 Traffic` simulation buttons             |
| Edge ingestion  | Cloud Run / local Python bridge        | Dashboard scenario buttons emit synthetic events               |

## Important Notes

- This is a hackathon prototype, not a certified emergency-service or medical device.
- The bundled Firebase web key is intentional and locked down via DB rules; rotate + re-restrict for production deployments.
- Real audio is not persisted — only inference labels and confidence are stored.
