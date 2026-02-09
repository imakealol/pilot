#!/usr/bin/env python3
"""
Quote Query Interface for Remanence
Query the QUOTE_BANK.yaml for social media promotion.

Usage:
    python quote_query.py                           # Show all curated quotes
    python quote_query.py --character seventeen     # Filter by character
    python quote_query.py --theme love              # Filter by theme
    python quote_query.py --max-length 280          # Twitter-ready quotes
    python quote_query.py --unused                  # Only unused quotes
    python quote_query.py --random                  # Get random quote
    python quote_query.py --mark-used Q001          # Mark quote as used
    python quote_query.py --stats                   # Show statistics
"""

import yaml
import random
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

QUOTE_BANK_PATH = Path(__file__).parent / "context/QUOTE_BANK.yaml"


def load_quotes() -> Dict:
    """Load the quote bank from YAML."""
    if not QUOTE_BANK_PATH.exists():
        print(f"Quote bank not found at {QUOTE_BANK_PATH}")
        print("Run: python quote_extractor.py")
        return {"quotes": []}

    with open(QUOTE_BANK_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_quotes(data: Dict):
    """Save the quote bank to YAML."""
    with open(QUOTE_BANK_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


def filter_quotes(quotes: List[Dict],
                  character: Optional[str] = None,
                  theme: Optional[str] = None,
                  max_length: Optional[int] = None,
                  min_length: Optional[int] = None,
                  quote_type: Optional[str] = None,
                  chapter: Optional[int] = None,
                  standalone_only: bool = False,
                  curated_only: bool = True,
                  unused_only: bool = False) -> List[Dict]:
    """Filter quotes based on criteria."""
    results = []

    for q in quotes:
        # Character filter
        if character and q.get("character", "").lower() != character.lower():
            continue

        # Theme filter
        if theme and theme.lower() not in [t.lower() for t in q.get("themes", [])]:
            continue

        # Length filters
        if max_length and q.get("length", 0) > max_length:
            continue
        if min_length and q.get("length", 0) < min_length:
            continue

        # Type filter
        if quote_type and q.get("type", "").lower() != quote_type.lower():
            continue

        # Chapter filter
        if chapter and q.get("chapter", 0) != chapter:
            continue

        # Standalone filter
        if standalone_only and not q.get("standalone", False):
            continue

        # Curated filter (social_ready)
        if curated_only and not q.get("social_ready", False):
            continue

        # Unused filter
        if unused_only and q.get("used", False):
            continue

        results.append(q)

    return results


def format_quote(q: Dict, verbose: bool = False) -> str:
    """Format a quote for display."""
    lines = []

    # Quote ID and status
    status = []
    if q.get("social_ready"):
        status.append("✓ READY")
    if q.get("used"):
        status.append("USED")
    status_str = f" [{', '.join(status)}]" if status else ""

    lines.append(f"\n{'='*60}")
    lines.append(f"[{q['id']}]{status_str} ({q['length']} chars)")
    lines.append(f"{'='*60}")

    # The quote text
    lines.append(f"\n\"{q['text']}\"\n")

    # Metadata
    lines.append(f"  Character: {q.get('character', 'unknown')}")
    lines.append(f"  Chapter:   {q.get('chapter', '?')}")
    lines.append(f"  Type:      {q.get('type', 'unknown')}")

    if q.get("themes"):
        lines.append(f"  Themes:    {', '.join(q['themes'])}")

    lines.append(f"  Standalone: {'Yes' if q.get('standalone') else 'No'}")

    if verbose and q.get("notes"):
        lines.append(f"  Notes:     {q['notes']}")

    # Platform suitability
    platforms = []
    if q["length"] <= 280:
        platforms.append("Twitter/X")
    if q["length"] <= 500:
        platforms.append("Instagram")
    if q["length"] <= 700:
        platforms.append("Facebook")
    platforms.append("Blog")

    lines.append(f"  Platforms: {', '.join(platforms)}")

    return "\n".join(lines)


def show_stats(quotes: List[Dict]):
    """Show statistics about the quote bank."""
    print("\n" + "="*60)
    print("QUOTE BANK STATISTICS")
    print("="*60)

    total = len(quotes)
    curated = sum(1 for q in quotes if q.get("social_ready"))
    used = sum(1 for q in quotes if q.get("used"))
    unused_curated = sum(1 for q in quotes if q.get("social_ready") and not q.get("used"))

    print(f"\nTotal quotes:           {total}")
    print(f"Curated (social_ready): {curated}")
    print(f"Used:                   {used}")
    print(f"Available (curated, unused): {unused_curated}")

    # By type
    print("\nBy Type:")
    by_type = {}
    for q in quotes:
        t = q.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    for t, count in sorted(by_type.items()):
        print(f"  {t}: {count}")

    # By character
    print("\nBy Character:")
    by_char = {}
    for q in quotes:
        c = q.get("character", "unknown")
        by_char[c] = by_char.get(c, 0) + 1
    for c, count in sorted(by_char.items(), key=lambda x: -x[1]):
        print(f"  {c}: {count}")

    # By theme
    print("\nBy Theme:")
    by_theme = {}
    for q in quotes:
        for theme in q.get("themes", []):
            by_theme[theme] = by_theme.get(theme, 0) + 1
    for t, count in sorted(by_theme.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")

    # Platform readiness
    print("\nPlatform Readiness:")
    twitter = sum(1 for q in quotes if q["length"] <= 280)
    instagram = sum(1 for q in quotes if q["length"] <= 500)
    print(f"  Twitter/X (<=280):  {twitter}")
    print(f"  Instagram (<=500):  {instagram}")

    # Curated platform readiness
    print("\nCurated Platform Readiness:")
    twitter_ready = sum(1 for q in quotes if q["length"] <= 280 and q.get("social_ready"))
    instagram_ready = sum(1 for q in quotes if q["length"] <= 500 and q.get("social_ready"))
    print(f"  Twitter/X (<=280):  {twitter_ready}")
    print(f"  Instagram (<=500):  {instagram_ready}")


def mark_used(quote_id: str, data: Dict) -> bool:
    """Mark a quote as used."""
    for q in data["quotes"]:
        if q["id"] == quote_id:
            q["used"] = True
            q["used_date"] = datetime.now().isoformat()
            save_quotes(data)
            print(f"Marked {quote_id} as used")
            return True
    print(f"Quote {quote_id} not found")
    return False


def mark_ready(quote_id: str, data: Dict, ready: bool = True) -> bool:
    """Mark a quote as social_ready."""
    for q in data["quotes"]:
        if q["id"] == quote_id:
            q["social_ready"] = ready
            save_quotes(data)
            status = "ready" if ready else "not ready"
            print(f"Marked {quote_id} as {status}")
            return True
    print(f"Quote {quote_id} not found")
    return False


def add_note(quote_id: str, note: str, data: Dict) -> bool:
    """Add a note to a quote."""
    for q in data["quotes"]:
        if q["id"] == quote_id:
            q["notes"] = note
            save_quotes(data)
            print(f"Added note to {quote_id}")
            return True
    print(f"Quote {quote_id} not found")
    return False


def interactive_review(quotes: List[Dict], data: Dict):
    """Interactive mode for reviewing and curating quotes."""
    print("\nINTERACTIVE REVIEW MODE")
    print("Commands: [y]es (mark ready), [n]o (skip), [u]sed, [q]uit, [s]kip to next")
    print("-" * 60)

    uncurated = [q for q in quotes if not q.get("social_ready")]

    for i, q in enumerate(uncurated):
        print(format_quote(q))
        print(f"\nProgress: {i+1}/{len(uncurated)}")

        while True:
            cmd = input("\nAction [y/n/u/s/q]: ").strip().lower()

            if cmd == 'y':
                mark_ready(q["id"], data, True)
                break
            elif cmd == 'n':
                break
            elif cmd == 'u':
                mark_used(q["id"], data)
                break
            elif cmd == 's':
                break
            elif cmd == 'q':
                print("Exiting review mode")
                return
            else:
                print("Unknown command. Use y/n/u/s/q")


def main():
    parser = argparse.ArgumentParser(description="Query Remanence quote bank")

    # Filter options
    parser.add_argument("--character", "-c", help="Filter by character")
    parser.add_argument("--theme", "-t", help="Filter by theme")
    parser.add_argument("--max-length", "-m", type=int, help="Maximum length")
    parser.add_argument("--min-length", type=int, help="Minimum length")
    parser.add_argument("--type", dest="quote_type", help="Filter by type (dialogue/prose/thematic)")
    parser.add_argument("--chapter", type=int, help="Filter by chapter number")
    parser.add_argument("--standalone", action="store_true", help="Only standalone quotes")
    parser.add_argument("--unused", "-u", action="store_true", help="Only unused quotes")

    # Include uncurated quotes
    parser.add_argument("--all", "-a", action="store_true",
                        help="Include uncurated quotes (not social_ready)")

    # Actions
    parser.add_argument("--random", "-r", action="store_true", help="Get random quote")
    parser.add_argument("--stats", "-s", action="store_true", help="Show statistics")
    parser.add_argument("--mark-used", metavar="ID", help="Mark quote as used")
    parser.add_argument("--mark-ready", metavar="ID", help="Mark quote as social_ready")
    parser.add_argument("--unmark-ready", metavar="ID", help="Unmark quote as social_ready")
    parser.add_argument("--add-note", nargs=2, metavar=("ID", "NOTE"), help="Add note to quote")
    parser.add_argument("--review", action="store_true", help="Interactive review mode")

    # Output options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of results")
    parser.add_argument("--twitter", action="store_true", help="Shortcut for --max-length 280")
    parser.add_argument("--instagram", action="store_true", help="Shortcut for --max-length 500")

    args = parser.parse_args()

    # Load data
    data = load_quotes()
    if not data.get("quotes"):
        return

    quotes = data["quotes"]

    # Handle actions
    if args.mark_used:
        mark_used(args.mark_used, data)
        return

    if args.mark_ready:
        mark_ready(args.mark_ready, data, True)
        return

    if args.unmark_ready:
        mark_ready(args.unmark_ready, data, False)
        return

    if args.add_note:
        add_note(args.add_note[0], args.add_note[1], data)
        return

    if args.stats:
        show_stats(quotes)
        return

    if args.review:
        interactive_review(quotes, data)
        return

    # Apply shortcuts
    max_length = args.max_length
    if args.twitter:
        max_length = 280
    elif args.instagram:
        max_length = 500

    # Filter quotes
    curated_only = not args.all

    filtered = filter_quotes(
        quotes,
        character=args.character,
        theme=args.theme,
        max_length=max_length,
        min_length=args.min_length,
        quote_type=args.quote_type,
        chapter=args.chapter,
        standalone_only=args.standalone,
        curated_only=curated_only,
        unused_only=args.unused,
    )

    if not filtered:
        print("No quotes match the specified criteria.")
        if curated_only:
            print("Try --all to include uncurated quotes.")
        return

    # Random selection
    if args.random:
        filtered = [random.choice(filtered)]

    # Apply limit
    if args.limit:
        filtered = filtered[:args.limit]

    # Display results
    print(f"\nFound {len(filtered)} quote(s)")

    for q in filtered:
        print(format_quote(q, verbose=args.verbose))


if __name__ == "__main__":
    main()
