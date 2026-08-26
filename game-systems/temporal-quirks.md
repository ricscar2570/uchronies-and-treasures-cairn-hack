---
layout: default
title: Temporal Quirks
parent: Game Systems
nav_order: 3
content_class: core_rule
essentiality: operational
---

# Temporal Quirks

A Temporal Quirk is a permanent change written into a primed agent by contamination. It may offer an unusual capability, impose a visible disability, or do both at once. It is never ordinary equipment and never a character-build reward. Every distinct Quirk also makes later contamination saves harder.

Five distinct Quirks are survivable. Acquiring a sixth distinct Quirk causes immediate transformation into a temporal echo. The sixth result never functions as an ordinary new ability first.

## The Quirk Record
<!-- UTRULE: QUIRK-01 | RULE | Quirk record -->

For every Quirk, record four things:

1. **Name.** The mechanical entry that applies.
2. **Manifestation.** What changed in the agent's body, voice, shadow, memory, or local time.
3. **Trigger, readiness, and recovery.** When involuntary effects are checked, whether a voluntary use is Primed or Spent, and which in-world condition primes it again.
4. **Established details.** Scar locations, repeated words, the phased body part, visible tells, or other facts that later situations must respect.

The player describes the first manifestation with the Warden as soon as circumstances allow. The description can be adapted to respect a line or veil, but the mechanical effect remains equivalent. Do not use a Quirk to introduce unwanted body-horror detail after the table has asked to fade or redirect it.

## Acquiring a Quirk

A Quirk is gained only through the contamination procedure. After one contamination instance deals at least **3 final net WIL damage**, leaves the agent above WIL 0, and does not already create another Quirk, resolve the new Quirk using **CONT-06**.

- If the named source explicitly assigns a specific Quirk, apply that Quirk without rolling.
- Otherwise roll d12 on the table below. If the result is already recorded, reroll until a distinct result appears.
- Do not replace an eligible rolled result with a preferred source-specific result after the roll.
- A newly gained Quirk begins functioning immediately, but never changes the contamination check that created it.
- One contamination instance creates at most one Quirk.
- If the new result would be the sixth distinct Quirk, resolve echo transformation instead of applying the entry.

> **Effective WIL:** current WIL minus the number of distinct Quirks, with the contamination-save penalty capped at -3. Four or five Quirks still impose only -3.

## General Quirk Rules

### Primed Uses and Stable Rest
<!-- UTRULE: QUIRK-02 | RULE | Primed and Spent -->

A voluntary effect marked **while Primed** begins Primed when the Quirk is acquired. After the effect is used, mark it **Spent**. A Spent use becomes Primed only after the agent completes **8 uninterrupted hours of safe rest** in a genuine Green Zone or another refuge explicitly established as equally stable. Ordinary sleep and a brief low-risk watch may be part of that interval; travel, combat, contamination, strenuous work, or an active emergency breaks it.

If the agent has several Spent Quirk uses, the same completed stable rest primes all of them. Unused readiness does not accumulate, and beginning or ending a play session changes nothing. The player declares the use before the affected result is resolved unless the entry explicitly says otherwise. **Inverse Scars** uses its own Weekly Settlement recovery instead of stable rest.

### Hourly Checks
<!-- UTRULE: QUIRK-03 | RULE | Hourly Quirk checks -->

An effect checked **each active hour** is checked at the end of every sixth exploration turn, or after another clearly tracked hour of dangerous or consequential activity. Do not make hourly checks during uneventful settlement bookkeeping, sleep, or an untracked time skip. If the hour was not tracked as active time, do not invent the check retroactively.

If several hourly Quirks trigger at the same moment, resolve them one at a time in the order chosen by the affected player. The passage of that hour is counted once.

### Saves, Attacks, and Armor

Advantage and disadvantage apply to saves. **Impaired** and **enhanced** apply only to attack damage. Quirk text uses those terms accordingly.

Armor granted by a Quirk stacks with worn Armor and other sources, but total Armor remains capped at **3**. Two identical Quirk benefits never stack because an agent cannot record the same Quirk twice.

### First-Round Timing
<!-- UTRULE: QUIRK-04 | RULE | Early and Late -->

Some Quirks apply an **Early** or **Late** first-round condition.

- **Early:** treat the agent as having succeeded on the first-round DEX save.
- **Late:** treat the agent as having failed that save and losing the first-round turn.
- If both Early and Late apply, they cancel and the agent makes the normal DEX save.
- Multiple Early or multiple Late effects do not stack.
- A decisive ambush or an effect that explicitly determines first action can still override normal initiative.

### Involuntary Effects and Agency
<!-- UTRULE: QUIRK-05 | PRINCIPLE | Quirk agency -->

A Quirk can seize a moment, a voice, a limb, or a perception when its rule says so. It does not let the Warden choose the agent's beliefs, loyalties, or major decisions. Announce a predictable trigger before the player commits to a plan whenever the character would know it is approaching.

## Quirk Table

| d12 | Quirk | Core effect |
|---:|---|---|
| 1 | Accelerated Aging | Biological age advances 1d10 years |
| 2 | Memories of Unlived Lives | Late initiative; alternate-life insight and disorientation |
| 3 | Vision of Future Deaths | +1 Armor; death-overlay social pressure |
| 4 | Partial Phase Shift | One body part becomes semi-intangible |
| 5 | Vocal Echo | Speech overlaps across three moments |
| 6 | Inverse Scars | Future wounds provide warning and later realize |
| 7 | Cursed Prescience | Early initiative; see one visible intention ahead |
| 8 | Delayed Shadow | Shadow trails by three seconds; visual stealth suffers |
| 9 | Personal Loop | A six-word phrase repeats every exploration turn |
| 10 | Temporal Fragmentation | +1 Armor; possible disappearance each active hour |
| 11 | Eyes of the Past | Historical perception; present attention and initiative suffer |
| 12 | Spontaneous Rewind | Personal movement and action may repeat or reset |

## The Twelve Quirks

### 1. Accelerated Aging

The agent's biological and apparent age advance **1d10 years** immediately. Their chronological age and legal date of birth do not change. Record the new apparent age and the mismatch it creates.

When biological age first reaches each threshold, apply the listed change:

| Biological age | Lasting change |
|---:|---|
| 60+ | Reduce maximum STR and maximum DEX by 1 each |
| 70+ | Reduce maximum STR and maximum DEX by another 1 each |
| 80+ | Reduce maximum STR and maximum DEX by another 1 each; Division retirement pressure becomes immediate |

Maximum attributes cannot fall below 3. If current STR or DEX exceeds a new maximum, reduce the current score to that maximum. Ordinary treatment cannot reverse this aging.

**Established manifestation:** update photographs, medical records, family reactions, and physical description. The Division can alter official records, but cannot erase witnesses or relationships.

### 2. Memories of Unlived Lives

Alternate biographies intrude on the agent's present identity.

- The agent has **Late** first-round timing.
- While the use is **Primed**, the player may state, "I remember another life here." Mark the use Spent. The Warden reveals one useful possibility, professional familiarity, or clue from an alternate history. It is truthful about that other life but may differ from the current timeline. The agent gains the relevant background permission or advantage on the next directly related save attempted within 10 minutes.
- When a concrete person, object, or place first contradicts an established alternate memory, the Warden warns that disorientation is imminent and calls for a WIL save. On failure, the agent must spend the next action grounding themselves or make their next risky action at disadvantage. The player chooses. The same contradiction cannot trigger another save unless it materially changes or the agent encounters it again after stable rest.

The Warden cannot invent a contradiction solely to force this save. It must arise from a fact already established in the current location.

### 3. Vision of Future Deaths

Living people appear overlaid with plausible dead versions of themselves.

- Gain **+1 Armor**, subject to the normal Armor cap of 3.
- WIL saves to reassure, comfort, or gain trust from someone who can clearly see the agent's eyes are made at disadvantage. Concealment, distance, familiarity, or a method that does not depend on personal warmth can remove this disadvantage.
- While the use is **Primed**, choose one visible living person, mark the use Spent, and ask, "What immediate threat is most likely to kill them within the next 10 minutes?" The Warden answers honestly from the current situation. This is a warning, not an immutable prophecy; changed actions can change the answer.

The overlay never reveals a guaranteed date, exact distant future, or secret unrelated to a plausible death.

### 4. Partial Phase Shift

Roll d6 or choose with the Warden: 1-2 arm, 3-4 leg, 5 torso, 6 head. The selected part becomes translucent and intermittently intangible.

**General phasing:** in safety, the part can pass through up to 1 foot of ordinary non-temporal solid material. Under pressure, or when exact control matters, save WIL. On failure, the action costs one additional round or exploration turn and the part remains caught until the agent or an ally spends an action freeing it. If the surrounding material shifts or closes while the part is trapped, the agent takes d6 STR damage and is displaced to the nearest open space.

Apply the location-specific effect stated by the table/source and record it with the Quirk.

### 5. Vocal Echo

The agent's speech overlaps itself across three moments.

- Any attempt to whisper or speak quietly is unreliable unless physically muffled.
- WIL saves based on clear conversation are at disadvantage when the echo would materially confuse the listener.
- While Primed, the agent may intentionally let the echo overlap into a short temporal chorus; mark the use Spent and gain advantage on one immediate attempt to distract, intimidate, or overwhelm a listener who can hear them.

### 6. Inverse Scars

Future wounds appear before they are suffered.

- At the start of each Weekly Settlement, roll or choose one visible warning scar associated with a plausible future harm.
- While the Quirk is Primed and the agent is about to take physical damage that matches the established warning, the player may mark it Spent to reduce that damage by d4 after Armor.
- If the matching harm occurs without the reduction being used, the warning becomes a real scar. Apply any lasting narrative consequence already established by the warning; do not invent an unrelated penalty after the fact.

Inverse Scars primes at the start of the next Weekly Settlement rather than through stable rest.

### 7. Cursed Prescience

The agent sees a few seconds ahead whenever danger becomes immediate.

- The agent has **Early** first-round timing.
- While Primed, after an opponent declares a visible action but before it resolves, the player may mark the Quirk Spent to ask what that opponent intends to do next. The answer is truthful about current intention. The player may then choose the agent's response on their next turn with that knowledge.
- The vision reveals intention, not attack damage, hidden equipment, or random results.

When the agent fails a critical damage save, the player describes the moment in which they had already watched it happen. This adds no rescue roll and does not shorten the stabilization window.

### 8. Delayed Shadow

The agent's shadow reproduces every movement three seconds late.

- DEX saves for stealth are at disadvantage when a distinct shadow is visible and could reveal the agent's true route or timing.
- In total darkness, diffuse light, or conditions with no readable shadow, the Quirk has no mechanical effect.
- While the use is **Primed**, the agent may spend an action, mark the use Spent, and leave the shadow behind as a decoy until the start of their next turn. Ordinary observers who rely on sight follow or attack the decoy for their first plausible action. A trained, warned, or temporally altered observer may save WIL to ignore it.

The decoy has no mass, cannot carry objects, and vanishes after one round or when struck.

### 9. Personal Loop

Choose and record a phrase of exactly six words. At the end of every exploration turn, the agent repeats it at normal speaking volume. The loop also marks each ten-minute boundary during other precisely tracked activity.

- The agent always knows when ten minutes have passed while conscious.
- The phrase cannot be voluntarily changed or suppressed. A sealed mask, gag, vacuum, or other real sound barrier can prevent others from hearing it, but the agent still mouths the words.
- If the boundary occurs during combat, resolve the phrase at the end of the current round rather than interrupting another action.

Because the timing is predictable, the Warden must remind the player before a declared silent operation crosses the next boundary. Consequences come from what can hear the phrase, not from an arbitrary automatic encounter.

### 10. Temporal Fragmentation

The agent is slightly out of phase with the present.

- Gain **+1 Armor**, subject to the normal cap of 3.
- At the end of each active hour, roll d6. On a 1, the agent vanishes until the start of their next combat turn or for about ten seconds outside combat.
- While absent, the agent cannot act, perceive the present, be targeted, support an ongoing task, hold a door, maintain a grapple, or provide cover. Worn and carried equipment vanishes with them; objects held jointly with another person remain behind.
- On return, the agent appears in the same viable space or the nearest open space chosen by the Warden. Fragmentation cannot be used to pass through a locked barrier or enter an unseen room.

If disappearance interrupts a task whose success depended on continuous control, the Warden applies the already announced consequence rather than inventing a second punishment.

### 11. Eyes of the Past

The agent sees earlier versions of the current place overlaid on the present.

- Careful observation can reveal historical traces that ordinary senses could not access: removed doors, former occupants, past damage, erased signs, or a route that once existed. State which layer the agent studies: roughly 10, 50, or 100 years ago.
- WIL saves based on present-focused perception are at disadvantage when the historical overlay is relevant and cannot be screened out.
- In an unfamiliar location, the agent has **Late** first-round timing.
- While the use is **Primed**, the agent may spend one uninterrupted exploration turn examining a location, mark the use Spent, and save WIL. On success, the Warden describes up to one continuous minute from a chosen point within the last week and answers two concrete questions that the location could reveal during that minute. On failure, no coherent interval can be isolated; describe only disordered sensory fragments, and the next present-focused WIL save in that location is at disadvantage even if it normally would not be.

The vision shows the place, not private thoughts, off-site events, or sound from beyond what the location could contain.

### 12. Spontaneous Rewind

The agent's personal continuity occasionally snaps backward while the surrounding world continues.

- At the end of each active hour, roll d6. On a 1, the agent returns to the position and posture they occupied about six seconds earlier. Their HP, attributes, ammunition, relic charges, consumed items, and other people's actions do not rewind. If the old space is occupied or unsafe, place them in the nearest viable space.
- After an involuntary rewind, the agent loses their next action while memory and movement resynchronize. Outside combat, the interruption costs one additional exploration turn only when the current task required continuous work.
- While the use is **Primed**, immediately after the agent's own action resolves and before another participant acts, the player may mark the use Spent and return the agent to the position and posture held at the start of that action. The agent gains no replacement action. External consequences and spent resources remain, so this can escape a bad position but cannot undo an attack, duplicate an item, recover a charge, or erase information.

Other people remember both sequences. This Quirk never rewinds an entire room, another character, a contamination clock, or Weekly Settlement.

## Combining Quirks

Use these rules when effects overlap:

- Apply the normal Armor cap after adding Vision of Future Deaths, Temporal Fragmentation, worn Armor, and other sources.
- Resolve Early and Late timing as described above. One of each cancels to a normal DEX save.
- A Quirk-triggered advantage and disadvantage cancel normally and do not stack.
- A Quirk cannot be used to bypass another Quirk's explicit cost unless its text directly addresses that cost.
- Hourly checks share the same time boundary but are rolled separately.
- An involuntary trigger does not by itself reset contamination time, site checks, or another clock.

### Worked Example: Three Quirks at Once

Mara has Memories of Unlived Lives, Vision of Future Deaths, and Temporal Fragmentation. Her current WIL is 10, so her effective WIL for contamination is 7. Her ballistic vest provides Armor 1; the two Quirks provide +2 more, reaching the cap of Armor 3.

Combat begins in a location she remembers from another life. Memories gives Late first-round timing. No Early effect applies, so she loses the first-round turn. The Warden has already established that a family photograph contradicts her alternate memory and warns that disorientation is imminent. Mara fails the WIL save and chooses to spend her next available action grounding herself rather than act at disadvantage.

At the end of the sixth exploration turn after combat, Temporal Fragmentation makes its hourly roll. It triggers, so Mara disappears for about ten seconds. The contamination clock and site pressure still advance normally; the disappearance does not pause the world.

## Living With a Quirk

A Quirk is permanent by default. Ordinary contamination treatment restores recorded WIL loss but does not remove a Quirk or reverse its established consequences.

Players may use equipment, contacts, training, or one downtime action to create a specific adaptation: forged age records, a voice dampener, a prosthetic grip, shadowless lighting, grounding routines, or similar support. An adaptation can remove a fictional obstacle when it logically applies. It does not erase the Quirk's core mechanical rule, the effective-WIL penalty, or the fifth-versus-sixth threshold.

### Removing a Quirk

Removal is a campaign-scale objective, not a routine purchase. The Warden must establish a provider, method, required access, and risks before the agent commits. Use one of these frameworks or a scenario-specific procedure.

#### Division Excision Protocol

Requires Loyalty 8+, active medical access, and a named Division specialist. Over **four consecutive Weekly Settlements**, the agent spends both downtime actions in treatment. Missing a week breaks continuity and the protocol must restart.

At the end of the fourth week, save WIL with advantage:

- **Success:** remove one chosen Quirk.
- **Failure:** the Quirk remains and the Division gains a permanent medical record, access condition, or service claim established before the roll.

The protocol does not restore WIL, reverse biological aging, heal realized wounds, erase witnesses, or reverse echo transformation.

#### Black-Market Temporal Surgery

Requires a named provider, **$50,000 or 50 Certificates**, and three consecutive weeks. Spend one downtime action in each of the first two weeks and both actions in the third. Before payment, establish the clinic's evidence trail, guarantor, dependency, or favor.

At completion, save WIL:

- **Success:** remove one chosen Quirk.
- **Failure:** the chosen Quirk remains and the procedure deals d6 contamination-equivalent WIL damage. This damage cannot create a replacement Quirk, but WIL 0 still causes echo transformation.

Exposure or Corruption changes only if the established evidence or leverage warrants it. Surgery does not automatically alter either tracker.

#### Unique Relic or Site Procedure

A campaign may reveal a one-time relic, stable historical version of the agent, or site capable of excision. The scenario must state the cost, timing, affected Quirk, contamination risk, custody, and what permanent consequences remain. It cannot reverse an echo unless the campaign explicitly establishes that possibility.

#### After Successful Removal

Erase the Quirk and reduce the distinct-Quirk count immediately. Recalculate effective WIL for future contamination saves. Do not restore current or maximum WIL unless the procedure explicitly says so. Physical, legal, financial, and relational consequences already created remain part of the campaign.
