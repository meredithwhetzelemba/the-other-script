# Final Project — Course Assignment Summary

**Due:** Monday, November 23, 2026 at 11:59 PM on Canvas  
**Type:** Solo project

## Big idea

Build an AI agent app that does something useful for real people. Show how it works, what it costs, and how you kept it safe.

Pick something that matters to someone: a business, nonprofit, classroom, hospital, old job, family, community. It does not have to make money — it has to make a difference.

---

## What you submit (Canvas)

| What | Details |
|------|---------|
| **GitHub repo** | Link to repo with all code + README how to run. Public, or private with `zlisto` added as collaborator. |
| **report.html** | Single self-contained HTML, 10–15 pages when printed. Embed images so it works offline. |
| **slides.html** | Single self-contained HTML, 10 slides max, reveal.js from CDN. Embed images. |
| **Demo video (optional)** | 2–3 min screen recording of real use. Backup for “It works” / “Look + feel” if local run fails; cannot earn the 5 “staff can run it” points. |

---

## Report sections (in order)

1. **Title + links** — name, your name, GitHub link, app link if online, one-sentence what it does  
2. **Motivation** — who has the problem, how they cope today, cost in money/time/frustration  
3. **What is new here** — existing apps/startups/ChatGPT; honest differentiation  
4. **The agents** — each agent’s job, tools, organization/handoffs + diagram, model(s) + why, one real run step-by-step with screenshots  
5. **Tokenomics** — tokens per typical run (input / cached / output), cost per run, per user/month, at 100 and 10,000 users, cost-cutting + whether it hurt performance  
6. **Safety** — prompt injection / data leak / misbehavior; hallucination / wrong action / infinite loops; overspend guards; show ≥1 defense working with screenshot/test  
7. **Impact** — numbers (money, hours, quality, reach) with sources; real user evidence strongest  
8. **Limits + next steps** — what doesn’t work; what you’d build next month  

Write for a smart manager who never saw the app. AI drafting OK; you own every word/number.

---

## Slides (reveal.js, ≤10)

Suggested order: Title → Problem → What’s new → Agents (diagram) → Demo screenshots → Cost → Safety → Impact numbers → What’s next

---

## Repo requirements

- All code needed to run the app  
- `README.md` — what it is + how to run (or live link)  
- `.env.example` — key names only, no secrets  
- Never commit `.env` or real `PORTKEY_API_KEY`  
- Load `.env` from **repo folder first**, then **parent folder** (staff clone layout under `submissions/.env`)  
- Keys: `PORTKEY_API_KEY` and/or `OPENAI_API_KEY` only (exact names)  
- Course key → `gpt-6-luna` via Portkey only; own key if other models  
- Large data → include small test dataset + README how to switch  
- Staff 10-minute rule: not running after 10 min following README → 0 for “staff can run it”

---

## Grading (100 pts) — tiers

- **Tier 1:** Works; familiar idea; thin cost/safety detail  
- **Tier 2:** Clever/new + thoughtful agents + measured tokens + real safety defense + screenshots  
- **Tier 3:** Tier 2 + clear real-world difference + evidence (real user, measured impact, org-scale cost thinking)

### Point breakdown

| Component | Pts | Top of range |
|-----------|-----|--------------|
| Novelty + real-world value | 21 | Clever, new, usable by real people (overdone ideas capped Tier 1 without twist) |
| It works | 15 | End-to-end real tools/data/results; clean repo; no secrets |
| Staff can run it | 5 | Online or fresh clone + parent `.env` ≤10 min |
| Look + feel | 10 | Clean, usable by a stranger |
| Motivation + what’s new | 8 | Real person + named existing products compared |
| Agent design | 10 | Agents/tools/diagram + traced real run with screenshots |
| Tokenomics | 8 | Real measured tokens/costs + cost cuts ± performance evidence |
| Safety | 8 | Built defenses + screenshot/test of one working |
| Impact + metrics | 5 | Believable numbers + sources; real user evidence preferred |
| Report design | 2 | Clean layout, sharp screenshots/diagrams |
| Slides content | 6 | Full story, diagram, screenshots, key numbers |
| Slides design | 2 | Big text, consistent style |
| **Total** | **100** | |

### Overdone ideas (Tier 1 cap without real twist)

Resume/cover letter reviewer · Chat with PDF/docs · Trip planner · Email/meeting summarizer · Recipe/meal planner · Generic study buddy/flashcards · Class/homework redo without new addition

---

## Tips (from prompt)

- Start with a person, then the tech  
- Talk to a real user (even 15 min)  
- Screenshot good runs, bad runs, safety catches as you go  
- Ship working first; then make it clever  
