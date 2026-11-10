# Sector Rotation Pool: US & A-Share, v1.2 (Phase-0 Architecture, Unregistered)

**v1.2 (2026-08-13).** Fills the "sector-rotation child contract" stub referenced but never built out in `Indicators_Pool_US_v2.md` and `Indicators_Pool_AShare_v2.md` (both at the line beginning "**Child contract, sector rotation**"). Derived from CodeX research across three review rounds; the third round found 7 confirmed issues in v1.1 (most seriously a genuine state-machine defect, not just missing detail) all independently re-verified before acceptance; see §12 changelog. **This is unregistered Phase-0 architecture, not a registered outline**: no atomic ID exists anywhere in `INDICATORS_REFERENCE.md` for anything in this document, and none should be added until §11's sequence is worked through.

**Parent files:** `Indicators_Pool_US_v2.md`, `Indicators_Pool_AShare_v2.md`. Siblings: `Indicators_Pool_MarketStructure_v1.md` (owns market-wide breadth/crowding), `Indicators_Pool_Fundamental_v1.md`, `Indicators_Pool_TrendReversal_v1.md`.

## 0. Verification note and bibliography

Checked directly rather than accepted on citation alone, across two rounds:

- **Every existing register ID cited**: grepped against `INDICATORS_REFERENCE.md`. All exist. **Corrected in v1.1:** `CN-T3`'s readiness is `S:F D:P P:U (P9)` (register line 972): v1.0 mistyped this as `P:N` in two places, which would have implied "PIT revisions not applicable," the opposite of the actual PIT-unverified blocker the row documents. Fixed throughout.
- **The "missing child contract" claim**: confirmed; both parent pools contain only a two-sentence stub.
- **Moskowitz & Grinblatt (1999)**, "Do Industries Explain Momentum?", *Journal of Finance* 54(4):1249–1290. [doi:10.1111/0022-1082.00146](https://doi.org/10.1111/0022-1082.00146). Confirmed: industry-level momentum explains much of individual-stock momentum.
- **申万 (Shenwan) 2021 revision**, confirmed materially significant: L1 28→31 industries (added 美容护理/beauty care, 石油石化/oil-petrochemical, 环保/environmental), several renamed, L2 104→134, L3 227→346.
- **Select Sector SPDR ETFs**, confirmed: the 11 sector SPDRs collectively span only the S&P 500.
- **Menzly & Ozbas (2010)**, "Market Segmentation and Cross-predictability of Returns," *Journal of Finance* 65(4). [doi:10.1111/j.1540-6261.2010.01578.x](https://doi.org/10.1111/j.1540-6261.2010.01578.x). Supplier/customer industries cross-predict returns via gradual information diffusion.
- **Hong, Torous & Valkanov (2007)**, "Do industries lead stock markets?", *Journal of Financial Economics* 83(2). [doi:10.1016/j.jfineco.2005.09.010](https://doi.org/10.1016/j.jfineco.2005.09.010). Some industries lead the broad market.
- **Chava, Hsu & Zeng (2020)**, "Does History Repeat Itself? Business Cycle and Industry Returns," *Journal of Monetary Economics* 116:201–218. [doi:10.1016/j.jmoneco.2019.10.005](https://doi.org/10.1016/j.jmoneco.2019.10.005). Confirmed via independent search (v1.1): industries with higher historical regime-conditioned Sharpe ratios earn higher expected returns conditional on the business cycle; a long-short sector-rotation strategy on this signal earned 11.9–14.0% annualized FF3/FF5 alpha, 1985–2014, not explained by industry momentum. **This is a source-faithful finding, not what §5 below builds**. See the §5 correction.
- **Boubaker, Du & Liu (2022)**, "Industry momentum with correlation consolidation: evidence from China," *Journal of Asset Management* 23:73–82. [doi:10.1057/s41260-021-00248-8](https://doi.org/10.1057/s41260-021-00248-8). Confirmed via independent search (v1.1): consolidating Chinese industries by return correlation (optimal threshold ρ=0.75) raised industry-momentum Sharpe from 0.71 to 1.16, June 2007–December 2020.

**Four** papers above (Menzly-Ozbas, Hong-Torous-Valkanov, Chava-Hsu-Zeng, Boubaker-Du-Liu) support **different mechanisms**, not one common "supply-chain/lead-lag" story, v1.0 blurred them together and additionally miscounted them as "three" in its own closing section. Corrected: Menzly-Ozbas and Hong-Torous-Valkanov are lead-lag/information-diffusion mechanisms; Chava-Hsu-Zeng is a business-cycle-conditioning mechanism (feeds §5, not §9's lead-lag item); Boubaker-Du-Liu is a correlation-consolidation mechanism specific to China (feeds §6's internal-correlation discussion, not lead-lag). None of the four have been read past abstract/search-result level. Treat the mechanism summaries above as plausible, not as a substitute for reading the papers before building on them.

---

## 1. What counts as sector rotation

A rising sector alone is not rotation. Rotation requires: relative outperformance, *accelerating* relative performance, a leadership change from prior leaders, participation from a meaningful share of constituents, and persistence beyond a few sessions.

**Sector definitions (PIT, dated, not backfilled):**
- **US:** historical GICS sector/industry group, effective-dated.
- **A-share:** historical Shenwan Level-1 (申万一级) as v1 default; Level-2 later. Pre-2021 and post-2021 Shenwan L1 series **cannot be concatenated as constant** (§0).

**Sector return construction:**
```
r_{g,t} = Σ_{i∈g_{t−1}} w_{i,g,t−1} · r_{i,t}
```
Membership and cap-weights frozen at `t−1`.

**Rebalance-convention gap, corrected in v1.1.** v1.0 never specified whether the *equal-weight* series' 1/N weights reset daily or only at fixed rebalance dates. Resetting daily creates a costless daily-rebalanced portfolio, which is not a tradable or even well-defined comparison series. **Decision, not yet tested:** equal weights should reset only at the same monthly cadence as the parent contract's stated default (§0 of the parent pool stub: "monthly rebalance default"), not daily.

**Delisting/corporate-action handling, still not a usable rule (confirmed gap, v1.2).** v1.1 said to "inherit" the main register's `P4` delisting-return gap, but that gap is itself unresolved: last-good-price exit is a **known upward-biased placeholder**, not a valid terminal-return convention, and citing it here doesn't pin anything new. This is not a detail to defer casually, it belongs explicitly in §11's registration sequence as its own required step: a sector return series needs (a) a terminal-return convention for delisted constituents (not silent last-price carry-forward), (b) distribution/dividend handling consistent with the total-return-index convention in §3.A, (c) index-removal timing (does a stock leave sector `g`'s return series the same period it's removed from `g`'s classification, or with a lag), and (d) corporate-action (split/spin-off) price continuity. None of these are decided.

```
ConcentrationGap_{g,t} = r^CW_{g,t} − r^EW_{g,t}
```
Large positive gap flags concentration-driven "rally," not broad participation.

---

## 2. Existing register coverage vs. gaps

**Directly reusable, cite by ID, do not redefine:**

| ID | What it is | Readiness |
|---|---|---|
| `US-T3` | 6-1m sector RS rank | `S:F D:A P:N` |
| `CN-T3` | 6-1m Shenwan-L1 RS rank | `S:F D:P P:U` (P9): **corrected from `P:N` in v1.0** |
| `US-B1.1`/`US-B1.2`, `US-B2` | Market-wide breadth level/divergence, net new highs | `S:F` various |
| `CN-B1.1-1.3` | Market-wide breadth level/A-D/divergence | `S:F D:T P:N` |
| `US-V3.1-3.3`, `US-V5` | Aggregate index-level revision breadth/magnitude/dispersion; quality breadth | `S:F D:L P:U` / `S:F D:B P:P` |
| `CN-V5.1-3`, `CN-V6` | Same, A-share | `S:F D:L P:U` / `S:F D:T P:U` |
| `US-X3` | Defensive-sector leadership (XLU/XLP vs SPY) | `S:F D:A P:N` |
| `CN-B2` | Normalized market-wide turnover | `S:F D:T P:N` |
| `CN-B3.1-8` | Limit-up/limit-down regime family | mixed, see §11 of the main register |
| `CN-F2` | ETF share creation (broad-index) | `S:F D:T P:N` |
| `US-R5.1/5.2`, `CN-R3.1/3.2` | **Market-wide** implied/realized correlation, cross-sectional dispersion: **not sector-conditioned; see §6 correction** | mixed |

**Confirmed gaps this document addresses:**
1. A real sector-rotation child specification.
2. Sector-specific breadth (existing `US-B1`/`CN-B1` are market-wide).
3. Sector-specific fundamental breadth.
4. Leadership-state and rotation-event definitions.
5. Cap/equal-weight sector concentration diagnostics.
6. Sector ETF/index investability mapping.
7. Sector-level crowding/capacity limits.
8. Lead-lag factors (Menzly-Ozbas / Hong-Torous-Valkanov mechanisms, distinct from each other, §0).
9. **Sector-internal correlation/dispersion**: genuinely new (§6), not a reuse of `US-R5`/`CN-R3`.
10. A monthly information-cutoff/clock discipline spanning the mixed-frequency inputs below (§3.F, new in v1.1).

---

## 3. Core identification signals, unregistered candidates, several formulas still incomplete

### 3.A Price leadership: level and acceleration

```
RS_{g,t} = TRIndex_{g,t} / TRIndex_{market,t}
RelMom^{6-1}_{g,m} = ln(RS_{g,m−1} / RS_{g,m−6})     ≡ US-T3 / CN-T3's own construction, cite, don't duplicate
RelMom^{3-1}_{g,m} = ln(RS_{g,m−1} / RS_{g,m−3})     new, faster variant
L_{g,t} = z_52w(ln RS_{g,t})                          normalized RS level
A_{g,t} = L_{g,t} − L_{g,t−20}                         RS acceleration, 20 trading days
```

| State | Rule |
|---|---|
| Improving | `L<0, A>0` |
| Leading | `L>0, A>0` |
| Weakening | `L>0, A<0` |
| Lagging | `L<0, A<0` |

### 3.B Sector breadth

```
Breadth^k_{g,t}            = #{i∈g: P_i,t > MA_k(i,t)} / N^eligible_{g,t}, general form, k = MA window in days
BreadthAcceleration_{g,t}  = Breadth^60_{g,t} − Breadth^60_{g,t−20}
PositiveReturnBreadth^63_{g,t} = #{i: r^63d_i,t > 0} / N^eligible_{g,t}
NetHighBreadth_{g,t}       = (NewHighs_{g,t} − NewLows_{g,t}) / N^eligible_{g,t}
```

**Corrected in v1.1:** v1.0 defined only `Breadth^200` (used in §4's `LeadershipScore`) but then used the undefined `Breadth^60` in `BreadthAcceleration`. Now both are instances of one general form `Breadth^k`, `k` pinned per use (200d for the leadership-score level term, 60d for the acceleration term, matching the two different questions "is the sector broadly above its long-term trend" vs. "is participation building over the last month").

**`N^eligible`: corrected, still not fully pinned.** v1.0 cited only `P4` (A-share) and never addressed the US side. **US should cite `P5`** (the register's US universe primitive) for the analogous eligibility filter; A-share continues to cite `P4`. Neither primitive alone fully defines a *sector's* eligible set, the actual requirement is `{market-eligible names} ∩ {sector_g membership at t−1}`, and that intersection rule (plus a minimum-constituent-count floor below which a sector's breadth read is not meaningful) is still open. This mirrors the same `N^eligible` gap already left open and explicitly documented for `CN-B3.5`/`.6` in the main register, naming the analogous primitive here is progress, but it is not the same as pinning the value.

### 3.C Fundamental breadth

```
ProfitImprovementBreadth_{g,t} = #{i: ΔOM_i,t > 0 ∧ ΔCoreProfit_i,t > 0} / N^observable_{g,t}
RevisionBreadth_{g,t}          = (UpwardRevisions_t − DownwardRevisions_t) / CoveredCompanies_t
```
**`ΔCoreProfit`: only the horizon is actually pinned (corrected, v1.2).** v1.1 claimed this was "now pinned" by pointing to the MAGNET spec's `ACCEL` convention, but MAGNET's own numerator is only pinned for CN (扣非归母净利润); its US leg ("core operating profit") has **no field map or exact formula** in MAGNET either (`MAGNET-A_US_Strategy_Spec_v1.md` §1.1, §2.1: MAGNET itself flags this as open). Delegating to an already-open definition doesn't close the gap here. Accurate status: the **comparison horizon** (`t` vs `t−4q`, TTM) is pinned; the **cross-market numerator convention**, especially the US core-profit field map, is not, and won't be until MAGNET resolves its own §2.1 open item, track this as one shared open decision, not two independent ones.

`MarginImprovementBreadth` (used in §4 but never defined in v1.0) is now: `#{i∈g: ΔOM_i,t > 0} / N^observable_{g,t}`. Note this makes it **partially redundant** with the `ΔOM>0` leg already inside `ProfitImprovementBreadth`; if both are used in the same `FundamentalBreadth` blend (§4), this overlap should be declared explicitly, not silently double-counted, per this project's standing redundancy-declaration discipline.

US: reuse the `US-V3`/`US-V5` aggregation logic at sector level. A-share: build from timestamped 业绩预告/快报/report deltas (`P14` announce-date spine); do not backfill.

**Still undefined, confirmed gap (v1.2):** `N^observable`'s exact population (same open question as `N^eligible` in §3.B, not yet given its own answer here), the revision-measurement window and frozen-consensus rule for `RevisionBreadth`, and the minimum-observable-companies/sector-coverage threshold below which a sector's fundamental-breadth read isn't meaningful.

### 3.D Flow and attention

Candidates only, **no combination formula defined** (this was true in v1.0 too, but v1.0 then used an undefined `Flow` term in §4's score. See that correction): US sector ETF net creations/AUM, sector ETF $ volume vs. trailing ADV, sector-level abnormal turnover. A-share: sector ETF share creations (extends `CN-F2`), margin-financing intensity, sector turnover/free-float mcap, limit-up breadth (extends `CN-B3`), northbound holdings under correct disclosure dating.

### 3.E Rotation intensity

```
Dispersion_t = SD_g(RelReturn^63d_{g,t})
Churn_t      = 1 − |TopK_t ∩ TopK_{t−20}| / K
```

**Still open, unchanged from v1.0:** the value of `K`, and the historical window/population over which `DispersionPercentile_t` is computed (all-history expanding? trailing N years?). Not pinned. Candidate confirmation rule (research starting point): `DispersionPercentile_t > 50` and `Churn_t ≥ 1/K` and persistence for 2 weekly observations or 1 month-end.

### 3.F Information cutoff and clock, an as-of rule, not yet an execution clock

v1.0 combined monthly `RelMom^{6-1}`, a 20-trading-day `A`/`BreadthAcceleration` window, weekly rotation-intensity persistence checks, quarter-lagged fundamental breadth, and (in §5) macro releases: **with no single information cutoff governing what's "known" at the monthly decision point**, unlike the main register's `CLK-*` discipline (e.g. `CLK-CORPACTION`, `CLK-FILING`/`CLK-RELEASE`). **As-of rule (v1.1, unchanged):** at each monthly rebalance cutoff, every input is evaluated using the latest observation with a timestamp strictly before the cutoff, carried forward from its last release, never using data released after the cutoff even if dated earlier in the period.

**Correction (v1.2): this rule alone is not an execution clock.** It says what's *knowable*, not when the decision is *made and acted on*. Still undefined, and confirmed as a real gap by re-reading this section: the exact rebalance timestamp and timezone; whether the month-end closing print itself is included in "before the cutoff" or excluded by a strict inequality landing exactly on it (a literal reading of "strictly before" would exclude the close if the cutoff *is* the close timestamp, almost certainly not the intent, but the document doesn't say so); the signal-completion timestamp (when the score itself is finished computing, which must be after the data cutoff but is a distinct moment); and the first executable session/price. **Placeholder, not yet decided:** model this on the register's own `CLK-RELEASE` pattern (scheduled release → first permissible trade) as `CLK-CLOSE(monthly) → next tradable open`, i.e. data as of the last trading day's close of the month, decision computed after that close, executed at the next session's open, but this is a proposal to test, not a frozen rule, and it duplicates the same execution-contract gap already left open in `MAGNET-A_US_Strategy_Spec_v1.md` §6. Don't solve it twice independently, resolve once and cite from both documents.

---

## 4. Sector leadership score, still not fully codeable

```
LeadershipScore_{g,t} = 0.35·PriceLeadership + 0.25·Breadth + 0.20·FundamentalBreadth + 0.10·Flow + 0.10·RegimeFit

PriceLeadership   = 0.50·P(RelMom^{6-1}) + 0.30·P(RelMom^{3-1}) + 0.20·P(A)
Breadth           = 0.40·P(Breadth^200) + 0.30·P(BreadthAcceleration) + 0.30·P(NetHighBreadth)
FundamentalBreadth = 0.40·P(RevisionBreadth) + 0.30·P(ProfitImprovementBreadth) + 0.30·P(MarginImprovementBreadth)
Flow              = not yet defined: §3.D gives candidates only, no combination rule
RegimeFit         = not yet defined: §5 gives RegimeSharpe, not a mapping from RegimeSharpe to a 0-100 percentile score
```
**`Flow` and `RegimeFit` remain undefined**: v1.0 used both as if specified; they are not. A placeholder on the three remaining terms (`PriceLeadership`/`Breadth`/`FundamentalBreadth`, reweighted to sum to 1.0) can be drafted, but **correction (v1.2): calling that placeholder "codeable" overstated it.** Those three terms themselves still rest on undefined sub-contracts, confirmed by re-reading §3: `NewHighs`/`NewLows`' horizon (52-week? trailing-year?) is never stated; the percentile method (`P(·)`) never specifies tie-handling or the minimum number of valid sectors needed for a percentile to be meaningful; and moving-average terms (`Breadth^k`) never state a price-adjustment convention (split/dividend-adjusted vs. raw) or a minimum-history requirement before a sector's MA reading is trusted. **Accurate status: even the three-term reduced score stays Phase-0 until §3's sub-contracts are pinned, not merely until `Flow`/`RegimeFit` are added.**

**Missing-data rule (unchanged):** if revision data are unavailable, define and test a separate no-consensus variant of `FundamentalBreadth` rather than silently redistributing weight.

### 4.1 Level label and hold/exit machine, two separate outputs, rebuilt in v1.2

v1.1 tried to fix v1.0's overlapping numeric bands with a single seven-branch ordered list, gated on "prior state." That introduced a **real logic defect**, confirmed by tracing it: `Rotation exit` (checked first, fires on `score<45`) made `Lagging` (`score<35`) structurally unreachable, every `<35` case was already caught by `<45`, and a sector that had never been held could still be labeled an "exit," which isn't a meaningful event for something never entered. Worse, `Strong leader` matched on `score≥75, breadth>60%` alone and returned immediately, so a sector whose breadth fell 75%→62% (a real ≥10pp drop that should trigger `Weakening`) stayed labeled `Strong leader` because the ordered list never reached the `Weakening` branch for it.

**Root cause:** a *level description* (what does this sector's score/breadth currently look like) and a *portfolio event* (did we just enter or exit a holding) were fused into one ordered list. Corrected by splitting them into two independent outputs:

**(a) Level label, pure function of current score, no ordering tricks, no state dependency:**

| Label | Score band | Extra gates (failing a gate drops one band, does not exit the machine) |
|---|---|---|
| Strong | `≥75` | breadth `>60%`, fundamental breadth positive: else treat as Confirmed |
| Confirmed | `[65,75)` | top quartile, `RelMom^{6-1}>0`, breadth `>50%`: else treat as Neutral |
| Emerging | `[55,65)` | 4-week score change `>0`, RS acceleration `>0`: else treat as Neutral |
| Neutral | `[35,55)`, or a higher band that failed its gate | n/a |
| Lagging | `<35` | n/a (now reachable: score alone determines this band, nothing upstream can claim it first) |

Score bands are disjoint by construction, no precedence rule is needed for this half, which is what removes the v1.1 defect.

**(b) Hold/exit machine, separate, applies only to sectors currently in the allocation budget (§8), hysteresis between entry and exit thresholds:**

- **Entry:** a not-currently-held sector becomes eligible for `SectorBudget` (§8) when its level label reaches `Confirmed` or `Strong`.
- **Hold:** a currently-held sector keeps its allocation while level label stays `Emerging` or better, **or** breadth has not dropped `≥10pp` from its level at entry/last re-confirmation, this is the check v1.1's ordering skipped; it now runs independently of what level label the sector currently carries.
- **Exit:** fires **only for a currently-held sector** (this is what makes exit "conditional on prior ownership," per the finding) when either: level label falls to `Lagging`/`Neutral` for 2 consecutive observations, or the breadth-drop trigger above fires, or `score<45` for 2 consecutive observations.

This is the same entry/hold-threshold-with-hysteresis pattern already used (after its own earlier correction) in `MAGNET-A_US_Strategy_Spec_v1.md` §4's rebalance state machine, reuse that precedent rather than re-deriving a third version.

Exact thresholds remain unfitted starting points; the fix here is the *machine's structure*, not the numbers.

---

## 5. Macro/business-cycle conditioning, corrected: separate the source-faithful benchmark from the extension

Reject the naive fixed "investment clock" as a primary signal, consistent with this project's standing rejection of fixed macro-regime mappings elsewhere (`SLOOS`/`ACM`).

**Source-faithful benchmark (Chava-Hsu-Zeng, §0), stated separately, not to be silently generalized:** their result uses **annual** industry excess returns and a **binary** positive/negative output-gap regime, with `RegimeSharpe` computed only from earlier years *within the same regime*. This is the actual replication target if anyone wants to test the paper's own finding.

**This document's extension (untested, not a replication):**
```
RegimeSharpe_{g,r,t} = Mean_{τ<t, Regime_τ=r}(ExcessReturn_{g,τ}) / SD_{τ<t, Regime_τ=r}(ExcessReturn_{g,τ})
```
generalized to multiple regime dimensions (US: growth/inflation/rate/credit/liquidity surprise; A-share: growth/CPI/PPI/credit-impulse/property/RMB, kept separate not netted) at a presumably monthly cadence rather than annual, and a `RegimeFit` mapping from `RegimeSharpe` to the leadership score that is not yet defined (§4). **This must be named and tested as a distinct extension from the Chava-Hsu-Zeng benchmark**, not presented as if it were the paper's own finding scaled up.

**A-share macro-data PIT status, already a known blocker, corrected (v1.2).** v1.1 called this an unchecked future question; it is not, the register already answers it directly. `P15` (macro vintage spine, register line 205) states explicitly: **`P15-CN` is `S:F D:U P:F`**: *"no verified standardized archive in the current free stack... forward snapshots"* until one is procured. This is the same forward-only constraint already established for A-share fundamentals (§7-equivalent discussion in the MAGNET spec), now confirmed to apply to the CN macro series this section proposes to use (CPI/PPI surprise, credit impulse, property-transmission indicators) as well. **Practical consequence:** any CN `RegimeSharpe` history built before a vintage archive exists is not backtest-causal, the CN regime-conditioning extension in this section is prospective-only for now, exactly like A-share fundamentals elsewhere in this project. Record this as a known blocker in §10, not a check still to run.

Test only after the price/breadth baseline (§9) is validated.

---

## 6. Crowding and false-rotation risk

Belongs in a `CROWDING/ROTATION_RISK` redundancy group (cross-reference the main register's `MS-R` family, don't duplicate), applied as a one-sided weight cap, not folded into `LeadershipScore`:

- Short-term sector return in the top 5% of its own history.
- Abnormal turnover above the 90th percentile.
- Breadth has stopped improving even as price extends.
- `ConcentrationGap` (§1) strongly positive.
- **Sector-internal correlation spike, corrected in v1.1.** v1.0 said "reuse `US-R5`/`CN-R3`" for this; those IDs are **market-wide** aggregate correlation/dispersion measures (register: `US-R5.1` is the CBOE COR index; `CN-R3.1/3.2` are market-wide 63d rolling dispersion/pairwise correlation): none are conditioned on sector membership. Computing correlation *within* a sector's constituents is a genuinely new aggregation (own minimum-constituent-count, own shrinkage/estimation-window contract) that happens to reuse the same *methodology* as `US-R5.2`/`CN-R3.2`, not the same *series*. Name it something distinct (e.g. `SectorInternalCorr`, unregistered) rather than citing the existing IDs as if they already cover this.
- A-share limit-up activity entering a blow-off regime (extend `CN-B3` conditioning).
- Valuation/earnings expectations extreme without further upward revisions.

---

## 7. US vs. A-share implementation differences

| Design axis | US | A-share |
|---|---|---|
| Classification | Historical GICS sector/industry group | Historical Shenwan L1 (2021 revision non-comparable pre/post) |
| Eligibility primitive | `P5` | `P4` |
| Primary price signal | `US-T3` (6-1m) | Test `CN-T3` (6-1m) against faster 4-12 week variants |
| Confirmation | Breadth + `US-V3`/`US-V5`-style revisions | Breadth + timestamped 预告/快报/report clusters |
| Flow | Sector ETF flows/turnover | Sector ETF flows, margin intensity, normalized turnover, limit-family conditioning |
| Tradability | ETF spread/impact, halts; Select Sector SPDRs cover only S&P 500 | T+1, price limits, suspensions, board-lot sizes, stamp duty |
| Benchmark | Equal-weight sector basket, monthly-reset (§1) | Equal-weight Shenwan-L1 basket, monthly-reset (§1) |

Walk-forward selection with a locked holdout. Do not report the best full-sample formation/holding combination as a finding.

---

## 8. Integration boundary with allocation / MAGNET

```
SectorBudget_{g,t} = BenchmarkWeight_{g,t} + ActiveTilt(LeadershipScore_{g,t})
```

**This is architecture only, not yet a portfolio-weight rule, confirmed gap, v1.2.** `ActiveTilt`'s functional form is not defined; there is no stated normalization (do tilts sum to zero across sectors, and what happens when they don't), no long-only floor, no maximum per-sector exposure, and no turnover cap. Do not read this equation as producing tradable weights, it states *where* sector rotation plugs into the allocation layer, not *how much*. Pinning `ActiveTilt` belongs in §11's registration sequence, likely deferring to the same allocation-layer machinery (`beta_cap`/projection objective) already specified at the contract level in `Indicators_Pool_Combination_v1.md`, rather than inventing a parallel one here.

Stock selection (`MAGNET-{A,US}-{EQ,EV}`, see `MAGNET-A_US_Strategy_Spec_v1.md`) runs *within* each sector's budget. Avoid double-counting: do not both give stocks a sector-leadership bonus in their own score AND overweight the sector at the allocation layer. `NEW` stays company-specific; `EMERGE`/`BREADTH` can use §3.C's fundamental breadth; sector price momentum sets the *budget*, stock-level `RMOM` sets *selection within* it. Test both layers' incremental value by ablation.

---

## 9. Recommended development order

1. Point-in-time sector returns and benchmarks, with the rebalance convention pinned (§1).
2. `RelMom^{6-1}` baseline, already registered as `US-T3`/`CN-T3`.
3. RS level/acceleration four-state map (§3.A).
4. Sector breadth, with `N^eligible` actually pinned this time, not just named (§3.B).
5. Fundamental breadth, using the now-pinned `ΔCoreProfit` convention (§3.C).
6. Define `Flow` and `RegimeFit` combination formulas before using them in `LeadershipScore` (§4).
7. Rotation-intensity and crowding diagnostics, with `SectorInternalCorr` built as its own contract, not cited from `US-R5`/`CN-R3` (§3.E, §6).
8. Macro conditioning, replicate Chava-Hsu-Zeng's actual (annual, binary-regime) construction first as a named benchmark before testing the multi-dimension monthly extension (§5).
9. Lead-lag models. Read Menzly-Ozbas and Hong-Torous-Valkanov directly; they are different mechanisms and may warrant separate cards.
10. ML challenger only after beating the plain 6-1 momentum baseline net of costs.

## 10. Explicitly not done

- No backtest of any component.
- No weight in §4's `LeadershipScore` fitted; even the reduced three-term placeholder stays Phase-0 until `NewHighs`/`NewLows` horizon, percentile tie-handling, minimum valid sectors, and MA price-adjustment/history are pinned (§4).
- `N^eligible` and `N^observable`'s exact per-sector intersection rules and minimum-constituent floors not pinned (§3.B, §3.C).
- `K` and the dispersion-percentile window (§3.E) not pinned.
- `ΔCoreProfit`'s cross-market numerator is not pinned, blocked on `MAGNET-A_US_Strategy_Spec_v1.md` §2.1's own open US core-profit definition (§3.C).
- The execution clock (§3.F) is an as-of/no-leakage rule only, exact cutoff timestamp/timezone, month-end-close inclusion, and first-executable session are undecided, and duplicate the same gap open in the MAGNET spec's §6.
- Delisting-return convention, distribution handling, index-removal timing, and corporate-action price continuity for sector returns are undecided (§1): last-good-price carry-forward is a known-biased placeholder, not a rule.
- `ActiveTilt`'s functional form, normalization, floors, caps, and turnover limits are entirely undefined (§8): `SectorBudget` is architecture, not a weight rule.
- Sector ETF/index investability mapping not built.
- The four literature mechanisms in §0 have not been read past search-result/abstract level.
- **A-share macro-series PIT status is a known blocker, not an open question**, `P15-CN` is `S:F D:U P:F` (register line 205, confirmed v1.2): no verified vintage archive, forward-snapshot only.

## 11. Registration sequence (do not register yet)

1. Pin `N^eligible`/`N^observable`, `K`, the dispersion window, and the delisting/corporate-action convention for sector returns (§1, §3.B, §3.C, §3.E).
2. Resolve `ΔCoreProfit`'s US numerator jointly with `MAGNET-A_US_Strategy_Spec_v1.md` §2.1, one shared decision, not two.
3. Define `Flow` and `RegimeFit` as actual formulas; pin percentile tie-handling and minimum-valid-sector rules for every `P(·)` term.
4. Pin the execution clock (§3.F) jointly with the MAGNET spec's §6, one shared decision, not two.
5. Build `SectorInternalCorr` as its own contract, separate from `US-R5`/`CN-R3`.
6. Replicate Chava-Hsu-Zeng's source-faithful (annual, binary-regime) construction as a named benchmark before testing this document's multi-dimension monthly extension, and treat any CN leg as prospective-only given `P15-CN`.
7. Read the four §0 papers directly; confirm the mechanism summaries above hold up.
8. Define `ActiveTilt` and its constraints, most likely by deferring to `Indicators_Pool_Combination_v1.md`'s existing allocation machinery rather than inventing a parallel one.
9. Only then assign atomic IDs and complete the register's mandatory field schema (clock, information timestamp, inputs, minimum history, missingness, dependencies, redundancy group, evidence grade) for each card.
10. Add a hypothesis/evaluation table (target horizon, benchmark, rejection rule, market-specific evidence grade) per the register's pre-registration requirement, before any backtest.
11. Backtest with locked holdouts, US and A-share independently.

---

## 12. Changelog

**v1.2 (2026-08-13).** Third-round CodeX review found 7 confirmed issues in v1.1, independently re-verified before acceptance:
- **State machine rebuilt, v1.1's fix had a real logic defect, not just missing detail.** Confirmed by tracing it: the ordered `Rotation exit →... → Lagging` list made `Lagging` (`score<35`) structurally unreachable (already caught by `Rotation exit`'s `score<45`), let a never-held sector be labeled an "exit," and let `Strong leader` re-match on `score≥75, breadth>60%` before the `Weakening` branch (breadth-drop check) was ever reached, so a sector whose breadth fell 75%→62% stayed `Strong leader`. Root cause: a level description and a portfolio event were fused into one ordered list. Fixed by splitting into (a) a disjoint score-band level label needing no ordering, and (b) a separate hold/exit machine gated on prior ownership, modeled on the MAGNET spec's own (already-corrected) rebalance state machine (§4.1).
- **`ΔCoreProfit` correction retracted.** v1.1 claimed this was "now pinned" by citing MAGNET's `ACCEL` convention, but MAGNET's own US numerator is itself open (no field map for "core operating profit"). Delegating to an open definition didn't close anything. Corrected: only the comparison horizon is pinned; the cross-market numerator is a shared open decision with the MAGNET spec, not two independent gaps (§3.C).
- **`P15-CN`: already a known register blocker, not an unchecked question.** v1.1 said "flagged, not yet checked"; the register states directly (line 205) that `P15-CN` is `S:F D:U P:F` (no verified vintage archive, forward-snapshot only). Should have been grepped before writing the softer v1.1 language. Corrected in §5, moved from "explicitly not done" to a stated blocker.
- §3.F reframed: the as-of/no-leakage rule is not an execution clock. Added the specific missing pieces (exact cutoff timestamp/timezone, month-end-close inclusion, signal-completion timestamp, first executable session) and a placeholder `CLK-CLOSE→next open` proposal, cross-referenced to the MAGNET spec's own open execution-contract gap rather than solved twice independently.
- §1: delisting/corporate-action handling corrected from "inherit an open gap" to an explicit four-part requirement (terminal return, distributions, index-removal timing, corporate-action continuity) added to §11's registration sequence.
- §4: acknowledged that even the reduced three-term `LeadershipScore` placeholder rests on further undefined sub-contracts (`NewHighs`/`NewLows` horizon, percentile tie-handling, MA price-adjustment/history): "codeable" was overstated.
- §8: `SectorBudget`/`ActiveTilt` explicitly labeled architecture-only, no normalization, floors, caps, or turnover limits defined; deferred to `Combination`'s existing allocation machinery rather than inventing a parallel one.
- Registration held again, confirmed appropriate, arguably more clearly than after v1.1 given the state-machine defect found this round.

**v1.1 (2026-08-13).** Second-round CodeX review found 10 confirmed issues in v1.0, independently re-verified before acceptance:
- `CN-T3` readiness corrected `P:N` → `P:U` (register line 972, a flat transcription error, not a judgment call).
- **"Registered outline" was a terminology misuse.** Checked against `MarketStructure`'s own established usage (its changelog: cards "outlined **in `INDICATORS_REFERENCE.md`**"): that term specifically means cards exist in the main register with IDs. Nothing here does. Retitled the whole document "Phase-0 architecture, unregistered."
- `Breadth^60` (used but undefined), `MarginImprovementBreadth` (used but undefined), `Flow` (candidates only, no combination formula), `RegimeFit` (no mapping from `RegimeSharpe` defined), `ΔCoreProfit`'s comparison period, and `K`/the dispersion-percentile window, all confirmed undefined-but-used in v1.0; fixed or explicitly flagged open (§3, §4).
- Rotation-state table rebuilt as an ordered, hysteresis-aware state machine, v1.0's numeric bands overlapped (confirmed by direct inspection: score 70 matched two states at once, score 30 matched two states at once) (§4.1).
- New §3.F: a monthly information-cutoff/clock rule, v1.0 mixed monthly/daily/weekly/quarterly/macro inputs with no cutoff discipline, unlike the register's `CLK-*` convention used everywhere else in this project.
- `N^eligible` guidance extended to name `P5` for the US side (v1.0 named only `P4`, A-share-only): still not fully pinned, now honestly scoped as such.
- §6 corrected: `US-R5`/`CN-R3` are market-wide, not sector-conditioned; sector-internal correlation needs its own contract (`SectorInternalCorr`).
- §0 literature: fixed a "four" vs "three" internal counting error; added an actual bibliography with verified DOIs for all four papers (two re-verified this round: Chava-Hsu-Zeng, Boubaker-Du-Liu); separated the four mechanisms explicitly rather than treating them as one "supply-chain" story.
- §5 corrected: separated Chava-Hsu-Zeng's actual (annual, binary-regime) construction from this document's untested multi-dimension monthly extension, which v1.0 presented as if scaled directly from the paper.
- §1: added the missing equal-weight rebalance-convention decision (monthly reset, not daily) and delisting/corporate-action inheritance note.
- Registration held again, confirmed appropriate.

**v1.0 (2026-08-13).** Initial draft filling the sector-rotation child-contract stub, derived from CodeX research with register-ID and citation spot-checks.
