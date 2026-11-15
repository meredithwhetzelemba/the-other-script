# Final Project — Working Plan

Due: Monday, November 23, 2026 · Work through these one at a time.

---

## Phase 1 — Idea

1. **Brainstorm real problems** — List people you know and friction they deal with (work, school, family, community). Prefer problems you can talk to a real person about.
2. **Pick a direction** — Choose 1 idea that is useful, not on the overdone list (or has a clear twist), and that we can build by the deadline.
3. **Write the one-liner** — Who it’s for, what pain it removes, what the app does in one sentence.

---

## Phase 2 — Design the agents

4. **Sketch the agent team** — Name each agent, what it does, what tools it needs, and who hands work to whom (simple diagram).
5. **Define a “happy path” demo** — One concrete example a stranger can run end-to-end in a few minutes.
6. **List safety + cost risks** — What could go wrong (injection, bad actions, token burn) and what defenses/cost controls we’ll build in from the start.

---

## Phase 3 — Build the app

7. **Scaffold the project** — Folder structure, `requirements.txt`, `.env.example`, parent-folder `.env` loading, README stub, black-and-pink UI shell.
8. **Ship a thin working version** — One useful flow that actually calls agents + tools (ugly is fine; must run).
9. **Add the clever parts** — Multi-agent handoffs, better tools, caching/cost cuts, polish UI.
10. **Add safety defenses** — At least one we can screenshot working (e.s. injection block, spend cap, validation).
11. **Instrument tokenomics** — Log/show input, cached, and output tokens per run so the report has real numbers.

---

## Phase 4 — Prove it

12. **Run real demos** — Screenshot good runs, a full agent walkthrough, and a safety catch.
13. **Measure costs** — Typical run cost; estimate per user/month and at 100 / 10,000 users; note any cost cut that hurt quality.
14. **Talk to a real user (if possible)** — Even 15 minutes: quote, before/after time, or them trying the app (Tier 3 evidence).

---

## Phase 5 — Report, slides, repo

15. **Write `report.html`** — All 8 sections, embedded screenshots/diagram, self-contained (double-click to open).
16. **Make `slides.html`** — reveal.js from CDN, ≤10 slides, same story + embedded visuals.
17. **Finish the repo** — Clean README (10-minute setup), no secrets, test dataset if needed, public or add `zlisto`.

---

## Phase 6 — Dry run + submit

18. **Dry run** — Fresh clone → `.env` one folder up → follow README → use the app. Fix anything that breaks.
19. **Optional demo video** — 2–3 min screen recording of a real example (backup if staff setup fails).
20. **Submit on Canvas** — Repo link + `report.html` + `slides.html` (+ video if you made one) before Nov 23, 11:59 PM.

---

## Where we are now

**Done:** Phase 1–3 core app (idea, design, working UI + agents + exec summary)  
**Done:** Phase 4 evidence — sample run screenshot, safety catch screenshot, token numbers  
**Done:** Phase 5 draft — `report.html` (Meredith Whetzel; screenshots embedded)  
**Current step:** Review report → `slides.html` → GitHub URL in report → dry-run → Canvas  
**Optional Tier 3 still open:** real user try / quote
