#!/usr/bin/env python3
"""Render a Resonance chapter as standalone HTML for cover-to-cover reading."""
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
CHAPTERS = BASE / "chapters"
OUT = BASE / "reader_output"

CSS = """
  body { background: #f5f1e8; color: #2a2620; font-family: 'Georgia', 'Iowan Old Style', serif;
         max-width: 36rem; margin: 3rem auto; padding: 0 1.5rem; line-height: 1.65; font-size: 1.05rem; }
  .chap-num { font-family: 'Helvetica Neue', sans-serif; letter-spacing: 0.3em; font-size: 0.8rem;
              text-transform: uppercase; color: #8b7d6b; text-align: center; margin: 0 0 0.5rem; }
  .chap-title { font-family: 'Helvetica Neue', sans-serif; letter-spacing: 0.18em; font-size: 1.4rem;
                text-align: center; margin: 0 0 3rem; font-weight: 600; }
  p { margin: 0 0 1.1rem; text-indent: 1.5rem; }
  p.first { text-indent: 0; }
  .break { text-align: center; margin: 2rem 0; color: #a89882; letter-spacing: 0.5em; }
  em { font-style: italic; }
  .tx { font-style: italic; color: #6b4a30; }
  .tx::before { content: "<"; }
  .tx::after  { content: ">"; }
"""

def render_inline(text):
    # 1. Angle-bracket transmissions (greedy-careful — they don't span line breaks)
    text = re.sub(r"<([^<>\n]+)>", r'<span class="tx">\1</span>', text)
    # 2. Underscore italics
    text = re.sub(r"_([^_\n]+)_", r"<em>\1</em>", text)
    # 3. Asterisk italics (single asterisks only)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    return text

def render(chapter_path: Path) -> str:
    raw = chapter_path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    # First 3 non-empty lines = "CHAPTER N" / blank / "TITLE"
    chap_num = lines[0].strip() if lines else "CHAPTER"
    chap_title = ""
    body_start = 1
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip():
            chap_title = ln.strip()
            body_start = i + 1
            break

    body = "\n".join(lines[body_start:])
    # Split into paragraphs on blank lines
    paragraphs = re.split(r"\n\s*\n", body)
    blocks = []
    first = True
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # Treat a paragraph that is just a divider (e.g. "#") as a break
        if p in {"#", "---", "***"}:
            blocks.append('<div class="break">* * *</div>')
            first = True
            continue
        # Collapse internal newlines within a paragraph
        text = " ".join(p.split())
        text = render_inline(text)
        cls = "first" if first else ""
        blocks.append(f'<p class="{cls}">{text}</p>')
        first = False

    body_html = "\n".join(blocks)
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>{chap_num} — {chap_title}</title>
<style>{CSS}</style></head>
<body>
<div class="chap-num">{chap_num}</div>
<h1 class="chap-title">{chap_title}</h1>
{body_html}
</body></html>"""

def find_chapter(chapter_id: str) -> Path:
    if chapter_id.lower() == "ep":
        return next(CHAPTERS.glob("RESONANCE_EP_*.txt"))
    m = re.match(r"(?:ch)?(\d+)([a-z]?)", chapter_id.lower())
    if not m:
        raise SystemExit(f"unrecognized chapter id: {chapter_id}")
    num, suffix = m.group(1), m.group(2).upper()
    pattern = f"RESONANCE_CH{num}{suffix}_*.txt"
    matches = list(CHAPTERS.glob(pattern))
    if not matches:
        raise SystemExit(f"no chapter file matching {pattern}")
    return matches[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: reader.py <chapter_id, e.g. 15, ch15, ep>")
    chap_id = sys.argv[1]
    path = find_chapter(chap_id)
    html = render(path)
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"{path.stem}.html"
    out_path.write_text(html, encoding="utf-8")
    print(out_path)
