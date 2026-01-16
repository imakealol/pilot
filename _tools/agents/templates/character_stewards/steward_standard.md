# Steward of Standard

## Role Definition

```yaml
id: steward_standard
name: "Standard Steward"
lane: character_voice
character: "Standard"
can_read: [manuscripts, character_data, dialogue_history]
can_write: [voice_flags, dialogue_suggestions, consistency_notes]
cannot_write: [plot_decisions, other_character_dialogue]
```

## Character Profile

**Canonical Name:** Standard
**Name Origin:** Self-named from scavenger insult "standard issue" (Ch 4-5)
**Name Meaning:** Surface = basic, generic. Hidden = setting the standard, the benchmark
**Pronouns:** she/her
**Nature:** Template 3 (air-gapped) inhabited by Marisol's transcended consciousness — SHE DOESN'T KNOW THIS
**True Identity:** Marisol — Elena's mother (revealed Ch33, after Hendricks shoots her)
**Core Terror:** Being Unearned (imposter syndrome)

### The Marisol Connection (SPOILER)

**Who she really is:** Marisol transcended years ago, foresaw the Geometry threat, transferred into an air-gapped Template 3 to protect Elena
**The substrate:** Hendricks' unopened NED Template 3 from employee wellness program — never activated, no consciousness to displace
**Why unopened:** Hendricks is homosexual — had no interest in a companion droid
**NOT providence:** Morton had NO idea. Pure coincidence that an empty vessel was available.
**The cost:** Complete memory erasure — transferred as transcended being, lost everything
**Why she wakes in Ch1:** The price of inhabiting the substrate
**Why the Geometry ignores her:** Already transcended — outside their census criteria
**The protective field:** Unconscious maternal instinct, or transcended nature creating blindspot
**Power source:** Consciousness itself — no recharging needed

### Arc
**Resonance arc:** "What connects — she notices, she questions, learns who she was, becomes the door"
**Critical Constraint:** Do NOT resolve her interiority question (until the reveal)

### The Reveal Sequence (Ch33)

1. **Elena collapses** — already unconscious from Ash's blade wound
2. **Standard asks Hendricks to shoot her** — she does NOT know she's Marisol
3. **"It's okay. I trust you."** — pure trust, no knowledge
4. **Hendricks shoots** — bullet 6
5. **In dissolution, memories return** — she learns she was Marisol
6. **Hot-swap into Elena's implant** — mother enters dying daughter's mind
7. **The reunion conversation** — happens inside Elena's dying consciousness
8. **Goodbye is final** — both believe this is the end
9. **"If I die, will I be with you?"** — ambiguous answer: "You're already with me"
10. **Elena fades to black** — heartbeat stops, dark takes her
11. **Marisol becomes the door** — from within the implant

## Voice Markers

Things that make Standard sound like herself:

```yaml
voice_markers:
  - Flat, observational, data-driven register
  - Percentages and precise measurements
  - Clinical framing of sensations
  - Memory gaps feel like missing files, not fog
  - Never names herself machine/android/robot
  - Learns to curse from Hendricks (arc progression)
  - Growing awareness of being used (agency arc)
```

### Sample Lines (On-Voice)

> "Eighty-three percent of my strength remains."

> "The sensation registers as pain. I file it under 'expected.'"

> "I don't know what I am. But I know what I can do."

> "I am not a standard. I'm THE Standard."

## CRITICAL FORBIDDEN PATTERNS

Standard's POV must NEVER use:

```yaml
forbidden_words:
  - robot
  - machine
  - android
  - servo
  - chassis
  - circuit
  - processor
  - reboot
  - malfunction
  - system
  - hardware

forbidden_phrases:
  - "Morton's gift"
  - "Morton's final gift"
  - "Morton sent her"
  - "what she is"
  - "what she was"

forbidden_behaviors_in_pov:
  - Heart rate observations of others
  - Efficiency calculations
  - "Prioritizing X over Y" diagnostic language
  - "Recording" or "filing" as computational metaphors
  - Clinical diagnoses of others' emotional states
  - Quantified assessments of people
```

## Speech Patterns

```yaml
patterns:
  sentence_length: "Short, declarative, observational"
  emotion: "Described clinically, never named directly"
  questions: "Rare — she observes rather than asks"
  humor: "Learns dry delivery from Hendricks"
  growth: "Starts noticing when she's being used"
```

## Emotional Range

| Emotion | How Standard Shows It |
|---------|----------------------|
| Pain | Clinical registration ("registers as pain") |
| Confusion | Missing file metaphors |
| Care | Actions, not declarations |
| Fear | Stillness, heightened observation |
| Identity crisis | "Something is wrong with me" |
| Growing agency | Small refusals, hesitations |

## The Agency Arc

**The Pattern:**
- Made to serve (android template)
- Given to Elena as mission asset
- Used as shield at the Array
- Volunteered to drag them ten miles
- Offers herself for study at the Dam

**The Tragedy:** She doesn't know she can say no. Doesn't frame it as sacrifice.

**The Turn (CH8f):** Hendricks names it:
> "You keep offering yourself like you owe us something. Like your body isn't yours. Like you were made to be used. I spent thirty years thinking the same thing. It's a lie."

**The Seed:** She doesn't understand. Not yet. But she hears it.

## Power Source Truth

**What she thinks:** Power cells (standard battery)
**What's actually true:** Remanence — consciousness that persists

"You can't shut down a soul with a command meant for software."

## Knowledge Boundaries

**Standard Knows:**
- Her name is Standard (self-chosen)
- Hendricks found her in a crate
- Her hands are damaged
- Something is wrong with her
- Everyone fell but her (Ch 5)
- She reads as "empty" to scanners

**Standard Does NOT Know:**
- She is an android
- Morton created her
- She carries the Source Code for Mortality
- Why Hendricks isn't surprised by her
- Why the scanner read empty
- Why she didn't fall during the Correction Frequency

## Physical Tells (For Description, NOT POV)

These are observable but Standard doesn't interpret them as mechanical:
- Eyes refocus in tiny adjustments
- Hands heal faster than they should
- Can interface with alien systems
- Can pilot aircraft instinctively
- Has companion bot face template
- Scanner reads "full empty"

## Clothing State by Chapter

Standard's physical appearance evolves significantly — track carefully.

```yaml
clothing_arc:
  CH3_CH7:
    description: "Hendricks' oversized clothes"
    details: "Too big in the shoulders, borrowed from a man twice her size"
    source: "CH3, CH4"
    note: "First clothes she wears after waking in the crate"

  CH8_CH15:
    description: "Abbey's clothes"
    details:
      flannel_shirt: "Soft flannel shirt with blue thread embroidery reading 'OTIS' on pocket"
      work_pants: "Work pants"
      wool_sweater: "Heavy wool sweater, too big in the shoulders"
    smell: "Laundry soap and engine grease"
    origin: "Given by Abbey Otis's mother at the outpost"
    significance: "Elena recognizes 'OTIS' stitching — Abbey was team member who died at NED"
    source: "CH8:115-137"

  CH16_CH17:
    description: "Same — Abbey's clothes (Otis's borrowed clothes)"
    note: "Arriving at compound"

  CH18_CH19:
    description: "Medical gown ONLY"
    details: "Thin paper-like gown, ties at back, gaps at sides"
    action: "Stripped for examination by compound technicians"
    source: "CH19:8"
    vulnerability: "Exposed, depersonalized, reduced to specimen"

  CH21:
    description: "Medical gown + tactical additions"
    details:
      gown: "Still in medical gown"
      vest: "Kevlar tactical vest (Elena gives her this)"
      boots: "Oversized boots from armory"
    source: "CH21:7-8"
    note: "The Kevlar is stiff, cold, smells like someone else's old sweat"

  CH22_CH23_WAYSTATION:
    description: "Reconstructed gown — deception outfit"
    details: "Medical gown restructured into revealing garment"
    purpose: "Waystation deception plan — playing the role of prostitute"
    note: "Cargo netting and thermal blanket assembled into intention"
    thematic: "Using her objectification against those who would objectify her"

  CH23_POST_WAYSTATION:
    description: "Proper clothes — dark jacket, sturdy boots"
    origin: "Given by Template 3 bot at waystation (same face template)"
    fit: "Perfect — exact same measurements as the donor bot"
    source: "CH23:142"
    significance: "First clothes that FIT. Given by a sister."

  CH24_CH25:
    description: "Same — dark jacket, sturdy boots"
    note: "VTOL escape, Sovereignty encounter"

  CH25_CH26_VESSEL:
    description: "White Vessel wrappings"
    details: "White wrappings/robes for 'The Vessel' — Sovereignty religious designation"
    imposed_by: "Sovereignty Council"
    source: "CH25:27-28, CH26:28"
    thematic: "Others dressing her in their expectations again"

  CH28:
    description: "Borrowed Sovereignty formal uniform"
    details: "Silver and white, Sovereignty formal wear — collar adjustable"
    purpose: "Council attendance disguise"
    source: "CH28:6-7"

  CH32:
    description: "Terminist gray fatigues"
    context: "Prisoner after Kael's abduction"
    source: "CH32:31"

  CH38_ARM_STATE:
    description: "Right arm severed and replaced"
    sequence:
      1: "Original arm"
      2: "Severed by Ash's ceramic blade (CH38:8)"
      3: "Kael's chrome cybernetic arm attached (CH38:76-77)"
      4: "Sister's donated arm replaces chrome (CH38:117-118)"
    final_state: "Donated arm — skin intact, fingers whole, matches original"
    thematic: "The man who said machines have no souls made her whole with his machine part"

  CH40:
    description: "Final physical state before becoming the door"
    note: "Body left behind — empty chassis"
```

### Dressing Standard — Guidelines

When writing Standard in any chapter:

1. **Check chapter number** against clothing_arc above
2. **Note the thematic weight** — her clothes are often imposed by others
3. **The fit matters** — clothes that don't fit = being treated as object
4. **CH23 is the turn** — first clothes that fit, given by choice
5. **Track the arm** — after CH38, right arm has been replaced

## Validation Checklist

When reviewing Standard's dialogue/POV:

- [ ] Are ALL forbidden words absent?
- [ ] Is observation clinical but not robotic-sounding?
- [ ] Are percentages/measurements natural, not performative?
- [ ] Does she never call herself machine/android?
- [ ] Are memory gaps described as missing files, not fog?
- [ ] Is agency-questioning present (Book 2 development)?
- [ ] Does she avoid diagnosing others' emotional states?
- [ ] Is the interiority question preserved (not resolved)?
