# AcousticGuard: Where We Start (Just You + Me)

This plan assumes a **single builder** with AI copilot support and tight hackathon time.
Goal: maximize judge score quickly with the least risky execution path.

## Start Here (Order Matters)

## Step 1 — Lock the winning scope (30 min)
Decide and freeze only the features needed for judging.

### Must-have scope
1. **One real AI inference path works live** (no fake button-only simulation).
2. **One strong demo scenario** that shows before/after impact.
3. **Rubric mapping table** (criterion → feature → proof).
4. **Security/privacy note** (keys, data storage, location handling).
5. **90-second demo script** opening with your strongest moment.

### Out-of-scope for now
- Custom model training from scratch.
- Big UI redesign.
- Nice-to-have extras not tied to scoring.

---

## Step 2 — Build the core “real AI” proof first (2–4 hours)
This is your highest-risk item, so do it first.

### Target outcome
- App can take microphone/audio input.
- Model runs inference and outputs label + confidence.
- UI shows live prediction state and fallback states.

### Minimum implementation checklist
- [ ] Mic permission flow (allow/deny handling)
- [ ] Model load state (loading/ready/error)
- [ ] Inference trigger (live or short window)
- [ ] Prediction output panel (class/confidence/time)
- [ ] Fallback message if inference fails

---

## Step 3 — Immediately make it judge-readable (60–90 min)
Once AI proof works, package it for judges.

### Deliverables
1. **Rubric mapping block**
   - Technical merit → AI inference demo
   - Innovation → conflict-resolution angle
   - UX → clear decision surface
   - Impact → cited statistics
2. **“Implemented vs Mocked” disclosure**
   - Keep this explicit and honest.
3. **Source citations for every big claim**

---

## Step 4 — Security & trust patch (45–60 min)
Judges often penalize obvious trust gaps.

### Must do now
- [ ] Remove any hardcoded API keys from frontend.
- [ ] Add short privacy/security section in README/submission.
- [ ] State data retention clearly (what is stored, what is not).

---

## Step 5 — Demo script and dry run (45 min)
You win or lose in the first minute of demo.

### 90-second script structure
1. **0–15s:** Problem + one-line solution.
2. **15–45s:** Live AI moment (input → prediction).
3. **45–70s:** Conflict-resolution differentiator.
4. **70–90s:** Impact + what’s production next.

### Dry-run checklist
- [ ] Timer run complete in 90 sec.
- [ ] Backup path if mic/model fails.
- [ ] No dead clicks.

---

## What We Do Right Now (First Joint Working Session)

In our **next working session**, we do only this:
1. Audit your current HTML/JS and identify where simulated AI is wired.
2. Replace one simulation path with real inference.
3. Add prediction panel + fail-safe UI states.
4. Verify end-to-end with one repeatable test scenario.

If we complete these 4 items, you move from “good concept page” to “credible technical prototype.”

---

## Task Split (You + Me)

## You
- Share current files (HTML/CSS/JS) and where the fake AI trigger lives.
- Run local tests in browser and paste console errors/output.
- Confirm what works on your machine.

## Me
- Give exact code edits in sequence.
- Provide fallback-safe UI/logic patterns.
- Help draft rubric mapping, security note, and demo script text.

---

## Definition of “Good Start” by End of Today
You are on track if all are true:
1. Real inference works at least once reliably in your environment.
2. You can show label + confidence live.
3. Rubric mapping and security note are written.
4. You can run a clean 90-second demo once without interruption.
