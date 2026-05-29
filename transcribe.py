#!/usr/bin/env python3
"""
Transcribe an audio file using local Whisper.

Usage:
    python _tools/transcribe.py path/to/file.m4a
    python _tools/transcribe.py path/to/file.m4a --model small   # more accurate, slower
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Transcribe audio to text')
    parser.add_argument('audio', help='Path to audio file')
    parser.add_argument('--model', default='base', choices=['tiny', 'base', 'small', 'medium'],
                        help='Whisper model size (default: base)')
    parser.add_argument('--output', '-o', help='Output file (default: same name as audio + .txt)')
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: {audio_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else audio_path.with_suffix('.txt')

    print(f"Loading model '{args.model}'...")
    import whisper
    model = whisper.load_model(args.model)

    print(f"Transcribing {audio_path.name}...")
    result = model.transcribe(str(audio_path))

    text = result['text'].strip()
    output_path.write_text(text)

    print(f"Done. Transcript saved to: {output_path}")
    print(f"Word count: {len(text.split())}")

if __name__ == '__main__':
    main()
