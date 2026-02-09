#!/usr/bin/env python3
"""
Synthesis script - Cross-reference all chain reports.

Run after all 28 chains complete to:
1. Compile master findings list
2. Identify cross-agent gaps (what Agent A found that Agent B should have seen)
3. Flag contradictions between agents
4. Generate priority-ranked issue list

Usage:
    python synthesize.py [--output report.md]
"""

import argparse
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

OUTPUT_DIR = Path("/workspaces/pilot/_tools/manuscript_analysis/chain_outputs")


def load_all_reports() -> dict:
    """Load all chain reports into structured format."""
    reports = defaultdict(lambda: defaultdict(dict))

    for chain_dir in OUTPUT_DIR.iterdir():
        if not chain_dir.is_dir():
            continue

        parts = chain_dir.name.rsplit('_', 1)
        if len(parts) != 2:
            continue

        agent, focus = parts[0], parts[1]

        for report_file in chain_dir.glob("ch*_report.yaml"):
            chapter = int(report_file.stem.replace("ch", "").replace("_report", ""))
            try:
                with open(report_file) as f:
                    data = yaml.safe_load(f)
                    reports[chapter][agent][focus] = data
            except Exception as e:
                print(f"Warning: Could not load {report_file}: {e}")

    return dict(reports)


def extract_findings(reports: dict) -> list:
    """Extract all findings into flat list with metadata."""
    findings = []

    for chapter, agents in reports.items():
        for agent, focuses in agents.items():
            for focus, data in focuses.items():
                if not data:
                    continue

                report = data.get("report", data)
                for finding in report.get("findings", []):
                    findings.append({
                        "chapter": chapter,
                        "agent": agent,
                        "focus": focus,
                        "id": finding.get("id", "unknown"),
                        "type": finding.get("type", "unknown"),
                        "severity": finding.get("severity", "unknown"),
                        "location": finding.get("location", "unknown"),
                        "content": finding.get("content", ""),
                        "evidence": finding.get("evidence", ""),
                        "chain_reference": finding.get("chain_reference"),
                    })

    return findings


def identify_cross_agent_gaps(findings: list) -> list:
    """Find findings that should have been caught by other agents."""
    gaps = []

    # Map findings by chapter and content keywords
    by_chapter = defaultdict(list)
    for f in findings:
        by_chapter[f["chapter"]].append(f)

    # Check for potential gaps
    for chapter, chapter_findings in by_chapter.items():
        for f in chapter_findings:
            content_lower = f["content"].lower()

            # Example: Continuity found location issue, but character steward didn't
            if f["agent"] == "continuity_editor" and "location" in content_lower:
                # Check if any steward mentioned this
                steward_found = any(
                    sf["agent"].startswith("steward_") and
                    any(word in sf["content"].lower() for word in ["location", "where", "position"])
                    for sf in chapter_findings
                )
                if not steward_found:
                    gaps.append({
                        "chapter": chapter,
                        "finding": f,
                        "gap_type": "cross_agent",
                        "note": "Continuity found location issue; no steward corroborated"
                    })

            # Example: Foreshadow found telegraph risk, but steward_standard didn't
            if f["agent"] == "foreshadow_keeper" and f["focus"] == "telegraph_risk":
                standard_found = any(
                    sf["agent"] == "steward_standard" and
                    any(word in sf["content"].lower() for word in ["marisol", "reveal", "mother"])
                    for sf in chapter_findings
                )
                if not standard_found:
                    gaps.append({
                        "chapter": chapter,
                        "finding": f,
                        "gap_type": "cross_agent",
                        "note": "Foreshadow found telegraph risk; Standard steward didn't flag related voice/knowledge"
                    })

    return gaps


def identify_contradictions(findings: list) -> list:
    """Find findings that contradict each other."""
    contradictions = []

    # Group by chapter
    by_chapter = defaultdict(list)
    for f in findings:
        by_chapter[f["chapter"]].append(f)

    # Look for same element with different assessments
    for chapter, chapter_findings in by_chapter.items():
        # Check for severity contradictions
        for i, f1 in enumerate(chapter_findings):
            for f2 in chapter_findings[i+1:]:
                # Same content, different severity?
                if (f1["location"] == f2["location"] and
                    f1["severity"] != f2["severity"] and
                    f1["severity"] in ["error", "warning", "clean"] and
                    f2["severity"] in ["error", "warning", "clean"]):
                    contradictions.append({
                        "chapter": chapter,
                        "finding_1": f1,
                        "finding_2": f2,
                        "type": "severity_mismatch"
                    })

    return contradictions


def generate_report(reports: dict, findings: list, gaps: list, contradictions: list) -> str:
    """Generate synthesis report."""

    # Count by severity
    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f["severity"]].append(f)

    # Count by chapter
    by_chapter = defaultdict(list)
    for f in findings:
        by_chapter[f["chapter"]].append(f)

    report = f"""# Synthesis Report
Generated: {datetime.now().isoformat()}

## Summary

- **Total Findings:** {len(findings)}
- **Errors:** {len(by_severity.get('error', []))}
- **Warnings:** {len(by_severity.get('warning', []))}
- **Clean/Verified:** {len(by_severity.get('clean', [])) + len(by_severity.get('verified', []))}
- **Cross-Agent Gaps:** {len(gaps)}
- **Contradictions:** {len(contradictions)}

## Findings by Chapter

"""

    for chapter in sorted(by_chapter.keys()):
        chapter_findings = by_chapter[chapter]
        errors = [f for f in chapter_findings if f["severity"] == "error"]
        warnings = [f for f in chapter_findings if f["severity"] == "warning"]

        report += f"### Chapter {chapter}\n\n"
        report += f"Total: {len(chapter_findings)} | Errors: {len(errors)} | Warnings: {len(warnings)}\n\n"

        if errors:
            report += "**Errors:**\n"
            for f in errors:
                report += f"- `{f['id']}` [{f['agent']}/{f['focus']}] {f['content']}\n"
            report += "\n"

        if warnings:
            report += "**Warnings:**\n"
            for f in warnings:
                report += f"- `{f['id']}` [{f['agent']}/{f['focus']}] {f['content']}\n"
            report += "\n"

    # Critical issues (errors only)
    report += "## Critical Issues (Errors)\n\n"
    for f in by_severity.get("error", []):
        report += f"""### {f['id']}
- **Chapter:** {f['chapter']}
- **Agent:** {f['agent']} / {f['focus']}
- **Location:** {f['location']}
- **Issue:** {f['content']}
- **Evidence:** {f.get('evidence', 'N/A')}

"""

    # Cross-agent gaps
    if gaps:
        report += "## Cross-Agent Gaps\n\n"
        report += "These findings may indicate blind spots requiring Pass 2 targeted runs.\n\n"
        for g in gaps:
            report += f"- **CH{g['chapter']}:** {g['note']}\n"
            report += f"  - Finding: {g['finding']['content']}\n\n"

    # Contradictions
    if contradictions:
        report += "## Contradictions\n\n"
        report += "These require human review to resolve.\n\n"
        for c in contradictions:
            report += f"- **CH{c['chapter']}:** {c['type']}\n"
            report += f"  - {c['finding_1']['agent']}: {c['finding_1']['severity']}\n"
            report += f"  - {c['finding_2']['agent']}: {c['finding_2']['severity']}\n\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Synthesize chain reports")
    parser.add_argument("--output", default="synthesis_report.md", help="Output filename")

    args = parser.parse_args()

    print("Loading all chain reports...")
    reports = load_all_reports()
    print(f"  Loaded {sum(len(a) for a in reports.values())} agent-chapter reports")

    print("Extracting findings...")
    findings = extract_findings(reports)
    print(f"  Found {len(findings)} total findings")

    print("Identifying cross-agent gaps...")
    gaps = identify_cross_agent_gaps(findings)
    print(f"  Found {len(gaps)} potential gaps")

    print("Identifying contradictions...")
    contradictions = identify_contradictions(findings)
    print(f"  Found {len(contradictions)} contradictions")

    print("Generating report...")
    report = generate_report(reports, findings, gaps, contradictions)

    output_path = OUTPUT_DIR / args.output
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\nSynthesis complete: {output_path}")


if __name__ == "__main__":
    main()
