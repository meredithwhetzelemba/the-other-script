# The Other Script

A promotion-synthesis stress tester for **people leadership** in consulting.

Bias rarely shows up as one sexist sentence. It shows up as different language for the same performance — and it often hardens when partner discussion becomes a decision. This app shows **Script A** (the narrative you’re about to ratify) vs **Script B** (the other script the same evidence supports), plus light calibration and questions to send back to partners.

It does **not** declare discrimination. It is decision hygiene.

## Quick start

Requires **Python 3.11+** (3.12 recommended).

```bash
cd "Final Project"   # or your clone root
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### API keys

Copy `.env.example` → `.env` in this folder **or** put `.env` one level above this folder (teaching-staff layout):

```
submissions/
├── .env                 ← PORTKEY_API_KEY / OPENAI_API_KEY
└── your-project/        ← this repo
```

The app loads **project `.env` first**, then the **parent** folder.

```bash
# .env
PORTKEY_API_KEY=your_key_here
OPENAI_MODEL=gpt-6-luna
```

Course key: use `PORTKEY_API_KEY` with `gpt-6-luna` only.  
Own key: set `OPENAI_API_KEY` instead if you use a different model.

### Run

```bash
python app.py
```

Open [http://127.0.0.1:8050](http://127.0.0.1:8050).

1. Sample case is preloaded (or click **Load sample case**).  
2. Leave **Gender-pattern stress test** on for the full demo.  
3. Click **Run The Other Script**.

## What’s in the box

| Path | Role |
|------|------|
| `app.py` | Dash UI (black & pink) |
| `pipeline.py` | Multi-agent orchestration |
| `models.py` | Structured outputs |
| `tools.py` | PII scrub, safety scan, token helpers |
| `config.py` | Env + Portkey/OpenAI model |
| `sample_cases/` | Anonymized demo packet |
| `IDEA.md` / `DESIGN.md` | Product lock + design |

## Safety (homework-style harness)

Same shape as course homeworks: **tools → stopping limits → guardrails → audit trail**.

- `blocked_request` / `is_unsafe_request` — injection, legal-finding pressure, secrets, illicit asks  
- Notes treated as untrusted data (strip instruction-like lines)  
- PII redaction; refuse legal discrimination verdicts; no invented metrics  
- `UsageLimits` per agent + per-run token spend cap  
- Audit log: `output/audit_trail.json`  
- Automated check: `python pressure_test.py`

## Tokenomics

Each run shows input / cached input / output tokens and an estimated USD cost on screen (for the report).
