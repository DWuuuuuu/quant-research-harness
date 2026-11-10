# Statistical Risk & Return-Distribution Pool: US & A-Share, v1.5 (Child Contract)

**Parent files:** `Indicators_Pool_US_v2.md`, `Indicators_Pool_AShare_v2.md`. Siblings: `Indicators_Pool_Fundamental_v1.md`, `Indicators_Pool_TrendReversal_v1.md`, `Indicators_Pool_MarketStructure_v1.md`. This is the **cross-sectional statistical-moment / lottery-risk** child contract. It owns IVOL, residual/close-substitute holding risk (R-X7 `ARB-RISK`), lottery characteristics and defensive volatility; broader market-structure constraints live in the Market Structure child, which consumes StatRisk's `ARB-RISK` (IVOL + close-substitute risk).
**Origin:** idiosyncratic-risk research review. Core conclusion: **do NOT add `−IVOL` as one unconditional factor.** The evidence supports (a) a *conditional* lottery complex and (b) a *separate* defensive-volatility characteristic, two distinct product objects, not one symmetric alpha. *(The "arbitrage-friction" framing is narrowed in v1.2: IVOL is an arbitrage-holding **risk** consumed by the Market Structure child as `ARB-RISK`; the loan/IO/delay/crowding **constraints** are owned there, not here.)*

> **Two objects, kept apart:**
> 1. **Defensive characteristic** (portfolio construction / risk-sizing): long-horizon total vol; used regardless of whether any return-prediction hypothesis survives.
> 2. **Lottery / mispricing alpha hypothesis** (return prediction): residual vol, MAX, idiosyncratic skewness; conditional, fragile, avoid-screen-leaning.
> Never merge the two; they have different signs, horizons, and purposes.

---

## 1. Research Contract (deltas from sibling children)

Inherits PIT-universe, sector-relative scoring, FDR/holdout, long-only-first, and the **shared capacity/cost/feasibility infrastructure now owned by `Indicators_Pool_MarketStructure_v1.md` §MS-I1** (this child supplies only its strategy-specific application, order, side, turnover, horizon and urgency). **Turnover note (v1.1): the LOTTERY measures (IVOL/MAX/IDSKEW) are high-turnover monthly signals; the defensive measures (R-X2 total vol, R-X6 beta/correlation) are slower, lower-turnover characteristics. Do not apply one blanket turnover assumption.**

| Field | US | A-share |
|---|---|---|
| Universe | PIT index membership w/ delistings; **large/liquid tier** (microcaps drive the raw anomaly, HXZ 2020) | All-A ex IPO<6m, ST/*ST, suspended (entry-eligibility), bottom-liquidity; **Main-Board breakpoints** (raw all-market breakpoints inflate the effect) |
| Targets: alpha object (LOTTERY) | 21/63/252d forward return vs EW eligible universe | same |
| **Targets: defensive object (R-X2/R-X6, v1.1)** | **risk targets over declared horizons (next 21/63/252d):** future realized vol, realized portfolio beta, downside beta/downside capture, drawdown & expected shortfall, tracking error, turnover, and return-per-unit-realized-risk. A useful defensive signal must not be rejected for failing to predict raw return. | same |
| **Mandatory control order (v1)** | **(1) prior-month return FIRST** (short-reversal contamination, Huang et al. 2010), then size, price, liquidity, distress, momentum, value, profitability, MAX, skewness | same + suspension/T+1/limit-fill modeling |
| Weighting | report **VW-capped AND EW** (the sign/significance depends on it, Bali–Cakici) | same |
| Estimation windows | **LOTTERY measures only (IVOL/MAX/IDSKEW): 21 / 63 / 252d, compared without retrospectively selecting the winner.** Defensive measures use their own source windows (R-X2 1y/3y total vol; R-X6 1y vol × 5y correlation. See rows). | same |
| Cost/turnover (gating, v1.2) | call MS-I1 with this strategy’s order, side, turnover, holding period and urgency; LOTTERY measures are usually monthly/high-turnover, defensive measures slower | same + stamp duty, T+1, board/date limit and suspension fill-feasibility; single-name short only when security×broker×date borrow and cost are verified, otherwise long-only/underweight + index-futures hedge |

**Grading:** the tables report the **E** (evidence) dimension; **P (portability) and R (readiness) remain pending** and are populated in the research tracker at field-spec time. A-share E grades not inherited from US.

**Redundancy groups:** `LOTTERY` (residual/lottery alpha complex: IVOL/MAX/IDSKEW co-move) · `DEFENSIVE-VOL` (low-total-vol characteristic) · `SYS-DEFENSIVE` (systematic low-risk, market beta/correlation/downside beta; defensive-first) · `CF-STABILITY` (cash-flow volatility (owned by Fundamental F-stability, cross-ref only) · `SYS-RISK` (common-IVOL beta) systematic, risk-attribution) · `ARB-RISK` (close-substitute / arbitrage-holding risk: R-X7, consumed by Market Structure). *(v1.1 added SYS-DEFENSIVE; v1.2 added ARB-RISK/R-X7.)*

---

## 2. Families

### R-X1: Classic idiosyncratic volatility, IVOL-21 (US **E:C** · CN **E:C**; RG `LOTTERY`)
`r_{i,d}−r_f = α + β_M·MKT + β_S·SMB + β_H·HML + ε`; `IVOL = StdDev(ε), d ∈ prior calendar month (t−1)`.
**⚠ R-X1 is the SINGLE SOURCE OF TRUTH for residual volatility across the whole suite** (TrendReversal `adjRet9` and any other consumer *reference* this contract, they do not redefine it). **Frozen residual-vol contract:** **US primary = FF3-residual σ** (as above); **A-share primary = CH3-residual σ** (Liu–Stambaugh–Yuan 3-factor); **CH4 is a named robustness variant, NOT co-primary** (one primary per market). **Estimation = OLS on the prior calendar month's DAILY returns, minimum 15 valid daily observations** (else NA), residual σ = **sample standard deviation (n−1 denominator)** of `ε`. **R-X1 also owns the shared inputs this depends on (declared here, referenced elsewhere):** the **risk-free series** (`r_f`), the **factor-return provider & construction** (US = Ken French FF3; A-share = the declared CH3 construction/vendor), and the **minimum factor-history availability** before a monthly regression is admissible. Any downstream `/residual-vol` denominator uses exactly this object and these inputs.
- Hypothesis (if accepted): high IVOL → low next-month return → score `−rank(IVOL)`. **But the negative premium is NOT settled**: fragile to weighting/breakpoints/screens (Bali–Cakici); HXZ 2020 conservative replication ≈ −0.52%/mo, t≈−1.71 (fails their bar); 15/16 vol measures insignificant.
- **Best interpretation = conditional mispricing, not "vol is bad"** (Stambaugh–Yu–Yuan 2015): among *overpriced* names high IVOL → lower returns; among *underpriced* → higher; stronger when hard-to-short and when sentiment is high. → use as an **avoid-screen + interaction variable**, not a symmetric factor.
- **Realized ≠ expected** (Fu 2009 EGARCH gave a *positive* sign), but **Fu's positive result is largely look-ahead** (Guo–Kassa–Ferguson 2014: EGARCH used contemporaneous month-t returns). Expected-IVOL is a **separate research hypothesis with the opposite sign** → deferred; never silently combined with R-X1.

### R-X2: Long-horizon total volatility, TOTVOL-252 (US **defensive B** · CN **defensive B**; RG `DEFENSIVE-VOL`)
1y daily total-return vol; 36-month total vol as a separate practitioner-style variant.
- **This is a defensive portfolio-construction characteristic, not a lottery-alpha bet**: how S&P Low-Vol (≈1y total vol, inverse-vol weight, turnover buffers) and MSCI Min-Vol (total-variance optimization) actually work; Barra carries residual vol as a *risk* exposure, implying no stable negative return premium. Robeco reports a China low-vol effect on 36m total vol (in tension with conservative replication. Flag).
- Owned here for *sizing/defensive selection*; return-prediction claims stay in `LOTTERY`, not here.

### R-X3: Idiosyncratic skewness, IDSKEW-21 (US **E:C** · CN **E:C, priority > IVOL**; RG `LOTTERY`)
Skewness of prior-month factor-model residuals, a **REALIZED skew / lottery proxy** (it is *not* an expected-skewness estimate; it stands in for the expected-skewness premium below, and is much easier to audit than a forecast-skewness model). Label it realized throughout.
- Lottery-seeking investors pay up for positive expected skewness → more positive skew → lower return (Boyer–Mitton–Vorkink ≈1%/mo, but their expected-skew model is complex/model-dependent → use *realized* first).
- **A-share priority:** in *Finding Anomalies in China*, idiosyncratic & total skewness were the **only risk proxies clearing the raw multiple-testing screen**: prior-month CAPM-residual skew VW HML −0.67%/mo (t=−3.15), CH4 alpha −0.90%/mo (t=−2.78), *just below* the ~2.85 hurdle. → **rank IDSKEW above classic IVOL for A-shares** (still C, honest about the hurdle).

### R-X4: MAX lottery demand, MAX1 / MAX5 (US **E:C** · CN **E:C, limit-AWARE complex mandatory**; RG `LOTTERY`)
Max daily return in prior month (MAX1); average of 5 largest (MAX5, robustness). High MAX → underperformance.
- **MAX is likely the more fundamental driver than IVOL:** when both are included, IVOL's coefficient turns *positive*, MAX absorbs and reverses it (Bali–Cakici–Whitelaw). This is the concrete reason to prioritize MAX/skew over classic residual vol.
- **A-share: raw MAX is corrupted by ±limits**. a name closing at +10% masks latent demand vs another also at +10%. **Do NOT fabricate a "limit-adjusted MAX", the latent uncapped return is unobservable.** Instead use **separate auditable primitives**: raw MAX, limit-hit count, close-at-limit flag, lock duration, and turnover, and let the model combine them. Retail-attention driven. **Heavy overlap with parent `SPEC-HEAT`/CN-B3 limit-up complex → mandatory cross-file ablation; not another additive vote.**

### R-X5: Cash-flow volatility, CFVOL-16Q (US **E:C** · CN **E:C**; RG `CF-STABILITY`: owned by Fundamental)
Vol of CFO/sales or CF/book over ~16 quarters. Business-instability, *not* price instability; high CFvol → lower returns, and neither CFvol nor return-IVOL fully subsumes the other (Huang 2009).
- **Owned by Fundamental F-stability, cross-referenced here, not duplicated.** Ablate against existing ROE/earnings/margin/sales-variability; not another independent quality vote.

### R-X6: Systematic low-risk / defensive, SYS-DEFENSIVE (US **defensive B** · CN **C, replicated-with-weak-alpha**; RG `SYS-DEFENSIVE`: v1.1, was the named-but-unowned orphan)
**Executable baseline (source-faithful Frazzini–Pedersen):** `β_i = ρ_{i,m} · σ_i/σ_m`, with **σ from 1-year daily returns (≥120 daily obs minimum)** and **ρ from 5-year overlapping 3-day log returns (≥750 daily obs minimum)** (the 3-day overlap is the nonsynchronous-trading correction), then **shrink toward 1** (FP: `0.6·β̂ + 0.4·1`). Benchmark = cap-weighted market TR; rf = short T-bill/repo. Rebalance monthly, 1-month hold.
- **Three measures, separate signs & grades (v1.1):**
  | Measure | Def | Sign | US Gr | CN Gr |
  |---|---|---|---|---|
  | Market beta | FP β above | low-β `+` (defensive) | B (defensive) | C (replicated-weak) |
  | Market correlation | ρ_{i,m} (5y, 3-day) | low-ρ `+` | B (defensive) | C |
  | Downside beta | β estimated on days **market return < 0** (primary state; below-median = robustness variant) | low downside-β `+` | C | C |
- **Beta = vol × correlation, so R-X6 and R-X2 (total vol) require a MANDATORY joint horse race**: "evaluate separately" is insufficient to stop low-beta merely repackaging low total vol (see build sequence & overlap map).
- **Defensive-first, not a clean alpha:** Frazzini–Pedersen document a broad BAB effect, **but** much of it reflects profitability/investment exposure, beta-estimation choices, microcaps and costs (still positive after estimated costs) ([BAB](https://pages.stern.nyu.edu/~afrazzin/pdf/Betting%20Against%20Beta%20-%20Frazzini%20and%20Pedersen.pdf), [Betting Against Betting Against Beta](https://www.sciencedirect.com/science/article/pii/S0304405X21002051), [Betting Against Correlation](https://www.aqr.com/Insights/Research/Journal-Article/Betting-Against-Correlation-Testing-Theories-of-the-Low-Risk-Effect)). Primary use = **defensive selection + risk attribution**; symmetric alpha only after ablation vs profitability/investment.
- **Leveraged long-short BAB = a separate strategy contract** (financing & shorting are integral to the published portfolio, out of scope for this long-only child). For **A-shares, evaluate low-beta / low-correlation selection, not a literal BAB** unless every short has verified security×broker×date borrow under MS-I1/MS-C1.
- **CN grade note (v1.1 correction):** *Finding Anomalies in China* already tests daily beta, downside beta and FP beta, results are **weak for value-weighted portfolios and largely explained by the CH factors** → grade **C = "replicated with weak alpha evidence,"** not "unreplicated" ([FAC](https://eng.pbcsf.tsinghua.edu.cn/dfiles/wp6.pdf)).
- Keep strictly separate from `LOTTERY` (own-IVOL) and `SYS-RISK` (CIV-beta): three different objects.

### R-X7: Close-substitute / arbitrage-holding risk (`ARB-RISK`; US **E:B** · CN **E:C**; risk-attribution, not a lottery vote)
The holding risk an arbitrageur bears because a stock has no perfect hedge, Wurgler–Zhuravskaya: without close substitutes, residual risk stops arbitrageurs from flattening demand curves. Measures: residual (idiosyncratic) volatility as the baseline proxy (reuses R-X1, do not re-vote); **peer-hedge / close-substitute quality: ONE declared primary: the regression `residual volatility` of the stock on a matched peer basket** (high residual = poorly hedgeable = high `ARB-RISK`); the **`R²`-based version is a named robustness variant** (they are monotonically related but not identical, pick one primary, don't leave "`R²` / residual vol" ambiguous). **Peer-basket construction contract (reproducible):** peers = same **申万/GICS industry × size tercile × style bucket (value/growth)**; **no-self-inclusion**; **minimum breadth = 5 eligible peers**: **below that, `ARB-RISK` is `NA/insufficient-peers` (a MISSINGNESS flag, NOT an adverse "high-risk" score. Do not conflate thin coverage with poor hedgeability); route to the disclosure/uncertainty handling, never a fabricated high value**; **equal-weight** basket, **re-formed monthly** (PIT membership); regression on a **252-day** daily window ending t−1. **This is the `ARB-RISK` object the Market Structure child consumes** (its MS-C3 close-substitute reference resolves here). Owned here as holding *risk*, not a directional signal.
- **Note (v1.2):** the Market Structure child conditions its constraint interactions on this; per Stambaugh–Yu–Yuan the holding-cost channel is *symmetric* (amplifies mispricing both ways), unlike short-side borrow constraints.

### Adjacent-but-distinct (name explicitly to prevent conflation)
- **Common-IVOL beta (CIV-beta)**: sensitivity to market-wide common idiosyncratic vol (Herskovic et al.; low-CIV-beta quintile ≈ +5.4%/yr, labor-income-risk story). **Systematic risk, NOT own-IVOL** → `SYS-RISK`, later risk-attribution/regime use only; distinct again from R-X6 market beta.

---

## 3. Redundancy map & the "one complex" rule

```
LOTTERY complex (ONE mechanism, not 6 votes): IVOL(R-X1) ~ MAX(R-X4) ~ IDSKEW(R-X3) ~ low-price ~ high-turnover ~ retail-attention
   ├─ MAX flips IVOL sign when co-included → MAX/skew primary, IVOL secondary
   ├─ built ON TOP of prior-month return (R-X reversal control): evaluate only after T-X3
   ├─ denominator overlap with TrendReversal T-X2 (residual momentum ÷ residual vol) → test corr, don't double-count
   └─ CN MAX/limit-hit ⊂ parent SPEC-HEAT / CN-B3 → ablate cross-file
DEFENSIVE-VOL (R-X2) ↔ SYS-DEFENSIVE (R-X6): β = vol × correlation → MANDATORY joint horse race (does low-β add anything beyond low total-vol?); both separate from the lottery composite
CF-STABILITY (R-X5) ⊂ Fundamental F-stability → cross-ref, ablate, don't duplicate
SYS-DEFENSIVE (R-X6 market beta/corr) & SYS-RISK (CIV-beta) = two more systematic objects, separate from each other and from own-IVOL. Never merged
```

**Conditional use (the payoff):**
- IVOL/MAX/skew enter as an **interaction with the Piotroski–So expectation-error matrix**: high IVOL *strengthens* the avoid/underweight signal in the `low-B/M + low-F` (overpriced + weak) cell; does **not** auto-reject `high-B/M + high-F` names merely for elevated IVOL. Pre-registered test:
  `LOTTERY_penalty = LOTTERY_score × I(negative expectation error OR independent overpricing)`, and interacted with aggregate sentiment (stronger negative among overpriced when sentiment high: SYY).
- Around F5 `EARN_EVENT` (CAR/SUE): high IVOL **reduces confidence / position size**, it is **not** averaged with CAR as another earnings signal.

First production stance: **avoid-screen + interaction + risk-budget input**, not an independent symmetric long/short factor. Expected outcome, for A-shares IDSKEW and the **limit-aware lottery complex** (raw MAX + limit-hit/close-at-limit/lock-duration/turnover primitives, never a fabricated adjusted return) are the stronger return predictors; for both markets long-horizon vol is the more practical *defensive* characteristic.

---

## 4. Deferred (Grade D / research-only; do not code in the first pass)
| Item | Why |
|---|---|
| Expected IVOL (EGARCH/forecast) | Opposite-sign hypothesis; Fu 2009 positive result largely look-ahead (Guo–Kassa–Ferguson 2014): needs a clean out-of-sample forecast contract |
| IVOL shock (current − forecast/baseline) | Event/risk-deterioration signal; depends on a validated forecast first |
| Options-implied idiosyncratic vol | Licensed data (US); conflicting-sign evidence |
| Intraday realized skewness / jump decomposition | Unstable estimators; intraday-data contract |
| Extreme-value tail risk | Sign & estimator instability |

---

## 5. Build sequence
1. Data spine: daily returns + FF3/CH3/CH4 factor returns (for residuals), turnover, price and decision-time limit/suspension fields (CN); call Market Structure §MS-I1 for capacity/cost/fill/shortability rather than re-specifying it here.
2. Compute R-X1/R-X3/R-X4 with the **mandatory control order** (prior-month return first): single-mechanism backtests, VW-capped + EW, three windows.
3. Redundancy audit: corr vs T-X2 residual-vol denominator, T-X3 reversal, parent SPEC-HEAT (CN), Fundamental F-stability (CFVOL).
4. Conditional tests: Piotroski–So interaction, aggregate-sentiment interaction, CAR/SUE position-size modulation.
5. R-X2 (total vol) and R-X6 (`SYS-DEFENSIVE` beta/correlation) evaluated as defensive characteristics (sizing/selection + risk attribution), not in the lottery composite: **but via a MANDATORY joint R-X2↔R-X6 horse race** (β = vol × correlation, so decompose and test which carries the defensive benefit; "separately" alone is insufficient). R-X6 also ablated vs profitability/investment before any alpha claim.
6. Walk-forward w/ multiple-testing discipline; A-share fill-feasibility (limits/T+1/suspensions) and board×regime breaks.

## Sources
[Ang–Hodrick–Xing–Zhang US](https://doi.org/10.1111/j.1540-6261.2006.00836.x) · [AHXZ international](https://www.sciencedirect.com/science/article/pii/S0304405X08001542) · [Bali–Cakici 2008](https://ideas.repec.org/a/cup/jfinqa/v43y2008i01p29-58_00.html) · [Huang–Liu–Rhee–Zhang 2010](https://ideas.repec.org/a/oup/rfinst/v23y2010i1p147-168.html) · [Fu 2009](https://www.sciencedirect.com/science/article/abs/pii/S0304405X08001694) + Guo–Kassa–Ferguson 2014 look-ahead critique · [Hou–Xue–Zhang 2020 replication](https://academic.oup.com/rfs/article/33/5/2019/5236964) · [Stambaugh–Yu–Yuan 2015](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12286) · [Hou–Loh 2016](https://smusg.elsevierpure.com/en/publications/have-we-solved-the-idiosyncratic-volatility-puzzle/) · [Bali–Cakici–Whitelaw MAX](https://pages.stern.nyu.edu/~rwhitela/papers/max%20jfe11.pdf) · [Boyer–Mitton–Vorkink skewness](https://ideas.repec.org/a/oup/rfinst/v23y2010i1p169-202.html) · [Huang 2009 CF-vol](https://www.sciencedirect.com/science/article/abs/pii/S0927539809000036) · [Herskovic et al. CIV](https://www.gsb.stanford.edu/faculty-research/publications/common-factor-idiosyncratic-volatility-quantitative-asset-pricing) · [Gu–Kang–Xu China](https://www.sciencedirect.com/science/article/pii/S0378426615002277) · [Li et al. 2023 China replication](https://pubsonline.informs.org/doi/10.1287/mnsc.2023.4904) · [Finding Anomalies in China](https://eng.pbcsf.tsinghua.edu.cn/dfiles/wp6.pdf) · [China limit-adjusted MAX](https://www.sciencedirect.com/science/article/pii/S1059056021000149) · [S&P Low Volatility](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-low-volatility-indices.pdf) · [MSCI Min-Vol](https://www.msci.com/msci-minimum-volatility-indexes) · [Robeco China low-vol](https://www.robeco.com/en-int/insights/2021/05/the-low-volatility-effect-in-china) · parent files + sibling children.

---

## Appendix: revision history

Kept for provenance. Nothing below is needed to read the contracts above.

**Change log v1.4→v1.5 (R-X1 owns shared inputs):** R-X1 now also **owns the risk-free series, factor-return provider/construction, minimum factor-history, and the sample-SD (n−1) convention**: the full residual-vol dependency chain lives in one place; consumers reference, never restate.

**Change log v1.3→v1.4 (residual-vol single source of truth):** R-X1 now **OWNS the exact residual-volatility contract** for the whole suite: US primary FF3-residual σ, A-share primary **CH3** (CH4 a variant, not co-primary), prior-calendar-month daily, OLS, **min-15-obs else NA**; downstream consumers (TrendReversal `adjRet9`) reference it, never redefine it.

**Change log v1.2→v1.3 (audit corrections):** **R-X7 peer-basket now a reproducible contract** (industry×size-tercile×style peers, no-self-inclusion, min-5 breadth, equal-weight, monthly PIT re-form, 252d window, was a proposed proxy); **R-X3 idiosyncratic skew explicitly labelled a REALIZED skew/lottery proxy** (not an expected-skewness estimate).

**Change log v1.1→v1.2 (Market Structure integration):** narrowed scope to IVOL/holding risk, lottery characteristics and defensive risk; broader arbitrage constraints (loan supply, institutional ownership, price delay and crowding) now live in `Indicators_Pool_MarketStructure_v1.md`; **added R-X7 close-substitute / arbitrage-holding risk (`ARB-RISK`, Wurgler–Zhuravskaya) so the Market Structure child's close-substitute reference resolves to a real owner** (was dangling); replaced the duplicated single-stock cost/borrow prose with the shared MS-I1 contract; reconciled A-share single-name shorting to verified security×broker×date availability only.

**Change log v1→v1.1 (coverage-gap review, steps 1–3 + audit):** added **R-X6 systematic low-risk / defensive (`SYS-DEFENSIVE`)** with a full executable FP baseline (1y-vol × 5y-overlapping-3d-correlation, nonsynchronous correction, shrinkage; separate signs/grades for beta/correlation/downside beta); added **risk targets** for the defensive objects (R-X2/R-X6) and a **mandatory R-X2↔R-X6 horse race** (β = vol × corr); corrected CN grade to "replicated with weak alpha" (FAC tests FP/downside beta); leveraged BAB flagged as a separate financing/shorting contract; kept distinct from `LOTTERY` and `SYS-RISK`. **Audit-2:** R-X6 given 120/750-obs minimums, a per-measure sign/grade table, one primary downside-beta state (market<0); estimation-window row restricted to LOTTERY measures; R-X2↔R-X6 horse race added to build sequence + overlap map; risk-target horizons declared; "high-turnover" qualified to lottery only; grading claim corrected to "E reported, P/R pending."
