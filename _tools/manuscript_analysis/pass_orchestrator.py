#!/usr/bin/env python3
"""
RESONANCE Manuscript Analysis - Pass Orchestrator
RLM-based parallel agent execution for manuscript review.

4 passes, 7 agents per pass, single focus per agent.
"""

import anthropic
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configuration
PROJECT_ROOT = Path("/workspaces/pilot")
CHAPTERS_DIR = PROJECT_ROOT / "RESONANCE" / "chapters"
DATA_DIR = PROJECT_ROOT / "RESONANCE" / "data"
CONTEXT_DIR = PROJECT_ROOT / "RESONANCE" / "context"
STEWARDS_DIR = PROJECT_ROOT / "_tools" / "agents" / "templates" / "character_stewards"
OUTPUT_DIR = PROJECT_ROOT / "_tools" / "manuscript_analysis" / "outputs"

# Chapters to analyze
TARGET_CHAPTERS = [38, 39, 40, 41, 42, 43, 44]

# Agent focus matrix: pass_number -> {agent: focus}
PASS_MATRIX = {
    1: {
        "continuity_editor": "timeline",
        "worldbuilder": "technology",
        "foreshadow_keeper": "setups",
        "steward_standard": "voice",
        "steward_hendricks": "voice",
        "steward_elena": "voice",
        "steward_four": "voice",
    },
    2: {
        "continuity_editor": "character_state",
        "worldbuilder": "locations",
        "foreshadow_keeper": "payoffs",
        "steward_standard": "knowledge",
        "steward_hendricks": "knowledge",
        "steward_elena": "knowledge",
        "steward_four": "knowledge",
    },
    3: {
        "continuity_editor": "world_rules",
        "worldbuilder": "social_faction",
        "foreshadow_keeper": "dangling_threads",
        "steward_standard": "arc",
        "steward_hendricks": "arc",
        "steward_elena": "arc",
        "steward_four": "arc",
    },
    4: {
        "continuity_editor": "object_tracking",
        "worldbuilder": "sensory",
        "foreshadow_keeper": "telegraph_risk",
        "steward_standard": "relationships",
        "steward_hendricks": "relationships",
        "steward_elena": "relationships",
        "steward_four": "relationships",
    },
}


def load_file(path: Path) -> str:
    """Load a file's contents."""
    if path.exists():
        return path.read_text()
    return f"[FILE NOT FOUND: {path}]"


def load_chapters() -> Dict[int, str]:
    """Load all target chapter files."""
    chapters = {}
    for ch_num in TARGET_CHAPTERS:
        # Find the chapter file (format varies)
        pattern = f"RESONANCE_CH{ch_num}_*.txt"
        matches = list(CHAPTERS_DIR.glob(pattern))
        if matches:
            chapters[ch_num] = load_file(matches[0])
        else:
            chapters[ch_num] = f"[CHAPTER {ch_num} NOT FOUND]"
    return chapters


def load_external_state() -> Dict[str, str]:
    """Load all external state files for RLM queries."""
    state = {}

    # Core data files
    state["CHARACTERS.yaml"] = load_file(DATA_DIR / "CHARACTERS.yaml")
    state["PROPS.yaml"] = load_file(DATA_DIR / "PROPS.yaml")

    # Context files
    state["GEOMETRY_VISUAL_LANGUAGE.md"] = load_file(CONTEXT_DIR / "GEOMETRY_VISUAL_LANGUAGE.md")
    state["NEGATIVE_CONSTRAINTS.md"] = load_file(CONTEXT_DIR / "NEGATIVE_CONSTRAINTS.md")

    # Key project files
    state["HANDOFF.md"] = load_file(PROJECT_ROOT / "HANDOFF.md")
    state["ACT_III_MAPS.md"] = load_file(PROJECT_ROOT / "RESONANCE" / "drafting" / "ACT_III_MAPS.md")
    state["RESONANCE_STYLE_GUIDE.md"] = load_file(PROJECT_ROOT / "RESONANCE_STYLE_GUIDE.md")

    # Character stewards
    for steward_file in STEWARDS_DIR.glob("steward_*.md"):
        state[steward_file.name] = load_file(steward_file)

    return state


def get_agent_prompt(agent: str, focus: str, chapters: Dict[int, str], state: Dict[str, str]) -> str:
    """Generate the full prompt for an agent with its specific focus."""

    # Combine chapter texts
    chapter_text = "\n\n".join([
        f"=== CHAPTER {num} ===\n{text}"
        for num, text in sorted(chapters.items())
    ])

    # Base enforcement protocol (all agents use this)
    enforcement = """
## ENFORCEMENT PROTOCOL (MANDATORY)

You are operating under RLM (Recursive Language Model) principles:
1. Query external state, don't work from memory
2. Cite sources for all claims (file:section or chapter:line)
3. Single focus only - defer out-of-scope observations
4. Self-validate before submitting

### Output Requirements
- query_log: List all external state you referenced
- findings: Each finding must cite source
- deferred: Out-of-scope observations logged, not acted upon
- self_check: Validate your own process

If you cannot cite a source for a claim, do not make the claim.
"""

    # Agent-specific prompts
    prompts = {
        "continuity_editor": {
            "timeline": f"""
# CONTINUITY EDITOR - Timeline Focus
## Question: "Do events happen in the correct order across CH38-44?"

{enforcement}

## Your Single Focus
Track ONLY timeline consistency:
- Event sequence (does A happen before B as established?)
- Time references (hours, days - do they add up?)
- Parallel action timing (are simultaneous events actually simultaneous?)

## External State Available
- HANDOFF.md (chapter structure, timeline notes)
- ACT_III_MAPS.md (parallel thread timing)
- CHARACTERS.yaml (event references)

## DO NOT track (defer these):
- Character locations (that's character_state focus)
- Object positions (that's object_tracking focus)
- Injuries (that's character_state focus)

## Chapters to Analyze
{chapter_text}

## External State
### HANDOFF.md
{state.get('HANDOFF.md', '[NOT LOADED]')[:15000]}

### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}
""",
            "character_state": f"""
# CONTINUITY EDITOR - Character State Focus
## Question: "Are characters in the right place with correct injuries and knowledge?"

{enforcement}

## Your Single Focus
Track ONLY character state:
- Location (where is each character in each scene?)
- Injuries (do wounds persist appropriately?)
- Knowledge (does character know only what they've learned on-page?)

## Key Characters to Track
- Standard: Location, arm status, injuries
- Hendricks: Location, stab wound (CH41), deterioration
- Elena: Location, blade wound (dying), knowledge of Marisol
- Four: Location, structural integrity percentage
- Ash: Location (dies CH41)

## External State Available
- CHARACTERS.yaml (knowledge sections, physical state)
- HANDOFF.md (reveal sequence - who knows what when)

## DO NOT track (defer these):
- Timeline sequence (different focus)
- Object locations separate from characters (different focus)

## Chapters to Analyze
{chapter_text}

## External State
### CHARACTERS.yaml
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}

### HANDOFF.md (reveal sequence section)
{state.get('HANDOFF.md', '[NOT LOADED]')[:20000]}
""",
            "world_rules": f"""
# CONTINUITY EDITOR - World Rules Focus
## Question: "Are established rules of this world followed consistently?"

{enforcement}

## Your Single Focus
Track ONLY world rule adherence:
- Geometry behavior (does it work as established?)
- Deletion zone mechanics (consistent?)
- Softing behavior (on/off states, effects)
- AI/consciousness rules (transfer, hot-swap, etc.)

## External State Available
- GEOMETRY_VISUAL_LANGUAGE.md (how Geometry works)
- PROPS.yaml (tech mechanics)
- HANDOFF.md (established rules)

## DO NOT track (defer these):
- Specific prop locations (different focus)
- Character knowledge (different focus)

## Chapters to Analyze
{chapter_text}

## External State
### GEOMETRY_VISUAL_LANGUAGE.md
{state.get('GEOMETRY_VISUAL_LANGUAGE.md', '[NOT LOADED]')}

### PROPS.yaml
{state.get('PROPS.yaml', '[NOT LOADED]')}
""",
            "object_tracking": f"""
# CONTINUITY EDITOR - Object Tracking Focus
## Question: "Where are important objects and do they behave consistently?"

{enforcement}

## Your Single Focus
Track ONLY objects:
- Revolver (who has it, bullet count)
- Ceramic blade (Ash's weapon)
- Standard's arms (which arm does she have?)
- Elena's gear (weapons, implant)
- Four's VTOL (status, location)

## Key Object States (from CHARACTERS.yaml)
- Revolver: Ash has it until CH41, then Hendricks. 2 bullets until CH41, then 1, then 0.
- Standard's arm: Kael's until CH41(?), then sister's gift

## External State Available
- CHARACTERS.yaml (inventory sections)
- PROPS.yaml (object details)
- ACT_III_MAPS.md (revolver journey, arm progression)

## Chapters to Analyze
{chapter_text}

## External State
### CHARACTERS.yaml (Hendricks inventory)
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}

### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}

### PROPS.yaml
{state.get('PROPS.yaml', '[NOT LOADED]')}
""",
        },

        "worldbuilder": {
            "technology": f"""
# WORLDBUILDER - Technology Focus
## Question: "Does technology work the same way each time?"

{enforcement}

## Your Single Focus
Track ONLY tech consistency:
- Bolt rounds (mechanics, effects)
- Frequency modulators (how they work)
- Hot-swap mechanics (AI transfer between systems)
- Implant behavior (Elena's neural implant)
- VTOL/ship systems

## External State Available
- PROPS.yaml (weapon/tech specifications)
- CHARACTERS.yaml (tech descriptions)

## DO NOT track (defer these):
- Location geography (different focus)
- Social/faction behavior (different focus)

## Chapters to Analyze
{chapter_text}

## External State
### PROPS.yaml
{state.get('PROPS.yaml', '[NOT LOADED]')}
""",
            "locations": f"""
# WORLDBUILDER - Locations Focus
## Question: "Does geography and setting stay consistent?"

{enforcement}

## Your Single Focus
Track ONLY location consistency:
- Quiet Zone layout (compound, throne room, eastern fields)
- New Geneva station (layout, docking)
- Deletion zone boundaries
- Motor pool, tower positions

## External State Available
- HANDOFF.md (location references)
- Chapter descriptions (establish and maintain)

## Chapters to Analyze
{chapter_text}

## External State
### HANDOFF.md
{state.get('HANDOFF.md', '[NOT LOADED]')[:15000]}
""",
            "social_faction": f"""
# WORLDBUILDER - Social/Faction Focus
## Question: "Do factions and organizations behave consistently?"

{enforcement}

## Your Single Focus
Track ONLY faction behavior:
- Carbonists (Ash's people) - motivations, methods
- Template 3s - behavior, organization
- Pragmatists/Jupiter forces - tactics
- Resonant/Protectors - goals, methods

## External State Available
- CHARACTERS.yaml (faction descriptions)
- HANDOFF.md (faction notes)

## Chapters to Analyze
{chapter_text}

## External State
### CHARACTERS.yaml
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}
""",
            "sensory": f"""
# WORLDBUILDER - Sensory Focus
## Question: "Are environmental and sensory details consistent?"

{enforcement}

## Your Single Focus
Track ONLY sensory consistency:
- What does the Geometry look/sound/feel like?
- Deletion zone sensory experience
- Quiet Zone atmosphere
- Battle sounds, smells, physical sensations

## External State Available
- GEOMETRY_VISUAL_LANGUAGE.md (visual vocabulary)
- RESONANCE_STYLE_GUIDE.md (sensory description patterns)

## Chapters to Analyze
{chapter_text}

## External State
### GEOMETRY_VISUAL_LANGUAGE.md
{state.get('GEOMETRY_VISUAL_LANGUAGE.md', '[NOT LOADED]')}

### RESONANCE_STYLE_GUIDE.md
{state.get('RESONANCE_STYLE_GUIDE.md', '[NOT LOADED]')}
""",
        },

        "foreshadow_keeper": {
            "setups": f"""
# FORESHADOW KEEPER - Setups Focus
## Question: "What is being planted/set up in these chapters?"

{enforcement}

## Your Single Focus
Track ONLY setups being planted:
- New information revealed that might matter later
- Objects introduced
- Character traits established
- Promises made (explicit or implicit)

## External State Available
- ACT_III_MAPS.md (existing callback tracker)
- HANDOFF.md (known setups)

## DO NOT track (defer these):
- Payoffs (different focus)
- Telegraph risks (different focus)

## Chapters to Analyze
{chapter_text}

## External State
### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}
""",
            "payoffs": f"""
# FORESHADOW KEEPER - Payoffs Focus
## Question: "What setups are being paid off in these chapters?"

{enforcement}

## Your Single Focus
Track ONLY payoffs being delivered:
- Which established setups get resolved?
- Are payoffs satisfying (earned)?
- Do payoffs match their setups?

## Known Callbacks That Should Pay Off (from ACT_III_MAPS.md)
- "Does it still hurt the same?" (CH27 setup)
- "I'll keep the engine warm" (CH30 setup)
- Ceramic blade (Book 1 setup)
- Three arms progression
- Bullet 6
- 16,749 souls / "It's okay"
- "You think that machine loves you?"
- CH1 shutdown phrase echo

## External State Available
- ACT_III_MAPS.md (callback tracker)
- HANDOFF.md (callbacks that must pay off)

## Chapters to Analyze
{chapter_text}

## External State
### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}

### HANDOFF.md (callbacks section)
{state.get('HANDOFF.md', '[NOT LOADED]')[:20000]}
""",
            "dangling_threads": f"""
# FORESHADOW KEEPER - Dangling Threads Focus
## Question: "What threads are still waiting for resolution?"

{enforcement}

## Your Single Focus
Track ONLY unresolved threads:
- Setups from earlier chapters not yet paid off
- Questions raised but not answered
- Promises not yet kept

## External State Available
- ACT_III_MAPS.md (callback tracker)
- HANDOFF.md (known threads)

## Chapters to Analyze
{chapter_text}

## External State
### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}
""",
            "telegraph_risk": f"""
# FORESHADOW KEEPER - Telegraph Risk Focus
## Question: "Does anything risk revealing Standard = Marisol too early?"

{enforcement}

## Your Single Focus
Track ONLY telegraph risks for the central reveal:
- Standard feeling "something familiar" about Elena
- Standard showing conscious preferential protection
- 287.3 Hz reading as recognition not coincidence
- Any suggestion Morton planned the Template 3
- Standard's POV hinting she knows more than she does

## The Reveal (from HANDOFF.md)
- Standard does NOT know she's Marisol until after bullet in CH43
- She says "It's okay. I trust you." without knowing
- Memories return only in dissolution
- Readers should discover WITH characters

## Severity Levels
- HIGH: First-time reader will guess
- MEDIUM: Attentive reader might guess
- LOW: Only visible on re-read (this is correct)

## External State Available
- HANDOFF.md (reveal sequence, negative constraints)
- CHARACTERS.yaml (Standard.true_identity)

## Chapters to Analyze
{chapter_text}

## External State
### HANDOFF.md
{state.get('HANDOFF.md', '[NOT LOADED]')}

### CHARACTERS.yaml (Standard section)
{state.get('CHARACTERS.yaml', '[NOT LOADED]')[:8000]}
""",
        },
    }

    # Character steward prompts
    for character in ["standard", "hendricks", "elena", "four"]:
        steward_file = f"steward_{character}.md"
        steward_content = state.get(steward_file, '[NOT LOADED]')
        char_upper = character.upper()

        prompts[f"steward_{character}"] = {
            "voice": f"""
# CHARACTER STEWARD: {char_upper} - Voice Focus
## Question: "Does {char_upper} sound like themselves in these chapters?"

{enforcement}

## Your Single Focus
Track ONLY voice consistency:
- Speech patterns (register, vocabulary, rhythm)
- Internal monologue style
- Forbidden words/phrases for this character
- Characteristic expressions

## External State Available
- steward_{character}.md (voice rules, forbidden words)
- CHARACTERS.yaml ({char_upper} section)

## DO NOT track (defer these):
- What they know (different focus)
- Arc progression (different focus)
- Relationships (different focus)

## Chapters to Analyze
{chapter_text}

## External State
### steward_{character}.md
{steward_content}

### CHARACTERS.yaml ({char_upper} section)
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}
""",
            "knowledge": f"""
# CHARACTER STEWARD: {char_upper} - Knowledge Focus
## Question: "Does {char_upper} know only what they should know at each point?"

{enforcement}

## Your Single Focus
Track ONLY knowledge boundaries:
- What has this character learned on-page?
- Do they act on information they shouldn't have?
- Key secrets: Who knows Standard = Marisol? When?

## External State Available
- CHARACTERS.yaml ({char_upper}.knowledge section)
- HANDOFF.md (reveal sequence)
- steward_{character}.md

## Chapters to Analyze
{chapter_text}

## External State
### CHARACTERS.yaml
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}

### HANDOFF.md
{state.get('HANDOFF.md', '[NOT LOADED]')[:15000]}

### steward_{character}.md
{steward_content}
""",
            "arc": f"""
# CHARACTER STEWARD: {char_upper} - Arc Focus
## Question: "Is {char_upper} where they should be emotionally at each point?"

{enforcement}

## Your Single Focus
Track ONLY arc progression:
- Emotional state matches narrative position?
- Character growth/change is earned?
- Arc beats land in correct sequence?

## External State Available
- ACT_III_MAPS.md ({char_upper} emotional arc)
- steward_{character}.md (arc notes)
- CHARACTERS.yaml

## Chapters to Analyze
{chapter_text}

## External State
### ACT_III_MAPS.md
{state.get('ACT_III_MAPS.md', '[NOT LOADED]')}

### steward_{character}.md
{steward_content}
""",
            "relationships": f"""
# CHARACTER STEWARD: {char_upper} - Relationships Focus
## Question: "Do {char_upper}'s interactions match established relationship dynamics?"

{enforcement}

## Your Single Focus
Track ONLY relationship consistency:
- How does this character relate to others?
- Do interactions match documented relationship status?
- Any relationship shifts - are they earned?

## External State Available
- CHARACTERS.yaml ({char_upper}.relationships)
- steward_{character}.md (relationship notes)

## Chapters to Analyze
{chapter_text}

## External State
### CHARACTERS.yaml
{state.get('CHARACTERS.yaml', '[NOT LOADED]')}

### steward_{character}.md
{steward_content}
""",
        }

    # Get the specific prompt
    if agent in prompts and focus in prompts[agent]:
        return prompts[agent][focus]
    else:
        return f"[ERROR: No prompt defined for agent={agent}, focus={focus}]"


async def run_agent(
    client: anthropic.Anthropic,
    agent: str,
    focus: str,
    chapters: Dict[int, str],
    state: Dict[str, str],
    model: str = "claude-sonnet-4-20250514"
) -> Dict[str, Any]:
    """Run a single agent with its focus."""

    prompt = get_agent_prompt(agent, focus, chapters, state)

    print(f"  Running {agent} ({focus})...")

    try:
        response = client.messages.create(
            model=model,
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return {
            "agent": agent,
            "focus": focus,
            "status": "success",
            "output": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        }
    except Exception as e:
        return {
            "agent": agent,
            "focus": focus,
            "status": "error",
            "error": str(e),
        }


async def run_pass(
    client: anthropic.Anthropic,
    pass_number: int,
    chapters: Dict[int, str],
    state: Dict[str, str],
    model: str = "claude-sonnet-4-20250514",
    sequential: bool = True,
    delay: int = 15
) -> Dict[str, Any]:
    """Run all agents for a single pass. Sequential mode avoids rate limits."""

    print(f"\n{'='*60}")
    print(f"PASS {pass_number}")
    print(f"{'='*60}")

    focus_map = PASS_MATRIX[pass_number]
    results = []

    if sequential:
        # Run agents sequentially with delay to avoid rate limits
        for i, (agent, focus) in enumerate(focus_map.items()):
            if i > 0:
                print(f"  Waiting {delay}s for rate limit...")
                await asyncio.sleep(delay)
            result = await run_agent(client, agent, focus, chapters, state, model)
            results.append(result)
    else:
        # Run all agents in parallel (may hit rate limits)
        tasks = []
        for agent, focus in focus_map.items():
            task = run_agent(client, agent, focus, chapters, state, model)
            tasks.append(task)
        results = await asyncio.gather(*tasks)

    # Compile pass report
    pass_report = {
        "pass_number": pass_number,
        "timestamp": datetime.now().isoformat(),
        "agents": {r["agent"]: r for r in results},
        "summary": {
            "total_agents": len(results),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "errors": sum(1 for r in results if r["status"] == "error"),
        }
    }

    return pass_report


def save_report(report: Dict[str, Any], pass_number: int):
    """Save a pass report to disk."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pass{pass_number}_{timestamp}.json"
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved: {filepath}")

    # Also save a human-readable version
    readable_filename = f"pass{pass_number}_{timestamp}_readable.md"
    readable_filepath = OUTPUT_DIR / readable_filename

    with open(readable_filepath, 'w') as f:
        f.write(f"# Pass {pass_number} Report\n\n")
        f.write(f"Generated: {report['timestamp']}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Total Agents: {report['summary']['total_agents']}\n")
        f.write(f"- Successful: {report['summary']['successful']}\n")
        f.write(f"- Errors: {report['summary']['errors']}\n\n")

        for agent, result in report['agents'].items():
            f.write(f"---\n\n## {agent.upper()} ({result['focus']})\n\n")
            if result['status'] == 'success':
                f.write(result['output'])
            else:
                f.write(f"**ERROR:** {result.get('error', 'Unknown error')}\n")
            f.write("\n\n")

    print(f"Readable report saved: {readable_filepath}")


async def main():
    """Main entry point."""
    import sys

    # Get API key from environment or argument
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]

    if not api_key:
        print("Error: No API key provided.")
        print("Usage: python pass_orchestrator.py <api_key>")
        print("   or: ANTHROPIC_API_KEY=<key> python pass_orchestrator.py")
        sys.exit(1)

    # Get pass number (default to 1)
    pass_number = 1
    if len(sys.argv) > 2:
        pass_number = int(sys.argv[2])

    if pass_number not in PASS_MATRIX:
        print(f"Error: Invalid pass number {pass_number}. Valid: 1-4")
        sys.exit(1)

    print("RESONANCE Manuscript Analysis")
    print(f"Pass {pass_number} of 4")
    print(f"Chapters: {TARGET_CHAPTERS}")
    print()

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    # Load chapters and external state
    print("Loading chapters...")
    chapters = load_chapters()
    print(f"  Loaded {len(chapters)} chapters")

    print("Loading external state...")
    state = load_external_state()
    print(f"  Loaded {len(state)} state files")

    # Run the pass
    report = await run_pass(client, pass_number, chapters, state)

    # Save report
    save_report(report, pass_number)

    print("\n" + "="*60)
    print("PASS COMPLETE")
    print("="*60)
    print(f"Successful: {report['summary']['successful']}/{report['summary']['total_agents']}")

    if report['summary']['errors'] > 0:
        print(f"Errors: {report['summary']['errors']}")
        for agent, result in report['agents'].items():
            if result['status'] == 'error':
                print(f"  - {agent}: {result.get('error', 'Unknown')}")


if __name__ == "__main__":
    asyncio.run(main())
