# State Architecture

Core infrastructure for the Go Squad Framework.

## Files

| File | Purpose |
|------|---------|
| `SCHEMAS.yaml` | Data structure definitions for all framework components |
| `query.py` | State query interface (code for structure, LLM prompts for semantics) |
| `process_log.py` | Audit trail and lane enforcement |

## Usage

### Query Interface

```python
from query import StateQuery

sq = StateQuery(project='remanence')

# Code-based queries (fast, deterministic)
sq.character('seventeen')
sq.chapter(28)
sq.quotes(character='morton', max_length=280, unused_only=True)
sq.search_text('287.3 Hz')
sq.word_count()

# LLM-augmented queries (returns prompts for semantic evaluation)
sq.voice_check_prompt('seventeen', '"I chose this."')
sq.theme_detect_prompt(passage)
sq.quote_assess_prompt(text)
```

### Process Logger

```python
from process_log import ProcessLog

log = ProcessLog(project='remanence')

# Record an action
log.record(
    agent_role='continuity_editor',
    action_type='validate',
    target='chapter_28',
    input_summary='Check timeline consistency',
    output_summary='Found 2 issues',
    status='partial',
)

# Check lane permissions
result = log.check_lane('prose_doctor', 'edit', 'manuscript_prose')
# {'allowed': True, 'reason': 'Lane allows writing manuscript_prose', ...}

# Query logs
log.query(agent_role='continuity_editor')
log.summary()
log.violations()
```

### CLI

```bash
# Query state
python query.py --project remanence character seventeen
python query.py quotes --character morton --twitter
python query.py search "287.3 Hz"
python query.py wordcount

# Query logs
python process_log.py summary
python process_log.py query --role continuity_editor
python process_log.py violations
python process_log.py check prose_doctor edit manuscript_prose
```

## RLM Principles

This architecture follows RLM (Recursive Language Models) principles:

**Code handles:**
- File search (glob, grep)
- YAML parsing and filtering
- Word counts and metrics
- Pattern matching (regex)
- Timeline calculations

**LLM handles:**
- Semantic matching ("Does this feel like X?")
- Voice validation ("Would character say this?")
- Theme detection ("What themes are present?")
- Quality judgment ("Is this quote standalone?")
- Suggestion generation ("How could this improve?")

The `*_prompt` methods return structured prompts for LLM evaluation, keeping the semantic work separate from the structural work.

## Lane Enforcement

Each agent role has defined boundaries:

```yaml
- id: continuity_editor
  lane: fact_checking
  can_read: [manuscripts, character_data, world_data, timelines]
  can_write: [continuity_flags, error_reports]
  cannot_write: [manuscript_prose, character_voice]
```

The `ProcessLog.check_lane()` method validates actions before execution, and violations are recorded for audit.
