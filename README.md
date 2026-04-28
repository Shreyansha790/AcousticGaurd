# AcousticGuard.ai

AcousticGuard.ai is a smart emergency-response prototype built for the Google Solution Challenge context. It detects ambulance siren signals from live audio, validates them using AI classification, and orchestrates traffic signal corridors to reduce urban ambulance delays.

The current prototype is focused on Bengaluru-like traffic conditions and demonstrates both single-ambulance and multi-ambulance conflict scenarios with live map visualization, hospital-aware routing, and real-time analytics.

## Why This Project

Urban emergency vehicles lose critical minutes in congestion. AcousticGuard.ai addresses this by combining:

- Real-time audio intelligence
- Intersection-level routing orchestration
- Explainable multi-ambulance arbitration
- Data-driven urban planning insights

## Core Features

- `Real AI Audio Detection`:
  - Live mic capture in browser
  - TensorFlow.js + YAMNet-based sound classification
  - Siren/noise confidence scoring with decision trace

- `Emergency Corridor Activation`:
  - Automatic route activation on high-confidence siren events
  - Animated corridor rendering on Leaflet map
  - Signal node sequencing visualization

- `Multi-Ambulance Arbitration`:
  - Conflict-first demo flow
  - Priority scoring based on urgency, ETA window, overlap risk, and traffic density
  - Winner and rerouted path logic
  - Explainable reasoning and ETA delta display
  - Deterministic replay mode for judging/demo consistency

- `Live Traffic Integration (TomTom)`:
  - Real-time traffic flow sampling from TomTom Flow Segment API
  - Traffic multipliers applied to ETA + conflict arbitration
  - Dynamic congestion visualization in route rendering and node table
  - Safe synthetic fallback when live traffic API is unavailable

- `Hospital-Aware Routing`:
  - Nearest hospital ranking
  - Bed-availability-aware selection panel
  - User location + nearest hospital path support

- `City Analytics & Report`:
  - Detection volume charts
  - Confidence distribution
  - Hotspot visibility
  - Session-level impact report modal

## Tech Stack

- `Frontend`: HTML, CSS, JavaScript (single-page architecture)
- `AI`: TensorFlow.js, YAMNet
- `Map`: Leaflet.js + dark basemap
- `Charts`: Chart.js
- `Backend/Data`: Firebase Realtime Database

## Project Structure

- `index.html`: Single source of truth for the full prototype app (UI + logic + inference + routing)
- `.gitignore`: Local artifact exclusions

Legacy note:
- Older draft file `acousticguard_live(4).html` has been removed to avoid demo confusion.

## Running Locally

Use a local server (recommended, not direct file open):

```bash
python -m http.server 5500
```

Then open:

`http://127.0.0.1:5500/index.html`

## Demo Flow (Recommended)

1. Enable `LIVE MIC`
2. Trigger `Conflict` to showcase multi-ambulance arbitration first
3. Use `Replay` for deterministic rerun
4. Trigger `Siren` and `Traffic` for single-event behavior
5. Switch to `City Analytics` and open report modal

## Impact Narrative

AcousticGuard.ai is designed as an emergency mobility orchestrator, not only a siren detector. It combines detection, explainable routing arbitration, and city-level impact telemetry to support faster response times and better emergency outcomes.

## Next Build Targets

- Stronger mobile responsiveness
- Hardening Firebase access rules and privacy posture
- Historical conflict history table for audits
- Edge-node telemetry beyond route probes
- Production split into modular JS files + deployment pipeline

