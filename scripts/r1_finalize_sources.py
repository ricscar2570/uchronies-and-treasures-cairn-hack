#!/usr/bin/env python3
"""Idempotent, fail-closed text migration from the 32dd003 R1 checkpoint.

Edits only explicitly named R1 passages. Does not migrate the Omnibus branch.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f'{path}: expected exactly one occurrence of {old[:60]!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


def migrate():
    econ = 'game-systems/economy.md'
    replace(econ,
        '1. **Income:** add base pay, previous mission pay, and side-gig income to Cash.',
        '1. **Income:** add only **unposted** base pay, mission pay, and side-gig receipts to Cash. Give each receipt a week/job label; income already recorded on receipt is already in opening Cash and is not added again.')
    replace(econ,
        '3. **Shortfall:** Cash stops at $0; any unpaid amount is added to Debt.',
        '3. **Shortfall:** Cash stops at $0; add unpaid **incurred obligations** to Debt and name the creditor. Record whether credit actually supplied the goods. Recording Debt does not produce food, medicine, or equipment that nobody delivered. If a purchase is refused, do not also charge for it; apply the stated consequences of going without. Credit availability must be stated before commitment.')
    replace(econ,
        '`New Debt = ceil(1.05 x max(0, Old Debt + unpaid costs - repayments - clemency))`',
        '`Principal = max(0, Old Debt + unpaid costs - repayments - clemency)`\n\n`New Debt = Principal + ceil(Principal / 20)`\n\nUse whole dollars and round only once at this step. Repayment cannot exceed available Cash or Debt. Clemency cannot exceed the remaining principal and never produces Cash. Starting Debt belongs to the individual agent and is held by Division Finance. Transfers and joint obligations must be explicitly recorded.')
    replace(econ,
        'Secondary objectives, civilian safety, speed, and recovered intelligence determine the band; they are not additive bonuses. An explicitly briefed artifact bounty of $300-$1,000 may **replace** the performance band. It never stacks.',
        'Secondary objectives, civilian safety, speed, and recovered intelligence determine the band; they are not additive bonuses. An explicitly briefed artifact bounty of $300-$1,000 may **replace** the performance band. It never stacks. All listed payouts are **per participating agent**, unless a briefing explicitly identifies a shared team reward. If a gross award is not a multiple of $10, round its 70% net payout down to whole dollars; the allowance is not deducted. Failure pays only the $50 allowance, not an unearned bounty.\n\n### Loyalty Benefits and Briefed Budgets\n\nSalary and financial access use the agent\'s Loyalty at the **start of the week**. Loyalty 9-10 retains the existing **+50% base-pay benefit**: Recruit $1,200, Agent $1,800, Veteran $2,700. It does not multiply mission awards, side income, or certificates. Benefits apply only while their access requirements are met, including the existing Instability benefit lock.\n\nAt Loyalty 7-8, the existing **better missions (+$200)** benefit means access to a specifically briefed assignment with a $200 **gross** increase included in its one successful performance award. It is not a guaranteed extra payment on every job. A standard success on such an assignment pays $50 + 70% of $400 = **$330**. Declare the assignment before departure. Do not add this adjustment to a replacement artifact bounty, or carry it into the Hero band as an additional automatic entitlement.\n\nExtra budget obtained from an NPC is either a documented expense reimbursement/advance or a stated gross mission-award adjustment; say which before use. Restricted operating funds are not personal earnings. Do not invent another overlapping bonus after the mission.\n\nThese benefits are genuine routes out of financial pressure. The ordinary-week table below uses unmodified Recruit base pay; it is **not** the cash flow of a Division Hero.')
    replace(econ,
        'Once every 4 weeks: Loyalty 5-6 reduces Debt by **$300**; Loyalty 7+ reduces it by **$400**. Requesting clemency costs **-1 Loyalty**. Clemency reduces principal before interest and never becomes Cash.',
        'Once every 4 weeks: Loyalty 5-6 reduces Debt by **$300**; Loyalty 7+ reduces it by **$400**. Use Loyalty immediately before the request; then pay **-1 Loyalty**, even if the remaining Debt uses only part of the allowance. The first request may be made in any eligible week; after using it in Week N, the next request is available in Week N+4. Record the last-used week. Clemency reduces principal before interest and never becomes Cash.')
    replace(econ,
        '| 6 | Debt collector / bribe / emergency | $100-$500 |',
        '| 6 | Debt collector / bribe / emergency | $100-$500 |\n\nOn a 6, use an amount already established in play. Otherwise roll d10, **reroll 10**, and pay $50 plus $50 times the result: 1 means $100, 9 means $500. This makes the nine amounts equally likely. The quoted mean of $133.33 applies only to this default random table, not to a campaign with fixed emergency costs.')
    replace(econ,
        'Tiers affect pay and narrative standing, not combat power. Promotion is a pressure release, not a reset: Debt, Exposure, Corruption, obligations, and Quirks remain.',
        'Check all promotion requirements at weekly close; new tier pay starts the **following week**, not retroactively. Tiers affect pay and narrative standing, not combat power. Promotion is a pressure release, not a reset: Debt, Exposure, Corruption, obligations, and Quirks remain.')

    loyalty = 'game-systems/loyalty-corruption.md'
    replace(loyalty,
        '| 7-8 | Trusted | Better missions (+$200). Priority Division medics (3 days instead of 1 week). |',
        '| 7-8 | Trusted | Access to a briefed higher-paid assignment (+$200 gross in its single successful award; see Economy). Priority Division medics (3 days instead of 1 week). |')
    replace(loyalty,
        '| 9-10 | Division Hero | Pay +50%. Military-grade equipment free. |',
        '| 9-10 | Division Hero | Base salary +50% from the next weekly opening; not mission pay. Military-grade equipment free. Benefits remain subject to the Instability lock. |')

    cheat = 'reference/warden-cheat-sheet.md'
    replace(cheat, '*All mechanical triggers in chronological session order. One page, behind the screen.*',
        '*Mechanical triggers in chronological session order. This is a reference, not a claim of complete cross-system validation.*')
    replace(cheat, '**Mission bonus:** $150 base (net) + variable bonuses subject to deductions',
        '**Mission pay:** $50 allowance + one non-cumulative net award: failure $50 total; standard $190; strong $260; exceptional $400. Briefed bounties replace the award. Record paid receipts now and do not add them again at settlement.\n\n**Loyalty money:** Hero 9-10: +50% base salary, subject to benefit lock. Trusted 7-8: only a briefed assignment gets +$200 gross inside its successful award. Do not stack with a replacement bounty.')
    replace(cheat, '| Zhou first offer | debt $500+ |', '| Zhou first offer | Debt $700+; an offer, never compulsory acceptance |')
    replace(cheat, '- **PC death:** New PC starts at Recruit tier. Inherits team\'s shared debt',
        '- **PC death:** New PC starts at Recruit tier with $500 Cash and $500 personal Debt. A joint obligation transfers only if that liability was explicitly recorded and the new character accepts it; there is no automatic inheritance of another PC\'s personal Debt.')

    replace('players-guide/example-of-play.md',
        'The $190 goes into Cash now. Reyes goes from $100 to $290 Cash; Marco from $180 to $370. Debt does not fall automatically.',
        'The $190 goes into Cash now. Mark this Week 4 mission receipt as PAID: it must not be added again next Monday. Reyes goes from $100 to $290 Cash; Marco from $180 to $370. Debt does not fall automatically.')
    replace('players-guide/example-of-play.md',
        'Field allowance is $50. Recover the chip and this is a standard success:',
        'This is an ordinary assignment, not a Trusted higher-paid mission. Field allowance is $50. Recover the chip and this is a standard success:')

    campaign = 'adventures/the-first-four-weeks.md'
    replace(campaign,
        'The new PC inherits the team\'s shared debt and starts at Recruit tier.',
        'The new PC starts at Recruit tier with $500 Cash and $500 personal Debt. Another PC\'s personal Debt is not automatically inherited; any explicitly recorded joint obligation requires an agreed new debtor.')
    replace(campaign,
        'If they succeed, the month breaks even.',
        'Success adds $400 mission income per agent. Whether the month breaks even depends on the actual ledger; Hayes cannot promise a result the numbers do not support.')
    replace(campaign,
        'For a PC who refuses Zhou and makes **no voluntary Debt repayments**:',
        'This isolated arithmetic example uses ordinary base salary, no Trusted assignments, no Hero salary modifier, no voluntary repayments and no clemency. It is not a trajectory for a successful agent whose Loyalty rises. Apply actual benefits at the table:')
    replace('wardens-guide/running-the-game.md',
        'New PC starts at Recruit tier. Inherits the team\'s shared debt proportion.',
        'New PC starts at Recruit tier with $500 Cash and $500 personal Debt. No other PC\'s personal Debt transfers automatically. Any expressly shared obligation needs an agreed new debtor.')
    replace('players-guide/overview-and-principles.md',
        '**Time Pressure.** Every week in game time costs money. Every mission costs time. Every delay increases the debt. Don\'t let the pace slacken.',
        '**Time Pressure.** Every week in game time incurs costs and every mission takes time. A delay can increase Debt when income and reserves do not cover obligations; do not add Debt merely because time passed. Use the ledger.')
    replace('players-guide/overview-and-principles.md',
        'you stay loyal but poor. Base pay, plus one loyalty point.',
        'you stay loyal and receive the briefed mission payout, plus one loyalty point. Your actual finances follow the ledger.')
    replace('wardens-guide/faq.md',
        'A PC who stays loyal and refuses Zhou will have more debt, more stress, and fewer resources.',
        'A PC who stays loyal and refuses Zhou may take longer to resolve a shortfall; that is not a guarantee of greater Debt. High Loyalty benefits, clemency and legal work can create stability.')
    replace('README.md',
        'Balance validated through Monte Carlo simulation; the method and the before/after numbers are documented openly in the',
        'The R1 economy has a reproducible, assumption-bound ledger simulation, not full-game or human-playtest validation; the method and limits are documented in the')
    replace('wardens-guide/design-notes.md',
        '## The Monte Carlo Validation',
        '## Simulation Scope\n\nR1B compares an isolated ledger with explicit Loyalty-benefit and clemency policies. It does not forecast player choices or validate the complete game. Historical figures in the next paragraph are reported legacy results: the original full-campaign simulator has not been recovered or rerun for this checkpoint.\n\n### Reported Historical Simulation')

    builder = ROOT / 'scripts/build-pdf.py'
    s = builder.read_text(encoding='utf-8')
    if '# R1B canonical chapter bridge' not in s:
        start = s.index('    s += [nfull(), pb(), h1("The Economy of Desperation")')
        end = s.index('    # ═', start)
        s = s[:start] + '''    # R1B canonical chapter bridge: no duplicate economic manuscript.
    from r1_pdf_sources import render_chapter
    s += [nfull(), pb()]
    s += render_chapter('game-systems/economy.md', globals())
    s += [npb(), pb()]

''' + s[end:]
        # Replace chapter groups already on full-width pages, preserving following templates.
        groups = [
            ('    s += [h1("Design Notes"),', '    # ═',
             ['wardens-guide/design-notes.md', 'wardens-guide/faq.md', 'reference/r1-economy-validation.md']),
            ('    s += [h1("The First Four Weeks"),', '    # ═', ['adventures/the-first-four-weeks.md']),
        ]
        for begin, finish, files in groups:
            a = s.index(begin)
            z = s.index(finish, a)
            block = '    s += [nfull(), pb()]\n'
            for i, path in enumerate(files):
                block += f"    s += render_chapter({path!r}, globals())\n"
                block += '    s += [pb()]\n'
            s = s[:a] + block + '\n' + s[z:]
        # Other chapters retain their established text/layout; update only R1 passages.
        for old, new in [
            ("(loyal, poor, +1 Loyalty)", "(briefed payout, +1 Loyalty)"),
            ("Track money carefully. The deficit is the game's heartbeat. If players are not worried about rent, something has gone wrong.",
             "Track Cash, Debt and Certificates separately. Financial stability earned through the rules is a valid outcome, not a mistake to punish."),
            ("Every week costs money. Every delay increases the debt. Do not let the pace slacken.",
             "Every week incurs costs. A delay increases Debt only when the actual ledger leaves obligations unpaid."),
            ("Know your weekly deficit.", "Know your Cash, your Debt, and the next weekly close."),
            ("Add unpaid costs to Debt; Cash cannot go below $0",
             "Add unpaid incurred obligations to Debt, naming the creditor. Cash cannot go below $0; Debt alone does not supply missing goods"),
            ('Better missions (+$200). Priority medics (3 days instead of 1 week).',
             'Briefed Trusted assignment: +$200 gross inside one successful award (not with a replacement bounty). Priority medics: 3 days.'),
            ('Pay +50%. Military-grade equipment free.',
             'Base salary +50% at next weekly opening, subject to Instability lock. Military-grade equipment free.'),
            ("The new PC inherits the team's shared debt proportionally.",
             'New PC: $500 Cash and $500 personal Debt. No automatic inheritance of another PC\'s Debt; agree any explicit joint obligation.'),
            ('Debt is massive but Hayes promotes them.',
             'Debt follows the actual ledger; Hayes may promote eligible agents. Honest financial stability is a valid outcome.'),
            ('Add base pay, previous mission pay, and side-gig income to Cash',
             'Add only UNPOSTED base pay, mission pay, and side-gig receipts to Cash; never count a paid receipt twice'),
            ('-$50-100/week at Recruit',
             '-$100 base-pay gap before mission income; outcomes vary'),
        ]:
            if old not in s:
                raise RuntimeError(f'PDF expected passage missing: {old}')
            s = s.replace(old, new)
        # Embedded example wording differs from Markdown: inject a non-duplicable receipt note.
        anchor = '    s += [h1("Example of Play"), rule(),'
        if anchor not in s:
            raise RuntimeError('PDF example anchor missing')
        s = s.replace(anchor, anchor + '\n    fullnote("Accounting note: mission income credited during play is a PAID receipt, already included in opening Cash. Do not add it again at weekly settlement. The ordinary assignment here has no Trusted gross adjustment."),')
        # Add the corrected table aid and ledger worksheet before the existing reference chapter.
        anchor = '    s += [h1("Reference"), rule(),'
        s = s.replace(anchor,
            "    s += render_chapter('reference/weekly-settlement-r1.md', globals())\n    s += [pb()]\n" + anchor)
        s = s.replace('CHRONOCAIRN: Complete KDP Manual',
                      'CHRONOCAIRN: R1B Economy Review Manual (not printer-certified)')
        # Layout repairs found by the first real render, not game-rule changes.
        s = s.replace('pdfmetrics.registerFont(TTFont("Ser",',
            'pdfmetrics.registerFont(TTFont("Helvetica", BASE+"LiberationSans-Regular.ttf"))\n'
            'pdfmetrics.registerFont(TTFont("Ser",', 1)
        s = s.replace('    base = FW if full else CW\n',
            '    base = FW if full else CW\n'
            '    widths = [w * (base - 12) / sum(widths) for w in widths]\n', 1)
        for title in ('Tables & Generators', 'Campaign Management'):
            s = s.replace(f'    s += [h1("{title}"),',
                          f'    s += [nfull(), pb(), h1("{title}"),')
        # Multiple chapter-end page breaks must not manufacture empty pages.
        s = s.replace('    return s\n',
            "    from r1_pdf_sources import normalize_breaks\n    return normalize_breaks(s)\n", 1)
        # Keep an actual navigable chapter outline after merging the cover.
        s = s.replace('        self._chapter = ""',
                      '        self._chapter = ""\n        self._r1_headings = {}', 1)
        s = s.replace('                self._chapter = txt',
                      '                self._chapter = txt\n                self._r1_headings[txt] = self.page', 1)
        s = s.replace('    final = str(here / "CHRONOCAIRN_Final_Complete.pdf")',
            '    for title, page in doc._r1_headings.items():\n'
            '        writer.add_outline_item(title, page - 1)\n'
            '    final = str(here / "CHRONOCAIRN_Final_Complete.pdf")', 1)
        builder.write_text(s, encoding='utf-8')
    print('R1B source migration applied; Omnibus remains a separate, unmigrated edition.')


if __name__ == '__main__':
    migrate()
