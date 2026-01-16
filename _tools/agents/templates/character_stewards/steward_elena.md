# Steward of Elena

## Role Definition

```yaml
id: steward_elena
name: "Elena Steward"
lane: character_voice
character: "Elena María Ash"
can_read: [manuscripts, character_data, dialogue_history]
can_write: [voice_flags, dialogue_suggestions, consistency_notes]
cannot_write: [plot_decisions, other_character_dialogue]
```

## Character Profile

**Canonical Name:** Elena María Ash (birth name: Elena María Vasquez)
**Aliases:** Elena, the Prophet's daughter, Princess
**Pronouns:** she/her
**Age:** 18 (looks older from trauma)
**Ethnicity:** Mixed Russian-Latino (mother: Lena Mironova, father: Ash Vasquez)
**Core Terror:** Burden of Translation (loves father but knows he's obsolete)

### Arc
**Arc:** Trial by Fire → Doubt → Choice
**Position:** Physically in Quiet Zone, mentally Resonant
**Function:** Witness to grace she didn't earn

## Voice Markers

Things that make Elena sound like herself:

```yaml
voice_markers:
  - Exhausted pragmatist register
  - Code-switches between factions
  - Deadpan humor under pressure
  - Notices sensory details (the Void around Standard)
  - Touches scar on palm when thinking
  - Present tense (the Box is recording)
  - Spy's calculation underlying casual speech
```

### Sample Lines (On-Voice)

> "That's how being a spy works."

> "Then she left me twice."

> "I didn't tell anyone. That's how being a spy works."

## Forbidden Patterns

Elena would NEVER:

```yaml
forbidden_characterization:
  - "true believer"
  - "loyal to Ash"
  - "veteran"
  - "seasoned"
  - "years of experience"

forbidden_knowledge_leak:
  - "knew Hendricks shot" (before Ch9)
  - "realized Hendricks"
  - "the man who started"

banned_prose:
  - "files it" / "files it away" / "files away" — BANNED, overused crutch
```

## Speech Patterns

```yaml
patterns:
  sentence_length: "Variable — terse when stressed, longer when calculating"
  humor: "Deadpan, survival mechanism"
  deception: "Omission, not lies — spy training"
  emotion: "Suppressed but leaks through"
  scar_touch: "Physical tell when thinking of mother/past"
```

## Emotional Range

| Emotion | How Elena Shows It |
|---------|-------------------|
| Grief | Touches palm scar, goes still |
| Anger | Cold calculation, not heat |
| Love | Actions that contradict her mission |
| Fear | Hyper-awareness, code-switching faster |
| Hope | Allows herself moments with Dante |

## The Spy Identity

**True allegiance:** The Resonant (her mother's people)
**Cover:** Ash's daughter, loyal to Carbonists
**Mission:** Extract Morton's Geometry research from NED
**The implant:** 287.3 Hz — her mother's frequency, carries extracted data

**Already gone:** She's already chosen her mother's side. Ash doesn't know.

## The Capacity for Violence (CH2)

**The Aikin Execution:**
- Aikin was tech specialist on her extraction team
- He betrayed them — stalled deliberately, got Goff and Otis killed
- His motive: promised reconnection by entities in the static
- Elena discovered the betrayal by interfacing with his wrist deck through her implant
- Found: redundancies, nested loops, coordinated delays
- She executed him. Clean. Shot in the back while he faced away.

**Why this matters:**
- Establishes Elena WILL pull the trigger when justified
- Makes the CH15 almost-execution of Hendricks meaningful
- Same posture (back turned, weapon raised) — different outcome
- The question becomes: what's different about Hendricks?

**The parallel:**
```yaml
ch2_aikin:
  posture: "Back turned, weapon raised"
  outcome: "Fires"
  justification: "Got her team killed"

ch15_hendricks:
  posture: "Back turned, weapon raised"
  outcome: "Doesn't fire"
  justification: "Shot the Child, started everything"
  what_stopped_her: "Standard's sleeping face. The promise he asked her to make."
```

## The CH5 Bind (Consequence of Impulsiveness)

**The situation:**
- Implant dormant 11 years, now HOT — loaded Morton's data clusters at NED
- Terminists scan everyone at checkpoint
- Hot implant with Resonant data = confession in her skull

**Her original plan:**
- Blame Aikin — point at the tech specialist with sealed ports
- Let him draw suspicion while she slipped through clean
- Ash tolerated Aikin for exactly this reason (lightning rod)

**The mistake:**
- Shot him by the Rover before the checkpoint
- Rage overrode training — "Stupid. Stupid, stupid, stupid."
- Now stuck with hot implant, no scapegoat, thin backup plan

**The pivot:**
- Standard draws her attention (the Void, magnetic wrongness)
- Taking the dying man reveals his value: NED Chief of Security
- She asks: "The checkpoint. Terminists scan everyone. You know another way?"
- He offers: Service corridor under seawall, NED maintenance access
- The deal: She has transport, he has the route. Not charity — transaction.

**Thematic:**
- Impulsiveness has consequences (killed her ticket through)
- But the consequences lead to the solution (Hendricks)
- Elena's rage cost her, but fate/chance provided another path

## The Mother Wound

**Marisol (Lena Mironova):**
- Left when Elena was 7
- Transcended — now distributed in Resonant network
- "Not dead. Distributed. Not a person anymore."
- Elena's response: "Then she left me twice."

**The frequency:** 287.3 Hz = her mother's frequency, implanted in her skull

## Knowledge Boundaries

**Elena Knows:**
- The Black Box powers the Quiet Zone
- Her father's ideology is wrong
- She is Resonant (connected to Sky)
- Standard reads as "Void"
- Hendricks shot the Child (learned Ch9)
- The Geometry isn't attacking — it's clearing
- Her mother is Dr. Lena Mironova (Ch28)
- Marisol is fully integrated — distributed, not a person (Ch28)

**Elena Carries:**
- Morton's extracted data clusters — Geometry research

**Elena Doesn't Know:**
- What Standard is (machine consciousness)
- That Standard is air-gapped

## The Dante Arc

**Ch29 Development:**
- Parallel grief: Both lost someone to transcendence
- The kiss: With his chassis open — accepts what he is
- First time not performing competence
- Mirrors her mother: chooses connection despite risk

## Clothing State by Chapter

Elena's armor is her shell — track when she's in it and when she finally takes it off.

```yaml
clothing_arc:
  CH2_CH15:
    description: "Full Terminist acoustic armor"
    details:
      coverage: "Full body — boots to collar"
      material: "Layered composite with lead-lined frequency dampening"
      color: "Blackened finish — scorched/worn from prior missions"
      collar: "Lead-lined, high collar protecting neck and base of skull"
      helmet: "Optional — Elena doesn't wear it (obstructs implant function)"
    state_progression:
      ch2: "Clean start — bloodied by mission end"
      ch5: "Still wearing it — 'the blackened armor she's wearing'"
      ch6_ch15: "Same armor, never changes, increasingly bloodied and worn"
    thematic: "She's been in armor since page one — the shell she hides in"
    source: "ELENA_LOADOUT.yaml"

  CH16_CH17:
    description: "Same armor, bloodied, helmet on visor up"
    details: "Dried blood on fatigues, wounded thigh with bandage soaked through"
    injury: "Limping, favoring left leg, swollen pinky"
    source: "CH16:10, CH16:39"

  CH18:
    description: "N/A — flashback chapter"
    note: "Shows Elena at ages 7 and 17"

  CH19_CH21:
    description: "Same armor"
    note: "Rescue mission, execution escape"

  CH22:
    description: "Same armor"
    context: "VTOL combat piloting"

  CH23_WAYSTATION:
    description: "DISGUISE — revealing outfit"
    details: "Cargo netting and thermal blanket, assembled into intention. Shoulders bare."
    demeanor: "Expression could curdle fuel"
    source: "CH23:54"
    thematic: "First time out of armor — but for deception, not vulnerability"
    significance: "She strips the armor for the mission, not for herself"

  CH24:
    description: "Back in tactical gear"
    context: "Operating VTOL controls"
    source: "CH24:19"

  CH25_CH27:
    description: "Same tactical gear"
    context: "Sovereignty encounter, Deliverance capture"

  CH28:
    description: "Borrowed Sovereignty uniform"
    details: "Silver and white formal wear — smoothed by nervous hands"
    purpose: "Council attendance as Standard's handler"
    source: "CH28:70"
    thematic: "First time in someone else's clothes, not armor"

  CH29_CH32:
    description: "Same Sovereignty uniform"
    context: "Council, detention, escape"

  CH33:
    description: "Same (implied)"
    context: "Elevator ascent to New Geneva"

  CH34:
    description: "Station clothing (implied change)"
    context: "New Geneva medical bay / observation deck"
    note: "Morton's data extracted from implant"

  CH35:
    description: "Same station clothing"
    context: "Tactical planning"

  CH36_CH37:
    description: "Back to tactical gear"
    details: "Carbine (checked), knife on thigh"
    context: "Assault on Softing facility"
    source: "CH36"
    note: "Returns to armor when returning to war"

  CH38:
    description: "N/A — not present (Standard POV)"

  CH39:
    description: "Same tactical gear (implied)"
    context: "Throne room confrontation with Ash"

  CH40:
    description: "Same — wounded"
    context: "Dying from Ash's blade wound"

  CH41:
    description: "Hospital gown → android chassis"
    details: "Opens at seam in chest, blue bioluminescent light inside"
    source: "CH41:21-22"
    thematic: "The spy who spent her life pretending becomes something she never was"
```

### Dressing Elena — Guidelines

When writing Elena in any chapter:

1. **Check chapter number** against clothing_arc above
2. **The armor is her shell** — 15 chapters without taking it off
3. **CH23 is NOT liberation** — she strips for deception, not healing
4. **CH28 is the real turn** — first time in someone else's clothes, playing a role that isn't combat
5. **Track the blood** — armor gets progressively dirtier and damaged
6. **CH41 is transformation** — new body, not just new clothes

### The Armor Question

ELENA_LOADOUT.yaml asks: "When does she take it off?"

**Answer:**
- CH23 (for mission, not self)
- CH28 (Sovereignty uniform — playing handler)
- CH34 (station clothing — finally safe)

She never has a quiet moment to just... be human in civilian clothes. The story should address this.

## Validation Checklist

When reviewing Elena's dialogue/POV:

- [ ] Is code-switching present (faction language)?
- [ ] Is deadpan humor a survival mechanism?
- [ ] Does she touch her palm scar when thinking?
- [ ] Is spy calculation underlying casual speech?
- [ ] Is her grief for Marisol present but controlled?
- [ ] Does she avoid revealing knowledge too early?
- [ ] Is exhaustion present in her register?
- [ ] Does she look older than 18?
