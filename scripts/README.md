# CHRONOCAIRN build and R1 verification

Install the repository Python requirements and Liberation fonts. Run commands from the repository root.

- `python -m unittest discover -s tests -v`: mechanical and source regression tests.
- `python scripts/economy_sim.py`: 100,000 paths per each of five explicit policies; fixed seed 42026; 15 weeks. Use `--trials` for a smaller smoke check and `--output` to keep it separate from published results.
- `python scripts/r1_report.py`: regenerate the measured evidence appendix from the JSON results.
- `python scripts/build-pdf.py`: rebuild `CHRONOCAIRN_Final_Complete.pdf`.
- `python scripts/r1_pdf_check.py`: structural/content checks of the generated PDF (not visual certification).

The economy, design/FAQ, mini-campaign and R1 evidence/worksheet sections are sourced directly from Markdown through `r1_pdf_sources.py`. Other chapters still use the legacy embedded builder; their complete migration is not claimed. `r1_finalize_sources.py` is an idempotent guarded migration from the recovered 32dd003 checkpoint. Do not apply it to the Omnibus line.

The manual is a review build, not KDP/POD-ready by certification. The PDF contains embedded rendering fonts; font binaries are not redistributed in the delivery patch.
