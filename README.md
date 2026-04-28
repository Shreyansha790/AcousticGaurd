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

You can provide live infra credentials in three ways:

1. `runtime-config.js` (recommended for local demo)
2. `firebase-config.json` (optional file; use `firebase-config.example.json` as template)
3. Browser `localStorage` / query param (`?tomtomKey=...`) for quick testing

By default:
- Firebase attempts live init and falls back to local mode if unavailable
- TomTom runs fallback traffic mode if no key is provided

## Edge Backend Emulator (Phase 2 Readiness)

To demonstrate non-browser telemetry ingestion:

```bash
pip install -r edge_node/requirements.txt
python edge_node/edge_sensor_bridge.py --service-account "C:/path/to/service-account.json" --database-url "https://your-project-default-rtdb.firebaseio.com"
```

This publishes edge heartbeats + detection events to Firebase so judges can see a realistic backend/edge integration path.

## Running Locally

Use a local server:

```bash
python -m http.server 5500
```

Then open:

`http://127.0.0.1:5500/index.html`

## Demo Flow

1. Select `Hotel` in Venue Mode.
2. Run `Medical Crisis`.
3. Show guest safety, staff tasks, responder gate, and crisis timeline.
4. Trigger `Conflict` to demonstrate multi-ambulance responder arbitration.
5. Use `Replay` for deterministic rerun.
6. Enable `LIVE MIC` and show the YAMNet siren/noise classifier if microphone access is available.
7. Switch to `Hospitality Crisis Analytics` and generate the crisis report.

## Important Notes

- This is a hackathon prototype, not a certified emergency-service or medical device.
- Do not commit real API keys/service-account secrets to public repos.
- If Firebase or TomTom is unavailable, the app stays usable through local/demo fallback paths.
- If YAMNet model fetch fails (network/CDN), the mic pipeline continues using fallback inference mode.
