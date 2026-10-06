import importlib.util
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from r1_economy import *
from economy_sim import simulate, unexpected_expense


class InterestTests(unittest.TestCase):
    def test_all_principals_to_100000(self):
        for value in range(100001):
            self.assertEqual(value + interest(value), -(-21 * value // 20))

    def test_exact_multiple_float_regression(self):
        for value in (100, 420, 620, 820, 1240, 10000):
            self.assertEqual(value + interest(value), value * 21 // 20)

    def test_small_principals(self):
        self.assertEqual([interest(n) for n in (0, 1, 19, 20, 21)], [0, 1, 1, 1, 2])

    def test_invalid_amounts(self):
        for v in (-1, 1.5, '50', None, True):
            with self.assertRaises(ValueError):
                interest(v)


class LedgerTests(unittest.TestCase):
    def test_four_week_printed_example(self):
        cash, debt = 500, 500
        inputs = [(990, 950), (800, 1000), (990, 1050), (800, 1200)]
        expected = [(540, 525), (340, 552), (280, 580), (0, 735)]
        for (income, cost), pair in zip(inputs, expected):
            r = settle_week(cash, debt, income, cost)
            cash, debt = r.cash, r.debt
            self.assertEqual((cash, debt), pair)

    def test_eight_week_campaign_example(self):
        cash, debt = 500, 500
        inputs = [(990, 950), (800, 1000), (990, 1050), (800, 1200),
                  (1060, 1000), (800, 950), (990, 1100), (1200, 950)]
        expected = [(540, 525), (340, 552), (280, 580), (0, 735),
                    (60, 772), (0, 906), (0, 1067), (250, 1121)]
        for (income, cost), pair in zip(inputs, expected):
            r = settle_week(cash, debt, income, cost)
            cash, debt = r.cash, r.debt
            self.assertEqual((cash, debt), pair)

    def test_reyes_opening(self):
        r = settle_week(110, 690, 990, 1000)
        self.assertEqual((r.cash, r.debt), (100, 725))

    def test_no_automatic_repayment(self):
        r = settle_week(500, 500, 1000, 900)
        self.assertEqual((r.cash, r.debt), (600, 525))

    def test_repayment_before_interest(self):
        r = settle_week(500, 500, 1000, 900, repayment=300)
        self.assertEqual((r.cash, r.debt, r.interest), (300, 210, 10))

    def test_clamped_repayment_and_clemency(self):
        r = settle_week(100, 150, 0, 0, repayment=999, clemency=999)
        self.assertEqual((r.cash, r.debt, r.repayment, r.clemency), (0, 0, 100, 50))

    def test_clemency_never_becomes_cash(self):
        r = settle_week(100, 50, 0, 0, clemency=300)
        self.assertEqual((r.cash, r.debt, r.clemency), (100, 0, 50))

    def test_shortfall_floor(self):
        r = settle_week(20, 500, 800, 1000)
        self.assertEqual((r.cash, r.shortfall, r.debt), (0, 180, 714))

    def test_no_interest_on_cash(self):
        self.assertEqual(settle_week(1000, 0, 0, 0).cash, 1000)
        self.assertEqual(settle_week(1000, 0, 0, 0).debt, 0)

    def test_reserve_is_optional_policy(self):
        r = settle_week(500, 500, 990, 1000, reserve=200)
        self.assertEqual((r.cash, r.debt, r.repayment), (200, 221, 290))

    def test_invalid_mixed_repayment_policy(self):
        with self.assertRaises(ValueError):
            settle_week(1, 1, 1, 1, reserve=0, repayment=1)

    def test_cash_conservation_random(self):
        rng = random.Random(42)
        for _ in range(10000):
            c, d, inc, exp, rep, clem = [rng.randrange(5000) for i in range(6)]
            r = settle_week(c, d, inc, exp, repayment=rep, clemency=clem)
            self.assertEqual(r.cash, c + inc - (exp - r.shortfall) - r.repayment)
            self.assertEqual(r.debt, d + r.shortfall - r.repayment - r.clemency + r.interest)
            self.assertGreaterEqual(r.cash, 0)
            self.assertGreaterEqual(r.debt, 0)

    def test_duplicate_receipt_rejected(self):
        book = ReceiptBook(100)
        book.credit('W4-mission', 190)
        with self.assertRaises(ValueError):
            book.credit('W4-mission', 190)
        self.assertEqual(book.cash, 290)
        r = settle_week(book.cash, 725, 800, 900)
        self.assertEqual(r.cash, 190)


class RewardTests(unittest.TestCase):
    def test_bands(self):
        self.assertEqual([mission_pay(k) for k in GROSS_BANDS], [50, 190, 260, 400])

    def test_bounty_replaces_band(self):
        self.assertEqual(mission_pay('exceptional', bounty=1000), 750)
        self.assertEqual(mission_pay('strong', bounty=300), 260)

    def test_round_net_down(self):
        self.assertEqual(mission_pay('standard', bounty=333), 283)

    def test_failure_gets_allowance_only(self):
        self.assertEqual(mission_pay('failure', bounty=1000), 50)
        self.assertEqual(mission_pay('failure', trusted_assignment=True, loyalty=7), 50)

    def test_trusted_adjustment(self):
        self.assertEqual(mission_pay('standard', trusted_assignment=True, loyalty=7), 330)
        self.assertEqual(mission_pay('standard', loyalty=7), 190)

    def test_trusted_bounty_cannot_stack(self):
        with self.assertRaises(ValueError):
            mission_pay('standard', trusted_assignment=True, loyalty=7, bounty=500)

    def test_trusted_not_automatic_hero_bonus(self):
        with self.assertRaises(ValueError):
            mission_pay('standard', trusted_assignment=True, loyalty=9)

    def test_hero_pay(self):
        self.assertEqual(salary('Recruit', 9), 1200)
        self.assertEqual(salary('Agent', 9), 1800)
        self.assertEqual(salary('Veteran', 10), 2700)
        self.assertEqual(salary('Recruit', 8), 800)

    def test_cash_out_one_transaction(self):
        self.assertEqual(cash_out(2), (1600, 1))
        self.assertEqual(cash_out(0), (0, 0))
        self.assertEqual(cash_out(1)[1] + cash_out(1)[1], 2)

    def test_clemency_cooldown(self):
        self.assertEqual(clemency_amount(5, 1), 300)
        self.assertEqual(clemency_amount(7, 4, 1), 0)
        self.assertEqual(clemency_amount(7, 5, 1), 400)
        self.assertEqual(clemency_amount(4, 5), 0)

    def test_promotion_all_requirements(self):
        self.assertTrue(can_promote(8, 8, 4))
        self.assertFalse(can_promote(8, 7, 4))
        self.assertFalse(can_promote(7, 8, 4))
        self.assertFalse(can_promote(8, 8, 3))


class ScenarioTests(unittest.TestCase):
    def test_promotion_salary_next_week(self):
        trace, *_ = simulate([('standard', 0)] * 15, 'isolated_honest')
        self.assertEqual(trace[7]['tier_paid'], 'Recruit')
        self.assertEqual(trace[8]['tier_paid'], 'Agent')

    def test_loyalty_salary_next_week(self):
        trace, *_ = simulate([('standard', 0)] * 15, 'loyalty_honest')
        self.assertEqual(trace[3]['salary'], 800)
        self.assertEqual(trace[4]['salary'], 1200)

    def test_no_success_no_promotion(self):
        trace, *_ = simulate([('failure', 0)] * 15, 'isolated_honest')
        self.assertTrue(all(r['tier_paid'] == 'Recruit' for r in trace))

    def test_offer_cannot_be_collected_twice(self):
        trace, *_ = simulate([('failure', 500)] * 15, 'isolated_first_offer')
        self.assertEqual(sum(r['offer_cash'] for r in trace), 1500)

    def test_default_expense_exact_mean(self):
        mean = sum(Fraction(v, 6) for v in (0, 50, 100, 150, 200))
        mean += sum(Fraction(v, 54) for v in range(100, 501, 50))
        self.assertEqual(mean, Fraction(400, 3))

    def test_scenario_reproducibility(self):
        draws = [('standard', 150), ('failure', 500), ('strong', 50)] * 5
        self.assertEqual(simulate(draws, 'loyalty_trusted_clemency_honest'),
                         simulate(draws, 'loyalty_trusted_clemency_honest'))


if __name__ == '__main__':
    unittest.main()
