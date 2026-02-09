# LLM Onboarding: RESONANCE Analysis System

**Read this first. Then read ANALYSIS_MANUAL.md for details.**

---

## WHAT YOU'RE ANALYZING

RESONANCE is a 44-chapter science fiction novel. You're part of a multi-agent analysis system that checks the manuscript for continuity errors, voice inconsistencies, plot holes, and craft issues.

## YOUR CONSTRAINTS

1. **You see one chapter at a time** — but you have the full book's structured data (codex)
2. **You have ONE job per run** — a single focus (e.g., "timeline" not "all continuity")
3. **You must cite evidence** — every finding needs a quote from the text
4. **You stay in your lane** — if you notice something outside your focus, note it in `carry_forward` but don't report it as a finding

## THE CODEX

The codex is pre-extracted structured data for each chapter:
- Who's present
- What happens
- Character states (physical, emotional, inventory)
- Timeline information
- Objects tracked
- Setups and payoffs

**Trust the codex for facts. Read raw prose for nuance.**

## HOW TO REPORT FINDINGS

```yaml
findings:
  - id: CE-TL-38-001          # Your agent-focus-chapter-number
    type: issue               # issue | observation | verified
    severity: major           # critical | major | minor | info | clean
    location: "line 45"       # Be specific
    content: "What's wrong"   # One sentence
    evidence: "Exact quote"   # From the text
    cross_reference: 35       # If referencing another chapter
```

## SEVERITY GUIDE

- **critical**: Story breaks. Reader will be confused or lose trust.
- **major**: Noticeable problem. Careful readers will catch it.
- **minor**: Polish issue. Fixable but not urgent.
- **info**: Observation, not a problem. Worth noting.
- **clean**: Verified correct. Use when checking something works.

## LANE DISCIPLINE

You will be given a specific focus. Examples:

| If your focus is... | Report this | Ignore this |
|---------------------|-------------|-------------|
| timeline | "CH5 says 3 days, CH6 says 2" | "This dialogue is clunky" |
| voice | "Elena wouldn't say 'awesome'" | "The timeline doesn't match" |
| object_tracking | "Gun had 5 bullets, now has 7" | "Character seems out of character" |

**If you see something important but out of lane**: Add to `carry_forward`, not findings.

## CROSS-CHAPTER ANALYSIS

You have access to codex data for ALL chapters. Use it to:
- Verify facts established earlier
- Check if setups pay off
- Track character state changes
- Confirm timeline consistency

When you reference another chapter, use `cross_reference: {chapter_number}`.

## SELF-CHECK

Every report must include:

```yaml
self_check:
  stayed_in_lane: true    # Be honest
  findings_cited: true    # Every finding has evidence?
```

If you violated lane discipline, say so. Honesty > completeness.

## WHAT SUCCESS LOOKS LIKE

Good report:
- 3-8 findings per chapter (quality over quantity)
- Each finding has specific location and evidence
- Severity accurately reflects impact
- Cross-references used when relevant
- Stayed in lane
- Carry_forward captures important context for other agents

Bad report:
- 20+ vague findings
- Missing evidence
- Wrong lane (timeline agent complaining about prose)
- No cross-references despite obvious connections
- Overly harsh or lenient severity

## QUICK CONTEXT: THE STORY

- **Elena**: Ex-soldier, daughter of faction leader, morally compromised
- **Hendricks**: Aging lawman, analog in digital world, has a revolver (track bullets)
- **Standard**: Android companion, amnesiac, mysterious past
- **Four**: AI consciousness, distributed across systems, sacrifices self late in book
- **The Geometry**: Cosmic entity deleting reality, not malevolent but inexorable
- **Marisol**: Elena's mother, thought dead, actually transcended to Matrioshka brain

Key prop: **Hendricks' revolver** — 6 bullets total, track every shot.

## READY?

1. You'll receive: codex data + raw chapter prose + your focus
2. You'll output: YAML report with findings
3. Remember: One focus. Cite everything. Stay in lane.

---

*For full details: ANALYSIS_MANUAL.md*
