# Indicator inventory

Research contracts for cross-sectional and timing indicators in A-share and US
equity markets. These are specifications, not code. Each indicator records what
would have to be true for it to work and what would rule it out.

Four conventions run through every file.

**Pre-registration.** Before any backtest: primary target and horizon, expected
sign, primary metric, the minimum effect that would be economically useful net
of stressed costs, minimum sample, subperiod-stability requirement, and a
rejection rule.

**Evidence grading on three axes.** `E` for empirical strength (A replicated,
B regime-specific, C exploratory, D none), `P` for portability to the target
market's microstructure, `R` for data readiness with point-in-time verification.
An indicator with a plausible mechanism and no verified data sits in Deferred
rather than in the signal set.

**Point-in-time discipline.** Every field carries four timestamps: observation,
publication, decision cutoff, first executable. Backtests join on publication
and trade at first executable. Breadth and dispersion studies need
point-in-time universe membership, including delistings, IPO seasoning windows,
ST-status history and free-float history.

**Structural breaks dated, not smoothed.** Where a series was redefined or an
exchange rule changed, the break is dated in the file and pre-break history is
marked unusable for live signals rather than spliced across.

## Files

| File | Scope |
|---|---|
| `INDICATORS_REFERENCE.md` | Cross-file reference and conventions |
| `Indicators_Pool_AShare_v2.md` | A-share timing and risk-state model |
| `Indicators_Pool_US_v2.md` | US equivalent |
| `Indicators_Pool_Fundamental_v1.md` | Cross-sectional fundamentals |
| `Indicators_Pool_Financials_v1.md` | Financial-statement quality |
| `Indicators_Pool_MarketStructure_v1.md` | Capacity, borrow, crowding, price delay |
| `Indicators_Pool_SectorRotation_v1.md` | Sector rotation child contract |
| `Indicators_Pool_TrendReversal_v1.md` | Trend and reversal |
| `Indicators_Pool_StatRisk_v1.md` | Statistical risk |
| `Indicators_Pool_PortfolioRisk_v1.md` | Portfolio-level risk states |
| `Indicators_Pool_Combination_v1.md` | Combining families into composites |

Earlier `v1` drafts of the A-share and US files are kept privately as idea
catalogues. The `v2` files state where they diverge.

Each file ends with an appendix carrying its revision history. Those notes
record how a contract reached its current form and are not needed to read it.

## Status

Most rows are hypotheses. Evidence grades of C and D are common, and that is
the intended state: the inventory records what has been tested separately from
what merely sounds reasonable. Nothing here should be read as a claim that a
given indicator makes money.

Third-party work is cited in-file where an indicator is adapted from published
research. The architecture reference in the A-share file (Man Group, 2025) is
cited for structure only and not as evidence for any indicator.

## Citing

The repository root carries a `CITATION.cff`, which GitHub renders as a "Cite
this repository" button with BibTeX export.

> Wu, J. D. (2026). *Quant indicator inventory: falsifiable research contracts
> for A-share and US equity indicators.* Version 0.1.0.
> https://github.com/DWuuuuuu/quant-research-harness

## License

CC BY 4.0, see [`LICENSE-docs`](../../LICENSE-docs) at the repository root. You
may share and adapt these files, including commercially, with credit. Code in
this repository is MIT and licensed separately, see [`LICENSE`](../../LICENSE).
