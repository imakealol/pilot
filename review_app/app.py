import os
import re
import glob
import yaml
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

BASE = Path(__file__).parent.parent / "RESONANCE"
CHAPTERS_DIR = BASE / "chapters"
DATA_DIR = BASE / "data"

_chapters_cache = None


def sort_key(key):
    if key == "ep":
        return (999, "")
    m = re.match(r"ch(\d+)([a-z]?)", key)
    if m:
        return (int(m.group(1)), m.group(2) or "")
    return (0, key)


def find_chapter_file(chapter_id):
    if chapter_id == "ep":
        matches = glob.glob(str(CHAPTERS_DIR / "RESONANCE_EP_*.txt"))
        return Path(matches[0]) if matches else None

    m = re.match(r"ch(\d+)([a-z]?)", chapter_id)
    if not m:
        return None

    num = m.group(1)
    suffix = m.group(2)

    if suffix:
        # For ch24a prefer the _TRANSCRIPT_ file (readable prose)
        transcript = CHAPTERS_DIR / f"_TRANSCRIPT_CH{num}{suffix.upper()}_In_The_Blind.txt"
        if transcript.exists():
            return transcript
        matches = glob.glob(str(CHAPTERS_DIR / f"*CH{num}{suffix.upper()}*.txt"))
        return Path(matches[0]) if matches else None

    matches = glob.glob(str(CHAPTERS_DIR / f"RESONANCE_CH{num}_*.txt"))
    return Path(matches[0]) if matches else None


def load_chapters_index():
    global _chapters_cache
    if _chapters_cache is not None:
        return _chapters_cache

    with open(DATA_DIR / "CHAPTERS.yaml") as f:
        data = yaml.safe_load(f)

    states = data.get("chapter_states", {})
    chapters = []

    for key in sorted(states.keys(), key=sort_key):
        ch = states[key]
        file_path = find_chapter_file(key)
        if file_path and file_path.exists():
            chapters.append({
                "id": key,
                "title": ch.get("title", key.upper()),
                "pov": ch.get("pov", ""),
                "word_count": ch.get("word_count", 0),
                "label": f"CH{key[2:].upper() if key != 'ep' else 'EP'}: {ch.get('title', '')}",
            })

    _chapters_cache = chapters
    return chapters


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chapters")
def get_chapters():
    return jsonify(load_chapters_index())


@app.route("/api/chapter/<chapter_id>")
def get_chapter(chapter_id):
    file_path = find_chapter_file(chapter_id)
    if not file_path or not file_path.exists():
        return jsonify({"error": "Chapter not found"}), 404

    text = file_path.read_text(encoding="utf-8")

    # Get metadata from index
    chapters = load_chapters_index()
    meta = next((c for c in chapters if c["id"] == chapter_id), {})

    return jsonify({
        "id": chapter_id,
        "text": text,
        "title": meta.get("title", ""),
        "pov": meta.get("pov", ""),
        "label": meta.get("label", ""),
        "word_count": meta.get("word_count", 0),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, port=port, threaded=True)
