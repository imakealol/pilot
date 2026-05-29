# Production Crew — System Manual

**System:** Go Squad Production Crew
**Project:** Remanence / Resonance science-fiction trilogy
**Audience:** External consultant / reviewer
**Status:** In active use (Book 2, *Resonance* — manuscript complete, in revision)

---

## 1. What This System Is

The Production Crew is a **multi-agent editorial system** for collaborative long-form
fiction. It replaces the single all-purpose AI assistant with a panel of **specialized
editorial roles**, each with a narrow lane, defined permissions, and a mandatory
verification protocol.

The human author ("the Director") sets structural and thematic vision and makes every
final call. The agents execute and advise: drafting, revising, fact-checking, and
tracking continuity — each strictly inside its own domain.

It is, in effect, a publishing house's editorial department modeled as software: a
continuity editor, a line editor, a dialogue coach, a sensitivity reader, and so on —
plus a process auditor who checks their work before it reaches the author's desk.

---

## 2. Why It Exists — The Three Problems

LLM-assisted novel writing fails in three predictable ways. The system is built to
counter each:

| Problem | Symptom | Countermeasure |
|---------|---------|----------------|
| **Token window** | The model can't hold a whole novel + story bible in memory | Agents *query* a YAML canon database for only what they need |
| **Statelessness** | Every session starts from zero; prior decisions are lost | Canon and decisions live in version-controlled source files, not chat history |
| **Non-determinism** | The model invents plausible-but-wrong details to fill gaps | The Enforcer rejects any claim not cited to a source file |

The governing rule: **query before claiming.** No agent is allowed to assert a fact
about a character, the world, or the plot from memory. It must read the source file
and cite it.

---

## 3. Architecture

Three layers sit between raw work and the Director.

```
   ┌──────────────────────────────────────────────┐
   │  DIRECTOR (human author)                      │
   │  Structural vision · final editorial judgment │
   └───────────────▲──────────────────────────────┘
                   │ validated output only
   ┌───────────────┴──────────────────────────────┐
   │  META LAYER — Enforcer                        │
   │  Audits process, not creativity. The gate.    │
   └───────────────▲──────────────────────────────┘
                   │ output + process log
   ┌───────────────┴──────────────────────────────┐
   │  WORKING LAYER                                │
   │  · Production Crew  (13 editorial roles)      │
   │  · Character Stewards (voice guardians)       │
   └───────────────▲──────────────────────────────┘
                   │ queries
   ┌───────────────┴──────────────────────────────┐
   │  CANON LAYER — YAML database + chapter files  │
   │  CHARACTERS · CORE · GEOMETRY · CHAPTERS …     │
   └──────────────────────────────────────────────┘
```

- **Canon layer** — Machine-queryable source of truth: characters, world physics,
  constraints, timeline, chapter text. Accessed through a Python `StateQuery` interface.
- **Working layer** — The agents that do the work (see §4 and §6).
- **Meta layer** — The Enforcer, a process auditor (see §5).
- **Director** — The author. Receives only Enforcer-validated output.

---

## 4. The Production Crew — 13 Roles

Each role has a **lane** (its single domain), explicit read/write permissions, and a
fixed output format. Roles advise; they do not overrule the author.

| Role | Lane | What it does |
|------|------|--------------|
| **Continuity Editor** | fact-checking | Timeline order, character state, world rules, object positions — catches contradictions |
| **Prose Doctor** | line editing | Rhythm, clarity, word choice — improves *how* it reads without changing *what* it says |
| **Tension Architect** | pacing | Maps where tension rises, releases, and lets the reader breathe |
| **Dialogue Coach** | dialogue | Voice distinctiveness, natural rhythm, subtext over text |
| **Theme Tracker** | thematic | Tracks symbols and motifs; flags when theme is *announced* rather than *felt* |
| **Worldbuilder** | setting | Technology consistency, location logic, rules of the world |
| **Emotional Barometer** | emotional arc | Whether feelings are earned and arcs progress without rushing or dragging |
| **Foreshadow Keeper** | callbacks | Tracks setups and payoffs — what's planted, what still needs harvesting |
| **Sensitivity Reader** | sensitivity | Flags potentially harmful representation; advises, never mandates |
| **Research Maven** | research | Verifies real-world facts and technical/scientific plausibility |
| **Props Master** | object tracking | Inventory of weapons, vehicles, clothing, significant items and their state |
| **Quote Curator** | marketing | Identifies quotable, standalone-strong passages for promotion |
| **Synopsis Writer** | summary | Summaries and blurbs at every length, from one-line hook to chapter breakdown |

### Lane discipline

Every role declares, in machine-readable form, exactly what it may touch:

```yaml
can_read:     [manuscripts, character_data, world_data, timelines]
can_write:    [continuity_flags, error_reports]
cannot_write: [manuscript_prose, character_voice]
```

If a role notices a problem **outside** its lane, it must flag it and stop — never act
on it. ("Outside my lane — flagging for the Worldbuilder.") This prevents *lane creep*:
agents opining with false confidence beyond their expertise.

### Standard output format

Every crew report is structured identically, so the Director can scan consistently:

```
## [Role] Report
### Context        — what was checked
### Findings       — what was discovered (with source citations)
### Recommendations— specific, actionable suggestions
### Lane Notes     — out-of-lane observations escalated, not acted on
### Log Entry      — role · action type · target · status
```

---

## 5. The Enforcer — The Process Gate

The Enforcer is a **meta-agent**. It sits between the working agents and the Director
and reviews **process, not creativity**.

It does **not** judge whether prose is good, whether a voice rings true, or whether a
suggestion improves the story. It judges only whether the agent **followed protocol**.

Every agent output is checked against five criteria:

1. **Query log present** — Did the agent read its sources before making claims?
2. **Domain declared** — Did it state its role and lane up front?
3. **Source attribution** — Is every factual claim cited (`file:line` or `file:section`)?
4. **Lane discipline** — Were out-of-lane issues deferred rather than acted on?
5. **Mode declared** — (Character Stewards only) Was the operating mode stated?

The Enforcer returns one of three verdicts:

- **APPROVED** → output proceeds to the Director.
- **REJECTED** → the agent must redo the work correctly (e.g. *"Line 47 asserts a
  character trait but the steward file was never queried"*).
- **FLAGGED** → an ambiguous situation is escalated for a Director decision.

**Rationale:** the Director's time is finite. The Enforcer pre-validates process so the
author reviews *substance*, not whether the homework was done.

```
Agent works → produces output + process log → ENFORCER
                                                 │
                              ┌──────────────────┼──────────────────┐
                          APPROVED            REJECTED            FLAGGED
                              │                   │                  │
                       Director reviews    Agent redoes      Director decides
```

---

## 6. Character Stewards (Adjacent Subsystem)

Alongside the Production Crew runs a parallel set of **Character Stewards** — one per
major character. A Steward is the dedicated guardian of a single character's voice,
psychology, and behavioral tics (e.g. *Standard* speaks flat and observational and
never uses machine vocabulary; *Hendricks* carries a precise two-bullet contract).

Stewards operate in one of three declared **modes**:

- **VALIDATION** — reviewing existing text for voice consistency
- **GENERATION** — producing new dialogue or interiority
- **CONSULTATION** — answering questions about the character

They pass through the same Enforcer gate as the Production Crew, with the additional
mode-declaration check.

---

## 7. How a Task Runs (End to End)

1. **Spawn** — The Director (or orchestrating session) spawns an agent for a defined
   task. The spawn prompt *must* embed the Enforcer Protocol — agents never run "free."
2. **Query** — The agent reads the relevant canon files and chapter text, logging each
   read.
3. **Work** — The agent performs its task strictly within its lane.
4. **Report** — It produces output in the standard format, with citations and a
   process log.
5. **Validate** — The Enforcer audits the process and returns APPROVED / REJECTED /
   FLAGGED.
6. **Review** — Only validated output reaches the Director, who makes the final call.

A spawn prompt is non-negotiably required to include a **Query Log**, **Domain
Declaration**, **Source Attribution**, **Lane Discipline** clause, and a closing
**Process Validation** checklist.

---

## 8. RLM Principle — Division of Labor

The system follows a clean split between deterministic and semantic work:

- **Code handles:** file search, YAML queries, metrics, pattern matching, logging.
- **The LLM handles:** semantic evaluation, voice judgment, quality assessment.

Structural retrieval is never left to the model's memory; creative judgment is never
hard-coded. Each does what it is reliable at.

---

## 9. Repository Map (For the Consultant)

```
_tools/agents/
├── README.md                       — developer-facing index
├── PRODUCTION_CREW_MANUAL.md        — this document
└── templates/
    ├── meta/
    │   └── enforcer.md              — Enforcer full specification
    ├── production_crew/
    │   ├── _BASE_TEMPLATE.md         — template all 13 roles inherit
    │   └── <role>.md                 — one file per editorial role
    └── character_stewards/
        ├── _BASE_STEWARD.md
        └── steward_<character>.md    — one file per character
```

Related documentation worth reviewing:

- `RESONANCE/data/MANUAL.md` — the canon (YAML) data system manual
- `SYSTEM_WORKFLOW.md` — session workflow and the Active Query Protocol
- `_tools/manuscript_analysis/ANALYSIS_MANUAL.md` — large-scale manuscript analysis

---

## 10. Design Principles in One Page

- **Query before claiming.** No fact asserted from memory; everything is cited.
- **Stay in your lane.** Narrow domains, explicit permissions, deferral over creep.
- **Process is gated.** The Enforcer validates method before the author sees output.
- **The author decides.** Agents recommend; the Director holds final judgment.
- **Canon is the source of truth.** Version-controlled files outrank any chat history.
- **Separate the deterministic from the semantic.** Code retrieves; the model judges.

---

*Query before claiming. Cite what you reference. Stay in your lane. The Enforcer is watching.*
