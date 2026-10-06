---
layout: default
title: Loyalty & Corruption
parent: Game Systems
nav_order: 4
---


## Loyalty & Corruption: The Dual System

### The Trackers

Loyalty and Corruption are two independent trackers, scale 0-10. They are **not** opposites. You can have both high. You can have both low.

- **Loyalty** measures how much the Division trusts you.
- **Corruption** measures how deep you are in Zhou's network.

**Loyalty is not "good." Corruption is not "evil."** They are measures of allegiance. The system records. It does not judge.

### The Loyalty Scale

| Value | Status | Consequences |
|---|---|---|
| 0-1 | Traitor | Division hunting you. Shoot-on-sight. |
| 2-3 | Suspect | Constant surveillance. Colleagues avoid you. |
| 4-6 | Neutral | Standard agent. No special treatment. |
| 7-8 | Trusted | Once per week, improve one successful Division performance band by one step (maximum Exceptional). Priority Division medics: 3 days instead of 1 week. |
| 9-10 | Division Hero | Keep Trusted benefits. Base Division pay +50%; mission allowance and bands unchanged. Mission-issued military equipment is loaned, not a cash award. |


**Benefit timing.** Use Loyalty immediately before a mission's rewards are resolved, before adding that mission's Loyalty gain. Trusted benefits change Standard to Strong or Strong to Exceptional; failure, an already Exceptional result and a separately briefed bounty do not improve. Only one eligible mission per agent per accounting week receives the improvement. It is never a separate $200 bonus.

At Loyalty 9-10, multiply **base pay only** by 1.5: a Recruit receives $1,200 before any disciplinary pay cut. Use rank and Loyalty recorded at the start of the paid week; changes take effect next week. Do not multiply allowances, performance pay, bounties or side income. During Instability, the benefit lock below suspends these special benefits, not ordinary base pay or medicine access.

### The Corruption Scale

| Value | Status | Consequences |
|---|---|---|
| 0 | Clean | Zhou doesn't know your name. |
| 1-2 | Dabbling | First offers arrive. Small favors, small costs. |
| 3 | Asset | Zhou shifts from offers to requests. See below. |
| 4 | Entangled | Regular customer. Refusing has consequences. |
| 5 | Watched | The Division suspects. See below. |
| 6 | Deep In | Automatic weekly offers. Side jobs expected. |
| 7 | Leveraged | Zhou has something on you. See below. |
| 8 | Committed | Zhou provides everything. Extraction is difficult. |
| 9-10 | Zhou's Property | You are not free. Division arrest order imminent. |


### Corruption Threshold: 3

At Corruption 3, Zhou considers the agent a confirmed asset. The dynamic shifts.

**Zhou stops making offers and starts making requests.** The first request is small: surveil a location for one night, carry a sealed package across town, confirm a name. Pay is $300. The framing is professional. But refusal has a cost: Zhou "withholds" $500 in payments from previous transactions for "administrative processing." Only unpaid receivables can be withheld: never subtract already-paid Cash or create a negative Cash balance. If less than $500 is pending, withhold only that amount. The money may or may not be returned.

> This is the mechanical moment where the agent realizes the relationship has changed. They are no longer a client. They are a resource.

### Corruption Threshold: 5

At Corruption 5, the Division has enough to act on suspicion, not enough to act on evidence.

**A second agent appears on every Division mission.** The Warden controls this NPC. They are professional, competent, and say little. The agent does not know with certainty whether this person reports to Hayes. They might be a standard field partner. They might be an informant. Every grey action in the field is now a gamble.

> The Warden should play this ambiguity honestly. Sometimes the second agent is just a second agent. Sometimes they report back. Players should not be able to reliably determine which. The uncertainty is the mechanic.

**Interaction with Raines:** Corruption 5 and the fifth completed Raines job can establish the same surveillance escort; they do not create two escorts. Raines-related reassignment pressure can coexist with that escort.

### Corruption Threshold: 7

At Corruption 7, Zhou has documentation.

**Zhou possesses something: a recording, a document, a witness who will testify.** She does not use it immediately. She uses the fact that she has it. Each time the agent attempts to refuse a job from Zhou, the Warden rolls d6. On a 1-2, Zhou makes the threat explicit in that conversation. The agent must make a **WIL save**. On a failure, they are **Deprived** for one week from stress (cannot recover HP or attributes until they complete a full week of rest outside active zones).

> Zhou's leverage is not a death sentence. It is a slow ratchet. Each refusal risks activating it. The agent can still refuse. They just cannot refuse without cost.

### Instability

Instability applies only when **Loyalty >= 3, Corruption >= 3, and |Loyalty - Corruption| <= 2**. It represents active double allegiance. Loyalty 0 / Corruption 0 and Loyalty 2 / Corruption 0 are not unstable.

1. **Faction-specific pressure.** Risky social saves with Division personnel, Zhou's network, or intermediaries who know about the divided allegiance are made with **disadvantage**. Do not roll for an ordinary conversation or a sound agreement that needs no save. Uninformed civilians and unrelated factions are unaffected. This is not the d4 damage rule for impaired attacks.
2. **Weekly suspicion.** At weekly close, if unstable, roll d20 once: **1-5**, Hayes suspects (WIL save or -2 Loyalty); **6-10**, Zhou doubts (WIL save or her next offered job tests allegiance; refusal remains possible); **11-15**, mark -2 to the next WIL save caused by this weekly suspicion procedure; **16-20**, no new consequence. The marked -2 is used once and does not stack. Do not apply it to the event-table roll, ordinary social saves or contamination. The two suspicion saves are pressure saves, not social interactions; they do not automatically suffer social disadvantage.
3. **Benefit lock.** While unstable, suspend the Loyalty 7+ band improvement, Loyalty 9+ base-pay increase and special equipment access, and Corruption 8+ preferential provision. Ordinary wages, existing debts and equipment already issued remain. Priority medical care still follows actual Loyalty 7+ and is not suspended by this benefit lock. Check mission benefits at resolution and payroll benefits at the start of the paid week; restored access never creates retroactive pay.
4. **A crisis, not a forced allegiance.** Count consecutive weekly closes at which the PC is still unstable after suspicion is resolved. At the third, present incompatible demands from both factions, each with stated costs of refusal. Players may satisfy one, bargain, expose the conflict, seek another patron or refuse both. Refusal can cost access, resources or protection; it never lets the Warden select the PC's allegiance or action. Reset the crisis count to 0 after a crisis; another three unstable closes may create a new one.

**Ending Instability:** when any activation condition ceases to hold, Instability ends; clear the consecutive-week count and unused suspicion penalty. Tracker changes come from actions and recorded consequences, not from declaring a side. A crisis can remain unresolved in the fiction after the mechanical condition ends.

### The Instability Rule

> "You want to play both sides? Both sides will be watching."

The system doesn't prevent the grey build. It makes it costly and risky, as it should be.
