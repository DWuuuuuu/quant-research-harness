# Market Structure & Arbitrage Constraints Pool: US & A-Share, v1.3 (Child Contract)

**v1.0 formalization (Jul 2026):** consolidates the previously deferred `LIQUIDITY-CAPACITY / DISAGREE-CONSTRAINT / INFORMED-POS-X / FLOW-PRESSURE` batch into one child; distinguishes directional mispricing, arbitrage constraints, implementation cost, and crowding; makes §MS-I1 the single owner of stock-level capacity/cost/feasibility fields; adds point-in-time event and ownership contracts, source-faithful price delay, sign-asymmetric use rules, provisional E/P/R grades, and explicit falsification gates. No strategy is implemented by this document.

**v1.0 review fixes:** (1) sign-asymmetry rule split by constraint type, short-side/borrow constraints are one-sided, but the holding-cost/IVOL channel (StatRisk `ARB-RISK`) is *symmetric* (Stambaugh–Yu–Yuan: high holding cost raises an underpriced long's expected return too); (2) close-substitute/`ARB-RISK` reference now resolves to StatRisk R-X7 (was dangling); (3) `CanShort=unknown` = not-shortable in production but *missing/coverage-flagged* in the research sample (avoid short-universe bias); (4) D1 R²-zero wording corrected (ordinary R² ∈ [0,1]).

**Parent files:** `Indicators_Pool_US_v2.md`, `Indicators_Pool_AShare_v2.md`. Siblings: `Indicators_Pool_Fundamental_v1.md`, `Indicators_Pool_TrendReversal_v1.md`, `Indicators_Pool_StatRisk_v1.md`.
**Scope/status:** cross-sectional limits-to-arbitrage / capacity / crowding child. Phase 0 architecture and Phase 1 **field contract** are specified; implementation remains pending. MS-C1–C4 and MS-R1 are research tiers, not approved production alpha.

> **“Cost of arbitrage” is not one signed factor.** Keep four objects separate:
>
> | Object | Question | Product use | Sign |
> |---|---|---|---|
> | Mispricing signal | over- or underpriced? | directional alpha | owned by another child |
> | Arbitrage constraint | how hard/slow is correction? | moderator, horizon and confidence | conditional |
> | Implementation cost | can *our* strategy capture the edge net? | trade/capacity/shortability gate | always reduces realizable edge |
> | Crowding / flow fragility | could common owners be forced to trade? | risk and position-limit overlay | not a mean-return vote |
>
> **Sign asymmetry is mandatory, but it depends on the constraint TYPE.**
> - **Short-side / borrow constraints (MS-C1 loan cost, shortability):** genuinely asymmetric, but **separate the *belief* from the *implementable weight*** (they move in opposite directions here). For an **overpriced/avoid** signal a binding short constraint **raises the *prior/confidence* that overpricing persists** (pessimists can't trade it away), yet it **simultaneously *reduces* the size and reliability of the executable short** (you can't borrow it). So: `mispricing prior/confidence ≠ implementable short weight`. The constraint strengthens the *conviction* the name is overpriced while *shrinking* what you can actually short, the later cost/feasibility sections (MS-I1) enforce the weight side; do not read "strengthens the short" as "trade a bigger short." For an **underpriced long** a borrow constraint does **not** magnify the long, it only implies slower convergence, longer holding, lower confidence and/or smaller sizing.
> - **Holding-cost / IVOL constraints (consumed from StatRisk as `ARB-RISK`):** **symmetric, not one-sided.** Stambaugh–Yu–Yuan show high arbitrage-holding cost amplifies mispricing in *both* directions, among **underpriced** names high IVOL predicts *higher* forward returns (arbitrageurs were kept from bidding it up, and it corrects). So a binding holding-cost constraint on an underpriced long can **raise** its expected return; do **not** apply the "never magnifies a long" rule to this channel.
> In all cases implementation cost is deducted and feasibility can veto the trade.

The conceptual sequence is therefore:

`directional signal → constraint-conditioned confidence/horizon → expected net alpha → position subject to capacity, shortability and crowding limits`.

Never publish one blended `CostOfArbitrageScore`, and never let a constraint create direction where no independent mispricing signal exists.

---

## 1. Research, output and boundary contract

### 1.1 Output objects

Start with a **vector of interpretable subscores**, not an equal-weight omnibus:

1. **Constraint vector:** `ShortConstraint`, `OwnershipBreadth`, `InfoDelay`, `Disagreement`.
2. **Capacity vector:** expected one-way/round-trip cost in bps, fill probability, days-to-liquidate, maximum tradable notional, and `CanShort`.
3. **Crowding vector:** owner concentration/overlap, flow sensitivity, stressed exit-demand/ADV and loan-supply concentration.

The product-facing names below are allowed only after the underlying components have survived ablation and out-of-sample tests:

- **`ArbConstraintScore`**: high = correction is harder/slower. It is a moderator, not standalone alpha, and must be read conditional on parent funding state (US SOFR/repo; China R007/DR007/NCD).
- **`CapacityScore`**: high = easier/cheaper for the specified strategy and order to trade. A stock has no strategy-independent “true capacity,” so the score must retain the order, side, urgency and horizon that generated it.
- **`CrowdingFragilityScore`**: high = greater exposure to common-owner/forced-flow shocks. It is a risk overlay, not “high crowding = sell”; fire-sale exposure can carry a positive risk premium.

Optional diagnostics: `BadNewsPersistence`, price-delay D1, analyst dispersion, public short-demand proxies and ownership breadth. Do not relabel them as borrow cost or realizable alpha.

### 1.2 Point-in-time cross-sectional contract

| Field | US default | A-share default |
|---|---|---|
| Universe | PIT R1000/R3000-style liquid universe with delistings; microcaps reported separately | All-A ex IPO<6m, ST/*ST, bottom-liquidity; suspension/limit state is **entry feasibility**, not an ex-post universe deletion |
| Signal timestamp | exact exchange/vendor/filing publication timestamp; 13F joins on EDGAR filing/amendment time, not quarter-end; loan fields use the broker/vendor snapshot available then | exact exchange/vendor/report timestamp; ownership and analyst data join on actual publication/snapshot time, not report period-end |
| First execution | next tradable open after information was public; an intraday timestamp may use a later intraday entry only when intraday data and the rule are pre-specified | same, subject to T+1 and board/date limit rules; if only daily data exist, an intraday or after-close event first trades next open |
| Refresh/rebalance | MS-I1 daily; loan/news event-driven; ownership monthly score using latest filed data; price delay annual source baseline | MS-I1 daily; shortability security×broker×date; ownership/coverage on each source’s actual refresh; price delay annual source baseline |
| Return targets | conditional abnormal return/convergence at 5/21/63/126/252d; event tests begin after executable entry | same, with board/industry benchmark and fill-feasible entry |
| Non-return targets | realized spread/shortfall, fill/no-fill, days-to-liquidate, future liquidity/volatility/drawdown and stressed exit-demand/ADV | same + limit-lock/suspension fill outcome and T+1-constrained exit |
| Benchmark/controls | eligible-universe EW and VW-capped returns; factor/industry residuals; size, price, liquidity, prior return, value, profitability, distress and source coverage | eligible-universe EW and VW-capped; 申万 industry/board controls; same characteristic controls + policy/regime dates |
| Portfolio use | long-only/underweight first; verified-borrow L/S is a separate contract | long-only/underweight default; single-name short only when security×broker×date borrow and cost are verified; otherwise index-futures hedge |
| Missingness | unavailable ≠ zero; publish coverage by date, size, sector and signal bucket | same; `CanShort=unknown` maps to **not shortable in *production***, but in the historical research sample `unknown` is **missing/coverage-flagged, NOT forced-unavailable** (forcing it would bias the historical short universe toward only-verifiable names) |
| Evaluation | nested walk-forward, locked holdout, HAC/block-bootstrap for overlapping targets, FDR ledger, raw and residualized variants reported separately, cost/fill stress and component ablation | same + board×regulatory-regime results; no pooled pre/post-rule coefficient without a dated stability test |

**Standardization discipline:** retain economically meaningful raw units first. Cross-sectional ranks/z-scores are formed within market and date; industry/size residualization is a separately graded production variant, not silently baked into the source measure. Coverage and missingness indicators cannot become accidental alpha.

### 1.3 Ownership boundaries

- Raw news tone → parent `NEWS` (US-S10a/b) or Fundamental F5/F8. This child owns only **news × constraint** interactions.
- Short interest as bearish demand → parent `INFORMED-POS` (US-S9). This child owns loan-market cost/supply and feasibility. Short **volume** is not short **interest**, and neither is borrow cost.
- IVOL / residual holding risk / close-substitute risk → StatRisk **R-X7 `ARB-RISK`** (now a real owner, was a dangling reference before StatRisk v1.2). Consume it; do not create another IVOL vote. **Note the sign asymmetry above:** this holding-cost channel is *symmetric* (SYY), unlike the short-side constraints this child owns.
- Aggregate funding state → parent risk layers. Condition on it; do not duplicate it.
- Directional value, quality, event, momentum and reversal signals remain in Fundamental or TrendReversal. Market Structure can moderate or veto them but cannot originate their sign.

### 1.4 Evidence, portability and readiness

`E` = published/replicated evidence for the claimed role; `P` = portability from the source market/sample to this platform; `R` = point-in-time data and implementation readiness. These are provisional research grades, not backtest results.

| Module | Intended role | US E | CN E | P | R | Binding issue |
|---|---|:--:|:--:|:--:|:--:|---|
| MS-I1 capacity/feasibility | infrastructure/gate, not alpha | n/a | n/a | A | B/C | quote/impact calibration; CN fill and borrow history |
| MS-C1 loan/short constraints | moderator + shortability gate | B | gate only | C | D US / C CN | US useful fields licensed; CN policy non-stationarity and broker inventory |
| MS-C2 institutional ownership | heterogeneous moderator/supply/crowding input | B | C | C | C/D | filing lag, owner classification, denominator and double-count audit |
| MS-C3 delay/disagreement | information-friction moderator | B | C | C | B/C | noisy delay estimates; analyst coverage selection/PIT history |
| MS-C4 news × constraint | event interaction | B research | C/D | C | D | timestamped archive, entity/event NLP, client short-flow/loan data |
| MS-R1 crowding/fragility | risk/capacity overlay | B | C | C | D | holdings×flow history and common-ownership reconstruction |

**Data tiers:** `PUBLIC` / `VENDOR` (licensed but standard) / `LICENSED` (proprietary loan/news/flow) / `DEFERRED` (unavailable or regime-non-stationary). A public proxy cannot inherit the evidence grade of the licensed source variable.

**Regulatory-date contract:** every rule-dependent field stores `{rule, effective_date, verified_on, official_source, next_verification, historical_snapshot, join_by_effective_date}`. Dates are mutable. As verified in Jul 2026, US Rule 13f-2/Form SHO relief runs to **2028-01-02**, while FINRA SLATE implementation is listed for **2028-09-28**; both must be rechecked at build time ([SEC order](https://www.sec.gov/file/34-104303), [FINRA SLATE](https://www.finra.org/filing-reporting/slate)). CSRC/exchange short rules are actively managed. The durable conclusion is that current public data do not substitute for broker-level availability and loan cost.

---

## 2. MS-I1: Common capacity, cost and feasibility infrastructure

**Phase 1 field contract; implement first. This is infrastructure, not an alpha family.** MS-I1 owns the shared stock-level field dictionary and cost/feasibility estimators. Each strategy child owns the intended order, target participation, turnover, holding period, urgency, realized implementation and break-even alpha.

| ID | Field | Definition | Tier | Point-in-time / use rule |
|---|---|---|---|---|
| I1-a | Dollar ADV | median daily traded value over trailing 20/60 valid sessions | PUBLIC | use only sessions observable at decision time; retain currency |
| I1-b | Free-float market cap | PIT free-float shares × **raw** close | PUBLIC/VENDOR | audit split/float histories; stale/current float substitutions are not allowed |
| I1-c | Amihud illiquidity | `mean_d(abs(r_d) / DollarVolume_d)` over trailing 21/63 valid sessions | PUBLIC | store scale/units; proxy, not execution cost; suspended/non-trading days are missing/exposure flags, never zero cost |
| I1-d | Turnover/staleness | share volume / PIT free-float shares; counts of no-trade, zero-volume and stale-price days kept separately | PUBLIC/VENDOR | denominator changes must be PIT; zero return with volume is not the same as no trade |
| I1-e | Quoted/effective spread | quoted `(ask−bid)/mid`; effective `2×abs(trade−mid_at_trade)/mid_at_trade` | VENDOR/TAQ | time-weight/volume-weight method fixed before testing; daily OHLC proxies stay separately labelled |
| I1-f | Price impact | Kyle-λ from return on signed order flow where valid direction data exist | LICENSED | if unavailable, Amihud/daily impact proxies remain separate and are not called Kyle-λ |
| I1-g | Participation | proposed **dollar** order / dollar ADV | strategy + PUBLIC | side and participation schedule supplied by strategy child |
| I1-h | Days-to-liquidate | absolute dollar position / (`participation_cap × dollar ADV`) | strategy + PUBLIC | same currency/units; report stressed ADV as well as normal ADV |
| I1-i | A-share fill state | current known suspension/limit-lock/order-book state **plus** an ex-ante probability of future no-fill using only decision-time features | PUBLIC/VENDOR | current lock can gate an order; a future close’s realized lock/no-fill is an outcome, never a signal input |
| I1-j | Common cost contract | expected explicit fees/tax + spread + impact + delay/no-fill opportunity cost + funding/borrow/dividend cost | mixed | conditions on market, security, date/time, side, order size, execution style, urgency, holding days and broker |
| I1-k | Short feasibility | US: broker/vendor locate/availability, fee and recall; public eligibility/option/threshold flags are diagnostics only. CN: exchange eligibility **and** broker inventory/cost | PUBLIC + LICENSED | `verified-available / unavailable / unknown`; unknown is unavailable for production |
| I1-l | Realized-cost validation | implementation shortfall, realized fill rate, slippage vs arrival/decision price and realized holding/borrow cost | INTERNAL | calibrate on true orders or a separately labelled external execution sample; avoid self-selection bias |

The cost contract must expose at least:

`ExpectedNetAlpha = GrossConditionalAlpha − EntryCost − ExitCost − Taxes/Fees − Funding/Borrow/DividendCost − ExpectedNoFillOrDelayCost`.

Report expected cost in bps and currency, expected fill probability, days-to-liquidate and maximum notional under a declared participation/stress rule. Do not collapse them to `CapacityScore` until the mapping is calibrated out of sample. Long and short legs require different cost paths; A-share stamp duty applies on sells and T+1 constrains exits.

**Acceptance test:** gross evidence is not implementation evidence. MS-I1 is accepted only if predicted cost/fill buckets order realized implementation shortfall and fill outcomes out of sample, calibration error is reported by market/size/liquidity/side, and the candidate signal survives realistic and stressed cost scenarios.

---

## 3. Constraint and crowding modules

### MS-C1: Short-sale and stock-loan constraints (US **E:B licensed** · CN **feasibility gate**)

The economic object is a **joint quantity-and-price loan market** (D’Avolio): borrow fee alone misses rationing, while short interest alone misses supply and price.

- **US licensed tier:** annualized fee/rebate; lendable/float; on-loan/float; utilization (`on-loan/lendable`); security×broker×date locate/availability; supply concentration; fee volatility; recall occurrence/probability and time-to-restore; options-implied synthetic-short cost.
- **US public fallback:** short interest/float and days-to-cover (`SI/ADV`); `high short demand × low institutional ownership` (Asquith–Pathak–Ritter, strong equal-weight and much weaker value-weight); threshold/FTD diagnostics. Public FINRA short interest is twice monthly and joins on its publication schedule. These are weaker objects, not replacements for loan cost.
- **China v1 decision:** MS-C1 is a production **feasibility gate, not a stationary return factor**. `CanShort_{i,t}` defaults to unavailable unless security×broker×date inventory and cost are verified. The 2024 suspension concerned 转融券/refinancing; ordinary 融券 remains legal but scarce. Exchange balances or an eligible list do not prove inventory ([CSRC](https://www.csrc.gov.cn/csrc/c100028/c7493852/content.shtml), [SSE eligible list](https://www.sse.com.cn/lawandrules/sselawsrules2025/trade/specific/margin/c/c_20260710_10825136.shtml)). Historical access changes may be studied only as separately labelled, regime-dated natural experiments.

**Use rule:** test `Overpricing × ShortConstraint` as the primary return interaction. For a positive underpricing signal, high short constraint/illiquidity reduces size or extends the convergence horizon; it does not mechanically strengthen the long. No unconditional `−ShortConstraint` factor.

### MS-C2: Institutional ownership and arbitrage capital (US **E:B moderator** · CN **E:C heterogeneous**)

**Never use `−InstitutionalOwnership`.** Institutional ownership can supply information production, securities lending, price-insensitive index demand, or correlated forced selling. Preserve at least:

- `ACTIVE_IO`: potential information production/arbitrage capital.
- `PASSIVE_IO` and `PASSIVE_LENDABLE_IO`: weak price-correcting demand but an important, often stable source of lendable shares; not assumed to be the “strongest” in every name.
- `NONLENDING_STRATEGIC_IO`: controlling, policy or strategic holdings that are not freely deployable arbitrage capital.
- `IO_BREADTH`, `ΔIO_BREADTH`, `IO_CONCENTRATION` (HHI/top-5), and `IO_FLOW_FRAGILITY`.
- `RESIDUAL_ACTIVE_IO`: residualize active IO on size, price, liquidity, index membership and free float; passive share remains separate.

**Mechanism map:** low ownership/breadth can imply weak information production and short supply (Nagel; Chen–Hong–Stein); diversified ownership can improve efficiency and lending (Boehmer–Kelley); concentrated or flow-sensitive ownership routes to MS-R1 (Greenwood–Thesmar). These mechanisms have different signs and must be tested separately.

**US PIT contract:** public 13F covers qualifying institutional investment managers’ long holdings in Section 13(f) securities and can arrive up to 45 days after quarter-end. Join each original/amended filing on its EDGAR timestamp; filter the security class; resolve sole/shared discretion and manager hierarchies; retain amendments/confidential-treatment effects; use PIT free float in the denominator; do not infer short positions, lending or active/passive status directly from a raw 13F percentage ([SEC 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f)). Active/passive/lendable classification is a separate vendor/research layer.

**China PIT contract:** retain public mutual fund, insurance/社保, QFII, broker-AM, trust/private, national-team/policy and controlling/strategic categories separately; denominator = PIT free-float A-shares. Disclosure coverage is **source-specific**, not simply “quarterly”: public-fund reports are quarterly, interim and annual, with report/template-dependent holding detail; historically quarterly reports expose top holdings while fuller portfolios arrive in interim/annual reports. Listed-company top-shareholder tables are a different sample. Join on actual publication, preserve each source’s coverage flag, and audit the applicable post-2026 CSRC format before implementation ([CSRC periodic-report format](https://www.csrc.gov.cn/csrc/c101954/c7619929/7619929/files/6597e7afd35843e1a6ec023ea547d126.pdf)). National-team and controlling shares are not presumed lendable arbitrage capital.

### MS-C3: Information diffusion and disagreement (US **E:B** · CN **E:C / coverage-biased**)

**Analyst information set:** active analyst count; abnormal coverage residualized on size/industry; stale-consensus age; recommendation/target/revision disagreement; and current-fiscal-year EPS forecast dispersion. Source-faithful DMS dispersion is:

`DISP_{i,t} = Std(EPS forecasts_{i,t}) / abs(Mean(EPS forecasts_{i,t}))`, requiring at least two active forecasts and using information available by month-end `t−1` for month `t`. Source-replication convention: exact-zero consensus receives the highest dispersion rank; the continuous raw ratio is monthly ranked and winsorized at fixed 1st/99th percentiles before modeling so near-zero denominators cannot dominate. A price-scaled dispersion measure is a separately named robustness variant, never tuned retrospectively. High dispersion is disagreement/uncertainty (not a direct trading cost) and its negative-return interpretation is conditional on pessimists being constrained.

**Source-faithful Hou–Moskowitz price delay:** at each end-June date, use prior-year Wednesday-to-Wednesday weekly returns and estimate

`r_{i,w} = α_i + β_i r_{m,w} + Σ_{n=1}^{4} δ_{i,−n} r_{m,w−n} + ε_{i,w}`.

Using **ordinary, not adjusted, R²**:

`D1_i = 1 − R²_restricted(δ_{−1}=...=δ_{−4}=0) / R²_unrestricted`.

Higher D1 means more variation is captured by lagged market returns. Require a declared valid-week minimum (v1 implementation default: ≥40); ordinary R² is bounded [0,1], so set D1 missing when unrestricted R² = 0 (degenerate), and flag `0<R²<0.01` as low-information and ineligible for an aggregate score while retaining it for coverage diagnostics. D2/D3, added industry returns, more lags, or a rolling-monthly update are separately named robustness/deployment variants, not parameters selected after seeing returns. The annual D1 baseline trades from July and is at least one month removed from most estimation returns ([Hou–Moskowitz full paper](https://www.ruf.rice.edu/~jgsfss/moskowitz.pdf)).

Price delay and analyst coverage are strongly related to size/liquidity; report raw and residualized measures and test whether either adds to those controls. Close-substitute/peer-hedge quality is consumed from StatRisk `ARB-RISK` rather than duplicated.

**Sign/use caution:** Hou–Moskowitz document a positive premium among highly delayed, neglected stocks and stronger PEAD with delay. D1 therefore measures slow incorporation; it is not an unconditional “high constraint = low return” factor. Use it to condition convergence horizon/event drift and test its incremental return sign separately from the short-constraint/overpricing mechanism.

### MS-C4: Negative news × constraint interactions (US **E:B research** · CN **E:C/D**)

Raw tone remains owned by `NEWS` / Fundamental F5/F8. This module pre-registers only two primary interactions; both enter the shared FDR ledger:

1. **`NEG_NEWS × ABNORMAL_CLIENT_SHORT_ACTIVITY`**: informed processing of public bad news (Engelberg–Reed–Ringgenberg). This is short activity/flow, not loan cost; licensed.
2. **`NEG_NEWS × LOW_COVERAGE`**: slower diffusion among poorly covered firms (Hong–Lim–Stein); vendor/public with coverage-bias controls.

Only if the primaries survive may `NEG_NEWS × BORROW_CONSTRAINT` be tested. The triple `NEG_NEWS × DISAGREEMENT × SHORT_CONSTRAINT` remains deferred.

**Event contract:** retain first public timestamp, source/credibility, entity relevance, duplicate/story-cluster ID, novelty vs prior stories, event class and finance-specific abnormal tone. If published after close, trade next open; if intraday but the study has only daily data, also trade next open. Define event-time abnormal reaction separately from future drift: immediate `[0,1]` or executable-entry reaction; then 5/21/63d abnormal returns beginning after entry. Do not use a full-day tone file to trade at that day’s open. Deduplicate syndicated stories and keep earnings/filing events distinct from general media. Generic word lists are not acceptable without a finance-specific validation (Loughran–McDonald).

The alternative Tetlock-style hypothesis (media pessimism causes temporary pressure and reversion) is a different sign/mechanism and must be a separately named test, not silently combined with bad-news persistence.

### MS-R1: Crowding and flow fragility (US **E:B risk overlay** · CN **E:C research**)

Candidate fields: ownership HHI; pairwise/common-owner overlap; flow-sensitive-fund share; owner systematic flow beta; passive/ETF share; short-horizon/high-turnover-institution share; factor-exposure crowding; aggregate position × days-to-liquidate; stressed exit-demand/ADV; securities-lending supply concentration; and return/liquidity sensitivity to mutual-fund outflows.

The outcome is **forced-sale vulnerability**, not a signed expected-return factor. Primary targets are next-period liquidity deterioration, volatility/drawdown, covariance spikes and realized outflow sensitivity. A positive fire-sale risk premium is a separate asset-pricing hypothesis and cannot be averaged with the risk overlay. Data tier: chiefly LICENSED holdings×flows.

### MS-R2–R11: Crowding / leverage / forced-flow subfamily (owner contract, v1.2)

**Status: registered research outline, not approved production.** Implementation cards (formulas, readiness, dependencies) are in `INDICATORS_REFERENCE.md` §9b. **Every output is a risk-state/conditioner. Never a signed alpha.** The three summary states these feed (`StructuralVulnerability`/`ForcedFlowPressure`/`LiquidityAbsorption`) are **not yet consumed by Combination/PortfolioRisk**: wiring them is an open task.

**One primary validation target per family (v1.2 correction): the earlier table listed 2–3 co-equal targets per row, violating the register's one-primary-target discipline.** Each family now has exactly one primary, measurable, falsifiable target; everything else is an explicitly labelled secondary diagnostic that rides along but does not itself gate promotion.

| ID(s) | Object | **Primary target (the ONE thing that promotes/demotes it)** | Secondary diagnostics (ride-along, not gating) | Sign use | RG | Status |
|---|---|---|---|---|---|---|
| MS-R2a/b | CoMomentum (winner/loser, separate) | **subsequent momentum-factor tail-loss event** (factor drawdown beyond a declared threshold within a declared horizon) | forward mean return; factor vol; skew | high = **cut** momentum budget | `CROWD-COMOM` | anchor; `S:C`, specify first |
| MS-R3a1/a2/b/c/d | Momentum×theme concentration | **factor-return R² on the theme basket** (`MS-R3d`) | leg cosine (a1/a2); sector-HHI (b/c) | high = concentration cap | `CROWD-THEME` | registered |
| MS-R4a/b | Holdings commonality / GT-fragility | **outflow-driven covariance spike** (realized, not the level) | overlap level; fragility level | high = fragility overlay | `CROWD-HOLD` | `S:O`, licensed holdings×flow |
| MS-R5 | Days-to-liquidate (external proxy, disclosed positions only) | **stressed exit capacity given a declared participation rate** | n/a | high = position/soft cap | `CROWD-EXIT` | **boundary: MarketStructure defines the primitive (formula, ADV source, participation-rate convention) for any EXTERNALLY-DISCLOSED position; PortfolioRisk owns the computed state for THIS book's own weights: MS-R5 never reads own-book weights** |
| MS-R6a/b-US/b-CN/c-own/c-mkt | Forced-flow: mechanical sell pressure | **realized next-session mechanical sell volume vs the estimate** (validates the estimator, not a level threshold) | rebalance-pressure level; trigger distance | high = accelerated de-risk | `LEV-FORCED-US` | registered; timing-diagnostic. **`c-own` boundary: MarketStructure defines the vol-target deleveraging FORMULA; PortfolioRisk owns its evaluation on this book's own AUM/weights: MS-R6c-own never reads own-book state here.** |
| MS-R7a1/a2/b1/b2 | CN leverage **vulnerability** (两融/质押) | **subsequent margin-call or pledge-liquidation event rate** (NOT a return target: this family predicts liquidation, not price) | level; acceleration | high = gradual cap | `LEV-VULN-CN` | cross-ref CN-N2/CN-N5 |
| MS-R7c | CN forced-sale **events** | **observed liquidation supply volume** | n/a | high = de-risk | `LEV-FORCED-CN` | `S:O`, needs event data |
| MS-R8a/a-agg/b/c/d1/d2 | Liquidity absorption | **realized bid-ask/impact deterioration in the stress window** (the direct "did MMs withdraw" test: `d1`/`d2` when licensed, else the public proxies are diagnostics of it, not replacements) | Amihud level (a/a-agg); Corwin-Schultz (b); reversal (c) | deterioration = execution restriction | `LIQ-ABSORB` | R8a=X-ILLIQ; d1/d2 licensed |
| MS-R9 | BadReactionBreadth | **breadth ratio itself, market/sector-controlled** (`#{SUE>0∧CAR<0}/#{SUE>0}`, net of a discount-rate/guidance control: NOT the underlying "positioning stress" construct, which is an interpretation, not the target) | n/a | rising = de-risk | `POS-STRESS` | `S:R`, needs F5-SUE + fwd CAR; market-specific PIT (US `P:P`, CN `P:F`) |
| MS-R10a–e | Reversal triggers | **each is its own primary** (drawdown / breadth-rotation / β-gap / correlation-spike / vol-shock are five DISTINCT triggers, not variants of one target. Do not average them into a composite trigger) | n/a | trigger = accelerate | `REV-TRIGGER` | registered |
| MS-R11a-US/a-CN/b | Short-leg squeeze / borrow | **days-to-cover** (`b`) as primary; SI/float (`a-US`/`a-CN`, separately standardized market adapters) is a secondary input, not itself the target | n/a | high = short-leg risk | `SQUEEZE` (cross-ref MS-C1/US-S9) | registered |

**Missing-data rule (all rows):** a family with a data gap reports **`state: UNKNOWN`**, never a default-safe value. An absent crowding read must not silently relax a risk cap.

**Rejection tests (all MS-R):** a crowding/leverage measure is demoted if it **fails to predict stress-period liquidity/volatility/outflow/forced-flow** and moves only mean return (that would make it a disguised alpha, which this family forbids); if the "forced-flow" cards cannot be shown to precede realized mechanical selling; or if a summary state adds nothing beyond `MS-R1` after ablation. **No omnibus `CrowdingScore`**: components promote individually, never equal-weighted.

---

## 4. Falsification and promotion gates

| Module | What would reject/demote the hypothesis? |
|---|---|
| MS-I1 | predicted cost/fill buckets fail to order realized cost/fill OOS; signal disappears under realistic rather than only extreme costs; calibration is unstable across side/size/regime |
| MS-C1 | constraints do not incrementally strengthen independently measured overpricing/negative-news persistence; public proxies fail to track licensed availability/fee; China results vanish outside one rule regime |
| MS-C2 | a monotonic IO sign appears only because of size/index/liquidity or filing staleness; active/passive/strategic decomposition adds no incremental explanatory power |
| MS-C3 | delay/dispersion adds nothing after size/liquidity/coverage controls; future drift is absent or reverses; results depend on one denominator/window chosen ex post |
| MS-C4 | either pre-registered interaction fails FDR/holdout, is driven by earnings duplication, or disappears after timestamp/dedup/entity-relevance controls |
| MS-R1 | crowding fails to predict stress liquidity/volatility/outflow sensitivity; only mean return moves, with no proposed fragility channel |

Promotion sequence: mechanism-consistent univariate result → control/neutralized variant → component ablation → market/regime portability → point-in-time walk-forward → implementation/fill stress → locked holdout. An omnibus `ArbConstraintScore` or `CrowdingFragilityScore` is allowed only after component-level promotion; equal weighting is not the default.

---

## 5. Build sequence

1. **Phase 0, specified:** architecture, ownership boundaries, signed/asymmetric use, data tiers, timestamps, grades and falsification rules.
2. **Phase 1, implement first (within Market Structure's own build):** MS-I1 shared capacity/cost/feasibility fields and realized-cost validation. TrendReversal and StatRisk consume this contract. *(This "first" is local to this document; the global cross-document order is `Indicators_Pool_Combination_v1.md` §13, where MS-I1 is global step 3.)*
3. **Phase 2, public/vendor research:** US 13F joined on filings/amendments; FINRA short interest on publication schedule; ownership breadth; source-faithful annual price delay; analyst coverage/dispersion with PIT audit; public A-share eligibility/balances and source-specific ownership.
4. **Phase 3, licensed/data-heavy, last:** broker loan fee/availability/utilization/recall, client short activity, timestamped news archive/NLP, active/passive/lendable owner classification, holdings×flows, common ownership and fire-sale fragility.

No licensed Phase-3 feature should block the buildable children. Until it exists, use the relevant public object only under its weaker name/grade, or leave it missing.

## 6. Cross-references consumed, not recomputed

- `ARB-RISK` (IVOL, residual holding risk, close-substitute risk) → **StatRisk**.
- Raw news tone → **parent `NEWS` (US-S10a/b)** / **Fundamental F5/F8**.
- Short interest as bearish demand → **parent `INFORMED-POS` (US-S9)**.
- Directional value/quality/events → **Fundamental**; momentum/reversal → **TrendReversal**.
- Aggregate funding state → parent US-R6a / CN-R4a; it conditions constraints but is not part of the cross-sectional score.

## Sources

[Shleifer–Vishny: Limits of Arbitrage](https://shleifer.scholars.harvard.edu/publications/limits-arbitrage) · [Pontiff: Costly Arbitrage](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=879787) · [Abreu–Brunnermeier, synchronization risk](https://markus.scholar.princeton.edu/publications/synchronization-risk-and-delayed-arbitrage) · [D’Avolio, market for borrowing stock](https://www.aqr.com/Insights/Research/Journal-Article/The-Market-for-Borrowing-Stock) · [Asquith–Pathak–Ritter](https://www.sciencedirect.com/science/article/abs/pii/S0304405X05001170) · [Cohen–Diether–Malloy](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2758846_code353319.pdf?abstractid=672381) · [Nagel, short sales & IO](https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/f/575/files/2020/07/shortbtm.pdf) · [Boehmer–Kelley](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1468202) · [Chen–Hong–Stein, breadth](https://stein.scholars.harvard.edu/publications/breadth-ownership-and-stock-returns) · [Greenwood–Thesmar, fragility](https://www.hbs.edu/ris/Publication%20Files/Stock%20Price%20Fragility_eac0d3cb-4174-4a4f-af7d-610ff4e9de48.pdf) · [Passive Ownership & Short Selling](https://revfin.org/passive-ownership-and-short-selling/) · [Strategic Borrowing from Passive Investors](https://academic.oup.com/rof/article/28/5/1537/7646071) · [Hou–Moskowitz (price delay](https://www.ruf.rice.edu/~jgsfss/moskowitz.pdf) · [Diether–Malloy–Scherbina) dispersion](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00490) · [Engelberg–Reed–Ringgenberg, shorts & news](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1535337) · [Diamond–Verrecchia](https://citeseerx.ist.psu.edu/document?doi=3f8737b6de767834093e5672ceb0fbb38a38a2b5&repid=rep1&type=pdf) · [Hong–Lim–Stein, bad news travels slowly](https://stein.scholars.harvard.edu/publications/bad-news-travels-slowly-size-analyst-coverage-and-profitability-momentum-strategi) · [Tetlock, media pessimism](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2007.01232.x) · [Loughran–McDonald](https://www.uts.edu.au/globalassets/sites/default/files/adg_cons2015_loughran-mcdonald-je-2011.pdf) · [Wurgler–Zhuravskaya, imperfect substitutes](https://www.parisschoolofeconomics.com/zhuravskaya-ekaterina/research/WurglerZhuravskaya_JB_2002.pdf) · [Brunnermeier–Pedersen, funding & market liquidity](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1408432) · [Novy-Marx–Velikov (trading costs](https://www.nber.org/papers/w20721) · [Frazzini–Israel–Moskowitz) trading costs & capacity](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2294498) · [China short-sale refinancing study](https://www.sciencedirect.com/science/article/pii/S1755309118302521) · [Finding Anomalies in China](https://eng.pbcsf.tsinghua.edu.cn/dfiles/wp6.pdf) · [SEC Form 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f) · [FINRA short interest](https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest) · parent files and sibling children.

---

## Appendix: revision history

Kept for provenance. Nothing below is needed to read the contracts above.

**Change log v1.0→v1.1 (audit correction):** short-side constraint wording split **belief vs implementable weight**: a binding borrow constraint *raises the prior/confidence* that overpricing persists but *shrinks* the executable short (`mispricing prior ≠ implementable short weight`); "strengthens the short" no longer reads as "trade a bigger short."

**Change log v1.2→v1.3 (owner-contract precision, single primary target, ownership boundaries):** rewrote the MS-R owner-contract table (below) so every family has exactly **one primary validation target**, not 2–3 co-equal ones (e.g. CoMomentum's primary is now the momentum-factor **tail-loss event**, with mean return/vol/skew demoted to secondary diagnostics); added the explicit **MarketStructure-defines-primitive / PortfolioRisk-owns-book-state** boundary for `MS-R5` days-to-liquidate and `MS-R6c-own` vol-target deleveraging (neither reads own-book weights here); added the missing-data rule (**`state: UNKNOWN`, never a default-safe value**); ID list updated for `INDICATORS_REFERENCE.md` v2.9's atomization (35 cards: `MS-R6b`→`R6b-US`/`R6b-CN`, `MS-R11a`→`R11a-US`/`R11a-CN`, `MS-R8a`→`R8a`/`R8a-agg`, since US short interest ≠ CN margin-short and a raw stock-level Amihud read ≠ its crowded-basket aggregation).

**Change log v1.1→v1.2 (crowding/leverage/forced-flow subfamily: MS-R, REGISTERED OUTLINE):** registered the **`MS-R` family**: 26 atomic cards **outlined** in `INDICATORS_REFERENCE.md` §9b (v2.7), covering the risk chain `crowding → forced selling → liquidity stress → factor crash` from the July-2026 momentum crash. **Status is outline, NOT frozen:** nothing is `S:F` (CoMomentum, the anchor, is `S:C`), and the three summary states (`StructuralVulnerability`/`ForcedFlowPressure`/`LiquidityAbsorption`) are **proposed but NOT yet consumed**: Combination and PortfolioRisk still reference only the legacy `MS-R1`. **Wiring MS-R2–R11 into the Combination input registry and PortfolioRisk is an OPEN cross-document task.** **All outputs are risk-state/conditioner. Never an alpha sign.** Design decisions recorded: A-share CoMomentum residual is market+size+industry (HML dropped, accounting is `P:F`, no PIT history); A-share 两融/质押 are **leverage VULNERABILITY, not observed forced flow** (true `ForcedFlow_CN` needs liquidation events, `S:O`); book momentum-RC/theme-cosine **extends** PortfolioRisk `PR-D4` (which reports only ENB/residual-share), it is not the same object. Cautions: the "retail-not-institutional" and "liquidity-didn't-withdraw" claims are **not identifiable from public data**.
