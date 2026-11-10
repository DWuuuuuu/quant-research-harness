# Quant Indicators Pool: US Market, v2.8 (Falsifiable Research Inventory)

The US counterpart to `Indicators_Pool_AShare_v2.md`, in the same four-layer form: research contract, alpha hypotheses, risk-state model, implementation. Each indicator carries an availability lag, an evidence grade, a sign hypothesis and a rejection rule fixed before any backtest. Supersedes `Indicators_Pool_US_v1.md`.

---

## Layer 1: Research Contract (defaults; every study must state deviations)

| Field | Default |
|---|---|
| Target market / instrument | S&P 500 total return. **Primary implementation: SPY.** **ES futures is a separate implementation contract** (roll schedule, collateral yield, margin, basis). Never interchangeable with SPY in a backtest. Sector rotation runs under a **child contract** (below). |
| Forecast targets | (i) excess return over T-bills, horizons 5d / 21d / 63d; (ii) realized vol next 21d; (iii) drawdown probability next 63d. Each hypothesis names ONE target. |
| Timestamps | Every field carries four: `observation ts` · `publication ts` · `decision cutoff` · `first executable ts`. Backtests join on publication ts and trade at first executable ts. |
| Decision & execution | **Default: signal frozen at close t → execute at open t+1 (or t+1 VWAP).** Same-close execution is permitted only when every input is frozen before a stated order cutoff (e.g., 15:45 ET) and the stored history reflects that cutoff. Close-derived values (index closes, VIX settlement, breadth, ETF shares outstanding) are never executable at the same close. |
| Positions | Long-only 0–100% initially; leverage cap 1.0; futures overlay (incl. short) as later extension under its own contract |
| Benchmark | Buy-and-hold SPY total return; secondary 60/40. Child contracts define their own benchmarks. |
| Costs | Dated low/base/high scenarios per instrument (2026 baseline): SPY 0.5 / 1 / 3 bps half-spread+impact per side; sector ETFs 1 / 3 / 8 bps. **Acceptance criterion: net edge remains positive with adequate uncertainty margin under the high (stressed) scenario**. no arbitrary multiplier. |
| Point-in-time universe | Breadth, new-highs, dispersion, and sector studies require historical index constituents with additions/deletions, delistings, and corporate actions as of each date. No current-membership shortcuts. |
| Evaluation | Nested walk-forward (model selection inside, evaluation outside); **locked final holdout** untouched until sign-off; **multiple-testing control** across the indicator × transform × horizon grid (deflated Sharpe / FDR); **block-bootstrap or HAC uncertainty** for overlapping 21d/63d targets; every alpha also reported **unscaled and ungated** so the risk overlay cannot act as hidden feature selection; ablation per component. |

**Pre-registration (required per hypothesis before any backtest):** primary target & horizon · expected sign/shape · primary metric · minimum economically useful effect net of stressed costs · minimum sample and subperiod-stability requirement · explicit rejection rule (e.g., "reject if OOS net contribution ≤ 0 or sign flips in >1/3 of 5y subperiods"). The failure-regime notes in the tables are context, **not** a substitute for this.

**Child contract, sector rotation:** universe = point-in-time sector membership; benchmark = equal- or cap-weight sector basket (not SPY); monthly rebalance default; own turnover and cost scenarios; target = sector return minus basket return.

**Evidence grading (three dimensions):** each indicator scores **E** (empirical evidence: A replicated across markets/samples · B market/regime-specific · C exploratory · D none/contradicted), **P** (portability to this market/instrument), **R** (data readiness: point-in-time availability verified). The `Gr` column shows the **E** dimension; where **P** or **R** is the binding constraint it is flagged in the row or the item sits in Deferred. Full E/P/R triples + one primary citation per indicator go into the research tracker at coding time.

**Redundancy groups (RG):** composites are built per *mechanism*, and correlation/ablation is tracked within group. Never treat two same-RG signals as diversification.
`CREDIT` credit-risk pricing · `FUNDING` money-market stress · `RATES` policy path & curve · `GROWTH` real-activity nowcast · `INFL` inflation/discount rate · `USD` dollar liquidity · `VALUE` long-run valuation · `EARN` earnings fundamentals · `CAPALLOC` capital allocation (v2.3) · `TREND` price continuation · `REV` short-horizon reversal · `BREADTH` participation · `SENT` sentiment (contrarian at extremes) · `POSITION` self-reported/derivative positioning · `INFORMED-POS` informed positioning (insiders, short interest: NOT contrarian) · `NEWS` news/narrative tone · `ISSUANCE-HEAT` capital-markets exuberance (IPO/equity issuance) · `LEV` leverage/crowding · `FLOW` fund flows · `XGROWTH` cross-asset growth pricing · `HAVEN` safe-haven demand · `VAR-RISK` option-implied variance risk premium (Layer-2 alpha) · `RISK-APPETITE-XA` cross-asset risk-appetite state (Layer-3, not vol) · risk-layer groups: `VOL`, `CORR`, `LIQ`. *(v2.4 added POSITION, INFORMED-POS, NEWS, ISSUANCE-HEAT; v2.6 added VAR-RISK, RISK-APPETITE-XA.)*

---

## Layer 1.5: Economic Environment & Exposure Map (v2.2)

*Architecture from* The All Weather Story *(Bridgewater 2012) and the Man Group level-vs-timing decomposition, both treated as architecture, not empirical validation. Bridgewater's paper is its own narrative and discloses no reproducible specification.*

**Attribution (mandatory in every backtest report):** decompose total return into `cash + passive beta + tactical timing + risk-overlay effect − costs`. A long/flat strategy earns cash while flat (US-M0). Any timing-skill claim refers to the *timing* component only. Never the blend.

**Environment scores:** `G_t` = standardized growth surprise, `I_t` = standardized inflation surprise. "Surprise" = actual outcome minus the **frozen consensus or market-implied expectation immediately before release**. Never "improving vs last month." Consensus snapshots must be point-in-time.
- `G_t` inputs: ISM new-orders surprise, payrolls/claims, retail sales/IP, GDP-nowcast revisions, earnings-revision breadth (US-M5, US-V3).
- `I_t` inputs: CPI/PCE/PPI surprises; breakeven *changes* tracked separately (realized-inflation news ≠ market repricing) (US-M6, US-M8).

**Three uses:** (1) **label** the environment; (2) **condition**: every alpha family is tested within environments; macro state variables enter as a conditioning/evaluation layer first and are promoted to directional alpha **only if independently predictive OOS**; (3) **expose**. Report the tactical portfolio's rolling beta to growth surprises, inflation surprises, rates, and liquidity shocks (**driver-risk dashboard**: risk concentration in economic-driver space, not just vol and pairwise correlations). A joint 2×2 regime table (G↑/↓ × I↑/↓) is permitted as **our research extension**: Bridgewater assigns risk to four driver directions, not a joint regime classifier.

**Inflation has no fixed sign for equities:** inflation news is "good" or "bad" depending on its relation to growth ([Fed research](https://www.federalreserve.gov/econres/feds/good-inflation-bad-inflation-implications-for-risky-asset-prices.htm)): hence the regime-conditional signs on US-M6/US-M8 and the US-R8 state variable.

**What NOT to import from All Weather:** (1) equal risk across the four environments is a portfolio-design **prior**, not evidence the regimes are equiprobable; (2) "betas outperform cash" and "similar return per unit of risk" are hypotheses, not laws; (3) risk parity ≠ inverse-vol weighting, a leveraged multi-asset implementation requires its own contract (futures rolls, financing, collateral, margin, stress deleveraging; [AQR: Leverage Aversion and Risk Parity](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf)) and is **out of scope here**; leverage cap stays 1.0. In these files All Weather supplies: a strategic baseline, a macro-state classification, conditional robustness tests, and a risk-concentration diagnostic.

---

## Layer 2: Alpha Hypotheses

Columns: **Raw → transform** · **Target/horizon** · **Lag** (availability after reference period) · **Hypothesis & failure regime** · **RG** · **Gr**(ade).

### 2.1 Macro & policy mechanisms

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-M0 | Cash & real-cash return (v2.2) | 3m T-bill yield/return; ex-ante real cash = T-bill − expected inflation (surveys/breakevens) | attribution baseline + state | same day | The return earned while flat: mandatory in Layer 1.5 attribution. High real cash raises the hurdle for holding equity risk (state variable, not directional alpha). | RATES | B |
| US-M1 | Yield-curve slope | FRED T10Y3M → level & 63d change | Recession prob / 63d–1y equity excess | same day | Inversion raises recession odds 12–18m out; **not** reliably bearish for 1–3m equity (equities often rally post-inversion). Fails when inversion driven by term-premium distortion (QE). | RATES | B |
| US-M2 | IG / HY OAS | FRED BAMLC0A0CM, BAMLH0A0HYM2 → rolling z of level + 21d change | 21–63d equity excess; DD prob | 1 day | Widening (esp. rapid Δ) precedes equity stress; *change* > level. Fails in supply-driven widening w/o default-risk change. | CREDIT | B |
| US-M3 | Fed path repricing | Fed funds futures implied path → 21d Δ in expected rate 12m ahead | 21–63d equity excess | same day | Dovish repricing bullish **iff** growth stable; easing that is endogenous to deteriorating growth is not bullish (sign flips in recession onset). Must be conditioned on GROWTH state. | RATES | B |
| US-M4 | Financial conditions | Chicago Fed NFCI → level + 13w Δ | 21–63d equity excess | ~1 wk | Tightening conditions bearish; partly *contains* equity prices (endogeneity. Do not treat as independent confirmation of TREND). | CREDIT/FUNDING mix | B |
| US-M5 | Growth nowcast | ISM mfg new orders; weekly claims (4w MA); GDPNow → surprise vs consensus & 3m Δ | 21–63d equity excess | ISM: 1st biz day; claims: weekly Thu | Improving growth surprise bullish for cyclicals/beta. Fails late-cycle when "good news = higher rates." Regime-conditional sign. | GROWTH | B |
| US-M6 | Inflation surprise (**realized data only**: breakevens live in US-M8, do NOT double-count) | CPI/PCE vs consensus (**5y5y breakevens Δ removed: that market-repricing component is owned by US-M8; Layer 1.5 keeps realized-inflation and market-repricing separate**) | 21d equity excess; RATES regime | CPI ~2 wks after month | Upside surprise bearish via discount rate when inflation above target; sign weakens when inflation at/below target. | INFL | B |
| US-M7 | USD / dollar liquidity | DXY 63d Δ (real-yield component moved to US-M8, v2.2) | 21–63d equity excess (growth/tech, EM) | same day | Strong USD tightens global liquidity → bearish risk assets. Fails when USD strength reflects US growth exceptionalism. | USD | B |
| US-M8 | Nominal-yield decomposition (v2.2) | Δ10y split into real-yield (TIPS) + breakeven components | 21–63d equity excess; `I_t` input | same day | Real-yield-driven rate rises bearish for long-duration equities; breakeven-driven rises have regime-dependent sign (good/bad inflation: Layer 1.5). Core All-Weather-style macro decomposition, not a USD adjunct. | INFL | B |

### 2.2 Valuation & fundamentals

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-V1 | CAPE / E-P percentile | Shiller CAPE → percentile vs trailing 30y | 5–10y expected return; strategic tilt only | monthly | High CAPE → low long-run returns. **No tactical power** (Welch–Goyal: most valuation predictors weak OOS; AQR: "sin a little" at best). Never a 21d signal. | VALUE | B |
| US-V2 | **ERP proxy (Fed-model-style), NOT a structural implied ERP** | Forward E/P − 10y TIPS | Strategic tilt; 1y+ | daily (E est. weekly) | Higher spread → better long-run equity vs bonds. **This is an earnings-yield-minus-real-yield *valuation spread*, not a cash-flow-implied equity risk premium**: label it a proxy; use a **cash-flow-implied ERP** (dividend/buyback-discount model) as a robustness variant. Same OOS caveats. | VALUE | B |
| US-V3 | Aggregate earnings expectations (v2.3) | index-level EPS revision breadth + magnitude + analyst dispersion → 4w MA, z | 21–63d index & sector | ~weekly | Rising aggregate revisions bullish; dispersion spike = uncertainty regime. Fails at inflections (analysts lag). Firm-level revisions/SUE → child contract F5. | EARN | B |
| US-V4 | Aggregate capital allocation (v2.3) | market net payout yield = (div + executed repurchases − issuance)/mcap; Δ diluted shares | Strategic, 63d+ | quarterly, ~45d filing lag | Net distribution regime bullish; issuance waves bearish (supply). Track executed buybacks via issuer-purchase tables/share counts, never announcements (Form 4 = insider activity only). Firm-level → child F7. | CAPALLOC | B |
| US-V5 | Aggregate quality trend (v2.3) | % of firms improving ROE / margins / cash conversion (breadth, not cap-weighted level) | 63d+; regime confirm | quarterly, ~45d lag | Broadening fundamental improvement confirms GROWTH; narrowing quality breadth under rising index = late-cycle warning (hypothesis). Firm-level quality → child F2–F4. | EARN | C |

### 2.2b Cross-sectional fundamental families, child-contract summary (v2.4)

**These are stock-selection factors, not index-timing signals.** They trade under `Indicators_Pool_Fundamental_v1.md` (own universe, benchmark, rebalance, costs, evaluation); only the aggregate rows above (US-V3/V4/V5) feed this timing file. Summary for orientation:

| Family | Core measures | Role | US Gr |
|---|---|---|---|
| F0 Size | mcap | **control only**: mandatory in all attribution; not alpha | n/a |
| F1 Multi-metric value | **(EQ)** E/P, fwd E/P, B/P · **(EV, unlevered numerators)** FCFF/EV (primary), EBIT/EV · robustness: EnterpriseCFO/EV, EBITDA/EV, NOPAT/EV, sales/EV: sector-relative; equity-vs-enterprise base tagged (child §1); financials → `Indicators_Pool_Financials_v1.md` (own contracts) | core | B |
| F2 Profitability | GP/assets, operating profitability, ROA/ROIC; ROE only leverage-decomposed (DuPont) | core | A |
| F2b Profit growth (`PROFIT_GROWTH`, v1.4) | realized ΔROA/ΔROE/Δmargin (**+sign**; Δlevel primary, Δ² separate variant); YoY | fundamental improvement; ablate vs F2 level | B |
| F3 Earnings/cash quality | accruals/assets, CFO/NI, FCF conversion | quality component (standalone anomaly decayed) | B |
| F4 Financial strength | net debt/EBITDA, coverage, debt/assets; Z/O-score (diagnostic); **distance-to-default → hybrid market/fundamental overlay (StatRisk-adjacent), not pure F4** | core | B |
| F5 Fundamental/event momentum (RG EARN_EVENT) | SUE, **CAR/ABR[-2,+1]**, revision ratio·magnitude·dispersion, **forecast-ROE revision** (expectation-based; realized ΔROE → F2b); event horizons 5/21/63d; PEAD/FIN betas = risk-attribution only | core; overlaps price momentum: redundancy-test | A (decay documented) |
| F6 Investment / asset growth | total asset growth, capex/assets, NOA growth (real-investment, **−sign**; **debt issuance → F7, debt level → F4**); **q5 `EXPECTED_INVESTMENT_GROWTH` own RG, +sign OPPOSITE to realized investment. Never composited with F6** (US B research · CN D unverified) | research tier; condition on F2/valuation | B |
| F7 Capital allocation (RG CAPALLOC) | net payout yield; Δ diluted shares; **NSI-1Y, CSI-5Y, FIN composite**; **net debt issuance JKP `DBNETIS/AT`** (not ΔNetDebt): all reconcile, don't multi-count | core-expand | B |
| F8 Governance/forensics | audit opinion, restatements, control weaknesses | **risk screen**, not symmetric alpha | screen |
| Overlays | stability embedded in quality; intangibles as fixed-parameter alternate spec (no tuned amortization) | measurement | n/a |
| Contextual score / expectation-error overlays (child v1.4) | Piotroski F-Score **within value**; Mohanram G-Score **within growth**; Piotroski–So `B/M 30/40/30 × F-Score 0–3/4–6/7–9` matrix | stage-2 research alternatives that repackage F2/F3/F4/F6/F7; **not additive families, not arithmetic B/M×F-Score** | B |

**Cross-sectional siblings (not in this timing file):** price-based → `Indicators_Pool_TrendReversal_v1.md` (incl. **T-X8 `SEASONAL`**); statistical-risk → `Indicators_Pool_StatRisk_v1.md` (IVOL/MAX/skew lottery + **R-X6 `SYS-DEFENSIVE`** low-beta, defensive-first); market structure → `Indicators_Pool_MarketStructure_v1.md` (stock-level capacity/cost/shortability, institutional ownership, price delay/news×constraint and crowding; parent funding state is only a conditioning input).

Initial production structure (child v1.4): **slow monthly sleeve** = F1 + quality(F2 profitability + stability) + **F2b PROFIT_GROWTH** with F3/F4/F8 as **one-sided penalties**; **event sleeve** = F5 (SUE + CAR/ABR + forecast-ROE revisions). F-Score/G-Score and the expectation-error matrix are stage-2 contextual variants, evaluated by ablation against the broad Value+Quality baseline. Sleeves combine at allocation level, never signal-averaged; slow families tested at 126/252d primary horizons, F5 at event horizons. F6 (−sign) / q5 EXPECTED_INVESTMENT_GROWTH (+sign, separate) / F7 on incremental OOS value. Full contracts: child file §§1–4.

### 2.3 Trend & reversal (transformations of price. Never "leading" by construction)

> **Scope (v2.3):** these rows are **index/sector timing** only. Cross-sectional individual-stock momentum & reversal (PRICE_MOM, RESID_MOM, REV_SHORT, REV_LONG, MOM_PATH) live in the sibling child contract `Indicators_Pool_TrendReversal_v1.md`; earnings-event continuation (CAR/PEAD) lives in fundamental F5. Do not add MACD/RSI/ROC/MA variants as new families, they are parameter variants of the same past-price information inside `TREND`.

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-T1 | Time-series momentum | 12-1m, 6m, 3m excess return sign/z | 21–63d excess return | none | Positive TSMOM → continuation. **Grade-A evidence is diversified multi-asset futures (Moskowitz–Ooi–Pedersen); single-index US equity timing is weaker**. Treat index-only trend as B. Fails in sharp V-reversals (2020-03/04) & choppy ranges. | TREND | A(multi-asset)/B(single-index) |
| US-T2 | MA filter (50/200d) | price vs MA, crossovers | 21–63d; regime gate | none | Above-MA = continuation regime. Redundant with US-T1 (same RG: pick one or blend, never count twice). | TREND | B |
| US-T3 | Cross-sectional sector momentum | 6-1m sector RS rank | 21–63d sector relative | none | Winners persist. Crash risk when vol spikes (momentum crashes, Daniel–Moskowitz). | TREND | A(x-sect generally)/B(sectors) |
| US-T4 | Short-horizon reversal | 1–5d index return z; RSI(2–14) | 1–5d | none | Extreme short-run moves partially revert. Modest in US indices post-2000; costs bite; fails in trending crashes. | REV | C |
| US-T5 | 52-week-high proximity | price / 252d max | 21–63d | none | Near-high = continuation (anchoring). Overlaps TREND heavily: same RG. | TREND | B |

### 2.4 Breadth & participation

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-B1 | % constituents > 200d MA | breadth level + divergence vs index (63d) | 21–63d; DD prob | none | Narrow breadth under rising index → elevated correction risk. Divergence signals are rare → wide CIs; mega-cap concentration eras (2023–24) generate false warnings. | BREADTH | B |
| US-B2 | Net new 52w highs | NH−NL → 21d MA | 21d | none | Same mechanism as US-B1 (same RG). | BREADTH | B |

### 2.5 Sentiment & positioning (sign depends on family, contrarian for SENT, NOT for INFORMED-POS/NEWS; all lag-aware)

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-S1 | AAII / II bull-bear | spread → percentile vs 5y | 21–63d, contrarian at extremes | AAII: weekly Thu | Extreme pessimism → above-avg fwd returns. Mid-range readings uninformative. Small-sample survey noise. | SENT | B |
| US-S2 | Equity put/call | **Core public variant:** aggregate CBOE ratio → 5d MA percentile. **Licensed research variant (do not splice histories):** customer-opening / small-trade ratio (Cboe Open-Close/DataShop) | 5–21d contrarian | after close → next session | Extreme puts = washout. Raw ratio distorted by early exercise, dealer/hedging flow and post-2021 0DTE ([Cboe](https://www.cboe.com/insights/posts/how-early-exercise-order-flow-impacts-equity-option-put-call-ratios)); small-trade/customer-only avoids some of it but is a *different data contract*. | SENT | C |
| US-S3 | NAAIM exposure | level percentile | 21d contrarian | weekly Thu | Manager exposure extremes fade-able. Short history (2006–). | POSITION | C |
| US-S4 | Net margin leverage (v2.4, was "margin debt") | **Primary:** `ML_net = (Debit − FreeCredit_cash − FreeCredit_margin)/mcap`. **Robustness (don't average):** `ML_ratio = Debit/(FreeCredit_cash+FreeCredit_margin)`. → YoY Δ, z | **Strategic only (63d+)** | **~3 weeks after measurement month-end** | Rapid leverage build = fragility; unwind = capitulation. Audit FINRA reporting-methodology breaks. **Latency unusable at short horizons.** | LEV | B |
| US-S5 | CFTC COT (E-mini, VIX futs) | net spec positioning percentile | 21–63d contrarian at extremes | **weekly; Fri release of Tue data (3-day lag)** | Crowded spec positioning at extremes precedes reversals. Weekly signal only; index-futures COT ambiguous (hedgers dominate). | POSITION | C |
| US-S6 | Fund flows (ICI/EPFR) | 4w equity flow z | 21–63d, contrarian at extremes | weekly, ~1wk lag | Persistent retail inflow extremes late-cycle marker. Detrend for structural passive-flow drift. | FLOW | C |
| US-S7 | Insider net buying (Form 4) | agg net buy ratio → 21d | 63d+ | 2 biz days per filing | **Reclassified SENT→INFORMED-POS (v2.4): informed corporate positioning, not uninformed investor psychology.** Cluster buying after selloffs bullish; cross-sectional evidence stronger than index-level. | INFORMED-POS | B |
| US-S8 | Yale confidence indices | 1y / buy-on-dip / crash / valuation confidence → percentile | 21–63d contrarian | monthly; **`R = unverified`: confirm Yale ICF release-day convention before coding** | **Direct beliefs**: conceptually cleaner than price proxies but survey-noisy ([Yale ICF](https://yale-icf.github.io/ShillerUSConfidence/)). | SENT | C |
| US-S9 | Aggregate short interest | short interest / float → detrended z | 21–63d | **twice monthly; public dissemination several biz days after settlement date: join on FINRA schedule** | **Informed bearish positioning, not sentiment**: aggregate SI carries market-return information. | INFORMED-POS | C |
| US-S10a | Daily news pessimism → pressure | **licensed/reconstructed timestamped DAILY news z** (the public SF-Fed series is weekly-published, so much of the 1–5d pressure is already realized before release: the public series CANNOT support this immediate-pressure hypothesis; deferred to a daily-news data contract) | **1–5d downward pressure at extreme pessimism** | daily (licensed): else `blocked-by-data` | Media pessimism → temporary downward pressure ([Tetlock](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2007.01232.x)). | NEWS | C (blocked on public data) |
| US-S10b | News → subsequent reversion | SF Fed news 4w-change z | **separate hypothesis: 5–21d reversion after the pressure** | weekly | Split from US-S10a (two distinct targets). | NEWS | C |

### 2.5b Capital-markets exuberance, Baker–Wurgler sleeve (v2.4, slow contrarian)

*Anchor: [Baker–Wurgler 2006](https://people.stern.nyu.edu/jwurgler/papers/sentiment.pdf): firms/underwriters supply more equity when investors are unusually willing to buy hard-to-value securities. Two caveats baked in: (1) B–W is primarily a **cross-sectional** result (high sentiment hits young/small/volatile/unprofitable/non-dividend/hard-to-arbitrage names hardest): it is **not** by itself proof of aggregate market timing; (2) the published index uses **annual data + full-sample PCA**: for deployment use **PIT monthly / trailing-12m inputs and expanding/rolling estimation, never full-sample PCA** (look-ahead). "Baker–Wurgler-inspired," not a mechanical copy.*

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-CM1 | IPO supply | trailing-K-month (predeclared 3/6/12m) IPO count & proceeds / total mcap → detrended | 6–24m, contrarian at extremes | **join per-event: pricing date, listing date: not "month-end"** | High supply = receptive market → lower long-run returns. Supply also driven by regulation/underwriting capacity, not pure sentiment. | ISSUANCE-HEAT | C |
| US-CM2 | IPO demand | **directions explicit:** `+`first-day return (market-adj), `+`price revision (vs filing midpoint), `+`oversubscription, `−`withdrawal, `−`broken-issue. Rolling composite (below), EW-mean for B–W replication + median/trimmed for robustness | 3–24m, contrarian at froth | **per-event, staggered by field:** offer-to-open at open t; first-day at close t; withdrawal known at withdrawal date | First-day return is demand **but also** underpricing/info-asymmetry/risk ([Derrien](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=687132), [Guo](https://homepages.uc.edu/~guohu/publications/IPO_GUO2009.pdf)). Offer-valuation-vs-comps is a **pricing control, not a demand vote**. | ISSUANCE-HEAT | C |
| US-CM3 | Equity share of issuance | equity issuance / (equity + LT-debt issuance) → z; **test raw + rolling-orthogonalized (never full-sample)** | 6–24m, contrarian at extremes | **aggregate flow series, not one filing: `R = unverified`: name the issuance database (SDC/Refinitiv or Fed Z.1 flows) & its release convention before coding** | High equity share = managers exploiting receptive equity investors. **Cross-ref fundamental F7 CAPALLOC: simultaneously sentiment, financing supply & corporate timing.** | ISSUANCE-HEAT | C |
| US-CM4 | Follow-on (SEO) issuance | SEO proceeds / mcap | 6–24m | quarterly | Combine with US-CM1 **only after redundancy test** (IPO/SEO/equity-issuance highly correlated → one RG, not three votes). | ISSUANCE-HEAT | C (research) |
| US-CM5 | SPAC heat | issuance, redemptions, de-SPAC activity | regime-specific | monthly | Regime-specific (2020–21) research candidate. | ISSUANCE-HEAT | C (research) |

**US-CM2 rolling sparse-event convention (v2.4, a monthly composite can't vanish when issuance is thin):**
**compounded market adjustment** (cleaner for large IPO returns): `IR_i = (C_i,1/P_i,offer) / (I_listing-close/I_pricing-close) − 1`; `RIPO_t = median{ IR_i: i listed in trailing K months }`, K∈{3,6,12} predeclared, **minimum event count (e.g. 5) or the composite is missing.** Missingness is **component-specific**: withdrawal rate stays observable in zero-completed-IPO months.

**Baker–Wurgler six-proxy mapping (explicit, v2.4):**

| Original B–W input | Treatment here |
|---|---|
| Number of IPOs (NIPO) | US-CM1 |
| IPO first-day return (RIPO) | US-CM2 |
| Equity share of issuance | US-CM3 |
| Detrended turnover | **research/excluded**: modern US turnover institutionally & mechanically contaminated (no core row) |
| Closed-end fund discount | **Deferred/historical replication** |
| Dividend premium | **Deferred (research tier)**: overlaps quality/value/dividend style (see Deferred table) |

Raw and macro-orthogonalized issuance variants both tested; **orthogonalization rolling/expanding only** (full-sample = look-ahead).

**Sub-composites: see the authoritative table in Mechanism Composites §7 (single source of truth. Do not duplicate here).**

### 2.6 Cross-asset confirmations

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-X1 | HY vs Treasury relative (HYG/IEF) | 21–63d relative return | 21d equity excess | none | Credit-risk pricing in tradable daily form. **Same RG as US-M2. Never both in one composite.** | CREDIT | B |
| US-X2 | Commodity complex, demand-vs-supply decomposition (v2.2) | copper/gold ratio + broad basket (BCOM) + oil: demand-driven strength vs supply shocks scored separately | 21–63d cyclical vs defensive; `G_t` vs `I_t` inputs | none | Demand-driven commodity strength = growth pricing (feeds `G_t`); supply-shock strength = inflationary with regime-dependent sign (feeds `I_t`). Copper/gold alone is too narrow; China-demand idiosyncrasies distort copper. | XGROWTH | C |
| US-X3 | Defensive leadership (XLU/XLP vs SPY) | 21–63d RS | 21–63d; DD prob | none | Defensive leadership precedes risk-off. Partly redundant with BREADTH/CREDIT. Verify incremental value. | XGROWTH | C |
| US-X4 | Gold + long-bond bid | 21d joint z | risk-off state confirm | none | Joint haven bid confirms flight-to-quality. Breaks when inflation makes bonds risky (2022: both fell with equities). | HAVEN | C |

### 2.7 Volatility risk premium (option-implied; v2.6, moved here from Layer 3)

| ID | Indicator | Raw → transform | Target/horizon | Lag | Hypothesis & failure regime | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-VRP2 | **VIX-extreme / fear contrarian return** (v2.6, moved from Layer-3 US-R2b): **NOT a variance-risk-premium measure** (VIX-extreme conflates expected physical variance *and* the variance premium; Bekaert–Hoerova separate them: the genuine VRP is US-VRP1) | VIX percentile vs 5y, extremes only | **21–63d equity excess at VIX extremes** (fear-contrarian compensation: directional alpha, hence Layer 2) | same day | Split from the vol-forecast use (US-R2a stays in Layer 3). Redundancy-test vs US-VRP1. | VAR-RISK | B (research) |
| US-VRP1 | Variance risk premium | `VRP_t = IV²^Q_{t,H} − E_t^P[RV_{t,t+H}]`: **both terms same horizon H, same annualization, variance units (not vol)**; `E_t^P[RV]` is a **time-t ex-ante HAR/GARCH forecast** | **21–63d equity excess return** (directional alpha: hence Layer 2, not Layer 3) | same day (declare close + next-executable ts) | **Using realized `RV_{t,t+H}` leaks the future: the primary VRP look-ahead error.** If VIX² is the implied term it is a ~30-calendar-day annualized variance object (match H accordingly). High VRP → higher subsequent returns (variance-risk compensation); OOS evidence beyond the VIX level ([Fed](https://www.federalreserve.gov/pubs/feds/2011/201152/index.html), [JFE](https://www.sciencedirect.com/science/article/pii/S0304405X18302782)). **Redundancy-test vs US-R2a VIX-level vol forecast & US-R3 term structure.** | VAR-RISK | B (research) |

*(A separate option-implied-variance measure used to **forecast future volatility** would belong in Layer 3; that is a different object and is deferred. Do not conflate with this return predictor. China VRP remains deferred, thin options.)*

---

## Layer 3: Risk / State Model (forecasts risk, sizes positions; NOT alpha)

| ID | Indicator | Raw → transform | Forecast | Lag | Notes | RG | Gr |
|---|---|---|---|---|---|---|---|
| US-R1 | Realized vol ratio | 21d RV / 252d RV | next-21d vol | none | **Volatility persistence** (clustering = high follows high, low follows low) is Grade-A. "Low vol precedes spikes" is a *separate, weaker* hypothesis. Test independently, don't assert. | VOL | A (persistence) |
| US-R2a | VIX level → vol forecast | percentile vs 5y | **next-21d realized vol** (the only Layer-3 use of VIX level) | same day | High VIX → high fwd RV (persistence). *(The VIX-extreme **contrarian-return** hypothesis is a Layer-2 return predictor: moved to §2.7 as `US-VRP2`, not a risk-state.)* | VOL | A |
| US-R3 | VIX term structure | VIX/VIX3M; front VX futures slope | vol regime; DD state | same day | **Convention corrected from v1: backwardation (near > far) = elevated near-term fear/stress = de-risk trigger; contango is the calm norm** whose *steepness* mainly reflects vol risk premium. | VOL | B |
| US-R4 | GARCH / HAR vol forecast | daily RV → model forecast | next 1–21d vol | none | Standard, robust. Feeds position sizing. | VOL | A |
| US-R5 | Implied correlation / dispersion | CBOE COR indices; avg pairwise 63d | diversification state | same day | Rising correlation = diversification failing → cut gross. | CORR | B |
| US-R6a | Funding stress | SOFR-OIS spread; GC repo − IORB | funding-stress state | **1 day: SOFR published ~8:00 ET next business day for prior day's transactions** ([NY Fed](https://www.newyorkfed.org/markets/reference-rates/sofr)) | **Replaces TED (discontinued Jan 2022).** Spikes = de-risk override. | FUNDING | B |
| US-R6b | Market liquidity | Amihud illiquidity & quoted spreads on SPY | equity-liquidity state | close-derived → t+1 executable | Different mechanism from funding stress: separate contract, separate ablation. | LIQ | B |
| US-R7 | Drawdown state | current DD from 252d high | state descriptor | none | Conditions which alpha families are active (e.g., disable REV in deep DD). | VOL | n/a (descriptor) |
| US-R8 | Bond–equity correlation sign | 63d rolling stock–bond corr | inflation-regime / hedge-validity descriptor | close-derived → t+1 | **Moved from alpha layer in v2.1**: regime descriptor, not alpha. Positive corr → bond hedge fails → cut gross. | CORR | B |
| US-R10 | **Cross-asset risk appetite (RTI, v2.6)** | Spearman rank-corr of recent asset-class returns vs ex-ante risk ranks (`Indicators_Pool_PortfolioRisk_v1.md` §PR-R1) | risk-state (not alpha); extremes only, via rolling percentile | weekly | **Risk-state, NOT direction**: pair with an absolute state (trend/drawdown/vol/credit); never sets long-vs-cash alone. **Gated on incremental value over US-R8/US-X3/US-X4/US-X1/US-R1–R4** (likely a consolidation of them, not new info). BlackRock-inspired, not a replication. Grades: **E:C · P:B/C · R:C**. Full contract in the Portfolio Risk child. | RISK-APPETITE-XA | C |

*Price-derived regime gates (e.g., US-T2 when used as a gate rather than a signal) are evaluated in this layer too, and every alpha must also be reported ungated and unscaled (Layer 1, Evaluation).*

*Reserved identifier: **US-R9** was the former Layer-3 VRP slot, the VRP **return predictor** now lives in Layer 2 §2.7 as `US-VRP1`. US-R9 is retired (no active row) to avoid a valid-looking empty ID in table ingestion; a future option-implied **vol-forecast** state, if built, would take a fresh Layer-3 ID.*

**Volatility-scaling policy (tested, not automatic):** Moreira–Muir (2017) report gains from vol-managed exposure; Cederburg et al. (2020, JFE) find no systematic real-time improvement across 103 strategies. Therefore: vol targeting is a **candidate risk policy** evaluated in its own ablation, with leverage cap 1.0 (long-only), vol-forecast smoothing (e.g., 5d), trade deadband to cap turnover, and full cost accounting. Never silently applied to every signal.

---

## Layer 4: Implementation Model

- **Availability discipline:** every series carries `(reference period, public timestamp)`; backtests join on public timestamp. Key lags: ISM: 1st business day; CPI: ~2 weeks; COT: Fri for Tue; **FINRA margin: ~3 weeks after measurement month-end; FINRA short interest: twice-monthly, several biz days after settlement (join on FINRA schedule); SF Fed news: published weekly; IPO fields: staggered per-event (pricing / listing / withdrawal dates)**; ICI flows: ~1 week; Form 4: 2 business days.
- **Revisions:** macro series (claims, GDPNow inputs, NFCI) revised. Use point-in-time vintages (ALFRED) where the signal depends on levels.
- **Costs/capacity:** governed by the Layer 1 dated low/base/high scenarios; acceptance under the stressed (high) scenario. (v2.2: obsolete 2× rule removed.)
- **Structural breaks to encode:** 2021– 0DTE options distort put/call and VIX-complex comparisons; passive-flow secular trend in fund flows; QE/QT eras distort curve signals (US-M1).
- **Execution:** governed by the Layer 1 decision & execution contract, default next-open (or t+1 VWAP); same-close only with a pre-cutoff freeze reflected in stored history. (v2.2: superseded ambiguous bullet removed.)

---

## Mechanism Composites (replaces v1 "one per category")

Build one composite per mechanism, verify pairwise/conditional correlations and run ablations *before* combining across mechanisms. **Frequency discipline (v2.1): never average mixed-frequency inputs into one score, build fast (daily), medium (weekly), slow (monthly+) sub-composites per mechanism and combine at the allocation level:**

1. **Credit stress** = US-M2 *or* US-X1 (same RG, choose by data quality) + US-R6a funding overlay
2. **Policy/rates** = US-M3 conditioned on Growth state (US-M5): sign is regime-dependent by design
3. **Growth nowcast** = US-M5 (+US-X2 as tradable daily confirm, if incremental)
4. **Valuation tilt** (strategic only, 1y+) = US-V1/V2
5. **Trend** = one of US-T1/T2/T5 (single RG) + US-T3 for the sector child contract
6. **Participation** = US-B1 (US-B2 redundant)
7. **Sentiment/positioning/exuberance, six sleeves with indicator-specific signs (v2.4, authoritative single source of truth). No blanket "contrarian"/"not-contrarian" label, each row carries its own sign.**

   | Sleeve | Horizon | Components (sign) |
   |---|---|---|
   | Fast sentiment | days–wks | US-S2 options (contrarian at clean extremes); retail order flow *deferred* |
   | Direct beliefs | 1–3m | US-S1 surveys + US-S8 Yale confidence (contrarian at extremes) |
   | Slow issuance heat | 6–24m | **one** composite from US-CM1/CM2/CM3 (`ISSUANCE-HEAT`, contrarian at extremes) |
   | Flow / crowding | wks–months | US-S3 NAAIM + US-S5 COT + US-S6 fund flows (`POSITION`/`FLOW`; each **contrarian at extremes**, tested separately before combining) |
   | Leverage / informed positioning | days–months | US-S4 margin (fragility, `LEV`); US-S7 insiders (`+`, informed-bullish); US-S9 short interest (`−`, informed-bearish): **indicator-specific signs, NOT one blanket sign** |
   | News | days–wks | US-S10b (`NEWS`, separate overlay); **US-S10a `blocked-by-data`** (needs licensed daily news) |

   Combine at allocation layer, never one daily number. (NAAIM moved out of "beliefs", it is observed positioning; fund flows kept at their true 21–63d horizon, not in the 6–24m exuberance sleeve; **turnover removed, no US turnover row exists, per the B–W mapping**.)
8. **Risk overlay** (Layer 3, sizing not direction) = US-R1/R4 + US-R3 + US-R5/R6a/R6b gates + **US-R8** (cut gross on positive stock–bond corr). **US-R10 (RTI) is `registered` (specified, not yet computed): a dashboard candidate NOT in sizing until it is computed (→ `shadow`) and passes the incremental-value test (→ `active`)** (US-VRP1 is Layer-2 alpha, not part of this overlay).

Known cross-composite correlations to monitor: Trend ↔ Participation ↔ Drawdown (all price-derived); Credit ↔ Financial conditions (NFCI *contains* markets); Sentiment ↔ Vol extremes (both spike in selloffs).

---

## Deferred, unresolved data contracts (Grade D; do not code yet)

| Item | Why deferred |
|---|---|
| Dealer gamma / GEX | Model-dependent estimate, vendor-proprietary assumptions, no clean point-in-time history; "edge" claim unvalidated |
| CNN Fear & Greed | Composite of components we already model separately; vendor methodology changes unversioned |
| BofA FMS / prime-broker positioning | Not public point-in-time; licensing unresolved |
| SKEW-based tail signals | Weak documented predictive power; 0DTE-era comparability issues |
| NYSE TICK / intraday internals | Belongs to intraday program, out of current contract |
| Retail order imbalance | Needs TAQ classification or proprietary broker/wholesaler data: not identifiable from public data with adequate consistency ([Boehmer et al.](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13033)) |
| Customer/small-trade put/call | Licensed (Cboe Open-Close/DataShop): the US-S2 research variant; do not splice onto the public aggregate history |
| Closed-end fund discount / dividend premium | B–W legacy proxies; historical-replication/research tier only (CEF universe contracted; dividend premium overlaps quality/value style) |

---

## Build sequence
1. Data spine w/ point-in-time timestamps: FRED (curve, OAS, NFCI, claims), CBOE (VIX complex, P/C), ISM/CPI calendars, ICI flows, COT, Form 4 aggregates, prices/breadth; **v2.4 pipelines: IPO/SEO/equity-issuance (per-event pricing/listing/withdrawal), Yale confidence, SF Fed news, FINRA short interest.**
2. Implement Layer 3 first (vol forecast + regime descriptors): it's needed to evaluate everything else. *(This is a **local sub-sequence within the US parent's own build**; the global order across all documents is `Indicators_Pool_Combination_v1.md` §13.)*
3. One composite per mechanism (§ above); single-mechanism backtests with ablation.
4. Cross-mechanism combination; redundancy audit (corr matrix, conditional corr in stress, incremental OOS value per Welch–Goyal discipline).
5. Vol-scaling policy tested as its own experiment (Moreira–Muir vs Cederburg framing).
6. Walk-forward everything; report net-of-cost with uncertainty.
7. Fundamental stock-selection sleeve (child contract, §2.2b) runs as its own program, start only after the PIT fundamental data spine (as-first-reported, announcement timestamps) is verified.

## Sources
- [Market Timing: More than a Mirage, Man Group](https://www.man.com/insights/market-timing) (architecture)
- [Moskowitz, Ooi, Pedersen: Time Series Momentum](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf) (Grade-A trend evidence, multi-asset)
- [Moreira & Muir (Volatility-Managed Portfolios](https://www.nber.org/papers/w22208) · [Cederburg et al.) On the performance of volatility-managed portfolios](https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X)
- [Goyal, Welch & Zafirov, comprehensive equity-premium prediction update](https://academic.oup.com/rfs/article/37/11/3490/7749383) (evidence-grading rationale)
- [AQR: Market Timing, Sin a Little](https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/Market-Timing-Sin-a-Little.pdf) (valuation-timing caution)
- [Baker & Stein: Market liquidity as a sentiment indicator](https://www.nber.org/papers/w8816) (conditional mechanism, short-sale constraints)
- [Baker & Wurgler 2006: Investor Sentiment and the Cross-Section of Stock Returns](https://people.stern.nyu.edu/jwurgler/papers/sentiment.pdf) (§2.5b anchor; cross-sectional, use PIT/rolling not full-sample PCA) · [Tetlock, media pessimism](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2007.01232.x) · [Boehmer et al. (retail order imbalance](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13033) · [Derrien) IPO retail demand](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=687132) · [SF Fed daily news sentiment](https://www.frbsf.org/research-and-insights/data-and-indicators/daily-news-sentiment-index/) · [Yale ICF confidence](https://yale-icf.github.io/ShillerUSConfidence/)
- [Cboe: VIX backwardation explainer](https://www.cboe.com/insights/posts/inside-volatility-trading-is-vix-backwardation-necessarily-a-sign-of-a-future-down-market/) · [FRED: TED discontinued](https://fred.stlouisfed.org/series/TEDRATE) · [CFTC COT release schedule](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm) · [FINRA margin statistics](https://www.finra.org/rules-guidance/key-topics/margin-accounts/margin-statistics)
- [The All Weather Story: Bridgewater 2012](https://www.bridgewater.com/research-and-insights/the-all-weather-story) (local PDF in Reading Materials; architecture: cash+beta+alpha, environmental balance, not empirical validation)
- [Fed: Good Inflation, Bad Inflation](https://www.federalreserve.gov/econres/feds/good-inflation-bad-inflation-implications-for-risky-asset-prices.htm) (regime-dependent inflation sign) · [AQR: Leverage Aversion and Risk Parity](https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf) (why leverage needs its own contract)
- Books folder: Narang (alpha/risk/execution separation, the Layer architecture), Katsanos, Clenow.

---

## Appendix: revision history

Kept for provenance. Nothing below is needed to read the contracts above.

**Change log v2.7→v2.8 (F1 orientation sync):** F1 summary corrected to the child's value structure: **(EV) FCFF/EV primary** + conditional EBIT/EV, robustness EnterpriseCFO/EV·EBITDA/EV·NOPAT/EV·sales/EV (was stale `CFO/EV, FCF/EV`; unlevered NOPAT-build-up numerators, §Fundamental F1).

**Change log v2.6→v2.7 (audit corrections):** US-M6 inflation surprise now **realized-data only**: 5y5y breakevens Δ removed (double-counted US-M8; Layer 1.5 keeps realized inflation and market-repricing separate); **US-VRP2 renamed "VIX-extreme / fear contrarian"** (VIX-extreme conflates expected variance + the premium, not a VRP; US-VRP1 is the genuine VRP, Bekaert–Hoerova); **US-V2 relabelled a Fed-model-style ERP *proxy*** (earnings-yield − real-yield spread, not a structural implied ERP; cash-flow-implied ERP as robustness).

**Change log v2.5→v2.6 (portfolio-risk states + bug-fix batch):** added **US-R10 cross-asset risk appetite (RTI)** as a Layer-3 risk-state (not alpha; extremes only; RG `RISK-APPETITE-XA`, not VOL; gated on incremental value over US-R8/US-X3/US-X4/US-X1/US-R1–R4): *(this entry originally said `shadow`; status later corrected to `registered` = specified-not-yet-computed per PortfolioRisk v1.2)*, full contract in `Indicators_Pool_PortfolioRisk_v1.md` (RTI + DR/ENB; DR dormant until a multi-sleeve combination layer exists). **Bug-fix batch:** VRP moved from Layer-3 to **Layer-2 §2.7 `US-VRP1`** (its target is future return = alpha) with variance-unit/horizon precision; RTI RG/version/grade corrected; stale v1-catalogue IDs (H6/H3/H7/A2/"E-family") replaced with US-X/US-R IDs; US-R8 added to the risk-overlay composite.

**Change log v2.4→v2.5 (parent-state additions):** added the variance risk premium: `IV² − E_t[RV]` with a mandatory ex-ante physical-variance forecast (HAR/GARCH; realized RV leaks the future), grade B research, distinct from VIX level (US-R2) and term structure (US-R3). *(v2.6: relocated to Layer-2 §2.7 `US-VRP1` as a return predictor; the Layer-3 `US-R9` identifier is retired (no active row, reserved in prose after the risk table.)* (A-share VRP deferred) thin options.)

**Child-integration pass (v2.4, alongside child Fundamental v1.4 / TrendReversal v1.3 / StatRisk v1.2 / MarketStructure v1.0):** §2.2b summary synced, added F2b `PROFIT_GROWTH`, F5 realized-ΔROE→forecast-ROE revision, F6 q5 `EXPECTED_INVESTMENT_GROWTH` (+sign, own RG, US B / CN D), F7 `DBNETIS/AT`; distance-to-default moved out of F4 to hybrid overlay; "debt issuance→F7, debt level→F4"; sibling cross-refs to `SEASONAL`/`SYS-DEFENSIVE`; stock-level capacity, loan constraints, ownership, price delay and crowding route to the Market Structure child rather than this index-timing file.

**Change log v2.3→v2.4 (sentiment/capital-markets review):** added §2.5b **capital-markets-exuberance sleeve** (Baker–Wurgler 2006 anchor: IPO supply US-CM1, IPO demand US-CM2, equity-issuance share US-CM3, + SEO/SPAC research; RG `ISSUANCE-HEAT`; PIT-monthly/rolling-estimation + cross-sectional-not-timing caveats); reclassified US-S7 insider SENT→`INFORMED-POS` and added US-S9 short interest (`INFORMED-POS`), US-S8 Yale confidence, US-S10 SF-Fed news (`NEWS`); improved US-S2 (customer/small-trade put/call) and US-S4 (net margin leverage, not debt level); four horizon-consistent sentiment sub-composites. **v2.4 integration pass:** authoritative §7 composite rebuilt as six sleeves with indicator-specific signs (NAAIM→flow/crowding, fund flows at true 21–63d horizon, no blanket contrarian sign, turnover removed); duplicate §2.5b sub-composite list collapsed to a pointer; US-S10 transform/targets specified; US-S8/US-CM3 marked `R=unverified`; US-CM2 first-day return compounded; dividend premium status aligned to Deferred.

**Change log v2.2→v2.3 (fundamental review):** cross-sectional fundamental factors (value/quality/profitability/investment/capital-allocation etc.) live in the new child contract `Indicators_Pool_Fundamental_v1.md`: NOT in this timing file. Here: US-V3 upgraded to a full aggregate-expectations composite, US-V4 upgraded from shareholder yield to net payout vs dilution, new US-V5 aggregate quality-trend breadth, and §2.2b summary table of the child-contract families.

**Change log v2.1→v2.2 (All-Weather review):** added Layer 1.5: Economic Environment & Exposure Map (growth/inflation surprise scores G_t/I_t vs frozen consensus; environment as conditioning layer promoted to alpha only if independently predictive OOS; driver-risk dashboard); mandatory cash+beta+alpha+overlay−costs attribution; new US-M0 (cash & real-cash return) and US-M8 (nominal-yield decomposition into real + breakeven, moved out of US-M7); US-X2 broadened to a demand-vs-supply commodity decomposition; explicit "what not to import from All Weather" cautions (equal-risk prior ≠ equiprobable regimes; beta>cash is a hypothesis; risk parity needs its own leverage/financing contract, out of scope, leverage cap stays 1.0); cleaned two v2.1 leftovers in Layer 4 (obsolete 2× cost rule; ambiguous close-execution bullet).

**Supersedes:** `Indicators_Pool_US_v1.md` (retained as idea catalogue).

**Change log v2→v2.1 (review round 2):** execution timing made internally consistent (default next-open execution; four timestamps per field); falsification pre-registration template + multiple-testing controls added; point-in-time universe requirement added; sector rotation split into a child contract; SPY vs ES treated as distinct implementations with dated low/base/high cost scenarios (arbitrary "2× cost" rejection dropped); SOFR-OIS lag corrected (SOFR published ~8:00 ET next business day for the prior day's transactions) and funding stress vs market liquidity split into separate contracts; bond–equity correlation moved from alpha to risk layer; evidence grade expanded to three dimensions (E/P/R); mixed-frequency composites split fast/medium/slow; all alphas must also be reported unscaled and ungated.

**Change log v1→v2:** restructured into four layers (research contract / alpha hypotheses / risk-state model / implementation model); every indicator now carries an explicit contract (raw field → transformation → target/horizon → availability lag → hypothesis + failure regime → redundancy group → evidence grade); `Dir` labels replaced by *hypothesized relationships*; TED spread removed (discontinued Jan 2022) in favor of SOFR-OIS/repo; COT and FINRA margin lags made explicit; VIX term-structure convention corrected (backwardation = elevated near-term fear); "vol clustering" restated as persistence, with calm-before-storm as a separate hypothesis; volatility scaling demoted from automatic transform to a separately tested risk policy (Moreira–Muir vs. Cederburg et al.); category-based composite replaced by mechanism composites; unresolved-data-contract items moved to a Deferred list.

**Framework reference (architecture, not evidence):** *Market Timing: More than a Mirage*, Man Group (2025). Its empirical section (104 proprietary managers, ex-post top-Sharpe selection, decade-vs-2018–2024 inconsistency) supports the *architecture*, granular data, combining signal families, converting signals to exposure via risk estimates, not any specific indicator claim here.
