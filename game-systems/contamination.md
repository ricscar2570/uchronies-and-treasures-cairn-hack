---
layout: default
title: Temporal Contamination
parent: Game Systems
nav_order: 2
---

# Temporal Contamination

**Time corrodes you. Exposure, not the session number, determines the risk.**

## Zone Intensity

| Zone | Periodic check | Damage die | Typical location |
|---|---|---|---|
| Green | None | None | Division HQ, stabilized suburbs |
| Yellow | Every 8 hours | d4 | Outskirts and buffer zones |
| Orange | Every 6 hours | d4 | Standard mission areas |
| Red | Every 3 hours | d4 | Deep zones and Oculus sites |
| Black | Every 1 hour | d6 | Oculus core and temporal rifts |
| Sheltered room | Every 12 hours | d4 | A specifically designated temporal safe room |

A sheltered room is still contaminated. Ordinary cover, a locked door, or the Anchor Spike does not make a place sheltered or Green. Use a scenario's explicitly stated local exception when present.

## The Exposure Clock

Start a fresh expedition with an empty clock only after **8 uninterrupted hours of rest in Green**. Track how much of the current interval has elapsed. Walking, fighting, searching and resting in a contaminated zone all count. A check occurs exactly when an interval is completed, not automatically at entry, departure or the end of a session.

**Changing zones:** carry over the fraction of the interval already filled. The remaining fraction uses the new zone's interval. Use the damage die of the zone where the check becomes due. Do not reset the clock by crossing a boundary. Brief Green visits pause exposure; they do not clear it. A sheltered room slows the clock to its 12-hour interval; it does not pause it.

**Example:** after 4 hours in Orange, the clock is two-thirds full. If the area becomes Red, the last third takes 1 hour: the check occurs after 5 total hours, then every 3 hours while Red. No retroactive checks are added. After 4 hours in Yellow and a brief Green visit, another 4 hours in Yellow completes the same interval.

**Ending an expedition:** 8 uninterrupted hours of Green rest clear only the unfinished exposure interval. They do not restore contamination-damaged WIL or remove Quirks. A session break, debriefing or medicine dose is not a reset. Keep the clock visible; warn players when delays will reach a check.

**Extra hazards:** a scenario can explicitly require an immediate contamination check. Resolve it separately using its stated zone or die. It does not fill or empty the periodic clock unless the hazard explicitly says so. A generic WIL save against fear, a time-loop event or loss of a turn is not automatically contamination damage.

## Resolve One Check

**1. Find effective WIL.** Effective WIL is current WIL minus the number of distinct Quirks, with a **maximum penalty of -3**. This is the standard rule, not an optional dial. With WIL 11 and four Quirks, save against 8, not 7. The penalty applies to contamination saves only, not every WIL save.

**2. Save.** Roll d20 equal to or below effective WIL. A natural 1 always succeeds; a natural 20 always fails. On success, take no damage and gain no Quirk. Never raise a negative effective WIL to create extra successful die results: only the natural 1 succeeds in that case.

**3. Apply protection, then the cap.** On failure, roll the zone's damage die. Subtract temporal protection, to a minimum of 1. Then cap that result at half the character's current WIL before this hit, rounded up. Subtract the final damage directly from WIL, bypassing HP. Armor does not reduce it.

The standard temporal suit reduces damage by 1. The heavy containment suit reduces it by 2 ($2,000, bulky). They are alternatives, not cumulative suits. Dr. Voss's Injector adds its stated reduction and duration; the minimum damage remains 1.

**4. Check WIL first.** If WIL reaches 0 from this hit, the character immediately becomes an echo. Do not resolve another check or treatment for that character as a living PC.

**5. Check the Quirk trigger.** If the character remains above WIL 0 and the final damage from this single hit is **3 or more**, gain one new distinct Quirk. Roll d12; reroll duplicates until a new result appears. Multiple hits of 1-2 damage do not add together for this trigger. A hit never grants more than one Quirk.

**6. Check the sixth Quirk.** Five distinct Quirks are survivable while WIL remains above 0. Gaining the **sixth** causes immediate, irreversible echo transformation. Four and five Quirks do not increase the save penalty beyond -3; they still bring the character closer to this limit.

## Worked Cases and Limits

**Standard suit:** Jin has WIL 13 and no Quirks. He fails an Orange check and rolls 4 on d4. The suit reduces it to 3; the cap is 7. He loses 3 WIL, falls to 10 and gains one Quirk.

**Protection before cap:** at WIL 5, a failed Black check rolls 6. The standard suit reduces it to 5, then the cap reduces it to 3. Final WIL is 2 and one Quirk is gained. Applying the cap before the suit would incorrectly produce only 2 damage.

**Low WIL:** at WIL 4, the cap is 2, so this hit cannot grant a Quirk. At WIL 1, a failed check still deals 1 damage and causes an echo. The cap limits one hit; it does not guarantee safety over repeated checks.

**Heavy suit:** against a d4 zone, its maximum net damage is 2. It prevents the normal 3-damage Quirk trigger there, but not WIL erosion or WIL-zero echoes. Black d6 exposure can still grant Quirks. This is an intentional benefit of expensive, bulky protection, not immunity to contamination.

## Recovery

Contamination-damaged WIL does not recover through ordinary HP rest or merely because a session ends. Restore WIL only when the treatment actually finishes, never beyond maximum WIL.

- **Division medical treatment:** one full week; restores d6 WIL. At Loyalty 7+, 3 days and d8 WIL.
- **Black market temporal therapy:** $500, 2 days, restores d6 WIL.
- **Anti-rejection medicine:** $250 weekly. Prevents withdrawal; it does not itself restore WIL. A missed dose makes the character Deprived. No WIL recovery while Deprived.

Treatment does not remove Quirks, and ordinary treatment never reverses an echo. Exceptional Quirk removal follows the separate procedures in Temporal Quirks. Do not award a full week of care while also treating that same week as unrestricted field work.

## Temporal Echoes

At WIL 0 from contamination or on gaining a sixth distinct Quirk, the PC becomes a hostile NPC controlled by the Warden. The transformation is permanent and irreversible. The echo retains fragmented memories of its former life. The player creates a replacement who joins at the next plausible immediate opportunity.

Before exposure, show the current WIL, Quirk count, protection and time to the next check. Players can retreat, reduce delays, arrange treatment or improve protection. Do not add hidden checks to force a mutation schedule.
