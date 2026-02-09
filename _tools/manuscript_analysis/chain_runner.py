#!/usr/bin/env python3
"""
RESONANCE Manuscript Analysis - Agent-First Chain Runner

Runs one agent-focus through all 7 chapters sequentially.
Each chapter run references previous chapter reports.
Clean chains, cumulative knowledge, enforcer-validated.

Usage:
    python chain_runner.py <api_key> <agent> <focus>

    # Run Continuity Editor timeline chain:
    python chain_runner.py $API_KEY continuity_editor timeline

    # List available agents/focuses:
    python chain_runner.py --list
"""

import anthropic
import argparse
import json
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path("/workspaces/pilot")
CHAPTERS_DIR = PROJECT_ROOT / "RESONANCE" / "chapters"
DATA_DIR = PROJECT_ROOT / "RESONANCE" / "data"
CONTEXT_DIR = PROJECT_ROOT / "RESONANCE" / "context"
STEWARDS_DIR = PROJECT_ROOT / "_tools" / "agents" / "templates" / "character_stewards"
OUTPUT_DIR = PROJECT_ROOT / "_tools" / "manuscript_analysis" / "chain_outputs"

CHAPTERS = [38, 39, 40, 41, 42, 43, 44]

# Agent-Focus Matrix
AGENT_FOCUSES = {
    # Pass 1: Fact & Voice
    "continuity_editor": ["timeline", "character_state", "world_rules", "object_tracking"],
    "worldbuilder": ["technology", "locations", "social_faction", "sensory"],
    "foreshadow_keeper": ["setups", "payoffs", "dangling_threads", "telegraph_risk"],
    "steward_standard": ["voice", "knowledge", "arc", "relationships"],
    "steward_hendricks": ["voice", "knowledge", "arc", "relationships"],
    "steward_elena": ["voice", "knowledge", "arc", "relationships"],
    "steward_four": ["voice", "knowledge", "arc", "relationships"],
    # Pass 2: Craft & Pacing
    "prose_doctor": ["style_violations", "density", "show_vs_tell", "fragment_integrity"],
    "tension_architect": ["scene_stakes", "chapter_hooks", "pacing_valleys", "fatigue_risk"],
    "emotional_barometer": ["earned_beats", "reader_arc", "catharsis_placement", "payoff_weight"],
}

# Rate limiting
DELAY_BETWEEN_RUNS = 60  # seconds


# ============================================================================
# FILE LOADERS
# ============================================================================

def load_chapter(chapter_num: int) -> tuple[str, str]:
    """Load a chapter file. Returns (filename, content)."""
    pattern = f"RESONANCE_CH{chapter_num}_*.txt"
    matches = list(CHAPTERS_DIR.glob(pattern))
    if matches:
        path = matches[0]
        return path.name, path.read_text()
    return f"CH{chapter_num}_NOT_FOUND", ""


def load_external_state(agent: str, focus: str) -> Dict[str, str]:
    """Load only the external state relevant to this agent-focus."""
    state = {}

    # Always load HANDOFF for context
    handoff_path = PROJECT_ROOT / "HANDOFF.md"
    if handoff_path.exists():
        state["HANDOFF.md"] = handoff_path.read_text()

    # Agent-specific state
    if agent == "continuity_editor":
        state["CHARACTERS.yaml"] = (DATA_DIR / "CHARACTERS.yaml").read_text() if (DATA_DIR / "CHARACTERS.yaml").exists() else ""
        state["ACT_III_MAPS.md"] = (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").read_text() if (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").exists() else ""
        if focus == "world_rules":
            geo_path = CONTEXT_DIR / "GEOMETRY_VISUAL_LANGUAGE.md"
            if geo_path.exists():
                state["GEOMETRY_VISUAL_LANGUAGE.md"] = geo_path.read_text()

    elif agent == "worldbuilder":
        props_path = DATA_DIR / "PROPS.yaml"
        if props_path.exists():
            state["PROPS.yaml"] = props_path.read_text()
        if focus in ["technology", "sensory"]:
            geo_path = CONTEXT_DIR / "GEOMETRY_VISUAL_LANGUAGE.md"
            if geo_path.exists():
                state["GEOMETRY_VISUAL_LANGUAGE.md"] = geo_path.read_text()
        if focus == "sensory":
            style_path = PROJECT_ROOT / "RESONANCE_STYLE_GUIDE.md"
            if style_path.exists():
                state["RESONANCE_STYLE_GUIDE.md"] = style_path.read_text()

    elif agent == "foreshadow_keeper":
        state["ACT_III_MAPS.md"] = (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").read_text() if (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").exists() else ""
        if focus == "telegraph_risk":
            state["CHARACTERS.yaml"] = (DATA_DIR / "CHARACTERS.yaml").read_text() if (DATA_DIR / "CHARACTERS.yaml").exists() else ""
            neg_path = CONTEXT_DIR / "NEGATIVE_CONSTRAINTS.md"
            if neg_path.exists():
                state["NEGATIVE_CONSTRAINTS.md"] = neg_path.read_text()

    elif agent.startswith("steward_"):
        char_name = agent.replace("steward_", "")
        steward_path = STEWARDS_DIR / f"steward_{char_name}.md"
        if steward_path.exists():
            state[f"steward_{char_name}.md"] = steward_path.read_text()
        state["CHARACTERS.yaml"] = (DATA_DIR / "CHARACTERS.yaml").read_text() if (DATA_DIR / "CHARACTERS.yaml").exists() else ""
        if focus in ["arc", "relationships"]:
            state["ACT_III_MAPS.md"] = (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").read_text() if (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").exists() else ""

    # Pass 2 agents
    elif agent == "prose_doctor":
        style_path = PROJECT_ROOT / "RESONANCE_STYLE_GUIDE.md"
        if style_path.exists():
            state["RESONANCE_STYLE_GUIDE.md"] = style_path.read_text()
        fight_path = PROJECT_ROOT / "fight_Guide.md"
        if fight_path.exists():
            state["fight_Guide.md"] = fight_path.read_text()

    elif agent == "tension_architect":
        state["ACT_III_MAPS.md"] = (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").read_text() if (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").exists() else ""
        style_path = PROJECT_ROOT / "RESONANCE_STYLE_GUIDE.md"
        if style_path.exists():
            state["RESONANCE_STYLE_GUIDE.md"] = style_path.read_text()

    elif agent == "emotional_barometer":
        state["ACT_III_MAPS.md"] = (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").read_text() if (PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md").exists() else ""
        state["CHARACTERS.yaml"] = (DATA_DIR / "CHARACTERS.yaml").read_text() if (DATA_DIR / "CHARACTERS.yaml").exists() else ""

    return state


def load_previous_reports(agent: str, focus: str, up_to_chapter: int) -> List[Dict]:
    """Load all previous chapter reports for this agent-focus chain."""
    reports = []
    chain_dir = OUTPUT_DIR / f"{agent}_{focus}"

    for ch in CHAPTERS:
        if ch >= up_to_chapter:
            break
        report_path = chain_dir / f"ch{ch}_report.yaml"
        if report_path.exists():
            with open(report_path) as f:
                reports.append(yaml.safe_load(f))

    return reports


# ============================================================================
# PROMPT GENERATION
# ============================================================================

def generate_prompt(
    agent: str,
    focus: str,
    chapter_num: int,
    chapter_content: str,
    external_state: Dict[str, str],
    previous_reports: List[Dict]
) -> str:
    """Generate the full prompt for this run."""

    # Base enforcement protocol
    enforcement = f"""
## ENFORCEMENT PROTOCOL

You are running as **{agent.upper()}** with focus **{focus.upper()}**.
This is Chapter {chapter_num} of 7 in your chain (CH38-44).

### Query Log Requirement
You must declare what you loaded:
- Current chapter: CH{chapter_num}
- Previous reports: {len(previous_reports)} loaded
- External state files: List them

### Citation Requirements
- New findings: Cite as `CH{chapter_num}:line_XX` or `CH{chapter_num}:paragraph_description`
- References to previous findings: Cite as `Report_CH{{num}}:{{finding_id}}`
- If claiming consistency with previous chapter, MUST cite the specific report finding

### Chain Integrity
{"This is CH38 (first in chain). No previous reports to reference." if chapter_num == 38 else f"You have {len(previous_reports)} previous report(s). You MUST reference relevant prior findings when they apply to current chapter."}

### Output Format
Produce a YAML report with this exact structure:
```yaml
report:
  agent: {agent}
  focus: {focus}
  chapter: {chapter_num}
  timestamp: [auto]

  query_log:
    chapter: CH{chapter_num}
    previous_reports: [list chapter numbers]
    external_state: [list files loaded]

  findings:
    - id: {agent[:2].upper()}-{focus[:2].upper()}-{chapter_num}-001
      type: issue | observation | verified
      severity: error | warning | info | clean
      location: "line X" or "paragraph description"
      content: "What was found"
      evidence: "Quote from text"
      chain_reference: null | "Report_CHXX:finding_id"

  carry_forward:
    - "Key items subsequent chapters must track"

  chain_citations:
    - report: CH{chapter_num - 1 if chapter_num > 38 else 'N/A'}
      finding_id: "referenced finding"
      relationship: "confirms | contradicts | extends"

  self_check:
    query_log_present: true/false
    findings_cited: true/false
    chain_referenced: true/false (N/A if CH38)
    stayed_in_lane: true/false
```
"""

    # Agent-specific instructions
    agent_instructions = get_agent_instructions(agent, focus)

    # Format previous reports for inclusion
    prev_reports_text = ""
    if previous_reports:
        prev_reports_text = "\n## PREVIOUS REPORTS IN THIS CHAIN\n\n"
        for rpt in previous_reports:
            prev_reports_text += f"### Report CH{rpt.get('report', {}).get('chapter', '?')}\n"
            prev_reports_text += f"```yaml\n{yaml.dump(rpt, default_flow_style=False)}\n```\n\n"

    # Format external state
    state_text = "\n## EXTERNAL STATE\n\n"
    for filename, content in external_state.items():
        # Truncate very large files
        if len(content) > 8000:
            content = content[:8000] + "\n\n[... truncated for length ...]"
        state_text += f"### {filename}\n```\n{content}\n```\n\n"

    # Assemble full prompt
    prompt = f"""# {agent.upper()} - {focus.upper()} FOCUS
## Chapter {chapter_num} Analysis

{enforcement}

{agent_instructions}

{prev_reports_text}

{state_text}

## CHAPTER {chapter_num} CONTENT

```
{chapter_content}
```

---

Now analyze this chapter according to your focus. Produce the YAML report.
"""

    return prompt


def get_agent_instructions(agent: str, focus: str) -> str:
    """Get specific instructions for this agent-focus combination."""

    instructions = {
        "continuity_editor": {
            "timeline": """
### Your Focus: TIMELINE
Track ONLY temporal consistency:
- Event sequence (does A happen before B?)
- Time references (hours, days - do they add up?)
- Parallel action timing
- Flashback/flash-forward alignment

DO NOT track: character locations, objects, injuries (other focuses)
""",
            "character_state": """
### Your Focus: CHARACTER STATE
Track ONLY character physical state:
- Location (where is each character?)
- Injuries (do wounds persist?)
- Physical condition (conscious, mobile, etc.)
- Knowledge boundaries (do they know only what they've learned?)

DO NOT track: timeline logic, objects, world rules (other focuses)
""",
            "world_rules": """
### Your Focus: WORLD RULES
Track ONLY rule consistency:
- Geometry behavior (does it work as established?)
- AI/consciousness mechanics (transfer, hot-swap, etc.)
- Physics of this world
- Established rules followed?

DO NOT track: specific objects, character locations (other focuses)
""",
            "object_tracking": """
### Your Focus: OBJECT TRACKING
Track ONLY important objects:
- Revolver (who has it, bullet count)
- Ceramic blade
- Standard's arms (which one?)
- Elena's implant
- Four's VTOL

DO NOT track: timeline, character state, world rules (other focuses)
""",
        },
        "worldbuilder": {
            "technology": """
### Your Focus: TECHNOLOGY
Track ONLY tech consistency:
- Weapons (bolt rounds, frequencies)
- Hot-swap mechanics
- Implant behavior
- Ship/VTOL systems

DO NOT track: locations, factions, atmosphere (other focuses)
""",
            "locations": """
### Your Focus: LOCATIONS
Track ONLY setting consistency:
- Geography (does layout make sense?)
- Distances (travel time logical?)
- Setting features (consistent descriptions?)

DO NOT track: technology, factions (other focuses)
""",
            "social_faction": """
### Your Focus: SOCIAL/FACTION
Track ONLY faction behavior:
- Carbonists (consistent methods?)
- Template 3s (consistent organization?)
- Resonant/Protectors (consistent goals?)

DO NOT track: technology, locations (other focuses)
""",
            "sensory": """
### Your Focus: SENSORY
Track ONLY environmental details:
- What does the Geometry look/sound/feel like?
- Consistent atmosphere?
- Sensory experience maintained?

DO NOT track: technology specifics, faction behavior (other focuses)
""",
        },
        "foreshadow_keeper": {
            "setups": """
### Your Focus: SETUPS
Track ONLY what's being planted:
- New information that might matter later
- Objects introduced
- Promises made (explicit or implicit)
- Character traits established

DO NOT track: payoffs, telegraph risks (other focuses)
""",
            "payoffs": """
### Your Focus: PAYOFFS
Track ONLY what's being paid off:
- Which setups get resolved?
- Are payoffs satisfying?
- Do payoffs match their setups?

Reference ACT_III_MAPS.md for known callbacks.

DO NOT track: new setups, telegraph risks (other focuses)
""",
            "dangling_threads": """
### Your Focus: DANGLING THREADS
Track ONLY unresolved elements:
- Setups not yet paid off
- Questions raised but not answered
- Promises not yet kept

DO NOT track: new setups, payoffs delivered (other focuses)
""",
            "telegraph_risk": """
### Your Focus: TELEGRAPH RISK
Track ONLY reveal protection:
- Does anything risk revealing Standard = Marisol?
- Clues that are too obvious?
- First-time reader would guess?

Severity:
- HIGH: First-time reader will guess
- MEDIUM: Attentive reader might guess
- LOW: Only visible on re-read (correct)

DO NOT track: general setups, payoffs (other focuses)
""",
        },
        # Pass 2: Craft & Pacing agents
        "prose_doctor": {
            "style_violations": """
### Your Focus: STYLE GUIDE VIOLATIONS
Check ONLY against RESONANCE_STYLE_GUIDE.md rules:
- Present tense maintained? (Resonance is present tense throughout)
- Fragments preserved? (Intentional fragments should NOT be "fixed")
- Em-dashes used correctly? (Syntactic pivots, not parentheticals)
- Body-as-inventory style? (Clinical listing of damage)
- Density maintained? (Compress, don't expand)

Flag: Passive voice, over-explanation, "telling" emotions

DO NOT track: plot, character, continuity (other agents)
""",
            "density": """
### Your Focus: DENSITY
Check ONLY prose compression:
- Could this sentence be shorter?
- Is information repeated unnecessarily?
- Are there filler words? (just, really, very, quite)
- Does dialogue have fat? (pleasantries, throat-clearing)
- Are beats earned or padded?

The style guide says: "Density is a feature, not a bug."

DO NOT track: style violations, show/tell, fragments (other focuses)
""",
            "show_vs_tell": """
### Your Focus: SHOW VS TELL
Check ONLY for telling that should be showing:
- Emotions labeled instead of demonstrated?
- "She felt sad" vs. showing sadness through action
- Thesis statements in dialogue? (Characters explaining theme)
- Over-explanation of character motivation?
- Reader told what to feel?

The style guide says: "Never explain emotions the reader should feel."

DO NOT track: density, style violations, fragments (other focuses)
""",
            "fragment_integrity": """
### Your Focus: FRAGMENT INTEGRITY
Check ONLY that intentional fragments are preserved:
- Fragments are a FEATURE of this prose style
- They should NOT be "fixed" into complete sentences
- Look for: fragments that feel awkward (may have been incorrectly completed)
- Look for: rhythmic breaks that should be fragments but aren't

The style guide says: "Fragment sentences for impact. Do not fix them."

DO NOT track: density, show/tell, style violations (other focuses)
""",
        },
        "tension_architect": {
            "scene_stakes": """
### Your Focus: SCENE STAKES
Check ONLY scene-level tension:
- Does each scene have clear stakes?
- What does the POV character want RIGHT NOW?
- What's preventing them from getting it?
- Is there consequence if they fail?
- Are stakes escalating or flat?

For CH38-44 (climax): Stakes should be at maximum.

DO NOT track: chapter hooks, pacing, fatigue (other focuses)
""",
            "chapter_hooks": """
### Your Focus: CHAPTER HOOKS
Check ONLY chapter endings:
- Does each chapter end with forward momentum?
- Is there a reason to turn the page?
- Cliffhangers, questions, promises?
- Or does the chapter end flat?

For CH38-44: Every chapter should DEMAND the next.

DO NOT track: scene stakes, pacing, fatigue (other focuses)
""",
            "pacing_valleys": """
### Your Focus: PACING VALLEYS
Check ONLY for momentum drops:
- Are there multiple slow beats in a row?
- Does action stop for too long?
- Exposition dumps that kill momentum?
- Reflection scenes that go on too long?

For CH38-44 (climax): Valleys should be brief or nonexistent.

DO NOT track: scene stakes, chapter hooks, fatigue (other focuses)
""",
            "fatigue_risk": """
### Your Focus: FATIGUE RISK
Check ONLY for reader exhaustion potential:
- Too many action beats without rest?
- Emotional intensity sustained too long?
- Same type of scene repeated?
- Reader needs a breath but doesn't get one?

Balance: Climax needs intensity BUT readers need micro-rests.

DO NOT track: scene stakes, chapter hooks, pacing valleys (other focuses)
""",
        },
        "emotional_barometer": {
            "earned_beats": """
### Your Focus: EARNED BEATS
Check ONLY if emotional moments are earned:
- Has the relationship been built to support this payoff?
- Has the character's journey justified this emotion?
- Does the reader have enough context to feel this?
- Or is the story TELLING us to feel without EARNING it?

Key beats in CH38-44:
- Four's sacrifice (CH42) — earned?
- Standard/Marisol reveal (CH43) — earned?
- Elena/Marisol reunion (CH43) — earned?
- Hendricks shooting Standard (CH43) — earned?

DO NOT track: reader arc, catharsis, payoff weight (other focuses)
""",
            "reader_arc": """
### Your Focus: READER ARC
Check ONLY the reader's emotional journey:
- What should the reader feel at each point?
- Is that feeling achieved?
- Are there emotional whiplash moments (too fast)?
- Are there dead spots (reader disengaged)?

Map the intended reader journey through CH38-44.

DO NOT track: earned beats, catharsis, payoff weight (other focuses)
""",
            "catharsis_placement": """
### Your Focus: CATHARSIS PLACEMENT
Check ONLY where release happens:
- Where are the cathartic moments?
- Are they placed correctly (after sufficient tension)?
- Is there premature release (catharsis before it's earned)?
- Is there delayed release (tension held too long)?

For CH38-44: Primary catharsis should be CH43 (the door opens).

DO NOT track: earned beats, reader arc, payoff weight (other focuses)
""",
            "payoff_weight": """
### Your Focus: PAYOFF WEIGHT
Check ONLY if payoffs match setup weight:
- Big setups need big payoffs
- Small setups need proportional payoffs
- Overdelivering on small setups = wasted energy
- Underdelivering on big setups = reader disappointment

Key payoffs in CH38-44:
- Standard = Marisol (MASSIVE setup, needs MASSIVE payoff)
- Bullet 6 (book-long setup)
- Four's "engine warm" callback
- "It's okay" echo from CH1

DO NOT track: earned beats, reader arc, catharsis (other focuses)
""",
        },
    }

    # Character steward instructions (shared pattern)
    if agent.startswith("steward_"):
        char_name = agent.replace("steward_", "").upper()
        steward_instructions = {
            "voice": f"""
### Your Focus: {char_name} VOICE
Track ONLY voice consistency:
- Speech patterns (register, vocabulary)
- Internal monologue style
- Forbidden words (check steward file)
- Characteristic expressions

DO NOT track: what they know, arc, relationships (other focuses)
""",
            "knowledge": f"""
### Your Focus: {char_name} KNOWLEDGE
Track ONLY knowledge boundaries:
- What has this character learned on-page?
- Do they act on info they shouldn't have?
- Key secrets: Who knows what when?

DO NOT track: voice, arc, relationships (other focuses)
""",
            "arc": f"""
### Your Focus: {char_name} ARC
Track ONLY emotional progression:
- Are they where they should be emotionally?
- Is growth/change earned?
- Arc beats in correct sequence?

Reference ACT_III_MAPS.md for character arcs.

DO NOT track: voice, knowledge, relationships (other focuses)
""",
            "relationships": f"""
### Your Focus: {char_name} RELATIONSHIPS
Track ONLY relationship dynamics:
- How does this character relate to others?
- Do interactions match documented status?
- Any relationship shifts - are they earned?

DO NOT track: voice, knowledge, arc (other focuses)
""",
        }
        return steward_instructions.get(focus, "")

    return instructions.get(agent, {}).get(focus, "")


# ============================================================================
# CHAIN EXECUTION
# ============================================================================

def run_chapter(
    client: anthropic.Anthropic,
    agent: str,
    focus: str,
    chapter_num: int,
    external_state: Dict[str, str],
    previous_reports: List[Dict],
    model: str = "claude-sonnet-4-20250514"
) -> Dict[str, Any]:
    """Run analysis on a single chapter."""

    # Load chapter
    chapter_file, chapter_content = load_chapter(chapter_num)

    if not chapter_content:
        return {
            "status": "error",
            "error": f"Chapter {chapter_num} not found"
        }

    # Generate prompt
    prompt = generate_prompt(
        agent, focus, chapter_num,
        chapter_content, external_state, previous_reports
    )

    print(f"    Prompt size: {len(prompt)} chars (~{len(prompt)//4} tokens)")

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.content[0].text

        # Try to parse YAML from response
        report = parse_yaml_report(output)

        return {
            "status": "success",
            "raw_output": output,
            "report": report,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def parse_yaml_report(output: str) -> Optional[Dict]:
    """Extract and parse YAML report from model output."""
    # Try to find YAML block
    import re

    # Look for ```yaml ... ``` block
    yaml_match = re.search(r'```yaml\s*\n(.*?)\n```', output, re.DOTALL)
    if yaml_match:
        try:
            return yaml.safe_load(yaml_match.group(1))
        except:
            pass

    # Try parsing the whole output as YAML
    try:
        return yaml.safe_load(output)
    except:
        pass

    # Return None if parsing fails
    return None


def save_chapter_report(agent: str, focus: str, chapter_num: int, result: Dict):
    """Save chapter report to chain directory."""
    chain_dir = OUTPUT_DIR / f"{agent}_{focus}"
    chain_dir.mkdir(parents=True, exist_ok=True)

    # Save parsed report as YAML
    if result.get("report"):
        report_path = chain_dir / f"ch{chapter_num}_report.yaml"
        with open(report_path, 'w') as f:
            yaml.dump(result["report"], f, default_flow_style=False, allow_unicode=True)

    # Save raw output
    raw_path = chain_dir / f"ch{chapter_num}_raw.txt"
    with open(raw_path, 'w') as f:
        f.write(result.get("raw_output", result.get("error", "No output")))

    # Save metadata
    meta_path = chain_dir / f"ch{chapter_num}_meta.json"
    with open(meta_path, 'w') as f:
        json.dump({
            "status": result["status"],
            "timestamp": datetime.now().isoformat(),
            "usage": result.get("usage"),
        }, f, indent=2)


def run_chain(
    api_key: str,
    agent: str,
    focus: str,
    start_chapter: int = 38,
    model: str = "claude-sonnet-4-20250514"
):
    """Run complete chain for one agent-focus combination."""

    print(f"\n{'='*60}")
    print(f"CHAIN: {agent} / {focus}")
    print(f"{'='*60}\n")

    client = anthropic.Anthropic(api_key=api_key)

    # Load external state once (it doesn't change per chapter)
    print("Loading external state...")
    external_state = load_external_state(agent, focus)
    print(f"  Loaded: {list(external_state.keys())}")

    # Run each chapter
    for i, chapter_num in enumerate(CHAPTERS):
        if chapter_num < start_chapter:
            print(f"\n  CH{chapter_num}: Skipping (before start_chapter)")
            continue

        print(f"\n  CH{chapter_num}: Running...")

        # Load previous reports
        previous_reports = load_previous_reports(agent, focus, chapter_num)
        print(f"    Previous reports loaded: {len(previous_reports)}")

        # Run analysis
        result = run_chapter(
            client, agent, focus, chapter_num,
            external_state, previous_reports, model
        )

        # Save result
        save_chapter_report(agent, focus, chapter_num, result)

        if result["status"] == "success":
            print(f"    ✓ Success")
            if result.get("usage"):
                print(f"    Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")
        else:
            print(f"    ✗ Error: {result.get('error', 'Unknown')}")

        # Rate limit delay (except after last chapter)
        if chapter_num < CHAPTERS[-1]:
            print(f"    Waiting {DELAY_BETWEEN_RUNS}s for rate limit...")
            time.sleep(DELAY_BETWEEN_RUNS)

    print(f"\n{'='*60}")
    print(f"CHAIN COMPLETE: {agent} / {focus}")
    print(f"Output: {OUTPUT_DIR / f'{agent}_{focus}'}")
    print(f"{'='*60}\n")


# ============================================================================
# CLI
# ============================================================================

def list_agents():
    """Print available agents and focuses."""
    print("\nAvailable Agent-Focus Combinations:\n")
    for agent, focuses in AGENT_FOCUSES.items():
        print(f"  {agent}:")
        for focus in focuses:
            print(f"    - {focus}")
    print(f"\nTotal: {sum(len(f) for f in AGENT_FOCUSES.values())} combinations")
    print(f"Chapters: {CHAPTERS}")
    print(f"Total runs: {sum(len(f) for f in AGENT_FOCUSES.values()) * len(CHAPTERS)}")


def main():
    parser = argparse.ArgumentParser(description="Run agent-focus chain analysis")
    parser.add_argument("api_key", nargs="?", help="Anthropic API key")
    parser.add_argument("agent", nargs="?", help="Agent name")
    parser.add_argument("focus", nargs="?", help="Focus area")
    parser.add_argument("--list", action="store_true", help="List available agents/focuses")
    parser.add_argument("--start", type=int, default=38, help="Start from chapter (default: 38)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Model to use")

    args = parser.parse_args()

    if args.list:
        list_agents()
        return

    if not all([args.api_key, args.agent, args.focus]):
        parser.print_help()
        print("\nExamples:")
        print("  python chain_runner.py $API_KEY continuity_editor timeline")
        print("  python chain_runner.py --list")
        return

    if args.agent not in AGENT_FOCUSES:
        print(f"Error: Unknown agent '{args.agent}'")
        print(f"Available: {list(AGENT_FOCUSES.keys())}")
        return

    if args.focus not in AGENT_FOCUSES[args.agent]:
        print(f"Error: Unknown focus '{args.focus}' for agent '{args.agent}'")
        print(f"Available: {AGENT_FOCUSES[args.agent]}")
        return

    run_chain(args.api_key, args.agent, args.focus, args.start, args.model)


if __name__ == "__main__":
    main()
