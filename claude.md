# Claude Project Tracker

**Project:** Remanence Trilogy
**Book 1:** Remanence (complete, reference material)
**Book 2:** Resonance (in progress)
**Book 3:** TBD

---

## Current Status

| Item | Status |
|------|--------|
| Book 1 Draft | Complete (~120K words) |
| Book 1 Context Engineering | Complete |
| Book 2 Chapters | 22 complete + interstitial (~40,000 words) |
| Book 2 Context Engineering | Active (split YAML system) |

---

## TODO: Dabble Export Workflow

**Problem:** Markdown `*italics*` in .txt files doesn't convert in Dabble's manuscript area.

**Solution needed:** Create a Python script to convert chapter .txt files to .docx with proper formatting:
- Convert `*text*` to italic runs
- Convert `**text**` to bold runs
- Convert `---` to centered scene break markers
- Preserve chapter/title structure
- Use `python-docx` library

**Workflow:**
1. Write chapters in .txt with `*italics*` markers
2. When ready for Dabble, run conversion script
3. Import .docx files into Dabble (rich text transfers correctly)

**Script location (when created):** `/workspaces/pilot/RESONANCE/scripts/convert_to_docx.py`

---

## End Session Protocol

When user says "run end session protocol":

1. **Draft the three dynamics answers from the session conversation** — do not ask the user to reflect from scratch. Observe what happened and write the answers yourself, then present them for quick approval or correction:
   - What did you redirect or override this session?
   - What surprised you?
   - Where was the friction?
   The user approves, corrects, or skips. One sentence each is enough. These go into the session log's "Session Dynamics" section.

2. **Update HANDOFF.md** with session work, decisions, and pending items.

3. **Run the script** in interactive mode: `python3 _tools/session_progress.py`
   Enter the dynamics answers when prompted.

4. **Update arc trackers** if character states changed.

5. **Note any new constraints** discovered.

---

## Session Log

### 2026-05-03 — Session 66 (Complete)

**Work Completed:**

**The Fold (CH11) — locked in canon:**
- Settled: the Fold takes BOTH people and structures
- GEOMETRY_TRACKER.yaml updated — `the_fold` definition under sensory_effects (relationship-to-drop, what-it-takes, visual, terminology, character-of-motion); `ch11_the_witness` chapter entry rewritten with Drop+Fold sequence
- CH11 back-update: body-fold beat in rescue, big-man-closer beat, closing courtyard fold

**Drop canon clarification (user correction):**
- YAML had drift: "All networked/augmented humans collapse" → corrected to "Every living person collapses. The Geometry is analyzing humanity for their data purposes — no exceptions by morphology or augmentation."
- "The Drop kills the bodies, the Fold removes what's left" was also drift → corrected to "the Drop puts people on the ground; the Fold removes them while they're down. The Drop is not lethal. The Fold is."
- The Drop is a census. Recoverable. Not a kill mechanism.

**CH10 line-level audit flags applied:**
- L14 (`hot stare`) and L101 (`body demanding payment`) — kept (somatic register, not interior leak)
- L104: `Warmth, salt, the slick of fat coating her tongue—all of it registers, and she feels it go down to her stomach.` → `Warmth, salt, the slick of fat coating her tongue. It goes down to her stomach.`
- L134: `with something that isn't anger—something older and harder to name.` → `like she's afraid to blink.`
- L146: cut `it changes nothing. No need fulfilled, no energy revived. Like texture without meaning.` — stone-in-her-chest already carries it

**CH11 line-level audit flags applied:**
- L11: cut `with the efficiency of someone who has been calculating this since before he heard the news` (narrator-explaining)
- L20: full reframe (continuity fix). User flagged that the big man's grief framing didn't track — the Drop isn't lethal, his family wouldn't have died from it. Rewritten as misplaced anger/fear with reputation hook back to CH10 old woman:
  - Original: `"You paid for fuel. You didn't pay for answers." His voice breaks. "My wife dropped. My brother dropped. Everyone I ever loved dropped. And she just stood there watching."`
  - New: `"You paid for fuel. You didn't pay for answers." His voice climbs. "When the bars came, we dropped. All of us. The whole town in the dirt with our teeth bit through. But her? Yeah, we heard of her. Word came a woman who stood. And she stood there. She didn't drop. So tell me what that makes her."`
- L54 (`Six. That's what the radius gave her.`) — kept, working as designed (load-bearing as reach + fold-distance double meaning)

**Session Dynamics:**
- **Major redirect:** offered three Option-style reconciliation paths for the Drop continuity question (purely census / lethal / variable severity). User cut through it: "EVERYONE dropped. Keep it simple. You AI keep adding layers to it that just complicate things." → saved `feedback_no_layering.md`. When canon seems contradictory, propose the simplest read first; don't generate Option 1/2/3 menus as the default.
- **POV slip recalibration:** user pushed back on flagging "hot stare" and "body demanding payment" as POV slips — these are externally observable somatic register, not interior. Saved `feedback_pov_slips.md`.
- **CH10 L137 protected:** the *other* big-man line ("my brother was human. And he dropped... Everyone except the machines.") is a categorization argument — works regardless of lethality. Kept as-is.

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH10_SHINING_DOWN.txt` (3 line-level edits)
- `RESONANCE/chapters/RESONANCE_CH11_THE_WITNESS.txt` (3 edits incl. big man reframe; fold beats added earlier in session)
- `RESONANCE/data/GEOMETRY_TRACKER.yaml` (Fold definition + Drop clarification)
- `HANDOFF.md` (Session 66 entry)
- `claude.md` (this entry)
- Memory: `feedback_pov_slips.md`, `feedback_no_layering.md`, MEMORY.md index

**Pending → Session 67:**
- Continue CH12+ line-level flags (CH12 epistemic register repetition, CH13 doubled lines, CH14 Reyes visibility)
- Write new CH2 opening (Morton's office through sublevel descent)
- CH2 server room beat structure (20-beat structure in Session 61 entry)
- Clean stale CH2 language ("transfer complete," "archive core," "progress bar," "decanting")
- Spot-check remaining chapters for unconverted Control/implant transmissions
- Docx rebuild when read is complete

---

### 2026-05-02 — Session 65 (Complete)

**Work Completed:**

**CH9 (THE DEPO') — close read complete:**
- All eight Session 64 flags applied (`Doesn't press.` → `He doesn't press.`, cut `The silence returns. Elena can't take it anymore.`, cut `She was about to deny it.`, cut `curious` from `Standard's voice is even, curious.`, collapsed `Elena clocks it. The relief in his face.` into the simile attached to physical beat, `Doesn't understand it.` → `She doesn't understand it.`, `The hull rings like a bell.` → `The hull shudders.`, cut Hendricks's repetitive `"Pulse-proof shielding, next-gen firepower. . ."` opener)
- Hendricks's `wet slide of bandages` (unreal sense detail) replaced with `Hendricks draws the revolver. It spins on his finger by the trigger guard—slow, balanced, easy.` — plants gunslinger muscle memory before line 107 names it
- `What about it.` → `What about it?` (Hendricks slightly more engaged; user call)
- `Riding the bones` moved to before `She flips the switch.` — Elena names the move first
- Black Box reference removed from Hendricks's NED timeline (continuity fix: Hendricks doesn't know the Box is in the Rover with them)
- Bullet/bolt terminology pass: lines 62, 105, 114 → bolt(s); line 28 ("two bullets" re Hendricks's revolver) correctly kept
- Elena: `Pulse-proof` → `Bolt-proof`. Hendricks: `Pulse-proof shielding` → `Boltproof shielding` (slight register variation, same in-world concept)
- `ordinance` → `ordnance`
- All straight quotes in CH9 converted to curly quotes
- Graze plant added at right→left vehicle pivot (`A round bites her side. She fires through it.`) — earns the closing image of "blood spreading on Elena's fatigues"

**Five typos fixed across chapters:**
- CH5: `looks Hendrick's way` → `looks Hendricks' way`
- CH6: `Elenas eyes roll back` → `Elena's eyes roll back`
- CH9: `in a millenium` → `in a millennium`
- CH23: `Standard remained buffering.` → `Standard doesn't answer. Four fills it.` (attribution fix — line 165 dialogue is Four's continuation, not Standard's)
- CH24: `The sound of computational thinking could almost be heard whirring.` → `The whir of computational thinking, almost audible.`

**CH10 (SHINE DOWN) — audit + edits:**
- Array description (lines 39–41) converted from narration to Elena/Hendricks dialogue. Section opener kept as Standard's framing. Elena delivers spec-knowledge ("Pre-Miracle panels. Forty percent on a good day."), deniable age joke "Almost as old as—" / Hendricks "Watch it" / Elena "—Hendricks' dad." Tactical close on infrastructure vulnerability.
- Hendricks's "unhelpful advice" (line 25) dramatized as actual coaching dialogue: "Lower your center" / "Shut up, Hendricks." / "Lean from the hips. More leverage." / "I will leave you here."
- "Yes, ma'am" line straight quotes → curly

**CH11 (THE WITNESS) — audit + new Geometry escalation:**
- Added the **fold** — structural deletion mechanism, distinct from the Drop (people-killer)
- Three deletion beats interspersed in rescue: bars descend; fence at far end folds along an axis the world doesn't have ("It edits"); clinic container folds (personal stakes); three more containers + solar panels rotate around an axis that doesn't exist in three dimensions, and is not
- Closing: "The fold is twenty meters off. Closing. / Six. That's what the radius gave her." — original line now doubles (her reach + fold's distance)
- Standard's voice held in third register: structural metaphors, geometric language, no machine vocab in interiority

**Open worldbuilding question:** does the fold take people, or only structures? Currently the fold edits "metal," "structure," "containers," "panels." Subsequent chapters will assume one or the other — to be settled.

**Session Dynamics:**
- **Redirect:** CH23 line 165 "Fuel vouchers, Seraphina..." — initially kept attributed to Standard via "Standard hesitates" minimal mechanical fix. User pushed back: line is Four's continuation of his "voice of God's personal rideshare" quip, answering his own rhetorical question. Reattributed to Four. Should have caught it on first read.
- **Surprise:** When integrating the fold into CH11, the existing "Six. That's what the radius gave her." line became a load-bearing double meaning (her reach + the fold's distance) without being touched. Original line carried the new structural work organically.
- **Friction:** Twice produced unnecessary option-menus when user already had clearer direction — "wet slide of bandages" replacement (3 options offered; user wanted revolver draw-and-spin), and "Standard remained buffering" attribution (kept ambiguous; should have read line 164→165 as Four's continuation).

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH5_THE_QUEUE.txt`
- `RESONANCE/chapters/RESONANCE_CH6_THE_REDACTED_SKY.txt`
- `RESONANCE/chapters/RESONANCE_CH9_THE_DEPO.txt` (extensive)
- `RESONANCE/chapters/RESONANCE_CH10_SHINING_DOWN.txt`
- `RESONANCE/chapters/RESONANCE_CH11_THE_WITNESS.txt`
- `RESONANCE/chapters/RESONANCE_CH23_THE_ICON.txt`
- `RESONANCE/chapters/RESONANCE_CH24_THE_SOVEREIGNTY.txt`

**Open Threads:**
- Settle fold-takes-people-or-just-structures question; back-update CH11 escape sequence (lines 54–59) for fold-aware urgency if needed
- Apply CH10/CH11 audit flags (line-level — see HANDOFF Session 65)
- Continue cover-to-cover read: CH12 next
- Update GEOMETRY_TRACKER.yaml with the fold mechanism
- New CH2 opening still pending (Morton's office through sublevel descent)
- Other inventory items (CH12 epistemic register, CH13 doubled lines, CH14 Reyes visibility, CH15 etc.)

---

### 2026-04-17 — Session 62 (Complete)

**Work Completed:**

**CH30 THE HANGAR — dialogue replaced:**
- Full Hendricks/Four exchange replaced with user-authored version
- Gender identity conversation added (Vessel/boats/grammar/they vs. other AIs)
- Sensor cluster dim moved to "Being loved" — earns its place
- VTOL hum moved to after "Said I was like a father"
- Narrator intrusion block cut; "I could continue the analysis internally—" replaced; "I figured" → "I do"
- Rest of chapter unchanged

**Methodology locked — Rhythm Rule for Dialogue and Description:**
- Tags/naked dialogue/physical beats are rhythm notes, not quality tiers
- Test: does this beat change how the reader receives the next line?
- No named silences — use ambient sound. Don't double-layer emotion and action.
- Saved to memory: `methodology_rhythm_dialogue.md`

**CH10 SHINE DOWN — rhythm pass:**
- Shoulders drop gloss cut; comparative clause in hunger interiority cut
- Three named silences removed: "changes. Thickens." cut, "hang in the air" cut, "shifts" cut
- "A bench scrapes back." added (user's choice over spoon suggestion)
- "The puzzle has added pieces, but they don't fit." cut
- "Or maybe just more human." cut
- "ma'am'd" line and "He walks over." both kept on user review

**Session Dynamics:**
- Redirect: "He walks over." — flagged as stage business, user correct to push back. Transit beat establishes proximity. Reversed.
- Surprise: Four named silences in old CH30 were an obvious pattern once rule articulated. Bench > spoon.
- Friction: Applied rule mechanically without testing context. It's a test, not a checklist.

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH30_THE_HANGAR.txt`
- `RESONANCE/chapters/RESONANCE_CH10_SHINING_DOWN.txt`

**Open Threads:**
- CH2 structural writes pending (new opening + server room beats + stale language cleanup)
- CH8 ration mechanic revision pending
- Cover-to-cover read: CH11 is next
- Transmission spot-check and docx rebuild when read complete

---

### 2026-04-03 — Session 60 (Complete)

**Work Completed:**

**Review app built** (`/workspaces/pilot/review_app/`):
- Flask server serving chapter text from `.txt` files, ordered via CHAPTERS.yaml
- Two-pane UI: reading pane (left) + prompt builder + notes (right)
- Text selection auto-captures to right panel; "Copy prompt to clipboard" formats chapter context + selected passage + constraints for pasting into Claude Code
- Notes panel persists per chapter via localStorage
- Transmission formatting: Control/implant lines converted from `_text_` italics to `<text>` angle brackets across CH2, CH5, CH7, CH8, CH16, CH17, CH32
- App renders `<text>` in distinct blue-grey style
- Start: `python3 review_app/app.py` → port 5001

**CH1 fix:** `*Her eyes open.*` de-italicized (was narrator, not internal voice)

**CH2 revision (user Dabble version integrated):**
- "Not speech — a data packet unfolding into words" → "A trill behind her back teeth, too rapid for language — and then it becomes language" (approved, kept)
- "Asset confirmed. Proceed to acquisition." replaces old infrastructure manifest line
- Cooling system extraction window cut (dead weight — promised a clock that the scene ignored)
- "Seals" → "Everyone, seals up"
- "Three liabilities" cut
- Aikin's competence reframed: confession before boast ("It's why your father tolerates me")
- Aikin betrayal: Elena discovers it herself via implant access to his wrist deck (replaces Control reporting it)
- `_idiot_` de-italicized in Goff's death line
- All transmission lines converted to angle brackets

**Methodology discussion — significant:**
Cross-project analysis of AI prose disease across Remanence, Resonance, Go Squad Book 1, Go Squad Book 2A. Key findings:

1. **The disease is an amplification mechanism, not random accumulation.** Early sessions establish defaults; later sessions amplify them. Different books developed different mutations (fragments vs. "the particular" tic) because different early defaults were established.

2. **Go Squad's escalation pattern is the human/AI boundary.** Book 1 early chapters (human original prose) are clean. Back half (AI revision takeover) is infected. The 9x fragment escalation is literally the handoff point made visible.

3. **"Be this person" vs "Write this person."** Remanence worked because the AI co-created characters from inside — embodiment, not description. Go Squad failed because the AI was handed existing characters and defaulted to narrator-with-facts. The Bellatrix steward output proves embodiment works mechanically even for outline generation.

4. **The "styleguide" is misnamed.** It's not a reference document — it's embodiment instructions. Cognitive architecture the AI inhabits before the first word, not character facts it consults while writing. The triplet-as-cognitive-architecture (Steward Experiment) is the mechanism. Specifying what the voice is *resistant to* is as important as what it does.

5. **Start fresh from the studs (Go Squad).** Retrofitting voice onto existing prose fights AI defaults sentence by sentence. Rebuilding from canon events + emotional geometry + character arcs, with embodiment instructions in place from word one, is how Remanence was made. Proof of concept: no one flagged Remanence as AI writing after disclosure.

6. **Beta reader protocol:** Let both readers finish unbiased. Their friction points (and non-friction points) are Phase 2 data — what the architecture actually does to a reader — needed before any rebuild begins.

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH1_RUDE_AWAKENING.txt` — de-italicized "Her eyes open."
- `RESONANCE/chapters/RESONANCE_CH2_THE_OFFERINGS.txt` — full Dabble revision integrated
- `RESONANCE/chapters/RESONANCE_CH5_THE_QUEUE.txt` — transmissions to angle brackets
- `RESONANCE/chapters/RESONANCE_CH7_MAKING_THE_DEPOSIT.txt` — transmissions to angle brackets
- `RESONANCE/chapters/RESONANCE_CH8_WHATS_IN_A_NAME.txt` — transmissions to angle brackets
- `RESONANCE/chapters/RESONANCE_CH16_THE_SILENT_HOUSE.txt` — transmissions to angle brackets
- `RESONANCE/chapters/RESONANCE_CH17_THE_SIGN.txt` — transmissions to angle brackets
- `RESONANCE/chapters/RESONANCE_CH32_FOLLOW_THE_LEADER.txt` — transmissions to angle brackets
- `review_app/app.py` — new
- `review_app/templates/index.html` — new
- `review_app/requirements.txt` — new
- `review_app/convert_transmissions.py` — new

**Open Threads:**
- Cover-to-cover read in progress (CH1–CH2 reviewed this session)
- Docx rebuild needed after read is complete
- Methodology: embodiment instructions / character styleguides to be developed for Go Squad rebuild
- Go Squad Book 1 and Book 2A: rebuild decision made, sequence TBD

---

### 2026-03-13 — Session 47 (Complete)

**Work Completed:**
- CH9–14 Array-to-Dam revision sequence: all four chapters rewritten and committed
- CH9: transit interiority added (Standard going somewhere for the first time); action sequence grounded (Standard at wheel keeping nose forward)
- CH11: Kellerman boards Rover; escape is chaotic/kinetic; Drop revival orienting beat; six survivors
- CH12: Pool/mud geography; heat sequence; everyone pushes then drops one by one; Standard alone face-down in mud at water's edge
- CH13: Pool geography throughout; amnesia reunion intact; no bridge/concrete; "she dragged them here and doesn't know their names"
- CH14: Structural splice fixed; Kellerman background presence; Hendricks speech ends "It's a lie"; seed/shooter lines cut
- CH22: Four/cells coherence motif installed (synchrony beat)
- CH44: Door mechanism grounded (temporal non-locality interiority passage)
- CH26–37 pacing diagnosis: section holds, no intervention needed
- Feedback locked: CH29 Standard's council speech imperfect composition is intentional
- New build: `RESONANCE_COMPLETE_20260313_171347.docx` (48 files, 93,687 words)

---

### 2025-12-20 — Session 1 (Complete)

**Work Completed:**
- Read complete Book 1 (Remanence, ~120K words)
- Created REMANENCE context engineering system
- Read existing RESONANCE materials (Ch 1-3, Codex, trackers)
- Wrote Chapter 4: The Convergence (~1,650 words)
- Integrated Codex v1 into HANDOFF.md
- Created character profile template
- Split character documents into profiles/ and state/
- Organized folder structure for both projects

**Session 1 Locks:**
- Elena age: 18 (was 17 during The Miracle)
- Elena experience: First major operation (NOT veteran)
- Hendricks Bomb: Elena does NOT know Hendricks shot the Child
- Thomas = Pilot's lover, NOT husband
- 287.3 Hz = frequency of consciousness
- Standard wakes from 287.3 Hz, BEFORE alien arrival

**Open Threads:**
- Brother Ash TBDs (ethnicity, sexuality) — fill before he appears
- Ash's compound physical description needed
- Book 2 ending TBD

**Session Reflection:** `/workspaces/pilot/sessions/2025-12-20_session1.md`

---

### 2025-12-26 — Session 11 (Complete)

**Work Completed:**
- Ran validators on Chapters 18-21 (all clean)
- Fixed Admiral Chen → Admiral Tien discrepancy in CHAPTERS.yaml
- Refined Four/Elena banter dialogue ("robot uprising handbook" exchange)
- Discovered Chapter 22 "The Leash" already complete
- Reviewed Act III planning, catalogued planted seeds needing payoff
- Drafted "Before the Verdict" scene (Elena/Standard moment) — not finalized

**Session 11 Updates:**
- CHAPTERS.yaml: ADMIRAL_CHEN → ADMIRAL_TIEN (2 occurrences)
- Confirmed chapters 1-22 complete (~40,000 words)

**Open Threads:**
- Path from Ch 22 → Geneva → Climax unmapped
- "The Gift" specifics not defined
- Four hot-swap payoff pending
- Dante sacrifice scene pending

**Session Reflection:** `/workspaces/pilot/sessions/2025-12-26_session11.md`

---

### 2026-03-11 — Session 40 (Complete)

**Work Completed:**
- Integrated ER=EPR as foundational physics for the Geometry
- Integrated temporal double-slit for Standard's temporal nature
- Retrofitted NED_EXTRACTION_MANIFEST.yaml with ER=EPR annotations
- Revised CH34 THE PROOF and CH35 THE ARCHIVE (surgical changes)
- Resolved CH24a open question: Geometry = one distributed consciousness

**Key Decisions Locked:**
- The Geometry IS the entanglement structure — they generate spacetime, don't inhabit it
- The Miracle = temporal interference pattern (Pilot/Seventeen as two temporal windows)
- 287.3 Hz = Miracle topology resonance frequency, NOT "Geometry's census marker"
- Standard's null status: two compounding physics layers (Remanence topology + temporal non-locality)
- Brook revival = temporal constructive interference via 287.3 Hz implant
- Geometry = one distributed consciousness (confirmed from CH24a prose)
- "You can't fight the shape of the space you're standing in" — new Dante line (CH34)

**Files Changed:**
- GEOMETRY_TRACKER.yaml (major additions)
- NED_EXTRACTION_MANIFEST.yaml (major additions)
- CHARACTERS.yaml (temporal_nature section added under Standard)
- RESONANCE_CH34_THE_PROOF.txt (3 surgical changes)
- RESONANCE_CH35_THE_ARCHIVE.txt (2 surgical changes)

**Next Session Priority:**
1. Epilogue structure — write with science punched up (temporal double-slit closed loop)
2. CH12/CH13 — confirm no scene work needed (prose already correct)
3. CH1 — assess whether "drilling high-pitch" needs any annotation

### 2026-03-12 — Session 45 (Complete)

**Work Completed:**
- Absorbed long brainstorming conversation clarifying AI-Ash/Control architecture (major corrections to Session 44 plan)
- Read all final-act chapters (CH39–CH45, EP) to map current prose state
- Wrote new chapter: `RESONANCE/chapters/RESONANCE_CH41_THE_DAUGHTER.txt`
- Chapter count now 46 (new CH41 inserted; existing CH41–CH45 need renaming to CH42–CH46)

**Key Corrections Locked (overrides Session 44):**
- Elena's deletion attempt is NOT a quiet grief moment at New Geneva — it happens DURING the finale confrontation with Ash, corners AI-Ash, triggers the puppeteering
- AI-Ash puppeteers Elena's body to attack Ash; Ash stabs her in self-defense not knowing she's controlled; her mercy is what AI-Ash weaponizes
- "Kid took my shot" (Hendricks) = Standard, not Elena
- Hendricks mourns Standard and Four; Elena survives in Template 3
- Epilogue needs TWO additions: (1) early mimicry scene during honeymoon phase (AI-Ash mimics Mironova, she laughs — establishes capability, shows who he was); (2) retrospective AI-Ash reveal

**THE DAUGHTER — Chapter summary:**
- Elena arrives alone at throne room; Ash is waiting
- Brief charged exchange: "It's over" / "That's what your mother said"
- Elena can't shoot him — love, not weakness
- She opens the deletion instead: tries to remove Control from her implant
- AI-Ash pushes back — puppeteers her body, uncertain agency rendered as "her arm rises. Or it does."
- Ash recognizes the Softing-quality in her face (he built this; never seen it on Elena)
- He stabs her with the ceramic blade in self-defense
- She goes down; the implant hums 287.3 Hz; "Stay" underneath; dark comes
- Chapter ends cold — Standard crashes in immediately after (current CH41/now CH42)

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH41_THE_DAUGHTER.txt` — new
- `/home/codespace/.claude/projects/-workspaces-pilot/memory/MEMORY.md` — AI-Ash corrections

**Renaming Still Needed:**
- CH41 HIGH NOON → CH42
- CH42 THE PILOT → CH43
- CH43 THE DOOR → CH44
- CH44 THE EXODUS → CH45
- CH45 THE SHORE → CH46
- Build script (`build_dabble_manuscript.py`) needs updating

**CH42 (current CH41 HIGH NOON) needs small revision:**
- Ash retrieves the revolver after stabbing Elena (he needs it when Standard crashes in)
- The ceramic blade wound on Hendricks happens during the Standard/Ash fight in THIS chapter (add one line — Ash uses the blade on Hendricks during the melee)

**Remaining Control Thread (not yet in prose):**
- CH2: Expand cadence moment — paralysis, "good hunting" wrongness
- CH5–CH8: Brief beats — signal fading near Standard, Elena noticing
- CH14: New Dam scene — Elena feels the silence, Standard fills it
- CH32: Control reconnects in Ash's voice — "Good hunting" — Elena goes cold
- CH43 (new THE DOOR): Add Marisol/AI-Ash confrontation — few beats, mercy without absolution, before she crosses to Elena
- Epilogue: Two additions (mimicry scene early + retrospective reveal)

**Next Session Priority:**
1. Rename CH41–CH45 files → CH42–CH46; update build script
2. Revise CH42 (current CH41 HIGH NOON): Ash retrieves revolver, ceramic blade wounds Hendricks during melee
3. CH43 (current CH43 THE DOOR): Add Marisol/AI-Ash confrontation beats
4. Epilogue additions (mimicry scene + AI-Ash reveal)
5. Earlier Control thread beats (CH2, CH14, CH32) — in that order

---

### 2026-03-11 — Session 44 (Complete)

**Work Completed:**
- CH31: Geometry attack targeting beat implemented (one sentence, Standard's POV)
- RESONANCE_TOPOLOGY.md Section IV written (Standard's census position at each major beat)
- Manuscript rebuilt: `RESONANCE_DABBLE_20260311_190928.docx` (45 chapters, 92,659 words)
- AI-Ash/Control architecture overhauled — full plan locked, not yet in prose

**Key Decisions Locked:**
- AI-Ash has no system access — just a consciousness on NED substrate with two relationships
- Both Ash and Elena know about the AI. Neither thinks they're being manipulated.
- Ash uses AI-Ash as go-between with Elena (can't father her directly). Elena keeps it for grief.
- AI-Ash edits both sides of the conversation. Adds subtext. Years of patient framing.
- Standard's proximity blocks Control's signal (same physics as Geometry protection)
- CH24a factory reset: AI-Ash loses Marisol voice disguise, reverts to Ash's voice
- CH32: Control reconnects in Ash's voice. "Good hunting, daughter." Elena hears it.
- Elena deletes Control not knowing it's AI-Ash — grief work, not confrontation
- Epilogue reveals what Elena never knew
- Elena's fatal wound (Ash's ceramic blade, CH41) needs more weight on the page

**Files Changed:**
- `RESONANCE/chapters/RESONANCE_CH31_KANGAROO_COURT.txt`
- `RESONANCE/data/RESONANCE_TOPOLOGY.md`
- `RESONANCE/RESONANCE_DABBLE_20260311_190928.docx`

**Next Session Priority:**
1. Decide: Control thread additions vs. Dabble read-through first
2. Control thread starts at CH2 — cadence moment, "good hunting" wrongness
3. CH14 Dam scene (new)
4. CH32 voice-drop moment (new)
5. CH41 weight (expand)
6. Epilogue reveal (small addition)

### 2026-03-11 — Session 43 (Complete)

**Work Completed:**
- Epilogue blank lines stripped (paragraphs run together within sections, blank lines kept around `---` breaks only)
- Reviewed AI-Ash architecture doc and all 8 Control chapters
- Decided against full architecture reveal (investigation scene, 5-layer cascade) — AI-Ash's presence handled as unexplained effects only
- CH5: directed pulse before Elena spots Standard
- CH17: acoustic-dampener beat holding the "how is Control reaching me?" question
- CH30: Four identifies Control as "a reproduction" — the one explicit moment

**Pending:**
- CH31: one beat flagging the Geometry's Deliverance attack as targeted (too precise for random sweep — someone fed coordinates)

**Next Session Priority:**
1. CH31 addition (small — one sentence during the formatting spread)
2. Dabble read-through
3. RESONANCE_TOPOLOGY.md Section IV
4. Chapter numbering audit

### 2026-03-11 — Session 42 (Complete)

**Work Completed:**
- Epilogue written and implemented: `RESONANCE/chapters/RESONANCE_EP_THE_BEDTIME_STORY.txt`
- Epilogue structure: linear, no narrator, opens on Lena Mironova's first immortality treatment, closes on Standard buried alive in the crate
- AI-Ash backstory locked: Ash's brainwaves as NED prototype control; Lena fell for the configuration, sought out the human original; AI-Ash's wound = rejection/inadequacy
- Nano-Skin introduced: emergency hemostatic nanotech, temporary, degrades — used by Hendricks in CH3
- CH3: legs/service corridor addition, Nano-Skin, "files it away" removed
- Manuscript-wide asterisk → underscore conversion (9 chapters)
- CH38 THE BEACONS compressed to 4 vessel sections
- Manuscript rebuilt: `RESONANCE_DABBLE_20260311_165130.docx` (45 chapters, CH24a excluded)

**Next Session Priority:**
1. Dabble read-through — apply italics manually, note edits
2. RESONANCE_TOPOLOGY.md Section IV
3. Chapter numbering audit
4. AI-Ash jealousy subtext audit in CH2-18

### 2026-03-11 — Session 41 (Complete)

**Work Completed:**
- Built RESONANCE_TOPOLOGY.md (Sections I, II, III, V — Section IV deferred)
- Section I: Full POV audit, all chapters read or verified against prose
- Section II: Seven interference events documented with corrected frames
- Section III: Thread map for Hendricks, Elena, Four + intersection map
- Section V: Closed loop documented as structural/physics fact
- Epilogue draft written to `RESONANCE/drafting/epilogue_draft.txt`

**Key Corrections Locked:**
- CH11: Standard single-anchor (not dual)
- CH32: Standard → Elena (Kael never holds POV)
- CH24a: Four as functional anchor despite transcript format
- CH12 interference frame: pattern going dark, not forward temporal pull
- CH24a interference frame: Standard in dissolution, not Four/Geometry census
- Ur-event: Pilot/Seventeen pre-book event documented as interference root

**Files Created:**
- `RESONANCE/data/RESONANCE_TOPOLOGY.md`
- `RESONANCE/drafting/epilogue_draft.txt`

**Next Session Priority:**
1. Epilogue — review draft, finish/revise, implement
2. RESONANCE_TOPOLOGY.md Section IV (Standard's topology)
3. CH3 cybernetic legs addition
4. Chapter numbering audit

---

## Folder Structure

```
/workspaces/pilot/
├── claude.md (this file)
├── HANDOFF.md (start-of-session briefing)
├── CONTEXT_ENGINEERING_FOR_FICTION.md
├── sessions/          (session reflections — trilogy-wide)
├── RESONANCE/
│   ├── chapters/      (Ch 1-4 drafts)
│   ├── characters/
│   │   ├── profiles/  (stable identity — 4 profiles + template)
│   │   └── state/     (dynamic per-chapter — 4 states + template)
│   ├── context/       (Codex, Entity Catalog, Constraints, Evaluator)
│   └── manifests/     (session manifests)
└── REMANENCE/
    └── (Book 1 reference materials)
```

---

## Quick Reference

**Blocking Constraints (Book 2):**
- Standard does NOT know she's an android
- NO Morton telegraphing ("Morton's gift", etc.)
- Elena transports Box, does NOT hand off at NED
- Hendricks removes Regulator ALONE, in apartment
- Standard wakes from 287.3 Hz, NOT alien signal

**Character States (Ch 4 End):**
- Standard: In rover, observing, doesn't know what she is
- Hendricks: Unconscious against Black Box, bleeding out
- Elena: Driving, exhausted, tactical decision made

**The Cargo:**
- The Void (Standard) — air-gapped, carries Source Code
- The Engine (Black Box) — powers Quiet Zone, 16,749 minds
