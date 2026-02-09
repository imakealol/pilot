#!/usr/bin/env python3
"""
Go Squad Framework - State Query Interface

RLM-based query system: code for structure, LLM for semantics.

Usage:
    from query import StateQuery
    sq = StateQuery(project='remanence')

    # Code-based queries (fast, deterministic)
    sq.character('seventeen')
    sq.chapter(28)
    sq.quotes(character='morton', max_length=280)
    sq.callbacks_pending()

    # LLM-augmented queries (semantic understanding)
    sq.voice_check('seventeen', '"I chose this."')
    sq.theme_detect(passage)
    sq.quote_assess(text)
"""

import yaml
import re
import os
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime

# Project roots
PROJECTS = {
    'remanence': Path('/workspaces/pilot/REMANENCE'),
    'resonance': Path('/workspaces/pilot/RESONANCE'),
}


@dataclass
class QueryResult:
    """Standardized query result."""
    success: bool
    data: Any
    source: str  # Where the data came from
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class StateQuery:
    """
    RLM-style state query interface.

    Code handles: file search, YAML parsing, filtering, metrics
    LLM handles: semantic matching, voice validation, theme detection
    """

    def __init__(self, project: str = 'remanence'):
        if project not in PROJECTS:
            raise ValueError(f"Unknown project: {project}. Available: {list(PROJECTS.keys())}")

        self.project = project
        self.root = PROJECTS[project]
        self._cache = {}

        # Standard paths
        self.paths = {
            'characters': self.root / 'context' / 'ENTITY_CATALOG.yaml',
            'quotes': self.root / 'context' / 'QUOTE_BANK.yaml',
            'chapters': self.root / 'chapters',
            'source': self.root / 'source',
        }

        # Resonance has different structure
        if project == 'resonance':
            self.paths['characters'] = self.root / 'data' / 'CHARACTERS.yaml'
            self.paths['world'] = self.root / 'data' / 'WORLD.yaml'

    # =========================================================================
    # CODE-BASED QUERIES (Fast, Deterministic)
    # =========================================================================

    def character(self, name: str) -> QueryResult:
        """Get character data by name."""
        data = self._load_yaml(self.paths['characters'])
        if not data:
            return QueryResult(False, None, str(self.paths['characters']))

        # Search in characters section
        characters = data.get('characters', data.get('entities', {}).get('characters', []))

        name_lower = name.lower()
        for char in characters:
            char_name = char.get('name', char.get('id', '')).lower()
            aliases = [a.lower() for a in char.get('aliases', [])]

            if name_lower == char_name or name_lower in aliases:
                return QueryResult(True, char, str(self.paths['characters']))

        return QueryResult(False, f"Character '{name}' not found", str(self.paths['characters']))

    def chapter(self, number: int) -> QueryResult:
        """Get chapter file and metadata by number."""
        chapter_dir = self.paths['chapters']

        if not chapter_dir.exists():
            return QueryResult(False, f"Chapters directory not found: {chapter_dir}", str(chapter_dir))

        # Find matching chapter file
        patterns = [
            f"*CH{number}_*.txt",
            f"*CH{number:02d}_*.txt",
            f"*CHAPTER_{number}*.txt",
        ]

        for pattern in patterns:
            matches = list(chapter_dir.glob(pattern))
            if matches:
                chapter_file = matches[0]
                content = chapter_file.read_text(encoding='utf-8')
                word_count = len(content.split())

                return QueryResult(True, {
                    'path': str(chapter_file),
                    'number': number,
                    'title': self._extract_title(chapter_file.name),
                    'word_count': word_count,
                    'content': content,
                }, str(chapter_file))

        return QueryResult(False, f"Chapter {number} not found", str(chapter_dir))

    def quotes(self,
               character: Optional[str] = None,
               theme: Optional[str] = None,
               max_length: Optional[int] = None,
               min_length: Optional[int] = None,
               quote_type: Optional[str] = None,
               unused_only: bool = False,
               social_ready_only: bool = True) -> QueryResult:
        """Query quote bank with filters."""
        data = self._load_yaml(self.paths['quotes'])
        if not data:
            return QueryResult(False, "Quote bank not found", str(self.paths['quotes']))

        quotes = data.get('quotes', [])
        results = []

        for q in quotes:
            # Apply filters
            if character and q.get('character', '').lower() != character.lower():
                continue
            if theme and theme.lower() not in [t.lower() for t in q.get('themes', [])]:
                continue
            if max_length and q.get('length', 0) > max_length:
                continue
            if min_length and q.get('length', 0) < min_length:
                continue
            if quote_type and q.get('type', '').lower() != quote_type.lower():
                continue
            if unused_only and q.get('used', False):
                continue
            if social_ready_only and not q.get('social_ready', False):
                continue

            results.append(q)

        return QueryResult(True, results, str(self.paths['quotes']))

    def callbacks_pending(self, through_chapter: Optional[int] = None) -> QueryResult:
        """Find callbacks/setups that haven't paid off yet."""
        # This requires a callbacks registry - check if it exists
        callbacks_path = self.root / 'context' / 'CALLBACKS.yaml'

        if not callbacks_path.exists():
            # Try HANDOFF.md for callbacks info
            handoff = Path('/workspaces/pilot/HANDOFF.md')
            if handoff.exists():
                content = handoff.read_text(encoding='utf-8')
                # Extract callbacks section
                callbacks_match = re.search(
                    r'## CALLBACKS THAT MUST PAY OFF\n\n(.*?)(?=\n## |\n---|\Z)',
                    content, re.DOTALL
                )
                if callbacks_match:
                    return QueryResult(True, {
                        'source': 'HANDOFF.md',
                        'raw': callbacks_match.group(1).strip()
                    }, str(handoff))

            return QueryResult(False, "No callbacks registry found", str(callbacks_path))

        data = self._load_yaml(callbacks_path)
        callbacks = data.get('callbacks', [])

        pending = [c for c in callbacks if not c.get('paid_off', False)]
        if through_chapter:
            pending = [c for c in pending if c.get('setup_chapter', 0) <= through_chapter]

        return QueryResult(True, pending, str(callbacks_path))

    def search_text(self, pattern: str, chapter: Optional[int] = None) -> QueryResult:
        """Search for text pattern in manuscript."""
        if chapter:
            result = self.chapter(chapter)
            if result.success:
                matches = list(re.finditer(pattern, result.data['content'], re.IGNORECASE))
                return QueryResult(True, {
                    'matches': len(matches),
                    'contexts': [m.group(0) for m in matches[:10]],
                    'chapter': chapter,
                }, result.source)
            return result

        # Search all chapters
        all_matches = []
        chapter_dir = self.paths['chapters']

        if chapter_dir.exists():
            for f in sorted(chapter_dir.glob('*.txt')):
                content = f.read_text(encoding='utf-8')
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                if matches:
                    all_matches.append({
                        'file': f.name,
                        'count': len(matches),
                        'samples': [m.group(0) for m in matches[:3]],
                    })

        return QueryResult(True, all_matches, str(chapter_dir))

    def word_count(self, chapter: Optional[int] = None) -> QueryResult:
        """Get word counts."""
        if chapter:
            result = self.chapter(chapter)
            if result.success:
                return QueryResult(True, result.data['word_count'], result.source)
            return result

        # Total word count
        total = 0
        by_chapter = {}
        chapter_dir = self.paths['chapters']

        if chapter_dir.exists():
            for f in sorted(chapter_dir.glob('*.txt')):
                content = f.read_text(encoding='utf-8')
                wc = len(content.split())
                total += wc
                by_chapter[f.name] = wc

        return QueryResult(True, {
            'total': total,
            'by_chapter': by_chapter,
        }, str(chapter_dir))

    # =========================================================================
    # LLM-AUGMENTED QUERIES (Semantic Understanding)
    # These return structured prompts for LLM evaluation
    # =========================================================================

    def voice_check_prompt(self, character: str, dialogue: str) -> QueryResult:
        """
        Generate prompt for voice validation.
        Returns structured prompt for LLM to evaluate.
        """
        char_result = self.character(character)
        if not char_result.success:
            return char_result

        char_data = char_result.data
        voice_markers = char_data.get('voice_markers', char_data.get('speech_patterns', []))
        forbidden = char_data.get('forbidden', char_data.get('never_says', []))

        prompt = f"""CHARACTER VOICE CHECK

Character: {character}
Voice Markers: {voice_markers}
Forbidden Phrases: {forbidden}

Proposed Dialogue:
"{dialogue}"

Evaluate:
1. Does this sound like {character}? (YES/NO/MAYBE)
2. What voice markers are present or missing?
3. Does it violate any forbidden patterns?
4. Suggested revision if needed.

Format response as:
VERDICT: [YES/NO/MAYBE]
MARKERS_PRESENT: [list]
MARKERS_MISSING: [list]
VIOLATIONS: [list or "none"]
REVISION: [suggestion or "none needed"]
"""

        return QueryResult(True, {
            'prompt': prompt,
            'character': character,
            'dialogue': dialogue,
            'voice_markers': voice_markers,
            'forbidden': forbidden,
        }, 'voice_check_prompt')

    def theme_detect_prompt(self, passage: str) -> QueryResult:
        """Generate prompt for theme detection."""
        prompt = f"""THEME DETECTION

Passage:
"{passage}"

Identify themes from this list:
- consciousness: awareness, sentience, understanding
- love: care, devotion, sacrifice for another
- sacrifice: giving up something precious
- choice: agency, decision, free will
- memory: remembering, forgetting, persistence
- identity: self-knowledge, who am I
- connection: bonds, relationships, bridges
- persistence: enduring, surviving
- optimization: efficiency, calculation
- grief: loss, mourning
- transcendence: transformation, becoming more
- humanity: what makes us human

Format response as:
PRIMARY_THEME: [strongest theme]
SECONDARY_THEMES: [list of other themes present]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASONING: [brief explanation]
"""

        return QueryResult(True, {'prompt': prompt, 'passage': passage}, 'theme_detect_prompt')

    def quote_assess_prompt(self, text: str) -> QueryResult:
        """Generate prompt for quote assessment."""
        prompt = f"""QUOTE ASSESSMENT FOR SOCIAL MEDIA

Quote:
"{text}"

Length: {len(text)} characters
Platform Fit: {"Twitter/X" if len(text) <= 280 else "Instagram" if len(text) <= 500 else "Facebook/Blog"}

Evaluate:
1. STANDALONE: Can this be understood without context? (YES/NO)
2. IMPACT: How powerful is this as a standalone quote? (HIGH/MEDIUM/LOW)
3. INTRIGUE: Does it make you want to read more? (YES/NO)
4. SOCIAL_READY: Should we use this for promotion? (YES/NO)

Format response as:
STANDALONE: [YES/NO]
IMPACT: [HIGH/MEDIUM/LOW]
INTRIGUE: [YES/NO]
SOCIAL_READY: [YES/NO]
NOTES: [any observations]
"""

        return QueryResult(True, {'prompt': prompt, 'text': text, 'length': len(text)}, 'quote_assess_prompt')

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _load_yaml(self, path: Path) -> Optional[Dict]:
        """Load and cache YAML file."""
        path_str = str(path)
        if path_str not in self._cache:
            if not path.exists():
                return None
            with open(path, 'r', encoding='utf-8') as f:
                self._cache[path_str] = yaml.safe_load(f)
        return self._cache[path_str]

    def _extract_title(self, filename: str) -> str:
        """Extract chapter title from filename."""
        # Pattern: RESONANCE_CH8_WHATS_IN_A_NAME.txt -> WHAT'S IN A NAME
        match = re.search(r'CH\d+[a-z]?_(.+)\.txt', filename, re.IGNORECASE)
        if match:
            title = match.group(1).replace('_', ' ')
            return title
        return filename

    def clear_cache(self):
        """Clear the YAML cache."""
        self._cache = {}

    def list_chapters(self) -> QueryResult:
        """List all available chapters."""
        chapter_dir = self.paths['chapters']
        if not chapter_dir.exists():
            return QueryResult(False, f"Directory not found: {chapter_dir}", str(chapter_dir))

        chapters = []
        for f in sorted(chapter_dir.glob('*.txt')):
            chapters.append({
                'file': f.name,
                'title': self._extract_title(f.name),
            })

        return QueryResult(True, chapters, str(chapter_dir))


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Go Squad State Query Interface")
    parser.add_argument('--project', '-p', default='remanence',
                        choices=['remanence', 'resonance'], help='Project to query')

    subparsers = parser.add_subparsers(dest='command', help='Query command')

    # Character query
    char_parser = subparsers.add_parser('character', help='Query character data')
    char_parser.add_argument('name', help='Character name')

    # Chapter query
    ch_parser = subparsers.add_parser('chapter', help='Query chapter data')
    ch_parser.add_argument('number', type=int, help='Chapter number')

    # Quote query
    quote_parser = subparsers.add_parser('quotes', help='Query quote bank')
    quote_parser.add_argument('--character', '-c', help='Filter by character')
    quote_parser.add_argument('--theme', '-t', help='Filter by theme')
    quote_parser.add_argument('--max-length', '-m', type=int, help='Max length')
    quote_parser.add_argument('--unused', '-u', action='store_true', help='Only unused')
    quote_parser.add_argument('--twitter', action='store_true', help='Twitter-ready (<=280)')

    # Search
    search_parser = subparsers.add_parser('search', help='Search text in manuscript')
    search_parser.add_argument('pattern', help='Search pattern (regex)')
    search_parser.add_argument('--chapter', type=int, help='Limit to chapter')

    # Word count
    wc_parser = subparsers.add_parser('wordcount', help='Get word counts')
    wc_parser.add_argument('--chapter', type=int, help='Specific chapter')

    # List chapters
    subparsers.add_parser('chapters', help='List all chapters')

    args = parser.parse_args()

    sq = StateQuery(project=args.project)

    if args.command == 'character':
        result = sq.character(args.name)
    elif args.command == 'chapter':
        result = sq.chapter(args.number)
        if result.success:
            # Don't print full content
            result.data['content'] = f"[{result.data['word_count']} words]"
    elif args.command == 'quotes':
        max_len = 280 if args.twitter else args.max_length
        result = sq.quotes(
            character=args.character,
            theme=args.theme,
            max_length=max_len,
            unused_only=args.unused,
        )
    elif args.command == 'search':
        result = sq.search_text(args.pattern, chapter=args.chapter)
    elif args.command == 'wordcount':
        result = sq.word_count(chapter=args.chapter)
    elif args.command == 'chapters':
        result = sq.list_chapters()
    else:
        parser.print_help()
        return

    # Print result
    print(f"\nSource: {result.source}")
    print(f"Success: {result.success}")
    print(f"Data:\n{yaml.dump(result.data, default_flow_style=False, allow_unicode=True)}")


if __name__ == '__main__':
    main()
