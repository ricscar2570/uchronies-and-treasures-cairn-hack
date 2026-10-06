---
layout: default
title: The Economy of Desperation
parent: Game Systems
nav_order: 1
---


## The Economy of Desperation

> The economy creates **persistent pressure, not predetermined corruption**. Honest play can produce good weeks. Zhou offers the fastest way to turn a bad month into immediate liquidity, and that speed has a price.

> **Core math.** Recruit pay is $800 against $900 mandatory expenses. A field mission adds a $50 allowance. A standard success adds $140 net after the Division's fixed 30% deduction, so a standard-success week is +$90 before unexpected costs. The unexpected-expense table averages about $133/week. Strong weeks can finish positive; they do not automatically erase Debt.

### The Three Ledgers

| Ledger | Starts At | Meaning |
|---|---:|---|
| **Cash** | $500 | Ordinary spendable dollars. Cash never goes below $0. |
| **Debt** | $500 owed | Formal amount owed. Record it as a positive amount, separate from Cash. |
| **Certificates** | 0 | Zhou-network scrip; about $1,000 purchasing power inside the black market. |

Cash does **not** automatically repay Debt. Certificates cannot directly pay rent, food, medicine, or Division Debt. Cash-out through Zhou: **1 certificate = $800 Cash** and **+1 Corruption per cash-out transaction**.

### Weekly Accounting Procedure

At the start of each new week, settle the previous week in this exact order:

1. **Income:** add base pay, previous mission pay, and side-gig income to Cash.
2. **Costs:** roll the weekly unexpected expense, then pay it plus mandatory expenses from Cash.
3. **Shortfall:** Cash stops at $0; any unpaid amount is added to Debt.
4. **Repayment / clemency:** spend remaining Cash or eligible clemency to reduce Debt.
5. **Interest:** apply **5% once** to remaining Debt; round the new Debt **up to the nearest dollar**.
6. **Pressure checks:** check Zhou thresholds, mission absence, and weekly triggers. Record closing Cash, Debt, and Certificates.

`New Debt = ceil(1.05 x max(0, Old Debt + unpaid costs - repayments - clemency))`

### Division Base Pay

| Tier | Weekly Pay | Notes |
|---|---:|---|
| **Recruit** | $800 | The pressure tier. |
| **Agent** | $1,200 | Late-campaign pressure release; old obligations remain. |
| **Veteran** | $1,800 | Financially stable by Division standards. |

### Mission Pay

Every field mission pays a **$50 allowance** plus at most **one** performance band. Bands do **not** stack. The Division deducts a fixed **30%** from gross performance pay.

| Outcome | Gross | Net | Total incl. allowance |
|---|---:|---:|---:|
| Failure / objective lost | $0 | $0 | **$50** |
| Standard success | $200 | $140 | **$190** |
| Strong success | $300 | $210 | **$260** |
| Exceptional success | $500 | $350 | **$400** |

Secondary objectives, civilian safety, speed, and recovered intelligence determine the band; they are not additive bonuses. An explicitly briefed artifact bounty of $300-$1,000 may **replace** the performance band. It never stacks.

### Mandatory Weekly Expenses

| Expense | Cost/Week | If Skipped |
|---|---:|---|
| **Rent** | $500 | Rent arrears; eviction process after 3 unpaid weeks |
| **Food & necessities** | $150 | Deprived; cannot recover HP |
| **Anti-rejection medicine** | $250 | Deprived; WIL degrades 1/week |
| **TOTAL** | **$900** | |

### Ordinary Week Before Unexpected Costs

| Week Type | Income | Fixed Costs | Cash Flow |
|---|---:|---:|---:|
| No field mission | $800 | $900 | **-$100** |
| Mission failure | $850 | $900 | **-$50** |
| Standard success | $990 | $900 | **+$90** |
| Strong success | $1,060 | $900 | **+$160** |
| Exceptional success | $1,200 | $900 | **+$300** |

Unexpected expenses average about **$133/week**. Honest play is viable; it is not reliably comfortable.

### Worked Four-Week Ledger

Assume no voluntary Debt repayments.

| Week | Cash In | Costs | Closing Cash | Debt After 5% |
|---|---:|---:|---:|---:|
| Start | - | - | $500 | $500 |
| 1: standard + $50 unexpected | $990 | $950 | $540 | **$525** |
| 2: no mission + $100 unexpected | $800 | $1,000 | $340 | **$552** |
| 3: standard + $150 unexpected | $990 | $1,050 | $280 | **$580** |
| 4: no mission + $300 unexpected | $800 | $1,200 | $0 | **$735** |

By Week 4 the agent is still clean and still has choices, but Zhou's first $700 Debt threshold is live.

### Division Clemency

Once every 4 weeks: Loyalty 5-6 reduces Debt by **$300**; Loyalty 7+ reduces it by **$400**. Requesting clemency costs **-1 Loyalty**. Clemency reduces principal before interest and never becomes Cash.

### The Black Market: Zhou's Economy

Certificates are separate scrip. Earn them from Zhou jobs, artifacts, or intelligence; spend them on black-market goods and services. Cash-out is **$800 Cash per certificate**, +1 Corruption per cash-out transaction. Other Zhou deals use the Corruption cost stated by that deal.

### What Happens When You Don't Pay

**Rent arrears (3 weeks):** eviction starts; social interactions are impaired from stress and lack of a fixed address.

**No food (2 weeks):** Deprived. After 4 weeks: -2 STR permanent.

**No medicine (1 week):** Deprived; WIL degrades 1/week. After 2 weeks: WIL save at disadvantage or gain a new Quirk.

### Side Gigs

| Side Gig | Pay | Risk | Corruption |
|---|---:|---|---|
| Security guard | $100-200/week | Low | None |
| Manual labor | $80-150/week | Low | None |
| Division consulting | $150-250/week | None | None (Loyalty 5+) |
| Temporal info market | $200-600 first sale/wk | WIL save | Exposure clock |
| Gambling | -$200 to +$400 | Medium | +1 after 3 wins |
| Street fighting | $200-500/fight | High | None |
| Drug courier | $300-600/run | High | +1 |
| Info sale to Zhou | $500-2,000 | Very high | +2 |

**Division Consulting:** available only in a week with no field mission. At the $200 midpoint, Recruit pay plus consulting reaches $1,000 before unexpected costs: a clean pressure valve, not a guaranteed escape.

**Temporal Information Market:** first sale $200-600. After each sale make a WIL save; failure costs -2 Loyalty. Additional same-week sales pay half. Exposure +1 per sale; at 6 the next buyer is a Zhou front, at 10 Zhou contacts you directly.

### Unexpected Weekly Expenses

| d6 | Expense | Cost |
|---|---|---:|
| 1 | Nothing extra | $0 |
| 2 | Phone / laundry / toiletries | $50 |
| 3 | Transport breakdown | $100 |
| 4 | Medical copay | $150 |
| 5 | Equipment replacement | $200 |
| 6 | Debt collector / bribe / emergency | $100-$500 |

### Mission Absence

1 absence: no consequence. 2 consecutive: warning. 3: -1 Loyalty. 4: disciplinary probation, another -2 Loyalty and half pay until 2 consecutive missions are completed. 5+: termination. Medical unfitness does not count.

### Zhou's Contact Thresholds

| Debt Owed | Offer |
|---:|---|
| **$700+** | $1,500 Cash courier job |
| **$1,300+** | $2,000-$3,000 Cash for Division intelligence |
| **$2,200+** | $5,000 Cash for sabotage or theft |
| **$4,000+** | Full employment; Zhou clears formal Debt for total dependence |

Refusing does not anger Zhou. She waits.

### Tier Advancement

**Recruit to Agent:** complete **8 successful missions**, spend at least **8 weeks** as a Recruit, and have **Loyalty 4+**.

**Agent to Veteran:** complete a significant narrative milestone.

Tiers affect pay and narrative standing, not combat power. Promotion is a pressure release, not a reset: Debt, Exposure, Corruption, obligations, and Quirks remain.
