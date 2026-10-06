import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class R1SourceTests(unittest.TestCase):
    def test_economy_has_single_default_expense_instruction(self):
        text = (ROOT/'game-systems/economy.md').read_text()
        self.assertEqual(text.count('On a 6, use an amount already established in play.'), 1)

    def test_receipt_and_credit_clarifications(self):
        text = (ROOT/'game-systems/economy.md').read_text()
        for token in ('**unposted**', '**incurred obligations**', 'name the creditor', 'Loyalty 9-10'):
            self.assertIn(token, text)

    def test_warden_reference_removes_old_pay_and_threshold(self):
        text = (ROOT/'reference/warden-cheat-sheet.md').read_text()
        self.assertNotIn('$150 base (net)', text)
        self.assertNotIn('debt $500+', text)
        self.assertIn('Debt $700+', text)

    def test_example_income_is_marked_paid(self):
        self.assertIn('must not be added again next Monday',
                      (ROOT/'players-guide/example-of-play.md').read_text())

    def test_builder_reads_canonical_economy(self):
        text = (ROOT/'scripts/build-pdf.py').read_text()
        self.assertIn("render_chapter('game-systems/economy.md'", text)
        self.assertNotIn('Why the Economy Is Unsustainable', text)
        self.assertNotIn('Every delay increases the debt.', text)

    def test_campaign_is_not_a_guaranteed_financial_result(self):
        text = (ROOT/'adventures/the-first-four-weeks.md').read_text()
        self.assertIn('isolated arithmetic example', text)
        self.assertNotIn('If they succeed, the month breaks even.', text)
        self.assertIn('no Hero salary modifier', text)

    def test_five_report_policies_have_same_input_seed(self):
        payload = json.loads((ROOT/'reports/r1b/economy_results.json').read_text())
        self.assertEqual(payload['seed'], 42026)
        self.assertEqual(payload['trials_per_scenario'], 100000)
        self.assertEqual(len(payload['results']), 5)
        a,b = payload['results'][:2]
        self.assertEqual(a['ever_debt_700'], b['ever_debt_700'])
        self.assertLess(a['agent_paid_week_15'], a['eligible_for_agent_after_week_15'])

    def test_full_game_claim_not_present(self):
        self.assertNotIn('Balance validated through Monte Carlo simulation',
                         (ROOT/'README.md').read_text())
        self.assertIn('not a forecast of player behaviour',
                      (ROOT/'reference/r1-economy-validation.md').read_text())


if __name__ == '__main__':
    unittest.main()
