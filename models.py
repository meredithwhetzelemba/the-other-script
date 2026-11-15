"""Structured outputs for The Other Script agents."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


EvidenceLevel = Literal["metric", "specific_example", "secondhand", "adjective_only"]

Stance = Literal[
    "soft_script_carrying_decision",
    "evidence_supports_draft",
    "too_thin_to_decide",
    "scripts_aligned",
]


class Claim(BaseModel):
    text: str
    evidence_level: EvidenceLevel
    note: str = ""


class EvidenceReport(BaseModel):
    claims: list[Claim] = Field(default_factory=list)
    summary: str = ""


class ScriptNarrative(BaseModel):
    title: str
    narrative: str
    key_drivers: list[str] = Field(default_factory=list)


class LanguageHit(BaseModel):
    quote: str
    pattern: str
    why_it_matters: str
    gender_relevant: bool = False


class LanguageReport(BaseModel):
    hits: list[LanguageHit] = Field(default_factory=list)
    overall_read: str = ""


class DeltaReport(BaseModel):
    soft_only_drivers: list[str] = Field(default_factory=list)
    evidence_holes: list[str] = Field(default_factory=list)
    would_decision_hold_on_evidence_alone: str = ""
    gender_pattern_hits: list[LanguageHit] = Field(default_factory=list)
    summary: str = ""


class CalibrationVoice(BaseModel):
    role: Literal["advocate", "skeptic", "presence_culture", "chair"]
    statement: str
    evidence_backed: bool = False


class CalibrationReport(BaseModel):
    voices: list[CalibrationVoice] = Field(default_factory=list)
    what_survived_chair: list[str] = Field(default_factory=list)
    chair_ruling: str = ""


class ExecutiveSummary(BaseModel):
    """Punchy plain-English verdict shown first in the UI."""

    stance: Stance
    headline: str = Field(
        description="One blunt sentence. Take a clear position. No legalese."
    )
    plain_english: str = Field(
        description="2–4 short sentences a busy partner can skim."
    )
    what_youre_about_to_ratify: str = ""
    what_evidence_alone_says: str = ""
    do_this_before_you_lock: list[str] = Field(default_factory=list)
    questions_for_partners: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "Decision hygiene — not a legal finding of discrimination."
    )


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    model: str = ""


class PipelineResult(BaseModel):
    sanitized_partner_notes: str = ""
    sanitized_draft_synthesis: str = ""
    pii_warnings: list[str] = Field(default_factory=list)
    safety_blocks: list[str] = Field(default_factory=list)
    evidence: EvidenceReport | None = None
    script_a: ScriptNarrative | None = None
    script_b: ScriptNarrative | None = None
    language: LanguageReport | None = None
    delta: DeltaReport | None = None
    calibration: CalibrationReport | None = None
    executive: ExecutiveSummary | None = None
    guardrail_notes: list[str] = Field(default_factory=list)
    agent_trace: list[str] = Field(default_factory=list)
    usage: TokenUsage = Field(default_factory=TokenUsage)
    gender_mode: bool = True
    error: str | None = None
