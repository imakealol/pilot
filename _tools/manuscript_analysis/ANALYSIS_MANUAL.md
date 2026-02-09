# RESONANCE Manuscript Analysis System

## Manual for LLM Contributors

This document explains the manuscript analysis methodology, architecture, and how to contribute. Read this before running or extending the system.

---

## 1. PHILOSOPHY

### 1.1 The Problem

Traditional manuscript analysis fails at scale because:
- **Context overflow**: A novel is ~150k tokens. No single pass can hold it all.
- **Lost in the middle**: Models lose attention to content in the middle of long contexts.
- **Hallucination risk**: Without verifiable external state, models confabulate details.
- **Scope creep**: Agents asked to "find everything" find nothing well.

### 1.2 The Solution: RLM Principles

This system applies **Recursive Language Model** principles:

1. **Treat the manuscript as external environment** — Query it, don't memorize it
2. **Codify before analyzing** — Structured data > raw prose for cross-reference
3. **Single-focus discipline** — One agent, one question, one pass
4. **Cite or it didn't happen** — Every finding must reference source material
5. **Stay in your lane** — Agents reject out-of-scope observations

### 1.3 The Codex Advantage

Raw chapter: ~4,000 tokens
Codified chapter: ~500 tokens

Full book raw: ~140,000 tokens (impossible to load)
Full book codified: ~50,000 tokens (fits in context)

Codification enables true cross-chapter analysis in a single pass.

---

## 2. ARCHITECTURE

```
RESONANCE/
├── chapters/                    # Raw manuscript prose
│   └── RESONANCE_CH{N}_{TITLE}.txt
├── data/
│   ├── CHAPTER_MANIFEST.yaml    # Canonical file mapping
│   ├── CHARACTERS.yaml          # Character reference data
│   ├── PROPS.yaml               # Object/prop tracking
│   └── codex/                   # Codified chapters
│       └── ch{NN}_codex.yaml    # Structured extraction per chapter
└── context/                     # World-building references
    └── GEOMETRY_VISUAL_LANGUAGE.md

_tools/manuscript_analysis/
├── schema/
│   └── chapter_codex.yaml       # Codification schema
├── codify_chapter.py            # Chapter → structured YAML
├── codex_analyzer.py            # Analysis engine
├── chain_runner.py              # Legacy chain-based analysis
├── codex_reports/               # Analysis output
│   └── {agent}_{focus}/
│       └── ch{NN}_report.yaml
└── ANALYSIS_MANUAL.md           # This file
```

---

## 3. THE CODEX

### 3.1 What Is a Codex?

A codex is a structured YAML representation of a chapter containing:

```yaml
chapter: 38
title: "THE BEACONS"
pov: Hendricks
wordcount: 4200

time:
  relative_to_previous: "immediate"
  time_of_day: "night"
  duration: "hours"

locations:
  - name: "Sovereignty perimeter"
    first_appearance: false

characters_present:
  - name: Hendricks
    role: pov
    entrance: "already present"
    exit: "chapter ends"

character_states:
  Hendricks:
    physical: "functional, fatigued"
    emotional: "determined, grief-suppressed"
    location: "approaching beacon"
    knowledge_delta:
      - "Beacon locations confirmed"
    inventory:
      - item: "revolver"
        status: "still has"

objects:
  - name: "revolver"
    status: "tracked"
    holder: "Hendricks"
    significance: "5 bullets remaining"

key_events:
  - "Hendricks reaches beacon perimeter"
  - "Standard provides navigation"
  - "Elena's wound worsens"

setups:
  - element: "Elena's deteriorating condition"
    payoff_chapter: 43

payoffs:
  - element: "Beacon signal from CH35"
    setup_chapter: 35

open_threads:
  - "Will Elena survive?"
  - "What happens when they reach the beacon?"
```

### 3.2 Codex Schema

See `schema/chapter_codex.yaml` for the complete schema definition.

Key sections:
- **Temporal**: When does this happen relative to other chapters?
- **Spatial**: Where are we? New locations?
- **Characters**: Who's present? What state are they in?
- **Objects**: What props matter? Where are they?
- **Plot**: Key events, revelations, setups, payoffs
- **Craft**: Tone, pacing, scene structure
- **Continuity**: Flags for cross-chapter verification

### 3.3 Generating Codex Files

```bash
# Single chapter
python3 codify_chapter.py <api_key> 38

# Range of chapters
python3 codify_chapter.py <api_key> 1-44
```

Output: `RESONANCE/data/codex/ch{NN}_codex.yaml`

### 3.4 Reviewing Codex Files

**CRITICAL**: Codex files should be human-reviewed before analysis runs.

Common extraction errors to check:
- Misidentified POV character
- Missing significant objects
- Wrong character state (especially injuries)
- Timeline misinterpretation
- Missing key events

The codex is the source of truth for analysis. Errors here propagate to all findings.

---

## 4. AGENTS

### 4.1 Agent Categories

**STRUCTURE AGENTS** — Load full codex, analyze patterns across chapters
- `continuity_editor`: Timeline, character state, world rules, object tracking
- `foreshadow_keeper`: Setups, payoffs, dangling threads, telegraph risk
- `worldbuilder`: Technology, locations, factions, sensory consistency

**PROSE AGENTS** — Load codex summary + raw prose, analyze writing quality
- `prose_doctor`: Style violations, density, show vs tell, fragments
- `tension_architect`: Scene stakes, chapter hooks, pacing valleys, fatigue
- `emotional_barometer`: Earned beats, reader arc, catharsis, payoff weight

**CHARACTER STEWARDS** — Load codex summary + raw prose, protect character voice
- `steward_standard`: Voice, knowledge, arc, relationships
- `steward_hendricks`: Voice, knowledge, arc, relationships
- `steward_elena`: Voice, knowledge, arc, relationships
- `steward_four`: Voice, knowledge, arc, relationships

### 4.2 Single-Focus Discipline

Each agent has multiple focuses but runs **ONE FOCUS PER PASS**.

```
WRONG: "Find all continuity issues"
RIGHT: "Find timeline issues only. Ignore character state, world rules, objects."
```

This prevents:
- Scope creep
- Shallow findings
- Lane violations
- Context overload

### 4.3 Lane Discipline

Agents MUST stay in their lane:

| Agent | In Lane | Out of Lane |
|-------|---------|-------------|
| continuity_editor (timeline) | "CH5 says 3 days passed but CH6 says 2" | "The prose here is purple" |
| prose_doctor (density) | "This paragraph is overpacked" | "The timeline doesn't add up" |
| steward_elena (voice) | "Elena wouldn't use this word" | "This plot point is weak" |

If an agent notices something out of lane, they note it in `carry_forward` for another agent but do NOT report it as a finding.

---

## 5. RUNNING ANALYSIS

### 5.1 Basic Command

```bash
python3 codex_analyzer.py <api_key> <agent> <focus> --chapters <range>
```

Examples:
```bash
# Timeline analysis, full book
python3 codex_analyzer.py $API_KEY continuity_editor timeline --chapters 1-44

# Voice analysis for Elena, Act III only
python3 codex_analyzer.py $API_KEY steward_elena voice --chapters 30-44

# Pacing analysis, finale sequence
python3 codex_analyzer.py $API_KEY tension_architect pacing_valleys --chapters 38-44
```

### 5.2 Output Structure

Each run produces:
```
codex_reports/{agent}_{focus}/
├── ch01_report.yaml    # Structured findings
├── ch01_raw.txt        # Raw LLM output
├── ch02_report.yaml
├── ch02_raw.txt
...
```

### 5.3 Rate Limits

The system uses 90-second delays between chapters to respect API rate limits (30k tokens/minute).

Full book analysis (44 chapters): ~66 minutes per agent-focus.

### 5.4 Recommended Run Order

**Pass 1: Fact & Voice**
1. `continuity_editor` — all 4 focuses
2. `worldbuilder` — all 4 focuses
3. `foreshadow_keeper` — all 4 focuses
4. Character stewards — voice focus for each

**Pass 2: Craft & Pacing**
1. `prose_doctor` — all 4 focuses
2. `tension_architect` — all 4 focuses
3. `emotional_barometer` — all 4 focuses

**Pass 3: Targeted**
- Re-run specific agent-focus combinations based on Pass 1-2 findings

---

## 6. REPORT FORMAT

### 6.1 Finding Structure

```yaml
findings:
  - id: CE-TL-38-001          # Agent-Focus-Chapter-Number
    type: issue               # issue | observation | verified
    severity: major           # critical | major | minor | info | clean
    location: "lines 45-52"   # Where in chapter
    content: "Timeline contradiction with CH35"
    evidence: "Quote from text showing the issue"
    cross_reference: 35       # Chapter number if referencing another
```

### 6.2 Finding ID Convention

`{AGENT_PREFIX}-{FOCUS_PREFIX}-{CHAPTER}-{NUMBER}`

Agent prefixes:
- CE = continuity_editor
- WB = worldbuilder
- FK = foreshadow_keeper
- PD = prose_doctor
- TA = tension_architect
- EB = emotional_barometer
- SS = steward_standard
- SH = steward_hendricks
- SE = steward_elena
- SF = steward_four

Focus prefixes:
- TL = timeline
- CS = character_state
- WR = world_rules
- OT = object_tracking
- (etc.)

### 6.3 Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| critical | Breaks story logic | Must fix before publication |
| major | Noticeable problem | Should fix |
| minor | Polish issue | Fix if time permits |
| info | Observation, not issue | Consider |
| clean | Verified correct | No action needed |

### 6.4 Carry Forward

Each report includes `carry_forward` — facts that subsequent analyses should know:

```yaml
carry_forward:
  - "Elena's wound was established in CH38, worsens through CH39-42"
  - "Hendricks has 5 bullets at chapter end (fired 1 in this chapter)"
  - "Standard's signal is degrading — established cause for CH42 events"
```

### 6.5 Self-Check

Every report includes a self-check:

```yaml
self_check:
  stayed_in_lane: true      # Did agent stick to focus?
  findings_cited: true      # Does every finding have evidence?
```

If either is false, the report should be reviewed for quality.

---

## 7. CONTRIBUTING

### 7.1 Adding a New Agent

1. Add to `AGENT_FOCUSES` dict in `codex_analyzer.py`:
```python
AGENT_FOCUSES = {
    ...
    "new_agent": ["focus1", "focus2", "focus3", "focus4"],
}
```

2. Add to appropriate category list:
```python
STRUCTURE_AGENTS = [..., "new_agent"]  # or PROSE_AGENTS
```

3. Add instructions in `get_agent_instructions()`:
```python
elif agent == "new_agent":
    if focus == "focus1":
        return """Instructions for this focus..."""
```

### 7.2 Adding a New Focus

1. Add to agent's focus list in `AGENT_FOCUSES`
2. Add instruction block in `get_agent_instructions()`

### 7.3 Modifying the Codex Schema

1. Edit `schema/chapter_codex.yaml`
2. Re-run codification on affected chapters
3. Update any agent instructions that reference changed fields

### 7.4 Quality Standards

All contributions should:
- Maintain single-focus discipline
- Include lane boundaries in instructions
- Require evidence citation
- Use consistent finding ID format
- Include self-check validation

---

## 8. INTERPRETING RESULTS

### 8.1 Cross-Referencing Findings

When multiple agents flag the same chapter/location:
- Likely a real issue
- Check if findings are complementary or contradictory
- Prioritize by severity

### 8.2 False Positives

Common causes:
- Agent misread codex data
- Codex extraction error
- Agent exceeded lane boundaries
- Subjective judgment disguised as issue

Mitigation:
- Verify against raw chapter text
- Check if codex is accurate
- Confirm finding matches agent's focus

### 8.3 Synthesis

After all passes complete, synthesize by:
1. Group findings by chapter
2. Group findings by severity
3. Identify patterns (same issue across chapters)
4. Prioritize fixes: critical → major → minor

---

## 9. QUICK REFERENCE

### Commands

```bash
# Codify chapters
python3 codify_chapter.py <api_key> 1-44

# Run analysis
python3 codex_analyzer.py <api_key> <agent> <focus> --chapters 1-44

# List agents
python3 codex_analyzer.py --list
```

### Files to Know

| File | Purpose |
|------|---------|
| `CHAPTER_MANIFEST.yaml` | Maps chapter numbers to files |
| `ch{NN}_codex.yaml` | Structured chapter data |
| `ch{NN}_report.yaml` | Analysis findings |
| `CHARACTERS.yaml` | Character reference |
| `PROPS.yaml` | Object tracking reference |

### Key Principles

1. **Codify first** — Never analyze raw prose without codex context
2. **One focus per pass** — Depth over breadth
3. **Cite everything** — No evidence = no finding
4. **Stay in lane** — Out-of-scope goes to carry_forward
5. **Trust the codex** — But verify it's accurate

---

## 10. TROUBLESHOOTING

### Rate Limit Errors (429)

Increase delay in `codex_analyzer.py`:
```python
time.sleep(120)  # Increase from 90 to 120 seconds
```

### YAML Parse Errors

Check `_raw` field in report for actual output. Common cause: unescaped quotes in evidence strings.

### Missing Cross-References

Verify codex files exist for referenced chapters. Structure agents need full codex loaded.

### Agent Exceeding Lane

Review instructions in `get_agent_instructions()`. Add explicit exclusions:
```
ONLY check X. Ignore Y, Z, and W.
```

---

*Last updated: 2026-01-17*
*System version: Codex Analyzer v1.0*
