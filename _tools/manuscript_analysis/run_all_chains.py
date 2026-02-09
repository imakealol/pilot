#!/usr/bin/env python3
"""
Batch runner for all 28 agent-focus chains.

Usage:
    python run_all_chains.py <api_key> [--resume]

Runs all chains sequentially with progress tracking.
Use --resume to continue from where you left off.
"""

import argparse
import json
import time
from pathlib import Path
from datetime import datetime

from chain_runner import AGENT_FOCUSES, CHAPTERS, OUTPUT_DIR, run_chain

PROGRESS_FILE = OUTPUT_DIR / "batch_progress.json"
DELAY_BETWEEN_CHAINS = 120  # 2 minutes between chains


def load_progress() -> dict:
    """Load progress from file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": [], "current": None, "started": None}


def save_progress(progress: dict):
    """Save progress to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def get_all_chains() -> list:
    """Get list of all agent-focus combinations."""
    chains = []
    for agent, focuses in AGENT_FOCUSES.items():
        for focus in focuses:
            chains.append((agent, focus))
    return chains


def run_all(api_key: str, resume: bool = False):
    """Run all chains."""

    all_chains = get_all_chains()
    progress = load_progress() if resume else {"completed": [], "current": None, "started": datetime.now().isoformat()}

    print(f"\n{'='*60}")
    print("BATCH RUN: All Agent-Focus Chains")
    print(f"{'='*60}")
    print(f"Total chains: {len(all_chains)}")
    print(f"Chapters per chain: {len(CHAPTERS)}")
    print(f"Total runs: {len(all_chains) * len(CHAPTERS)}")
    print(f"Completed: {len(progress['completed'])}")
    print(f"Remaining: {len(all_chains) - len(progress['completed'])}")
    print(f"{'='*60}\n")

    for i, (agent, focus) in enumerate(all_chains):
        chain_id = f"{agent}_{focus}"

        if chain_id in progress["completed"]:
            print(f"[{i+1}/{len(all_chains)}] {chain_id}: Already complete, skipping")
            continue

        print(f"\n[{i+1}/{len(all_chains)}] Starting: {chain_id}")
        progress["current"] = chain_id
        save_progress(progress)

        try:
            run_chain(api_key, agent, focus)
            progress["completed"].append(chain_id)
            progress["current"] = None
            save_progress(progress)
            print(f"[{i+1}/{len(all_chains)}] Completed: {chain_id}")

        except KeyboardInterrupt:
            print(f"\n\nInterrupted! Progress saved. Resume with --resume flag.")
            save_progress(progress)
            return

        except Exception as e:
            print(f"[{i+1}/{len(all_chains)}] Error in {chain_id}: {e}")
            # Continue to next chain

        # Delay between chains
        if i < len(all_chains) - 1:
            remaining = len(all_chains) - i - 1
            print(f"\nWaiting {DELAY_BETWEEN_CHAINS}s before next chain... ({remaining} remaining)")
            time.sleep(DELAY_BETWEEN_CHAINS)

    progress["finished"] = datetime.now().isoformat()
    save_progress(progress)

    print(f"\n{'='*60}")
    print("BATCH COMPLETE")
    print(f"{'='*60}")
    print(f"Completed: {len(progress['completed'])}/{len(all_chains)} chains")
    print(f"Output directory: {OUTPUT_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Run all agent-focus chains")
    parser.add_argument("api_key", help="Anthropic API key")
    parser.add_argument("--resume", action="store_true", help="Resume from previous run")

    args = parser.parse_args()
    run_all(args.api_key, args.resume)


if __name__ == "__main__":
    main()
