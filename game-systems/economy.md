---
layout: default
title: The Economy of Desperation
parent: Game Systems
nav_order: 1
---


## The Economy of Desperation

> The economic system is designed to be **unsustainable**. This is not a bug. It is the beating heart of the game. The Division pays you *just enough* to survive. But life costs more. And when you're desperate, Zhou is waiting.

### Division Base Pay

  -----------------------------------------------------------------------
  Tier              Weekly Pay      Notes
  ----------------- --------------- -------------------------------------
  **Recruit**       $800/week       The bare minimum. You start here.
  **Agent**         $1,200/week     Confirmed agent. Slightly better.
  **Veteran**       $1,800/week     Finally breathing. But debts remain.
  -----------------------------------------------------------------------

**Mission bonuses:** Guaranteed base: +$150 per completed mission (not subject to deductions). Successful completion: +$200 (subject to deductions). Secondary objective: +$100 each (subject to deductions). No civilian casualties: +$150 (subject to deductions). Artifact recovery: +$300-$1,000 (varies, subject to deductions).

> Bonuses (except the guaranteed $150) are subject to "administrative deductions." A $500 bonus becomes $350 after deductions. This fuels resentment toward the Division.

### Mandatory Weekly Expenses

  -----------------------------------------------------------------------
  Expense                    Cost/Week   What happens if you skip
  -------------------------- ----------- --------------------------------
  **Rent**                   $500        Eviction in 4 weeks
  **Food & necessities**     $150        Deprived, can't recover HP
  **Anti-rejection medicine** $250       Deprived, WIL degrades 1/week
  **TOTAL**                  **$900**
  -----------------------------------------------------------------------

**Guaranteed deficit at Recruit tier: -$100 per week.**

### Weekly Cash Flow by Tier

  -----------------------------------------------------------------------
  Tier       Pay     Expenses  Balance     After 10 weeks
  ---------- ------- --------- ----------- ----------------------------
  Recruit    $800    $900      **-$100**   -$1,000 (desperate)
  Agent      $1,200  $900      **+$300**   Paying off Recruit debts
  Veteran    $1,800  $900      **+$900**   Comfortable (damage is done)
  -----------------------------------------------------------------------

> At Agent and Veteran tiers, expenses may rise to $1,100-$1,300 due to lifestyle inflation, Quirk-related medical costs, and Zhou's "voluntary" payments for past favors.

### The Black Market (Zhou's Economy)

Madame Zhou's currency is **certificates** (1 certificate = approximately $1,000).

**Earning:** Sell artifacts to Zhou (1-15 certs), sell Division intel (2-10 certs), complete side jobs (1-5 certs).

**Spending:** Ballistic vest 2 Armor (2 certs), heavy containment suit for contamination (3 certs), assault weapons (1-3 certs), fake IDs (1 cert), temporal surgery to remove a Quirk (50 certs), safe house 1 month (3 certs), bribes (1-3 certs).

**Every transaction with Zhou costs +1 or +2 Corruption.**

### The Debt Trap

**Starting debt: -$500.** Grows by $100/week at Recruit tier. **Interest: 5% per week on negative balance** (at -$500, that's $25/week; at -$1,000, it's $50/week). The debt accelerates. Monthly clemency of $300 available on request, but costs -1 Loyalty.

> **4-week example:**
>
> **Week 1:** Pay $800, expenses $900, bonus $150. Balance: +$50. Debt: -$450.
> **Week 2:** Yellow Zone mission. Bonus $150 + $200 (after deductions: $140). Balance: +$190. Debt: -$260.
> **Week 3:** Mission fails. Only guaranteed $150. Broken phone: -$50. Balance: $0. Debt: -$260.
> **Week 4:** Zhou offers $2,000 for "a small piece of information." Rent is due. Medicine runs out in 3 days. What do you do?

### What Happens When You Don't Pay

**Rent arrears (3 weeks):** Eviction starts. Social interactions are **impaired** (stress, no fixed address). Sleep in Division barracks (if Loyalty 6+) or Zhou's safe house (+1 Corruption).

**No food (2 weeks):** Deprived. After 4 weeks: -2 STR permanent.

**No medicine (1 week):** Deprived. WIL degrades 1/week. After 2 weeks: WIL save at disadvantage or gain new Quirk.

### Side Gigs

  -----------------------------------------------------------------------
  Side Gig              Pay               Risk           Corruption
  --------------------- ----------------- -------------- --------------------
  Security guard        $100-200/week     Low            None
  Manual labor          $80-150/week      Low            None
  Division consulting   $300-400/week     None           None (Loyalty 5+)
  Temporal info market  $200-600/info     WIL save       None (direct)
  Gambling              -$200 to +$400    Medium         +1 after 3 wins
  Street fighting       $200-500/fight    High (d6 STR)  None
  Drug courier          $300-600/run      High           +1 Corruption
  Info sale to Zhou     $500-2,000        Very high      +2 Corruption
  -----------------------------------------------------------------------

**Division Consulting (Loyalty 5+ only).** The agent uses their background expertise as a consultant for other Division teams. Pay: $300-400 per week. Cost: 2 full days of downtime. During those 2 days, no other side gigs, missions, or significant actions are possible. This is work: it requires presence and focus. Not available to agents under active surveillance. Requires Loyalty 5 or higher to access; if Loyalty drops below 5 while consulting, the contract is suspended without pay for that week.

> **Design note.** Division Consulting is intentionally narrow. At Recruit tier it does not eliminate the deficit (base $800 + $350 consulting - $900 expenses = $250 surplus). It makes the honest path survivable, not comfortable. It costs time that cannot be spent on missions or other income. The choice between consulting and a Raines mission is a real choice.

**Temporal Information Market.** Researchers, archivists, and journalists pay for information about temporal zones: anomaly locations, echo behavior, relic descriptions, zone boundary shifts. Pay: $200-600 per piece of information sold, depending on quality and exclusivity.

*Mechanic:* After each sale, make a **WIL save**. On a failure, the information reaches the Division through a third party. Result: **-2 Loyalty** (the Division does not appreciate agents monetizing operational intelligence). On a success, the sale goes undetected. There is no Corruption cost, but there is no safety either. Every sale is a roll.

> Agents with high WIL can exploit this consistently. Agents with degraded WIL (from contamination) find it increasingly dangerous. The two systems interact.

**Gambling (modified).** The pay range has been reduced from the original -$500/+$1,000 to **-$200/+$400**. The original range made gambling a high-variance lottery rather than a real economic decision.

*Addiction rule:* Three consecutive weeks of gambling wins trigger **+1 Corruption** (compulsive behavior, visible to NPCs who know the agent). The Corruption is not from Zhou or the black market; it reflects the agent's deteriorating self-control, which is visible and has social consequences.

### Unexpected Weekly Expenses

Each week, the Warden rolls **d6** for unexpected costs:

| d6 | Expense | Cost |
|----|---------|------|
| 1 | Nothing extra this week | $0 |
| 2 | Phone broken / laundry / toiletries | $50 |
| 3 | Transport breakdown (car repair, taxi) | $100 |
| 4 | Medical copay (non-Division injury) | $150 |
| 5 | Equipment replacement (lost/damaged) | $200 |
| 6 | Warden's choice (debt collector, bribe, emergency) | $100-$500 |

### Mission Absence

The Division is a government agency in permanent crisis. An agent who refuses missions repeatedly is dead weight.

- **1 absence:** No consequence. The Division is understanding. Once.
- **2 consecutive:** Captain Rodriguez has an informal chat. Narrative warning.
- **3 consecutive:** Formal reprimand. -1 Loyalty. Hayes: "The next mission is not optional."
- **4 consecutive:** Disciplinary probation. -2 Loyalty (cumulative). Pay halved until 2 consecutive missions completed.
- **5+ consecutive:** Terminated. The PC loses pay, housing, and Division protection. Alone in Vegas with Quirks and no medicine.

Participating in a mission (even a failed one) resets the counter. Being medically unfit doesn't count as absence.

### Zhou's Contact Thresholds

Zhou doesn't approach randomly. She watches, calculates, then strikes when the math is right.

| PC's Total Debt | Zhou's Offer |
|-----------------|-------------|
| -$700+ | First contact: $1,500 for a simple courier job |
| -$1,300+ | Second offer: $2,000-3,000 for intel on Division operations |
| -$2,200+ | Third offer: $5,000 for sabotage or theft |
| -$4,000+ | Final offer: Full employment with Zhou. All debts cleared. Freedom from the Division. Total corruption. |

Each offer includes +1 to +3 Corruption. Refusing doesn't anger Zhou. She waits. The debt does the persuading.

### Tier Advancement

**Recruit to Agent:** Complete 5 missions successfully AND Loyalty 4+. Hayes promotes you.

**Agent to Veteran:** Complete a significant narrative milestone (Warden decides). Examples: survive a Black Zone, expose a mole, recover a critical artifact.

> Tiers only affect pay and narrative standing. Your character doesn't get mechanically stronger. They get financially stable, which in this game is the same thing.
