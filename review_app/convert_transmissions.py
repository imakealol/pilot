"""
Convert Control/implant transmission italics (_text_) to angle brackets (<text>).
Only targets confirmed Control ↔ Elena transmission lines.
Thoughts, sign language, narration emphasis, and the CH44 Geometry exchange stay as italic.
"""

import re
from pathlib import Path

CHAPTERS = Path("/workspaces/pilot/RESONANCE/chapters")


def convert_line(line):
    """Replace _..._ with <...> throughout a line."""
    # Match _content_ where content doesn't contain newlines
    # Handles both standalone and inline occurrences
    return re.sub(r'_([^_]+)_', r'<\1>', line)


# Map of filename → set of line numbers (1-indexed) to convert
TRANSMISSION_LINES = {
    "RESONANCE_CH2_THE_OFFERINGS.txt": {
        13, 15, 16, 41, 42, 108, 129, 131, 148, 150, 151, 153, 154
    },
    "RESONANCE_CH5_THE_QUEUE.txt": {19, 27},
    "RESONANCE_CH7_MAKING_THE_DEPOSIT.txt": {18, 23},
    "RESONANCE_CH8_WHATS_IN_A_NAME.txt": {45},
    "RESONANCE_CH16_THE_SILENT_HOUSE.txt": {14, 16, 17, 62},
    "RESONANCE_CH17_THE_SIGN.txt": {7},
    "RESONANCE_CH32_FOLLOW_THE_LEADER.txt": {148, 151, 154, 156, 157},
}


def process_file(filename, line_numbers):
    path = CHAPTERS / filename
    if not path.exists():
        print(f"MISSING: {filename}")
        return

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = []

    for i, line in enumerate(lines, start=1):
        if i in line_numbers:
            new_line = convert_line(line)
            if new_line != line:
                print(f"  {filename}:{i}")
                print(f"    BEFORE: {line.rstrip()}")
                print(f"    AFTER:  {new_line.rstrip()}")
                changed.append((i, line, new_line))
            lines[i - 1] = new_line

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
        print(f"  → {len(changed)} line(s) updated\n")
    else:
        print(f"  → No changes needed in {filename}\n")


if __name__ == "__main__":
    for filename, line_numbers in TRANSMISSION_LINES.items():
        print(f"\n{filename}:")
        process_file(filename, line_numbers)

    print("\nDone.")
