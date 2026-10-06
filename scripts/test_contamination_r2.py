"""Deterministic regression checks. These are not human playtests."""
from fractions import Fraction
from pathlib import Path
import json
import random
import unittest
from contamination_rules import (RULES, ExposureClock, effective_wil, net_damage,
                                 recover, resolve_check, save_succeeds)
from contamination_sim import PROFILES, simulate

class ScriptedDice:
    def __init__(self, *rolls):
        self.rolls = iter(rolls)
    def randint(self, a, b):
        result = next(self.rolls)
        if not a <= result <= b:
            raise AssertionError('Scripted roll outside die range')
        return result
    def choice(self, values):
        return values[0]

class ResolutionTests(unittest.TestCase):
    def test_penalty_cap_at_three(self):
        self.assertEqual([effective_wil(11, q) for q in range(6)], [11,10,9,8,8,8])
    def test_natural_one_and_twenty(self):
        self.assertTrue(save_succeeds(1, -2))
        self.assertFalse(save_succeeds(2, -2))
        self.assertFalse(save_succeeds(20, 50))
    def test_saved_check_consumes_no_damage_roll(self):
        o = resolve_check(12, frozenset(), 4, ScriptedDice(12))
        self.assertEqual((o.wil, o.damage, o.gained, o.echo_cause), (12,0,None,None))
    def test_single_hit_trigger(self):
        o = resolve_check(13, frozenset(), 4, ScriptedDice(20,4))
        self.assertEqual((o.wil,o.damage,len(o.quirks)), (10,3,1))
    def test_protection_before_cap(self):
        self.assertEqual(net_damage(5,6,1), 3)
        o = resolve_check(5, frozenset(), 6, ScriptedDice(20,6))
        self.assertEqual((o.wil,o.damage,len(o.quirks)), (2,3,1))
    def test_small_hits_do_not_combine(self):
        one = resolve_check(13, frozenset(), 4, ScriptedDice(20,3))
        two = resolve_check(one.wil, one.quirks, 4, ScriptedDice(20,3))
        self.assertEqual((two.wil, len(two.quirks)), (9,0))
    def test_low_wil_blocks_quirk_not_echo(self):
        for wil in range(1,5):
            self.assertLess(net_damage(wil,6), 3)
        o = resolve_check(1,frozenset(),4,ScriptedDice(20,4))
        self.assertEqual((o.wil,o.gained,o.echo_cause), (0,None,'wil_zero'))
    def test_fifth_is_survivable(self):
        o = resolve_check(13,frozenset(range(1,5)),4,ScriptedDice(20,4))
        self.assertEqual(len(o.quirks),5)
        self.assertIsNone(o.echo_cause)
    def test_sixth_is_echo_and_distinct(self):
        o = resolve_check(13,frozenset(range(1,6)),4,ScriptedDice(20,4))
        self.assertEqual((o.gained,len(o.quirks),o.echo_cause),(6,6,'sixth_quirk'))
    def test_heavy_suit_and_black_zone(self):
        for raw in range(1,5):
            self.assertLess(net_damage(18,raw,2),3)
        self.assertEqual(net_damage(18,6,2),4)
    def test_minimum_one_and_monotonicity_exhaustive(self):
        for wil in range(1,19):
            for raw in range(1,7):
                damage = [net_damage(wil,raw,r) for r in range(5)]
                self.assertTrue(all(1 <= x <= (wil+1)//2 for x in damage))
                self.assertEqual(damage, sorted(damage,reverse=True))
    def test_exact_clean_wil_twelve_quirk_probability(self):
        triggers=0
        for save in range(1,21):
            for damage in range(1,5):
                o=resolve_check(12,frozenset(),4,ScriptedDice(save,damage))
                triggers += o.gained is not None
        self.assertEqual(Fraction(triggers,80), Fraction(1,10))
    def test_recovery_not_automatic(self):
        self.assertEqual(recover(5,12,6),11)
        self.assertEqual(recover(10,12,6),12)
        self.assertEqual(recover(5,12,6,deprived=True),5)
        self.assertEqual(recover(5,12,6,completed=False),5)
        self.assertEqual(recover(0,12,6,echo=True),0)
    def test_invalid_inputs_are_rejected(self):
        for value in (-1,0,True,1.5):
            with self.assertRaises(ValueError):
                effective_wil(value,0)
        with self.assertRaises(ValueError):
            resolve_check(12,frozenset({0}),4,random.Random(1))
        with self.assertRaises(ValueError):
            resolve_check(12,frozenset(range(1,7)),4,random.Random(1))

class ClockTests(unittest.TestCase):
    def test_exact_boundaries_all_zones(self):
        for zone, data in RULES['zones'].items():
            interval=data['interval_minutes']
            if interval is None:
                continue
            clock=ExposureClock()
            self.assertEqual(clock.advance(zone,interval-1),[])
            self.assertEqual(clock.advance(zone,1),[data['damage_die']])
            self.assertEqual(clock.dose,0)
    def test_short_yellow_trip_has_no_periodic_check(self):
        clock=ExposureClock()
        self.assertEqual(clock.advance('yellow',240),[])
        self.assertEqual(clock.dose,Fraction(1,2))
    def test_zone_transition_five_total_hours(self):
        clock=ExposureClock()
        self.assertEqual(clock.advance('orange',240),[])
        self.assertEqual(clock.dose,Fraction(2,3))
        self.assertEqual(clock.advance('red',59),[])
        self.assertEqual(clock.advance('red',1),[4])
        self.assertEqual(clock.advance('red',180),[4])
    def test_green_visit_does_not_reset(self):
        clock=ExposureClock()
        clock.advance('yellow',240)
        self.assertEqual(clock.advance('green',60),[])
        self.assertEqual(clock.advance('yellow',240),[4])
    def test_eight_hour_rest_resets_only_residual_clock(self):
        clock=ExposureClock(Fraction(3,4))
        clock.advance('green',479,resting=True)
        self.assertEqual(clock.dose,Fraction(3,4))
        clock.advance('green',1,resting=True)
        self.assertEqual(clock.dose,0)
    def test_green_work_is_not_rest_and_interrupts_rest(self):
        clock=ExposureClock(Fraction(1,2))
        clock.advance('green',300,resting=True)
        clock.advance('green',30)
        clock.advance('green',300,resting=True)
        self.assertEqual(clock.dose,Fraction(1,2))
    def test_shelter_slows_does_not_reset(self):
        clock=ExposureClock()
        clock.advance('orange',180)
        self.assertEqual(clock.advance('sheltered',359),[])
        self.assertEqual(clock.advance('sheltered',1),[4])
    def test_black_three_hours_and_residual(self):
        clock=ExposureClock()
        self.assertEqual(clock.advance('black',190),[6,6,6])
        self.assertEqual(clock.dose,Fraction(1,6))
    def test_chunking_does_not_change_checks(self):
        for zone in ('yellow','orange','red','black','sheltered'):
            a,b=ExposureClock(),ExposureClock()
            total=a.advance(zone,1000)
            chunks=[]
            for _ in range(100):
                chunks+=b.advance(zone,10)
            self.assertEqual((total,a.dose),(chunks,b.dose))
    def test_unknown_zone_and_negative_time_rejected(self):
        with self.assertRaises(ValueError):
            ExposureClock().advance('pink',60)
        with self.assertRaises(ValueError):
            ExposureClock().advance('red',-1)

class EvidenceTests(unittest.TestCase):
    def test_reproducible_and_counts_partition(self):
        a=simulate(PROFILES[3],100,10,42)
        b=simulate(PROFILES[3],100,10,42)
        self.assertEqual(a,b)
        self.assertEqual(sum(a['outcome_counts'].values()),100)
        self.assertEqual(sum(a['quirk_distribution_all'].values()),100)
        self.assertAlmostEqual(a['echo_percent'],a['echo_wil_percent']+a['echo_sixth_percent'])
    def test_no_checks_zero_contamination_outcomes(self):
        a=simulate(PROFILES[0],100,10,42)
        self.assertEqual((a['echo_percent'],a['quirks_all_mean'],a['mean_checks_taken']),(0,0,0))
    def test_heavy_suit_no_d4_mutations(self):
        a=simulate(PROFILES[6],100,10,42)
        self.assertEqual((a['quirks_all_mean'],a['echo_sixth_percent']),(0,0))
    def test_saved_report_provenance(self):
        root=Path(__file__).resolve().parents[1]
        report=json.loads((root/'reports/r2-contamination.json').read_text())
        import hashlib
        for name,digest in report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((root/'scripts'/name).read_bytes()).hexdigest(),digest)
        self.assertEqual(hashlib.sha256((root/'_data/contamination.json').read_bytes()).hexdigest(),report['rules_sha256'])
        self.assertEqual(report['human_playtests_added'],0)
        self.assertEqual(len(report['rows']),12)
        self.assertTrue(all(row['runs']==20000 for row in report['rows']))
    def test_web_and_pdf_source_invariants(self):
        root=Path(__file__).resolve().parents[1]
        build=(root/'scripts/build-pdf.py').read_text()
        self.assertIn('markdown_chapter("game-systems/contamination.md")',build)
        self.assertIn('markdown_chapter("reference/monte-carlo-transparency.md")',build)
        self.assertIn('markdown_chapter("adventures/the-first-four-weeks.md")',build)
        self.assertIn("class CheckedTable(Table):",build)
        banned=['Accumulate 5 Quirks and you become','echo threshold of 5',
                'On any WIL damage from contamination','WIL minus 4',
                'First Quirk around session 4-5', '2 checks guaranteed', 'A Quirk is nearly certain']
        texts=[build]+[p.read_text() for p in root.rglob('*.md') if '.git' not in p.parts]
        for bad in banned:
            self.assertFalse(any(bad in text for text in texts), bad)

if __name__=='__main__':
    unittest.main()
