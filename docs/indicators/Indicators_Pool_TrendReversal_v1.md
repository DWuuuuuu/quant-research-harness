# Cross-Sectional Trend & Reversal Pool: US & A-Share, v1.10 (Child Contract)

**Parent files:** `Indicators_Pool_US_v2.md`, `Indicators_Pool_AShare_v2.md`. Siblings: `Indicators_Pool_Fundamental_v1.md`, `Indicators_Pool_StatRisk_v1.md`, `Indicators_Pool_MarketStructure_v1.md`. This is the **cross-sectional (individual-stock) price-based** child contract. The parent Trend sections (US-T*/CN-T*) stay **index/sector timing**; this file ranks *stocks against each other* by past-price behavior.
**Origin:** Codex review round 7 (trend/DHS). Earnings-event continuation (CAR/PEAD) is **not** here, it lives in fundamental F5 (`EARN_EVENT`), but is cross-referenced because it competes with price momentum for the same forward return.

> **Cross-sectional ≠ time-independent.** Rank all eligible names each rebalance and bet on relative past-price patterns; rankings recompute every period and factor efficacy is regime-dependent (momentum crashes, reversal regimes). Roughly market-direction-neutral; long-only tilts still carry market beta.

---

## 1. Research Contract (deltas from the fundamental child contract)

Inherits the fundamental child's PIT-universe, sector-relative scoring, FDR/holdout, and long-only-first rules. **The binding difference: these are the highest-turnover signals in the whole suite, cost & fill-feasibility modeling is the gating constraint, not an afterthought.**

| Field | US | A-share |
|---|---|---|
| Universe | PIT index membership w/ delistings | All-A ex IPO<6m, ST/*ST, suspended (entry-eligibility only), bottom-liquidity |
| **Strategy definition (v1.1: not just targets)** | formation date = signal computed from data through close t; **first executable = open t+1 (or t+1 VWAP)**; monthly rebalance default (family-specific), **overlapping cohorts** (e.g. Jegadeesh–Titman K-month overlapping portfolios) for K>1m holds; delistings carried at last-valid then final treatment; missing prices ≠ 0 return; explicit **long-only mapping** (rank → weight) | same, **T+1-aware** (position cuts respect the overnight hold) |
| Targets (IC decay only) | 5/21/63d (short) · 21/63/126d (momentum) · 126–756d (long reversal) forward return vs EW eligible universe | same |
| **Single-stock cost/borrow model (v1.3: parent ETF costs DO NOT apply; shared fields are owned by `Indicators_Pool_MarketStructure_v1.md` §MS-I1, while this file supplies orders, side, target participation, turnover, holding period and urgency)** | via MS-I1: explicit fees + spread + impact + ADV participation + funding/borrow/dividend cost + no-fill/delay cost; this file tests break-even alpha and realized capacity | + stamp duty on sells, T+1, board/date limit and suspension fill-feasibility; **融券 is legal but inventory is scarce and security×broker×date-specific: permit a short only where availability and cost are verified; unknown = unavailable; otherwise long-only + index-futures hedge** |
| Sector/style neutralize | **two stages, graded separately:** (1) source-faithful raw sort; (2) production sector-/beta-/size-neutral rank | 申万 sector; board (STAR/ChiNext/Main/BSE) beta differences neutralized at stage 2 |
| Positions | long-only first; L/S later | long-only default (single-name short only where borrow verified: MS-I1/MS-C1; else index-futures hedge) |

**Anti-zoo rule (inherited):** MACD, RSI, ROC, stochastics, moving-average crossovers are **parameter variants of past price inside a family**. Never new families. One composite per mechanism; incremental-value ablation.

**Grading: the tables report the E (evidence) dimension** (attached to the *source-faithful baseline*, not the neutralized production variant); **P (portability) and R (readiness) remain pending** and are populated in the research tracker at field-spec time. Provisional classification:

| Family | US E | CN E | Binding constraint |
|---|:--:|:--:|---|
| T-X1 Raw monthly price momentum | A | D | CN = benchmark, not a production presumption |
| T-X2 Residual momentum | A | B | CN priority candidate: *not yet "primary"* |
| T-X3 Short reversal | B | B | cost/capacity + long-only mapping binding |
| T-X4 Long reversal | B | B | supporting; conflicting CN replications → robustness |
| T-X5 Information discreteness | B | C | CN portability not established |
| T-X6 Volume conditioning | B | C | overlaps CN parent SPEC-HEAT/turnover |
| T-X7 52-week-high proximity | B | C | anchoring; distinct from return lookback |
| T-X8 Same-month seasonality | B | B raw / C risk-adj | own RG; cleared CN screen in raw returns, not after CH4 |

---

## 2. Families

### T-X1: Price momentum (US **A** · CN **D**; RG `PRICE_MOM`)
*(CN grade is **D**: broad weekly/monthly momentum is historically weak, matching the evidence line below; the `C`-graded **daily-horizon** momentum is a **separate deferred object** with its own ID/grade, not this row, the earlier "D/C" conflated the two.)*
**Source baseline (grade attaches here):** raw cumulative-return cross-sectional sort, skip most recent month (→ avoid 1-month reversal). **PRIMARY formation window = 12-1m (v1.7, canonical Jegadeesh–Titman): EXACT equation on THIS suite's formation clock (v1.10, timestamp and equation now consistent):** this child's convention is **signal computed through month-`t` close, held in month `t+1`** (§1). On that clock the momentum is `MOM_{12-1,t} = ∏_{k=1}^{11}(1 + r_{t−k}) − 1` (equivalently `Σ_{k=1}^{11} r^{log}_{t−k}`): the 11-month window **`t−11` through `t−1`, skipping the most-recent (formation) month `t`** (the skip avoids 1-month reversal). *(This equals the Kenneth-French `t−12…t−2` window under French's "formed at end of `t−1`, held in `t`" timestamp, same signal, shifted one month by the differing formation clock; the earlier v1.9 text mixed French's window with this suite's timestamp, which was the inconsistency.)* 6-1m and 9-1m (QEPM `ret9`) are named HORIZON robustness variants of this same equation, one momentum mechanism at different lookbacks, not separate factors. **Production adaptation (separate object, re-grade):** sector-/beta-/size-neutral rank. Note neutralizing removes the *industry* component of momentum (see Cross-references).
- US: the canonical cross-sectional factor; **crashes in volatile rebounds** (Daniel–Moskowitz momentum crashes) → dynamic scaling / vol-target as a later, pre-registered extension.
- **CN: broad weekly/monthly momentum is historically weak (E: D)**. benchmark, not a production signal; daily-horizon momentum is a *different* phenomenon (Deferred, below).
- Diagnostic (pre-register, not a new factor): **12-7 vs 6-2 sub-period return decomposition** to locate where continuation lives.

### T-X2: Residual momentum (US **A** · CN **B**; RG `RESID_MOM`)
**Exact Blitz–Huij–Martens specification (v1.1):**
$$RMOM_{i,t}=\frac{\sum_{s=t-12}^{t-2}\hat{\varepsilon}_{i,s}}{\sigma(\hat{\varepsilon}_{i,\,t-12:t-2})}$$
where $\hat{\varepsilon}$ are residuals from a **monthly Fama–French 3-factor regression estimated over the preceding 36 months**. Requires a complete 36m history; skips the latest month; **does not add estimated $\alpha$ to the signal**; test overlapping 1/3/6/12-month holds. More stable than total-return momentum ([Blitz–Huij–Martens](https://pure.eur.nl/ws/files/46882404/ResidualMomentum-2011.pdf)).
- **Robustness variants = separate named indicators, not "…":** CH3-residual, q-factor-residual, industry-augmented-residual (each a distinct object requiring its own grade). Industry factors are BHM's robustness extension, not the base spec.
- **QEPM `adjRet9` (= total 9-1 price momentum / residual vol) is NOT T-X2, one transformed-momentum comparator only:** T-X2's numerator is the *sum of factor-model residual returns* (factor exposure removed) whereas `adjRet9`'s numerator is *total* return merely *scaled* by residual vol (factor exposure NOT removed). T-X2 is the cleaner isolation of stock-specific continuation. **The `/residual-vol` denominator is OWNED BY StatRisk R-X1, pure reference, no restatement (single source of truth):** `adjRet9` uses **the current active primary R-X1 residual-vol estimate defined in StatRisk §R-X1** (this file deliberately does not repeat the FF3/CH3/window/min-obs numbers, so there is only one maintenance location). `adjRet9` reuses that single estimate and **must NOT create a second IVOL vote.**
- **CN, priority candidate, NOT yet "primary":** some China studies find strong residual momentum ([A-share anomaly study](https://www.sciencedirect.com/science/article/pii/S0927538X21001141)), but the conservative 469-anomaly replication finds 6m residual momentum only in the *full* sample; **post-2007 the significant past-return variables are mainly SUE and announcement returns (F5), not price momentum** ([Jansen–Swinkels–Zhou](https://pure.eur.nl/ws/portalfiles/portal/58642799/Anomalies_in_the_China_A_share_market.pdf), [Li et al.](https://ira.lib.polyu.edu.hk/bitstream/10397/115240/1/Li_Replicating_Digesting_Anomalies.pdf)). Grade B, prove incremental OOS before elevating.

### T-X3: Short-horizon reversal (US **B** · CN **B**; RG `REV_SHORT`)
**Two horizon sub-IDs, 1-week and 1-month reversal are DIFFERENT horizons (microstructure/turnover), not one row:** **`T-X3w`** = **1-week** prior-return reversal (higher-turnover, more bid-ask-bounce contaminated); **`T-X3m`** = **1-month** prior-return reversal (slower). Declared separately; do not average. **Within each, RAW short reversal is the declared PRIMARY; residual (risk-model-neutralized) short reversal is a named robustness variant** (residual reversal has US evidence but did not clearly improve conventional reversal in the cited CN study). **The raw-vs-residual primary is now fixed (raw); what remains open is the field contract, which SEPARATES two layers (do not lump them):** **(1) formation SIGNAL** = a **frozen split/dividend-adjusted total-return close-to-close series** (one declared adjusted-price source); **(2) TRADABILITY & EXECUTION** = raw prices + suspension/limit status, with the **first feasible open (or VWAP) defined separately** as the fill. Close-vs-VWAP is an *execution* choice, not a signal-construction field, mixing them would blend signal with simulated execution.
- **Gross evidence requires implementation validation** (softened from v1): T+1 is decisive for *daily* strategies but less so for a 1-month hold; the larger binding issues are **price-limit fills, suspensions, spreads, turnover/capacity, and the constrained single-name short leg** (legal-but-scarce 融券. Verify borrow or hedge via futures; see MS-I1). Model these before believing any spread.
- Separate the microstructure (bid-ask bounce) component from the behavioral one.

### T-X4: Long-horizon reversal (US **B** · CN **B**; RG `REV_LONG`)
**Formation window FROZEN: 60-13m prior return (primary), 36-13m as a named robustness variant** (was "36-13 or 60-13", pick one; 60-13 is the fuller De Bondt–Thaler long-term-reversal window). Reversal sign; overlaps VALUE (F1): **redundancy-test against value before standalone inclusion.** CN replications conflict → carry as robustness, not conviction.

### T-X5: Information discreteness / momentum path quality (US **B** · CN **C**; RG `MOM_PATH`)
$$ID=\operatorname{sign}(PRET)\times(\%\,\text{negative days}-\%\,\text{positive days})$$
Low ID = gradual/continuous information → stronger continuation, *conditional on formation return* ([Da–Gurun–Warachka](https://business.uq.edu.au/sites/default/files/events/files/mitch-warachka-paper.pdf)). **Therefore a sequential double-sort / interaction with T-X1/T-X2, never a standalone bullish score.** CN caution: **suspended days must not be counted as zero-return; illiquid zero-return days distort ID.**

### T-X6: Volume conditioning (US **B** · CN **C**; RG `MOM_FLOW`)
Primary variable = **average daily share turnover over the formation period; distinguish turnover *level* from turnover *change*.** Independent double-sort of momentum × turnover ([Lee–Swaminathan](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=92589)): "volume trend" is a different specification. **CN: overlaps the parent `SPEC-HEAT`/abnormal-turnover mechanism → mandatory cross-file ablation before inclusion.**

### T-X7, 52-week-high proximity (US **B** · CN **C**; RG `H52`: v1.1, main addition)
$$H52_{i,t}=\frac{P_{i,t}}{\max_{s\in[t-252,\,t]}P_{i,s}}$$
Anchoring / reference-price behavior: **not merely another return lookback** ([George–Hwang](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2004.00695.x)); already noted in [workspace momentum notes §2.6](../../Quant/Learning%20Notes/Momentum%20Factors%20and%20Strategies.md). **TWO MUTUALLY-EXCLUSIVE declared variants (not "and/or", this matches Combination's `T-X7a`/`T-X7b` role-variant split): `T-X7a`** = standalone x-sectional alpha, **`T-X7b`** = momentum-conditioning moderator. A product activates **exactly one**; resolve which by testing incremental value over T-X1 before activation.

### T-X8: Cross-sectional same-month seasonality (US **B** · CN **B raw / C risk-adjusted**; RG `SEASONAL`: v1.2, was orphaned)
Source-faithful ([Heston–Sadka](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/seasonality-in-the-cross-section-of-stock-returns-the-international-evidence/449422A711AB698236AD46F6BA7414D6)): rank stocks by same-calendar-month performance in prior years,
$$SEAS^{2\text{-}5}_{i,t}=\tfrac{1}{4}\left(r_{i,t-24}+r_{i,t-36}+r_{i,t-48}+r_{i,t-60}\right)$$
- **Own RG `SEASONAL`: NOT folded into `PRICE_MOM`** (neither momentum nor index-level calendar timing). Other-month (non-same-month) seasonal *reversal* is a **separately named variant**, not the same signal.
- **A-share evidence (precise):** in *Finding Anomalies in China* seasonality was the only past-return strategy clearing the ~2.85 multiple-testing hurdle **in value-weighted RAW returns (t≈2.93)**; the **CH4 alpha does not vanish, it is ≈0.89%/mo with t≈2.52, i.e. it simply does not clear the ~2.85 threshold** ([FAC](https://eng.pbcsf.tsinghua.edu.cn/dfiles/wp6.pdf)) → **B for raw cross-sectional evidence; C for incremental risk-adjusted alpha.**
- **Data contract:** signal formed at the **end of the preceding month for the coming calendar month**; execute first feasible session, 1-month hold; **min 60-month history**. **Missing-data (pick one, don't blend): source-faithful baseline requires ALL FOUR lagged months (keeps the ¼ denominator); a mean-of-available-with-≥3 version is a *separately named robustness variant*.** Delisting/suspension treatment declared.
- Falsification: control for size/industry and (critically) T-X1/T-X2 momentum. **Independence from momentum is an empirical result to TEST, not assumed**, Heston–Sadka support same-month *persistence*, not statistical independence. Test 2–5y / 2–10y / 2–20y lag windows without retrospective selection; VW-capped + EW.

### Cross-references (not owned here)
- **Earnings-event continuation (CAR/ABR, PEAD, SUE) → fundamental F5 `EARN_EVENT`.** Correlated with T-X1 but **potentially complementary, not simply "competing"**: joint ablation across `PRICE_MOM`+`RESID_MOM`+`EARN_EVENT` (momentum & surprise carry incremental info after mutual control, [Chan–Jegadeesh–Lakonishok](https://www.nber.org/papers/w5375)).
- **Industry momentum ownership (v1.1):** stage-2 sector-neutral ranking here *strips* the industry-momentum component; that component is **owned by the parent sector-rotation sleeve** ([Moskowitz–Grinblatt](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00146); workspace notes §2.5). Don't double-count or orphan it.
- **Same-calendar-month seasonality** → now **owned as T-X8 (`SEASONAL`)** above; kept isolated from `PRICE_MOM`.
- **Factor momentum** → factor-sleeve *allocation* layer, not stock ranking.
- **CN daily cross-sectional momentum / new-investor attention → Deferred (v1.1):** a distinct *daily* (not weekly/monthly) attention-driven, execution-sensitive phenomenon ([Daily Momentum and New Investors](https://www.nber.org/papers/w31839)); admit only as its own defined research family once an intraday/T+1 execution model exists.
- **Statistical-risk overlap (v1.1 note) → `Indicators_Pool_StatRisk_v1.md`:** T-X2 residual momentum divides cumulative residuals by residual volatility, so it shares a denominator with that child's IVOL: **test the correlation, don't double-count.** T-X3 short reversal is also a *mandatory control* for the IVOL anomaly (daily IVOL's negative relation is partly prior-month reversal). MAX/idiosyncratic-skewness there overlap T-X5 path-quality and T-X7 52-week-high, joint ablation across the lottery complex.

---

## 3. Overlap map & initial structure

```
PRICE_MOM (T-X1) ─ RESID_MOM (T-X2)   [common past-return input; RESID_MOM = factor-stripped. Test incremental info, pick/blend, don't double-count]
        │ correlated, potentially complementary with
EARN_EVENT (F5: CAR/SUE/revisions)     [joint ablation]
MOM ↔ REV_SHORT (T-X3)                 [different lag bands; 12-1 skip removes much mechanical overlap, but they can be CORRELATED in rebounds: NOT statistically orthogonal]
REV_LONG (T-X4) ↔ VALUE (F1)           [redundancy-test]
MOM_PATH (T-X5), MOM_FLOW (T-X6), H52 (T-X7) = conditioning overlays / interactions, not standalone votes
SEASONAL (T-X8) = own RG, distinct hypothesis, independence from momentum is an empirical result to TEST (control for T-X1/T-X2 before claiming a separate premium)
```

**Initial production candidates** (cost-gated, one composite per RG):
- **US:** RESID_MOM (or PRICE_MOM) conditioned by MOM_PATH; REV_SHORT only if it clears MS-I1 net-cost/fill stress; joint ablation with F5 EARN_EVENT.
- **CN:** RESID_MOM as the **priority research candidate** (not presumed primary, post-2007 evidence favors F5 SUE/CAR over price momentum); raw PRICE_MOM benchmark-only; REV_SHORT/REV_LONG as research with mandatory fill-feasibility.
- **Stage-2 (both markets):** T-X8 `SEASONAL` enters as a **stage-2 candidate** (own RG), tested for incremental value after momentum controls, not part of the first momentum composite but not orphaned either.

**Regime-gating is a secondary, pre-registered hypothesis, not the baseline.** Automatically switching momentum↔reversal on vol/dispersion is *an additional model with substantial overfitting risk*, the **ungated sleeves remain the baseline**, and every signal is reported **cost-net, unscaled and ungated** (parent discipline) before any gate is tested.

---

## Sources
[Blitz–Huij–Martens residual momentum (full spec)](https://pure.eur.nl/ws/files/46882404/ResidualMomentum-2011.pdf) · [George–Hwang 52-week high](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1540-6261.2004.00695.x) · [Da–Gurun–Warachka frog-in-the-pan](https://business.uq.edu.au/sites/default/files/events/files/mitch-warachka-paper.pdf) · [Lee–Swaminathan volume & momentum](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=92589) · [Moskowitz–Grinblatt industry momentum](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00146) · [Chan–Jegadeesh–Lakonishok momentum & surprise](https://www.nber.org/papers/w5375) · [Jansen–Swinkels–Zhou China anomalies](https://pure.eur.nl/ws/portalfiles/portal/58642799/Anomalies_in_the_China_A_share_market.pdf) · [Li et al. RDQ A-share replication](https://ira.lib.polyu.edu.hk/bitstream/10397/115240/1/Li_Replicating_Digesting_Anomalies.pdf) · [A-share anomaly study (residual momentum/reversal)](https://www.sciencedirect.com/science/article/pii/S0927538X21001141) · [Daniel–Hirshleifer–Sun 2020 (PEAD, for F5)](https://www.kentdaniel.net/papers/published/DHS_2019_04_08.pdf) · [Daily Momentum and New Investors (CN)](https://www.nber.org/papers/w31839) · parent files, `Indicators_Pool_Fundamental_v1.md`, `Indicators_Pool_MarketStructure_v1.md`, [Learning Notes/Momentum Factors and Strategies.md](../../Quant/Learning%20Notes/Momentum%20Factors%20and%20Strategies.md).

---

## Appendix: revision history

Kept for provenance. Nothing below is needed to read the contracts above.

**Change log v1.9→v1.10 (clock + reference fixes):** 12-1m equation now **consistent with THIS suite's formation clock** (signal through close `t`, held `t+1` → `MOM=∏_{k=1}^{11}(1+r_{t−k})−1`, window t−11…t−1, skip formation month `t`): the v1.9 text mixed French's t−12…t−2 window with this suite's timestamp; **`adjRet9` trimmed to a pure REFERENCE to StatRisk R-X1** (no restated definition → one maintenance location).

**Change log v1.8→v1.9 (single-source + exact-eqn):** `adjRet9` residual-vol now **REFERENCES StatRisk R-X1** (which owns the frozen contract) rather than redefining it here, numerator/denominator can't drift; **12-1m momentum given its exact equation** `MOM_{12-1,t}=∏_{k=2}^{12}(1+r_{t−k})−1` (window t−12…t−2, skip t−1), preventing a `t−12…t−1` vs `t−11…t−2` disagreement.

**Change log v1.7→v1.8 (adjRet9 pin):** `adjRet9` residual-vol denominator pinned to R-X1's *declared primary*: **US prior-month daily FF3-residual σ, A-share prior-month daily CH3-residual σ** (CH3 chosen; CH4 a variant), min-15-obs/OLS/NA-on-insufficient, no longer an open FF3/CH3 × 21/63/252d menu.

**Change log v1.6→v1.7 (QEPM closure):** T-X1 **primary formation window selected = 12-1m** (canonical J-T; 6-1m & 9-1m are named horizon robustness variants, resolves the previously-unselected 12-1-vs-6-1 primary); **`adjRet9`'s residual-vol denominator pinned to StatRisk R-X1** (declared FF3/CH3 model + window), reproducible and never a second IVOL vote.

**Change log v1.5→v1.6 (QEPM Ch.5 cross-map):** **`9-1m` momentum (QEPM `ret9`)** documented as a **horizon robustness variant** of T-X1 (12-1/6-1/9-1 = one mechanism, not a new factor); **QEPM `adjRet9` clarified as NOT T-X2** (total return scaled by residual vol, factor exposure not removed): a horse-race comparator only, and its `/residual-vol` must not create a **second IVOL vote** (owned by StatRisk R-X1).

**Change log v1.4→v1.5 (field-contract precision):** T-X3 field contract now **separates the formation SIGNAL (frozen adjusted total-return close-to-close) from TRADABILITY/EXECUTION (raw prices+status, first-feasible open/VWAP)**: close-vs-VWAP is an execution choice, not a signal-construction field.

**Change log v1.3→v1.4 (audit corrections):** **T-X1 CN grade fixed to D** (broad momentum; daily-horizon C is a separate deferred object, was conflated "D/C"); **T-X3 split into `T-X3w` (1-week) / `T-X3m` (1-month)**: different horizons/microstructure, not one row; **T-X4 formation frozen to 60-13m** (36-13m robustness): was "36-13 or 60-13"; **T-X7 made two mutually-exclusive variants `T-X7a` (alpha) / `T-X7b` (moderator)** matching Combination (was "and/or").

**Change log v1.2→v1.3 (Market Structure integration):** made `Indicators_Pool_MarketStructure_v1.md` §MS-I1 the single owner of stock-level capacity/cost/short-feasibility fields; retained only this child’s strategy-specific orders, turnover, urgency, holding period and break-even alpha; reconciled A-share shorting to *legal but inventory-scarce and security×broker×date-specific*, with unknown borrow treated as unavailable.

**Change log v1.1→v1.2 (coverage-gap review, steps 1–3 + audit):** removed the duplicated `PRICE_MOM ↔ RESID_MOM` overlap-map line; **added T-X8 cross-sectional same-month seasonality (`SEASONAL`, Heston–Sadka)**: owned family + RG. Audit-2: T-X8 missing-data rule made single (all-four baseline vs ≥3 named variant), CN evidence stated precisely (CH4 α≈0.89%/mo t≈2.52, doesn't clear ~2.85), T-X8 added as a stage-2 candidate; grading claim corrected to "E reported, P/R pending."

**Change log v1→v1.1 (momentum-precision review):** residual momentum given its exact Blitz–Huij–Martens specification (FF3 residuals, 36m window, standardized, 12-1 skip, no alpha), with CH3/q-factor/industry-augmented named as *separate* robustness variants; T-X1 split into source-faithful raw baseline vs production-neutralized adaptation (grade attaches to the baseline); strategy-definition + single-stock cost/borrow contract rows added (parent ETF costs don't apply); overlap-map "orthogonal" error fixed (opposite sign ≠ statistical independence); regime-gating demoted to a secondary pre-registered hypothesis (ungated baseline stays primary); grades split into E/P/R with a provisional evidence table; over-categorical "fiction/gut executability" wording softened to "gross evidence requires implementation validation"; T-X5/T-X6 given formulas; **new T-X7 52-week-high proximity (George–Hwang)**: the main substantive addition; industry-momentum ownership made explicit; China daily momentum promoted from orphan cross-ref to a defined Deferred item; 12-7-vs-6-2 and raw-vs-residual-reversal added as diagnostics. Cross-references [Learning Notes/Momentum Factors and Strategies.md](../../Quant/Learning%20Notes/Momentum%20Factors%20and%20Strategies.md).
