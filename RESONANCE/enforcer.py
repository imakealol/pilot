#!/usr/bin/env python3
"""
RESONANCE Constraint Enforcer

Runs mechanical (regex) and judgment (Claude API) checks against CORE.yaml constraints.
Flags violations of CON_008, CON_001, CON_011 (regex) and CON_013, CON_015 (API).

Usage:
    python enforcer.py <api_key>                    # all chapters, haiku
    python enforcer.py <api_key> --chapters 1-5     # chapter range
    python enforcer.py <api_key> --model sonnet     # use Sonnet for judgment
    python enforcer.py --mechanical-only            # regex only, no API
"""

import anthropic
import argparse
import re
import time
import yaml
from pathlib import Path
from datetime import datetime

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path("/workspaces/pilot")
CHAPTERS_DIR = PROJECT_ROOT / "RESONANCE" / "chapters"
OUTPUT_DIR = PROJECT_ROOT / "RESONANCE" / "enforcer_outputs"

MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
}

DELAY = 2  # seconds between API calls

# ============================================================================
# MECHANICAL CONSTRAINTS
# ============================================================================

MECHANICAL_CHECKS = [
    {
        "id": "CON_008",
        "name": "Machine vocabulary",
        "note": "Violation only if in Standard's POV — verify before cutting",
        "pattern": r'\b(servo|chassis|circuit|processor|reboot|malfunction|hardware)\b',
        "flags": re.IGNORECASE,
    },
    {
        "id": "CON_001",
        "name": "Ozone descriptor",
        "note": "Do not use ozone as a sensory descriptor",
        "pattern": r'\bozone\b',
        "flags": re.IGNORECASE,
    },
    {
        "id": "CON_011",
        "name": "Transaction framing",
        "note": "No rights/debts/proof framing — step outside the transaction",
        "pattern": r'earn the right|prove her consciousness|owe them|debt to',
        "flags": re.IGNORECASE,
    },
]

# ============================================================================
# JUDGMENT PROMPT
# ============================================================================

JUDGMENT_PROMPT = """You are a constraint enforcer for a literary manuscript. Flag passages that violate these two rules. Be strict — only flag clear violations, not marginal cases. When in doubt, don't flag.

## CON_013: Lecture Mode
A character is directly explaining what the scene means, what something represents, or delivering thematic interpretation as dialogue or internal monologue. The character becomes a mouthpiece for the theme rather than a person in a scene.

## CON_015: Trust the Reader
The prose shows something, then immediately interprets or labels what it just showed. The image does the work; the sentence after it explains the image to the reader. Cut the explanation — the image is enough.

Clear CON_015 violations (already fixed, for reference):
- Action shows Otis step in front → prose adds "She didn't believe in any of it. And she still stepped in front." [labels the irony]
- Control's message is cold → prose adds "Her mother reduces death to supply logistics." [interprets for reader]
- Goff walks into wave mid-sermon → prose adds "He trusted his faith over his sensors. The building exploited belief." [explains the action]

## OUTPUT
Return YAML only. If no violations, return an empty flags list.

```yaml
flags:
  - constraint: CON_015
    line: 41
    evidence: "exact quote of the offending sentence(s)"
    reason: "one sentence: what the preceding image already showed"
```

## CHAPTER

{content}
"""

# ============================================================================
# FILE LOADING
# ============================================================================

def sort_key(filename):
    """Sort CH1, CH2... CH24a, EP correctly."""
    if 'EP_' in filename:
        return 99
    match = re.search(r'CH(\d+)([a-z])?', filename)
    if match:
        num = int(match.group(1))
        sub = match.group(2) or ''
        return num + ((ord(sub) - ord('a') + 1) * 0.1 if sub else 0)
    return 999


def get_chapter_files(chapter_range=None):
    """Get all chapter files sorted. Optionally filter by chapter number range."""
    files = list(CHAPTERS_DIR.glob("RESONANCE_CH*.txt")) + \
            list(CHAPTERS_DIR.glob("RESONANCE_EP*.txt"))
    files = [f for f in files if '_TRANSCRIPT' not in f.name and 'SCAFFOLD' not in f.name]
    files.sort(key=lambda f: sort_key(f.name))

    if chapter_range:
        nums = parse_range(chapter_range)
        files = [f for f in files if any(
            re.search(rf'CH{n}[_a-z]', f.name) for n in nums
        )]

    return files


def parse_range(range_str):
    """'1-10' → [1..10], '5' → [5]"""
    if '-' in range_str:
        a, b = range_str.split('-')
        return list(range(int(a), int(b) + 1))
    return [int(range_str)]

# ============================================================================
# MECHANICAL PASS
# ============================================================================

def mechanical_pass(content):
    flags = []
    lines = content.split('\n')
    for check in MECHANICAL_CHECKS:
        pattern = re.compile(check['pattern'], check.get('flags', 0))
        for line_num, line in enumerate(lines, 1):
            for match in pattern.finditer(line):
                flags.append({
                    'constraint': check['id'],
                    'line': line_num,
                    'match': match.group(),
                    'evidence': line.strip(),
                    'note': check['note'],
                })
    return flags

# ============================================================================
# JUDGMENT PASS
# ============================================================================

def judgment_pass(client, content, model_id):
    prompt = JUDGMENT_PROMPT.format(content=content)
    try:
        response = client.messages.create(
            model=model_id,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.content[0].text
        match = re.search(r'```yaml\s*\n(.*?)\n```', output, re.DOTALL)
        if match:
            parsed = yaml.safe_load(match.group(1))
            return parsed.get('flags') or [], response.usage
        parsed = yaml.safe_load(output)
        if isinstance(parsed, dict):
            return parsed.get('flags') or [], response.usage
    except Exception as e:
        return [{'constraint': 'ERROR', 'evidence': str(e)}], None
    return [], None

# ============================================================================
# RUN
# ============================================================================

def run(api_key=None, chapter_range=None, model_name='haiku', mechanical_only=False):
    model_id = MODELS.get(model_name, MODELS['haiku'])
    client = anthropic.Anthropic(api_key=api_key) if not mechanical_only else None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = get_chapter_files(chapter_range)

    print(f"Checking {len(files)} chapter(s)...")
    print(f"Mode: {'mechanical only' if mechanical_only else f'mechanical + API ({model_name})'}\n")

    report = {}
    total = 0

    for f in files:
        name = f.stem
        content = f.read_text(encoding='utf-8')
        print(f"  {name}...", end='', flush=True)

        flags = mechanical_pass(content)

        if not mechanical_only:
            j_flags, usage = judgment_pass(client, content, model_id)
            flags.extend(j_flags)
            if usage:
                print(f" ({usage.input_tokens}in/{usage.output_tokens}out)", end='')
            time.sleep(DELAY)

        count = len(flags)
        total += count
        print(f" → {count} flag(s)")

        report[name] = {
            'flags': flags if flags else [],
            'status': 'clean' if not flags else f'{count} flag(s)',
        }

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = 'mechanical' if mechanical_only else model_name
    out = OUTPUT_DIR / f"enforcer_{mode}_{timestamp}.yaml"
    with open(out, 'w') as fh:
        yaml.dump(report, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\n{'='*50}")
    print(f"{total} total flags across {len(files)} chapters")
    print(f"Report: {out.name}")
    return out


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='RESONANCE Constraint Enforcer')
    parser.add_argument('api_key', nargs='?', help='Anthropic API key')
    parser.add_argument('--chapters', help='Range e.g. 1-5 or single e.g. 3')
    parser.add_argument('--model', choices=['haiku', 'sonnet'], default='haiku',
                        help='Model for judgment pass (default: haiku)')
    parser.add_argument('--mechanical-only', action='store_true',
                        help='Regex checks only, no API calls')
    args = parser.parse_args()

    if not args.mechanical_only and not args.api_key:
        parser.print_help()
        print('\nError: api_key required unless --mechanical-only')
        return

    run(
        api_key=args.api_key,
        chapter_range=args.chapters,
        model_name=args.model,
        mechanical_only=args.mechanical_only,
    )


if __name__ == '__main__':
    main()
