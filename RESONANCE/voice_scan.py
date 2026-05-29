#!/usr/bin/env python3
"""
RESONANCE Voice Scan — the MEASUREMENT half of the voice scoring rubric.

Computes the deterministic metrics only (Section C C1-C4 + the machine-vocab gate
+ a C5 *distribution* proxy). It does NOT score Track A/B signatures or C5-density
("is this sentence an attitude-aside?") — those are semantic and stay with the
human/agent read. Per the rubric: this tells you WHERE to look, deterministically.
It does not impersonate judgment it can't do.

Keys off file paths/titles (never YAML chapter numbers — the CHAPTERS.yaml numbering
is offset from the .txt filenames).

Usage:
    python voice_scan.py                  # scan all chapters, print table + medians + flags
    python voice_scan.py --file PATH      # also score one extra file (e.g. a draft) against the medians
"""

import argparse
import re
import statistics
from pathlib import Path

CHAPTERS_DIR = Path("/workspaces/pilot/RESONANCE/chapters")

# CON_008 machine vocabulary (a VIOLATION only in Standard's POV — flag, don't assume)
MACHINE_VOCAB = re.compile(
    r"\b(servo|chassis|circuit|processor|reboot|malfunction|hardware|calibrate|"
    r"diagnostic|diagnostics|subroutine|firmware|motherboard)\b", re.I)

FRAGMENT_MAX_WORDS = 5      # narration paragraph this short = emphasis-fragment candidate
EXIT_MAX_WORDS = 6          # chapter/section final line this short = portent-button candidate
DIALOGUE_STARTS = ('"', '“', '<', '#')


def load_body(path):
    """Return list of body paragraphs (skip CHAPTER/title header and blanks)."""
    raw = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    nonblank = [ln for ln in raw if ln]
    # drop leading "CHAPTER N" and the title line that follows it
    out, dropped_header = [], False
    for ln in nonblank:
        if not dropped_header:
            if re.match(r"^CHAPTER\b", ln, re.I):
                continue
            # the first all-caps-ish line after CHAPTER is the title; skip one
            if ln.isupper() or re.match(r"^[A-Z0-9 '’,\.\-]+$", ln) and len(ln.split()) <= 7:
                dropped_header = True
                continue
            dropped_header = True
        out.append(ln)
    return out


def wc(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))


def split_sentences(paragraphs):
    """Crude sentence split across the body, protecting the '. . .' ellipsis."""
    text = " ".join(paragraphs)
    text = text.replace(". . .", "…").replace("...", "…")
    # split on sentence-final punctuation followed by space/quote/end
    parts = re.split(r"(?<=[.!?])[\"”]?\s+", text)
    return [p for p in (x.strip() for x in parts) if wc(p) > 0]


def is_dialogue(par):
    return par.startswith(DIALOGUE_STARTS)


def count_antithesis(paragraphs):
    """C3: 'not X' / 'not X, but Y' / 'Not.' antithesis-correction proxy."""
    text = " ".join(paragraphs)
    n = 0
    n += len(re.findall(r"—\s*not\b", text, re.I))      # —not
    n += len(re.findall(r"\bnot\b[^.?!—]*—", text, re.I))  # not ... —
    n += len(re.findall(r"(?:^|[.?!]\s+)Not\b", text))       # sentence-initial "Not"
    n += len(re.findall(r"\bnot\b[^.?!]*,\s*but\b", text, re.I))     # not X, but Y
    return n


def scan(path):
    body = load_body(path)
    words = sum(wc(p) for p in body)
    per_k = (1000.0 / words) if words else 0

    # C2 fragment-punch density (narration only, exclude dialogue/transmission)
    frag_idx = [i for i, p in enumerate(body)
                if not is_dialogue(p) and 0 < wc(p) <= FRAGMENT_MAX_WORDS]
    c2 = round(len(frag_idx) * per_k, 2)

    # C3 antithesis count
    c3 = count_antithesis(body)

    # C4 sentence-length variance
    sents = split_sentences(body)
    lengths = [wc(s) for s in sents] or [0]
    c4_med = statistics.median(lengths)
    c4_std = round(statistics.pstdev(lengths), 2) if len(lengths) > 1 else 0.0
    c4_max = max(lengths)

    # C1 exit: is the final body paragraph a short portent line?
    exit_short = wc(body[-1]) <= EXIT_MAX_WORDS if body else False

    # machine-vocab gate (count; POV-gated meaning)
    mv = MACHINE_VOCAB.findall(" ".join(body))

    # C5 DISTRIBUTION PROXY: are the fragment-punches evenly spread (metronome)
    # or clustered (spiking)? Split body into thirds, count fragments in each.
    n = len(body)
    thirds = [0, 0, 0]
    for i in frag_idx:
        thirds[min(2, i * 3 // max(1, n))] += 1
    # evenness: stdev of the thirds (low = even spread = metronome-ish)
    c5_even = round(statistics.pstdev(thirds), 2) if any(thirds) else 0.0

    return {
        "chapter": path.stem.replace("RESONANCE_", ""),
        "words": words,
        "C1_exit_short": exit_short,
        "C2_frag_per1k": c2,
        "C3_antithesis": c3,
        "C4_sent_std": c4_std,
        "C4_sent_med": c4_med,
        "C4_sent_max": c4_max,
        "C5_frag_thirds": "/".join(map(str, thirds)),
        "C5_evenness": c5_even,
        "machine_vocab": len(mv),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="extra single file to score against the medians")
    args = ap.parse_args()

    rows = [scan(p) for p in sorted(CHAPTERS_DIR.glob("RESONANCE_CH*.txt"))]

    def med(key):
        vals = [r[key] for r in rows]
        return round(statistics.median(vals), 2)

    med_c2, med_c3, med_c4 = med("C2_frag_per1k"), med("C3_antithesis"), med("C4_sent_std")
    exit_short_pct = round(100 * sum(r["C1_exit_short"] for r in rows) / len(rows))

    hdr = f'{"chapter":34} {"wc":>5} {"exit<":>5} {"C2/1k":>6} {"C3":>4} {"C4std":>6} {"C4max":>6} {"mvoc":>5}'
    print(hdr); print("-" * len(hdr))
    for r in rows:
        flags = []
        if r["C2_frag_per1k"] > med_c2 * 1.4: flags.append("C2")
        if r["C3_antithesis"] > med_c3 * 1.5: flags.append("C3")
        if r["C4_sent_std"] < med_c4 * 0.8: flags.append("C4-flat")
        if r["machine_vocab"]: flags.append(f"mv:{r['machine_vocab']}")
        print(f'{r["chapter"]:34} {r["words"]:>5} {"Y" if r["C1_exit_short"] else "-":>5} '
              f'{r["C2_frag_per1k"]:>6} {r["C3_antithesis"]:>4} {r["C4_sent_std"]:>6} '
              f'{r["C4_sent_max"]:>6} {r["machine_vocab"]:>5}   {" ".join(flags)}')

    print("-" * len(hdr))
    print(f'MEDIANS: C2/1k={med_c2}  C3={med_c3}  C4std={med_c4}  |  '
          f'chapters ending on short line: {exit_short_pct}%  (rubric flags >~40%)')
    print('Flags: C2=frag-dense  C3=antithesis-heavy  C4-flat=low sentence variance (metronome)  mv=machine-vocab (Standard-POV only)')
    print('NOTE: this is the measurement half only. Track A/B signatures and C5-DENSITY '
          '(is a line an attitude-aside?) are semantic and stay with the read.')

    if args.file:
        r = scan(Path(args.file))
        print("\n=== EXTRA FILE vs medians ===")
        print(f'{r["chapter"]}: wc={r["words"]}  exit_short={r["C1_exit_short"]}  '
              f'C2/1k={r["C2_frag_per1k"]} (med {med_c2})  C3={r["C3_antithesis"]} (med {med_c3})  '
              f'C4std={r["C4_sent_std"]} (med {med_c4})  C5_thirds={r["C5_frag_thirds"]} even={r["C5_evenness"]}  '
              f'mvoc={r["machine_vocab"]}')


if __name__ == "__main__":
    main()
