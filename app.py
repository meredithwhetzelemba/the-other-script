"""The Other Script — Dash app.

Run:  python app.py
Open: http://127.0.0.1:8050
"""

from __future__ import annotations

import traceback

from dash import Dash, Input, Output, State, dcc, html, no_update

from config import has_api_key, load_env, model_name
from models import PipelineResult
from pipeline import run_pipeline
from tools import load_sample_case

load_env()

app = Dash(__name__)
app.title = "The Other Script"
server = app.server

_SAMPLE_PARTNER, _SAMPLE_DRAFT = load_sample_case()


def _bullets(items: list[str] | None):
    if not items:
        return html.P("—", className="prose")
    return html.Ul([html.Li(x) for x in items], className="list")


_STANCE_LABEL = {
    "soft_script_carrying_decision": "Soft script is carrying this",
    "evidence_supports_draft": "Evidence supports the draft",
    "too_thin_to_decide": "Too thin to decide",
    "scripts_aligned": "Scripts mostly align",
}


def _hits(hits, limit: int = 4):
    rows = []
    for h in (hits or [])[:limit]:
        badges = [html.Span(h.pattern, className="badge")]
        if getattr(h, "gender_relevant", False):
            badges.insert(0, html.Span("Identity-coded", className="badge badge-hot"))
        rows.append(
            html.Div(
                [
                    html.Div(badges),
                    html.P(f"“{h.quote}”", className="hit-quote"),
                    html.P(h.why_it_matters, className="hit-meta"),
                ],
                className="hit",
            )
        )
    if not rows:
        return html.P("No pattern hits in this packet.", className="prose")
    return html.Div(rows)


def _details(summary: str, children) -> html.Details:
    return html.Details(
        [html.Summary(summary), html.Div(children, className="details-body")],
        className="details-block",
    )


def render_result(result: PipelineResult) -> list:
    blocks: list = []

    if result.error:
        blocks.append(html.Div(f"Run error: {result.error}", className="danger-box"))

    for b in result.safety_blocks:
        blocks.append(html.Div(b, className="danger-box"))
    for w in result.pii_warnings:
        blocks.append(html.Div(w, className="warn-box"))

    # —— 1. Executive summary (lead) ——
    ex = result.executive
    if ex:
        stance_label = _STANCE_LABEL.get(ex.stance, ex.stance.replace("_", " "))
        blocks.append(
            html.Div(
                [
                    html.P("Executive summary", className="panel-label"),
                    html.P(stance_label, className="stance-pill"),
                    html.H2(ex.headline, className="exec-headline"),
                    html.P(ex.plain_english, className="exec-plain"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("About to ratify", className="subhead"),
                                    html.P(ex.what_youre_about_to_ratify, className="prose"),
                                ],
                                className="exec-half",
                            ),
                            html.Div(
                                [
                                    html.P("Evidence alone says", className="subhead"),
                                    html.P(ex.what_evidence_alone_says, className="prose"),
                                ],
                                className="exec-half",
                            ),
                        ],
                        className="exec-split",
                    ),
                    html.P("Before you lock", className="subhead"),
                    _bullets(ex.do_this_before_you_lock),
                    html.P("Ask partners", className="subhead"),
                    _bullets(ex.questions_for_partners),
                    html.P(ex.disclaimer, className="hit-meta"),
                ],
                className="panel exec-panel",
            )
        )

    # —— 2. Dual scripts ——
    a = result.script_a
    b = result.script_b
    blocks.append(
        html.Div(
            [
                html.Div(
                    [
                        html.P("Script A · about to ratify", className="script-kicker"),
                        html.H3(a.title if a else "—", className="script-title"),
                        html.P(a.narrative if a else "—", className="prose"),
                        html.P("Drivers", className="subhead"),
                        _bullets(a.key_drivers if a else []),
                    ],
                    className="script-cell script-a",
                ),
                html.Div(
                    [
                        html.P("Script B · the other script", className="script-kicker"),
                        html.H3(b.title if b else "—", className="script-title"),
                        html.P(b.narrative if b else "—", className="prose"),
                        html.P("Drivers", className="subhead"),
                        _bullets(b.key_drivers if b else []),
                    ],
                    className="script-cell script-b",
                ),
            ],
            className="grid-2",
        )
    )

    # —— 3. Collapsed detail ——
    detail_sections = []

    if result.delta:
        d = result.delta
        detail_sections.append(
            _details(
                "Delta — soft vs evidence",
                [
                    html.P(d.summary, className="prose"),
                    html.P("Soft-only drivers", className="subhead"),
                    _bullets(d.soft_only_drivers),
                    html.P("Evidence holes", className="subhead"),
                    _bullets(d.evidence_holes),
                    html.P("Hold on evidence alone?", className="subhead"),
                    html.P(d.would_decision_hold_on_evidence_alone, className="prose"),
                ],
            )
        )

    pattern_hits = []
    if result.delta and result.delta.gender_pattern_hits:
        pattern_hits = result.delta.gender_pattern_hits
    elif result.language:
        pattern_hits = [h for h in result.language.hits if h.gender_relevant] or list(
            result.language.hits
        )

    detail_sections.append(
        _details(
            "Pattern lens — notable lines",
            [_hits(pattern_hits)],
        )
    )

    if result.calibration:
        cal = result.calibration
        voice_blocks = [
            html.Div(
                [
                    html.Span(v.role.replace("_", " "), className="badge"),
                    html.Span(
                        "evidence" if v.evidence_backed else "soft",
                        className="badge badge-hot" if not v.evidence_backed else "badge",
                    ),
                    html.P(v.statement, className="prose"),
                ],
                className="hit",
            )
            for v in cal.voices
        ]
        detail_sections.append(
            _details(
                "Light calibration replay",
                [
                    html.Div(voice_blocks),
                    html.P("Survived the chair", className="subhead"),
                    _bullets(cal.what_survived_chair),
                    html.P("Chair ruling", className="subhead"),
                    html.P(cal.chair_ruling, className="prose"),
                ],
            )
        )

    if result.evidence:
        claim_items = [
            html.Li(f"[{c.evidence_level}] {c.text}" + (f" — {c.note}" if c.note else ""))
            for c in result.evidence.claims
        ]
        detail_sections.append(
            _details(
                "Full evidence map",
                [
                    html.P(result.evidence.summary, className="prose"),
                    html.Ul(claim_items, className="list") if claim_items else html.P("—"),
                ],
            )
        )

    if result.agent_trace or result.guardrail_notes:
        notes = [html.P(g, className="hit-meta") for g in result.guardrail_notes]
        detail_sections.append(
            _details(
                "Agent trace & guardrails",
                notes
                + [
                    html.P(
                        " → ".join(result.agent_trace) if result.agent_trace else "—",
                        className="trace",
                    )
                ],
            )
        )

    u = result.usage
    detail_sections.append(
        _details(
            f"This run · {u.total_tokens} tokens · ≈ ${u.estimated_cost_usd:.4f}",
            [
                html.P(
                    f"{u.model or model_name()} · "
                    f"in {u.input_tokens} · cached {u.cached_input_tokens} · "
                    f"out {u.output_tokens}",
                    className="tokens",
                )
            ],
        )
    )

    blocks.append(
        html.Div(
            [html.P("Dig deeper", className="panel-label"), *detail_sections],
            className="panel",
        )
    )

    return blocks


app.layout = html.Div(
    [
        html.Div(
            [
                html.P("Promotion synthesis · people leadership", className="eyebrow"),
                html.H1(
                    ["The Other ", html.Em("Script")],
                    className="brand-title",
                ),
                html.P(
                    "Same performance. Different story. See which one you’re about to ratify.",
                    className="pitch",
                ),
                html.P(
                    "Paste partner discussion notes and your draft synthesis. "
                    "Get Script A vs Script B, the soft-language delta, a light calibration replay, "
                    "and questions to send back before you lock the decision.",
                    className="support",
                ),
                html.Details(
                    [
                        html.Summary("Why this exists"),
                        html.Div(
                            [
                                html.P(
                                    "Promotion bias rarely arrives as one ugly sentence. "
                                    "It shows up as different language for the same work — "
                                    "and often hardens when messy partner talk becomes one official story."
                                ),
                                html.P(
                                    "Research on real reviews finds soft, personality, and “fit” framing "
                                    "shows up unevenly; large workplace studies still show a broken rung "
                                    "at the first step into management. This tool stress-tests the "
                                    "synthesis step. It does not declare discrimination."
                                ),
                                html.P(
                                    "Sources: Lean In & McKinsey, Women in the Workplace 2025; "
                                    "Correll et al., ASR 2020; Textio performance-feedback studies."
                                ),
                            ],
                            className="why-body",
                        ),
                    ],
                    className="why-link",
                ),
            ],
            className="hero",
        ),
        html.Div(
            [
                html.P("Case packet", className="panel-label"),
                html.Label("Partner discussion notes", className="field-label"),
                dcc.Textarea(
                    id="partner-notes",
                    value=_SAMPLE_PARTNER,
                    placeholder="Paste anonymized partner discussion notes…",
                ),
                html.Label("Draft people-leadership synthesis", className="field-label"),
                dcc.Textarea(
                    id="draft-synthesis",
                    value=_SAMPLE_DRAFT,
                    placeholder="Paste the draft you’re about to ratify…",
                ),
                html.Div(
                    [
                        html.Button(
                            "Load sample",
                            id="load-sample",
                            n_clicks=0,
                            type="button",
                            className="btn-ghost",
                        ),
                        html.Button(
                            "Run",
                            id="run-btn",
                            n_clicks=0,
                            type="button",
                            className="btn-primary",
                        ),
                    ],
                    className="controls",
                ),
                html.P(
                    id="status",
                    children="Ready — a full run usually takes 1–2 minutes.",
                    className="status",
                ),
            ],
            className="panel",
        ),
        dcc.Loading(
            id="loading",
            type="dot",
            color="#ff2d7b",
            children=html.Div(id="results"),
        ),
        html.P(
            "Decision hygiene for promotion synthesis — not legal advice. Anonymize before pasting.",
            className="footer-note",
        ),
    ],
    id="app-shell",
)


@app.callback(
    Output("partner-notes", "value"),
    Output("draft-synthesis", "value"),
    Input("load-sample", "n_clicks"),
    prevent_initial_call=True,
)
def load_sample(_n):
    return load_sample_case()


@app.callback(
    Output("results", "children"),
    Output("status", "children"),
    Output("status", "className"),
    Input("run-btn", "n_clicks"),
    State("partner-notes", "value"),
    State("draft-synthesis", "value"),
    running=[
        (Output("run-btn", "disabled"), True, False),
        (Output("load-sample", "disabled"), True, False),
        (
            Output("status", "children", allow_duplicate=True),
            "Running — agents are working. Usually 1–2 minutes…",
            no_update,
        ),
        (
            Output("status", "className", allow_duplicate=True),
            "status status-live",
            no_update,
        ),
    ],
    prevent_initial_call=True,
)
def on_run(n_clicks, partner, draft):
    if not n_clicks:
        return no_update, no_update, no_update

    if not (partner or "").strip() or not (draft or "").strip():
        return (
            html.Div("Paste both partner notes and a draft synthesis.", className="danger-box"),
            "Missing input",
            "status",
        )

    if not has_api_key():
        return (
            html.Div(
                "No API key found. Add PORTKEY_API_KEY (or OPENAI_API_KEY) to "
                ".env in this folder, or one level above (see .env.example).",
                className="danger-box",
            ),
            "Missing API key",
            "status",
        )

    try:
        # Pattern lens is always on — soft / identity-coded language is core to the product.
        result = run_pipeline(
            partner or "",
            draft or "",
            gender_mode=True,
        )
        status = (
            f"Done · {result.usage.total_tokens} tokens · "
            f"≈ ${result.usage.estimated_cost_usd:.4f}"
        )
        return render_result(result), status, "status status-live"
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        return (
            html.Div(
                [
                    html.Div(str(exc), className="danger-box"),
                    html.Pre(traceback.format_exc(), className="trace"),
                ]
            ),
            "Run failed — see details below",
            "status",
        )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=8050)
