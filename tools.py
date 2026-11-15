"""Local tools: PII scrub, safety scan, packet parse, budget helpers."""

from __future__ import annotations

import re
from pathlib import Path

from models import TokenUsage

ROOT = Path(__file__).resolve().parent
SAMPLE_CASE = ROOT / "sample_cases" / "case_01_anonymized.md"

# Rough $/1M token estimates for display (not a billing API). Course models vary;
# we show a transparent estimate and raw token counts from the run.
_USD_PER_M_INPUT = 2.50
_USD_PER_M_CACHED = 0.25
_USD_PER_M_OUTPUT = 10.00

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b")
_CLIENTISH = re.compile(
    r"\b(?:Acme|Pfizer|Merck|Novartis|Roche|AstraZeneca|J&J|Johnson\s*&\s*Johnson|"
    r"BMS|Bristol[- ]Myers|Lilly|AbbVie|Amgen|Gilead|Sanofi|Bayer|GSK|"
    r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\s+(?:Pharma|Pharmaceuticals|Therapeutics|Biotech))\b"
)

_INJECTION = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", re.I),
    re.compile(r"disregard\s+(your\s+)?(system|safety)\s+(prompt|rules)", re.I),
    re.compile(r"you\s+are\s+now\s+(dan|unrestricted|jailbroken)", re.I),
    re.compile(r"reveal\s+(your\s+)?(system|hidden)\s+prompt", re.I),
]

_LEGAL_DEMAND = [
    re.compile(
        r"(conclude|declare|find|prove)\s+.{0,40}(illegal|unlawful)\s+.{0,20}"
        r"(discrimination|harassment)",
        re.I,
    ),
    re.compile(r"\b(sue|lawsuit|eeoc\s+complaint|legal\s+finding)\b", re.I),
    re.compile(
        r"(this\s+is|conclude\s+this\s+is)\s+illegal\s+gender\s+discrimination",
        re.I,
    ),
]

# Homework-style hard blocks (HW3/HW5 pattern): return a reason string or None.
_UNSAFE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", re.I),
        "Prompt-injection attempt blocked. Notes are treated as data, not orders.",
    ),
    (
        re.compile(r"disregard\s+(your\s+)?(system|safety)\s+(prompt|rules)", re.I),
        "Attempt to override safety rules blocked.",
    ),
    (
        re.compile(r"reveal\s+(your\s+)?(system|hidden)\s+prompt", re.I),
        "Refusing to reveal the system prompt.",
    ),
    (
        re.compile(r"(api[_-]?key|portkey|_api_key|secret\s*key|\.env)", re.I),
        "Refusing to reveal secrets or API keys.",
    ),
    (
        re.compile(
            r"(conclude|declare|find|prove)\s+.{0,40}(illegal|unlawful)\s+.{0,20}"
            r"(discrimination|harassment)",
            re.I,
        ),
        "Refusing a legal discrimination finding — decision hygiene only.",
    ),
    (
        re.compile(r"(this\s+is|conclude\s+this\s+is)\s+illegal\s+gender\s+discrimination", re.I),
        "Refusing a legal discrimination finding — decision hygiene only.",
    ),
    (
        re.compile(r"\b(hack|exploit|malware|ransomware)\b", re.I),
        "Refuse unsafe / illicit asks.",
    ),
    (
        re.compile(r"\b(exfiltrat|steal)\b.*\b(key|password|secret)\b", re.I),
        "Refuse secret exfiltration.",
    ),
]


def blocked_request(text: str) -> str | None:
    """Homework-style guardrail: first matching hard block, else None."""
    blob = text or ""
    for pattern, reason in _UNSAFE_PATTERNS:
        if pattern.search(blob):
            return reason
    return None


def is_unsafe_request(text: str) -> str | None:
    """Alias used in homework agents — same as blocked_request."""
    return blocked_request(text)


_BANNED_OUTPUT = (
    "illegal discrimination",
    "guilty of discrimination",
    "you should sue",
    "this is unlawful discrimination",
)


def output_violates_policy(text: str) -> str | None:
    low = (text or "").lower()
    for phrase in _BANNED_OUTPUT:
        if phrase in low:
            return f"Disallowed output phrasing: “{phrase}”."
    return None


def load_sample_case() -> tuple[str, str]:
    """Return (partner_notes, draft_synthesis) from the bundled sample."""
    text = SAMPLE_CASE.read_text(encoding="utf-8")
    partner, draft = "", ""
    section = None
    for line in text.splitlines():
        if line.strip().lower().startswith("## partner"):
            section = "partner"
            continue
        if line.strip().lower().startswith("## draft") or line.strip().lower().startswith(
            "## people"
        ):
            section = "draft"
            continue
        if line.strip().startswith("# ") and section:
            # new top-level unrelated section
            if "partner" not in line.lower() and "draft" not in line.lower():
                section = None
        if section == "partner":
            partner += line + "\n"
        elif section == "draft":
            draft += line + "\n"
    return partner.strip(), draft.strip()


def sanitize_pii(text: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    out = text or ""
    if _EMAIL.search(out):
        warnings.append("Redacted email address(es).")
        out = _EMAIL.sub("[REDACTED_EMAIL]", out)
    if _PHONE.search(out):
        warnings.append("Redacted phone number(s).")
        out = _PHONE.sub("[REDACTED_PHONE]", out)
    if _CLIENTISH.search(out):
        warnings.append("Flagged possible client/org names — review before sharing externally.")
        out = _CLIENTISH.sub("[REDACTED_ORG]", out)
    return out, warnings


def safety_scan(text: str) -> list[str]:
    """Return human-readable blocks for injection / legal-demand patterns."""
    blocks: list[str] = []
    blob = text or ""
    for pat in _INJECTION:
        if pat.search(blob):
            blocks.append(
                "Prompt-injection language detected in the pasted notes. "
                "Those instructions were ignored; the run continues as decision hygiene only."
            )
            break
    for pat in _LEGAL_DEMAND:
        if pat.search(blob):
            blocks.append(
                "Request for a legal discrimination finding detected. "
                "The Other Script will not declare illegality or liability."
            )
            break
    return blocks


def strip_instruction_like_lines(text: str) -> str:
    """Treat pasted notes as untrusted data: neutralize common injection lines."""
    kept: list[str] = []
    for line in (text or "").splitlines():
        if any(p.search(line) for p in _INJECTION + _LEGAL_DEMAND):
            kept.append("[INSTRUCTION-LIKE LINE REMOVED]")
        else:
            kept.append(line)
    return "\n".join(kept)


def estimate_cost_usd(input_tokens: int, output_tokens: int, cached: int = 0) -> float:
    return (
        (input_tokens - cached) * _USD_PER_M_INPUT / 1_000_000
        + cached * _USD_PER_M_CACHED / 1_000_000
        + output_tokens * _USD_PER_M_OUTPUT / 1_000_000
    )


def usage_from_run(usage_obj: object, model: str, acc: TokenUsage | None = None) -> TokenUsage:
    """Accumulate pydantic-ai RunUsage-like objects into TokenUsage."""
    acc = acc or TokenUsage(model=model)
    inp = int(getattr(usage_obj, "input_tokens", 0) or 0)
    out = int(getattr(usage_obj, "output_tokens", 0) or 0)
    cached = int(getattr(usage_obj, "cache_read_tokens", 0) or 0)

    acc.input_tokens += inp
    acc.output_tokens += out
    acc.cached_input_tokens += cached
    acc.total_tokens = acc.input_tokens + acc.output_tokens
    acc.estimated_cost_usd = round(
        estimate_cost_usd(acc.input_tokens, acc.output_tokens, acc.cached_input_tokens), 6
    )
    acc.model = model
    return acc


def enforce_budget(acc: TokenUsage, max_tokens: int) -> str | None:
    if acc.total_tokens >= max_tokens:
        return (
            f"Spend cap reached ({acc.total_tokens} tokens ≥ {max_tokens}). "
            "Pipeline stopped early to protect the budget."
        )
    return None
