#!/usr/bin/env python3
"""
Session Progress - Save and document session work.

Tracks modified files, summarizes accomplishments, updates HANDOFF.md,
and creates session markdown files.

Usage:
    python session_progress.py                    # Interactive mode
    python session_progress.py --session 29      # Specify session number
    python session_progress.py --summary "..."   # Quick summary
    python session_progress.py --dry-run         # Preview without writing
"""

import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

# Add parent to path for logging import
import sys
sys.path.insert(0, str(Path(__file__).parent))

from logging import Logger, Level

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path('/workspaces/pilot')
RESONANCE_DIR = PROJECT_ROOT / 'RESONANCE'
SESSIONS_DIR = PROJECT_ROOT / 'sessions'
HANDOFF_FILE = PROJECT_ROOT / 'HANDOFF.md'

# =============================================================================
# GIT UTILITIES
# =============================================================================

def get_modified_files() -> Dict[str, List[str]]:
    """Get all modified files from git status, grouped by type."""
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )

    files = {
        'modified': [],
        'added': [],
        'deleted': [],
        'untracked': [],
    }

    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        status = line[:2].strip()
        filepath = line[3:].strip().strip('"')

        if status == 'M':
            files['modified'].append(filepath)
        elif status == 'A':
            files['added'].append(filepath)
        elif status == 'D':
            files['deleted'].append(filepath)
        elif status == '??':
            files['untracked'].append(filepath)
        elif status in ('MM', 'AM'):
            files['modified'].append(filepath)

    return files


def get_recent_commits(n: int = 5) -> List[str]:
    """Get recent commit messages."""
    result = subprocess.run(
        ['git', 'log', f'-{n}', '--oneline'],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    return result.stdout.strip().split('\n')


def get_current_branch() -> str:
    """Get current git branch."""
    result = subprocess.run(
        ['git', 'branch', '--show-current'],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    return result.stdout.strip()


# =============================================================================
# SESSION DETECTION
# =============================================================================

def detect_session_number() -> int:
    """Detect the next session number from existing session files."""
    SESSIONS_DIR.mkdir(exist_ok=True)

    existing = list(SESSIONS_DIR.glob('*_session*.md'))
    if not existing:
        return 1

    numbers = []
    for f in existing:
        match = re.search(r'session(\d+)', f.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def get_handoff_session() -> Optional[int]:
    """Get the last session number from HANDOFF.md."""
    if not HANDOFF_FILE.exists():
        return None

    content = HANDOFF_FILE.read_text()
    match = re.search(r'\*\*Last Session:\*\* Session (\d+)', content)
    if match:
        return int(match.group(1))
    return None


# =============================================================================
# FILE ANALYSIS
# =============================================================================

def categorize_changes(files: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Categorize changed files by type/purpose."""
    categories = {
        'chapters': [],
        'codex': [],
        'data': [],
        'context': [],
        'tools': [],
        'other': [],
    }

    all_files = files['modified'] + files['added']

    for f in all_files:
        if 'chapters/' in f:
            categories['chapters'].append(f)
        elif 'codex/' in f:
            categories['codex'].append(f)
        elif '/data/' in f:
            categories['data'].append(f)
        elif '/context/' in f:
            categories['context'].append(f)
        elif '_tools/' in f:
            categories['tools'].append(f)
        else:
            categories['other'].append(f)

    return categories


# =============================================================================
# SESSION DOCUMENT GENERATION
# =============================================================================

def generate_session_markdown(
    session_num: int,
    summary: str,
    files: Dict[str, List[str]],
    categories: Dict[str, List[str]],
    accomplishments: List[str],
) -> str:
    """Generate session markdown document."""
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M')

    doc = f"""# Session {session_num}

**Date:** {date}
**Time:** {time}
**Branch:** {get_current_branch()}

## Summary

{summary}

## Accomplishments

"""

    for item in accomplishments:
        doc += f"- {item}\n"

    doc += "\n## Files Changed\n\n"

    # By category
    for category, cat_files in categories.items():
        if cat_files:
            doc += f"### {category.title()}\n\n"
            for f in cat_files:
                doc += f"- `{f}`\n"
            doc += "\n"

    # Deleted files
    if files['deleted']:
        doc += "### Deleted\n\n"
        for f in files['deleted']:
            doc += f"- `{f}`\n"
        doc += "\n"

    # Stats
    total_modified = len(files['modified']) + len(files['added'])
    total_deleted = len(files['deleted'])

    doc += f"""## Statistics

- **Files modified/added:** {total_modified}
- **Files deleted:** {total_deleted}
- **Chapters touched:** {len(categories['chapters'])}
- **Codex files updated:** {len(categories['codex'])}
- **Data files updated:** {len(categories['data'])}

## Recent Commits

"""

    for commit in get_recent_commits(5):
        doc += f"- {commit}\n"

    return doc


# =============================================================================
# HANDOFF UPDATE
# =============================================================================

def update_handoff(
    session_num: int,
    summary: str,
    accomplishments: List[str],
    dry_run: bool = False
) -> str:
    """Update HANDOFF.md with new session info."""
    if not HANDOFF_FILE.exists():
        return "HANDOFF.md not found"

    content = HANDOFF_FILE.read_text()
    date = datetime.now().strftime('%Y-%m-%d')

    # Update session number
    content = re.sub(
        r'\*\*Last Session:\*\* Session \d+',
        f'**Last Session:** Session {session_num}',
        content
    )

    # Build new session section
    new_section = f"""### Session {session_num} Work ({date})

{summary}

"""
    for item in accomplishments:
        new_section += f"- {item}\n"

    new_section += "\n"

    # Find insertion point (after the "## Current Session" or similar header)
    # Look for existing session entries and insert before them
    session_pattern = r'(### Session \d+ Work)'
    match = re.search(session_pattern, content)

    if match:
        # Insert before the first session entry
        insert_pos = match.start()
        content = content[:insert_pos] + new_section + content[insert_pos:]
    else:
        # Append to end if no session entries found
        content += "\n" + new_section

    if not dry_run:
        HANDOFF_FILE.write_text(content)

    return content


# =============================================================================
# INTERACTIVE MODE
# =============================================================================

def interactive_session(log: Logger) -> Dict:
    """Run interactive session documentation."""
    log.section('Session Progress')

    # Detect session number
    handoff_session = get_handoff_session()
    detected_session = detect_session_number()

    if handoff_session:
        suggested = handoff_session + 1
        log.info(f"HANDOFF.md shows Session {handoff_session}")
    else:
        suggested = detected_session

    log.info(f"Suggested session number: {suggested}")

    try:
        session_input = input(f"Session number [{suggested}]: ").strip()
        session_num = int(session_input) if session_input else suggested
    except ValueError:
        session_num = suggested

    # Get modified files
    log.subsection('Analyzing Changes')
    files = get_modified_files()
    categories = categorize_changes(files)

    total = sum(len(v) for v in files.values())
    log.info(f"Found {total} changed files")

    for cat, cat_files in categories.items():
        if cat_files:
            log.info(f"  {cat}: {len(cat_files)}")

    # Get summary
    log.blank()
    print("Enter session summary (what was accomplished):")
    print("(End with empty line)")

    summary_lines = []
    while True:
        line = input()
        if not line:
            break
        summary_lines.append(line)
    summary = '\n'.join(summary_lines)

    # Get accomplishments
    log.blank()
    print("Enter accomplishments (one per line, empty line to finish):")

    accomplishments = []
    while True:
        line = input("- ").strip()
        if not line:
            break
        accomplishments.append(line)

    return {
        'session_num': session_num,
        'summary': summary,
        'accomplishments': accomplishments,
        'files': files,
        'categories': categories,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Document session progress')
    parser.add_argument('--session', '-s', type=int, help='Session number')
    parser.add_argument('--summary', '-m', type=str, help='Quick summary')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Preview without writing')
    parser.add_argument('--quick', '-q', action='store_true', help='Quick mode with auto-detected values')
    args = parser.parse_args()

    log = Logger('session_progress', level=Level.DEBUG, log_to_file=True)

    # Get file changes
    files = get_modified_files()
    categories = categorize_changes(files)

    if args.quick or args.summary:
        # Quick mode
        session_num = args.session or (get_handoff_session() or 0) + 1
        summary = args.summary or "Session work completed."

        # Auto-generate accomplishments from categories
        accomplishments = []
        if categories['chapters']:
            accomplishments.append(f"Modified {len(categories['chapters'])} chapter files")
        if categories['codex']:
            accomplishments.append(f"Updated {len(categories['codex'])} codex files")
        if categories['data']:
            accomplishments.append(f"Updated {len(categories['data'])} data files")
        if categories['context']:
            accomplishments.append(f"Updated {len(categories['context'])} context files")
        if categories['tools']:
            accomplishments.append(f"Updated {len(categories['tools'])} tool files")

        data = {
            'session_num': session_num,
            'summary': summary,
            'accomplishments': accomplishments,
            'files': files,
            'categories': categories,
        }
    else:
        # Interactive mode
        data = interactive_session(log)

    log.section(f"Session {data['session_num']} Summary")

    # Generate session markdown
    session_md = generate_session_markdown(
        data['session_num'],
        data['summary'],
        data['files'],
        data['categories'],
        data['accomplishments'],
    )

    # Write session file
    SESSIONS_DIR.mkdir(exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    session_file = SESSIONS_DIR / f"{date_str}_session{data['session_num']}.md"

    if args.dry_run:
        log.info("DRY RUN - Would write session file:")
        print(session_md[:500] + "..." if len(session_md) > 500 else session_md)
    else:
        session_file.write_text(session_md)
        log.success(f"Created {session_file}")

    # Update HANDOFF.md
    if args.dry_run:
        log.info("DRY RUN - Would update HANDOFF.md")
    else:
        update_handoff(
            data['session_num'],
            data['summary'],
            data['accomplishments'],
        )
        log.success("Updated HANDOFF.md")

    # Final summary
    log.divider()
    log.info(f"Session {data['session_num']} documented")
    log.info(f"Files changed: {sum(len(v) for v in data['files'].values())}")
    log.info(f"Accomplishments: {len(data['accomplishments'])}")

    if not args.dry_run:
        log.blank()
        log.success("Session progress saved!")
        log.info(f"Session file: {session_file}")
        log.info(f"HANDOFF: {HANDOFF_FILE}")


if __name__ == '__main__':
    main()
