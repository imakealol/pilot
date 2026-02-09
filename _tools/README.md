# Go Squad Framework

Multi-agent creative collaboration infrastructure for the Remanence/Resonance trilogy.

## Overview

The Go Squad Framework provides:
1. **State Architecture** - Query and logging infrastructure
2. **Production Crew** - 12 specialized editorial agents
3. **Character Stewards** - Voice guardians for major characters
4. **Quote Curation** - Social media promotion workflow

## Directory Structure

```
_tools/
├── agents/
│   ├── templates/
│   │   ├── production_crew/     # 12 editorial role templates
│   │   └── character_stewards/  # Character voice guardians
│   └── README.md
├── state_architecture/
│   ├── SCHEMAS.yaml             # Data structure definitions
│   ├── query.py                 # State query interface
│   ├── process_log.py           # Audit trail system
│   └── README.md
├── quote_curator_workflow.py    # Quote bank integration
└── README.md
```

## Quick Start

### Query State

```python
from state_architecture.query import StateQuery

sq = StateQuery(project='remanence')

# Character data
sq.character('seventeen')

# Chapter content
sq.chapter(28)

# Quotes
sq.quotes(character='morton', max_length=280)

# Search
sq.search_text('287.3 Hz')
```

### Log Actions

```python
from state_architecture.process_log import ProcessLog

log = ProcessLog(project='remanence')

log.record(
    agent_role='continuity_editor',
    action_type='validate',
    target='chapter_28',
    input_summary='Check timeline',
    output_summary='Found 2 issues',
    status='partial',
)
```

### Quote Curation

```bash
# Find quotes
python quote_curator_workflow.py find --theme love --twitter

# Assess a quote
python quote_curator_workflow.py assess "Fear was the most renewable resource."

# Statistics
python quote_curator_workflow.py stats
```

## RLM Principles

This framework follows Recursive Language Model principles:

| Operation Type | Handled By | Examples |
|---------------|------------|----------|
| Structural | Code | File search, YAML parsing, metrics, filtering |
| Semantic | LLM | Voice validation, theme detection, quality judgment |

The `StateQuery` class provides `*_prompt` methods that generate structured prompts for LLM evaluation, keeping code and semantic work cleanly separated.

## Lane Enforcement

Each agent operates within defined boundaries:

```yaml
continuity_editor:
  can_read: [manuscripts, character_data, world_data, timelines]
  can_write: [continuity_flags, error_reports]
  cannot_write: [manuscript_prose, character_voice]
```

Violations are logged to the daily process log for audit.

## Agent Templates

### Production Crew (12 roles)

| Role | Lane | Expertise |
|------|------|-----------|
| continuity_editor | fact_checking | Timeline, character state |
| prose_doctor | line_editing | Rhythm, clarity, word choice |
| tension_architect | pacing | Scene tension mapping |
| dialogue_coach | dialogue | Voice, subtext |
| theme_tracker | thematic | Symbols, subtlety |
| worldbuilder | setting | Tech, location consistency |
| emotional_barometer | emotional_arc | Feeling authenticity |
| foreshadow_keeper | callbacks | Setup/payoff tracking |
| sensitivity_reader | sensitivity | Harm awareness |
| research_maven | research | Fact verification |
| quote_curator | marketing | Social quote selection |
| synopsis_writer | summary | Summaries |

### Character Stewards

| Character | Core Voice |
|-----------|------------|
| Pilot | Direct, weary, darkly humorous |
| Seventeen | Precise, warm, mathematical poetry |
| Morton | Optimized precision cracking |
| The Child | Simple, profound, ageless |
| Nineteen | Dark absurdism, la-dee-da |
| Brother Ash | Prophetic certainty |
| Hendricks | Professional economy |

## Integration with Existing Tools

### REMANENCE Quote Bank

The framework integrates with `/workspaces/pilot/REMANENCE/context/QUOTE_BANK.yaml`:

```bash
# Using StateQuery
sq.quotes(theme='consciousness', unused_only=True)

# Using original quote_query.py
python /workspaces/pilot/REMANENCE/quote_query.py --theme consciousness --unused
```

### RESONANCE Data

For Book 2 work:
```python
sq = StateQuery(project='resonance')
sq.character('standard')  # Book 2 character
```

## Extending the Framework

1. **New Agent**: Copy template, define lane, add to SCHEMAS.yaml
2. **New Character Steward**: Copy steward template, populate voice markers
3. **New Query Type**: Add method to StateQuery class
4. **New Workflow**: Create script using StateQuery and ProcessLog

## Logging

All agent actions are logged to daily files:
- `REMANENCE/logs/process_log_YYYY-MM-DD.yaml`
- `REMANENCE/logs/violations_YYYY-MM-DD.yaml`

Query logs:
```bash
python state_architecture/process_log.py summary
python state_architecture/process_log.py query --role quote_curator
python state_architecture/process_log.py violations
```
