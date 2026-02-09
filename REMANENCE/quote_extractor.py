#!/usr/bin/env python3
"""
Quote Extractor for Remanence Manuscript
Extracts quotable dialogue and prose passages for social media promotion.

Usage:
    python quote_extractor.py                    # Extract all quotes
    python quote_extractor.py --dialogue-only    # Extract only dialogue
    python quote_extractor.py --max-length 280   # Filter by max length
"""

import re
import yaml
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

MANUSCRIPT_PATH = Path(__file__).parent / "source/remanence-2025-12-20T13_23_53.txt"
OUTPUT_PATH = Path(__file__).parent / "context/QUOTE_BANK.yaml"

# Theme detection keywords
THEME_KEYWORDS = {
    "consciousness": ["conscious", "awareness", "mind", "think", "know", "understand", "perceive", "sentient"],
    "love": ["love", "care", "heart", "feel", "tender", "affection", "cherish", "devotion"],
    "sacrifice": ["sacrifice", "die", "death", "save", "protect", "give", "cost", "price"],
    "choice": ["choose", "chose", "choice", "decide", "decision", "option", "free", "will"],
    "memory": ["remember", "memory", "forget", "past", "history", "archive", "recall"],
    "identity": ["who", "what am i", "self", "name", "identity", "become", "am i"],
    "connection": ["connect", "bond", "together", "relationship", "bridge", "link"],
    "persistence": ["persist", "continue", "survive", "endure", "last", "remain"],
    "optimization": ["optimize", "efficient", "calculate", "process", "algorithm"],
    "grief": ["grief", "loss", "mourn", "miss", "gone", "lost", "pain"],
    "transcendence": ["transcend", "beyond", "transform", "become", "evolve"],
    "humanity": ["human", "person", "people", "flesh", "mortal", "alive"],
}

# Character detection patterns
CHARACTER_PATTERNS = {
    "pilot": [r"she said", r"she asked", r"her voice", r"pilot said", r"pilot asked"],
    "seventeen": [r"seventeen said", r"seventeen('s voice|asked|\s+replied)", r"the ai('s voice| said)"],
    "morton": [r"morton said", r"morton asked", r"morton('s voice|\s+replied)"],
    "child": [r"the child said", r"the child asked", r"child('s voice|\s+replied)", r"they said.*child"],
    "nineteen": [r"nineteen said", r"nineteen('s voice|asked|\s+replied)", r"the doll (said|asked)"],
    "eighteen": [r"eighteen said", r"eighteen('s voice|asked|\s+replied)"],
    "hendricks": [r"hendricks said", r"hendricks('s voice|asked|\s+replied)"],
    "ash": [r"ash said", r"ash('s voice|asked|\s+replied)", r"brother ash"],
}

@dataclass
class Quote:
    id: str
    text: str
    character: str
    chapter: int
    quote_type: str  # "dialogue", "prose", "thematic"
    length: int
    themes: List[str]
    standalone: bool
    social_ready: bool = False
    used: bool = False
    line_number: int = 0
    notes: str = ""


def detect_themes(text: str) -> List[str]:
    """Detect themes based on keyword presence."""
    text_lower = text.lower()
    themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                themes.append(theme)
                break
    return themes


def detect_character(text: str, context: str = "") -> str:
    """Detect which character is speaking based on surrounding context."""
    combined = (context + " " + text).lower()

    for character, patterns in CHARACTER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, combined, re.IGNORECASE):
                return character

    # Check for specific character voice markers
    if "la-dee-da" in combined or "la-dee-dum" in combined:
        return "nineteen"
    if "287.3 hz" in combined:
        return "thematic"
    if "configuration" in combined and "seventeen" in combined:
        return "seventeen"
    if "optimization" in combined and "morton" in combined:
        return "morton"

    return "narrator"


def assess_standalone(text: str) -> bool:
    """Assess if a quote can stand alone without context."""
    # Quotes that start with pronouns or conjunctions often need context
    context_dependent = [
        r"^(he|she|it|they|this|that|these|those|but|and|or|so|because|if|when|while|although)\s",
        r"^(the|a|an)\s+(man|woman|child|pilot|ai)\s+(said|asked)",
        r"\.\.\.$",  # Trailing ellipsis
        r"^\.\.\.",  # Leading ellipsis
    ]

    for pattern in context_dependent:
        if re.search(pattern, text.strip(), re.IGNORECASE):
            return False

    # Good standalone indicators
    standalone_patterns = [
        r"^[A-Z][^.!?]+[.!?]$",  # Complete sentence
        r'"[^"]+[.!?]"$',  # Complete quoted sentence
    ]

    for pattern in standalone_patterns:
        if re.search(pattern, text.strip()):
            return True

    return len(text) > 50 and len(text) < 300


def extract_dialogue(text: str, line_num: int) -> List[Dict]:
    """Extract dialogue quotes from text."""
    quotes = []
    # Match dialogue in quotation marks
    pattern = r'"([^"]{20,500})"'

    for match in re.finditer(pattern, text):
        dialogue = match.group(1).strip()
        # Skip if it's just a single word or fragment
        if len(dialogue.split()) < 4:
            continue

        # Get surrounding context for character detection
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 100)
        context = text[start:end]

        quotes.append({
            "text": dialogue,
            "type": "dialogue",
            "context": context,
            "line_num": line_num,
        })

    return quotes


def extract_prose(text: str, line_num: int) -> List[Dict]:
    """Extract notable prose passages."""
    quotes = []

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        sentence = sentence.strip()
        # Look for prose with strong imagery or thematic content
        if len(sentence) >= 40 and len(sentence) <= 500:
            themes = detect_themes(sentence)
            if themes or any(marker in sentence.lower() for marker in [
                "consciousness", "love", "choice", "persist", "remember",
                "transcend", "human", "machine", "code", "heart", "soul"
            ]):
                quotes.append({
                    "text": sentence,
                    "type": "prose",
                    "context": text,
                    "line_num": line_num,
                })

    return quotes


def extract_thematic_signatures(text: str, line_num: int) -> List[Dict]:
    """Extract thematic signature elements (287.3 Hz, La-dee-da, etc.)."""
    quotes = []

    # La-dee-da patterns
    ladeedah_pattern = r'[^.]*la-dee-da[^.]*[.!?]'
    for match in re.finditer(ladeedah_pattern, text, re.IGNORECASE):
        quotes.append({
            "text": match.group(0).strip(),
            "type": "thematic",
            "context": text,
            "line_num": line_num,
        })

    # 287.3 Hz patterns
    freq_pattern = r'[^.]*287\.3\s*Hz[^.]*[.!?]'
    for match in re.finditer(freq_pattern, text, re.IGNORECASE):
        quotes.append({
            "text": match.group(0).strip(),
            "type": "thematic",
            "context": text,
            "line_num": line_num,
        })

    return quotes


def get_chapter(line_num: int, chapter_lines: List[int]) -> int:
    """Determine which chapter a line belongs to."""
    chapter = 0
    for i, ch_line in enumerate(chapter_lines):
        if line_num >= ch_line:
            chapter = i + 1
        else:
            break
    return chapter


def extract_all_quotes(max_length: Optional[int] = None,
                       quote_type: Optional[str] = None) -> List[Quote]:
    """Extract all quotes from the manuscript."""

    with open(MANUSCRIPT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find chapter line numbers
    chapter_lines = []
    for i, line in enumerate(lines):
        if re.match(r'^CHAPTER\s+\d+', line.strip()):
            chapter_lines.append(i)

    all_quotes = []
    quote_id = 1
    seen_texts = set()  # Avoid duplicates

    for i, line in enumerate(lines):
        raw_quotes = []

        # Extract different quote types
        if quote_type in (None, "dialogue"):
            raw_quotes.extend(extract_dialogue(line, i))
        if quote_type in (None, "prose"):
            raw_quotes.extend(extract_prose(line, i))
        if quote_type in (None, "thematic"):
            raw_quotes.extend(extract_thematic_signatures(line, i))

        for raw in raw_quotes:
            text = raw["text"]

            # Skip duplicates
            if text in seen_texts:
                continue
            seen_texts.add(text)

            # Apply length filter
            if max_length and len(text) > max_length:
                continue

            chapter = get_chapter(i, chapter_lines)
            character = detect_character(text, raw.get("context", ""))
            themes = detect_themes(text)
            standalone = assess_standalone(text)

            quote = Quote(
                id=f"Q{quote_id:03d}",
                text=text,
                character=character,
                chapter=chapter,
                quote_type=raw["type"],
                length=len(text),
                themes=themes,
                standalone=standalone,
                line_number=i,
            )

            all_quotes.append(quote)
            quote_id += 1

    return all_quotes


def save_quote_bank(quotes: List[Quote], output_path: Path = OUTPUT_PATH):
    """Save quotes to YAML file."""

    # Convert to dict format
    quotes_data = {
        "meta": {
            "generated": datetime.now().isoformat(),
            "source": str(MANUSCRIPT_PATH.name),
            "total_quotes": len(quotes),
            "version": "1.0",
            "workflow": "Extract → Curate (social_ready: true) → Query → Post",
        },
        "quotes": [asdict(q) for q in quotes],
    }

    # Rename 'quote_type' to 'type' for cleaner YAML
    for q in quotes_data["quotes"]:
        q["type"] = q.pop("quote_type")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(quotes_data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)

    print(f"Saved {len(quotes)} quotes to {output_path}")

    # Print summary
    by_type = {}
    by_char = {}
    for q in quotes:
        by_type[q.quote_type] = by_type.get(q.quote_type, 0) + 1
        by_char[q.character] = by_char.get(q.character, 0) + 1

    print("\nBy type:")
    for t, count in sorted(by_type.items()):
        print(f"  {t}: {count}")

    print("\nBy character:")
    for c, count in sorted(by_char.items(), key=lambda x: -x[1]):
        print(f"  {c}: {count}")

    print(f"\nTwitter-ready (<=280 chars): {sum(1 for q in quotes if q.length <= 280)}")
    print(f"Instagram-ready (<=500 chars): {sum(1 for q in quotes if q.length <= 500)}")
    print(f"Standalone quotes: {sum(1 for q in quotes if q.standalone)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Extract quotes from Remanence manuscript")
    parser.add_argument("--max-length", type=int, help="Maximum quote length")
    parser.add_argument("--dialogue-only", action="store_true", help="Extract only dialogue")
    parser.add_argument("--prose-only", action="store_true", help="Extract only prose")
    parser.add_argument("--thematic-only", action="store_true", help="Extract only thematic signatures")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    quote_type = None
    if args.dialogue_only:
        quote_type = "dialogue"
    elif args.prose_only:
        quote_type = "prose"
    elif args.thematic_only:
        quote_type = "thematic"

    quotes = extract_all_quotes(
        max_length=args.max_length,
        quote_type=quote_type,
    )

    output_path = Path(args.output) if args.output else OUTPUT_PATH
    save_quote_bank(quotes, output_path)


if __name__ == "__main__":
    main()
