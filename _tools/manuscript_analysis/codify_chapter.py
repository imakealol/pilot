#!/usr/bin/env python3
"""
Codify a single chapter into structured YAML format.
Extracts metadata, character states, plot beats, and continuity markers.
"""

import anthropic
import yaml
import sys
import os
import re
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
RESONANCE_DIR = SCRIPT_DIR.parent.parent / "RESONANCE"
CHAPTERS_DIR = RESONANCE_DIR / "chapters"
SCHEMA_PATH = SCRIPT_DIR / "schema" / "chapter_codex.yaml"
MANIFEST_PATH = RESONANCE_DIR / "data" / "CHAPTER_MANIFEST.yaml"
OUTPUT_DIR = RESONANCE_DIR / "data" / "codex"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_schema() -> str:
    """Load the codex schema."""
    with open(SCHEMA_PATH) as f:
        return f.read()


def load_manifest() -> dict:
    """Load the chapter manifest."""
    with open(MANIFEST_PATH) as f:
        return yaml.safe_load(f)


def find_chapter_file(chapter_num: int | float) -> tuple[Path, str] | None:
    """Find the chapter file using the manifest."""
    manifest = load_manifest()

    # Handle interstitial chapters (e.g., 24.5 for CH24a)
    key = chapter_num if isinstance(chapter_num, float) else int(chapter_num)

    if key not in manifest['chapters']:
        return None

    chapter_info = manifest['chapters'][key]
    file_path = CHAPTERS_DIR / chapter_info['file']
    title = chapter_info['title']

    if not file_path.exists():
        return None

    return file_path, title


def load_chapter(chapter_path: Path) -> str:
    """Load chapter content."""
    with open(chapter_path) as f:
        return f.read()


def get_extraction_prompt(schema: str, chapter_num: int, title: str, content: str) -> str:
    """Build the extraction prompt."""
    return f"""You are a precise manuscript analyst. Your task is to extract structured data from a novel chapter.

## SCHEMA
Follow this schema exactly. Output valid YAML only.

```yaml
{schema}
```

## TASK
Extract structured data from Chapter {chapter_num}: "{title}" following the schema above.

## RULES
1. Output ONLY valid YAML - no markdown code fences, no explanatory text
2. Use null for unknown/unspecified values
3. Be precise - extract what's explicitly stated, don't infer beyond the text
4. Character states should reflect END of chapter status
5. For inventory, only track plot-significant objects (weapons, documents, keys, etc.)
6. Key events should be 3-7 major beats, ordered chronologically
7. Setups/payoffs: only flag clear foreshadowing, not every detail
8. If a field doesn't apply, use empty list [] or null as appropriate

## CHAPTER TEXT

{content}

## OUTPUT
Return the completed YAML codex for this chapter:"""


def codify_chapter(chapter_num: int, api_key: str) -> dict:
    """Extract structured data from a chapter."""
    # Load schema
    schema = load_schema()

    # Find and load chapter
    result = find_chapter_file(chapter_num)
    if not result:
        raise FileNotFoundError(f"No chapter file found for CH{chapter_num}")

    chapter_path, title = result
    content = load_chapter(chapter_path)

    # Build prompt
    prompt = get_extraction_prompt(schema, chapter_num, title, content)

    # Call API
    client = anthropic.Anthropic(api_key=api_key)

    print(f"  Extracting CH{chapter_num}: {title}...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.content[0].text

    # Parse YAML
    # Strip any markdown code fences if present
    yaml_content = raw_output.strip()
    if yaml_content.startswith("```"):
        yaml_content = re.sub(r'^```\w*\n?', '', yaml_content)
        yaml_content = re.sub(r'\n?```$', '', yaml_content)

    try:
        codex = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print(f"  WARNING: YAML parse error, saving raw output")
        codex = {"_parse_error": str(e), "_raw": raw_output}

    return codex, raw_output


def save_codex(chapter_num: int, codex: dict, raw: str):
    """Save the codex to files."""
    # Save structured YAML
    yaml_path = OUTPUT_DIR / f"ch{chapter_num:02d}_codex.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(codex, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Save raw output for debugging
    raw_path = OUTPUT_DIR / f"ch{chapter_num:02d}_raw.txt"
    with open(raw_path, 'w') as f:
        f.write(raw)

    print(f"  Saved: {yaml_path.name}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python codify_chapter.py <chapter_num> <api_key>")
        print("       python codify_chapter.py <start>-<end> <api_key>")
        print("Example: python codify_chapter.py 38 sk-ant-...")
        print("         python codify_chapter.py 1-44 sk-ant-...")
        sys.exit(1)

    chapter_arg = sys.argv[1]
    api_key = sys.argv[2]

    # Parse chapter range
    if '-' in chapter_arg:
        start, end = map(int, chapter_arg.split('-'))
        chapters = list(range(start, end + 1))
    else:
        chapters = [int(chapter_arg)]

    print(f"\n{'='*60}")
    print(f"CODIFYING {len(chapters)} CHAPTER(S)")
    print(f"{'='*60}\n")

    success = 0
    failed = []

    for chapter_num in chapters:
        try:
            codex, raw = codify_chapter(chapter_num, api_key)
            save_codex(chapter_num, codex, raw)
            success += 1
        except FileNotFoundError as e:
            print(f"  SKIP: {e}")
            failed.append((chapter_num, str(e)))
        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append((chapter_num, str(e)))

    print(f"\n{'='*60}")
    print(f"COMPLETE: {success} succeeded, {len(failed)} failed")
    if failed:
        print(f"Failed: {[f[0] for f in failed]}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
