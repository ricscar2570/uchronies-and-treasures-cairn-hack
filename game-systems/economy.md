---
layout: default
title: The Economy of Desperation
parent: Game Systems
nav_order: 1
---


## The Economy of Desperation

> The economic system is designed to be **unsustainable**. This is not a bug. It is the beating heart of the game. The Division pays you *just enough* to survive. But life costs more. And when you're desperate, Zhou is waiting.

> **The Core Math (the one number to remember).** At Recruit tier, a week with **no mission** loses you **$100** (pay $800 minus mandatory expenses $900). That is the floor. **Completing a mission** adds the guaranteed +$50, narrowing the worst case to **-$50/week**. The +$50 is not automatic: it requires actually running a mission, success or failure. Success and objective bonuses can lift a strong week into the black, but they are variable, shaved by "administrative deductions," and never compound into a structural surplus at Recruit tier. You start **-$500** in debt, and that balance accrues **5% interest per week**. The honest path keeps you breathing. It does not get you out.

### Division Base Pay

| Tier | Weekly Pay | Notes |
|---|---|---|
| **Recruit** | $800/week | The bare minimum. You start here. |
| **Agent** | $1,200/week | Confirmed agent. Slightly better. |
| **Veteran** | $1,800/week | Finally breathing. But debts remain. |


**Mission bonuses:** Guaranteed base: +$50 per completed mission (not subject to deductions). Successful completion: +$200 (subject to deductions). Secondary objective: +$100 each (subject to deductions). No civilian casualties: +$150 (subject to deductions). Artifact recovery: +$300-$1,000 (varies, subject to deductions).

> Bonuses (except the guaranteed $50) are subject to "administrative deductions." A $500 bonus becomes $350 after deductions. This fuels resentment toward the Division.

### Mandatory Weekly Expenses

| Expense | Cost/Week | What happens if you skip |
|---|---|---|
| **Rent** | $500 | Eviction in 4 weeks |
| **Food & necessities** | $150 | Deprived, can't recover HP |
| **Anti-rejection medicine* | $250 | Deprived, WIL degrades 1/week |
| **TOTAL** | **$900** |  |


**Deficit at Recruit tier:** with **no mission**, you lose **-$100/week** (pay $800 - expenses $900). This is the floor. **Run a mission** and the guaranteed +$50 narrows it to **-$50/week**. The guaranteed bonus is not automatic: it requires undertaking a mission (even a failed one). Skip missions and you sit at the full -$100 floor.

### Weekly Cash Flow by Tier

| Tier | Pay | Expenses | Balance | After 10 weeks |
|---|---|---|---|---|
| Recruit | $800 | $900 | **-$100** | -$1,000 from deficits alone; past -$1,500 with starting debt and interest |
| Agent | $1,200 | $900 | **+$300** | Paying off Recruit debts |
| Veteran | $1,800 | $900 | **+$900** | Comfortable (damage is done) |


> The Recruit row shows the **no-mission floor** (-$100/week). Running a mission each week improves it to -$50; the occasional successful mission can push a single week positive. Even so, with the -$500 starting debt and 5%/week interest, ten weeks at Recruit tier leaves you well past **-$1,500** owed. The deficit is structural, not bad luck.


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
> **Week 1:** Pay $800, expenses $900, bonus $50. Balance: -$50. Debt: -$550.
> **Week 2:** Yellow Zone mission. Bonus $50 + $200 (after deductions: $140). Balance: +$90. Debt: -$460.
> **Week 3:** Mission fails. Only guaranteed $50. Broken phone: -$50. Balance: -$100. Debt: -$560.
> **Week 4:** Zhou offers $2,000 for "a small piece of information." Rent is due. Medicine runs out in 3 days. What do you do?

### What Happens When You Don't Pay

**Rent arrears (3 weeks):** Eviction starts. Social interactions are **impaired** (stress, no fixed address). Sleep in Division barracks (if Loyalty 6+) or Zhou's safe house (+1 Corruption).

**No food (2 weeks):** Deprived. After 4 weeks: -2 STR permanent.

**No medicine (1 week):** Deprived. WIL degrades 1/week. After 2 weeks: WIL save at disadvantage or gain new Quirk.

### Side Gigs

| Side Gig | Pay | Risk | Corruption |
|---|---|---|---|
| Security guard | $100-200/week | Low | None |
| Manual labor | $80-150/week | Low | None |
| Division consulting | $150-250/week | None | None (Loyalty 5+) |
| Temporal info market | $200-600 first sale/wk | WIL save | None direct (Exposure clock) |
| Gambling | -$200 to +$400 | Medium | +1 after 3 wins |
| Street fighting | $200-500/fight | High (d6 STR) | None |
| Drug courier | $300-600/run | High | +1 Corruption |
| Info sale to Zhou | $500-2,000 | Very high | +2 Corruption |


**Division Consulting (Loyalty 5+ only).** The agent uses their background expertise as a consultant for other Division teams. Pay: $150-250 per week. Cost: 2 full days of downtime. During those 2 days, no other side gigs, missions, or significant actions are possible. This is work: it requires presence and focus. Not available to agents under active surveillance. Requires Loyalty 5 or higher to access; if Loyalty drops below 5 while consulting, the contract is suspended without pay for that week.

> **Design note (the honest ceiling).** Division Consulting is intentionally narrow. A consulting week at Recruit tier reaches break-even at best: base $800 + $200 consulting (mid-range) - $900 expenses = +$100 *before* the 5% interest on your existing debt and the weekly unexpected-cost roll (which averages over $100). Net those in and even your best honest week trends to zero or slightly negative. Consulting also burns the two days you would have spent on a mission, so you forgo that income too. The honest path is survivable, never comfortable, and it never produces the structural surplus needed to clear the debt. The choice between consulting and a Raines mission is a real choice.

**Temporal Information Market.** Researchers, archivists, and journalists pay for information about temporal zones: anomaly locations, echo behavior, relic descriptions, zone boundary shifts. Pay: $200-600 for the first piece of information sold in a week, depending on quality and exclusivity.

*Mechanic:* After each sale, make a **WIL save**. On a failure, the information reaches the Division through a third party. Result: **-2 Loyalty** (the Division does not appreciate agents monetizing operational intelligence). On a success, the sale goes undetected. There is no direct Corruption cost, but there is no safety either. Every sale is a roll.

*Saturation:* The market is small. Each **additional** sale in the same week pays half the previous one (round down to the nearest $50): first $200-600, second roughly half, third half again. You cannot flood the buyers indefinitely; the price collapses.

*Exposure clock:* Keep a running **Exposure** tally, +1 for every info sale you ever make (it does not reset between weeks). The buyers are a thin community, and most of it is Zhou-adjacent. When Exposure reaches **6**, the next buyer is one of Zhou's fronts: the sale pays as normal but costs **+1 Corruption** and Zhou now has a name and a pattern. At **10**, Zhou makes contact directly, regardless of your debt. The clean income was never as clean as it looked. It was a slow on-ramp.

> High WIL lets you sell more safely, but it does not stop Exposure from climbing or the per-week price from collapsing. The honest information trade keeps you alive for a while. It does not keep you clean forever, and it does not get you ahead.

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
