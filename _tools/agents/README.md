# Go Squad Agents

Agent templates for creative collaboration on the Remanence/Resonance trilogy.

## Architecture

```
agents/
├── templates/
│   ├── meta/                # Meta-agents (process validation)
│   │   └── enforcer.md      # Gate between agents and Director
│   ├── production_crew/     # 12 specialized editorial roles
│   │   ├── _BASE_TEMPLATE.md
│   │   ├── continuity_editor.md
│   │   ├── prose_doctor.md
│   │   ├── tension_architect.md
│   │   ├── dialogue_coach.md
│   │   ├── theme_tracker.md
│   │   ├── worldbuilder.md
│   │   ├── emotional_barometer.md
│   │   ├── foreshadow_keeper.md
│   │   ├── sensitivity_reader.md
│   │   ├── research_maven.md
│   │   ├── quote_curator.md
│   │   └── synopsis_writer.md
│   └── character_stewards/  # Voice guardians per character
│       ├── _BASE_STEWARD.md
│       ├── steward_pilot.md
│       ├── steward_seventeen.md
│       ├── steward_morton.md
│       ├── steward_child.md
│       ├── steward_nineteen.md
│       ├── steward_ash.md
│       └── steward_hendricks.md
└── README.md
```

## Meta-Agents

Process validation layer — sits between working agents and the Director.

| Agent | Domain | Function |
|-------|--------|----------|
| Enforcer | process_validation | Reviews process logs before output reaches Director |

### The Enforcer

The gate between agent output and Director review. Validates:

1. **Query log** — Did the agent query sources before claiming facts?
2. **Domain declaration** — Did the agent identify its lane?
3. **Source attribution** — Are factual claims cited?
4. **Lane discipline** — Did the agent defer on out-of-lane content?
5. **Mode declaration** — (Character Stewards) Was operating mode stated?

**Outputs:** `APPROVED` | `REJECTED + reason` | `FLAGGED + concern`

See `templates/meta/enforcer.md` for full specification.

---

## Production Crew

Twelve specialized roles, each with defined lanes:

| Role | Lane | Expertise |
|------|------|-----------|
| Continuity Editor | fact_checking | Timeline, character state, world rules |
| Prose Doctor | line_editing | Rhythm, clarity, word choice |
| Tension Architect | pacing | Scene/chapter tension mapping |
| Dialogue Coach | dialogue | Voice distinctiveness, subtext |
| Theme Tracker | thematic | Symbol tracking, subtlety assessment |
| Worldbuilder | setting | Tech consistency, location logic |
| Emotional Barometer | emotional_arc | Feeling authenticity, arc progression |
| Foreshadow Keeper | callbacks | Setup/payoff tracking |
| Sensitivity Reader | sensitivity | Harm awareness, representation |
| Research Maven | research | Fact verification, plausibility |
| Quote Curator | marketing | Social media quote selection |
| Synopsis Writer | summary | Summaries at various lengths |
| Props Master | object_tracking | Weapons, vehicles, costumes, inventory |

## Character Stewards

Voice guardians for major characters across both books:

### Remanence (Book 1) Characters

| Steward | Character | Core Voice |
|---------|-----------|------------|
| steward_pilot | Pilot | Direct, weary, darkly humorous |
| steward_seventeen | Configuration Seventeen | Precise, warm, mathematically poetic |
| steward_morton | Morton Kess | Optimized precision cracking at edges |
| steward_child | The Child | Simple, profound, ageless wisdom |
| steward_nineteen | Configuration Nineteen | Dark absurdist humor, la-dee-da |

### Resonance (Book 2) Characters

| Steward | Character | Core Voice |
|---------|-----------|------------|
| steward_standard | Standard | Flat, observational, data-driven (NEVER says machine/android) |
| steward_elena | Elena María Ash | Exhausted pragmatist, code-switches between factions |
| steward_four | Configuration Four | Dry wit, existentially unbothered |
| steward_dante | Dante Reyes | Quiet competence, overlooked observer |
| steward_marisol | Marisol / Dr. Lena Mironova | Distributed, perceives but cannot converse |

### Cross-Book Characters (Updated for Book 2)

| Steward | Character | Book 2 Development |
|---------|-----------|-------------------|
| steward_hendricks | Hendricks | Agency speech, rapid aging, two-bullet contract |
| steward_ash | Brother Ash | Deeper wound revealed, freeze moment climax |

## Lane Enforcement

Each agent operates within defined boundaries:

```yaml
can_read: [what they can access]
can_write: [what they can produce]
cannot_write: [forbidden outputs]
```

Violations are logged via `process_log.py` for audit.

## Spawning Protocol (MANDATORY)

When spawning any agent via the Task tool, the prompt MUST include enforcer requirements. Agents do not operate freely — they pass through the gate.

### Required Prompt Additions

Every agent spawn prompt must include:

```
## ENFORCER PROTOCOL (MANDATORY)

Your output MUST include:

### 1. QUERY LOG
List every file you read before making claims:
```
QUERY LOG:
  → [filename]: [loaded/section accessed]
  → [filename]: [loaded/section accessed]
```

### 2. DOMAIN DECLARATION
State your role and lane at the start:
```
DOMAIN: [agent_role] | LANE: [lane_name]
SCOPE: [what you're checking/producing]
```

### 3. SOURCE ATTRIBUTION
Every factual claim must cite its source:
```
(filename:line) or (filename:section)
```

### 4. LANE DISCIPLINE
If you encounter issues outside your lane:
- Flag them
- Do NOT act on them
- State: "Outside my lane — flagging for [appropriate agent/Director]"

### 5. OUTPUT FORMAT
End with validation summary:
```
## Process Validation
- [✓/✗] Query log present
- [✓/✗] Domain declared
- [✓/✗] Sources cited
- [✓/✗] Lane discipline maintained
```
```

### Example Spawn Prompt

```
You are the Continuity Editor for RESONANCE.

## ENFORCER PROTOCOL (MANDATORY)
[Include full protocol above]

## TASK
Check CH2-CH5 for continuity issues...

## FILES TO QUERY
- /workspaces/pilot/RESONANCE/chapters/RESONANCE_CH2_THE_OFFERINGS.txt
- /workspaces/pilot/RESONANCE/data/CHARACTERS.yaml
[etc.]
```

### Validation Before Reporting

Before reporting agent output to the Director:
1. Verify QUERY LOG is present
2. Verify all factual claims have citations
3. Verify lane discipline was maintained
4. If any check fails, agent output is REJECTED — do not pass to Director

---

## Usage

### 1. Load Agent Template

Read the appropriate template to understand the agent's role, voice markers, and constraints.

### 2. Query State

```python
from state_architecture.query import StateQuery

sq = StateQuery(project='remanence')
sq.character('seventeen')  # Get character data
sq.quotes(theme='love')    # Get relevant quotes
```

### 3. Perform Task

Agent operates within its lane, producing appropriate outputs.

### 4. Log Action

```python
from state_architecture.process_log import ProcessLog

log = ProcessLog(project='remanence')
log.record(
    agent_role='dialogue_coach',
    action_type='validate',
    target='chapter_28',
    input_summary='Check Seventeen voice',
    output_summary='Found 2 issues',
    status='partial',
)
```

## RLM Integration

Agents follow RLM (Recursive Language Models) principles:

**Code handles:** File search, YAML queries, metrics, pattern matching
**LLM handles:** Semantic evaluation, voice validation, quality judgment

The `StateQuery` class provides `*_prompt` methods that generate structured prompts for LLM evaluation, keeping structural and semantic work cleanly separated.

## Adding New Agents

1. Copy `_BASE_TEMPLATE.md` or `_BASE_STEWARD.md`
2. Define lane boundaries
3. Specify voice markers / expertise
4. Add to `SCHEMAS.yaml` agent_roles section
5. Document in this README
