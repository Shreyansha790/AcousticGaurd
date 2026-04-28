# AcousticGuard.ai - Complete Project Understanding Document

## 1) Project in One Line
AcousticGuard.ai is a hospitality-focused crisis command dashboard that detects emergency audio/events, coordinates venue staff, and routes responders/ambulances to hospitals using live traffic intelligence.

## 2) Why This Project Exists
Large hospitality spaces (hotels, malls, stadiums, resorts) struggle in emergencies because response actions are fragmented across guests, front desk, security, medical teams, and city responders.  
This project creates one operational control layer that unifies:
- detection,
- coordination,
- responder routing,
- and incident reporting.

## 3) Hackathon Fit
This directly fits **Rapid Crisis Response / Emergency Coordination in Hospitality** because it demonstrates:
- immediate crisis identification,
- coordinated communication flow,
- responder bridge (venue -> ambulance -> hospital),
- and measurable response analytics.

## 4) Current Product Scope
The build currently supports:
- Venue profiles: `hotel`, `mall`, `stadium`, `resort`
- Crisis presets: `medical`, `fire`, `security`, `evacuation`
- Live map-based corridor and responder visualization
- Multi-ambulance arbitration conflict demo
- Replay mode for deterministic judging
- Live mic inference with AI model + fallback safety layer

## 5) Core Modules

### A) Venue Crisis Command Layer
- Venue mode selector
- Active zone / safe zone / responder gate model
- Crisis timeline and command panel
- Staff dispatch board

### B) AI Audio Detection Layer
- Primary engine: **TensorFlow.js + YAMNet**
- Browser microphone input
- Siren/noise classification and confidence
- Decision diagnostics panel
- Runtime resilience: fallback classifier if YAMNet fails

### C) Routing & Traffic Layer
- TomTom Flow API for traffic multipliers
- TomTom Routing geometry for actual road path rendering
- Venue-origin medical path logic (start at crisis venue, end at selected hospital)
- Leaflet map for corridor and ambulance movement

### D) Conflict Arbitration Layer
- Simulates simultaneous ambulance demand
- Priority scoring based on urgency, ETA, overlap, traffic
- Winner corridor allocation + second vehicle reroute
- Explainable conflict notes for judging

### E) Data & Persistence Layer
- Firebase Realtime Database integration
- Local in-memory fallback when Firebase is unavailable
- Crisis/detection/corridor records maintained for dashboard + analytics

## 6) Technical Stack
- Frontend: `HTML`, `CSS`, `JavaScript` (single-file app in `index.html`)
- AI: `TensorFlow.js`, `YAMNet`
- Maps: `Leaflet`
- Charts: `Chart.js`
- Traffic: `TomTom APIs`
- Backend store: `Firebase Realtime Database` (+ local fallback)

## 7) Data Objects (Conceptual)
The app tracks (directly or effectively) these entities:
- `venue`: profile, coordinates, display labels
- `activeCrisis`: type, severity, affected zone, safe zone, responder gate
- `staffTasks`: role -> task -> status -> timestamp
- `crisisTimeline`: ordered event log
- `detections`: audio/scenario trigger records
- `corridors`: active responder paths and route context

## 8) End-to-End Runtime Flow
1. User selects venue and scenario (`medical`/`fire`/etc.).
2. Crisis state activates with staff tasks + timeline updates.
3. For medical:
   - venue coordinates become route origin,
   - nearest/best hospital is selected,
   - TomTom route geometry is fetched,
   - ambulance path is rendered on map.
4. Traffic multipliers affect ETA/conflict behavior.
5. Results update logs, diagnostics, conflict panel, and analytics.

## 9) AI Reliability Design (Important)
To avoid pipeline breakage:
- YAMNet load has retry strategy with alternate source format.
- Load timeout and runtime error guards are active.
- If model loading/execution fails, app automatically switches to fallback inference.
- Mic flow remains usable even during model/CDN failure.

## 10) What Is Real vs Simulated

### Real / Live
- Browser microphone capture
- YAMNet inference (when available)
- TomTom traffic flow sampling
- TomTom routing geometry
- Firebase writes/reads (when configured)

### Simulated / Demo Logic
- Some arbitration scoring logic (rule-based)
- Scenario presets and task progression
- Replay determinism for judging consistency

## 11) Files That Matter Most
- `index.html` -> full application logic/UI/data flow
- `README.md` -> project overview and run guide
- `PROJECT_UNDERSTANDING.md` -> this complete understanding document

## 12) Local Run
Use:
```bash
python -m http.server 5500
```
Then open:
`http://127.0.0.1:5500/index.html`

## 13) Recommended Judge Demo Script (Short)
1. Select a venue mode.
2. Trigger `Medical Crisis`.
3. Show command panel: affected zone, safe zone, responder gate, staff tasks.
4. Highlight route: venue -> hospital with TomTom traffic context.
5. Trigger `Conflict` and explain arbitration.
6. Show `Replay` deterministic behavior.
7. Open analytics/report and summarize impact.

## 14) Current Strengths
- Strong visual operational dashboard
- Good challenge alignment for hospitality emergency coordination
- Real external integrations (TomTom, mic AI, Firebase)
- Explainable conflict logic and replay safety for judges
- Improved resilience (fallbacks for network/model issues)

## 15) Current Gaps / Risks
- Not production-certified emergency tooling
- Some logic is demo-grade rather than fully deployed backend orchestration
- API key/security posture must be hardened before production
- Multi-tenant auth and role-based controls are not yet implemented

## 16) Immediate Next Upgrades
- Add explicit `Inference Engine: YAMNet/Fallback` badge in UI
- Add one-click `Demo Reset` action
- Add hospitality KPI cards: detection-to-dispatch, zone-clearance time, ETA saved
- Improve mobile responsiveness for narrower screens
- Rotate exposed keys post-demo

## 17) Final Positioning Statement
AcousticGuard.ai is not just a siren detector. It is a hospitality crisis coordination command layer that connects live detection, staff synchronization, and responder routing into one judge-visible emergency workflow.
