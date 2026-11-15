"""Environment and model setup for The Other Script.

Looks for .env in this project folder first, then one level up
(teaching-staff layout: submissions/.env next to the cloned repo).
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")

ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = "gpt-6-luna"
PORTKEY_BASE = "https://api.portkey.ai/v1"

# Soft ceiling so a bad loop cannot burn the budget (tokens ≈ rough units).
MAX_TOKENS_PER_RUN = 60_000
MAX_AGENT_STEPS = 8


def load_env() -> Path | None:
    """Load .env from project dir, then parent. Returns which file won (if any)."""
    local = ROOT / ".env"
    parent = ROOT.parent / ".env"
    found: Path | None = None
    if local.exists():
        load_dotenv(local, override=False)
        found = local
    if parent.exists():
        # Parent fills any missing keys (staff layout); does not override locals.
        load_dotenv(parent, override=False)
        if found is None:
            found = parent
    os.environ.setdefault("OPENAI_MODEL", DEFAULT_MODEL)
    return found


def model_name() -> str:
    load_env()
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def build_model() -> OpenAIResponsesModel:
    """Prefer Portkey (PORTKEY_API_KEY); fall back to direct OpenAI."""
    load_env()
    portkey = os.getenv("PORTKEY_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    name = model_name()

    if portkey:
        provider = OpenAIProvider(api_key=portkey, base_url=PORTKEY_BASE)
        return OpenAIResponsesModel(name, provider=provider)
    if openai_key:
        provider = OpenAIProvider(api_key=openai_key)
        return OpenAIResponsesModel(name, provider=provider)
    raise RuntimeError(
        "Missing API key. Set PORTKEY_API_KEY or OPENAI_API_KEY in "
        f"{ROOT / '.env'} or {ROOT.parent / '.env'} (see .env.example)."
    )


def has_api_key() -> bool:
    load_env()
    return bool(
        os.getenv("PORTKEY_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    )
