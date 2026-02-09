#!/usr/bin/env python3
"""
Quote Curator Workflow

Integrates the QUOTE_BANK.yaml with the Go Squad Framework.
Demonstrates how the quote_curator agent operates within its lane.

Usage:
    python quote_curator_workflow.py assess "Quote text here"
    python quote_curator_workflow.py find --theme love --twitter
    python quote_curator_workflow.py report chapter 28
    python quote_curator_workflow.py stats
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_architecture.query import StateQuery
from state_architecture.process_log import ProcessLog

# Agent identity
AGENT_ROLE = 'quote_curator'
LANE = 'marketing'


def assess_quote(text: str):
    """
    Assess a quote for social media readiness.
    Uses LLM prompt generation from StateQuery.
    """
    sq = StateQuery(project='remanence')
    log = ProcessLog(project='remanence')

    # Generate assessment prompt
    result = sq.quote_assess_prompt(text)

    if result.success:
        print("\n" + "="*60)
        print("QUOTE ASSESSMENT")
        print("="*60)
        print(f"\nQuote: \"{text}\"")
        print(f"Length: {result.data['length']} characters")

        # Platform fit
        length = result.data['length']
        platforms = []
        if length <= 280:
            platforms.append("Twitter/X")
        if length <= 500:
            platforms.append("Instagram")
        if length <= 700:
            platforms.append("Facebook")
        platforms.append("Blog")

        print(f"Platforms: {', '.join(platforms)}")
        print("\n" + "-"*60)
        print("LLM PROMPT FOR SEMANTIC ASSESSMENT:")
        print("-"*60)
        print(result.data['prompt'])

        # Log the action
        log.record(
            agent_role=AGENT_ROLE,
            action_type='assess',
            target='quote',
            input_summary=f'Assess quote: "{text[:50]}..."',
            output_summary=f'Generated assessment prompt, {length} chars',
            status='success',
            lane_scope=LANE,
        )


def find_quotes(theme: str = None, character: str = None, twitter: bool = False, unused: bool = True):
    """
    Find quotes matching criteria.
    """
    sq = StateQuery(project='remanence')
    log = ProcessLog(project='remanence')

    max_length = 280 if twitter else None

    result = sq.quotes(
        theme=theme,
        character=character,
        max_length=max_length,
        unused_only=unused,
    )

    if result.success:
        quotes = result.data
        print(f"\n{'='*60}")
        print(f"QUOTE SEARCH RESULTS")
        print(f"{'='*60}")

        filters = []
        if theme:
            filters.append(f"theme={theme}")
        if character:
            filters.append(f"character={character}")
        if twitter:
            filters.append("twitter-ready")
        if unused:
            filters.append("unused")

        print(f"Filters: {', '.join(filters) if filters else 'none'}")
        print(f"Found: {len(quotes)} quotes\n")

        for q in quotes[:10]:  # Limit display
            status = "[READY]" if q.get('social_ready') else "[pending]"
            print(f"{status} [{q['id']}] ({q['length']} chars)")
            print(f"  \"{q['text'][:80]}{'...' if len(q['text']) > 80 else ''}\"")
            print(f"  Character: {q.get('character', 'unknown')}")
            print(f"  Themes: {', '.join(q.get('themes', []))}")
            print()

        if len(quotes) > 10:
            print(f"... and {len(quotes) - 10} more")

        # Log
        log.record(
            agent_role=AGENT_ROLE,
            action_type='query',
            target='quote_bank',
            input_summary=f'Search: {filters}',
            output_summary=f'Found {len(quotes)} quotes',
            status='success',
            lane_scope=LANE,
        )

    else:
        print(f"Error: {result.data}")


def chapter_report(chapter_num: int):
    """
    Generate quote report for a chapter.
    """
    sq = StateQuery(project='remanence')
    log = ProcessLog(project='remanence')

    # Get chapter content
    chapter_result = sq.chapter(chapter_num)

    if not chapter_result.success:
        print(f"Error: {chapter_result.data}")
        return

    # Get existing quotes from this chapter
    all_quotes = sq.quotes(social_ready_only=False)

    if all_quotes.success:
        chapter_quotes = [q for q in all_quotes.data if q.get('chapter') == chapter_num]

        print(f"\n{'='*60}")
        print(f"QUOTE REPORT: Chapter {chapter_num}")
        print(f"{'='*60}")
        print(f"\nChapter: {chapter_result.data['title']}")
        print(f"Word Count: {chapter_result.data['word_count']}")
        print(f"\nExisting Quotes from Chapter: {len(chapter_quotes)}")

        # Categorize
        ready = [q for q in chapter_quotes if q.get('social_ready')]
        pending = [q for q in chapter_quotes if not q.get('social_ready')]

        print(f"  Social Ready: {len(ready)}")
        print(f"  Pending Review: {len(pending)}")

        if ready:
            print(f"\n--- READY QUOTES ---")
            for q in ready:
                print(f"[{q['id']}] \"{q['text'][:60]}...\"")

        if pending:
            print(f"\n--- PENDING QUOTES ---")
            for q in pending[:5]:
                print(f"[{q['id']}] \"{q['text'][:60]}...\"")

        # Log
        log.record(
            agent_role=AGENT_ROLE,
            action_type='report',
            target=f'chapter_{chapter_num}',
            input_summary=f'Generate report for chapter {chapter_num}',
            output_summary=f'{len(chapter_quotes)} quotes, {len(ready)} ready',
            status='success',
            lane_scope=LANE,
        )


def show_stats():
    """
    Show quote bank statistics.
    """
    sq = StateQuery(project='remanence')
    log = ProcessLog(project='remanence')

    result = sq.quotes(social_ready_only=False)

    if result.success:
        quotes = result.data

        print(f"\n{'='*60}")
        print("QUOTE BANK STATISTICS")
        print(f"{'='*60}")

        total = len(quotes)
        ready = sum(1 for q in quotes if q.get('social_ready'))
        used = sum(1 for q in quotes if q.get('used'))
        unused_ready = sum(1 for q in quotes if q.get('social_ready') and not q.get('used'))

        print(f"\nTotal Quotes: {total}")
        print(f"Social Ready: {ready}")
        print(f"Used: {used}")
        print(f"Available (ready, unused): {unused_ready}")

        # Platform breakdown
        twitter_ready = sum(1 for q in quotes if q['length'] <= 280 and q.get('social_ready'))
        insta_ready = sum(1 for q in quotes if q['length'] <= 500 and q.get('social_ready'))

        print(f"\nPlatform Ready:")
        print(f"  Twitter/X (<=280): {twitter_ready}")
        print(f"  Instagram (<=500): {insta_ready}")

        # By character
        by_char = {}
        for q in quotes:
            if q.get('social_ready'):
                c = q.get('character', 'unknown')
                by_char[c] = by_char.get(c, 0) + 1

        print(f"\nBy Character (ready only):")
        for c, count in sorted(by_char.items(), key=lambda x: -x[1]):
            print(f"  {c}: {count}")

        # By theme
        by_theme = {}
        for q in quotes:
            if q.get('social_ready'):
                for t in q.get('themes', []):
                    by_theme[t] = by_theme.get(t, 0) + 1

        print(f"\nBy Theme (ready only):")
        for t, count in sorted(by_theme.items(), key=lambda x: -x[1]):
            print(f"  {t}: {count}")

        # Log
        log.record(
            agent_role=AGENT_ROLE,
            action_type='query',
            target='quote_bank',
            input_summary='Generate statistics',
            output_summary=f'{total} total, {unused_ready} available',
            status='success',
            lane_scope=LANE,
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Quote Curator Workflow (Go Squad Framework)"
    )
    subparsers = parser.add_subparsers(dest='command')

    # Assess command
    assess_parser = subparsers.add_parser('assess', help='Assess a quote')
    assess_parser.add_argument('text', help='Quote text to assess')

    # Find command
    find_parser = subparsers.add_parser('find', help='Find quotes')
    find_parser.add_argument('--theme', '-t', help='Filter by theme')
    find_parser.add_argument('--character', '-c', help='Filter by character')
    find_parser.add_argument('--twitter', action='store_true', help='Twitter-ready only')
    find_parser.add_argument('--all', action='store_true', help='Include used quotes')

    # Report command
    report_parser = subparsers.add_parser('report', help='Chapter quote report')
    report_parser.add_argument('chapter', type=int, help='Chapter number')

    # Stats command
    subparsers.add_parser('stats', help='Show quote bank statistics')

    args = parser.parse_args()

    if args.command == 'assess':
        assess_quote(args.text)
    elif args.command == 'find':
        find_quotes(
            theme=args.theme,
            character=args.character,
            twitter=args.twitter,
            unused=not args.all,
        )
    elif args.command == 'report':
        chapter_report(args.chapter)
    elif args.command == 'stats':
        show_stats()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
