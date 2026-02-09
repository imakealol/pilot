#!/usr/bin/env python3
"""
RESONANCE Manuscript Analysis - Codex-Aware Analyzer

Uses codified chapter data for efficient full-book analysis.
Two modes:
  - STRUCTURE: Load full codex (all chapters) + raw prose for current chapter
  - PROSE: Load codex summary + raw prose for current chapter

This replaces the chain approach for most analysis tasks.

Usage:
    python codex_analyzer.py <api_key> <agent> <focus> [--chapters 1-44]
    python codex_analyzer.py --list
"""

import anthropic
import argparse
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path("/workspaces/pilot")
RESONANCE_DIR = PROJECT_ROOT / "RESONANCE"
CHAPTERS_DIR = RESONANCE_DIR / "chapters"
DATA_DIR = RESONANCE_DIR / "data"
CODEX_DIR = DATA_DIR / "codex"
CONTEXT_DIR = RESONANCE_DIR / "context"
MANIFEST_PATH = DATA_DIR / "CHAPTER_MANIFEST.yaml"
OUTPUT_DIR = PROJECT_ROOT / "_tools" / "manuscript_analysis" / "codex_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Agent categories
STRUCTURE_AGENTS = [
    "continuity_editor",
    "foreshadow_keeper",
    "worldbuilder",
]

PROSE_AGENTS = [
    "prose_doctor",
    "tension_architect",
    "emotional_barometer",
    "steward_standard",
    "steward_hendricks",
    "steward_elena",
    "steward_four",
]

# Agent-Focus Matrix (same as chain_runner)
AGENT_FOCUSES = {
    "continuity_editor": ["timeline", "character_state", "world_rules", "object_tracking"],
    "worldbuilder": ["technology", "locations", "social_faction", "sensory"],
    "foreshadow_keeper": ["setups", "payoffs", "dangling_threads", "telegraph_risk"],
    "steward_standard": ["voice", "knowledge", "arc", "relationships"],
    "steward_hendricks": ["voice", "knowledge", "arc", "relationships"],
    "steward_elena": ["voice", "knowledge", "arc", "relationships"],
    "steward_four": ["voice", "knowledge", "arc", "relationships"],
    "prose_doctor": ["style_violations", "density", "show_vs_tell", "fragment_integrity"],
    "tension_architect": ["scene_stakes", "chapter_hooks", "pacing_valleys", "fatigue_risk"],
    "emotional_barometer": ["earned_beats", "reader_arc", "catharsis_placement", "payoff_weight"],
}


# ============================================================================
# LOADERS
# ============================================================================

def load_manifest() -> dict:
    """Load chapter manifest."""
    with open(MANIFEST_PATH) as f:
        return yaml.safe_load(f)


def load_full_codex(chapter_range: range = None) -> str:
    """Load all codified chapters as a single document."""
    manifest = load_manifest()
    chapters = chapter_range or range(1, 45)

    codex_text = []
    for ch_num in chapters:
        codex_path = CODEX_DIR / f"ch{ch_num:02d}_codex.yaml"
        if codex_path.exists():
            with open(codex_path) as f:
                content = f.read()
            codex_text.append(f"# CHAPTER {ch_num} CODEX\n{content}")

    return "\n\n---\n\n".join(codex_text)


def load_codex_summary(chapter_range: range = None) -> str:
    """Load condensed summary of codex (key fields only)."""
    manifest = load_manifest()
    chapters = chapter_range or range(1, 45)

    summaries = []
    for ch_num in chapters:
        codex_path = CODEX_DIR / f"ch{ch_num:02d}_codex.yaml"
        if codex_path.exists():
            with open(codex_path) as f:
                codex = yaml.safe_load(f)

            # Extract just key fields
            summary = {
                "chapter": ch_num,
                "title": codex.get("title"),
                "pov": codex.get("pov"),
                "locations": [loc.get("name") for loc in codex.get("locations", [])],
                "characters_present": [c.get("name") for c in codex.get("characters_present", [])],
                "key_events": codex.get("key_events", [])[:3],  # First 3 only
                "tone": codex.get("tone"),
                "open_threads": codex.get("open_threads", [])[:2],  # First 2 only
            }
            summaries.append(summary)

    return yaml.dump(summaries, default_flow_style=False, allow_unicode=True)


def load_chapter_raw(chapter_num: int) -> tuple[str, str]:
    """Load raw chapter prose."""
    manifest = load_manifest()
    if chapter_num not in manifest['chapters']:
        return f"CH{chapter_num}", ""

    chapter_info = manifest['chapters'][chapter_num]
    file_path = CHAPTERS_DIR / chapter_info['file']
    title = chapter_info['title']

    if file_path.exists():
        return title, file_path.read_text()
    return title, ""


def load_codex_for_chapter(chapter_num: int) -> dict:
    """Load codex for a specific chapter."""
    codex_path = CODEX_DIR / f"ch{chapter_num:02d}_codex.yaml"
    if codex_path.exists():
        with open(codex_path) as f:
            return yaml.safe_load(f)
    return {}


# ============================================================================
# AGENT PROMPTS
# ============================================================================

def get_structure_agent_prompt(agent: str, focus: str, full_codex: str, chapter_num: int, chapter_raw: str) -> str:
    """Build prompt for structure-focused agents (full codex + current chapter raw)."""

    # Agent-specific instructions
    instructions = get_agent_instructions(agent, focus)

    return f"""You are a manuscript analysis agent specializing in {agent.replace('_', ' ')}, focus: {focus}.

## YOUR ROLE
{instructions}

## FULL BOOK CODEX (Structured Data)
This contains structured metadata for ALL chapters. Use this for cross-chapter analysis.

{full_codex}

## CURRENT CHAPTER RAW PROSE (CH{chapter_num})
Analyze this chapter in detail, referencing the codex for context.

{chapter_raw}

## OUTPUT FORMAT
Return a YAML report with this structure:

```yaml
report:
  agent: {agent}
  focus: {focus}
  chapter: {chapter_num}
  findings:
    - id: <AGENT_PREFIX>-<FOCUS_PREFIX>-<CH>-<NUM>
      type: issue|observation|verified
      severity: critical|major|minor|info|clean
      location: <where in chapter>
      content: <what you found>
      evidence: <quote from text>
      cross_reference: <chapter number if referencing another chapter>
  carry_forward:
    - <key facts for future chapters>
  self_check:
    stayed_in_lane: true|false
    findings_cited: true|false
```
"""


def get_prose_agent_prompt(agent: str, focus: str, codex_summary: str, chapter_num: int, chapter_raw: str, chapter_codex: dict) -> str:
    """Build prompt for prose-focused agents (codex summary + current chapter raw + current chapter codex)."""

    instructions = get_agent_instructions(agent, focus)
    codex_yaml = yaml.dump(chapter_codex, default_flow_style=False, allow_unicode=True)

    return f"""You are a manuscript analysis agent specializing in {agent.replace('_', ' ')}, focus: {focus}.

## YOUR ROLE
{instructions}

## BOOK OVERVIEW (Codex Summary)
Condensed metadata for all chapters - use for context only.

{codex_summary}

## CURRENT CHAPTER CODEX (CH{chapter_num})
Structured data for this chapter:

{codex_yaml}

## CURRENT CHAPTER RAW PROSE (CH{chapter_num})
Analyze this text in detail.

{chapter_raw}

## OUTPUT FORMAT
Return a YAML report with this structure:

```yaml
report:
  agent: {agent}
  focus: {focus}
  chapter: {chapter_num}
  findings:
    - id: <AGENT_PREFIX>-<FOCUS_PREFIX>-<CH>-<NUM>
      type: issue|observation|verified
      severity: critical|major|minor|info|clean
      location: <line number or section>
      content: <what you found>
      evidence: <quote from text>
  carry_forward:
    - <key facts for future reference>
  self_check:
    stayed_in_lane: true|false
    findings_cited: true|false
```
"""


def get_agent_instructions(agent: str, focus: str) -> str:
    """Return focus-specific instructions for each agent."""

    # Continuity Editor instructions
    if agent == "continuity_editor":
        if focus == "timeline":
            return """Track temporal consistency. Flag:
- Time jumps that don't add up
- Events that contradict established timeline
- "How long ago" references that conflict
ONLY look for timeline issues. Ignore other continuity types."""
        elif focus == "character_state":
            return """Track character physical/emotional state across chapters. Flag:
- Injuries that heal too fast or are forgotten
- Emotional states that don't carry through
- Characters in impossible locations
ONLY track character state continuity. Ignore other issues."""
        elif focus == "world_rules":
            return """Track world/technology consistency. Flag:
- Technology that works differently than established
- World rules that contradict earlier chapters
- Inconsistent physics or capabilities
ONLY check world rule consistency. Ignore character/timeline issues."""
        elif focus == "object_tracking":
            return """Track significant objects/props. Flag:
- Objects appearing without explanation
- Objects lost or forgotten
- Inventory inconsistencies (weapons, documents, etc.)
ONLY track objects. Ignore other continuity types."""

    # Foreshadow Keeper instructions
    elif agent == "foreshadow_keeper":
        if focus == "setups":
            return """Catalog foreshadowing elements planted in this chapter. List:
- Details that seem significant but aren't yet explained
- Character statements that hint at future events
- Environmental details that could pay off later
ONLY identify setups. Don't track payoffs here."""
        elif focus == "payoffs":
            return """Identify payoffs to earlier setups. Reference:
- Which earlier setup is being paid off
- Whether the payoff feels earned
- If any payoffs feel rushed or underdeveloped
ONLY track payoffs. Reference setup chapters from codex."""
        elif focus == "dangling_threads":
            return """Find unresolved plot threads. Flag:
- Questions raised but not answered
- Character arcs left incomplete
- Mysteries that might be forgotten
ONLY identify danglers. Check against full codex for resolution."""
        elif focus == "telegraph_risk":
            return """Identify overly telegraphed moments. Flag:
- Foreshadowing that's too obvious
- Reveals that won't surprise anyone
- Heavy-handed hints
ONLY check for telegraph risk. Subjective judgment allowed."""

    # Worldbuilder instructions
    elif agent == "worldbuilder":
        if focus == "technology":
            return """Verify technology consistency. Check:
- Android/AI mechanics work as established
- Geometry abilities consistent
- Weapons, vehicles, communications logical
ONLY check technology. Ignore social/location issues."""
        elif focus == "locations":
            return """Track location consistency. Check:
- Physical descriptions match earlier mentions
- Geography makes sense
- Travel times are plausible
ONLY track locations. Ignore other world elements."""
        elif focus == "social_faction":
            return """Track faction/political consistency. Check:
- Faction motivations consistent
- Power dynamics make sense
- Alliances/conflicts track logically
ONLY check social dynamics. Ignore physical world."""
        elif focus == "sensory":
            return """Check sensory world consistency. Verify:
- The Geometry's visual language consistent
- Environmental effects track
- Sensory descriptions match world rules
ONLY check sensory details. Ignore plot/character."""

    # Character Steward instructions
    elif agent.startswith("steward_"):
        character = agent.replace("steward_", "").title()
        if focus == "voice":
            return f"""Verify {character}'s voice consistency. Check:
- Dialogue patterns match character
- Internal monologue sounds right
- Word choice, rhythm, verbal tics
ONLY check voice. Flag departures from established patterns."""
        elif focus == "knowledge":
            return f"""Track what {character} knows vs. shows. Flag:
- Character acting on info they shouldn't have
- Character forgetting something they learned
- Knowledge consistency across chapters
ONLY track knowledge. Ignore voice/emotional issues."""
        elif focus == "arc":
            return f"""Track {character}'s emotional/developmental arc. Check:
- Growth feels earned
- Regression makes sense
- Arc beats land properly
ONLY track arc progression. Ignore voice mechanics."""
        elif focus == "relationships":
            return f"""Track {character}'s relationships. Check:
- Relationship dynamics consistent
- Changes feel motivated
- Interactions match established dynamics
ONLY track relationships. Ignore individual characterization."""

    # Prose Doctor instructions
    elif agent == "prose_doctor":
        if focus == "style_violations":
            return """Flag style guide violations. Check against established voice:
- Passive voice overuse
- Adverb clutter
- Purple prose
- Inconsistent tense
ONLY flag style issues. Cite specific lines."""
        elif focus == "density":
            return """Evaluate prose density. Flag:
- Overpacked paragraphs
- Too much white space
- Information density imbalance
ONLY check density. Ignore style/content issues."""
        elif focus == "show_vs_tell":
            return """Flag telling vs. showing problems. Identify:
- Emotions stated rather than shown
- Exposition dumps
- Missed opportunities for dramatization
ONLY check show/tell balance. Cite specific passages."""
        elif focus == "fragment_integrity":
            return """Check sentence fragment usage. Flag:
- Fragments that don't land
- Fragment overuse
- Fragments breaking rhythm
ONLY evaluate fragments. Style choice, not grammar."""

    # Tension Architect instructions
    elif agent == "tension_architect":
        if focus == "scene_stakes":
            return """Evaluate scene-level stakes. Check:
- Are stakes clear?
- Do stakes escalate properly?
- Any scenes with unclear purpose?
ONLY evaluate stakes. Ignore prose quality."""
        elif focus == "chapter_hooks":
            return """Evaluate chapter openings and endings. Check:
- Does opening hook reader?
- Does ending create pull to next chapter?
- Any weak transitions?
ONLY check hooks. Ignore mid-chapter pacing."""
        elif focus == "pacing_valleys":
            return """Find pacing problems. Flag:
- Scenes that drag
- Rushed important moments
- Momentum killers
ONLY identify pacing valleys. Subjective judgment allowed."""
        elif focus == "fatigue_risk":
            return """Identify reader fatigue risks. Flag:
- Action sequences too long
- Emotional intensity without relief
- Repetitive beats
ONLY check fatigue risk. Consider reader experience."""

    # Emotional Barometer instructions
    elif agent == "emotional_barometer":
        if focus == "earned_beats":
            return """Evaluate if emotional beats are earned. Check:
- Is there sufficient buildup?
- Does the payoff match investment?
- Any unearned emotional moments?
ONLY evaluate earned beats. Ignore prose mechanics."""
        elif focus == "reader_arc":
            return """Track intended reader emotional journey. Check:
- What should reader feel at each point?
- Are transitions smooth?
- Any jarring emotional shifts?
ONLY track reader arc. Don't evaluate character arcs."""
        elif focus == "catharsis_placement":
            return """Evaluate catharsis timing. Check:
- Are release moments well-placed?
- Is tension held long enough?
- Any premature releases?
ONLY check catharsis timing. Ignore content quality."""
        elif focus == "payoff_weight":
            return """Evaluate payoff emotional weight. Check:
- Do big moments land with appropriate weight?
- Any anticlimactic resolutions?
- Is emotional investment respected?
ONLY evaluate payoff weight. Reference setups from codex."""

    return "Analyze this chapter according to your specialization."


# ============================================================================
# ANALYSIS ENGINE
# ============================================================================

def analyze_chapter(
    agent: str,
    focus: str,
    chapter_num: int,
    api_key: str,
    full_codex: str = None,
    codex_summary: str = None
) -> dict:
    """Run analysis on a single chapter."""

    # Load chapter data
    title, chapter_raw = load_chapter_raw(chapter_num)
    chapter_codex = load_codex_for_chapter(chapter_num)

    # Build prompt based on agent type
    if agent in STRUCTURE_AGENTS:
        if not full_codex:
            full_codex = load_full_codex()
        prompt = get_structure_agent_prompt(agent, focus, full_codex, chapter_num, chapter_raw)
    else:
        if not codex_summary:
            codex_summary = load_codex_summary()
        prompt = get_prose_agent_prompt(agent, focus, codex_summary, chapter_num, chapter_raw, chapter_codex)

    # Call API
    client = anthropic.Anthropic(api_key=api_key)

    print(f"  Analyzing CH{chapter_num}: {title}...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.content[0].text

    # Parse YAML from response
    import re
    yaml_content = raw_output.strip()
    if yaml_content.startswith("```"):
        yaml_content = re.sub(r'^```\w*\n?', '', yaml_content)
        yaml_content = re.sub(r'\n?```$', '', yaml_content)

    try:
        report = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        # Try to extract report structure even if YAML fails
        # Store raw for manual review
        report = {"_parse_error": str(e), "_raw": raw_output}
        # Attempt to extract key data via regex as fallback
        try:
            findings_match = re.findall(r'id: ([\w-]+)', yaml_content)
            if findings_match:
                report["_extracted_finding_ids"] = findings_match
        except:
            pass

    return report, raw_output


def run_analysis(
    agent: str,
    focus: str,
    chapters: List[int],
    api_key: str
) -> List[dict]:
    """Run analysis across specified chapters."""

    # Pre-load codex data for efficiency
    print("Loading codex data...")
    full_codex = load_full_codex() if agent in STRUCTURE_AGENTS else None
    codex_summary = load_codex_summary() if agent not in STRUCTURE_AGENTS else None

    results = []
    output_subdir = OUTPUT_DIR / f"{agent}_{focus}"
    output_subdir.mkdir(parents=True, exist_ok=True)

    for i, ch_num in enumerate(chapters):
        try:
            report, raw = analyze_chapter(
                agent, focus, ch_num, api_key,
                full_codex=full_codex,
                codex_summary=codex_summary
            )

            # Save report
            report_path = output_subdir / f"ch{ch_num:02d}_report.yaml"
            with open(report_path, 'w') as f:
                yaml.dump(report, f, default_flow_style=False, allow_unicode=True)

            raw_path = output_subdir / f"ch{ch_num:02d}_raw.txt"
            with open(raw_path, 'w') as f:
                f.write(raw)

            results.append({"chapter": ch_num, "status": "success", "report": report})
            print(f"  ✓ CH{ch_num} complete")

        except Exception as e:
            results.append({"chapter": ch_num, "status": "error", "error": str(e)})
            print(f"  ✗ CH{ch_num} failed: {e}")

        # Rate limit delay (except for last chapter)
        if i < len(chapters) - 1:
            print(f"  Waiting 90s for rate limit...")
            import time
            time.sleep(90)

    return results


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Codex-aware manuscript analyzer")
    parser.add_argument("api_key", nargs="?", help="Anthropic API key")
    parser.add_argument("agent", nargs="?", help="Agent name")
    parser.add_argument("focus", nargs="?", help="Focus area")
    parser.add_argument("--chapters", default="1-44", help="Chapter range (e.g., 1-44, 38-44)")
    parser.add_argument("--list", action="store_true", help="List available agents")

    args = parser.parse_args()

    if args.list:
        print("\nAVAILABLE AGENTS AND FOCUSES:")
        print("=" * 50)
        print("\nSTRUCTURE AGENTS (full codex loaded):")
        for agent in STRUCTURE_AGENTS:
            focuses = AGENT_FOCUSES.get(agent, [])
            print(f"  {agent}: {', '.join(focuses)}")
        print("\nPROSE AGENTS (codex summary + raw prose):")
        for agent in PROSE_AGENTS:
            focuses = AGENT_FOCUSES.get(agent, [])
            print(f"  {agent}: {', '.join(focuses)}")
        return

    if not all([args.api_key, args.agent, args.focus]):
        parser.print_help()
        return

    # Parse chapter range
    if "-" in args.chapters:
        start, end = map(int, args.chapters.split("-"))
        chapters = list(range(start, end + 1))
    else:
        chapters = [int(args.chapters)]

    # Validate agent/focus
    if args.agent not in AGENT_FOCUSES:
        print(f"Unknown agent: {args.agent}")
        return
    if args.focus not in AGENT_FOCUSES[args.agent]:
        print(f"Invalid focus '{args.focus}' for agent '{args.agent}'")
        print(f"Available: {AGENT_FOCUSES[args.agent]}")
        return

    print(f"\n{'='*60}")
    print(f"CODEX ANALYZER: {args.agent} / {args.focus}")
    print(f"Chapters: {chapters[0]}-{chapters[-1]} ({len(chapters)} chapters)")
    print(f"{'='*60}\n")

    results = run_analysis(args.agent, args.focus, chapters, args.api_key)

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    print(f"\n{'='*60}")
    print(f"COMPLETE: {success}/{len(chapters)} chapters analyzed")
    print(f"Output: _tools/manuscript_analysis/codex_reports/{args.agent}_{args.focus}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
