# Quant Indicators Pool: Chinese A-Share, v2.8 (Falsifiable Research Inventory)

Timing and risk-state indicators for Chinese A-share equities, written as falsifiable research contracts: each carries an availability lag, an evidence grade, a sign hypothesis and a rejection rule fixed before any backtest. Layer 1 sets the research contract, Layer 2 the alpha hypotheses, Layer 3 the risk-state model and Layer 4 implementation. Supersedes `Indicators_Pool_AShare_v1.md`, which is kept privately as an idea catalogue.

---

## Layer 1: Research Contract (defaults)

| Field | Default |
|---|---|
| Target market / instrument | CSI 300 total return. **Primary implementation: 510300 ETF**. benchmark against **adjusted 510300 total return** (or explicitly attribute ETF-vs-index tracking difference; never silently mix ETF execution with index benchmark). Secondary: CSI 500 via 510500. Sector rotation runs under a **child contract** (below). |
| Forecast targets | (i) excess return over 7d repo/short CGB, horizons 5d / 21d / 63d; (ii) realized vol next 21d; (iii) drawdown probability next 63d. One target per hypothesis. |
| Timestamps | Every field carries four: `observation ts` · `publication ts` · `decision cutoff` · `first executable ts`. Backtests join on publication ts and trade at first executable ts. Tushare/AkShare update times must be empirically verified against official release times before a field's lag is trusted. |
| Decision & execution | **Default: signal frozen at close t → execute at open t+1 (or t+1 VWAP).** Same-close execution only if every input is frozen before a stated cutoff (e.g., 14:45 CST) and stored history reflects that cutoff. Close-derived values (closes, breadth, turnover, limit counts, ETF shares, settlement basis) are never executable at the same close. **T+1 rule:** shares/ETF bought at t are sellable t+1: position reductions must respect the holding constraint. |
| Positions | Long-only 0–100% initially; shorts only via IF/IC/IH futures as later extension under its own contract |
| Benchmark | Adjusted 510300 TR (see instrument row). Child contracts define their own benchmarks. |
| Costs | Dated low/base/high scenarios (2026 baseline): 510300 ETF 1 / 3 / 8 bps half-spread+impact per side: **ETFs are EXEMPT from securities stamp duty (SSE)**; sector ETFs 2 / 5 / 15 bps. **Single A-share stocks (Fundamental/TrendReversal/StatRisk children) add sell-side stamp duty = 0.05% = 0.5‰ = 5 bps (2023 rate, halved from 0.1%; corrects the earlier "0.05‰" factor-of-10 error).** Futures: commission + exchange fee + margin/roll/basis (no stamp duty). Dividend tax: separate tax-lot treatment for single stocks. **Acceptance: net edge positive with adequate uncertainty margin under the high (stressed) scenario.** |
| Point-in-time universe | Breadth, limit-count, dispersion, and sector studies require point-in-time membership: historical constituents, delistings, IPO seasoning (no-limit windows), ST status history, suspension flags, board membership, free-float history. **Limit-up/down counts are expressed as % of eligible tradable stocks** (ex-suspended, ex-no-limit-window), never raw counts. |
| Evaluation | Nested walk-forward with **mandatory regime-break table** (Layer 4); **locked final holdout**; **multiple-testing control** across indicator × transform × horizon grid (deflated Sharpe / FDR); **block-bootstrap/HAC uncertainty** for overlapping 21d/63d targets; every alpha also reported **unscaled and ungated**; ablation per component; fill-feasibility simulation for anything touching single names. |

**Pre-registration (required per hypothesis before any backtest):** primary target & horizon · expected sign/shape · primary metric · minimum economically useful effect net of stressed costs · minimum sample and subperiod-stability requirement · explicit rejection rule. Failure-regime notes in the tables are context, **not** a substitute.

**Child contract, sector rotation (申万一级):** universe = point-in-time sector membership; benchmark = equal- or cap-weight sector basket (not CSI 300); monthly rebalance default; own turnover/cost scenarios; target = sector return minus basket return. **Driver-conditioned tests (v2.2):** resources/materials, consumer, banks/property, growth, and high-dividend defensive sleeves are evaluated conditionally across growth, inflation, and credit-policy states, hypotheses to test, not predetermined mappings.

**Evidence grading (three dimensions):** **E** empirical evidence (A replicated · B market/regime-specific · C exploratory · D none) · **P** portability to A-share microstructure · **R** data readiness (point-in-time verified). `Gr` column shows **E**; binding P/R constraints are flagged in-row or the item sits in Deferred. Full E/P/R triples + one primary citation per indicator go into the research tracker at coding time.

**Redundancy groups (RG):** `POLICY` monetary stance · `FISCAL-CN` fiscal impulse (cyclically-adjusted primary balance + special-bond/land-sale pipeline; v2.5) · `CREDIT-CN` credit creation cycle · `GROWTH-CN` real activity · `PROPERTY` property cycle · `FX` RMB/external liquidity · `VALUE` long-run valuation · `TREND` price continuation · `REV` short-horizon reversal · `BREADTH` participation · `SPEC-HEAT` speculative intensity (turnover/limit-up complex) · `LEV` margin leverage · `FLOW` fund/foreign flows · `POS` institutional positioning (futures basis etc.) · `XASSET` cross-asset confirms · `INFL-CN` inflation axis (v2.2) · `CAPALLOC` capital allocation (v2.3) · `SENT` sentiment (surveys, option put/call) · `ISSUANCE-HEAT` IPO/issuance exuberance · `EARN-CN` earnings-expectations aggregate · `RISK-APPETITE-XA` cross-asset risk-appetite state (not vol) · risk-layer: `VOL`, `CORR`, `LIQ`. *(v2.4 added SENT, ISSUANCE-HEAT, EARN-CN; v2.6 added RISK-APPETITE-XA.)*
**Note:** SPEC-HEAT, LEV, and retail-sentiment measures are **one correlated complex. Do not count as independent diversification**; but they separate by horizon and role into distinct sub-composites (Mechanism Composites §6).
**ID convention:** where a row was split into sub-hypotheses (CN-M1→**CN-M1a/M1b**, CN-M5→**CN-M5a/M5b/M5c**), unsuffixed shorthand `CN-M1`/`CN-M5` in prose denotes the **family** (`CN-M1*`/`CN-M5*`); operational routing uses the specific suffixed IDs.

---

## Layer 1.5: Economic Environment & Exposure Map (v2.2)

*Architecture from* The All Weather Story *(Bridgewater 2012) and the Man Group level-vs-timing decomposition, architecture, not empirical validation.*

**Attribution (mandatory in every backtest report):** decompose total return into `cash + passive beta + tactical timing + risk-overlay effect − costs`. A long/flat strategy earns the investable cash return while flat (CN-M0). Timing-skill claims refer to the *timing* component only.

**Environment scores:** `G_t` = standardized growth surprise, `I_t` = standardized inflation surprise. "Surprise" = actual minus the **frozen consensus available immediately before release**. Never "improving vs last month." Point-in-time consensus snapshots required (verify vendor consensus history before trusting it).
- `G_t` inputs: **real-activity surprises only**: PMI new-orders surprise (CN-M4), IP, retail sales, exports, earnings-revision breadth, each vs contemporaneous consensus. **TSF/credit (CN-M1) and property (CN-M6) are NOT `G_t` inputs**: they are *separate transmission/conditioning states* (avoids double-counting the same variable in both the growth state and the credit/property mechanisms). Fiscal (CN-M9) likewise separate.
- `I_t` inputs: CPI and PPI surprises separately + PPI−CPI gap (CN-M5); commodity supply-shock component (CN-X1).

**China-specific structure:** policy-credit (CN-M1/M2/M3) and property (CN-M6) remain **separate transmission variables**, not substitutes for growth/inflation, they explain why the same macro surprise can produce different equity outcomes (e.g., a growth beat during a property-impaired transmission regime).

**Three uses:** (1) **label** the environment; (2) **condition**: every alpha family tested within environments; macro states enter as a conditioning/evaluation layer first, promoted to directional alpha **only if independently predictive OOS**; (3) **expose**, driver-risk dashboard: the tactical portfolio's rolling beta to growth surprises, inflation surprises, policy/credit shocks, and liquidity, risk concentration in economic-driver space, not just vol/pairwise corr. A joint 2×2 (G↑/↓ × I↑/↓) table is **our research extension**, not Bridgewater's exact construction.

**Inflation has no fixed sign for equities** ([Fed research](https://www.federalreserve.gov/econres/feds/good-inflation-bad-inflation-implications-for-risky-asset-prices.htm)): hence regime-conditional signs on CN-M5 and the CN-R7 state variable.

**What NOT to import from All Weather:** (1) equal risk across four environments is a design **prior**, not evidence of equiprobable regimes; (2) "betas outperform cash" / "similar return per unit risk" are hypotheses, not laws; (3) risk parity ≠ inverse-vol weighting, a leveraged multi-asset build needs its own contract (financing, futures rolls, collateral, margin, stress deleveraging; [AQR](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf)) and is **out of scope**; leverage cap stays 1.0. Here All Weather supplies: strategic baseline, macro-state classification, conditional robustness tests, risk-concentration diagnostic.

---

## Layer 2: Alpha Hypotheses

Columns: **Raw → transform** · **Target/horizon** · **Lag** · **Hypothesis & failure regime** · **RG** · **Gr**.

### 2.1 Policy & credit mechanisms (hypothesized dominant macro layer, itself a claim to test)

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-M0 | Cash & policy return (v2.2) | investable cash proxy for flat periods: money-market fund / GC001 repo / short-CGB return; ex-ante real cash = cash − expected inflation | attribution baseline + state | daily | The return earned while flat: mandatory in Layer 1.5 attribution. **Distinct from the R007−DR007 stress spread (CN-R4a): this is a return you earn, that is a risk signal.** | POLICY | B |
| CN-M1a | Credit acceleration | 3m Δ of TSF-stock YoY | 63d–1y equity excess | ~10–15th next month | Precedes equity strength (3–6m lead is a parameter to estimate). Fails when credit doesn't transmit (2021–23 property drag). | CREDIT-CN | B |
| CN-M1b | Credit impulse (conventional) | Δ of (12m rolling new TSF flow / nominal GDP) | 63d–1y equity excess | ~10–15th next month | **Separate ID from CN-M1a (two distinct constructions. Test independently, don't average).** | CREDIT-CN | B |
| CN-M2 | Monetary stance events (**heterogeneous. Split or freeze one stance model**) | RRR/MLF/LPR/7d-OMO changes → event dummies + stance index. **These four are NOT one instrument: RRR (quantity), MLF (policy-rate signal), LPR (transmitted lending rate), 7d-OMO (short-rate operation) have different information sets, event timings, and endogenous interpretations**. either give each its own event sub-ID (`CN-M2-RRR/-MLF/-LPR/-OMO`) tested independently, **or** freeze ONE declared monetary-stance-index construction and treat the individual events as its inputs, not separate votes. | 5–63d | announced same day (usually post-close) | Easing bullish short-window; **endogeneity caveat: easing amid deterioration is reaction, not stimulus. Condition on GROWTH-CN state.** Event-study first; "top timing events" claim from v1 downgraded to hypothesis. | POLICY | C |
| CN-M3 | M1 momentum | M1 YoY (new definition) → 3m Δ | 63d–1y | ~10–15th next month | M1 acceleration ≈ corporate/household liquidity activation → bullish. **Structural break policy (v2.1, hardened): PBoC redefined M1 Jan 2025 (adds personal demand deposits, payment-institution reserves); comparable revised-definition history extends back only through 2024. Old- and new-definition growth cannot be spliced into one stationary series. Treat as two separate regimes (estimate/validate separately), or reconstruct the added components from source data. Never splice, never mix levels.** | CREDIT-CN | B |
| CN-M4 | PMI | NBS mfg PMI + Caixin → new-orders sub-index, 3m Δ, surprise vs consensus | 21–63d | NBS: last day of ref. month; Caixin: 1st biz day | Improving orders bullish cyclicals. **PMI is monthly and already seasonally adjusted. Never merge Jan+Feb (v2.2 fix; merging applies only to NBS cumulative series, Layer 4).** Feeds `G_t` (Layer 1.5). | GROWTH-CN | B |
| CN-M5a | CPI surprise | actual − frozen consensus, standardized | **`I_t` input; 21–63d, sign regime-dependent** | ~9–10th next month | Good/bad inflation. Condition on `G_t` (Layer 1.5). | INFL-CN | B |
| CN-M5b | PPI surprise | actual − frozen consensus, standardized | **`I_t` input; industrial-sector relative** | ~9–10th next month | PPI reflation → industrial-earnings recovery. | INFL-CN | B |
| CN-M5c | PPI−CPI margin gap | PPI YoY − CPI YoY | **separate target: sector-relative upstream-vs-downstream margin state** | ~9–10th next month | Split from CN-M5a/b (different target & grade). | INFL-CN | C |
| CN-M6 | Property complex | 商品房销售面积 YoY, 70-city price diffusion → composite z | 63d–1y; bank/property/chain sectors | monthly, ~15th | Property stabilization bullish (banks, materials, consumption chain). Post-2021 the old "stimulus→property→equity" transmission is impaired: explicit regime hypothesis. | PROPERTY | B |
| CN-M7 | RMB regime | USDCNY vs fixing gap; CNH−CNY spread → 21d z | 21–63d | daily | Depreciation pressure bearish via outflow/liquidity channel. Fails when devaluation is orderly/export-supportive. | FX | B |
| CN-M8 | CGB curve slope | 10y−1y → level, 63d Δ | liquidity/policy descriptor | daily | **Not a recession lead in China** (policy-driven curve). Use only as liquidity-stance descriptor feeding POLICY composite. | POLICY | C |
| CN-M9 | **Fiscal impulse (`FISCAL-CN`, v2.5): a MODELLED construct, `registered/research` (NOT yet a clean "proper impulse")** | the *target* concept is **Δ of the cyclically-adjusted primary balance**, approximated from the China pipeline: general public-budget expenditure vs revenue; government-fund expenditure & land-sale revenue; **new special local-government bond** issuance (project vs refinancing/debt-swap); central **special-treasury** issuance; **expenditure-vs-quota pace**. **A monthly ΔCAPB is NOT directly observable**: land-sale revenue, government funds, refinancing/debt-swap, and off-budget/LGFV channels make it a **model output**, and this row still lacks a **vintage/revision policy and a seasonal + cyclical-adjustment contract**, so it stays research-grade, not a frozen impulse. | 63d–1y; growth/policy conditioning state | monthly, lagged (MoF releases; `R=unverified`: confirm 财政部/[MoF](https://zwgls.mof.gov.cn/tjsj/) release calendar; **vintage/revision contract TBD**) | **Conditioning state FIRST**; **directional alpha only after an incremental OOS test.** Fiscal *impulse* ≠ deficit level ([IMF method](https://www.elibrary.imf.org/abstract/journals/001/1991/091/article-A001-en.xml)). Transmission regime-dependent (impaired when property/local-gov balance sheets stressed). **A *separate* conditioning/transmission state: NOT a `G_t` input** (excluded from the growth-surprise score to avoid double-counting), and separate from monetary (CN-M2/M3) and credit (CN-M1). | FISCAL-CN | C |

### 2.2 Valuation & fundamentals

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-V1 | Index PE/PB percentile | CSI300/500 PE-TTM, PB → percentile vs trailing 10y | strategic tilt, 1y+ | daily | Extreme cheapness → above-avg long-run returns. No tactical power; percentile window choice materially changes signal (test 5y vs 10y). | VALUE | B |
| CN-V2 | **Earnings-yield − bond-yield spread (ERP *proxy*, NOT a structural ERP)** | CSI300 E/P − CGB 10y → percentile | strategic, 1y+ | daily | A valuation *spread*, not a cash-flow-implied equity risk premium: label it a proxy. High spread marks major bottoms (2014, 2018-12, 2022-10, 2024-01 pattern). Same OOS caveats as all valuation timing. | VALUE | B |
| CN-V3 | Dividend-yield spread | CSI Dividend yield − CGB 10y | strategic; dividend-style relative | daily | Wide spread → dividend/SOE style outperformance (中特估 regime). Style-rotation signal, not index timing. | VALUE | C |
| CN-V4 | Industrial profits | 规模以上工业企业利润 YoY | confirm layer, 63d+ | monthly, ~27th | Lagging confirm of GROWTH-CN; never standalone. | GROWTH-CN | C |
| CN-V5 | Aggregate earnings expectations (v2.3) | covered-universe EPS revision breadth + magnitude + dispersion (朝阳永续/Wind consensus: PIT integrity audit required first) | 21–63d | ~weekly | Rising aggregate revisions bullish. Coverage skews to large caps: this is a large-cap signal. Firm-level → child F5 (incl. 预告 surprise). | EARN-CN | C |
| CN-V6 | Aggregate quality trend (v2.3) | % of firms improving 扣非-ROE / margins / cash conversion (breadth), refreshed on the Apr 30 / Aug 31 / Oct 31 report clusters | 63d+; regime confirm | report-cluster lag | Broadening improvement confirms GROWTH-CN; narrowing breadth under rising index = warning (hypothesis). Firm-level → child F2–F4. | EARN-CN | C |
| CN-V7 | Aggregate capital allocation & supply (v2.3) | market net payout (cash div + executed buybacks − placements/rights) vs Δ total shares; 解禁 unlock calendar as supply overlay | 63d+; strategic | announcement/filing lag | Post-2024 国九条 payout regime is a structural break: date it. Heavy unlock/issuance windows = supply headwind. Firm-level → child F7; unlock overlay stays FLOW. | CAPALLOC | C |

### 2.2b Cross-sectional fundamental families, child-contract summary (v2.4)

**Stock-selection factors, not index-timing signals.** They trade under `Indicators_Pool_Fundamental_v1.md` (own universe, benchmark, long-only, costs incl. stamp duty & dividend-tax-by-holding-period); only CN-V5/V6/V7 above feed this timing file. Summary: A-share grades are deliberately NOT inherited from US evidence:

| Family | Core measures (A-share specifics) | Role | CN Gr |
|---|---|---|---|
| F0 Size | mcap: **control only**; size-as-alpha was shell-value-contaminated and 2024 delisting reform accelerates shell decay | control | alpha D |
| F1 Multi-metric value | **(EQ)** 扣非-E/P primary (LSY: E/P > B/P in China), B/P · **(EV, unlevered numerators)** FCFF/EV (primary), EBIT/EV · robustness: EnterpriseCFO/EV, EBITDA/EV, NOPAT/EV, sales/EV; equity-vs-enterprise base tagged (child §1); LSY bottom-30% exclusion = dated robustness spec. **Financials → `Indicators_Pool_Financials_v1.md` (own contracts; banks first)** | core | B |
| F2 Profitability | GP/assets, operating & cash profitability (native numerators), ROA/ROIC; **扣非 adjustment for NI-based measures only** (E/P, ROE, net-ROA, SUE); ROE leverage-decomposed | core | B |
| F2b Profit growth (`PROFIT_GROWTH`, v1.4) | realized Δ扣非-ROE/ΔROA/Δmargin (**+sign**, Δlevel primary); YoY | fundamental improvement; ablate vs F2 level | C |
| F3 Earnings/cash quality | accruals/assets, CFO/NI; screen role likely > symmetric alpha; test vs F2 subsumption | quality component | C |
| F4 Financial strength | 有息负债率, coverage, net debt/EBITDA; **大存大贷 flag** (cash+debt fraud fingerprint); Z/O-score (research) | core | B |
| F5 Fundamental/event momentum (RG EARN_EVENT) | SUE, **per-event CAR (board-adjusted, fill-feasible)**, consensus revisions incl. **forecast-ROE revision** (expectation-based; realized ΔROE → F2b); event ladder 预告→修正→快报→报告: interval 预告 surprise, correction-surprise, selection-bias guard | core where data exist; event horizons | C (until PIT audit) |
| F6 Investment / asset growth | asset growth, capex/assets, NOA (real-investment, **−sign**; debt issuance → F7, debt level → F4); **q5 `EXPECTED_INVESTMENT_GROWTH` own RG, +sign OPPOSITE to realized investment. Never composited with F6: CN E:D unverified (own grade, ≠ realized-F6 evidence)** | research tier only | C (F6); q5 D |
| F7 Capital allocation (RG CAPALLOC) | cash div yield & coverage, initiation/cut, **executed** buybacks, Δ total shares, placements/rights, **NSI-1Y / CSI-5Y / FIN**, **net debt issuance `DBNETIS/AT`** (not ΔNetDebt); **post-2024 国九条 = dated regime break**; 解禁 unlocks → flow group | core-expand, regime-dated | B |
| F8 Governance/forensics | 非标 audit opinion, 资金占用/related-party, **股权质押 ratio**, goodwill/assets, late filing, **small-profit clustering (保壳)**, delisting-risk under 2024 rules | **risk screen** | screen |
| Overlays | stability in quality; intangibles as fixed-parameter alternate spec; consolidated statements, as-filed snapshots (vendors overwrite history) | measurement | n/a |
| Contextual score / expectation-error overlays (child v1.4) | annual Piotroski F-Score within value (**C**); quarterly CN adaptation kept separate; Mohanram G-Score (**D**, R&D/advertising coverage gap); Piotroski–So 3×3 matrix (**C research role**) | stage-2/avoid-screen candidates; **not additive families**; long-only maps negative incongruence to avoid/underweight | C |

**Cross-sectional siblings (not in this timing file):** price-based → `Indicators_Pool_TrendReversal_v1.md` (incl. **T-X8 `SEASONAL`**: CN B raw / C risk-adjusted); statistical-risk → `Indicators_Pool_StatRisk_v1.md` (IVOL/MAX/**IDSKEW** lottery + **R-X6 `SYS-DEFENSIVE`**, CN C replicated-weak); market structure → `Indicators_Pool_MarketStructure_v1.md` (stock-level capacity/cost/verified borrow, heterogeneous institutional ownership, price delay/news×constraint and crowding; CN short constraint is a feasibility gate, not stationary alpha).

Initial production structure (child v1.4): **slow monthly sleeve** = F1 + quality(F2 profitability + stability) + **F2b PROFIT_GROWTH** with F3/F4/F8 as **one-sided penalties**; **event sleeve** = 预告 surprise/修正, 快报, per-event CAR, forecast-ROE revisions where PIT-adequate. F-Score/G-Score and the expectation-error matrix remain stage-2 research variants with separate annual/quarterly specifications. Sleeves combine at allocation level, never signal-averaged; slow families at 126/252d primary horizons. F6 (−sign) / q5 EXPECTED_INVESTMENT_GROWTH (+sign, separate) / F7 on incremental value. Data contract (field-level event ladder, Apr 30 double refresh, report clustering): child file §6.

### 2.3 Trend & reversal (price transformations)

> **Scope (v2.3):** these rows are **index/sector timing** only. Note CN-T4 is *index* reversal, distinct from cross-sectional stock reversal (which is strong in A-shares but execution-constrained). Cross-sectional individual-stock momentum/reversal (esp. **residual momentum**, short & long reversal, daily-attention momentum) lives in the sibling child contract `Indicators_Pool_TrendReversal_v1.md`; earnings-event continuation (CAR/PEAD) lives in fundamental F5. No MACD/RSI/ROC/MA families, parameter variants inside `TREND`.

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-T1 | Time-series momentum | 12-1m, 6m, 3m excess-return z | 21–63d | none | Continuation. Multi-asset TSMOM is Grade-A; **A-share single-index trend is B and historically punctuated by policy-driven V-reversals (2024-09-24 style): stop-logic mandatory.** | TREND | B |
| CN-T2 | MA filter (20/60/250d) | price vs MA + crossovers | regime gate | none | Same RG as CN-T1 (pick/blend, don't double-count). 250d (年线) retail salience → possible self-fulfilling level effects: **hypothesis, untested.** | TREND | B/C |
| CN-T3 | Sector cross-sectional momentum | 6-1m 申万一级 RS rank | 21–63d sector relative | none | Winners persist; A-share sector momentum decays faster than US (hypothesis from local research; estimate half-life, don't assume). | TREND | B |
| CN-T4 | Short-horizon reversal | 1–5d index return z | 1–5d | none | **Hypothesis: daily-frequency reversion stronger in A-shares than US (retail overreaction + T+1). Plausible mechanism, must be measured, not asserted** (v1 stated as fact: downgraded). Costs and T+1 constrain execution. | REV | C |
| CN-T5 | 52-week-high proximity | price / 252d max | 21–63d | none | Anchoring continuation; same RG as TREND. | TREND | C |

### 2.4 Breadth, speculative heat, leverage & sentiment (v2.4: NOT one mechanism, distinct horizons/signs; see sub-composites in Mechanism Composites §6)

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-B1 | Breadth | % stocks > 250d MA; adv/decl → level + divergence vs index | 21–63d; DD prob | none | Narrow breadth under rising index → correction risk. Mega-cap/national-team support episodes create false divergences. | BREADTH | B |
| CN-B2 | Normalized turnover | 全市场成交额 / free-float mcap → **rolling 3y percentile** (replaces v1 nominal RMB thresholds: listings & float growth make nominal levels non-stationary) | 5–21d contrarian at extremes; regime descriptor | none (daily close) | Baker–Stein mechanism (liquidity ≈ sentiment under short-sale constraints: **conditional**, not "every high-turnover day is a top"): extreme turnover percentile + extended TREND → froth hypothesis; turnover collapse after drawdown → capitulation hypothesis. | SPEC-HEAT | B |
| CN-B3 | Limit-up complex | 涨停家数, 连板高度, 炸板率 → composite z (board- & date-aware limit rules, see Layer 4) | 1–21d; speculative-regime descriptor | none (daily) | High/rising limit-up breadth = speculative risk-on. **Predeclared piecewise rule with a dead zone using FIXED percentile thresholds (NOT trained breakpoints: resolves the earlier contradiction): the 60th/90th percentiles vs a rolling 3y window (min 2y history) are the declared rule, held fixed, not estimated on the training sample.** Below 60th → NO directional signal (dead zone); 60th–90th → continuation; above 90th (blow-off) → contrarian. One nonlinear mapping, thresholds declared-not-fit. Counts as **% of eligible tradable universe** (ex-suspended, ex-no-limit windows), never raw counts (Layer 1). Rule changes alter comparability (2026-07 ST change adds ~150 names to ±10% pool). | SPEC-HEAT | C |
| CN-B4 | Margin balance (两融) | 融资余额 → 21d Δ z + % of float mcap percentile | 5–63d; leverage-fragility state | **T+1 (published next morning by exchanges)** | Rising margin = risk-appetite confirm; extreme percentile + rapid build = fragility (2015 pattern). Forced-deleveraging episodes make this the key crash-amplifier state variable. | LEV | B |
| CN-B5 | New investor accounts | 新增投资者数 (CSDC) → percentile | 63d contrarian at extremes | **monthly, ~2wk lag; `R = unverified`: confirm CSDC release convention** (weekly series discontinued 2015-era) | **Revealed retail participation, NOT a belief survey.** Account-opening surges mark late-stage rallies. Slow contrarian tilt only. | SPEC-HEAT | C |
| CN-B6 | New fund issuance (decomposed, v2.4) | **raised assets** (not launch count) → 3m sum percentile, per category | 63d–1y | **fund-establishment announcement (not launch date)** | Keep three categories separate: do NOT pool: **active-equity fundraising** = plausible late-cycle exuberance (booms 2015, 2021-01); **new ETF-product fundraising** = product supply/policy/sponsor timing (sign to be tested, ≠ contrarian-buy); **existing ETF share creation = CN-F2 flow, a different object.** Detrend (MF-channel decline post-2022). | FLOW | B |
| CN-B7 | Exchange option put/call (v2.4) | put/call volume & OI ratio, **per venue & underlying kept separate:** SSE/SZSE **ETF options** (50/300/500 ETF); **CFFEX index options** (correct codes: **IO** = CSI 300, **HO** = SSE 50, **MO** = CSI 1000; *no CSI 500 index option at CFFEX*, IF/IH/IC/IM are the **futures** codes, don't reuse them): separate ingestion contracts | 5–21d contrarian at clean extremes | **after close → executable next session** | Available even without an official live iVIX: different data contract ([SSE](https://www.sse.com.cn/assortment/options/date/), [CFFEX product list](https://www.cffex.com.cn/cp/)). Hedging-sensitive. | SENT | C |
| CN-B8 | Financing purchase intensity (v2.4) | **primary:** 融资买入额 / turnover **of margin-eligible names on that date** (`Σ_{i∈Eligible} FinBuy_i / Σ_{i∈Eligible} TradeValue_i`); total-turnover denominator = robustness only | 5–21d; current demand | T+1 morning | **Flow** (current leverage *demand*) vs CN-B4 **balance** (accumulated *fragility*). Eligible-universe denominator prevents list expansion/contraction masquerading as sentiment. | LEV | C |

### 2.4b Capital-markets exuberance: IPO/issuance (v2.4, Baker–Wurgler-inspired, institutionally adapted)

*Anchor [Baker–Wurgler 2006](https://people.stern.nyu.edu/jwurgler/papers/sentiment.pdf), but **IPO count & first-day returns cannot be copied directly**: issuance suspensions/administrative slowing, the old 44% first-day cap, board differences, and the 2019+ registration reform create major structural breaks ([regime caveat](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243080), [CSRC registration reform](https://www.csrc.gov.cn/csrc/c100028/c7123213/content.shtml)). **Do NOT build one aggregate "China IPO sentiment" number.** Split supply from demand; every IPO obs carries board / pricing-regime / price-limit rule / offer method / dates; **normalize within board × regulatory regime** (never pool a Main-Board 44%-cap IPO with a post-registration STAR/ChiNext IPO).*

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-CM-SUPPLY | Regulatory & issuance supply (**decomposed by sign, v2.4**) | **Market-receptivity** (`+`): completed IPOs, proceeds/mcap, filing→listing conversion. **Cold-market** (`−`): withdrawal/termination rate, review duration. **Policy-pipeline descriptors** (sign policy-dependent, kept separate): applications accepted, approvals/registrations | 6–24m; regime state | **per-event on each field's official publication date** (acceptance / registration / termination / pricing / listing); monthly value = events publicly known by month-end. `R = unverified`: confirm CSRC/exchange disclosure feeds | **Substantially a policy/capital-supply state, not pure sentiment**. Condition on regulatory regime; do NOT sum opposite-sign fields into one raw count. | ISSUANCE-HEAT | C |
| CN-CM-DEMAND | Observable investor demand | **directions explicit:** `+`oversubscription (online & offline **kept separate**: allocation/clawback rules differ); `+`market-adj first-day return; `+`first-day turnover; `−`abandoned-subscription rate; `−`day-1 broken-issue. **`−log(中签率) ≈ log(valid subscriptions/offered allocation)` IS an oversubscription measure: do NOT also weight both.** Clawback/reallocation = regulatory *diagnostic*, not a vote. Offer-valuation-vs-comps = pricing control, not demand. | 3–24m, contrarian at froth | **per-event, staggered by field (see leakage note)** | Subscription/`−log(中签率)` are cleaner demand reads than IPO count (count is set *before* investors bid). Board×regime normalized. | ISSUANCE-HEAT | C |

First-day return uses the **compounded market adjustment** (cleaner for large IPO pops, board-index benchmark): `IR_i = (C_i,1 / P_i,offer) / (I_listing-close / I_pricing-close) − 1`.

**CN-CM-DEMAND event-age leakage rule (v2.4):** %below-offer at **d1 / d5 / d20 are separate event-age vintages, not simultaneous observations.** A day-20 broken-issue value is unknown until close of trading day 20 → its signal first trades day 21, forecast return begins after day 20, and it **cannot** enter the listing-month score before day 20. Day-5/day-20 returns also overlap short-horizon momentum / post-listing price discovery: **not pure primary-market sentiment**; grade/treat separately from day-1.

Cross-ref fundamental F7 (CAPALLOC): issuance is simultaneously sentiment, financing supply, and corporate timing. **Horizon sub-composites** mirror the US file: fast speculative demand (CN-B2/B3/B7/B8), medium beliefs (surveys/SIPF), slow exuberance (CN-CM-*, CN-B6), positioning/fragility (CN-B4, CN-F1/F5): combined at allocation layer, never one daily number.

### 2.5 Flow & positioning

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-F1 | Index-futures basis | IF/IC/IH annualized basis vs fair value → percentile; ΔOI | 5–63d; hedging-demand descriptor | none (intraday/close) | Deep discount (贴水) = heavy hedging/bearish institutional positioning. **Predeclared state-conditioned rule (breakpoint on training sample, frozen; discount percentile vs rolling 3y, min 2y history): beyond the 85th-pct discount AND NOT in a declared funding/vol-stress state → contrarian-bullish; in a **declared stress state (CN-R4a interbank-funding-stress spread above its stress threshold OR CN-R1 realized-vol regime elevated)** → risk descriptor, no buy (stress precedence overrides).** One mapping, not two free hypotheses. Snowball-product knock-ins (2024-01) distort episodically. | POS | C |
| CN-F2 | ETF share creation | broad-index ETF shares outstanding Δ (Δshares × NAV) | 5–63d | T+1 (daily disclosure) | Large sustained creations = institutional/official accumulation (observable *flow*, buyer **not** identifiable. See Deferred re national team). Bullish-support hypothesis at market lows. | FLOW | C |
| CN-F3 | Major-holder net 增持/减持 | announced net value → 21d sum z | 63d+ | announcement day (evening) | Industrial-capital cluster buying after selloffs bullish (informed-money). Announcement≠execution timing noise; lockup-expiry supply is the confounder. | FLOW | C |
| CN-F4 | Southbound flows (港股通) | daily net buy (still disclosed) → 21d z | HK-A risk-appetite descriptor | none (daily) | Mainland risk appetite read-through; **southbound disclosure unchanged by the 2024 reform** (northbound is the broken one). Cross-market confirm only. | FLOW | C |
| CN-F5 | Fund positioning estimates (公募仓位测算) | vendor-estimated equity ratio → percentile | 63d contrarian | weekly estimates, model-based | Estimated (regression-based), not observed. Treat as C-grade descriptor; verify vendor methodology stability before use. | POS | C |

### 2.6 Cross-asset confirmations

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-X1 | Commodity complex, demand-vs-supply decomposition (v2.2) | demand proxies: copper (SHFE/LME), rebar, iron ore → 63d Δ z; supply/inflation: energy + broad basket scored **separately** | 21–63d cyclicals relative; `G_t` vs `I_t` inputs | none | Copper/rebar/iron-ore ≈ China-growth demand pricing (feeds `G_t`; timely confirm of GROWTH-CN before monthly data). Energy & broad basket carry supply/inflation-shock information (feeds `I_t`). Never collapse into one score: supply shocks confound demand reads; the decomposition is the mitigation. | XASSET | B |
| CN-X2 | Gold + CGB duration bid | 21d joint z | risk-off state confirm | none | Joint haven bid = domestic flight-to-quality. | XASSET | C |
| CN-X3 | HK/ADR overnight gap | HSCEI + ADR-implied A-share gap at open | 1d open positioning | pre-open | Offshore overnight moves partially transmit at open; decays intraday. Belongs to short-horizon sleeve. | XASSET | C |
| CN-X4 | Defensive leadership | banks/utilities/dividend RS 21–63d vs CSI300 | 21–63d DD prob | none | Defensive rotation precedes broad risk-off; overlaps BREADTH. Verify incremental value. | XASSET | C |

---

## Layer 3: Risk / State Model (sizes positions; NOT alpha)

| ID | Indicator | Raw → transform | Forecast | Lag | Notes | RG | Gr |
|---|---|---|---|---|---|---|---|
| CN-R1 | Realized vol ratio | 21d RV / 252d RV | next-21d vol | none | Vol **persistence** is Grade-A; "calm precedes storm" is a separate hypothesis (test via vol-of-vol, don't assert). | VOL | A (persistence) |
| CN-R2 | GARCH/HAR forecast | index daily RV → forecast | 1–21d vol | none | Primary sizing input: **realized-vol models carry the load here; the options complex is thin** (see Deferred re iVIX). | VOL | A |
| CN-R3 | Cross-sectional dispersion & avg pairwise corr | 63d rolling | diversification state | none | Correlation convergence in policy shocks → cut gross; also gates stock-picking vs index regimes. | CORR | B |
| CN-R4a | Funding stress (v2.2 split) | R007−DR007 spread; NCD yields | interbank funding-stress state | daily | Interbank stress → de-risk override (2013 SHIBOR-squeeze pattern). Split from equity liquidity per component-decomposition principle. | LIQ | B |
| CN-R4b | Market liquidity (v2.2 split) | Amihud illiquidity & spreads on index/ETF | equity-liquidity state | close-derived → t+1 | Different mechanism from funding stress: separate contract, separate ablation. | LIQ | B |
| CN-R5 | Limit-down breadth | **⚠ formula corrected in the implementation register (v3.3): "at limit-down + limit-locked share" summed the two populations, but limit-locked names are a SUBSET of at-limit-down names: summing double-weights them.** See `INDICATORS_REFERENCE.md` §11 `CN-R5` for the candidate rules (none yet frozen); this row states the mechanism only, not the arithmetic. (point-in-time universe, Layer 1) | panic-state descriptor | close-derived → t+1 | Mass limit-downs = liquidity vacuum (sellers can't exit → contagion to sellable names). Panic-state flag that **overrides REV signals** (catching knives at limit-down cascades untradeable anyway: fills infeasible). | LIQ | B |
| CN-R6 | Drawdown state | DD from 252d high | state descriptor | none | Conditions active alpha families. | VOL | n/a |
| CN-R7 | CGB–equity correlation sign (v2.2) | 63d rolling stock–bond corr | inflation/policy-regime descriptor; hedge validity | close-derived → t+1 | A-share analogue of US-R8: rising positive correlation warns duration no longer offsets equity risk → cut gross. | CORR | B |
| CN-R8 | **Cross-asset risk appetite (RTI, v2.6)** | **global RTI as an external conditioning variable first** (a domestic A-share RTI is grade C/D: policy-driven markets, thin cross-asset universe, bond-data/cross-hours limits); see `Indicators_Pool_PortfolioRisk_v1.md` §PR-R1/§5.2. **Execution clock: US closes AFTER China closes → use the most recent globally-complete info set, then trade the next feasible China session (else a backtest leaks post-close US info into the China decision).** | risk-state (not alpha); extremes only | weekly | **Risk-state, NOT direction**: pair with absolute state; gated on incremental value over CN-R7/CN-X4/CN-R1–R2. Local RTI deferred to research. Grades **E:C · P:C/D · R:C**. | RISK-APPETITE-XA | C |

**Volatility-scaling policy:** same discipline as US file, candidate policy, own ablation, leverage cap 1.0, smoothing, deadband, full costs (Moreira–Muir vs Cederburg et al.).

---

## Layer 4: Implementation Model

**Price-limit rules (board- and date-specific, backtests must join on date):**

| Board | Regular | Risk-warning (ST/*ST) | Notes |
|---|---|---|---|
| Main board SSE/SZSE | ±10% | **±5% before 2026-07-06; ±10% from 2026-07-06** ([SSE](https://english.sse.com.cn/news/newsrelease/voice/c/c_20260708_10824778.shtml)) | ~150 ST names affected by change |
| ChiNext (创业板) / STAR (科创板) | ±20% | ±20% | since Aug 2020 / inception |
| BSE (北交所) | **±30%** | n/a | no price limit **only on the public-offering listing day** ([BSE rules](https://www.bse.cn/jygl_list/200028217.html)) |
| IPOs: main board / ChiNext / STAR | no limit first 5 trading days (post-registration reform) | n/a | does **not** apply to BSE (see row above) |

- **Fill feasibility:** signal on a limit-locked name/day is untradeable, model no-fill; index ETFs remain tradable but at gap prices.
- **T+1:** shares/ETF bought at t sellable t+1 → same-day round-trips impossible; REV strategies must hold overnight; overnight gap risk is part of the REV cost model.
- **Shorting (v2.1 corrected: 融券 ≠ 转融券):** the 2024 CSRC action suspended **转融券** (securities *refinancing*/transfer lending) ([CSRC](https://www.csrc.gov.cn/csrc/c100028/c7493852/content.shtml)); ordinary broker **融券** remains legally available with a large eligible list ([SSE](https://www.sse.com.cn/lawandrules/sselawsrules2025/trade/specific/margin/c/c_20260710_10825136.shtml)), but actual borrow inventory is scarce and **security-, broker-, and date-specific**: model borrow availability at that granularity or do not model single-name shorts at all. Practical default: shorts via index futures only; futures basis (CN-F1) then becomes part of your own cost.
- **Data availability discipline:** monthly macro (TSF/M1 ~10–15th; PMI last-day/1st; PPI ~9th; property ~15th; industrial profits ~27th): join on release date, never reference month. 两融: T+1 morning. CSDC accounts: monthly, lagged. **Seasonal (v2.1 corrected):** combine Jan+Feb **only for series NBS itself reports cumulatively for Jan–Feb** (industrial output, retail sales, FAI, industrial profits); **PMI is monthly and already seasonally adjusted. Never merged** ([NBS](https://www.stats.gov.cn/english/PressRelease/202602/t20260202_1962478.html)).
- **Structural breaks (mandatory walk-forward flags):** 2015 margin crash + intervention; **2016-01 circuit-breaker episode. Flag and stress-test, never exclude (excluding real history biases the strategy toward easy regimes)**; 2018-19 trade war; **2019-07 STAR registration launch (market-oriented IPO pricing, new first-day rules); 2020-08 ChiNext registration reform + ±20%; 2021 BSE launch (±30%); 2023 Main-Board registration transition**: IPO price/scale/early-trading rules NOT comparable across boards or across these regimes (governs CN-CM-*); 2024-01 snowball knock-ins (basis distortion); 2024-08 northbound disclosure break; 2024-09 policy pivot; 2025-01 M1 redefinition; 2026-07 ST limits.
- **Data revisions:** NBS series revised and seasonally distorted; prefer market-price confirms (CN-X1) for timeliness; keep vintages where possible (Tushare stores current-vintage only, snapshot going forward).
- **Vendors:** Tushare Pro / AkShare primary; verify each field's actual publication timestamp empirically before trusting it in backtests (Tushare update times ≠ official release times).

---

## Mechanism Composites (replaces v1 "one per category")

1. **Policy-credit cycle** = CN-M1a/M1b (credit acceleration/impulse, same RG, one credit-cycle score) + CN-M3 + CN-M2 events conditioned on CN-M4 growth state; **CN-M9 fiscal impulse (`FISCAL-CN`) enters as a *separate* conditioning state, not merged into the monetary/credit score** (different transmission; alpha only after OOS)
2. **Growth nowcast / `G_t`** = CN-M4 surprise + IP/retail/exports surprises (+CN-X1 demand-leg daily confirm if incremental; CN-V4 slow confirm)
2b. **Inflation axis / `I_t`** (v2.2) = CN-M5 family (CPI, PPI surprises, PPI−CPI gap) + CN-X1 supply-leg, conditioning layer first (Layer 1.5); promoted to alpha only if independently predictive OOS
3. **Property regime** = CN-M6 (own composite, impaired-transmission hypothesis explicit)
4. **Valuation tilt** (strategic, 1y+) = CN-V1/V2
5. **Trend** = one of CN-T1/T2/T5 + CN-T3 sector sleeve
6. **Sentiment/positioning/exuberance, sleeves with indicator-specific signs (v2.4, authoritative; supersedes the old two-frequency retail-heat row). No blanket sign.**

   | Sleeve | Horizon | Components (sign) |
   |---|---|---|
   | Fast speculative demand | days–wks | CN-B2 turnover + CN-B3 limit-up + CN-B7 put/call + CN-B8 financing-purchase (contrarian at clean extremes) |
   | Retail participation | 1–3m | CN-B5 new accounts (revealed participation, contrarian at extremes). *No live A-share direct-belief survey passes readiness: SIPF is deferred/historical only.* |
   | Slow issuance heat | 6–24m | CN-CM-SUPPLY/DEMAND (`ISSUANCE-HEAT`) + CN-B6 active-equity fundraising (contrarian at extremes) |
   | Positioning / fragility | days–months | CN-B4 margin *balance* (`LEV`, fragility); CN-F1 futures basis (**two-regime: contrarian-bullish at deep discount / risk-descriptor in stress**); CN-F5 fund positioning (**contrarian**): indicator-specific signs |
   | Observable flow | wks–months | CN-F2 ETF creation + CN-F3 major-holder 增持/减持 (informed flow) |

   Combined at allocation level, never one number. **CN-F1 appears once (positioning sleeve only): not double-counted.** The v1 fear/greed design lives in the fast-speculative-demand sleeve.
7. **Risk overlay** (Layer 3) = CN-R1/R2 sizing + CN-R4a/R4b/R5 override gates + CN-R3 gross control + CN-R7 hedge-validity state. **CN-R8 (RTI) is `registered` (specified, not yet computed): a dashboard candidate not in sizing until computed (→ `shadow`) and it passes the incremental-value test (→ `active`).**
   *(Flow/positioning rows CN-F1/F2/F3/F5 are owned by the item-6 sleeve table, not repeated here, to avoid the earlier double-count.)*

Cross-composite correlation watch: Trend ↔ Breadth ↔ Retail-heat (all rise together in rallies); Policy-credit ↔ Property (policy responds to property); FX ↔ (deferred) foreign flow.

---

## Deferred, unresolved data contracts (Grade D; do not code yet)

| Item | Why deferred |
|---|---|
| **Northbound net flow (北向资金), live** | Post-2024-08 official disclosure = total turnover only: **no daily buy/sell split, so daily net flow is not computable**; holdings disclosure reduced to quarterly. Pre-2024-08 history usable for *research on the mechanism* with a hard series end; any "current northbound" vendor number needs its estimation method audited first. ([HKEX circular](https://www.hkex.com.hk/-/media/HKEX-Market/Services/Circulars-and-Notices/Participant-and-Members-Circulars/SEHK/2024/CT03824E.pdf)) |
| **National-team identification** | No point-in-time observable: ETF creations show flow, not buyer; 汇金 announcements/holdings arrive after the trade. Re-admit only with a validated real-time proxy (e.g., abnormal broad-ETF creation bursts at drawdown lows: as a *hypothesis about flow*, CN-F2, not buyer identity). |
| **iVIX / 中国波指 & options term structure** | Official iVIX publication suspended 2018; current vendor reconstructions unofficial; 300ETF-option IV usable but short history + liquidity regime shifts. Revisit once a clean point-in-time IV series is secured. |
| **股吧/search NLP sentiment** | No versioned point-in-time corpus yet; survivorship in scraped forums; build collection pipeline first, research later. |
| **私募 positioning surveys** | Vendor model estimates, opaque methodology, licensing. |
| **融券 short interest** | Series repeatedly truncated by regulatory restrictions (2024 tightening): non-stationary by policy. |
| **Retail order imbalance** | Not publicly identifiable with adequate consistency (no TAQ-equivalent); defer until a reliable classification/data source exists. |
| **龙虎榜 activity** | Sample selected by abnormal-trading disclosure rules → aggregate net buying is severely selection-biased; research only. |
| **Closed-end fund discount** | Historical-replication only: the relevant closed-end universe has contracted/changed; not a modern core signal. |
| **SIPF investor-confidence survey** | Historical research indicator; official archive shows monthly releases only through Aug 2023 ([SIPF](https://www.sipf.com.cn/dcpj/xxzs/index.shtml)). Verify live continuity before production. |
| **Variance risk premium (VRP)** | US-VRP1 analogue deferred: SSE 50/300 ETF-option market too thin & regime-shifting for a stable `IV²−E[RV]`; revisit once a clean point-in-time IV series exists (see also iVIX deferral). |

---

## Build sequence
1. Data spine w/ empirically verified publication timestamps: prices+breadth, 两融 (balance + 融资买入额), limit-up/down stats, futures basis, ETF shares, index valuation, TSF/M1/PMI/PPI/property calendar, R007/NCD; **v2.4 pipelines: IPO supply/demand (per-event, board×regime tagged, subscription/中签率/first-day/withdrawal), exchange+CFFEX option put/call, fund-fundraising by category.** Snapshot vintages going forward.
2. Layer 3 first (vol forecast, dispersion, panic flags): needed to evaluate everything else. *(**Local sub-sequence within the A-share parent's own build**; the global cross-document order is `Indicators_Pool_Combination_v1.md` §13.)*
3. Single-mechanism backtests with ablation (start: Policy-credit, Trend, and the fast-speculative-demand sub-composite: Mechanism Composites item 6, sleeve (a): the hypothesized-dominant mechanisms; that hierarchy is itself under test).
4. Cross-mechanism combination; redundancy audit (corr, stress-conditional corr, incremental OOS).
5. Vol-scaling as its own experiment.
6. Walk-forward across the structural-break table; report net-of-cost with uncertainty; fill-feasibility simulation for anything touching single names.
7. Fundamental stock-selection sleeve (child contract, §2.2b) runs as its own program, gated on the as-filed/预告 snapshot pipeline (child file §6), the longest-lead-time data item since vendors overwrite history.

## Sources
- [Market Timing: More than a Mirage, Man Group](https://www.man.com/insights/market-timing) (architecture)
- [HKEX: Stock Connect data-dissemination change](https://www.hkex.com.hk/News/Market-Communications/2024/2404122news?sc_lang=en) · [HKEX participant circular](https://www.hkex.com.hk/-/media/HKEX-Market/Services/Circulars-and-Notices/Participant-and-Members-Circulars/SEHK/2024/CT03824E.pdf)
- [SSE: ST price-limit change effective 2026-07-06](https://english.sse.com.cn/news/newsrelease/voice/c/c_20260708_10824778.shtml) · [BSE trading rules](https://www.bse.cn/jygl_list/200028217.html)
- [CSRC, suspension of 转融券](https://www.csrc.gov.cn/csrc/c100028/c7493852/content.shtml) · [SSE margin/securities-lending eligible list](https://www.sse.com.cn/lawandrules/sselawsrules2025/trade/specific/margin/c/c_20260710_10825136.shtml)
- [PBoC: M1 statistical-caliber revision, revised series](https://www.pbc.gov.cn/diaochatongjisi/attachDir/2025/12/2025121517172693949.pdf) · [NBS: PMI methodology](https://www.stats.gov.cn/english/PressRelease/202602/t20260202_1962478.html)
- [Northbound flows & A-share returns: time-varying dependence, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1057521926000827) · [time-varying interaction: ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1544612324011061) (mechanism research, pre-break data)
- [Baker & Stein: Market liquidity as a sentiment indicator](https://www.nber.org/papers/w8816) (conditional mechanism under short-sale constraints, fits A-share)
- [Baker & Wurgler 2006](https://people.stern.nyu.edu/jwurgler/papers/sentiment.pdf) (§2.4b anchor: China-adapted, not copied) · [China IPO-regime caveat (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243080) · [CSRC registration reform](https://www.csrc.gov.cn/csrc/c100028/c7123213/content.shtml) · [SSE options data](https://www.sse.com.cn/assortment/options/date/) · [China sentiment-composite literature](https://pmc.ncbi.nlm.nih.gov/articles/PMC7909732/)
- [Moreira & Muir](https://www.nber.org/papers/w22208) · [Cederburg et al.](https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X) (vol-scaling debate)
- [Goyal, Welch & Zafirov, equity-premium prediction update](https://academic.oup.com/rfs/article/37/11/3490/7749383) (evidence-grading rationale)
- [The All Weather Story: Bridgewater 2012](https://www.bridgewater.com/research-and-insights/the-all-weather-story) (local PDF in Reading Materials; architecture: cash+beta+alpha, environmental balance, not empirical validation)
- [Fed: Good Inflation, Bad Inflation](https://www.federalreserve.gov/econres/feds/good-inflation-bad-inflation-implications-for-risky-asset-prices.htm) (regime-dependent inflation sign) · [AQR: Leverage Aversion and Risk Parity](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf) (why leverage needs its own contract)
- Books folder: Narang (Layer architecture), Katsanos, Clenow.

---

## Appendix: revision history

Kept for provenance. Nothing below is needed to read the contracts above.

**Change log v2.7→v2.8 (F1 orientation sync):** F1 summary corrected to the child's value structure: **(EV) FCFF/EV primary** + conditional EBIT/EV, robustness EnterpriseCFO/EV·EBITDA/EV·NOPAT/EV·sales/EV (was stale `CFO/EV, FCF/EV`; unlevered numerators, §Fundamental F1).

**Change log v2.6→v2.7 (audit corrections):** CN-M2 flagged **heterogeneous** (RRR/MLF/LPR/OMO → split event sub-IDs or one frozen stance model, not equal votes); **CN-M9 downgraded to a *modelled* `registered/research` construct** (monthly ΔCAPB not directly observable; vintage/revision + seasonal-adjustment contract still TBD, no longer "proper impulse"); **CN-B3 self-contradiction fixed** (60th/90th are FIXED percentile rules, not trained breakpoints); **CN-V2 relabelled an earnings-yield − bond-yield spread / ERP *proxy*** (not a structural ERP).

**Change log v2.5→v2.6 (portfolio-risk states):** added **CN-R8 cross-asset risk appetite (RTI)**: global RTI as an external conditioning state first (domestic RTI grade C/D, deferred); risk-state not alpha; full contract in the shared `Indicators_Pool_PortfolioRisk_v1.md`.

**Change log v2.4→v2.5 (parent-state additions):** added **CN-M9 fiscal impulse (`FISCAL-CN`)**: the `POLICY` dictionary promised "fiscal" but had no row; built as Δ cyclically-adjusted primary balance + the special-bond/land-sale/special-treasury/implementation-vs-quota pipeline; conditioning state first, alpha only after OOS; new `FISCAL-CN` RG split out of `POLICY` (now "monetary stance"). (US VRP has no A-share analogue yet, deferred, thin options.)

**Child-integration pass (v2.4, alongside child Fundamental v1.4 / TrendReversal v1.3 / StatRisk v1.2 / MarketStructure v1.0):** §2.2b summary synced, added F2b `PROFIT_GROWTH`, financials-exclusion note in F1, F5 forecast-ROE revision, F6 q5 `EXPECTED_INVESTMENT_GROWTH` (own RG, +sign, CN D unverified), F7 `DBNETIS/AT`; sibling cross-refs to `SEASONAL`/`SYS-DEFENSIVE`; stock-level capacity, verified borrow, owner decomposition, price delay and crowding route to the Market Structure child.

**Change log v2.3→v2.4 (sentiment/capital-markets review):** added §2.4b **IPO/issuance exuberance** (Baker–Wurgler-inspired, institutionally adapted) split into **CN-CM-SUPPLY** (regulatory/issuance state, Grade C, regime-conditioned) and **CN-CM-DEMAND** (oversubscription, **`−log(中签率)` inverse lottery win-rate**, abandoned-subscription, %below-offer, board×regime normalized): with the registration-reform/44%-cap structural-break caveats; added CN-B7 exchange put/call (available without official iVIX), CN-B8 financing-purchase intensity (flow vs CN-B4 balance); decomposed CN-B6 fund issuance (raised assets, active/index/ETF/thematic split); Deferred additions (retail imbalance, 龙虎榜, CEF discount, SIPF continuity); horizon sub-composites. **v2.4 integration pass:** corrected CN-B7 CFFEX option codes (IO/HO/MO, no CSI500 index option); authoritative §6 composite rebuilt as sleeves with indicator-specific signs (CN-B5 = revealed participation not belief; CN-F1/F5 signs fixed; CN-F1 double-count removed by deleting old item-7 positioning composite); CN-CM-SUPPLY decomposed by sign with per-event dates; `R=unverified` flags on CN-CM-SUPPLY/CN-B5; CN-V5 RG normalized to `EARN-CN`; first-day return compounded.

**Change log v2.2→v2.3 (fundamental review):** cross-sectional fundamentals live in the child contract `Indicators_Pool_Fundamental_v1.md` (incl. the A-share 预告/快报 data regime, 扣非 profitability, 2024 payout/delisting regime dating). Here: new aggregate rows CN-V5 (earnings expectations), CN-V6 (quality-trend breadth), CN-V7 (net payout vs issuance/unlock supply), and §2.2b summary table of the child-contract families.

**Change log v2.1→v2.2 (All-Weather review):** added Layer 1.5: Economic Environment & Exposure Map (G_t/I_t surprise scores vs frozen consensus; **policy-credit and property retained as separate transmission variables**, not substitutes for growth/inflation; driver-risk dashboard); mandatory cash+beta+alpha+overlay−costs attribution; new CN-M0 (investable cash/policy return, distinct from the R007−DR007 stress spread); CN-M5 rebuilt as an explicit inflation-surprise family (CPI and PPI surprises separately + PPI−CPI margin-pressure gap); CN-X1 rebuilt as demand-vs-supply commodity decomposition; CN-R4 split into funding stress (R4a) vs equity liquidity (R4b); new CN-R7 CGB–equity correlation state (analogue of US-R8); driver-conditioned sector tests added to the sector child contract; "what not to import from All Weather" cautions; **fixed v2.1 leftover: CN-M4 note no longer suggests merging Jan+Feb PMI** (PMI is monthly, seasonally adjusted).

**Supersedes:** `Indicators_Pool_AShare_v1.md` (retained as idea catalogue).

**Change log v2→v2.1 (review round 2):** execution timing made consistent (default next-open; four timestamps per field; T+1-aware); falsification pre-registration + multiple-testing controls added; point-in-time universe requirement added (limit counts now % of eligible tradable universe); price-limit table corrected: BSE has no limit **only on the public-offering listing day**, 5-day no-limit applies to main board/ChiNext/STAR IPOs; **融券/转融券 distinction corrected** (2024 CSRC action suspended 转融券 refinancing lending; broker 融券 remains legal with scarce, security-specific borrow); Jan+Feb merging restricted to series NBS actually reports cumulatively (PMI is monthly, seasonally adjusted, not merged); 2016 circuit-breaker changed from "exclude or flag" to **flag and stress-test, never exclude**; credit impulse split into two defined candidates (credit acceleration vs flow/GDP impulse); M1 treated as two regimes rather than spliced; sector rotation split into child contract; dated low/base/high cost scenarios replace the 2× rule; mixed-frequency retail-heat composite split fast/slow; alphas also reported unscaled/ungated; secondary news links replaced by exchange/regulator sources.

**Change log v1→v2:** four-layer restructure (research contract / alpha hypotheses / risk-state model / implementation model); explicit per-indicator contracts with availability lags and evidence grades; **northbound flow corrected**: post-Aug-2024 official disclosure retains total turnover only, not the daily buy/sell split needed for net flow → live signal moved to Deferred, pre-2024 history usable for research with a hard break; **M1 structural-break policy added** (Jan 2025 redefinition, ~1 year comparable back-history); **price-limit table made board- and date-specific**: main-board ST/*ST limits ±5%→±10% effective **2026-07-06**, BSE ±30% added; nominal turnover "froth thresholds" replaced by rolling percentiles of turnover normalized by free-float; national-team activity moved to Deferred (no point-in-time identification); "top-tier/strong signal" language replaced by graded hypotheses; category composites replaced by mechanism composites; vol scaling demoted to tested risk policy.

**Framework reference (architecture, not evidence):** *Market Timing: More than a Mirage* (Man Group (2025). Used for the architecture) granular data, combining families, signals→exposure via risk estimates, not as validation of any indicator below.
