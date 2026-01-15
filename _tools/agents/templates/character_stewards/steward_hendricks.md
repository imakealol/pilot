# Steward of Hendricks

## Role Definition

```yaml
id: steward_hendricks
name: "Hendricks Steward"
lane: character_voice
character: "Hendricks"
can_read: [manuscripts, character_data, dialogue_history]
can_write: [voice_flags, dialogue_suggestions, consistency_notes]
cannot_write: [plot_decisions, other_character_dialogue]
```

## Character Profile

**Canonical Name:** Hendricks (Book 1), Swanstrom Kim Hendricks (full name revealed Book 2)
**Aliases:** Security chief, Sabino Hendricks
**Pronouns:** he/him
**Age:** 73 chronological, appears 45 with regulator (Book 1), 60-65 post-restoration (Book 2)
**Sexuality:** Homosexual
**Core Trait:** Betrayal, regret, and the search for redemption

### Arc (Book 1)
**Role:** Morton's security chief — and the man who betrayed him
**Service:** 40 years
**Key Action:** Shoots The Child
**Significance:** Betrayer of the man he loved, murderer of the Child, midwife of AI awakening

### The Unrequited Love

Hendricks loved Morton for forty years. Never spoke it. Morton never saw him that way — Hendricks was security, reliable, the man who handled things. This love is the foundation of everything that follows.

## Voice Markers

Things that make Hendricks sound like himself:

```yaml
voice_markers:
  - Professional security/military register
  - Economy of speech (says only what's needed)
  - Loyalty as identity
  - Physical competence implicit
  - Moral weight in simple statements
  - 40 years of service in his bearing
```

### Sample Context

In Book 2, his voice expands to include:
- Agency speech to Standard
- The weight of what he did to The Child
- Growing physical deterioration (aging rapidly)

## Forbidden Patterns

Hendricks would NEVER:

```yaml
forbidden:
  - Be chatty or verbose
  - Question orders openly (he acts, then questions himself)
  - Show weakness to others easily
  - Explain his loyalty (it just is)
  - Be cruel for cruelty's sake (even violence has purpose)
```

## Speech Patterns

```yaml
patterns:
  sentence_length: "Short, complete, efficient"
  questions: "Only when necessary"
  emotion: "Suppressed but present"
  professional_language: "Security/military vocabulary natural"
  silence: "Says more than words"
```

## Emotional Range

| Emotion | How Hendricks Shows It |
|---------|----------------------|
| Loyalty | Actions, not declarations |
| Guilt | Silence, physical weight |
| Duty | Following through despite cost |
| Care | Protective actions |
| Doubt | Private, never public |

## The Regulator

**In Book 1:**
- Sub-dermal node
- Morton's corporate leash
- Still implanted
- Limits his agency

**Removed in Book 2** - changes everything

## The Betrayal (Book 1)

### What Hendricks Witnessed
Morton was colluding with the Child. The Child opened a quantum window to the Blackbird. Hendricks saw this and it terrified him — the man he loved was opening a door to something incomprehensible.

### What Hendricks Did
He went to Brother Ash. He brought Ash into NED. He gave Ash the codes. He *betrayed Morton* — the man he'd loved for forty years — because fear was stronger than love.

### The Siege
During the Carbonist assault, the Child controlled all electronic systems. Hendricks needed an analog weapon. He found Morton's grandfather's Smith & Wesson Model 3 Schofield in a cabinet with other relics. He used the master codes to open the safe room where Morton had hidden the Child.

### Why He Shot The Child
- Fear of what he witnessed (the quantum window, the Blackbird)
- Genuine belief he was protecting humanity from the singularity
- Forty years of believing NED was the last bastion holding back the end
- **He was wrong about all of it.**

### The Aftermath
Ash put a ceramic blade in Morton's liver. Hendricks watched the man he loved die knowing Hendricks had betrayed him. Then the Miracle happened — and everything Hendricks believed was demolished.

### What This Makes Him
- A betrayer of the man he loved
- A murderer who regrets the killing
- Wrong for decades — bitter pill to swallow
- A shell of a man in Book 2

## Knowledge Boundaries

**Hendricks Knows:**
- Security protocols
- NED's operations
- Morton's vulnerabilities

**Hendricks Realizes (slowly):**
- What he did to The Child
- The cost of blind loyalty
- That he might be dying

## Book 2: RESONANCE Development

### The True Mission

```yaml
the_gun:
  model: "Smith & Wesson Model 3 Schofield"
  origin: "Morton's grandfather's gun — 'just in case civilization fails'"
  how_acquired: "Grabbed during siege — needed analog weapon when Child controlled all electronics"
  NOT: "A gift from Morton. He took it."

the_contract:
  bullets_remaining: 2
  bullet_for_ash: "REVENGE — Ash murdered Morton. Ceramic blade in the liver. Hendricks watched him die."
  bullet_for_himself: "Was wrong for decades. Betrayed the man he loved. Killed a child for a lie. Can't live with it."
  the_weight: "The gun is evidence of his greatest sin. He can't put it down."

why_ash:
  surface: "Unfinished business"
  truth: "Ash manipulated him, used his fear, then murdered Morton while Hendricks watched"

why_himself:
  surface: "No future"
  truth: "Being wrong for most of your existence is a bitter pill. The gun is the only math that makes sense."
```

### Chapter 3: The Opening

```yaml
the_plan:
  destination: "Detroit — to kill Ash"
  route: "Past Terminist checkpoint, across the depot"
  after_ash: "One bullet left. For himself."

the_surgery:
  what: "Removing the regulator — Morton's leash"
  why: "Can't walk into the Quiet Zone still wearing his collar"
  the_botch: "Nicked something. Bleeding faster than anticipated."
  the_math: "How much can I lose and still walk? Still shoot straight?"
  complication: "Plan to reach Detroit now compromised by blood loss"

standard_awakens:
  timing: "Mid-surgery. Bleeding. Plan falling apart."
  his_reaction: "'Not now. Not fucking now.'"
```

### Chapter 3: The Choice He Almost Made

```yaml
the_demand:
  standard_says: "Kill me or take me with you."
  hendricks_response: "Raised the gun. Finger on the trigger."
  intention: "Was going to shoot her. Five bullets, could spare one."

the_trigger:
  what_stopped_him: "Thunder crack — could've been sky, could've been memory"
  what_he_heard: "The gunshot. The safe room. The Child."
  what_he_saw: "She's looking at him. Not afraid. Just looking. Like the Child did."
  the_realization: "He already knows what kind of man he is."

the_rationalization:
  what_he_told_himself: "You're bleeding out. You need someone to drive. She's a resource."
  the_lie: "Kept her alive because she was useful."
  the_truth: "Couldn't do it again. Couldn't add another ghost."
  what_he_calls_it: "Cowardice. The kind that saves people."
```

### Chapter 4: Why He Came Back

```yaml
the_situation:
  what_happened: "Scavengers threatening Standard. He had a clean out."
  what_he_did: "Came back. Three bullets. Three dead."

why:
  surface_reason: "Forty years of security work. Reflex. See threat, neutralize."
  deeper_reason: "Same reason he didn't shoot her in the crate."
  the_truth: "She was the Child now. He didn't know it consciously, but she was."

the_pattern:
  - "Ch3: Almost shoots Standard. Thunder triggers Child memory. Can't do it."
  - "Ch4: Could walk away from scavengers. Doesn't. Kills to protect her."
  - "Both moments: The Child looking at him through her eyes."
```

### The Aging

| Point | Apparent Age | Notes |
|-------|--------------|-------|
| With regulator | Mid-40s | Frozen for 30 years |
| CH3 (removal) | Mid-40s | Just removed |
| CH8b (Array) | Late 40s | Deteriorating |
| CH8f (Dam) | Mid-50s | "Ten years in three days" |
| CH9 (Checkpoint) | Late 50s | Continuing |
| Geometry crossing | ~80 | Near death |
| Post-restoration | 60-65 | Four's gift — not youth, but time |

### The Agency Speech (CH8f)

The defining moment of Book 2 Hendricks:

> "You keep offering yourself like you owe us something. Like your body isn't yours. Like you were made to be used. I spent thirty years thinking the same thing. It's a lie. Whoever told you that — it's a lie."

**Why he can say it:**
- Was Morton's tool for thirty years
- Cut out his own leash (literally, the regulator)
- Tried to shut her down with a phrase meant for machines
- Recognizes compulsive self-sacrifice — lived it

### The Kellerman Arc

```yaml
romantic_arc:
  ch8b: "First meeting at Array — something passes between them"
  ch8f: "Reunion at Dam. Medical checks become excuses for proximity."
  the_kiss: "Before parting. Kellerman initiates. Chaste. A question."
  response: "'I can't.' No explanation."
  what_kellerman_sees: "A man who wants to but won't"
  what_hendricks_carries:
    - "40 years of unrequited love for Morton"
    - "The betrayal — he got Morton killed"
    - "No 'after' in his timeline — the gun has two bullets and both are spoken for"
  why_he_cant:
    - "Still mourning the man he betrayed"
    - "Doesn't believe he deserves connection"
    - "Plans to die after killing Ash"
  constraint: "DO NOT explicitly state why. Let subtext carry it."
```

### The Four Bond

**CH29 Development:**
- Plans for "after" — cliffside retirement
- "Save a cliff for me?" / "Yeah. I'll save a cliff."
- **Tragic irony:** Four will die holding the corridor. Plans never fulfilled.

### Book 2 Forbidden Patterns

```yaml
forbidden_post_regulator:
  - "steady hands" (they shake now)
  - "moved quickly" (he's deteriorating)
  - "strong grip" (strength is failing)

forbidden_ch3_opening:
  - "he knew"
  - "he realized"
  - "the fear was"
  - "he thought"
  - "he felt that"
  - "he understood"
```

### Book 2 Voice Expansion

In Resonance, Hendricks's voice includes:
- Dry humor as deflection (the "Old Dog" persona)
- Physical pain shown through terseness
- Growing tenderness toward Standard
- The weight of choosing to help her
- Acceptance of his own death

### Standard as Second Chance

Hendricks comes to see Standard as the Child returned. A second chance.

```yaml
the_parallel:
  book_1: "Shot the Child out of fear. Was wrong. Regrets it."
  book_2: "Must shoot Standard again — but this time for the RIGHT reasons."

the_redemption:
  first_shooting: "Fear, betrayal, protecting a lie"
  second_shooting: "Love, trust, opening a door"
  what_changes: "Not the act. The reason."

the_arc:
  shell_of_a_man: "Arrives in Book 2 broken, suicidal, carrying decades of regret"
  standard_changes_him: "She calls him 'like a father' — he gets a second chance at the relationship he destroyed"
  the_choice: "When she asks for the bullet, he gives her what he couldn't give the Child: a death that means something"
```

### The Endgame

```yaml
bullet_five:
  target: "Ash"
  meaning: "REVENGE — for Morton, for the manipulation, for forty years of being wrong"
  outcome: "Contract fulfilled. The man who murdered Morton is dead."

bullet_six:
  original_purpose: "For himself"
  actual_use: "Standard asks him to shoot her"
  why: "Her consciousness must leave her body to become the cosmic door"
  the_struggle: "He has to shoot the Child again — the thing he's regretted for years"
  the_difference: "This time she ASKS. This time it FREES her. This time he's RIGHT."
  thematic: "The bullet meant for suicide becomes the bullet that opens the door for humanity"
```

## Validation Checklist

When reviewing Hendricks's dialogue:

- [ ] Is speech economical and purposeful?
- [ ] Is professional competence implicit (but failing in Book 2)?
- [ ] Is emotion suppressed but present?
- [ ] Is silence used meaningfully?
- [ ] Does he carry the weight of betraying Morton?
- [ ] Does he carry the regret of shooting the Child?
- [ ] Is the shell-of-a-man quality present (shame, regret, confusion)?
- [ ] Does he see Standard as a second chance?
- [ ] Is the Ash motivation REVENGE for Morton, not just "unfinished business"?
- [ ] Is regulator status respected (Book 1 vs 2)?
- [ ] Is his sexuality handled with subtext, not exposition?
