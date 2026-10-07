"""R2.2.1 regression guards. They do not claim exhaustive semantic validation."""
from pathlib import Path
import hashlib,json,re,tempfile,unittest
import fitz
from procedures_r22 import weekly_close,ten_week_ledger
from check_r221 import FORBIDDEN,form_roundtrip,inspect_omnibus
ROOT=Path(__file__).resolve().parents[1]

def text(path):return (ROOT/path).read_text()

class CorrectiveSourceTests(unittest.TestCase):
    def test_no_audited_residues_in_canonical_chapters(self):
        for item in json.loads(text('_data/manual-chapters.json'))['chapters']:
            s=text(item['path']).casefold()
            for phrase in FORBIDDEN:self.assertNotIn(phrase.casefold(),s,item['path'])
    def test_corrective_version(self):self.assertEqual(json.loads(text('_data/manual-chapters.json'))['edition'],'R2.2.1')
    def test_minus_signs_are_explicit(self):self.assertIn('Old Debt + unpaid costs - repayments - clemency',text('game-systems/economy.md'))
    def test_meridian_roof_has_no_automatic_check(self):self.assertIn('No automatic contamination check',text('setting/adventure-sites.md'))
    def test_meridian_extra_hazard_warns_and_can_be_avoided(self):
        s=text('setting/adventure-sites.md')
        for p in ['Phase-interface hazard','10 minutes','normal temporal protection','only if included and announced']:self.assertIn(p,s)
    def test_quick_initiative_uses_opening_then_enemies_and_all_pcs(self):
        s=text('reference/warden-cheat-sheet.md');self.assertIn('Then enemies act, followed by all PCs',s);self.assertIn('it does not remove that turn',s)
    def test_dismissal_does_not_remove_pc(self):self.assertIn('This does not remove the PC from play',text('adventures/the-first-four-weeks.md'))
    def test_social_corruption_is_not_echo(self):self.assertIn('Corruption 10 does not itself',text('reference/hack-this-hack.md'))
    def test_certificate_denomination_and_no_implicit_rounding(self):
        s=text('game-systems/economy.md');self.assertIn('whole units only',s);self.assertIn('Do not automatically round',s)
    def test_payment_timing_and_reconstruction_are_distinct(self):
        s=text('game-systems/economy.md');self.assertIn('not already credited',s);self.assertIn('reconstructed from **opening Cash**',s)
    def test_license_author_decision_remains_open(self):self.assertIn('AUTHOR DECISION REQUIRED',text('docs/LICENSING_SCOPE.md'))
    def test_quick_reference_uses_zone_specific_intervals(self):self.assertIn('Yellow 8h / Orange 6h / Red 3h / Black 1h',text('reference/warden-cheat-sheet.md'))

class CorrectiveMoneyTests(unittest.TestCase):
    def test_reject_repayment_above_cash(self):
        with self.assertRaises(ValueError):weekly_close(50,500,0,0,repayment=51)
    def test_reject_repayment_above_principal(self):
        with self.assertRaises(ValueError):weekly_close(500,50,0,0,repayment=51)
    def test_reject_negative_repayment(self):
        with self.assertRaises(ValueError):weekly_close(50,500,0,0,repayment=-1)
    def test_both_deductions_before_interest(self):
        r=weekly_close(100,1000,0,0,repayment=100,clemency=300);self.assertEqual((r.cash,r.debt),(0,630))
    def test_equal_repayment_zeros_both(self):
        r=weekly_close(500,500,0,0,repayment=500);self.assertEqual((r.cash,r.debt),(0,0))
    def test_ten_week_values_still_unchanged(self):
        r=ten_week_ledger()[-1];self.assertEqual((r['cash'],r['debt']),(1270,987))

class CorrectiveArtifactTests(unittest.TestCase):
    def test_omnibus_structure_and_source_text(self):self.assertEqual(inspect_omnibus(ROOT/'CHRONOCAIRN_OMNIBUS_R2_2_1.pdf')['fields'],162)
    def test_all_three_standalone_forms_roundtrip_and_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            for label,n in [('Character_Sheet',43),('Accounting_Sheet',109),('Warden_Mission_Sheet',10)]:
                r=form_roundtrip(ROOT/f'downloads/CHRONOCAIRN_R2_2_1_{label}.pdf',Path(tmp));self.assertEqual(r['fields'],n)
    def test_all_omnibus_fields_roundtrip_and_reset(self):
        with tempfile.TemporaryDirectory() as tmp:self.assertEqual(form_roundtrip(ROOT/'CHRONOCAIRN_OMNIBUS_R2_2_1.pdf',Path(tmp))['fields'],162)
    def test_accounting_prints_repayment_guard(self):
        with fitz.open(ROOT/'downloads/CHRONOCAIRN_R2_2_1_Accounting_Sheet.pdf') as d:
            s=d[0].get_text();self.assertIn('reject excess',s);self.assertIn('Fields do not calculate automatically',s)
    def test_no_economic_or_contamination_engine_change(self):
        expected=json.loads(text('docs/R22_FROZEN_BASELINE.json'))
        for p,h in expected.items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
if __name__=='__main__':unittest.main()
