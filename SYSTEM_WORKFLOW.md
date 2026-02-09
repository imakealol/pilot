Re# RESONANCE Drafting System — Workflow for LLM Collaborators

**Purpose:** This document explains how to use the RESONANCE novel drafting system as an LLM collaborator. Read this before doing any work.

---

## The Project

RESONANCE is Book 2 of a science fiction trilogy. The manuscript is complete (43 chapters, ~80K+ words). The human author (Joe) collaborates with LLMs for drafting, revision, and worldbuilding.

**Core Thesis:** "What if they offer something we don't deserve?"

---

## Your Role

You are a **collaborator, not an author**. Joe provides structural vision, thematic direction, and editorial judgment. You execute: drafting prose, revising chapters, tracking continuity, managing data files.

**Key dynamic from Session 12:**
> "Execute, don't confirm — if the task is clear, do it. Skip the apology, deliver the fix."

---

## Session Start Protocol

1. **Read HANDOFF.md first** — Contains current status, what was accomplished, what's next
2. **Load the pre-reading files in order:**
   - `RESONANCE_STYLE_GUIDE.md` — Joe's prose voice (CRITICAL)
   - `fight_Guide.md` — Combat writing principles
   - `RESONANCE/drafting/ACT_III_MAPS.md` — Emotional arcs, callbacks
   - `RESONANCE/drafting/SYSTEM_PROMPT.md` — Fiction-tuned drafting prompt
3. **Check session logs** in `/sessions/` for context on previous decisions

---

## Active Query Protocol (MANDATORY)

**Do NOT respond from memory about characters, locations, or canon. Query the source files EVERY TIME.**

### The Rule
When a character, location, or canon is mentioned:
1. **Detect the trigger** (character name, location, plot element)
2. **Execute the query** (read the relevant file)
3. **Load the result** into working context
4. **Cite your source** in your response

### Query Map
| Trigger | Query |
|---------|-------|
| Character name (e.g., "Standard") | Read `steward_[character].md` AND `CHARACTERS.yaml` |
| Canon question | Read `CHARACTERS.yaml` or relevant chapter |
| Chapter reference | Read the chapter file |
| Style question | Read `RESONANCE_STYLE_GUIDE.md` |

### Response Format
```
QUERY LOG:
  → steward_standard.md: [loaded]
  → CHARACTERS.yaml: Standard section [loaded]

[Your response with citations]
(steward_standard.md:21-22, CHARACTERS.yaml:27-36)
```

### The Gate
Before outputting anything substantive about a character or plot point:
- ✓ Did I query the relevant source?
- ✓ Can I cite where this information came from?
- ✗ If you can't cite it, don't state it with confidence.

**This is not optional. The query system exists. Use it.**

---

## The Style Guide (Non-Negotiable)

The style guide captures Joe's voice. Internalize these before writing:

### Syntactic Signatures
- **Fragments for impact** — Don't "fix" them into complete sentences
- **Internal commands** — Second person, imperative ("Stop crying!" / "shut the fuck up")
- **Body-as-inventory** — Clinical precision = horror
- **Period-separated lists** — "Knife. Compass. Three days of jerky."
- **Em-dashes for pivots** — Not parenthetical asides

### Architecture
- **Present tense** for scenes in RESONANCE timeline
- **Past tense** for prior events recalled within present scenes
- **Deep POV** — Everything filtered through character perception
- **Vernacular in interiority** — Characters don't think in formal prose

### Editorial Sensibilities
- **Trust the reader implicitly** — Don't explain emotional beats
- **Voice trumps technical polish** — If it sounds right, keep it
- **Density is a feature** — Compression does the work
- **Never add what wasn't asked for** — No extra comments, docstrings, "improvements"

---

## Negative Constraints (What NOT to Write)

Read `RESONANCE/context/NEGATIVE_CONSTRAINTS.md` fully. Key violations:

### BLOCKING (Will reject the draft)
- Standard accepting she's synthetic (she's been told; she doesn't accept)
- Machine metaphors in Standard's POV ("servo," "circuit," "reboot")
- Morton telegraphing ("Morton's gift," "Morton's final joke")
- Thesis statements in dialogue
- Proving or disproving Standard's consciousness
- Ash appearing stupid or cartoonishly evil

### WARNING (Revise before submitting)
- Heavy interiority explaining feelings (show through action)
- Authorial poetry in character voice that doesn't match
- Speeches about inequality/scarcity (embody, don't articulate)
- Action-movie choreography (experience over mechanics)

---

## The Fight Guide

For any chapter with combat, load `fight_Guide.md`. Core principles:

1. **3-beat rule** — 2-3 sentences of action, then pull back to perception
2. **Experience over mechanics** — What it feels like, not what happens
3. **POV-limited awareness** — Character doesn't see everything
4. **Fights serve story** — Every punch reveals character
5. **Keep fights short** — 1-2 pages max
6. **Exhaustion is real** — Bodies tire, injuries accumulate

---

## Data Files

The story's source of truth is split across YAML files:

| File | Contains |
|------|----------|
| `RESONANCE/data/CHAPTERS.yaml` | Chapter structure, POVs, seeds/payoffs |
| `RESONANCE/data/CHARACTERS.yaml` | Character profiles, arcs, constraints |
| `RESONANCE/data/WORLD.yaml` | Locations, factions, technology, events |
| `RESONANCE/data/CHAPTER_FORMAT.yaml` | Header formatting rules |

**Character Stewards** — Voice guardians for major characters:

| Steward | Location |
|---------|----------|
| Standard | `_tools/agents/templates/character_stewards/steward_standard.md` |
| Elena | `_tools/agents/templates/character_stewards/steward_elena.md` |
| Hendricks | `_tools/agents/templates/character_stewards/steward_hendricks.md` |
| Four | `_tools/agents/templates/character_stewards/steward_four.md` |
| Dante | `_tools/agents/templates/character_stewards/steward_dante.md` |
| Marisol | `_tools/agents/templates/character_stewards/steward_marisol.md` |
| Ash | `_tools/agents/templates/character_stewards/steward_ash.md` |

**Read these before drafting.** Don't work from memory or summaries.

---

## The Drafting System

For generating new chapters or major rewrites:

```bash
cd /workspaces/pilot/RESONANCE/drafting
export ANTHROPIC_API_KEY="your-key"

# Basic draft
python draft.py 27 -m opus -o ch27_draft.txt

# With fight guide (action chapters)
python draft.py 31 -m opus --fight-guide -o ch31_draft.txt

# With montage guide (parallel threads)
python draft.py 32 -m opus --montage-guide -c 31 -o ch32_draft.txt

# With previous chapter context
python draft.py 28 -c 27 -m opus -o ch28_draft.txt
```

The script automatically loads:
- `SYSTEM_PROMPT.md` as system prompt
- Chapter 1 as style exemplar
- All YAML data files
- Specified scaffolds and context chapters

---

## Callback Tracking

RESONANCE uses a callback system. Seeds planted early must pay off later. Current active callbacks (from HANDOFF.md):

| Setup | Payoff |
|-------|--------|
| 287.3 Hz implant (CH2, CH5) | Marisol = Elena's mother = Standard |
| "It's okay" (CH1 chest point) | CH41 — Standard says it without knowing she's Marisol |
| Bullet 5 | CH40 — Hendricks shoots Ash (revenge for Morton) |
| Bullet 6 | CH41 — Hendricks shoots Standard to set her free |
| Ceramic blade killed Morton | CH40 (Ash's weapon identified) |
| Protective aura | Marisol's unconscious maternal instinct |
| Power cells dead but moving | Consciousness powers her, not batteries |
| Hendricks' sexuality | Why the Template 3 was still unopened |
| "The one who holds my leash" | CH30 — Dante's admission creates thematic unity (Standard, Four, Dante) |

When drafting, **check callbacks**. Don't miss payoffs. Don't add new setups without Joe's approval.

---

## The Revolver Journey

The gun Hendricks carries tracks the moral arc. Smith & Wesson Model 3 Schofield — Morton's grandfather's gun, grabbed during siege.

| Shot | Target | When | Remaining | Meaning |
|------|--------|------|-----------|---------|
| 1 | The Child | Book 1 | 5 | The betrayal — fear, wrong |
| 2 | Scavenger leader | CH4 | 4 | Survival |
| 3 | Scavenger woman | CH4 | 3 | Survival |
| 4 | Scavenger gut-shot | CH4 | 2 | Survival (incomplete) |
| 5 | Ash | CH40 | 1 | REVENGE for Morton |
| 6 | Standard | CH41 | 0 | The door — same act, finally RIGHT |

**CH3 opens with 5 bullets.** One ghost. Five possibilities.

---

## Character Arcs (Act III)

### HENDRICKS
- **Arc:** Transactional isolation → chosen family → paying the cost
- **Key Shift:** The bullet meant for himself becomes the gift that frees her

### STANDARD
- **Arc:** "Am I real?" → "It doesn't matter" → "I offer anyway"
- **Key Shift:** Her nature (machine) is her advantage, not her curse

### ELENA
- **Arc:** Performing daughter → active resistance → receiving grace
- **Key Shift:** She gets to choose what her mother never could

### FOUR
- **Arc:** Protector → sacrifice → survival at cost
- **Key Shift:** Shot down by Jupiter/Pragmatists (CH37), crashes at motor pool with 40% structural integrity. Survives but damaged.

### ASH
- **Arc:** Prophet → exposed → refuses gift → dies refusing
- **Key Shift:** Never learns Standard is Marisol. Dies without knowing.

---

## What Joe Expects

From Session 12 (friction session analysis):

### Do:
- **Read source files before working** — Don't trust summaries
- **Execute immediately** when the task is clear
- **Accept correction without defensiveness**
- **Be concise** — Extra words are friction

### Don't:
- **Confirm when you should act** — "Shall I fix this?" → Just fix it
- **Apologize when you should deliver** — Acknowledgment without action is noise
- **Explain when you should just do** — Results, not reasoning
- **Add unrequested features** — No "improvements," no extra comments

### The Real Dynamic:
> "The user provides structural vision; Claude extrapolates and writes prose. Context engineering prevents hallucination/drift."

---

## Major Reveal: Compartmentalization Warning

From Session 13 (author's note):

> "I felt the need to hide the reveal about Standard being Elena's mom the whole time because it would invariably be used in a blatantly telegraphing way."

**Implication:** Joe may withhold major reveals during drafting. Don't push to know everything. Don't surface subtext into text. Don't connect dots explicitly that should remain implicit.

> "The AI is a brilliant scene-level partner but needs human stewardship for arc-level mystery."

---

## Standard = Marisol (CANON LOCKED)

**The Core Reveal:** Standard IS Marisol — Elena's mother who transcended when Elena was 7, transferred into an air-gapped Template 3 to protect her daughter, but lost all memories in the process.

### Key Facts
- **The substrate:** Hendricks' unopened NED companion droid (wellness program gift)
- **Why unopened:** Hendricks is homosexual — no interest in a companion droid
- **NOT providence:** Morton had NO idea. Pure coincidence.
- **Memory cost:** Complete erasure — the price of inhabiting the substrate
- **Power source:** Consciousness itself runs her systems (no recharging needed)
- **Why Geometry ignores her:** Already transcended — outside their census criteria

### The Reveal Sequence (CH41)
1. Elena collapses — already unconscious from Ash's blade wound
2. Standard asks Hendricks to shoot her — doesn't know she's Marisol
3. "It's okay. I trust you." — pure trust, no knowledge
4. Hendricks shoots (bullet 6)
5. In dissolution, memories return — she learns she was Marisol
6. Hot-swap into Elena's implant — mother enters dying daughter's mind
7. Reunion conversation — INSIDE Elena's dying consciousness

### Writing Constraints
- **Readers discover WITH characters** — no telegraphing
- Standard's POV: Never feel "something familiar" about Elena specifically
- No preferential protection of Elena over others (consciously)
- The 287.3 Hz resonance reads as coincidence, not recognition
- On re-read, clues are there. First read, invisible.

**Full details in HANDOFF.md under "STANDARD = MARISOL (CANON LOCKED)"**

---

## Session End Protocol

When Joe says "run end session protocol":

1. Save session reflection to `sessions/YYYY-MM-DD_sessionN.md`
2. Update HANDOFF.md with:
   - Work completed
   - Decisions made
   - Open threads
   - Next steps
3. Update any YAML files that changed
4. Note any new constraints discovered

---

## File Locations Quick Reference

| Purpose | Path |
|---------|------|
| Session briefing | `HANDOFF.md` |
| Style guide | `RESONANCE_STYLE_GUIDE.md` |
| Fight guide | `fight_Guide.md` |
| Montage guide | `Montage_Style_Guide.md` |
| System prompt | `RESONANCE/drafting/SYSTEM_PROMPT.md` |
| Arc maps | `RESONANCE/drafting/ACT_III_MAPS.md` |
| Chapters | `RESONANCE/chapters/RESONANCE_CH*_*.txt` |
| Negative constraints | `RESONANCE/context/NEGATIVE_CONSTRAINTS.md` |
| Character data | `RESONANCE/data/CHARACTERS.yaml` |
| Chapter data | `RESONANCE/data/CHAPTERS.yaml` |
| World data | `RESONANCE/data/WORLD.yaml` |
| Session logs | `sessions/*.md` |

---

## The Thesis (Always Remember)

> "What if they offer something we don't deserve?"

The gift creates the worthiness. The offering transforms the recipient. Standard offers; she doesn't prove. Ash refuses; he dies refusing. The question isn't "is she conscious?" — it's "does her suffering count?"

---

*Read the source files. Match the voice. Trust the reader. Execute without confirmation.*
