#!/usr/bin/env python3
"""
Compare before/after prose changes using Claude API.
Extracts diff hunks and evaluates whether changes improve the writing.
"""

import anthropic
import re
import sys
from pathlib import Path

DIFF_FILE = Path("/tmp/resonance_session_diff.txt")

ANALYSIS_PROMPT = """You are a literary editor evaluating prose revisions for a science fiction novel.

I'll give you a series of before/after passage pairs from the same manuscript. For each pair, assess whether the revision improves or weakens the prose, and why. Be honest — not everything is an improvement.

Criteria (in priority order):
1. Trust the reader — does the revision remove over-explanation or labeling of what was already shown?
2. Precision — does the revision arrive at the right word more directly?
3. Rhythm — does the revision read better aloud?
4. Loss — does the revision cut something load-bearing?

After assessing all pairs, give:
- Overall verdict: net improvement, mixed, or net loss
- The strongest improvements (up to 3)
- Any cuts that feel like losses (up to 3)
- One honest concern, if any

Here are the before/after pairs:

{pairs}
"""

def parse_diff_hunks(diff_text):
    """Extract (filename, before, after) tuples from a unified diff."""
    pairs = []
    current_file = None
    before_lines = []
    after_lines = []
    in_hunk = False

    for line in diff_text.split('\n'):
        if line.startswith('--- a/'):
            current_file = line[6:]
        elif line.startswith('+++ b/'):
            pass
        elif line.startswith('@@'):
            if in_hunk and (before_lines or after_lines):
                b = '\n'.join(before_lines).strip()
                a = '\n'.join(after_lines).strip()
                if b != a and b and a:
                    pairs.append((current_file, b, a))
            before_lines = []
            after_lines = []
            in_hunk = True
        elif in_hunk:
            if line.startswith('-') and not line.startswith('---'):
                before_lines.append(line[1:])
            elif line.startswith('+') and not line.startswith('+++'):
                after_lines.append(line[1:])
            elif line.startswith(' '):
                before_lines.append(line[1:])
                after_lines.append(line[1:])

    if in_hunk and (before_lines or after_lines):
        b = '\n'.join(before_lines).strip()
        a = '\n'.join(after_lines).strip()
        if b != a and b and a:
            pairs.append((current_file, b, a))

    return pairs


def format_pairs_for_prompt(pairs, max_pairs=40):
    """Format pairs as readable before/after blocks."""
    # Filter out trivial changes (very short diffs)
    meaningful = [(f, b, a) for f, b, a in pairs
                  if abs(len(b) - len(a)) > 10 or len(b) > 50]

    # Sample evenly across the manuscript
    step = max(1, len(meaningful) // max_pairs)
    sampled = meaningful[::step][:max_pairs]

    lines = []
    for i, (fname, before, after) in enumerate(sampled, 1):
        chapter = re.search(r'RESONANCE_(CH\w+|EP_\w+)', fname)
        ch = chapter.group(1) if chapter else fname
        lines.append(f"--- Pair {i} ({ch}) ---")
        lines.append(f"BEFORE:\n{before}")
        lines.append(f"AFTER:\n{after}")
        lines.append("")

    return '\n'.join(lines), len(meaningful)


def run(api_key):
    client = anthropic.Anthropic(api_key=api_key)

    diff_text = DIFF_FILE.read_text()
    pairs = parse_diff_hunks(diff_text)
    formatted, total = format_pairs_for_prompt(pairs, max_pairs=40)

    print(f"Total meaningful changes found: {total}")
    print(f"Sending sample of 40 to API for analysis...\n")

    prompt = ANALYSIS_PROMPT.format(pairs=formatted)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.content[0].text)
    print(f"\n({response.usage.input_tokens} in / {response.usage.output_tokens} out)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compare_versions.py <api_key>")
        sys.exit(1)
    run(sys.argv[1])
