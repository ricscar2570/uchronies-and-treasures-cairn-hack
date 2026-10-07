"""R2.2 regression examples, source guards and compiled-artifact checks."""
from pathlib import Path
import hashlib,json,re,tempfile,unittest
from procedures_r22 import Ammunition,attack,base_pay,mission_pay,scar_result,ten_week_ledger,unstable,weekly_close
ROOT=Path(__file__).resolve().parents[1]

class InstabilityTests(unittest.TestCase):
    def test_low_low_is_not_double_allegiance(self):
        for pair in [(0,0),(2,0),(0,2),(2,2),(3,2),(2,3)]:self.assertFalse(unstable(*pair))
    def test_activation_boundaries(self):
        for pair in [(3,3),(3,5),(5,3),(8,10),(10,8),(10,10)]:self.assertTrue(unstable(*pair))
    def test_difference_three_is_stable(self):
        self.assertFalse(unstable(3,6));self.assertFalse(unstable(6,3))
    def test_all_121_pairs_are_symmetric(self):
        for l in range(11):
            for c in range(11):self.assertEqual(unstable(l,c),unstable(c,l))
    def test_invalid_trackers_rejected(self):
        for pair in [(-1,0),(11,3),(True,3),(3.0,3)]:
            with self.assertRaises(ValueError):unstable(*pair)

class PayTests(unittest.TestCase):
    def test_canonical_unmodified_bands(self):
        self.assertEqual([mission_pay(b,5) for b in ['None','Failure','Standard','Strong','Exceptional']],[0,50,190,260,400])
    def test_trusted_standard_improves_one_band(self):self.assertEqual(mission_pay('Standard',7),260)
    def test_trusted_strong_improves_one_band(self):self.assertEqual(mission_pay('Strong',8),400)
    def test_no_uplift_for_failure_or_exceptional(self):
        self.assertEqual(mission_pay('Failure',10),50);self.assertEqual(mission_pay('Exceptional',10),400)
    def test_weekly_uplift_is_not_repeated(self):self.assertEqual(mission_pay('Standard',8,uplift_used=True),190)
    def test_instability_blocks_uplift(self):self.assertEqual(mission_pay('Standard',8,is_unstable=True),190)
    def test_hero_multiplies_base_only(self):
        self.assertEqual(base_pay('Recruit',9),1200);self.assertEqual(mission_pay('Exceptional',9),400)
        self.assertEqual(base_pay('Recruit',9)+mission_pay('Exceptional',9),1600)
    def test_tier_and_probation(self):
        self.assertEqual(base_pay('Agent',9),1800);self.assertEqual(base_pay('Veteran',9),2700)
        self.assertEqual(base_pay('Recruit',9,probation=True),600)
    def test_instability_keeps_ordinary_base(self):self.assertEqual(base_pay('Recruit',9,is_unstable=True),800)
    def test_bounty_replaces_band(self):self.assertEqual(mission_pay('Standard',9,bounty_gross=500),400)
    def test_model_rejects_undefined_or_fractional_money(self):
        with self.assertRaises(ValueError):mission_pay('Victory',5)
        with self.assertRaises(ValueError):mission_pay('Standard',5,bounty_gross=333)
    def test_base_close_matches_r1(self):
        self.assertEqual((weekly_close(0,580,800,920).cash,weekly_close(0,580,800,920).debt),(0,735))
    def test_cash_does_not_auto_repay(self):self.assertEqual(weekly_close(1000,500,0,0).debt,525)
    def test_repayment_then_interest(self):self.assertEqual(weekly_close(100,500,0,0,repayment=100).debt,420)
    def test_clemency_does_not_become_cash(self):
        r=weekly_close(0,100,0,0,clemency=300);self.assertEqual((r.cash,r.debt),(0,0))
    def test_no_overpayment(self):
        with self.assertRaises(ValueError):weekly_close(10,500,0,0,repayment=11)
    def test_ten_week_values(self):
        rows=ten_week_ledger();self.assertEqual([r['cash'] for r in rows],[540,340,280,0,200,50,10,660,860,1270])
        self.assertEqual([r['debt'] for r in rows],[525,552,580,735,772,811,852,895,940,987])
    def test_ten_week_manuscript_matches_executable(self):
        text=(ROOT/'adventures/the-first-four-weeks.md').read_text()
        for r in ten_week_ledger():
            numeric=' | '.join(f'${r[k]:,}' for k in ['income','costs','cash','debt'])
            self.assertIn(numeric,text)

class DamageTests(unittest.TestCase):
    def test_scar_uses_after_armor_damage(self):self.assertEqual(scar_result(4,5,1),4)
    def test_no_random_scar_on_overflow(self):self.assertIsNone(scar_result(4,6,1))
    def test_no_scar_when_already_at_zero(self):self.assertIsNone(scar_result(0,4,0))
    def test_no_scar_for_zero_damage(self):self.assertIsNone(scar_result(1,1,2))
    def test_scar_cap_twelve(self):self.assertEqual(scar_result(14,15,1),12)
    def test_reduced_strength_target(self):
        r=attack(2,11,6,1);self.assertEqual((r['hp'],r['str'],r['save_target']),(0,8,8))
    def test_zero_strength_is_death_without_save(self):
        r=attack(1,2,6,0);self.assertTrue(r['dead']);self.assertIsNone(r['save_target'])

class AmmoTests(unittest.TestCase):
    def test_loaded_with_no_spares_can_fire(self):self.assertTrue(Ammunition('ready',0).can_fire)
    def test_one_empties_current_only(self):
        a=Ammunition().after_firefight(1);self.assertEqual((a.state,a.spares),('empty',2))
    def test_two_then_two_empties(self):self.assertEqual(Ammunition().after_firefight(2).after_firefight(2).state,'empty')
    def test_low_persists_on_three_to_six(self):
        for die in range(3,7):self.assertEqual(Ammunition('low',1).after_firefight(die).state,'low')
    def test_reload_consumes_one_spare(self):self.assertEqual(Ammunition('empty',2).reload(),Ammunition('ready',1))
    def test_empty_without_spare_cannot_reload(self):
        with self.assertRaises(ValueError):Ammunition('empty',0).reload()
    def test_spare_slot_rounding(self):
        self.assertEqual([Ammunition('ready',i).spare_slots for i in range(6)],[0,1,1,2,2,3])
    def test_no_usage_roll_for_empty_firearm(self):
        with self.assertRaises(ValueError):Ammunition('empty',2).after_firefight(1)

class SourceTests(unittest.TestCase):
    def test_no_prohibited_active_residues(self):
        for entry in json.loads((ROOT/'_data/manual-chapters.json').read_text())['chapters']:
            text=(ROOT/entry['path']).read_text()
            for p in [r'\bXP\b',r'\(intended\)',r'failure state',r'No choice: it',r'a PC probably dies',r"team.s shared debt",r'\+1 Exposure']:
                self.assertIsNone(re.search(p,text,re.I),(entry['path'],p))
    def test_seven_creation_steps(self):
        text=(ROOT/'players-guide/character-creation.md').read_text()
        self.assertEqual(re.findall(r'^### (\d)\.',text,re.M),list('1234567'))
    def test_no_embedded_story_copy(self):
        text=(ROOT/'scripts/build-pdf.py').read_text();self.assertIn('CHAPTER_CONFIG',text)
        self.assertNotIn('Negotiate (intended)',text);self.assertNotIn('Better missions (+$200)',text)
    def test_causal_table_has_twelve_entries(self):
        text=(ROOT/'wardens-guide/tables-and-generators.md').read_text().split('## Causal Distortions (d12)')[1].split('## NPC Generator')[0]
        self.assertEqual(re.findall(r'^\| (\d+) \|',text,re.M),[str(i) for i in range(1,13)])
    def test_old_economy_simulation_is_not_current_validation(self):
        text=(ROOT/'reference/monte-carlo-transparency.md').read_text();self.assertIn('do not validate R2.2 economics',text)
        self.assertIn('Code-licensing clarification remains',text)
    def test_replacement_rule_has_no_inherited_debt(self):
        for p in ['players-guide/core-rules.md','wardens-guide/running-the-game.md','adventures/the-first-four-weeks.md']:
            self.assertIn('do not inherit the dead PC', (ROOT/p).read_text())
    def test_engine_and_data_unchanged(self):
        # R2.2 reference rules may change; the R2.1 contamination engine and parameters are frozen.
        reference=json.loads((ROOT/'docs/R22_FROZEN_BASELINE.json').read_text())
        for p,sha in reference.items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),sha,p)

class ArtifactTests(unittest.TestCase):
    def test_pdf_geometry_and_navigation(self):
        from check_pdf_r22 import inspect
        r=inspect(ROOT/'CHRONOCAIRN_Final_Complete.pdf');self.assertTrue(r['pass'],r)
    def test_all_source_hashes_match_rendered_build(self):
        manifest=json.loads((ROOT/'reports/r22-build-sources.json').read_text());self.assertEqual(len(manifest['chapters']),26)
        for e in manifest['chapters']:self.assertEqual(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest(),e['sha256'])
    def test_printable_forms_have_expected_fields(self):
        import fitz
        for label,n in [('Character_Sheet',43),('Accounting_Sheet',109),('Warden_Mission_Sheet',10)]:
            with fitz.open(ROOT/f'downloads/CHRONOCAIRN_R2_2_1_{label}.pdf') as doc:
                self.assertEqual(len(doc),1);widgets=list(doc[0].widgets());self.assertEqual(len(widgets),n)
                self.assertEqual(len({w.field_name for w in widgets}),n)
                for w in widgets:self.assertTrue(doc[0].rect.contains(w.rect),w.field_name)
    def test_form_fill_save_reopen(self):
        import fitz
        path=ROOT/'downloads/CHRONOCAIRN_R2_2_1_Character_Sheet.pdf'
        with tempfile.TemporaryDirectory() as tmp:
            with fitz.open(path) as doc:
                page=doc[0]  # Keep the parent page alive while modifying the widget.
                w=next(w for w in page.widgets() if w.field_name=='name');w.field_value='Reyes test';w.update();doc.save(Path(tmp)/'filled.pdf')
            with fitz.open(Path(tmp)/'filled.pdf') as doc:
                self.assertEqual(next(w.field_value for w in doc[0].widgets() if w.field_name=='name'),'Reyes test')
if __name__=='__main__':unittest.main()
