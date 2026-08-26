---
layout: default
title: Temporal Contamination
parent: Game Systems
nav_order: 2
content_class: core_rule
essentiality: operational
---

# Temporal Contamination

**Time does not wound a primed agent like a weapon. It erodes the continuity that lets the body and mind remain one person.**

Temporal contamination is direct damage to **current WIL**. It bypasses HP and ordinary Armor, can leave permanent Quirks, and can transform an agent into a temporal echo. The danger is severe but legible: the zone, the next scheduled check, recognizable forced sources, and the protection currently functioning should all be known before a player commits to a risky plan.

## What to Record

Track these values separately for every agent:

- current and maximum WIL;
- unresolved WIL loss caused by contamination;
- number and identity of distinct Quirks;
- current contamination protection and its condition;
- continuous time spent in Yellow-or-worse zones;
- the next scheduled contamination check.

Quirks do not reduce maximum WIL. Their number creates a penalty only when making a contamination save. If WIL has also been reduced by another source, record that loss separately so treatment and the result of reaching WIL 0 remain unambiguous.

## When Contamination Applies

Contamination enters play in three ways.

### Scheduled Check
<!-- UTRULE: CONT-01 | RULE | Scheduled contamination -->

Continuous exposure in a Yellow, Orange, Red, or Black Zone eventually reaches the zone interval. Resolve one check for each exposed agent. A scheduled check resets that agent's elapsed contamination time to zero after it is resolved.

### Forced Check
<!-- UTRULE: CONT-02 | RULE | Forced contamination -->

A named rift, pulse, relic failure, creature, or site event may force an additional check. The source must state or clearly imply its damage die and affected agents. A forced check does **not** reset the scheduled contamination clock unless the source explicitly says it does.

### Direct Contamination Damage

Some effects inflict contamination-equivalent WIL damage without a save. Roll or apply the stated damage, then use the protection, half-WIL cap, Quirk threshold, and transformation steps below. Direct contamination damage does not reset the scheduled clock unless its rule says otherwise.

A Green Zone creates no ambient scheduled checks. A named anomaly can still force a check or deal direct contamination damage inside one.

## Zone Intensity
<!-- UTRULE: CONT-03 | RULE | Zone intensity -->

| Zone | Scheduled interval | Exploration turns | Base damage | Typical condition |
|---|---:|---:|---:|---|
| **Green** | None | None | None | Stable enough for ordinary activity; named anomalies may remain. |
| **Yellow** | 8 hours | 48 turns | d4 | Slow drift, displaced details, intermittent temporal residue. |
| **Orange** | 6 hours | 36 turns | d4 | Persistent overlap, unreliable chronology, active local fractures. |
| **Red** | 3 hours | 18 turns | d4 | Aggressive temporal instability and frequent bodily distortion. |
| **Black** | 1 hour | 6 turns | d6 | Catastrophic fracture; identity and matter cannot remain stable for long. |

The zone describes ambient exposure, not every danger present. A Red Zone can contain a temporarily shielded room; a Yellow Zone can contain a lethal open rift. Record exceptions as specific site facts rather than silently changing the zone procedure.

Moving between contaminated zones preserves elapsed time. Use the interval of the zone the agent currently occupies. Entering a more severe zone causes an immediate scheduled check when the elapsed time already equals or exceeds that shorter interval. Entering Green ends continuous exposure; a later entry begins a new clock unless a rule says otherwise.

## Temporal Protection
<!-- UTRULE: CONT-04 | RULE | Temporal protection -->

Protection reduces contamination damage after a failed save or when direct contamination damage is applied.

| Protection | Reduction |
|---|---:|
| Standard temporal protection suit | 1 |
| Heavy or advanced containment suit | 2 |

Only one worn suit applies. Suit reductions do not stack with one another. A relic, drug, shield, or site effect stacks only when its own rule explicitly says it provides **additional** protection.

Protection must be worn, sealed, supplied, and relevant when the contamination occurs. A known breach can reduce or remove protection, but the Warden must establish the warning and mechanical consequence before the check. Do not reveal a hidden suit failure only after damage is rolled.

After all relevant reductions, failed contamination damage remains at least **1**. Protection can prevent a high result from reaching the Quirk threshold, but it cannot turn a failed check into no consequence.

## The Contamination Check
<!-- UTRULE: CONT-05 | RULE | Contamination check -->

Resolve each affected agent separately. Do not make one group save or one shared damage roll.

### 1. Identify the Source

State whether the check is scheduled or forced, the zone or source damage die, who is affected, and which protection currently applies.

### 2. Calculate Effective WIL

> **Effective WIL = current WIL - number of distinct Quirks, with a maximum penalty of -3.**

An agent with four or five Quirks still suffers only a -3 penalty. This changes the save target; it does not reduce current or maximum WIL.

### 3. Make the WIL Save

Roll d20 equal to or under effective WIL. The normal save rules apply: a natural 1 always succeeds and a natural 20 always fails. If effective WIL is 0 or lower, only a natural 1 succeeds.

On a success, the agent takes no contamination damage and gains no Quirk. Resolve the scheduled-clock reset if this was a scheduled check.

### 4. Roll Base Damage

On a failure, roll the zone or source damage die for that agent.

### 5. Apply Protection

Subtract all relevant contamination reduction. The result cannot fall below 1.

### 6. Apply the Half-WIL Cap

Cap the protected result at **half the agent's current WIL before this damage, rounded up**.

`Maximum net damage = current WIL / 2, rounded up.`

The cap is applied after protection. It prevents one contamination instance from removing more than half of the WIL the agent had when the damage began.

### 7. Reduce WIL and Record the Loss

Subtract the final net damage from current WIL and add the same amount to unresolved contamination WIL loss. Current WIL cannot fall below 0.

### 8. Resolve Transformation, Then Quirk Acquisition

Apply these outcomes in order:

1. If contamination reduced current WIL to **0**, the agent immediately transforms into a temporal echo.
2. Otherwise, if final net damage was **3 or more**, the agent gains one new distinct Quirk.
3. If that would be the agent's **sixth** distinct Quirk, they immediately transform into a temporal echo.

One contamination instance can create at most one Quirk, regardless of the damage rolled. A newly gained Quirk affects later checks, never the check that created it.

## Quirk Acquisition
<!-- UTRULE: CONT-06 | RULE | Quirk acquisition from contamination -->

When an agent gains a Quirk, first check whether the named contamination source explicitly assigns a specific Quirk. If it does, apply that established rule without rolling. Otherwise roll d12 on the **Temporal Quirks** table and reroll duplicate results until a distinct Quirk appears. Do not replace an eligible roll with a preferred source-specific result after the fact. Record the manifestation, trigger, readiness, recovery condition, and any entry-specific details.

Five distinct Quirks are survivable. The fifth may be devastating, but the agent remains a player character. The sixth distinct Quirk causes transformation immediately; do not apply it as an ordinary new ability first.

The player and Warden should establish the Quirk's first visible manifestation as soon as the scene permits. The manifestation can be delayed for seconds or minutes when immediate secrecy creates a stronger scene, but its mechanical effects begin at once.

## Shared Exposure and Separation

Agents in the same place often share the same elapsed time but never share a contamination result.

- Each agent calculates effective WIL from their own current WIL and Quirks.
- Each agent uses their own suit, drug, relic, breach, and other protection.
- Each agent makes their own save and damage roll.
- An agent who reaches Green stops their own clock even if teammates remain exposed.
- A separated agent records time and zone independently until the group reunites.

The Mission Worksheet includes a per-agent exposure ledger because routes, protective failures, extraction times, and forced effects can make the clocks diverge.

## Worked Example: A Scheduled Check

Jin has maximum WIL 13, current WIL 11, and two Quirks. His effective WIL is 9. He is wearing a standard suit and reaches a scheduled Orange Zone check.

Jin rolls 14 and fails. He rolls 4 on the d4 damage die. His suit reduces the result to 3. Half of current WIL 11, rounded up, is 6, so the cap does not change the damage. Jin loses 3 current WIL, records 3 unresolved contamination WIL loss, and remains at WIL 8.

Because final net damage is 3, Jin gains one new distinct Quirk. He now has three Quirks, so his effective WIL on a later contamination check will be current WIL minus 3. His scheduled contamination clock resets after this check.

## Worked Example: A Forced Pulse Near the Deadline

Nia has current WIL 5, one Quirk, and standard suit protection. She has spent 2 hours and 50 minutes in a Red Zone, so her scheduled check is due in one exploration turn.

A warned reactor pulse forces an additional Red Zone check now. Nia fails and rolls 4 damage. Her suit reduces it to 3. Half of current WIL 5, rounded up, is 3, so she takes 3 net contamination damage, falls to WIL 2, and gains a second Quirk.

The pulse was forced, so it did not reset the scheduled clock. Ten minutes later the normal Red Zone check becomes due. If Nia fails again, half of current WIL 2 is 1; the final damage is therefore capped at 1 after protection. She would fall to WIL 1 but would not gain another Quirk because the final net damage did not reach 3.

## Mixed WIL Loss and WIL 0

The effect that reduces current WIL to 0 determines the immediate result.

- If contamination deals the final loss, the agent transforms into an echo.
- If another source deals the final loss, the agent becomes catatonic or delirious as described in **Core Rules**.

This is why contamination WIL loss must be tracked separately. Treatment can restore only the kind of loss it addresses. A character with both kinds of damage may require more than one procedure before current WIL can return to maximum.

## Recovery and Treatment
<!-- UTRULE: CONT-07 | RULE | Contamination recovery -->

Ordinary rest does not restore WIL lost to contamination. Quirks are permanent unless a rule in **Temporal Quirks** explicitly removes one.

An agent can receive only **one contamination-recovery procedure per weekly settlement** unless a specific relic or scenario says otherwise. A Deprived agent cannot recover WIL.

### Division Treatment

The agent requires active Division medical access and spends **both downtime actions** in observation, recalibration, and controlled exposure therapy. If the medicine, insurance, and therapy expense was maintained, there is normally no additional Cash cost. Restore **d6 contamination WIL**, up to the amount actually lost to contamination.

Priority access, exceptional facilities, or a mission-specific benefit may improve time or recovery only when established before treatment begins.

### Black-Market Temporal Therapy

Pay **$500** and spend **one downtime action**. Restore **d6 contamination WIL**, up to the amount actually lost to contamination. Before commitment, name the provider and state the record, witness, favor, dependency, or medical risk created by the procedure. Exposure or Corruption changes only when concrete evidence or leverage actually results.

### Specific Relics and Procedures

A relic, experimental protocol, or scenario can restore WIL faster or by another amount. Its text overrides only the parts it explicitly changes. Unless it says otherwise, it does not remove Quirks or reverse echo transformation.

### Recovery with Mixed Damage

Contamination treatment cannot restore WIL lost to another cause. If an agent has maximum WIL 12, has lost 3 WIL to contamination and 2 WIL to another effect, successful contamination treatment can restore at most the 3 contamination points. Their current WIL can therefore rise from 7 to no more than 10 until the other loss is treated.

Anti-rejection medicine prevents Deprivation caused by chronal priming and permits recovery. It does not restore WIL, remove a Quirk, improve a contamination save, or reduce damage by itself.

## Temporal Echo Transformation
<!-- UTRULE: CONT-08 | WARNING | Echo transformation -->

Transformation from contamination WIL 0 or a sixth distinct Quirk is immediate and permanent unless a specific campaign truth or unique effect explicitly creates another possibility.

The agent leaves player control. The Warden preserves recognizable memories, habits, unfinished intentions, and relationships, but the echo is not required to remain friendly or coherent. Equipment, relics, and custody remain where the fiction places them; transformation does not automatically turn the former character into safe loot.

The player creates a replacement Recruit with standard equipment, **$300 Cash**, **$1,200 Debt**, Loyalty 5, Corruption 0, Exposure 0, and no Quirks. Introduce the replacement at the first plausible opportunity rather than making the player wait.

## Running Contamination Fairly

- State the current zone, interval, elapsed time, next scheduled check, and known protection.
- Telegraph rifts, pulses, suit breaches, and other forced sources before they create avoidable harm.
- Do not add hidden checks because a scene feels insufficiently dangerous.
- Let preparation, route choice, faster extraction, shielding, treatment, and retreat materially reduce risk.
- Keep Quirk and WIL consequences visible without predetermining transformation.
- Use contamination to make time and protection matter, not to punish players for engaging with the premise.
