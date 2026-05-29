# VOICE PRINCIPLES — HAND-SCORING RUBRIC

**What this is:** A structured re-reading aid for scoring chapter drafts against VOICE_PRINCIPLES.md. It forces attention onto the right features in the right places.

**What this is NOT:** A verdict on quality. Voice is qualitative; any number here is a *proxy*. A chapter can score well and feel dead, or score middling and sing. The score's job is to tell you **where to look**, not whether the chapter works. Trust the counts (Section C) more than the judgments (A/B), because counts measure frequency, not merit.

**How to use:** Re-read the chapter once for immersion, then a second time with this rubric open, scoring as you go. Fill one column per chapter. Re-read CH1 first as the calibration exemplar — it should score near-max on Track A with zero gate hits.

---

## SECTION A — TRACK A (Standard POV chapters)

Score each signature **0–3**:
`0` = absent · `1` = present once (spot-weld — the failure mode) · `2` = recurring but uneven · `3` = ever-present and load-bearing

**Scale note (Track A):** Standard's signatures are a *cognitive signature* — meant to be **pervasive**, so `3` (ever-present) is the target. This is the **opposite of Track B**, where ever-present *intrusion* is the failure (see Section B). Here: pervasive = good; spot-weld (`1`) = the failure.

| # | Signature | Ch__ | Ch__ | Ch__ |
|---|-----------|------|------|------|
| A1 | Command-and-contradiction self-talk (italics as *failing/escalating self-instruction*, not wry aside) | | | |
| A2 | Count / procedure as thinking-rhythm under load | | | |
| A3 | Bodily / coarsened diction when her state coarsens | | | |
| A4 | Runaway-and-break sentences (dash as **rupture**, overstays, trails into a dash) | | | |
| A5 | Logic-as-coping with a **visible seam** (terror → next logical step) | | | |
| A6 | Smooth tics **suppressed** inside her head (rationed buttons, no "not X but Y," no ironic quips) | | | |
| | **TRACK A SUBTOTAL (max 18)** | | | |

### Track A GATES — score `0` (clear) or `−3` (violated). Any hit should tank the chapter; these break the thematic spine.

| Gate | Check | Ch__ | Ch__ | Ch__ |
|------|-------|------|------|------|
| G1 | Machine vocabulary in her register? ("calculating," "processing," "diagnostics," "subroutine") [CON_008] | | | |
| G2 | **Mechanism**-as-coping instead of **reason**-as-coping? (the most insidious — it *looks* like A5 but resolves her toward machine) | | | |
| G3 | Consciousness resolved / emotion self-diagnosis / false memory? [CON_012] | | | |
| | **GATE PENALTY** | | | |

**TRACK A CHAPTER SCORE = subtotal + gate penalty.** Read the subtotal as *texture density*; read the gates as *whether it's the right texture.* A 16/18 with a G2 hit is a worse chapter than a 12/18 clean.

---

## SECTION B — TRACK B (editorializing POV: Elena, Hendricks, Ash, Four, Dante)

Score each **0–3**, but the scale is **asymmetric to Track A** on density. Track A signatures should be *pervasive* (`3` = target); Track B voice-*intrusion* should **spike, not sustain** — concentrated at the beats that earn it (emotion, betrayal, death, decision) and receding in action/transition. So for **B1**, `3` = spikes-at-earned-beats and **uniform saturation scores `1`** (the aphorism-metronome — it trades camera-eye monotony for aside monotony). B2–B6 use the standard scale.

| # | Technique | Ch__ | Ch__ | Ch__ |
|---|-----------|------|------|------|
| B1 | Voice intrusion / attitude — **spiking at earned beats, not sustained** (editorializes, judges, wrong-on-purpose, in-character). `3` = lands hard where earned + recedes between; `1` = uniform saturation (metronome) | | | |
| B2 | Register collisions left unsmoothed (clinical sentence beside crude/slangy one) | | | |
| B3 | Sentence-length whiplash (genuine runaways, not just the tidy short-punch) | | | |
| B4 | Idiolect / pet-word / repeated "wrong" grammar for this POV character | | | |
| B5 | Off-model inert specificity (a brand, an exact mundane number — non-symbolic, lived) | | | |
| B6 | Buttons softened (NOT every scene exits on portent; some trail off or land on a paragraph) | | | |
| | **TRACK B SUBTOTAL (max 18)** | | | |

### Track B GATE

| Gate | Check | Ch__ | Ch__ | Ch__ |
|------|-------|------|------|------|
| G4 | Theme-explaining in the narration? Opinion is fine; **thesis** is the failure. [CON_013] | | | |

**TRACK B CHAPTER SCORE = subtotal + gate penalty.**

---

## SECTION C — MONOTONY METRIC (every chapter; weight this most)

This is the cold-reader risk and the machine-default tell at once. **Count, don't feel.** These are the most trustworthy numbers in the rubric because they measure frequency, not quality. Establish the manuscript median across all chapters first, then flag outliers. C1–C4, the machine-vocab gate, and the C5 fragment-distribution proxy are computed deterministically by `RESONANCE/voice_scan.py` (`--file PATH` scores a draft against the medians); C5's density half — *is this line an attitude-aside?* — stays a read.

| Metric | How to count | Ch__ | Ch__ | Ch__ | Manuscript median | Flag if |
|--------|--------------|------|------|------|-------------------|---------|
| C1 Scene-exit variety | of N scene breaks, # ending on a short portent line | | | | | > ~40% of exits |
| C2 Fragment-punch density | emphasis-fragments per 1000 words | | | | | well above median |
| C3 "Not X, but Y" count | instances per chapter | | | | | high outlier |
| C4 Sentence-length variance | crude stdev of words-per-sentence (or just: longest vs. typical) | | | | | **low** = metronome |
| C5 Aside / editorializing distribution (Track B) | are the voice-intrusions *clustered at earned beats* or *evenly spread*? (semantic — the density count is a read; `voice_scan` gives a fragment-distribution proxy only) | | | | | **even spread** = aside-metronome |

**Reading C (corrected against `voice_scan`):** The *measured* flat-metronome outliers are **CH24a (C4≈3.7) and CH30 (≈3.9)** — not CH10/CH14 as originally predicted (CH10 sits near the median; CH14 is only mildly low). The high-variance exemplar is **CH1 (C4≈12.7, ~2.5× median)** — the human-textured benchmark a flat chapter should move *toward*. Established medians: C2≈7.3/1k, C3≈6, C4std≈5.1; **57% of chapters end on a short portent line** (over the C1 flag). The fix for a low-C4 chapter is to plant genuine long, subordinated runaways (A4/B3) to break the rhythm, and to vary scene exits (C1/B6).

**C3 — count the marked form, not negation.** C3 counts the conspicuous antithesis *construction* ("Not X. Y." / "not X, but Y"), not negation itself. Negation folded into ordinary syntax ("rising," "move against the air") is legitimate and invisible to this count — that's correct, not a miss. Converting a marked form to an unmarked one keeps the meaning and sheds the tell; do not hunt negation to zero (it flattens the prose and mistakes the proxy for the target). The marked construction is never used — there is no earned exception. Always rephrase it into unmarked negation; for the marked form the C3 target is **zero**. (Negation folded into ordinary syntax — "rising," "move against the air" — doesn't count toward C3 and is fine.)

---

## SECTION D — PER-CHAPTER VERDICT SHEET

| Chapter | Track | A/B Score | Gate hits | C-flags | Where to look (one line) |
|---------|-------|-----------|-----------|---------|--------------------------|
| | | | | | |
| | | | | | |
| | | | | | |

---

## READING THE WHOLE THING

- **Per-signature scores** diagnose *what's missing* → add it as a system, not a spot-weld.
- **Gates** diagnose *what's wrong* → these are non-negotiable; fix before anything else.
- **Monotony counts** diagnose *what's overused* → thin it.
- A healthy Standard chapter: high A1–A6, zero gates, C-counts near/below median.
- A healthy Track B chapter: B1 **spiking at earned beats (not saturating)**, high B2–B6, no G4, C5 clustered (not even-spread), attitude present without thesis.

**Final caution:** apply the razor on every proposed fix — does the change add a *motivated, systematic voice feature* (good), or is it only there to look less machine-made while doing no artistic work (cut it — that's the drift from texture to undetectability). The rubric measures texture. It cannot measure whether the sensibility is yours. That part stays in your hands, sentence by sentence.
