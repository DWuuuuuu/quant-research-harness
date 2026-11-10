# Indicators Reference (Implementation Dictionary) v3.6

**Purpose.** The canonical **implementation** source of truth: one atomic, versioned output per entry, with the exact formula, direction, transform, field mapping, timing, universe, missingness rule and readiness needed to code it without reopening nine research files.

**→ If you only want "what can I build today", read [§0 Ready-now view](#0-ready-now-view) and stop.**

## Authority model (split, not hierarchical)

| Domain | Authoritative document |
|---|---|
| **Implementation**: formulas, directions, transforms, field contracts, windows, minimum history, tie/missingness, timing, dependencies, readiness | **This register** |
| **Research**: evidence, mechanism, caveats, grades, portability, promotion criteria, falsification | `Indicators_Pool_*.md` contracts |
| **Empirical lifecycle**: `registered → shadow → validated → active`, `active-stale`, `blocked-by-data` | `Indicators_Pool_Combination_v1.md` §status registry (**not restated here**) |
| **Allocation**: how any of this becomes a position | `Indicators_Pool_Combination_v1.md` (**not frozen**) |

If this register and a contract disagree **on a formula, direction, field or timing rule, this register wins.** If they disagree **on evidence, sign rationale or promotion readiness, the contract wins.** Log divergences in §17.

---

## 0. Ready-now view

**⚠ Regenerated in v2.3 and re-scoped.** v2.2's counts were wrong (§0.1 claimed 34 while listing 60; §0.2 claimed 38 while listing 40) and the filter used **owner** readiness, so rows whose own status is `S:C`: the EV value ratios, every F4 penalty, appeared as "formula-ready." Both fixed. **This section is derived; if it disagrees with a card, the card wins.**

**"Ready" was also one word doing three jobs.** Split into three gates that must be passed in order:

| Tier | Question | Gate |
|---|---|---|
| **T1: Computable** | Does the number compute deterministically today? | `Own S:F` · `Eff D:A`, `D:B` or `D:T` (**a series you must build, or one behind your entitlement, still computes**) |
| **T2: Backtest-causal** | Was it *knowable* at each historical decision date? | T1 **and** `Eff P:V/N`. **`D:P` (current-only) can never reach T2.** |
| **T3a: Live-production** | Can the value be produced live on schedule, timestamped, monitored, with a fallback? | T1 **and** a pinned clock (§2.2) **and** a live feed. **Independent of T2: no equity universe required.** |
| **T3b: Strategy-execution** | Can it be *traded*? | T3a **and** P4/P5 survivorship-free universe **and** tradability, costs, borrow, portfolio rules |

**⚠ T2 and T3a are INDEPENDENT axes, not ordered gates (v2.5 fix).** v2.4 defined `T3a = T2 + clock`, which misclassifies both directions: a **licensed real-time news feed can be live-production-ready with no historical archive** (T3a without T2), and a **decommissioned archive can be backtest-causal but no longer producible** (T2 without T3a). Read the three as: *historical-backtest* (T2) · *live-production* (T3a) · *strategy-execution* (T3b, which does require T3a plus a universe).

**⚠ v2.3 conflated two different finish lines**: a Treasury-curve state, a VIX level or the ACM term premium can be **produced and timestamped without any equity universe**, so requiring P4/P5 of them was wrong. Split into **T3a (indicator-production)** and **T3b (strategy-execution)** above.
**Nothing is T3b today** (P1's fill choice unpinned, no survivorship-free US universe, P4's liquidity threshold undefined). **Several macro/volatility states are T3a-eligible now**: they need only a pinned clock.

**Data class resolves by market, and the row shows the best case.** The `Own` column carries the most favourable class; `Eff US`/`Eff CN` carry the binding one. Global resolution: **US price/macro from FRED, yfinance and Ken French = `D:A`** · **anything reconstructed from EDGAR, Form 4, filings or index constituents = `D:B`** · **every A-share row sourced from Tushare = `D:T` (entitlement-gated, PIT-unvalidated), never `D:A`** · **fundamentals are `D:B` in both markets** (US build from XBRL; CN `D:T` on top).

### 0.1 T2, computable **and** backtest-causal
Market-derived, no as-filed dependency. **This is the honest "start here" list.**

**⚠ Raw value vs ranked score are different outputs (v2.5).** A stock's **raw** momentum is computable and causal with prices alone. A **cross-sectional rank** additionally needs a PIT-eligible universe (P4/P5), which is unresolved. Rows below are listed at their **raw-value** readiness; **every `TR-RANK` score inherits the §0.4 universe caveat and is one tier lower.** This is why `T-X1` can show `Eff D:P P:U` on its card and still appear here.

**Cross-sectional price/risk (US, factor returns from Ken French):** `T-X1` `T-X1v6` `T-X1v9` `T-X2` `T-X3w` `T-X3m` `T-X4` `T-X4v` `T-X5` `T-X6a` `R-X1` `R-X2` `R-X2v` `R-X3` `R-X4a` `R-X4b` `R-X6a` `R-X6b` `R-X6c`: *(subject to the P5 universe caveat in §0.4)*
**Cross-sectional price/risk (CN, no factor model needed):** `T-X1` `T-X1v6` `T-X1v9` `T-X3w` `T-X3m` `T-X4` `T-X4v` `T-X5` `T-X6a` `R-X2` `R-X2v` `R-X4a` `R-X4b` `R-X4c` `R-X4d`
**Index timing, market-observable only:** `US-M1.1` `US-M1.2` `US-M2.1` `US-M2.2` `US-M2.3` `US-M2.4` `US-M7` `US-M8.1` `US-M8.2` `US-T1.1` `US-T1.2` `US-T1.3` `US-T2.1` `US-T2.2` `US-T3` `US-T5` `US-B2` `US-X1` `US-X3` `US-R1` `US-R2a` `US-R3.1` `US-R6a.1` `US-R6a.2` `US-R6b.1` `US-R7` `US-R8` `US-VRP2` · `CN-M7.1` `CN-M7.2` `CN-M8.1` `CN-M8.2` `CN-V1.1` `CN-V1.2` `CN-V1.3` `CN-V2` `CN-V3` `CN-T1.1` `CN-T1.2` `CN-T1.3` `CN-T2.1` `CN-T2.2` `CN-T2.3` `CN-T5` `CN-B1.1` `CN-B1.2` `CN-B1.3` `CN-B2` `CN-B3.1` `CN-B3.2` `CN-B3.3` `CN-B4.1` `CN-B4.2` `CN-B8` `CN-F1.1` `CN-F2` `CN-F4` `CN-X3` `CN-R1` `CN-R3.1` `CN-R3.2` `CN-R4a.1` `CN-R4a.2` `CN-R4b.1` `CN-R4b.2` `CN-R5` `CN-R6` `CN-R7`
**Portfolio state:** `PR-R1A` `PR-R1B`

**⚠ A-share `R-X1`/`R-X3`/`T-X2` are NOT on this list.** CH3's value factor consumes reported earnings, so those three are **T1 only** for A-shares until the earnings vintage audit passes (§2.1).

### 0.2 T1 only, computes, but **not** backtest-causal
Every fundamental row plus revision-prone macro. Fine for exploratory work; **not** for a result you would size on.

**⚠ Downgraded after the §2.4 smoke test.** CN fundamentals are **`P:F` (forward-only)**, not merely unverified: Tushare overwrites in place and exposes no prior vintages, so **these rows can never become backtest-causal on historical data from this source**: only from a forward archive started now, or an announcement-PDF build. US fundamentals stay `P:P` (EDGAR keeps as-filed submissions).

`F1-EP` `F1-BP` `F1-DY` `F1-EBITDAEV` `F2-GPA` `F2-GPA-NM` `F2-OPA` `F2-OP-FF` `F2-ROA` `F2-ROE` `F2-COP` `F2b-dROA` `F2b-dROE` `F2b-dGM` `F2b-dOM` `F2b-dCOP` `F3-ACC` `F3-CFOA` `F6-AG` `F6-CAPEXA` `F6-INVG` `F6-GWG` `F7-NPY` `F7-DSH` `F7-DBNETIS` `F7-NSI1Y` `F7-CSI5Y` `F5-CAR` · **A-share factor-model rows:** `R-X1` `R-X3` `T-X2` · **revision-prone macro:** `US-M4.1` `US-M4.2` `US-M5.1` `US-M5.3` `US-M5.4` `US-V1` `US-V4.1` `US-V4.2` `US-V5` `US-S4` `US-S10b` `US-CM2.1` `US-CM2.2` `US-CM3` `US-CM4` `CN-M1a` `CN-M1b` `CN-M3` `CN-M4.1` `CN-M4.2` `CN-M4.3` `CN-M5c` `CN-M6.1` `CN-M6.2` `CN-V4` `CN-V6` `CN-V7.1` `CN-V7.2` `CN-T3` `CN-B5` `CN-B6` `CN-F3` `CN-X4`

### 0.3 Blocked by **one pinnable choice** (`Own S:C`)

| Entry | The one decision |
|---|---|
| `T-X6b` | turnover-change lookback `k` |
| `T-X7` | role: `a` standalone alpha **XOR** `b` moderator |
| `T-X8` | missingness: all-four-required **XOR** mean-of-≥3 |
| `R-X5` | ratio: `CFO/sales` **XOR** `CF/book` |
| `F1-FCFFEV` `F1-SEV` `F1-EBITEV` `F1-ECFOEV` `F1-NOPATEV` | **the EV floor value**, plus `NormalizedEBIT`'s exceptional-item field map and `T_op_exact` |
| `F2-ROIC` | invested-capital boundary |
| `F3-CFONI` | "materially positive NI" threshold |
| `F4-NDE` `F4-ICOV` `F4-DA` `F4-CR` `F4-CNIBD` | **`TR-TAIL` absolute thresholds**: a tail penalty without thresholds is not codeable |
| `F4-CNDCDD` | both 大存大贷 thresholds |
| `F5-CNPRE` `F5-CNEXP` | interval encoding **and** the surprise reference |
| `F5-SUE` | expectation basis + σ-floor |
| `F7-FIN` | tail-classification thresholds |
| `F8-FS` (composite) | tie + missing-component rule: **`F8-PS` inherits this**, so both are `S:C` |
| `F8-GS*` | missing-data treatment **only**: source-faithful `0` vs production `NA` *(the 5y window / 3y minimum is frozen, not open)* |
| `US-M0.2` | expected-inflation source |
| `US-T2.3` | crossover event window |
| `US-T4.1` `US-T4.2` `CN-T4` | reversal horizon; **one** RSI parameter (anti-zoo) |
| `US-R4.1` `US-R4.2` `CN-R2` | GARCH vs HAR specification |
| `US-X2.3` `CN-X1.4` | demand-vs-supply decomposition rule |
| `CN-M0` | cash proxy |
| `CN-M2.5` | stance-index weights |
| `CN-M6.3` `CN-B3.4` | composite weights (**and B3.4 sign alignment**) |
| `CN-CM-S.3` `CN-CM-S.*` | listing-speed definition |

### 0.4 Universe caveat, applies to every cross-sectional row
**A-share (`P4`): a survivorship-free universe IS buildable, smoke-tested (§2.3).** Delisted names and their price history are retrievable; ST history is reconstructable with pagination. Remaining: a delisting-return convention and the liquidity threshold.
**US (`P5`): no survivorship-free PIT universe exists on the free stack.** CRSP is `LICENSED`; EDGAR+CIK gives filing and identifier history but **not** historical index eligibility, complete prices or delisting returns. Until P5 is resolved, **US** cross-sectional results are survivorship-contaminated. This blocks belief, not computation.

### 0.5 Blocked by licensed data (§15)
Analyst consensus (`F5-REV/RECO/LTG`, `F1` forward E/P, `US-V2`, `US-V3.*`, `CN-V5.*`, and the *surprise legs* of `US-M5.2` `US-M6.*` `CN-M4.4` `CN-M5a` `CN-M5b`) · bank regulatory (`FIN-B*`) · borrow, ownership, news (`MS-C1/C2/C4`, `MS-R1`, `US-S10a`) · option surface (`US-VRP1`, `US-R5.1`) · vendor positioning (`CN-F5`) · intraday limit-lock (`R-X4e`).

### 0.6 Source-verification queue (`S:R` → `S:F`)
**Cleared:** `F2-COP` (Ball et al.) · `MS-C3a` (Hou–Moskowitz) · `F8-FS*` components (Piotroski: **corrected to beginning-of-year assets in v2.3**) · `F8-PS` (**was already frozen in the contract**) · `P7-CN` CH3 (LSY, §2.1).
**Still queued:** `F5-SUE` (denominator + σ-floor) · `F6-q5` (`Cop` account list + fallbacks) · `F4-ALTZ`/`F4-OHLO` (coefficients).

### 0.7 Highest-leverage unblocks
1. **A-share fundamental vintage audit (P13)**: now the top blocker. It gates all 30+ CN fundamental rows **and**, via CH3's earnings input, `R-X1`/`R-X3`/`T-X2`.
2. **Survivorship-free universe (P4/P5)**: gates belief in every cross-sectional result.
3. **PIT sector membership (P9)**: gates `R-X7`, `F8-GS*`, `CN-T3`, `CN-X4`, all `TR-SECRANK`.
4. ~~Register `X-SIZE` and `X-ILLIQ`~~: **DONE in v2.4/v2.5** (§12b.1, with `X-SIZE-T` vs `X-SIZE-F` separated). Remaining: pin `X-TURN`'s denominator.
5. **Pin P1's execution clock** (§2.2): the only thing standing between T2 and T3 for the §0.1 list.

---

## 1. Schema, readiness & transforms

### 1.1 Mandatory fields, fixed order

| # | Field | Meaning |
|---|---|---|
| 1 | **ID** | Stable atomic reference. **One ID = one scalar output.** `.n` suffix = an atomic output split out of a parent family row. |
| 2 | **Name / class** | Navigation. |
| 3 | **Out** | Portfolio role: `alpha` · `penalty` · `cond` · `risk` · `state` · `diag`. |
| 4 | **Dir** | **Raw→score direction** (§1.4). Distinct from `Out`. |
| 5 | **TR** | Production transform, one named ID from §1.5. |
| 5b | **CLK** | Execution clock, one named ID from §2.2. Defaults to `CLK-CLOSE`; **must be stated explicitly when it differs**. |
| 5c | **Info-ts** | When the input becomes knowable (release/filing timestamp) **and** when the *signal* is complete: these differ whenever a signal spans an event window. |
| 6 | **Formula** | Exact raw output, windows in `m0` notation (§1.3). |
| 7 | **Inputs** | Vendor fields and units. |
| 8 | **Min hist** | Minimum observations for a valid value. |
| 9 | **Miss/tie** | Reproducibility rule. `NA` never means `0`. |
| 10 | **Dep** | Value-dependencies (§1.2). |
| 11 | **RG** | Redundancy group: one-budget rule. |
| 12 | **Own / Eff** | Readiness, §1.2. |
| 13 | **E** | Evidence grade `US/CN`, from the owning contract. |
| 14 | **Spec** | Contract pointer. |

### 1.2 Readiness, three dimensions, two scopes

| Dim | Codes (best → worst) |
|---|---|
| **S** specification | `F` FROZEN · `C` CHOICE-OPEN (choice named) · `R` DRAFT-REPRO (reproduced, unverified vs source) · `O` OUTLINE (not codeable) |
| **D** raw data (**v2.3: six operational classes**) | `A`→**`PUBLIC-DIRECT`** downloadable clean series · `B`→**`PUBLIC-BUILD`** raw disclosures you must normalize yourself · `T`→**`ACCOUNT-TIER`** reachable on your entitlement, PIT completeness unvalidated · `P`→**`PARTIAL/CURRENT-ONLY`** current snapshot, no usable history · `L`→**`LICENSED`** · `U`→**`UNAVAILABLE`** |
| **P** PIT history | `V` VERIFIED / `N` N-A (market-observable, not revised) · `P` PARTIAL · `U` UNVERIFIED · `F` FORWARD-ONLY |

**Two scopes, this is the fix for v2.0's broken propagation:**
- **`Own`** = readiness of the indicator *definition itself*.
- **`Eff`** = `min(Own, all value-dependencies)` per dimension. Stated per market where they differ.

**Value vs execution dependencies.** `Eff` propagates only over **value** dependencies, what you need to compute the number (P2, P4/P5, P6, P7, P8, P9, P13, P14). **P1 and P3 are *execution* primitives**: they gate the tradable strategy, not the indicator value. A raw accounting ratio is not made less computable by an unpinned open-vs-VWAP choice. **Every tradable use additionally inherits P1 (`S:C`): stated once here, not repeated on 180 rows.**

**Not tracked here:** *implementation status* (rots weekly → build tracker) and *empirical lifecycle* (owned by Combination's registry). Field 13 carries the evidence grade only.

### 1.3 Month indexing: `m0` convention

**Overloaded `t` caused a real bug in v1.0 and a second one in v2.0.** All monthly windows are now expressed relative to:
- **`m0`** = the **formation month**: the signal is complete at the **close of `m0`**.
- **`m0+1`** = the **first holding month**.

Translating a source that forms at end of `t−1` and holds `t`: its `t−k` becomes **`m0−k+1`**. Applied throughout §4. Any source-faithful window quoted in a research contract under the other convention must be reindexed before coding: **do not copy month indices across conventions.**

### 1.4 `Dir`: raw→score direction

`Out` says how the portfolio uses the number; `Dir` says what to do with the raw value. They are independent and v2.0 conflated them.

| Code | Meaning |
|---|---|
| `+` | higher raw → higher score |
| `−` | higher raw → lower score (negate) |
| `+inv` | higher raw is *good* but the ratio is unbounded/undefined at 0 → use a bounded inverse or tail tier, never a raw negation |
| `tail−` | only the adverse tail carries information; middle is uninformative |
| `state` | no directional score: regime/level variable |
| `bin` | binary 0/1 |

### 1.5 Transform menu (replaces v2.0's non-deterministic P12)

Each entry declares **exactly one** `TR`. A composite or product variant may declare a different one; that is a separate object.

| TR | Definition |
|---|---|
| **`TR-RANK`** | winsorize 1/99 → cross-sectional **rank** within the declared universe → scale to [−1,1]. Default for continuous alpha. |
| **`TR-Z`** | winsorize 1/99 → cross-sectional **z-score**. Use only where the cardinal spacing is meaningful. |
| **`TR-SECRANK`** | `TR-RANK` computed **within sector** (P9). The stage-2 production object (P11); a **separate output** from its stage-1 parent. |
| **`TR-BINARY`** | 0/1 as defined. **No winsorization, no ranking.** F-Score/G-Score components. |
| **`TR-TAIL`** | assign to adverse tail tiers by **absolute declared thresholds**, not symmetric ranking. Penalties. Thresholds must be declared per entry. |
| **`TR-STATE`** | raw level or percentile-vs-own-history. No cross-sectional operation. Risk states, macro. |
| **`TR-EVENTZ`** | standardize **within the event cohort** (same announcement window), not the calendar cross-section. Event surprises. |
| **`TR-NONE`** | consumed raw by a downstream object; never scored standalone. Conditioners and diagnostics. |

**Breakpoint population is declared separately from the transform**: a source-faithful sort may require **NYSE** (US) or **Main-Board** (CN) breakpoints even when scoring the full universe. See P4/P5.

**Neutralization is a method, not a flag.** Where used, declare one: `TR-SECRANK` (within-sector ranking) · residualization on declared controls · constrained projection. These produce different outputs and are not interchangeable.

---

## 2. Primitives

| ID | Primitive | Contract | Class | Ready |
|---|---|---|---|---|
| **P1** | Execution clock **family** (§2.2) | **NOT one universal rule.** Six named clocks by information type; each entry declares one. Default `CLK-CLOSE` (signal at close `m0` → first executable open `m0`+1). **CHOICE-OPEN: open vs VWAP within each clock.** | execution | `S:C D:A P:N` |
| **P2** | Signal price series | One frozen split/dividend-adjusted **total-return** close-to-close series. CN `daily`×`adj_factor`; US adjusted close. **⚠ `adj_factor` is cumulative and IS restated** (smoke-tested: 600519.SH, 8 restatements in 3y, 7.65→8.45). **Return RATIOS are invariant to later restatement; price LEVELS are not**: any indicator on a price *level* (`X-PRC`) must use unadjusted prices. | value | `S:F D:A P:N` (returns) · `P:U` (levels) |
| **P3** | Tradability series | Raw prices + status. CN `stk_limit`, `suspend_d`. Never blended into P2. | execution | `S:F D:A P:N` |
| **P4** | Universe: A-share | All-A **ex** IPO<6m, ST/\*ST, suspended, bottom-liquidity. **Main-Board breakpoints** for sorts. **CHOICE-OPEN: liquidity threshold undefined.** ST-status built from `namechange`: **⚠ that endpoint is ROW-CAPPED at 10,000; pagination via `offset` is MANDATORY** (≥14,157 rows, history back to 1990-12). | value | **`S:C D:T P:P`** (upgraded. See §2.3) |
| **P5** | Universe: US | PIT index membership with delistings carried. **Free stack does NOT guarantee this** (CRSP 💲 or reconstruct from EDGAR+CIK). **NYSE breakpoints** where source-faithful. | value | `S:F D:P P:U` |
| **P6** | **Residual-regression engine** | The *estimation contract*, not an indicator: OLS of excess daily returns on the declared factor set over the **prior calendar month**, **min 15 valid obs else NA**, residual σ = **sample SD (n−1)**, skewness from the same residual vector. Factor set: **US FF3 · CN CH3**. **Emits** the residual vector `ε` consumed by R-X1, R-X3 and any `/residual-vol` denominator. | value | `S:F` · D/P inherit P7 |
| **P7** | Factor returns & `r_f` | **US: Ken French FF3 + T-bill**: `PUBLIC-DIRECT`, pre-built. **CN: CH3: construction specified in §2.1; `r_f` = the ONE-YEAR DEPOSIT RATE, not repo/SHIBOR.** Self-constructed from Tushare inputs. **⚠ CH3 consumes reported earnings → inherits fundamental PIT risk (§2.1).** | value | US `S:F D:A P:N` · **CN `S:F D:T P:U`** |
| **P8** | PIT discipline | Four timestamps per field: `observation / publication / decision-cutoff / first-executable`. Join on publication, trade at first-executable. As-filed, not restated. **Missing ≠ zero.** | value | `S:F D:P P:U` |
| **P9** | Sector / industry | CN **申万**; US **GICS**. **Historical PIT membership unconfirmed**: current-membership backfill is a silent look-ahead. | value | `S:F D:P P:U` |
| **P10** | Reporting convention | Report **VW-capped AND EW** for every cross-sectional sort. | reporting | `S:F D:A P:N` |
| **P11** | Two-stage grading | Stage 1 = source-faithful raw sort (the published grade attaches here). Stage 2 = neutralized rank: **a separate object with its own grade** (`TR-SECRANK`). | reporting | `S:F D:A P:N` |
| **P13** | Fundamental information time | Publication = **as-filed announcement date** (`f_ann_date`), **never fiscal-period date**. Quarterly, TTM unless stated. **⚠ Smoke-tested (§2.4): Tushare retains NO prior vintages: `update_flag` is metadata, not versioning. CN as-filed history is FORWARD-ONLY.** | value | US `S:F D:B P:P` · **CN `S:F D:T P:F`** |
| **P14** | Announcement-date spine | Per-name event dates. CN: report + `forecast` + `express`. US: EDGAR filing / 8-K. **Constructed.** | value | US `S:F D:B P:P` · CN `S:F D:T P:U` |
| **P15** | **Macro vintage spine** | First-release vs revised series; release timestamps; seasonal-adjustment re-runs; definition breaks. **US: ALFRED. CN: no *verified standardized* archive in the current free stack: commercial vintage archives may exist and should be validated at procurement; until then, forward snapshots.** | value | US `S:F D:P P:P` · **CN `S:F D:U P:F`** |

*(P12 removed, replaced by the §1.5 transform menu.)*

### 2.1 CH3 factor construction (P7-CN): **specified in v2.2, `S:F`**

Extracted from **Liu, Stambaugh & Yuan, *Size and value in China*, JFE 134 (2019) 48–69**: the **published** version. ⚠ v2.2 initially quoted the **January 2018 working draft**, whose shell-value figure was revised before publication; the published numbers are used below.

**Factor universe (distinct from P4. See the warning below):**
- Tickers beginning **60** (SH main), **00** (SZ main), **30** (ChiNext). ⚠ **This is the source's legacy universe, it omits STAR (688) and BSE (8xx/4xx).** Faithful for replication; **not** automatically right for a live modern universe. Treat the original as the **source-faithful legacy primary** and any modern-universe extension as a separately tested variant (the sample ends **2016**, before listing reforms that may have weakened the shell mechanism).
- Exclude **(i)** the **bottom 30% by market cap**: shell-value contamination; 83% of Chinese reverse mergers use shells from this group, and roughly **30% of a typical bottom-30% stock's market value is shell value** (published estimate: mean `S/V` = **29.5%**, fluctuating 10–60% over 2009–2016). These stocks are only **7% of total market capitalization**, so dropping them costs little breadth.
- Exclude **(ii)** stocks **listed < 6 months**; **(iii)** stocks with **< 120 trading records in the past 12 months** or **< 15 trading records in the most recent month** (guards against post-suspension returns).

**Inputs.**
- **Size (ME)** = previous month's closing price × **total shares outstanding, INCLUDING non-tradable shares** (⚠ *not* free-float).
- **EP** = most recently reported **annualized net profit excluding non-recurrent gains/losses** (**扣非净利润**) ÷ **previous month's** ME.

**Monthly sort (Fama–French procedure, independent 2×3):**
- 2 size groups **split at the median ME of the remaining 70% universe** → Small, Big.
- 3 EP groups on the same universe → **top 30% Value (V), middle 40% Middle (M), bottom 30% Growth (G)**.
- Intersections → six **value-weighted** portfolios: `S/V, S/M, S/G, B/V, B/M, B/G`.

```
SMB = ⅓(S/V + S/M + S/G) − ⅓(B/V + B/M + B/G)
VMG = ½(S/V + B/V)       − ½(S/G + B/G)
MKT = value-weighted return of the top-70% universe − one-year deposit rate
```
Rebalance **monthly**, hold one month.

**⚠ The CH3 factor universe is NOT the P4 signal universe.** CH3 deletes the bottom 30% by size; P4 excludes ST/\*ST, suspensions and a bottom-liquidity tier. **Do not conflate them**: the factor universe defines the *regression's* right-hand side; P4 defines which names you *rank and trade*. Two different objects that happen to overlap.

**⚠ Documented CH3 limits (do not over-trust the residuals).** LSY report CH-3 accommodates anomalies in size, value, profitability and volatility, but **fails on parts of the reversal and turnover categories.** So `T-X3w/m` and `T-X6a/b` residual-based variants sit exactly where the factor model is weakest. Keep raw primaries there, and treat CH3-residualized reversal/turnover as diagnostics, not cleaner signals.

**⚠ CH3 IS NOT PIT-CLEAN, the single most consequential readiness correction in v2.3.** The value factor consumes **most-recently-reported earnings**, so historical CH3 construction **inherits the full P8/P13 fundamental vintage problem**. A factor *return* being a market series does not make its *inputs* market data. Until A-share earnings vintages are validated as-available-at-each-month-end, **`P7-CN` is `P:U`, not `P:N`**, and therefore `R-X1`, `R-X3` and `T-X2` are **computable but not backtest-trustworthy** for A-shares.

**Data access: `ACCOUNT-TIER`, not "free".** All inputs: `daily`, `adj_factor`, `daily_basic` (`total_share`, `total_mv`), `fina_indicator` (扣非), `namechange`: are reachable at your 5,000-point entitlement, and the one-year deposit rate is a published PBoC benchmark. That is an **account entitlement with unvalidated PIT completeness**, not public-free clean data.

---

**P6/R-X1 circularity fixed.** v2.0 defined P6 *as* R-X1 while R-X1 depended on P6. P6 is now the **estimation engine** (consumes P2+P7, emits `ε`); **R-X1 is the IVOL indicator that consumes `ε`**. Downstream `/residual-vol` consumers reference **P6's output**, not the R-X1 row.

**⚠ `D:A` was doing two very different jobs.** v2.2 merged "a clean downloadable series" (Ken French factors, FRED) with "raw disclosures from which a difficult series might be constructed" (EDGAR XBRL, Tushare statements). The six-class scheme above separates them. **Practical consequence: nearly every A-share row is `ACCOUNT-TIER`, not free**, and most US fundamental rows are `PUBLIC-BUILD`, not `PUBLIC-DIRECT`: EDGAR gives timestamped submissions, but custom tags, amendments, contexts, fiscal calendars and units all need normalizing before you have a panel.

**Live A-share endpoints @5000 pt (`ACCOUNT-TIER`):** `daily`, `adj_factor`, `daily_basic`, `income`, `balancesheet`, `cashflow`, `fina_indicator`, `forecast`, `express`, `dividend`, `moneyflow`, `index_weight`, `stk_limit`, `suspend_d`, `namechange`, macro (`cn_pmi`/`cn_cpi`/`cn_ppi`/`cn_m`/`shibor`).

---

### 2.2 Execution clocks (`P1` family): **v2.3, replaces the single universal rule**

v2.2 asserted that every signal completes at the close and first trades the next open. That is right for daily cross-sectional signals and **wrong for at least five other information types**: it would either forfeit a session of alpha or, worse, book a fill that was never available.

| Clock | Rule | Applies to |
|---|---|---|
| **`CLK-CLOSE`** | signal at close `m0` → first executable **open `m0`+1** | default; all §4–§6 cross-sectional rows |
| **`CLK-PREOPEN`** | information available **before** the session → executable **same-session open** | `CN-X3` (HK/ADR gap), overnight macro, overseas closes |
| **`CLK-INTRADAY`** | continuously observable → executable **intraday** | `CN-F1.*` futures basis, option-implied states, `US-R2a`/`US-R3.*` |
| **`CLK-FILING`** | exact **corporate filing** timestamp; post-close disclosure → **day 0 = next session** | `F5-CAR`, `F5-CN*`, all `P14` event rows |
| **`CLK-RELEASE`** | scheduled **macro/statistical release**: exact public release timestamp → first permissible trade. **Not a filing clock**: the calendar is known in advance and the release is simultaneous to all. | `US-M9.*` SLOOS, CPI/PCE/PMI prints, all `P15` rows |
| **`CLK-WEEKLY`** | weekly formation, own holding period: **must not be forced into the `m0` monthly grid** | `T-X3w`, `MS-C3a` |
| **`CLK-CORPACTION`** | **four separate dates: declaration · record · ex · payment.** Declare which drives the **signal** (normally declaration: the information event) and which drives **execution/valuation** (normally ex-date: the price adjustment). Not the filing clock. | `F1-DY`, `F7-NPY`, `F7-DSH`, `CN-N4` unlocks |

**Every entry inherits `CLK-CLOSE` unless its card names another.** The open-vs-VWAP fill choice is orthogonal and still unpinned, pin it once per product, across all six clocks.

---

### 2.3 Smoke-test results: `T-X1` A-share, end to end (2026-08)

First indicator run against live data. **Formation `m0` = 2025-12, holding 2026-01**, 40 Main-Board names listed pre-2023.

| Check | Result | Effect on the register |
|---|---|---|
| Monthly bar coverage | **40/40 names, 11/11 window months** | clean |
| Full-history eligibility | 40/40 passed the 11-month rule; **0 dropped** | the `NA`-not-`0` rule never fired on this sample: retest on a younger cohort |
| First-executable price | **open of 2026-01 present for 40/40** | `CLK-CLOSE` → open `m0`+1 **confirmed executable** |
| Suspension feed | `suspend_d` Dec-2025: 407 records / 83 names | P3 live |
| `adj_factor` restatement | **8 restatements in 3y** on 600519.SH (7.65→8.45) | P2 split: ratios `P:N`, levels `P:U` |
| **Delisted-name price history** | **6/6 retrieved**, bars through the final full month | **P4 upgraded. See below** |
| `namechange` completeness | **row-capped at 10,000**; `offset` yields ≥14,157, back to **1990-12** | **a silent truncation bug**: first run got a partial ST history and did not error |
| **`m0` clock sensitivity** | correct vs naive-including-`m0`: **corr 0.716, mean rank shift 5.3 of 40** | the v2.1 clock fix is **load-bearing, not cosmetic** |

**⚠ P4 was too pessimistic, corrected.** The register carried A-share universe data as `D:P P:F` and §0.4 said cross-sectional results are survivorship-contaminated in *both* markets. **For A-shares that is now wrong:** `stock_basic(list_status='D')` returns **339 delisted names (208 delisted 2020-2026)**, and `pro_bar` **returns their full price history**. A survivorship-free A-share universe is **buildable today**. The US claim stands unchanged, no free survivorship-free universe exists there.

**Residual P4 gap (small, real):** the last retrievable bar is the final *full* month before delisting (e.g. `000005.SZ` delisted 2024-04-26, last bar 2024-03-29). **The delisting-period return is missing**, so a delisting-return convention must be declared, otherwise names exit the panel at their last good price, which is a mild upward bias.

**⚠ The `namechange` row cap is the most transferable lesson.** It returned exactly 10,000 rows and **did not error**. Any endpoint in this register with a large row count needs an explicit pagination check; a truncated pull looks like clean data. Add this to every field contract that hits a list endpoint.

---

### 2.4 Smoke-test results: `F1-EP` A-share fundamentals, PIT (2026-08)

Second indicator run. **The result is negative and it downgrades 38 entries.**

| Check | Result | Verdict |
|---|---|---|
| `update_flag` 0/1 pairs | 3 of 7 periods return **two rows**, but with **identical `ann_date`, `f_ann_date` and NI** | **metadata duplication, NOT a vintage mechanism** |
| Restatement scan | **0 of 216 firm-periods** (12 names, 2020–2024) carry more than one distinct NI | as-filed history is **not retained** |
| `report_type` 4/5 (调整前/调整合并) | only `report_type=1` returned across all tested names | no pre-adjustment vintage exposed |
| Publication lag, FY2023 annual | min **86d**, median **89d**, **max 121d** after fiscal end | the 4-month convention **leaks** |
| Bulk cross-section (`period=` without `ts_code`) | **`必填参数, ts_code`**: blocked at 5,000 points | per-stock loop only |
| `profit_dedt` (扣非) | present, 16/16 rows non-null on the tested name | CN numerator available |

**⚠ `P13` downgraded `P:U → P:F`: as-filed fundamental history is NOT recoverable from this stack.** `update_flag` looked like a vintage field and is not one: the paired rows share the *same announcement date*, which is structurally incompatible with being an original-plus-restatement pair. Combined with zero NI divergence across 216 firm-periods, the conclusion is that **Tushare serves the latest version only and overwrites in place.**
*(Honest caveat: the 12 names sampled are large caps, which restate rarely. But the identical-`f_ann_date` structure is the decisive evidence, not the zero count.)*

**Consequence.** The register's build-step-1 claim (*"vendors overwrite history, capture now"*) is now **evidenced, not assumed**. Every A-share fundamental row is **forward-only**: a PIT panel can be built **from today onward** by daily archiving, and historical as-filed values are obtainable only from 巨潮/交易所 announcement PDFs, which is a separate NLP build (`D:B`, high effort). **There is no shortcut.**

**⚠ The 4-month availability convention can leak.** `F6-q5` uses *"latest fiscal year ending ≥4 months earlier"* and similar shortcuts appear elsewhere. Observed FY2023 lag reached **121 days > 120**. **Always join on the actual `f_ann_date`** (P8 already requires this); the 4-month rule is a fallback that must be widened to ≥125d **and flagged** whenever `f_ann_date` is missing.

**⚠ Operational cost of the PIT spine, quantified.** With bulk pulls blocked, one full history pass is ≈**5,873 stocks × 4 endpoints ≈ 23,500 calls**; at the 80/min statement limit that is **~5 hours per pass**, and forward archiving needs it **repeated on a schedule**. This is a scheduling and storage problem, not a research problem, and it is the true critical path for 38 of this register's entries.

---

## 3. Master index

**Counting rule (v2.4, the previous counts were hand-maintained and drifted twice).** An **entry** is one catalogued atomic output, typed: **primary** (production candidate) · **variant** (named robustness alternative, never an independent vote) · **component** (feeds a composite) · **composite** (scalar built from components) · **outline** (`S:O`, not codeable) · **backlog** (§18, not active). **"Catalogued" ≠ "active"**: a large share is choice-open, licensed, outline or registered-only. Totals are **regenerated by `tools/validate.py`** (saved in the repo; also flags malformed tables and schema-incomplete rows), not hand-maintained, the previous three versions each drifted (284→286→325 all wrong; §12b was claimed at 39 against an actual 33). **Cross-references count once**: `US-BW3/4/5` alias `US-CM1.1`/`US-CM2.1`/`US-CM3` and are excluded from the unique total.

| Class | § | Atomic entries |
|---|---|---|
| Cross-sectional price (T) | §4 | 13 |
| Cross-sectional statistical risk (R) | §5 | 14 |
| Fundamental: value | §6.1 | 9 |
| Fundamental: profitability | §6.2 | 16 |
| Fundamental: quality & strength | §6.3 | 11 |
| Fundamental: investment & capital | §6.4 | 12 |
| Event | §7 | 5 |
| Accounting overlays | §8 | 17 components + 3 composites |
| Market structure | §9 | 1 |
| **Crowding / leverage / forced-flow (MS-R)** | §9b | 35 |
| **Limit-event family expansion (CN-B3.5-14)** | §11 | 10 |
| **Retail small-order proxy (CN-RET1)** | §12b.5 | 2 |
| Index timing: US | §10 | 90 |
| Index timing: CN | §11 | 91 |
| Cross-asset & book-dependent | §12 | 6 |
| Registered-but-inactive registrations | §12b | 35 |
| Composites (`F8-FS`, `F8-GS`, `F8-PS`) | §8 | 3 |
| **Total catalogued rows** | | **377** |
| **less 4 cross-references** (`US-BW3/4/5` = `US-CM1.1`/`US-CM2.1`/`US-CM3`; `CN-B3.3` = `CN-B3.7`) | | **373 unique** |
| Excluded | §15 | 25 |

---

## 4. Cross-sectional price (T)

**Common:** Value-dep `P2, P4/P5`. Reporting `P10, P11`. Monthly formation unless noted. Miss: incomplete window → `NA`; missing price ≠ 0 return. All windows in `m0` notation (§1.3).

| ID | Name | Out | Dir | TR | Formula (m0 = formation month) | Min hist | Own | Eff US | Eff CN | E |
|---|---|---|---|---|---|---|---|---|---|---|
| **T-X1** | Momentum 12-1 | alpha | `+` | `TR-RANK` | `∏_{k=1}^{11}(1+r_{m0−k}) − 1`: months `m0−11 … m0−1`, **skip `m0`** | 11m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | A/D |
| T-X1v6 | Momentum 6-1 | alpha | `+` | `TR-RANK` | same, `k=1…5` | 5m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | variant |
| T-X1v9 | Momentum 9-1 | alpha | `+` | `TR-RANK` | same, `k=1…8` | 8m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | variant |
| **T-X2** | Residual momentum | alpha | `+` | `TR-RANK` | `Σ_{k=1}^{11} ε̂_{m0−k} / σ(ε̂_{m0−11:m0−1})`; `ε̂` from **monthly FF3/CH3 over the 36 months ending `m0−1`**; **no α added** | 36m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | A/B |
| **T-X3w** | Reversal 1w | alpha | `−` | `TR-RANK` | prior 5-session cumulative return through close `m0` | 5d | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/B |
| **T-X3m** | Reversal 1m | alpha | `−` | `TR-RANK` | return of month `m0` | 15d | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/B |
| **T-X4** | Long reversal 60-13 | alpha | `−` | `TR-RANK` | cumulative return months **`m0−59 … m0−12`** (48m, skipping the most recent 12 incl. `m0`) | 48m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/B |
| T-X4v | Long reversal 36-13 | alpha | `−` | `TR-RANK` | months `m0−35 … m0−12` | 24m | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | variant |
| **T-X5** | Information discreteness | cond | `−` | `TR-NONE` | `ID = sign(PRET) × (%neg − %pos days)` over the formation window | window | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/C |
| **T-X6a** | Turnover level | cond | `state` | `TR-NONE` | mean daily turnover over the formation window | window | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/C |
| **T-X6b** | Turnover change | cond | `state` | `TR-NONE` | `T-X6a_{m0} / T-X6a_{m0−k} − 1`; **pin `k`** | window+k | `S:C D:A P:N` | `S:C D:P P:U` | `S:C D:P P:F` | B/C |
| **T-X7** | 52-week-high proximity | see note | `+` | `TR-RANK` | `P_{m0 close} / max_{s∈[m0−251d, m0]} P_s` | 252d | `S:C D:A P:N` | `S:C D:P P:U` | `S:C D:P P:F` | B/C |
| **T-X8** | Same-month seasonality | alpha | `+` | `TR-RANK` | **`¼(r_{m0−23} + r_{m0−35} + r_{m0−47} + r_{m0−59})`**: the same calendar month as the **holding** month `m0+1`, in years 2–5 back | 60m | `S:C D:A P:N` | `S:C D:P P:U` | `S:C D:P P:F` | B / B-raw, C-adj |

**Clock corrections applied in v2.1.** `T-X2`, `T-X4`, `T-X4v` and `T-X8` were stated under the source (form-at-end-of-`t−1`) convention while the register declares close-`m0` formation, the same defect fixed for T-X1 in v1.11. All four are reindexed above. **`T-X8` in particular changed meaning:** the source targets the calendar month being *held*, so under `m0` formation the lags are 23/35/47/59, not 24/36/48/60.

**T-X5 missingness (binding, A-share):** suspended and zero-volume days are **excluded from both day counts**, never counted as flat. Otherwise illiquidity manufactures apparent "continuous information."

**T-X7 role, pin one, they are mutually exclusive:** `T-X7a` standalone alpha (`Out: alpha`) **XOR** `T-X7b` momentum moderator (`Out: cond`, `TR-NONE`). A product activates exactly one; resolve by incremental value over T-X1.

**T-X8 missingness, pin one, never blend:** all-four-required (source-faithful, keeps the ¼ denominator) **XOR** mean-of-available-with-≥3 (separately named variant).

**Traps.** T-X1 CN grade is **D**: broad A-share monthly momentum is weak; benchmark, not production. Stage-2 `TR-SECRANK` **strips industry momentum**, owned by `US-T3`/`CN-T3`. Don't orphan or double-count. T-X2's σ is the **in-window residual SD of its own 36-month regression**, not P6's monthly IVOL; QEPM `adjRet9` is a *separate comparator*, not T-X2, and if built its denominator must be **P6's output**. T-X3 primary is **raw**, not residual. T-X4 overlaps F1 by construction.

---

## 5. Cross-sectional statistical risk (R)

| ID | Name | Out | Dir | TR | Formula | Min hist | Miss/tie | Dep | Own | Eff US | Eff CN | E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **R-X1** | IVOL-21 | screen | `−` | `TR-RANK` | `SD(ε)` over the prior calendar month, `ε` from **P6** | 15 obs | <15 → NA | P2,P6,P7 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:U` | C/C |
| **R-X2** | TOTVOL-252 | risk | `state` | `TR-STATE` | SD of daily total returns, trailing 252d | 120d | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/B |
| R-X2v | TOTVOL-36m | risk | `state` | `TR-STATE` | SD of monthly returns, trailing 36m | 24m | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | variant |
| **R-X3** | IDSKEW-21 | alpha | `−` | `TR-RANK` | **skewness of `ε`** over the prior calendar month (same vector as R-X1) | 15 obs | NA | P6,P7 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:U` | C / **C, > IVOL** |
| **R-X4a** | MAX1 | alpha | `−` | `TR-RANK` | max daily return in the prior calendar month | 15d | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | C/C |
| **R-X4b** | MAX5 | alpha | `−` | `TR-RANK` | mean of the 5 largest daily returns, prior month | 15d | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | variant |
| **R-X4c** | Limit-hit count | diag | `state` | `TR-NONE` | # sessions at ±limit, prior month | 15d | 0 is valid | P3 | `S:F D:A P:N` | n/a | `S:C D:P P:F` | CN |
| **R-X4d** | Close-at-limit flag | diag | `bin` | `TR-BINARY` | 1 if close = limit on the MAX1 day | n/a | 0 is valid | P3 | `S:F D:A P:N` | n/a | `S:C D:P P:F` | CN |
| **R-X4e** | Limit-lock duration | diag | `state` | `TR-NONE` | mean minutes locked at limit, prior month | 15d | NA | P3 (intraday) | `S:F D:P P:N` | n/a | `S:C D:P P:F` | CN |
| **R-X5** | CFVOL-16Q | alpha | `−` | `TR-RANK` | SD of the pinned ratio over 16 quarters | 16q | NA | P13 | `S:C D:B P:U` | `S:C D:B P:P` | `S:C D:T P:U` | C/C |
| **R-X6a** | Market beta (FP) | risk | `−` | `TR-STATE` | `β = ρ_{i,m}·σ_i/σ_m`, then **shrink `0.6β̂ + 0.4`**; σ from **1y daily**, ρ from **5y overlapping 3-day log returns** | σ≥120d, ρ≥750d | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/C |
| **R-X6b** | Market correlation | risk | `−` | `TR-STATE` | `ρ_{i,m}`, 5y overlapping 3-day log returns | 750d | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | B/C |
| **R-X6c** | Downside beta | risk | `−` | `TR-STATE` | β on days **market return < 0** (primary; below-median = variant) | 120 down-days | NA | P2 | `S:F D:A P:N` | `D:P P:U` | `S:C D:P P:F` | C/C |
| **R-X7** | ARB-RISK | risk | `+` | `TR-STATE` | residual σ of the stock regressed on an **equal-weight matched peer basket**, 252d window ending `m0` | 252d, **≥5 peers** | **<5 peers → `NA/insufficient-peers`** | P2,**P9** | `S:F D:A P:N` | `D:P P:U` | `D:P P:U` | B/C |

**R-X7 does NOT depend on CH3.** Its declared **primary** is the peer-basket residual regression (P2 + P9). The R-X1 IVOL proxy is only a *named baseline alternative*. v2.0's excluded register wrongly listed R-X7 among the CH3-blocked rows, corrected. R-X7's real blocker is **P9 PIT industry membership**.

**No composite cards.** `R-X6a/b/c` have separate signs and grades and **no frozen aggregation**: no `SYS-DEFENSIVE-COMP` is offered. The A-share limit complex (`R-X4a` + `R-X4c/d/e`) likewise has **no combination rule**: the latent uncapped return is **unobservable**, so do not fabricate a "limit-adjusted MAX." Compositing either would invent an aggregation no contract authorizes.

**`Dir` note on R-X1/R-X4/R-X3.** All carry `Dir: −` (high raw → low score) but `Out` differs: R-X1 is a **screen** (one-sided avoid, per the conditional-mispricing reading, high IVOL predicts lower returns among *overpriced* names, higher among *underpriced*), while R-X3/R-X4a are ranked alphas. Do not implement R-X1 as a symmetric factor.

**Traps.** `R-X2 ↔ R-X6a` horse race is **mandatory** (`β = vol × corr`). `R-X4a` absorbs and *reverses* R-X1's coefficient when both are included, this is why MAX/skew outrank classic IVOL. `R-X4 ↔ CN-B3` cross-file ablation required. `R-X3` is **realized** skew, not an expected-skewness estimate; **rank above IVOL for A-shares**. `R-X5` is owned by Fundamental F-stability, instantiate once. R-X6 is **defensive-first, not clean alpha**; leveraged BAB is a separate strategy contract. Expected-IVOL (EGARCH) has the **opposite sign** and is largely look-ahead. Never combined with R-X1.

---

## 6. Fundamental (F)

**Common:** Value-dep `P8, P13, P4/P5`. Publication = as-filed announcement date. `avg` = (beginning + ending)/2. **Missing ≠ zero.**
**PIT split (now applied per row, not just in prose):** **US `P:P`**. EDGAR as-filed submissions are timestamped, but a validated standardized panel (amendments, duplicate facts, units, taxonomy) must still be built. **CN `P:U`**. endpoints exist, vintage completeness unaudited.

### 6.1 Value (F1): RG `VALUE`

> **Base convention.** `(EQ)` = claim to *equity* holders, denominator market cap or book equity (**capital-structure-dependent**. `(EV)` = claim to *all* capital providers) **capital-structure-neutral**. The tag travels with the measure so composites are auditable for base-mixing. **Never apply either base to financials.**

| ID | Name | Base | Out | Dir | TR | Formula | Miss/tie | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|---|
| **F1-EP** | Earnings yield | EQ | alpha | `+` | `TR-RANK` | `NI_TTM / mcap` · **CN 扣非** | negative NI → **retain the value + flag**, do not NA | `S:F D:B` | `P:P` | `P:U` |
| **F1-BP** | Book-to-price | EQ | alpha | `+` | `TR-RANK` | `BookEquity / mcap` | negative book → NA + flag | `S:F D:B` | `P:P` | `P:U` |
| **F1-DY** | Dividend yield | EQ | alpha | `+` | `TR-RANK` | `Dividends_TTM / mcap` | no dividend → **0 valid** (real economic zero) | `S:F D:B` | `P:P` | `P:U` |
| **F1-FCFFEV** | FCFF yield | EV | alpha | `+` | `TR-RANK` | `FCFF / EV`: **sole enterprise cash yield in the base composite** | EV ≤ floor → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| **F1-SEV** | Sales yield | EV | alpha | `+` | `TR-RANK` | `Sales_TTM / EV` | EV ≤ floor → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| **F1-EBITEV** | Enterprise earnings yield | EV | alpha | `+` | `TR-RANK` | `NormalizedEBIT_TTM / EV` | EV ≤ floor → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| F1-ECFOEV | EnterpriseCFO yield | EV | variant | `+` | `TR-RANK` | `EnterpriseCFO / EV`: **nested in F1-FCFFEV**; never both | EV ≤ floor → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| F1-NOPATEV | NOPAT yield | EV | variant | `+` | `TR-RANK` | `NOPAT / EV` | EV ≤ floor → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| F1-EBITDAEV | EBITDA yield | EV | variant | `+` | `TR-RANK` | `EBITDA_TTM / EV` | EV ≤ floor → NA | `S:F D:B` | `P:P` | `P:U` |

**All EV rows are `S:C`, not `S:F`**. corrected in v2.1. Three unpinned items make them non-deterministic: **(i) the EV floor value**, **(ii) the `NormalizedEBIT` exceptional-item field map**, **(iii) `T_op_exact`'s field map.** (`F1-EBITDAEV` escapes (ii)/(iii) but still needs the floor, it inherits `S:C` via the EV rule; shown `S:F` own, `S:C` effective.)

**EV construction (frozen), MIXED timing, both clocks declared:**
```
EV = market cap + total debt (short + long) + minority interest + preferred − cash & equivalents
```
- **market cap** = **signal-date** price × **signal-date** shares outstanding
- **debt / cash / minority / preferred** = **latest causally-available filing**, as-filed, not restated
- **No zero-substitution** for a missing component → the `(EV)` measure is `NA`.

**⚠ Nonpositive-EV rule.** `EV ≤ floor` → **EV measures NA; keep `(EQ)` measures; report the excluded population separately; NEVER winsorize a tiny or negative denominator into apparent extreme cheapness.** *(Floor value undeclared, this is the `S:C`.)*

**Enterprise-cash chain: ONE authoritative form:**
```
NOPAT         = NormalizedEBIT · (1 − T_op)
EnterpriseCFO = NOPAT + D&A + NC_{ex-D&A} − ΔNOWC
FCFF          = EnterpriseCFO − capex
```
- `NC_{ex-D&A}` **excludes anything already in D&A or in working-capital liabilities** (provisions counted once). Signed: **add** non-cash expenses, **subtract** non-cash gains.
- `ΔNOWC` = Δ(noncash operating current assets − nondebt operating current liabilities). **Supplier-finance → debt in *both* balances.** Acquisitions, FX, restatement effects **excluded**.
- `capex` = PP&E + operating intangibles, **net of disposals**.
- **Do NOT code `CFO + after-tax interest`** (double-adds interest under IFRS/CN-ASBE, a reconciliation bridge only). **Do NOT code any `+ other non-cash charges` form** (double-counts amortization/provisions).

**`NormalizedEBIT`**: remove **only flagged non-recurring** items; **do NOT auto-remove recurring impairments or restructuring**; keep **reported EBIT unnormalized** as a robustness baseline. **CN: 扣非净利润 ≠ NormalizedEBIT** (扣非 is after interest *and* tax): build from operating profit minus the *operating subset* of 非经常性损益.

**`T_op`:** `T_op_exact` = observable company-period effective operating rate (`S:C`, not field-mapped) · `T_op_proxy` = **dated statutory** (US graduated top **35%** pre-2018 / **21%** after; CN **25%**, **15%** qualifying 高新: **never apply a post-2018 rate to a pre-2018 period**) · NOL rule: `EBIT ≤ 0 → T_op = 0`, **a realizability convention, not a marginal rate**.

**Composite:** build **`ValueEQ`**, **`ValueEV`**, **`ValueBoth`** as separate portfolios over their own coverage populations, combined **at the allocation level**. Cash-rich/nonpositive-EV firms stay in `ValueEQ`. Never deleted. Fixed sub-weights, coverage flags, minimum coverage, controlled renormalization.
**Trap:** `B/M × ROE` is E/P **by identity**.

### 6.2 Profitability (F2) & growth (F2b)

| ID | Name | Out | Dir | TR | Formula | Miss/tie | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|
| **F2-GPA** | Gross profit / **average** assets (harmonized) | alpha | `+` | `TR-RANK` | `GrossProfit_TTM / avgTotalAssets`: **generic asset-return measure, NOT canonical Novy-Marx** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-OPA** | Operating profit / **average** assets (harmonized) | alpha | `+` | `TR-RANK` | `OperatingProfit_TTM / avgTotalAssets`: **NOT Fama–French OP** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-GPA-NM** | **Gross profitability (Novy-Marx, source-faithful)** | alpha | `+` | `TR-RANK` | `(Revenue − COGS) / TotalAssets`: **book total assets, NOT averaged** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-OP-FF** | **Operating profitability (Fama–French, source-faithful)** | alpha | `+` | `TR-RANK` | `(Revenue − COGS − SG&A − InterestExpense) / BookEquity`: **book equity denominator, interest subtracted** | negative equity → NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-ROA** | Return on assets | alpha | `+` | `TR-RANK` | `NI_TTM / avgTotalAssets` · **CN 扣非** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-ROE** | Return on equity | alpha | `+` | `TR-RANK` | `NI_TTM / avgBookEquity` · **CN 扣非** | negative equity → NA | `S:F D:B` | `P:P` | `P:U` |
| **F2-ROIC** | Return on invested capital | alpha | `+` | `TR-RANK` | `NOPAT / avgInvestedCapital`; `IC = totalDebt + bookEquity − cash` | IC ≤ 0 → NA | **`S:C D:B`** | `S:C P:P` | `S:C P:U` |
| **F2-COP** | Cash operating profitability | alpha | `+` | `TR-RANK` | see build-up below | NA | `S:F D:B` | `P:P` | `P:U` |
| F2-RNOA | Return on NOA | variant | `+` | `TR-RANK` | `NOPAT / avg NOA` | n/a | **`S:O D:U P:U`**: §15 | `D:U P:U` | `D:U P:U` |
| F2-CRNOA | Cash RNOA | variant | `+` | `TR-RANK` | `EnterpriseCFO / avg NOA` | n/a | **`S:O D:U P:U`**: §15 | `D:U P:U` | `D:U P:U` |
| F2-OL | Operating-liability leverage | cond | `state` | `TR-NONE` | `operating liabilities / NOA` | n/a | **`S:O D:U P:U`**: §15 | `D:U P:U` | `D:U P:U` |
| **F2c-DAT** | Δ Asset turnover | alpha | `+` | `TR-RANK` | `(Sales_TTM/avgTotalAssets)_t − (Sales_TTM/avgTotalAssets)_{t−4q}`: **new v3.5, Sorensen–Hua–Qian (2005) Operating Efficiency composite**. Only existed as a Piotroski **binary** (`F8-FS9`, `>`/`<`) before this; this is the continuous alpha version | NA | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F2c-OPLEV** | Operating leverage (candidate reading A: degree-of-operating-leverage) | alpha | `+` | `TR-RANK` | `%ΔOperatingProfit_TTM / %ΔSales_TTM`: **⚠ attribution UNRESOLVED, v3.6.** Exhibit 1 names the factor "level of operating leverage" but gives no formula. This DOL-style reading is one plausible interpretation; the register's OWN `F2-OL` (operating liabilities/NOA, Nissim–Penman "operating liability leverage") is a second, textually closer candidate under the same author team's QEPM glossary: not independently confirmed either way from primary text. **Do not attribute this card to the source paper as settled; do not claim `F2-OL` is unrelated.** | `%ΔSales≈0 → NA`, floor `S:C` | `S:O D:B` | `S:O P:P` | `S:O P:U` |
| **F2c-CFOS** | Cash flow from operations / sales (alt-estimator of `F3-CFOA`) | alpha | `+` | `TR-RANK` | `CFO_TTM / Sales_TTM`: **downgraded `S:F → S:C` in v3.6**. Exhibit 1 gives the factor name only, not the calculation; CFO scope, reporting period and cross-accounting-regime treatment are unverified from the primary source, not merely "obvious." Sales-denominator variant of `F3-CFOA` (assets-denominator) | Sales≈0 → NA | `S:C D:B` | `S:C P:P` | `S:C P:U` |

**⚠ Sorensen–Hua–Qian (2005) Operating Efficiency composite (`OE`): v3.6 correction.** *Contextual Fundamentals, Models, and Active Management*, JPM 32(1), 23–36, same author team as the QEPM book already cross-mapped into this register. Their `OE` = {increase in asset turnover, operating leverage, CFO/sales}. **⚠ Source-verification caveat (all three):** the paper's Exhibit 1 gives factor **names**, not calculation formulas: `F2c-DAT`'s TTM/average-assets construction and `F2c-CFOS`'s scope are **plausible, standard constructions, not confirmed against the primary text**; treat both as `S:C` pending verification against the book's factor appendix, not as source-faithful replications. **`F2c-OPLEV`'s attribution is genuinely unresolved** (see the row note): it is registered as one candidate reading, not confirmed as *the* Sorensen–Hua–Qian factor, and the pre-existing `F2-OL` may be the closer match under this same author team's own QEPM terminology. **Retracted from v3.5:** the claims that "0/3 existed" and that `F2c-OPLEV` was "the first true operating-leverage card", both overstated a genuinely uncertain attribution as settled fact.

**⚠ F2-COP correction (v2.1): v2.0 contained a dimensional error.** It defined `CashOpProfit = OperatingProfit − accruals` while `F3-ACC` is a **scaled ratio** and operating profit is a **currency amount**. Those cannot be subtracted. The Ball et al. construction subtracts **working-capital accrual *amounts*, in currency**:
```
CashOpProfit = OperatingProfit
               − ΔAccountsReceivable − ΔInventory − ΔPrepaidExpenses
               + ΔDeferredRevenue + ΔAccountsPayable + ΔAccruedExpenses
F2-COP       = CashOpProfit / avgTotalAssets
```

**Verified (v2.2) against Ball, Gerakos, Linnainmaa & Nikolaev (2016)**: the accrual components removed from operating profitability are exactly the changes in **accounts receivable, inventory, prepaid expenses, deferred revenue, accounts payable and accrued expenses**. Six accounts, matching the form above → promoted **`S:R` → `S:F`**.

**CN 扣非 scoping (hard):** applies **only to NI-based measures** (`F1-EP`, `F2-ROA`, `F2-ROE`, `F5-SUE`). **Gross, operating and cash profitability keep native numerators**: 扣非净利润 cannot be the numerator of GP/assets or ROIC.
**⚠ Canonical-vs-harmonized naming (v2.3).** v2.2 attached canonical *names* to non-canonical *formulas*. **Novy-Marx gross profitability** divides by **book total assets** (not averaged); **Fama–French operating profitability** subtracts SG&A *and interest* and divides by **book equity** (not assets). Those are now separate cards (`F2-GPA-NM`, `F2-OP-FF`). The `avgTotalAssets` versions are retained as **harmonized** measures, useful, internally consistent with §6.3, but **they must not be reported under the source authors' evidence grades.**

**F2-ROE is leverage-contaminated**: pair with ROA/ROIC or DuPont-decompose. **Cash-vs-accrual primary is market-specific** (US: cash-based can subsume accruals; CN: ordinary operating profitability can subsume cash): decide by ablation, do not hard-code.
**No F2 composite is frozen**: six overlapping outputs under one budget.

**F2b: RG `PROFIT_GROWTH` · all `Dir +` · `TR-RANK` · YoY (`t` vs `t−4q`) on TTM numerators · each its OWN denominator**

| ID | Measure | Formula | Own | Eff US | Eff CN |
|---|---|---|---|---|---|
| **F2b-dROA** | ΔROA | `NI_TTM,t/avgAssets_t − NI_TTM,t−4q/avgAssets_t−4q` | `S:F D:B` | `P:P` | `P:U` |
| **F2b-dROE** | ΔROE | `NI_TTM,t/avgEquity_t − (…)_{t−4q}` · **CN 扣非** | `S:F D:B` | `P:P` | `P:U` |
| **F2b-dGM** | Δ gross margin | `GrossProfit_TTM,t/Sales_TTM,t − (…)_{t−4q}` | `S:F D:B` | `P:P` | `P:U` |
| **F2b-dOM** | Δ operating margin | `OpProfit_TTM,t/Sales_TTM,t − (…)_{t−4q}` | `S:F D:B` | `P:P` | `P:U` |
| **F2b-dCOP** | Δ cash op. profitability | `F2-COP_t − F2-COP_{t−4q}` | `S:F D:B` | `P:P` | `P:U` |

**Δ vs Δ²:** first difference is **primary**; second difference is a separate, noisier variant, not the default.
**⚠ Overlap guard:** realized ΔROE lives **here**; F5 carries the *expectations* read; q5 carries `dROE` as a predictor. These are **three different variables with a real attribution overlap** (§13): not an identity, but they must not become three votes on one mechanism.

### 6.3 Quality (F3) & strength (F4)

| ID | Name | Out | Dir | TR | Formula | Miss/tie | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|
| **F3-ACC** | Accruals (cash-flow-statement method) | alpha | `+` | `TR-RANK` | `−(NI_TTM − CFO_TTM) / avgTotalAssets`: **leading minus: higher score = lower accruals**. The "cash flow statement" accrual variant, Hribar–Collins (2002) terminology | NA | `S:F D:B` | `P:P` | `P:U` |
| **F3-ACC-BS** | Accruals (balance-sheet method, alt-estimator of `F3-ACC`) | alpha | `+` | `TR-RANK` | `−[(ΔCA − ΔCash) − (ΔCL − ΔSTD − ΔTP) − Dep] / avgTotalAssets` (Sloan 1996: **`−Dep` corrected in v3.6, was omitted in v3.5**; ΔCA=Δcurrent assets, ΔCL=Δcurrent liabilities, ΔSTD=Δshort-term debt, ΔTP=Δtaxes payable, Dep=depreciation & amortization) | NA | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F3-CFOA** | Cash flow / assets | alpha | `+` | `TR-RANK` | `CFO_TTM / avgTotalAssets` | NA | `S:F D:B` | `P:P` | `P:U` |
| F3-CFONI | CFO / NI | diag | `+` | `TR-NONE` | `CFO_TTM / NI_TTM` | **only for materially positive NI (threshold `S:C`); else unavailable**. explodes/flips near NI≈0 | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F4-NDE** | Net debt / EBITDA | penalty | `tail−` | `TR-TAIL` | `(totalDebt − cash) / EBITDA_TTM` | **EBITDA ≤ 0 → NA + distress flag**, never a large positive | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F4-ICOV** | Interest coverage | penalty | **`+inv`** | `TR-TAIL` | `EBIT_TTM / InterestExpense_TTM` | **interest = 0 → NA + "no-debt" flag**, not ∞ | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F4-DA** | Debt / assets | penalty | `tail−` | `TR-TAIL` | `totalDebt / totalAssets` | NA | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| **F4-CR** | Current ratio | penalty | **`+inv`** | `TR-TAIL` | `currentAssets / currentLiabilities` | CL = 0 → NA | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| F4-ALTZ | Altman-Z | **diag only** | `+` | `TR-NONE` | 5-factor Z | **never additive with F2/F4** | `S:R D:B` | `S:R P:P` | `S:R P:U` |
| F4-OHLO | Ohlson-O | **diag only** | `−` | `TR-NONE` | 9-factor O | same restriction | `S:R D:B` | `S:R P:P` | `S:R P:U` |
| **F4-CNIBD** | 有息负债率 | penalty | `tail−` | `TR-TAIL` | `interest-bearing debt / totalAssets` | NA | `S:C D:B` | n/a | `S:C P:U` |
| **F4-CNDCDD** | 大存大贷 flag | penalty | `bin` | `TR-BINARY` | 1 if cash/assets **AND** IB-debt/assets **both** above thresholds | **both thresholds undeclared** | `S:C D:B` | n/a | `S:C P:U` |

**⚠ `Dir` is the v2.1 fix for F4.** All four core ratios are `Out: penalty`, but their raw directions **differ**: high `F4-NDE` and `F4-DA` are **bad** (`tail−`); high `F4-ICOV` and `F4-CR` are **good** (`+inv`). v2.0 gave no direction, so a programmer could not tell whether to negate, invert or threshold. **`+inv` specifically means: do not naively negate**. coverage is unbounded above and undefined at zero interest, so use a bounded inverse or an absolute tail tier.
**All F4 rows are `S:C`** because `TR-TAIL` requires **declared absolute thresholds**, which do not exist yet. This is honest: a tail penalty without thresholds is not codeable.
**⚠ F3/F4 target typing:** validated on **tail/distress/drawdown reduction net of opportunity cost: NOT rank-IC.** Grading them as alpha rows is a category error. F8 overlays inherit this.
**Distance-to-default is deliberately absent**: it uses market equity and volatility → hybrid overlay, not pure accounting.
**F3 caveats:** the US standalone accrual anomaly **decayed post-publication** → component, not isolated alpha. CN: operating profitability may subsume accruals; **screen role likely > symmetric alpha.**
**⚠ `F3-ACC-BS` added v3.5, the two accrual constructions are not interchangeable.** Sorensen–Hua–Qian (2005) list "accounting accruals (balance sheet)" and "accounting accruals (cash flow statement)" as **two separate factors in their own Accounting Accruals composite**, not one factor with two implementations. Hribar–Collins (2002) show the balance-sheet method (`F3-ACC-BS`) and the cash-flow-statement method (`F3-ACC`, already in the register) **diverge materially around M&A, discontinued operations and FX translation**: the CFO-based `F3-ACC` is generally the cleaner estimator, which is presumably why the register only had it before this pass, but the balance-sheet variant is a distinct, independently-motivated factor per the source paper, not a redundant alternative computation of the same number.

### 6.4 Investment (F6) & capital allocation (F7)

| ID | Name | Out | Dir | TR | Formula | Miss/tie | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|
| **F6-AG** | Asset growth | alpha | `−` | `TR-RANK` | `(AT_t − AT_{t−1})/AT_{t−1}` | NA | `S:F D:B` | `P:P` | `P:U` |
| **F6-CAPEXA** | Capex / assets | alpha | `−` | `TR-RANK` | `capex_TTM / avgTotalAssets` | NA | `S:F D:B` | `P:P` | `P:U` |
| **F6-INVG** | Inventory growth | alpha | `−` | `TR-RANK` | `(Inv_t − Inv_{t−1})/avgTotalAssets` | inventory-free industries → NA, **not 0** | `S:F D:B` | `P:P` | `P:U` |
| **F6-GWG** | Goodwill growth | alpha | `−` | `TR-RANK` | `(GW_t − GW_{t−1})/avgTotalAssets` | no goodwill → **0 valid** | `S:F D:B` | `P:P` | `P:U` |
| F6-NOAG | NOA growth | alpha | `−` | `TR-RANK` | `(NOA_t − NOA_{t−1})/avgTotalAssets` | unfixed NOA contract | **`S:O D:U P:U`**: §15 | `D:U P:U` | `D:U P:U` |
| **F6-q5** | Expected investment growth | alpha | **`+`** | `TR-RANK` | long-form card below | see card | `S:R D:B` | `S:R P:P` | `S:R P:U` |
| **F7-NPY** | Net payout yield | alpha | `+` | `TR-RANK` | `(dividends + repurchases − issuance) / mcap` | NA | `S:F D:B` | `P:P` | `P:U` |
| **F7-DSH** | Δ diluted shares | alpha | `−` | `TR-RANK` | `(dilShares_t − dilShares_{t−1})/dilShares_{t−1}`: **NOT announced buybacks** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F7-DBNETIS** | Net debt issuance | alpha | `−` | `TR-RANK` | `(debtIssued − debtRepaid)/totalAssets`, net LT + net ST. **NOT `ΔNetDebt`** | NA | `S:F D:B` | `P:P` | `P:U` |
| **F7-NSI1Y** | Net share issuance | alpha | `−` | `TR-RANK` | `ln(splitAdjShares_t / splitAdjShares_{t−1})`: excludes cash dividends | NA | `S:F D:B` | `P:P` | `P:U` |
| **F7-CSI5Y** | Composite share issuance | alpha | `−` | `TR-RANK` | `ln(ME_t/ME_{t−5}) − r^{log}_{t−5,t}` | **<5y listing → missing stays missing, NEVER imputed neutral** | `S:F D:B` | `P:P` | `P:U` |
| F7-FIN | NSI+CSI family score | alpha | `−` | `TR-TAIL` | **tail classifications** of NSI1Y + CSI5Y: **not** a 50/50 average | thresholds undeclared | `S:C D:B` | `S:C P:P` | `S:C P:U` |
| F7-EFNOA | External financing / NOA | variant | `−` | `TR-RANK` | `(net debt issuance + net equity issuance) / avg NOA`: **new v3.5, Sorensen–Hua–Qian (2005) External Financing composite**; NOA-denominator version of the combined channel already covered on a total-assets/mcap basis by `F7-DBNETIS`+`F7-NPY` | n/a | **`S:O D:U P:U`**. blocked by the same NOA field contract as `F2-RNOA` (§15) | `D:U P:U` | `D:U P:U` |
| F7-DINOA | Debt issuance / NOA | variant | `−` | `TR-RANK` | `(debtIssued − debtRepaid) / avg NOA`: NOA-denominator variant of `F7-DBNETIS` (which uses total assets) | n/a | **`S:O D:U P:U`**. same NOA blocker | `D:U P:U` | `D:U P:U` |
| F7-EINOA | Equity issuance / NOA | variant | `−` | `TR-RANK` | `netEquityIssuance / avg NOA`: NOA-denominator variant of `F7-NSI1Y` (which is a share-count log-ratio, not NOA-scaled) | n/a | **`S:O D:U P:U`**. same NOA blocker | `D:U P:U` | `D:U P:U` |

**F6/F7 boundary (hard):** F6 = **real-investment** side only; financing-side items belong **exclusively** to F7. Debt-financed investment → an F6×F7 interaction, **never a third vote**. Debt **level** → F4; debt **issuance** → F7.

**⚠ ARCHITECTURE NOTE (v3.6 correction, not a market-regime finding, not a general 3–8x claim).** Sorensen–Hua–Qian (2005)'s contexts are **cross-sectional company characteristics** (value/growth/earnings-variability), not market regimes over time, the paper fits `w ∝ V⁻¹·IC` separately within high/low buckets of each characteristic and blends toward each stock's proximity to a bucket, not a discrete one-context-per-stock, continually-reoptimized assignment. **The magnitude claim is narrower than v3.5 stated:** two specific composite-weight comparisons are numerically supportable directly from the paper's exhibits: `EF` 43.0% (high value) vs 5.1% (low value); `OE` 52.7% (high growth) vs 16.9% (low growth): this is **not** evidence that "all factor weights move 3–8x." The **earnings-variability context was not clearly differentiated from the static (uncontextualized) model** in the paper's own results, the value and growth contexts were the strongest. Sample = Russell 1000, Jan 1987–Sep 2004; a full source-faithful reproduction used Compustat Quarterly, IBES QFS and Barra US E3: **IBES and Barra are licensed**, so exact replication is not a free-data project even before this register's own consensus-data gap is considered. **This register has no mechanism for cross-sectional contextual reweighting**, but it substantially **overlaps the existing Combination open item (d), moderator routing** (`f_context = m(context)·f`): it is better framed as a registered hypothesis about stock-context × factor interactions (candidate for hierarchical shrinkage across buckets) than as a wholly new architectural decision. Cross-referenced from `Indicators_Pool_Combination_v1.md` §13.
**F7, three DISTINCT channels, one budget:** equity payout/NSI (`BB2P`), financing policy (`DBNETIS`), combined capital supply (`BB2EV`/`XF`). **Not algebraic re-expressions**: re-derive each formula and confirm sign and denominator; do not copy dated textbook labels.
**CN construction:** total vs free-float shares; rights issues and private placements; stock dividends and splits; equity-financed acquisitions. **解禁 unlocks are supply/flow, NOT NSI.**
**⚠ CN regime break:** the **2024 国九条** reform changed this family's distribution (ST warnings for insufficient dividends, buybacks-via-bid counted as cash dividends, record payouts, 市值管理 pressure on SOEs). **Pre-2024 and post-2024 are different regimes, walk-forward flag mandatory.** SOE vs POE is a conditioning variable.

#### F6-q5: Expected investment growth (Hou–Mo–Xue–Zhang), `S:R`

> **⚠ Sign is OPPOSITE to realized investment.** High *forecast* investment growth predicts **higher** returns: F6-AG is `−`. **Never composited with negatively-signed realized investment. Own RG `EXP_INV_GROWTH`.**

- `(I/A)_t = (AT_t − AT_{t−1}) / AT_{t−1}` · response `d₁I/A = (I/A)_{t+1} − (I/A)_t`
- predictors: **Tobin's `q`**, **`Cop`**, **`dROE`**; predictors and dependent **winsorized 1%/99%**; **monthly cross-sectional WLS weighted by market equity**

**⚠ `Cop` corrected (v2.1): v2.0's wording double-added R&D.** Written as "`SG&A(excl. R&D) + R&D`" it reads as removing R&D from SG&A and then adding it back. The source subtracts the **reported SG&A field, which already embeds R&D**, and the `+R&D` term **reverses that embedding**:
```
Cop = REVT − COGS − XSGA + XRD
      − ΔRECT − ΔINVT − ΔXPP
      + ΔDR + ΔAP + ΔXACC
      (scaled by total assets)
```
where `XSGA` is the **as-reported** SG&A line **including** R&D, and `+XRD` adds R&D back exactly once. **Verify the full account list and the paper's component-level missing-value fallbacks against source §3.1 before freezing.** This is a cash-based operating profitability in the Ball et al. lineage: **not** an unspecified `CFO/assets`.

**Estimation is already rolling-and-lagged, there is no "full-sample" reading.** Coefficients = **average slopes of the prior 120 monthly cross-sectional regressions** (**≥30-month minimum**), regressors further lagged to match the response horizon.
**⚠ Response-maturity PIT rule:** a coefficient estimated at month `s` enters the library used at decision date `t` **only after (a)** the 12-month window `[s, s+12m]` has elapsed **AND (b)** the statements measuring that response are published. `log(q)` and `Cop` from the **latest fiscal year ending ≥4 months earlier**; `dROE` from the **latest announced quarterly earnings (4-month fallback)**.
**Cadence:** monthly rebalance, 1-month return; 6/12-month overlapping holds = decay variants.
**Buildable, q5 needs NO consensus feed.** Accounting and market inputs only.
**Trap:** a ranked `q / CFO / ΔROE` composite is a **separately named approximation, NOT source-faithful q5**.
**E:** US **B** research · CN **D** unverified.

---

## 7. Event indicators (F5): RG `EARN_EVENT`

| ID | Name | Out | Dir | TR | Formula | Dep | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|
| **F5-CAR** | Announcement CAR | alpha | `+` | `TR-EVENTZ` | `CAR = Σ_{τ=−2}^{+1} (r_i − r_m)`: **4 trading days**, simple **market-adjusted, NOT beta-estimated** | P2,P14 | `S:F D:B` | `P:P` | `P:U` |
| F5-CARv | Industry/beta-adjusted CAR | variant | `+` | `TR-EVENTZ` | same window, adjusted benchmark | P2,P9,P14 | `S:F D:P` | `P:U` | `P:U` |
| **F5-SUE** | Standardized unexpected earnings | alpha | `+` | `TR-EVENTZ` | `SUE = (E_q − E_{q−4}) / max(σ(ΔE_{trailing 8q}), floor)` | P13,P14 | **`S:R D:B`** | `S:R P:P` | `S:R P:U` |
| **F5-CNPRE** | 预告 surprise | alpha | `+` | `TR-EVENTZ` | interval-valued guidance vs declared reference | P14 | **`S:C D:B`** | n/a | `S:C P:U` |
| **F5-CNEXP** | 快报 surprise / revision | alpha | `+` | `TR-EVENTZ` | 快报 result vs the prior ladder rung | P14 | **`S:C D:B`** | n/a | `S:C P:U` |

**`TR-EVENTZ` applies to all five**: event surprises standardize **within the announcement cohort**, not against the calendar cross-section. Using `TR-RANK` here would compare a January reporter against an April reporter.

**F5-CAR.** Measures the market's *initial interpretation*; **PEAD is the subsequent drift, the tradable part.** **Do not make CAR and ABR two indicators**: the beta-estimated version is `F5-CARv`. **`CLK-FILING`, three timestamps, state all three:** event **day 0** (post-close disclosure → day 0 = next session) · **signal completion = after the close of day +1** (the `[−2,+1]` window means the CAR does not exist before then) · **first permissible execution = day +2's first feasible session.** v2.3 implied this in prose but never as a field; the `[−2,−1]` leg is leakage, not tradable. Targets 5/21/63d, short horizons primary.
**⚠ CN event clock:** compute a **separate CAR per economically meaningful event on the ladder**: the formal report is often *not* the first release. Post-close disclosure → **day 0 = first subsequent session**. **Broad-market primary benchmark**; board/industry-adjusted as robustness (STAR/ChiNext vs Mainboard beta differences contaminate raw market-adjusted CAR). **Limits and suspensions can make a strong-CAR name untradeable.**

**F5-SUE: `S:R`, two load-bearing items.** v1.0 named only the expectation basis; the **standardization denominator** matters equally. Above: **seasonal random walk** expectation (`E_{q−4}`, the only consensus-free variant) with the **trailing-8-quarter SD of seasonal differences** as denominator and a **mandatory σ-floor** (without it, SUE explodes when `σ(ΔE) ≈ 0`). **Verify the 8-quarter window and floor convention before freezing.**

**F5-CN ladder.** `预告 → 预告修正 → 快报 → 正式报告 → 重述`, **field-level availability: each field is released only at the event that actually disclosed it.** A 预告 profit range reveals **no** cash-flow, balance-sheet or detailed profitability data. Do not backfill.
**`S:C`, two unpinned choices:** (i) **interval encoding** (midpoint + width vs bounds); (ii) **the reference the interval is a surprise *against***: prior-year same-period actual, prior ladder rung, or a time-series expectation. **Without (ii) there is no surprise, only a level.**
**⚠ Selection bias:** handle **mandatory vs voluntary** separately. **Firms without a 预告 are NOT neutral-surprise firms**: treating a missing 预告 as zero manufactures a signal out of a disclosure choice.
This is **company self-guidance, not analyst consensus**: the reason these rows are buildable while F5-REV is not.

---

## 8. Accounting overlays

### 8.1 Piotroski F-Score: `S:F` (**source-faithful, resynced to the owning contract in v2.3**) · 9 binary components · `TR-BINARY` · sum 0–9

> **⚠ v2.2 carried a HARMONIZED version while claiming the components were "verified."** It used `NI / avgAssets`. Piotroski (2000) uses **net income before extraordinary items scaled by BEGINNING-of-year total assets**, and the owning contract ([Fundamental §F-Score](Indicators_Pool_Fundamental_v1.md)) already recorded this correctly. The register was wrong and the contract was right. Corrected below; the average-assets version survives only as an explicitly named variant.

**Population:** source-faithful application is to **high-B/M (value) firms**: F-Score was designed for financially weak-looking value stocks, not the whole universe. Extreme comparison in the source is **F 8–9 vs F 0–1**.

| ID | Component | Rule (1 if true) |
|---|---|---|
| F8-FS1 | ROA positive | `NI_before_XO,t / Assets_{t−1} > 0` |
| F8-FS2 | CFO positive | `CFO_t / Assets_{t−1} > 0` |
| F8-FS3 | ΔROA | `ROA_t > ROA_{t−1}` |
| F8-FS4 | Accrual quality | `CFO_t / Assets_{t−1} > ROA_t` |
| F8-FS5 | Leverage | `LTDebt_t/avgAssets_t < LTDebt_{t−1}/avgAssets_{t−1}` |
| F8-FS6 | Liquidity | `CurrentRatio_t > CurrentRatio_{t−1}` |
| F8-FS7 | Dilution | **no** new common equity issued in year `t` |
| F8-FS8 | Gross margin | `GrossMargin_t > GrossMargin_{t−1}` |
| F8-FS9 | Asset turnover | `Sales_t / Assets_{t−1} > Sales_{t−1} / Assets_{t−2}` |

**Annual, as-reported data available at the rebalance date.** `F8-FS = Σ F8-FS1…9`, then `TR-RANK` on the sum.
**Named variant, not the primary:** `F8-FS-avg`: the same nine rules on **average** assets. Harmonizes with §6.2/§6.3 denominators but **is not Piotroski**. Never report it under the source grade.
**Tie/missingness, still `S:C` at the composite level:** strict `>` scores exact ties 0 (state it); **a missing component is NOT a 0**: either the whole score is NA or a declared minimum-component rule with rescaled denominator applies. Pin one.

### 8.2 Mohanram G-Score: `S:C` · 8 binary components · `TR-BINARY` · sum 0–8

**Population (source-faithful, was missing in v2.2):** apply to the **lowest B/M quintile (growth)** first; medians are computed **within that low-B/M population**, by **two-digit SIC industry** (CN: 申万 equivalent), **not** across the whole market. Intensity variables use **beginning assets**. Variability windows are **five years**, with a declared shorter-history minimum.

| ID | Component | Rule (1 if true) |
|---|---|---|
| F8-GS1 | ROA vs peers | `ROA_t >` low-B/M industry median |
| F8-GS2 | CFO vs peers | `CFO/Assets_{t−1} >` industry median |
| F8-GS3 | Accrual quality | `CFO_t > NI_t` |
| F8-GS4 | Earnings stability | earnings variability (5y) `<` industry median |
| F8-GS5 | Growth stability | sales-growth variability (5y) `<` industry median |
| F8-GS6 | R&D intensity | `R&D/Assets_{t−1} >` industry median |
| F8-GS7 | Capex intensity | `capex/Assets_{t−1} >` industry median |
| F8-GS8 | Advertising intensity | `advertising/Assets_{t−1} >` industry median |

**Dep P9**, every median is industry-relative → inherits P9's PIT-membership problem (`Eff D:P P:U` both markets).
**Minimum history is NOT open, frozen in v2.4:** the variability windows are **five years with a minimum of three**; below three years the variance is not computable. *(The **source assigns the stability signal 0** when history is insufficient, the firm simply does not earn the point. Some third-party implementations mark it `na` instead; that is an adaptation, not an alternative reading of the paper.)*
**`S:C` because ONE thing remains unpinned, which of two NON-equivalent options you run:** **source-faithful primary**: insufficient history → **0** (the firm does not earn the point): versus **production-conservative variant**: insufficient history → **NA** + coverage gating, so thin history is not silently penalised. These give materially different scores for young firms, and young firms are exactly the low-B/M growth population G-Score targets. Declare one; the source-faithful option is the default, the source's original handling must be declared *separately* from any more conservative production variant. **F8-GS6/7/8 have material CN disclosure gaps** (R&D, and especially advertising) → `D:P`; a missing intensity field is **not** a 0.

### 8.3 Piotroski–So expectation-error matrix: `F8-PS` · **matrix `S:F`, effective `S:C`** · `Out: cond` · `TR-NONE`

> **⚠ v2.2 called this "undeclared" and left terciles-vs-quintiles open. It was already frozen in the owning contract** ([Fundamental §3.1](Indicators_Pool_Fundamental_v1.md)). A second split-authority failure in the same section.

**Source-faithful annual 3×3, frozen:**
- **Value axis (B/M):** glamour `< 30th percentile` · middle `30th–70th` · value `> 70th percentile`
- **Strength axis (F-Score):** low `0–3` · middle `4–6` · high `7–9`

**Output:** the 3×3 cell label.
**⚠ v2.3 mislabelled the corners.** Both tradable legs are **INCONGRUENT**, fundamentals *contradict* the expectation embedded in price:
- **Long, incongruent VALUE:** high B/M (market expects weakness) × **high** F-Score (fundamentals are strong).
- **Short/avoid, incongruent GLAMOUR:** low B/M (market expects strength) × **low** F-Score (fundamentals are weak).

The **congruent** cells (where fundamentals *confirm* the embedded expectation) are **high B/M × low F** and **low B/M × high F**, and they show little to no value/glamour spread. Calling the long leg "congruent-value" inverted the paper's central construct.

**Keep these cutoffs fixed for the primary replication.** Sector-relative B/M, and E/P, C/P or composite-value axes, are **named robustness variants**.
**⚠ Effective readiness is `S:C`, not `S:F`.** The *matrix structure* is frozen, but one axis **is** `F8-FS`, whose composite missing-component rule is still unpinned. By the register's own worst-of-dependencies rule, `F8-PS` cannot be deterministic for firms with incomplete data until that choice is made. v2.3 marked it `S:F` and listed it in T1, both wrong.
**Not a product of raw variables**: a two-dimensional conditional sort. It is also not proof that B/M measures mispricing rather than risk.

**Overlay guard (all §8):** components draw on the same inputs as F2/F3/F4/F6/F7. **An overlay must not re-vote a signal already carried by its underlying family inside the same budget.**

---

## 9. Market structure

| ID | Name | Out | Dir | TR | Min hist | Dep | Own | Eff | E |
|---|---|---|---|---|---|---|---|---|---|
| **MS-C3a** | Price delay (D1) | cond | `+` | `TR-NONE` | 52 weekly obs | P2 | `S:F D:A P:N` | `D:P P:U` | B/C |

**Price delay (Hou–Moskowitz 2005): verified v2.2, `S:F`.** **Weekly returns = compounded daily returns Wednesday-to-Wednesday** (closing prices; bid-ask midpoint plus dividends when a close is unavailable). Weekly frequency is deliberate, it identifies delayed responders without high-frequency noise. Two regressions over a rolling year with **four lags**:
```
unrestricted:  r_{i,t} = α + β·r_{m,t} + Σ_{n=1}^{4} δ_n·r_{m,t−n} + ε
restricted:    r_{i,t} = α + β·r_{m,t} + ε           (all δ_n = 0)

Delay = 1 − R²_restricted / R²_unrestricted
```
High delay = slow diffusion. **`D1` (the `R²`-ratio above) is the declared primary.** `D2` and `D3` are **named variants** that weight the lag coefficients by `max[m − |m − n|, 0]` with **`m = 4`**, so that higher-order lags count more (they are more informative about delay, and less precisely estimated). D1 does not distinguish short from long lags or estimate precision, that is exactly what D2/D3 add. **One primary: D1.**

**Evidence note:** the most-delayed firms command a large premium that **captures the size effect and half the value premium**, so `MS-C3a` overlaps `X-SIZE` and `F1-*` heavily and must be ablated against both, not treated as independent.
**Role: moderator / research conditioner. Never an alpha sign.** MS-C3's analyst-coverage and dispersion legs are excluded (§15); this is the delay leg only.

---

## 9b. Crowding, leverage & forced-flow risk (MS-R): v2.7

**⚠ STATUS: REGISTERED RESEARCH OUTLINE, not a frozen implementation section.** v2.6 overstated this, it marked cards `S:F`, claimed the summary states were "consumed once by Combination" (they are **not wired**. See §9b.5), and bundled multiple scalars under single IDs. v2.8 atomizes to one-ID-one-scalar, downgrades readiness to honest values (**no newly-specified MS-R construction is `S:F`**, only `MS-R8a`, a cross-reference to the already-frozen `X-ILLIQ`, carries `S:F`; CoMomentum, the nearest new construction, is `S:C`), and relabels the A-share leverage cards as *vulnerability*, not *forced flow*. Treat this as the design contract for a subfamily still being specified.

**Origin & rule (unchanged, correct):** the July-2026 momentum crash, a measurable chain `crowding → forced selling → liquidity stress → factor crash`. **HARD RULE: no MS-R output emits an alpha sign**. every card is `risk`/`state`/`cond`/`diag`, consumed by PortfolioRisk/Combination as a cap/scalar. **Article-number caution:** the 92/98-percentile figures are proprietary; *"leverage was retail not institutional"* is **not identifiable** from public data (absence of observable institutional leverage ≠ its absence); *"liquidity did not withdraw"* must be **tested** via §9b MS-R8, never inferred from a flat index.

### 9b.1 Atomic cards

**Common:** Out ∈ {`state`,`cond`,`diag`} only. A-share rows inherit `P4` (PIT ST-universe) and `P9` (PIT industry) → their `Eff CN` is bounded by those even where own-readiness is higher.

| ID | Name | Out | Formula / cross-ref (one scalar) | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|
| **MS-R2a** | CoMomentum: winner leg | state | `mean_{i∈W} Corr(ε_i, ε̄_{W\{i}})`, 52w residuals on 12-1 winner decile | `S:C D:A P:N` | `D:P P:U` (P5) | `D:T P:U` (P4/P9) |
| **MS-R2b** | CoMomentum: loser leg | state | same on the loser decile | `S:C D:A P:N` | `D:P P:U` (P5) | `D:T P:U` (P4/P9) |
| **MS-R3a1** | Momentum×theme cosine: long leg | state | `cos(w_MOM_long, w_theme)` (never net L−S: it cancels) | `S:C D:B P:U` | `D:B P:U P9` | `D:T P:U P4/P9` |
| **MS-R3a2** | Momentum×theme cosine: short leg | state | `cos(w_MOM_short, w_theme)` | `S:C D:B P:U` | `D:B P:U P9` | `D:T P:U P4/P9` |
| **MS-R3b** | Sector-HHI: momentum long leg | state | `Σ_s share_s²` over the long leg | `S:C D:A P:N` | `D:B P:U` (P9) | `D:T P:U` (P4/P9) |
| **MS-R3c** | Sector-HHI: momentum short leg | state | same, short leg | `S:C D:A P:N` | `D:B P:U` (P9) | `D:T P:U` (P4/P9) |
| **MS-R3d** | Momentum-return theme R² | state | `R²` of factor return on AI/semi/high-β/growth basket returns: **needs a frozen thematic basket + factor construction, not raw prices** | `S:C D:A P:N` | `D:P P:U` (P5 + basket def.) | `D:T P:U` (P4/P9 + basket def.) |
| **MS-R4a** | Holdings overlap | state | AUM-weighted pairwise holdings overlap (fund universe) | `S:O D:L P:U` | `D:L P:U` (**N-PORT access itself is public, but no public implementation of the overlap construction is specified here: effective readiness stays at Own until one is**) | `D:L P:U` (same reason; `fund_portfolio` access ≠ a specified construction) |
| **MS-R4b** | Greenwood–Thesmar fragility | state | `G_i = W_i' Ω W_i / mcap_i²`, `Ω` = fund-flow covariance | `S:O D:L P:U` | `D:L P:U` | `D:L P:U` |
| **MS-R5** | Days-to-liquidate (external proxy) | cond | `disclosed_holding_$ / (p · ADV$)`, **externally-disclosed positions only**: **ownership boundary: MarketStructure owns this formula for external holdings; PortfolioRisk owns the identical computation applied to this book's OWN weights (never read here)** | `S:C D:B P:U` | `D:B P:U` | `D:T P:U` |
| **MS-R6a** | Leveraged-ETF rebalance pressure (US) | state | `Σ_j L_j(L_j−1)A_{j,t−1}r_t / ClosingAuction$` (ADV$ fallback) | `S:C D:B P:U` | `D:B P:U` | n/a (no CN analog) |
| **MS-R6b-US** | Trend-book trigger distance: US | state | `ΔP` to sign-flip of the reconstructed trend book (`US-T1` + vol-target) | `S:C D:A P:N` | `D:A P:N` | n/a |
| **MS-R6b-CN** | Trend-book trigger distance: CN | state | same construction on `CN-T1`; **not a CTA proxy in China** (CTA-style managed-futures penetration is minimal in A-shares: this reads mechanical trend-follower exposure generally, not the same institutional base) | `S:C D:T P:U` | n/a | `D:T P:U` (P4/P9) |
| **MS-R6c-own** | Vol-target deleveraging: own book | state | `AUM_own·(σ*/σ̂_t − σ*/σ̂_{t−1})`: **ownership boundary: MarketStructure freezes the formula; PortfolioRisk owns its evaluation against this book's own AUM/weights: this card is a formula reference, not a computed value here** | `S:C D:A P:N` | `D:A P:N` | `D:T P:N` |
| **MS-R6c-mkt** | Vol-target deleveraging: industry est. | state | same with **estimated external AUM** (not observable) | `S:O D:L P:U` | `D:L P:U` | `D:L P:U` |
| **MS-R7a1** | CN margin vulnerability: level | state | = `CN-N2a` (融资余额/float): **leverage present, NOT forced sale** | `S:C D:T P:U` | n/a | `D:T P:U` |
| **MS-R7a2** | CN margin vulnerability: acceleration | state | = `CN-N2b` (21d Δ) | `S:C D:T P:U` | n/a | `D:T P:U` |
| **MS-R7b1** | CN pledge vulnerability: level | state | = `CN-N5a` (pledged/total): **overhang, NOT liquidation** | `S:C D:T P:U` | n/a | `D:T P:U` |
| **MS-R7b2** | CN pledge vulnerability: change | state | = `CN-N5b` (Δ pledge ratio) | `S:C D:T P:U` | n/a | `D:T P:U` |
| **MS-R7c** | CN forced-sale **events** | state | margin-call / pledge-liquidation / auction announcements (the actual `ForcedFlow_CN`) | `S:O D:B P:F` | n/a | `D:B P:F` |
| **MS-R8a** | Amihud illiquidity: raw stock-level | state | **cross-ref `X-ILLIQ`**: no parallel metric | `S:F D:A P:N` | `D:A P:N` | `D:T P:N` |
| **MS-R8a-agg** | Amihud illiquidity: crowded-basket aggregation | state | basket-weighted `MS-R8a` over the momentum/theme basket | `S:C D:A P:N` | `D:P P:U` (basket formation, P5) | `D:T P:U` (P4/P9) |
| **MS-R8b** | Corwin–Schultz spread estimator | state | high-low spread estimator (daily prices) | `S:C D:A P:N` | `D:A P:N` | `D:T P:N` |
| **MS-R8c** | Short-horizon reversal (MM-P&L proxy) | state | 1–5d reversal magnitude of the crowded basket | `S:C D:A P:N` | `D:P P:U` (basket via P5) | `D:T P:U` (P4/P9) |
| **MS-R8d1** | Quoted depth | state | top-of-book / N-level displayed size: **direct "did MMs withdraw" test** | `S:O D:L P:U` | `D:L P:U` | `D:L P:U` |
| **MS-R8d2** | Kyle-λ price impact | state | slope of price vs signed order flow | `S:O D:L P:U` | `D:L P:U` | `D:L P:U` |
| **MS-R9** | BadReactionBreadth | cond | `#{SUE>0 ∧ CAR<0} / #{SUE>0}`: pin event type, expectation basis, CAR window/benchmark, min-announcers, controls | `S:R D:B P:P` | `D:B P:P` (EDGAR/price) | `D:T P:F` |
| **MS-R10a** | Reversal trigger: factor drawdown | state | drawdown of the L/S factor from trailing high: **inherits the momentum factor's own PIT universe** | `S:C D:A P:N` | `D:P P:U` (P5) | `D:T P:U` (P4/P9) |
| **MS-R10b** | Reversal trigger: breadth rotation | state | equal-weight minus cap-weight return | `S:C D:A P:N` | `D:P P:U` (P5) | `D:T P:U` (P4) |
| **MS-R10c** | Reversal trigger: long/short β gap | state | `β_long − β_short` to market | `S:C D:A P:N` | `D:A P:N` | `D:T P:N` |
| **MS-R10d** | Reversal trigger: correlation spike | state | Δ avg pairwise correlation of the crowded basket | `S:C D:A P:N` | `D:P P:U` (crowded-basket formation, P5) | `D:T P:U` (P4/P9) |
| **MS-R10e** | Reversal trigger: vol shock | state | realized-vol jump of the factor return | `S:C D:A P:N` | `D:P P:U` (P5) | `D:T P:U` (P4/P9) |
| **MS-R11a-US** | Short interest / float: US | cond | = `US-S9`: **cross-ref `MS-C1`** | `S:C D:B P:P` | `D:B P:P` (FINRA) | n/a |
| **MS-R11a-CN** | Margin-short balance / float: CN | cond | 融券余额/float: **NOT economically identical to US short interest** (融券 is legal-but-scarce inventory, not a broad short market); feeds the same `SQUEEZE` state via a separately standardized market adapter | `S:C D:T P:U` | n/a | `D:T P:U` |
| **MS-R11b** | Days-to-cover | cond | short interest ÷ ADV shares | `S:C D:B P:P` | `D:B P:P` | `D:T P:U` |

**Book momentum/theme risk contribution → PortfolioRisk, and it EXTENDS `PR-D4`, does not equal it.** v2.6 wrongly called this an "identity of object." `PR-D4` reports systematic-ENB / residual-share / residual-HHI; it does **not** report momentum-factor risk contribution, theme contribution, or sleeve-exposure cosine. Those must be **added to PortfolioRisk** (derived from its frozen factor model), not assumed present. Filed as a PortfolioRisk gap, not an MS-R card.

### 9b.2 Formulas & the two non-negotiable A-share constraints

**CoMomentum (Lou–Polk).** 12-1 winner/loser deciles; per-stock 52-week factor-residual weekly returns; leg score = mean pairwise correlation with the leave-one-out leg residual. High = common trading pressure, not shared fundamentals → predicts lower forward momentum returns, higher vol, more negative skew. **Legs kept separate.** *Open (why `S:C`, not `S:F`): monthly formation cadence, minimum valid weeks, decile exclusions, weighting, and the A-share factor set are all unspecified.*
- **Residual set is FORCED, not chosen, for A-shares:** US = FF3 residuals; **A-share = market+size+industry, HML dropped**: the §2.4 F1-EP result proved A-share accounting is `P:F` (Tushare overwrites in place). Narrow claim: an HML-residual CoMomentum is **not backtestable from the current normalized data stack without reconstructing historical filings from source PDFs**: not "impossible forever," but out of reach absent that separate NLP build. This is a hard constraint on the *current* stack, not a stylistic choice.

**Forced-flow US (`MS-R6a`).** `RebalanceTrade_{j,t} ≈ L_j(L_j−1)A_{j,t−1}r_t + L_j Flow_{j,t}`. **Timing caveat:** it uses same-day return and closing-auction volume, so realized pressure is *diagnostic* unless computed from intraday estimates. CTA (`R6b-US`/`R6b-CN`) and vol-target (`R6c`) are **separate IDs**. Do not fuse.

**A-share is vulnerability, not forced flow (`MS-R7`).** 两融 balance and 质押 ratio measure *leverage present*, not *leverage being liquidated*. A pledge is not forced supply until collateral thresholds, lender action and sale restrictions are known. `R7a/R7b` feed a `LeveragedVulnerability_CN` state; the true `ForcedFlow_CN` (`R7c`) needs **observable liquidation events** and is `S:O`.

**BadReactionBreadth (`MS-R9`).** `#{SUE>0 ∧ CAR<0}/#{SUE>0}`. Rising = positive fundamental news no longer attracts marginal buyers = positioning stress. **Not uniquely positioning**: a discount-rate move or simultaneous guidance can also drive it, so it is a `cond`, controlled for market/sector. `S:R` because it inherits `F5-SUE` (`S:R`) and `F5-CAR`. **PIT is market-specific, not uniformly `P:F`: US `P:P`** (EDGAR filings + price-based CAR can in principle be reconstructed historically, even if a validated panel isn't built yet); **CN `P:F`** (needs the announcement-window CAR archived forward, per the general A-share fundamental constraint).

### 9b.3 Percentile-reproducibility rule (family-wide)

Declare five things or the percentile is meaningless: **raw numerator · denominator · investor universe · frequency · history window.** Strict PIT empirical percentile `Pct_t(x)=(1/N)Σ_{s=t−N}^{t−1}1(x_s≤x_t)`. Effective N over 5y: daily ≈1260, weekly ≈260, monthly ≈60 (noisy), **quarterly ≈20, too coarse for a "98th-percentile" claim.** **Never forward-fill quarterly holdings into a "daily" percentile.** Always report raw value, percentile, and recent change together.

### 9b.4 Tiered response: NOT a Boolean AND (v2.7 correction)

v2.6 proposed `crowding AND leverage AND weak-liquidity AND reversal` as the trigger. **A strict AND activates late** (only after the reversal is already visible) **or fails when one slow/licensed input is missing.** Replace with a graded response by signal speed:

| Signal class | Cards | Response |
|---|---|---|
| **Slow structural vulnerability** | R2, R3, R4, R7a/b | **gradual** risk-budget cap / uncertainty buffer: always on, updates slowly |
| **Fast forced-flow / reversal trigger** | R6, R7c, R10 | **accelerated** de-risking on trigger |
| **Liquidity failure** | R8 | **emergency** execution restriction (widen, halt adds) |
| **Missing crowding data** | any unavailable | treat as **"unknown," never "safe"**. Do not relax caps on absent data |

The structural legs raise the *prior*; the fast legs supply the *timing*; liquidity governs *execution*. The old conjunction survives only as the *worst-case* label (all four lit at once), not as the activation condition.

### 9b.5 Consumers: PENDING, not wired

**⚠ These three summary states are PROPOSED, not consumed.** As of v2.7, Combination's registry consumes only the legacy `MS-R1`; PortfolioRisk references only `MS-R1`. Wiring `StructuralVulnerability` ← {R2,R3,R4,R7a/b} · `ForcedFlowPressure` ← {R6,R7c,R10} · `LiquidityAbsorption` ← {R8} into the Combination input registry and PortfolioRisk is an **open cross-document task**, tracked in the MarketStructure and Combination contracts. Until then MS-R is a reference-layer outline that does not size anything.

**Do NOT promote to primary indicators** (research-prose only): July momentum seasonality; the "−20%→+6%" statistic (tiny event sample); anecdotes (Samsung); exact bank CTA-flow numbers (proprietary).

---

## 9c. Sentiment cross-cutting transforms & narrative outline (v3.0)

**Status: same as §9b, registered outline, most rows `S:C`/`S:O`, not implementation-ready.** This section absorbs a broad sentiment-architecture proposal. Most of the underlying mechanisms are already registered elsewhere (breadth `CN-B1`, limit heat `CN-B3`, margin/pledge `CN-N2/N5`, options `CN-B7`, IPO exuberance `CN-CM-*`/`US-CM*`/`US-BW*`, crowding `MS-R2-11`, price-reaction `MS-R9`/`F5-CAR`, surveys `US-S1-3`, fund flows `CN-F2-5`), §9c adds only what was genuinely missing: a sector-sentiment aggregation method, `CN-RET1` (above, §12b.5), and a narrative/LLM family. **It does not introduce a fourth sentiment composite**: `MS-R`'s three summary states already carry the "positioning fragility" role, and the separately-maintained `AShare_Fear_Greed_Index` project (`Quant/Projects/`) already carries a tested 6-leg timing composite. Cross-reference both; do not build a third.

**⚠ On the existing Fear/Greed project, corrected framing.** It is not a "validated sentiment composite." Its own README states the 25/75 timing rule **ties** a drawdown-matched lower-risk benchmark on the strict 6-leg series, an implemented development benchmark whose incremental timing edge over "hold less" **did not survive** honest execution and de-lever accounting. Its six legs (leverage temp/flow, turnover heat, valuation percentile, price strength, momentum) **do overlap this framework materially**: turnover→fast demand, margin→demand+fragility, momentum/price-strength→trend, valuation→slow exuberance. Rule: **register its six components as atomic indicators if/when they get their own IDs; register the composite itself as a benchmark/dashboard object; never consume both the composite and its components in the same allocation decision** (that would double-count the same information).

### 9c.1 Sector-relative sentiment, sparse-count specification

A continuous-signal sector transform (`z(sector) − β·z(market)`) is fine for turnover, text tone, or any smooth series. **It is the wrong tool for sparse limit-event counts and small sectors**: a sector with 8 constituents and 1 limit-up does not have a meaningful z-score.

**For limit-event counts, use a board-adjusted expected-count statistic:**
```
Z_limit_{s,t} = (U_{s,t} − Σ_b N_{s,b,t}·p_{b,t}) / sqrt(Σ_b N_{s,b,t}·p_{b,t}·(1−p_{b,t}))
```
where `b` indexes board/limit-rule regime (Main/ChiNext/STAR/BSE, each with its own hit-probability `p_{b,t}`), `N_{s,b,t}` = eligible count of sector `s` on board `b`, `U_{s,t}` = observed limit-up count. **Then shrink small sectors toward the market mean** via a beta-binomial or hierarchical prior, a raw z-score on an 8-name sector is noise, not signal.

**Continuous series** (turnover, text tone, options skew) keep the simpler `z(sector) − β·z(market)` transform.
**⚠ Inherits `P9` (PIT sector membership, unresolved).** No sector-sentiment read is causal until historical sector membership is point-in-time, the same constraint that already blocks `CN-T3`/`CN-X4`/`MS-R3b/c`.

### 9c.2 Narrative / LLM sentiment, atomic outline (not seven implementable cards)

**⚠ v2.9's `SENT-LLM1-7` was a labelling error, a research list presented as cards.** Every LLM-derived output needs its own: corpus + provider, publication timestamp, deduplication rule, entity/sector mapping, frozen prompt + model version, formula, horizon/target, missingness rule, data license, and named consumer. None of that is specified below, this is the **honest outline**, `S:O` throughout, not a card set.

| Proposed ID | Construct | Overlaps existing | Data source (unverified) |
|---|---|---|---|
| `SENT-N1` | Narrative concentration (share of discussion on one theme) | extends `MS-R3` (theme concentration): **measurement upgrade, not a duplicate factor** | text corpus, TBD |
| `SENT-N2` | Semantic crowding (cross-security narrative similarity) | new: no existing register object | text corpus, TBD |
| `SENT-N3` | Retail-FOMO intensity (urgency/chasing language) | new; complements `CN-RET1`/`CN-B3` | forum/social text |
| `SENT-N4` | Bull–bear narrative disagreement, credibility-weighted | new | text corpus + source-quality labels |
| `SENT-N5` | Evidence-to-claim gap (sentiment strength vs new factual content) | new | text corpus |
| `SENT-N6` | Fundamental/price-reaction mismatch | **= `MS-R9` BadReactionBreadth. Do not duplicate; this is a text-sentiment robustness check on the same construct, not a new ID** | n/a |
| `SENT-N7` | Policy-narrative state (confirmed policy vs speculative expectation, propagation speed) | extends `MS-C4a` (news, licensed) | text corpus + official release calendar |

**China-native text sources to evaluate (not yet verified feasible):** Tushare exposes exchange investor Q&A (互动易) under **separate authorization**: access status unconfirmed on this account. THS/东方财富 app hot-rankings and vendor theme/concept data (`kpl_concept`, seen unreachable in the same entitlement check as `limit_list_d` above) are candidate attention proxies; entitlement and commercial-use restrictions must be recorded before any card is written, not assumed.

**Hard rule (inherits §9b):** every `SENT-N*` output, if and when specified, is `state`/`cond`/`diag` only: **never a signed alpha**, and never consumed until a full field contract exists.

---

## 10. Index timing: US

**⚠ SCHEMA DEFICIT, the parent tables carry 7 of the 14 mandatory fields.** §10/§11 give ID, name, transform, `Dir`, lag, RG, readiness and grade, but **not** exact lookback, minimum history, missingness rule, standardization population, units or clock. Phrases like "percentile vs 5y", "rolling z", "surprise" and "composite" are therefore **under-specified**: the lookback, the vintage, the population the z is computed against and the minimum sample all change the number. **For these 181 rows the register does NOT yet meet its own mission**; you will still need the parent contract. Closing this is the largest remaining paper task. The standing defaults below reduce but do not eliminate it.

**Standing defaults for §10/§11 (apply unless a row overrides):** `CLK` = `CLK-CLOSE` for close-derived series, `CLK-PREOPEN` for overnight/overseas, `CLK-INTRADAY` for continuously-quoted states · **rolling z / percentile** = trailing **5 years** of the indicator's **own history**, minimum **3 years**, else `NA` · **`Δ`** = simple difference over the stated window · **surprise** = actual − frozen consensus **as of the release timestamp** · **missing** = `NA`, never 0 and never carried forward beyond one period · **units** = the source series' native units.

**Convention:** `.n` suffix = one atomic output split from a parent family row. Full hypothesis, failure regime and grade rationale live in `Indicators_Pool_US_v2.md` §2–3.
**PIT tiering (v2.1 correction):** `P:N` is reserved for **market-observable, non-revised** series (prices, yields, spreads, index levels, volumes, option-implied). **Statistical-agency output is revision-prone**: re-seasonalized, redefined, benchmarked, so a current FRED history is *not* the value released at the historical decision date. Those rows are `P:U` and require **ALFRED vintages** (P15). Nowcasts are `P:F`.
**All rows `Out: state`, `TR-STATE`** unless noted. Dep `P15` for every `P:U` row.

| ID | Name | Formula / transform | Dir | Lag | RG | Own | E |
|---|---|---|---|---|---|---|---|
| US-M0.1 | Cash return | 3m T-bill yield/return | `state` | same day | RATES | `S:F D:A P:N` | B |
| US-M0.2 | Ex-ante real cash | T-bill − expected inflation | `state` | same day | RATES | `S:C D:P P:U` (source unpinned) | B |
| US-M1.1 | Curve slope level | FRED `T10Y3M` level | `state` | same day | RATES | `S:F D:A P:N` | B |
| US-M1.2 | Curve slope 63d Δ | `T10Y3M_t − T10Y3M_{t−63}` | `state` | same day | RATES | `S:F D:A P:N` | B |
| US-M2.1 | IG OAS level z | `BAMLC0A0CM` → rolling z | `−` | 1 day | CREDIT | `S:F D:A P:N` | B |
| US-M2.2 | IG OAS 21d Δ | 21d change | `−` | 1 day | CREDIT | `S:F D:A P:N` | B |
| US-M2.3 | HY OAS level z | `BAMLH0A0HYM2` → rolling z | `−` | 1 day | CREDIT | `S:F D:A P:N` | B |
| US-M2.4 | HY OAS 21d Δ | 21d change (**change > level**) | `−` | 1 day | CREDIT | `S:F D:A P:N` | B |
| US-M3 | Fed path repricing | FF futures → 21d Δ in expected rate 12m ahead | `state` | same day | RATES | `S:F D:P P:N` | B |
| US-M4.1 | NFCI level | Chicago Fed NFCI | `−` | ~1 wk | CREDIT/FUNDING | `S:F D:A P:U` | B |
| US-M4.2 | NFCI 13w Δ | 13-week change | `−` | ~1 wk | CREDIT/FUNDING | `S:F D:A P:U` | B |
| US-M5.1 | ISM new orders 3m Δ | ISM mfg new-orders sub-index, 3m change | `+` | 1st biz day | GROWTH | `S:F D:A P:U` | B |
| US-M5.2 | ISM surprise | actual − frozen consensus | `+` | 1st biz day | GROWTH | `S:F D:L P:U` | B |
| US-M5.3 | Initial claims 4w MA z | 4-week MA, z | `−` | weekly Thu | GROWTH | `S:F D:A P:U` | B |
| US-M5.4 | GDPNow 3m Δ | Atlanta Fed GDPNow, 3m change | `+` | continuous | GROWTH | `S:F D:B P:U` (**vintage archive exists back to 2011Q3: ingest, then verify**) | B |
| US-M6.1 | CPI surprise | actual − frozen consensus (**realized data only**) | `−` | ~2 wks | INFL | `S:F D:L P:U` | B |
| US-M6.2 | PCE surprise | actual − frozen consensus | `−` | ~1 mo | INFL | `S:F D:L P:U` | B |
| US-M7 | USD / dollar liquidity | DXY 63d Δ | `−` | same day | USD | `S:F D:A P:N` | B |
| US-M8.1 | Real-yield component | Δ10y real (TIPS) | `−` | same day | INFL | `S:F D:A P:N` | B |
| US-M8.2 | Breakeven component | Δ10y breakeven | `state` (regime-dependent sign) | same day | INFL | `S:F D:A P:N` | B |
| US-V1 | CAPE percentile | Shiller CAPE → percentile vs trailing 30y | `−` | monthly | VALUE | `S:F D:A P:U` | B |
| US-V2 | ERP **proxy** | Forward E/P − 10y TIPS | `+` | daily | VALUE | `S:F D:L P:N` | B |
| US-V3.1 | Agg. revision breadth | index EPS revision breadth → 4w MA, z | `+` | ~weekly | EARN | `S:F D:L P:U` | B |
| US-V3.2 | Agg. revision magnitude | index EPS revision magnitude → 4w MA, z | `+` | ~weekly | EARN | `S:F D:L P:U` | B |
| US-V3.3 | Analyst dispersion | cross-analyst dispersion → z | `−` | ~weekly | EARN | `S:F D:L P:U` | B |
| US-V4.1 | Market net payout yield | `(div + executed repurchases − issuance)/mcap` | `+` | quarterly ~45d | CAPALLOC | `S:F D:B P:P` | B |
| US-V4.2 | Δ diluted shares (agg) | aggregate change in diluted share count | `−` | quarterly ~45d | CAPALLOC | `S:F D:B P:P` | B |
| US-V5 | Agg. quality breadth | % of firms improving ROE/margins/cash conversion (**breadth, not cap-weighted level**) | `+` | quarterly ~45d | EARN | `S:F D:B P:P` | C |
| US-T1.1 | TSMOM 12-1m | index excess return `m0−11…m0−1` → sign/z | `+` | none | TREND | `S:F D:A P:N` | A (multi-asset) |
| US-T1.2 | TSMOM 6m | 6-month excess return → sign/z | `+` | none | TREND | `S:F D:A P:N` | A |
| US-T1.3 | TSMOM 3m | 3-month excess return → sign/z | `+` | none | TREND | `S:F D:A P:N` | A |
| US-T2.1 | Price vs 50d MA | `P/MA50 − 1` | `+` | none | TREND | `S:F D:A P:N` | B |
| US-T2.2 | Price vs 200d MA | `P/MA200 − 1` | `+` | none | TREND | `S:F D:A P:N` | B |
| US-T2.3 | MA crossover event | 50d crosses 200d → event flag | `bin` | none | TREND | `S:C D:A P:N` (event window undeclared) | B |
| US-T3 | Sector momentum | 6-1m sector RS rank | `+` | none | TREND | `S:F D:A P:N` | A (x-sec) |
| US-T4.1 | Index short reversal | 1–5d index return z | `−` | none | REV | `S:C D:A P:N` (**horizon unpinned**) | C |
| US-T4.2 | RSI | RSI(n) | `−` | none | REV | `S:C D:A P:N` (**n unpinned; anti-zoo: pick ONE**) | C |
| US-T5 | 52-week-high proximity | `P / 252d max` | `+` | none | TREND | `S:F D:A P:N` | B |
| US-B1.1 | Breadth level | % constituents > 200d MA | `+` | none | BREADTH | `S:F D:P P:U` (P5) | B |
| US-B1.2 | Breadth divergence | 63d breadth change − 63d index change | `+` | none | BREADTH | `S:F D:P P:U` (P5) | B |
| US-B2 | Net new 52w highs | `NH − NL` → 21d MA | `+` | none | BREADTH | `S:F D:A P:N` | B |
| US-S1.1 | AAII bull-bear | spread → percentile vs 5y | `−` (contrarian) | weekly Thu | SENT | `S:F D:A P:N` | B |
| US-S1.2 | II bull-bear | spread → percentile vs 5y | `−` | weekly | SENT | `S:F D:L P:U` (Investors Intelligence: **licensed, not public-partial**) | B |
| US-S2 | Equity put/call | aggregate Cboe ratio → 5d MA percentile | `+` (contrarian) | after close → next session | SENT | `S:F D:P P:U` (**history discontinuous; full detail via DataShop**) | C |
| US-S3 | NAAIM exposure | level percentile | `−` | weekly Thu | POSITION | `S:F D:A P:N` | C |
| US-S4 | Net margin leverage | `ML_net = (Debit − FreeCredit_cash − FreeCredit_margin)/mcap` | `−` | **~3 wks** | LEV | `S:F D:A P:U` | B |
| US-S5.1 | COT E-mini net spec | net spec positioning percentile | `−` | Fri release of Tue | POSITION | `S:F D:A P:N` | C |
| US-S5.2 | COT VIX futures net spec | net spec positioning percentile | `−` | Fri release of Tue | POSITION | `S:F D:A P:N` | C |
| US-S6 | Fund flows | 4w equity flow z | `−` | weekly ~1wk | FLOW | `S:F D:L P:U` (**EPFR licensed**; ICI aggregate is `D:B`) | C |
| US-S7 | Insider net buying | agg net buy ratio → 21d (Form 4) | **`+` (NOT contrarian)** | 2 biz days | INFORMED-POS | `S:F D:B P:V` | B |
| US-S8.1 | Yale 1-year confidence | percentile | `−` | monthly | SENT | `S:F D:L P:U` | C |
| US-S8.2 | Yale buy-on-dip | percentile | `−` | monthly | SENT | `S:F D:L P:U` | C |
| US-S8.3 | Yale crash confidence | percentile | `+` | monthly | SENT | `S:F D:L P:U` | C |
| US-S8.4 | Yale valuation confidence | percentile | `−` | monthly | SENT | `S:F D:L P:U` | C |
| US-S9 | Aggregate short interest | short interest / float → detrended z | **`−` on raw SI** | twice monthly | INFORMED-POS | `S:F D:A P:N` | C |
| US-S10a | Daily news pessimism | timestamped daily news z | `−` | daily | NEWS | `S:F D:L P:N` | C |
| US-S10b | News → reversion | SF Fed news 4w-change z | `+` | weekly | NEWS | `S:F D:B P:U` | C |
| US-CM1.1 | IPO count | trailing-K-month count (**K predeclared 3/6/12**) → z | `−` | per-event pricing date | ISSUANCE-HEAT | `S:C D:B P:U` | C |
| US-CM1.2 | IPO proceeds / mcap | trailing-K-month proceeds / total mcap → z | `−` | per-event | ISSUANCE-HEAT | `S:C D:B P:U` | C |
| US-CM2.1 | IPO first-day return | market-adjusted first-day return | `−` | per-event | ISSUANCE-HEAT | `S:F D:B P:U` | C |
| US-CM2.2 | IPO price revision | offer vs filing-range midpoint: **parse ranges, link amendments, timestamp** | `−` | per-event | ISSUANCE-HEAT | `S:F D:B P:U` | C |
| US-CM3 | Equity share of issuance | equity / (equity + LT-debt) issuance → z | `−` | aggregate flow | ISSUANCE-HEAT | `S:F D:B P:U` | C |
| US-CM4 | SEO issuance | SEO proceeds / mcap | `−` | quarterly | ISSUANCE-HEAT | `S:F D:B P:U` | C |
| US-CM5.1 | SPAC issuance | issuance volume | `−` | monthly | ISSUANCE-HEAT | `S:C D:P P:U` | C |
| US-CM5.2 | SPAC redemptions | redemption rate | `+` | monthly | ISSUANCE-HEAT | `S:C D:P P:U` | C |
| US-CM5.3 | De-SPAC activity | completed de-SPAC count | `−` | monthly | ISSUANCE-HEAT | `S:C D:P P:U` | C |
| US-X1 | HY vs Treasury | HYG/IEF 21–63d relative return | `+` | none | CREDIT | `S:F D:A P:N` | B |
| US-X2.1 | Copper/gold ratio | 63d Δ z | `+` | none | XGROWTH | `S:F D:A P:N` | C |
| US-X2.2 | Broad commodity (BCOM) | 63d Δ z | `state` | none | XGROWTH | `S:F D:A P:N` | C |
| US-X2.3 | **Oil** | 63d Δ z: **demand vs supply attribution required** | `state` | none | XGROWTH | `S:C D:A P:N` | C |
| US-X3 | Defensive leadership | XLU/XLP vs SPY, 21–63d RS | `−` | none | XGROWTH | `S:F D:A P:N` | C |
| US-X4.1 | Gold bid | 21d z | `−` | none | HAVEN | `S:F D:A P:N` | C |
| US-X4.2 | Long-bond bid | 21d z | `−` | none | HAVEN | `S:F D:A P:N` | C |
| US-VRP1 | Variance risk premium | `IV²^Q_{t,H} − E^P_t[RV_{t,t+H}]`: **both terms same horizon H and measure** | `+` | same day | VAR-RISK | `S:C D:L P:N` | B (research) |
| US-VRP2 | VIX-extreme contrarian | VIX percentile vs 5y, **extremes only** | `+` | same day | VAR-RISK | `S:F D:A P:N` | B (research) |
| US-R1 | Realized vol ratio | 21d RV / 252d RV | `−` | none | VOL | `S:F D:A P:N` | A (persistence) |
| US-R2a | VIX level | percentile vs 5y | `−` | same day | VOL | `S:F D:A P:N` | A |
| US-R3.1 | VIX term structure | VIX / VIX3M | `−` | same day | VOL | `S:F D:A P:N` | B |
| US-R3.2 | VX futures slope | front-month VX slope | `−` | same day | VOL | `S:F D:P P:N` | B |
| US-R4.1 | GARCH vol forecast | daily RV → GARCH forecast | `−` | none | VOL | `S:C D:A P:N` (**spec unpinned**) | A |
| US-R4.2 | HAR vol forecast | daily RV → HAR forecast | `−` | none | VOL | `S:C D:A P:N` (**spec unpinned**) | A |
| US-R5.1 | Implied correlation | CBOE COR index | `−` | same day | CORR | `S:F D:L P:N` | B |
| US-R5.2 | Realized avg pairwise corr | 63d rolling average pairwise | `−` | close → t+1 | CORR | `S:F D:P P:U` (P5) | B |
| US-R6a.1 | SOFR-OIS spread | spread level | `−` | 1 day | FUNDING | `S:F D:A P:N` | B |
| US-R6a.2 | GC repo − IORB | spread level | `−` | 1 day | FUNDING | `S:F D:A P:N` | B |
| US-R6b.1 | Amihud illiquidity (SPY) | Amihud measure | `−` | close → t+1 | LIQ | `S:F D:A P:N` | B |
| US-R6b.2 | Quoted spread (SPY) | **true quoted spread needs TAQ/SIP quote history**: daily OHLCV cannot reconstruct it | `−` | close → t+1 | LIQ | `S:F D:L P:N` | B |
| US-R7 | Drawdown state | current DD from 252d high | `state` | none | VOL | `S:F D:A P:N` | descriptive |
| US-R8 | Bond–equity correlation | 63d rolling stock–bond corr | `state` (positive corr → cut gross) | close → t+1 | CORR | `S:F D:A P:N` | B |
| US-R10 | **RTI** | → §12 | n/a | weekly | RISK-APPETITE-XA | `S:F D:A P:N` (→§12) | C |

**`US-R2b` and `US-R9` carry no rows.** `US-R2b` was **relocated to `US-VRP2`** (v2.6); `US-R9` is an **explicitly retired reserved identifier** (its VRP return-predictor role moved to `US-VRP1`). v2.0 carried both as empty placeholders, removed. Do not reintroduce them.

**Sign traps in this table.** `US-S7` (insider buying) is **`+`**: insiders are informed buyers. **`US-S9` is `−` on RAW short interest** (v2.2 had this backwards): shorts being *informed* means high short interest predicts **lower** subsequent returns. "Informed-positioning" is the RG, not the direction, if you want a `+`-oriented score, define an explicit negated "informed-bearishness" variable rather than flipping `Dir` on the raw series. `US-S8.3` (crash confidence) inverts relative to the other three Yale series. `US-M8.2` (breakeven) has a **regime-dependent sign** (good vs bad inflation). Do not hard-code it. `US-T4.2` RSI must pick **one** horizon: the anti-zoo rule forbids a parameter sweep.

---

## 11. Index timing: A-share

Same conventions as §10. Dep `P15-CN` for every `P:U`/`P:F` row: **and note P15-CN is `D:U`**. there is **no vendor vintage archive for Chinese macro**, so revision-prone series are **`P:F` (forward-snapshot only)** unless you already hold history.

| ID | Name | Formula / transform | Dir | Lag | RG | Own | E |
|---|---|---|---|---|---|---|---|
| CN-M0 | Cash & policy return | money-market fund / GC001 repo / short NCD | `state` | daily | POLICY | `S:C D:T P:N` (**proxy unpinned**) | B |
| CN-M1a | Credit acceleration | 3m Δ of TSF-stock YoY | `+` | ~10–15th next mo | CREDIT-CN | `S:F D:T P:U` | B |
| CN-M1b | Credit impulse | Δ of (12m rolling new TSF flow / nominal GDP) | `+` | ~10–15th next mo | CREDIT-CN | `S:F D:T P:U` | B |
| CN-M2.1 | RRR change | **easing-signed** event: `−Δrate` (RRR: `−ΔRRR`) | `+` | same day | POLICY | `S:F D:T P:N` | C |
| CN-M2.2 | MLF rate change | **easing-signed** event: `−Δrate` (RRR: `−ΔRRR`) | `+` | same day | POLICY | `S:F D:T P:N` | C |
| CN-M2.3 | LPR change | **easing-signed** event: `−Δrate` (RRR: `−ΔRRR`) | `+` | same day | POLICY | `S:F D:T P:N` | C |
| CN-M2.4 | 7d OMO rate change | **easing-signed** event: `−Δrate` (RRR: `−ΔRRR`) | `+` | same day | POLICY | `S:F D:T P:N` | C |
| CN-M2.5 | Composite stance index | weighted combination of.1–.4, **all pre-signed as easing** | `+` | same day | POLICY | **`S:C D:T P:N`** (**weights undeclared: four heterogeneous instruments**) | C |
| CN-M3 | M1 momentum | M1 YoY → 3m Δ | `+` | ~10–15th next mo | CREDIT-CN | `S:C D:T P:U` (**definition break: regime-date it**) | B |
| CN-M4.1 | NBS PMI new orders | sub-index level | `+` | last day of ref. month | GROWTH-CN | `S:F D:T P:U` | B |
| CN-M4.2 | NBS PMI 3m Δ | 3-month change | `+` | last day | GROWTH-CN | `S:F D:T P:U` | B |
| CN-M4.3 | Caixin PMI | level (**different sample: not a robustness variant of NBS**) | `+` | ~1st biz day | GROWTH-CN | `S:F D:T P:U` | B |
| CN-M4.4 | PMI surprise | actual − frozen consensus | `+` | per release | GROWTH-CN | `S:F D:L P:U` | B |
| CN-M5a | CPI surprise | actual − **frozen** consensus, standardized | `−` | ~9–10th next mo | INFL-CN | `S:F D:L P:U` | B |
| CN-M5b | PPI surprise | actual − **frozen** consensus, standardized | `+` | ~9–10th next mo | INFL-CN | `S:F D:L P:U` | B |
| CN-M5c | PPI−CPI margin gap | `PPI YoY − CPI YoY` | `+` | ~9–10th next mo | INFL-CN | `S:F D:T P:U` | C |
| CN-M6.1 | 商品房销售面积 YoY | YoY growth | `+` | monthly ~15th | PROPERTY | `S:F D:T P:U` | B |
| CN-M6.2 | 70-city price diffusion | % cities with rising prices | `+` | monthly ~15th | PROPERTY | `S:F D:T P:U` | B |
| CN-M6.3 | Property composite z | weighted z of.1 +.2 | `+` | monthly | PROPERTY | **`S:C D:T P:U`** (weights) | B |
| CN-M7.1 | USDCNY vs fixing gap | spot − fixing → 21d z | `−` | daily | FX | `S:F D:T P:N` | B |
| CN-M7.2 | CNH−CNY spread | offshore − onshore → 21d z | `−` | daily | FX | `S:F D:T P:N` | B |
| CN-M8.1 | CGB slope level | 10y − 1y | `state` | daily | POLICY | `S:F D:T P:N` | C |
| CN-M8.2 | CGB slope 63d Δ | 63-day change | `state` | daily | POLICY | `S:F D:T P:N` | C |
| CN-M9 | Fiscal impulse | **modelled**: Δ cyclically-adjusted primary balance | `+` | monthly, MoF lag | FISCAL-CN | **`S:O D:P P:U`** (construction unspecified) | C |
| CN-V1.1 | CSI300 PE-TTM percentile | percentile vs trailing 10y | `−` | daily | VALUE | `S:F D:T P:N` | B |
| CN-V1.2 | CSI300 PB percentile | percentile vs trailing 10y | `−` | daily | VALUE | `S:F D:T P:N` | B |
| CN-V1.3 | CSI500 PE-TTM percentile | percentile vs trailing 10y | `−` | daily | VALUE | `S:F D:T P:N` | B |
| CN-V2 | E/P − CGB 10y (ERP **proxy**) | `CSI300 E/P − CGB10y` → percentile | `+` | daily | VALUE | `S:F D:T P:N` | B |
| CN-V3 | Dividend-yield spread | CSI Dividend yield − CGB 10y | `+` | daily | VALUE | `S:F D:T P:N` | C |
| CN-V4 | Industrial profits | 规模以上工业企业利润 YoY | `+` | monthly ~27th | GROWTH-CN | `S:F D:T P:U` | C |
| CN-V5.1 | Agg. revision breadth | covered-universe EPS revision breadth | `+` | ~weekly | EARN-CN | `S:F D:L P:U` | C |
| CN-V5.2 | Agg. revision magnitude | covered-universe magnitude | `+` | ~weekly | EARN-CN | `S:F D:L P:U` | C |
| CN-V5.3 | Analyst dispersion | cross-analyst dispersion | `−` | ~weekly | EARN-CN | `S:F D:L P:U` | C |
| CN-V6 | Agg. quality breadth | % firms improving 扣非-ROE / margins / cash conversion | `+` | report-cluster lag | EARN-CN | `S:F D:T P:U` | C |
| CN-V7.1 | Market net payout | cash div + executed buybacks − placements/rights | `+` | filing lag | CAPALLOC | `S:F D:T P:U` | C |
| CN-V7.2 | Δ total shares (agg) | aggregate share-count change | `−` | filing lag | CAPALLOC | `S:F D:T P:U` | C |
| CN-T1.1 | TSMOM 12-1m | index excess return `m0−11…m0−1` → z | `+` | none | TREND | `S:F D:T P:N` | B |
| CN-T1.2 | TSMOM 6m | 6-month excess return → z | `+` | none | TREND | `S:F D:T P:N` | B |
| CN-T1.3 | TSMOM 3m | 3-month excess return → z | `+` | none | TREND | `S:F D:T P:N` | B |
| CN-T2.1 | Price vs 20d MA | `P/MA20 − 1` | `+` | none | TREND | `S:F D:T P:N` | B/C |
| CN-T2.2 | Price vs 60d MA | `P/MA60 − 1` | `+` | none | TREND | `S:F D:T P:N` | B/C |
| CN-T2.3 | Price vs 250d MA | `P/MA250 − 1` | `+` | none | TREND | `S:F D:T P:N` | B/C |
| CN-T3 | Sector momentum | 6-1m 申万一级 RS rank | `+` | none | TREND | `S:F D:P P:U` (P9) | B |
| CN-T4 | Index short reversal | 1–5d index return z | `−` | none | REV | `S:C D:T P:N` (**horizon unpinned**) | C |
| CN-T5 | 52-week-high proximity | `P / 252d max` | `+` | none | TREND | `S:F D:T P:N` | C |
| CN-B1.1 | Breadth level | % stocks > 250d MA | `+` | none | BREADTH | `S:F D:T P:N` | B |
| CN-B1.2 | Advance/decline | adv/decl ratio | `+` | none | BREADTH | `S:F D:T P:N` | B |
| CN-B1.3 | Breadth divergence | breadth change vs index change | `+` | none | BREADTH | `S:F D:T P:N` | B |
| CN-B2 | Normalized turnover | 全市场成交额 / free-float mcap → **rolling 3y percentile** | `−` | daily close | SPEC-HEAT | `S:F D:T P:N` | B |
| CN-B3.1 | 涨停家数 | limit-up count: **all-boards-pooled is now EMPIRICALLY confirmed invalid, v3.4**: 2026-08-10 touch-up rate was Main 3.47%, ChiNext 0.43%, STAR 0.65%, BSE 0%: an 8x spread. Superseded by board-conditioned `.5` | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**downgraded. See.5/.6 for the board-conditioned replacement**) | C |
| CN-B3.2 | 连板高度 | consecutive-limit height | `state` | daily | SPEC-HEAT | `S:F D:T P:N` | C |
| CN-B3.3 | 炸板率 (**RETIRED v3.2**) | identical construct to `CN-B3.7`: kept as a legacy cross-reference for `CN-B3.4`'s composite weights only; not a separate atomic output | `state` | daily | SPEC-HEAT | `S:F D:T P:N` (**alias of `CN-B3.7`, same triple**) | C |
| CN-B3.4 | Limit composite z | weighted z of **sign-aligned**.1–.3 (**board- & date-aware limit rules**) | `state` | daily | SPEC-HEAT | **`S:C D:T P:N`** (weights and alignment) | C |
| CN-B3.5 | Touch-limit-up share | `Σ 1(High_i = UpLimit_i) / N^{eligible}_t`: **board-conditioned**, do NOT pool 10/20/30% boards | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**numerator verified live; `N^eligible`: ex-ST, ex-suspended, listed ≥6m per P4: is undefined, so the SHARE is not frozen even though the raw count is**) | n/a |
| CN-B3.6 | Close-limit-up share | `Σ 1(Close_i = UpLimit_i) / N^{eligible}_t`: board-conditioned | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**numerator verified live; `N^eligible` undefined: same gap as `.5`**) | n/a |
| CN-B3.7 | Failed-limit rate | `N(Touch=1,Close=0)/N(Touch=1)`: **exact complement of `CN-B3.8`**; report ONE, not both | `state` | daily | SPEC-HEAT | `S:F D:T P:N` | n/a |
| CN-B3.8 | Seal-success rate | `1 − CN-B3.7`: derived readout, not a second vote | `state` | daily | SPEC-HEAT | `S:F D:T P:N` | n/a |
| CN-B3.9 | Limit-up continuation rate | `Σ 1(CloseUp_{i,t}=1 and CloseUp_{i,t-1}=1) / Σ 1(CloseUp_{i,t-1}=1)`: 2-day chain of the `CN-B3.6` join, no new endpoint | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**arithmetic verified live; board aggregation + edge rules open, see prose**) | n/a |
| CN-B3.10 | Close-limit-down share | `Σ 1(Close_i = DownLimit_i)/N^{eligible}_t`: same `stk_limit`+`daily` join as `.5`/`.6`, down-limit side. **Renamed from earlier drafts' "locked-limit-down": measures closing at limit-down, NOT being locked there all day (see `.14`)** | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**numerator verified live, mechanically identical to `.5`/`.6`; `N^eligible` undefined: same gap**) | n/a |
| CN-B3.11 | Reopening count (aggregated) | **`open_num`, from `limit_list_ths`** (v3.2 correction: `kpl_list` has NO reopening-count field, only `open_time`, a timestamp; `limit_list_ths.open_num` is the actual field). Aggregation method (total openings / mean per touched name / reopening share) still open | `diag` | daily | SPEC-HEAT | `S:C D:L P:U` (**8,000-pt entitlement, above the register's 5,000-pt baseline; data starts 2023-11-01; personal-research-use restriction only: commercial use requires separate 同花顺 licensing**) | n/a |
| CN-B3.12 | Queue intensity | **`limit_order` (or `lu_limit_order` for the max variant) / `free_float`, from `kpl_list`** (v3.2 correction: `kpl_list` has no `fd_amount` field; that name was carried over incorrectly from a different endpoint). Closing-queue vs maximum-queue choice, and units, still open | `diag` | daily | SPEC-HEAT | `S:C D:L P:U` (same `kpl_list` entitlement gap as `.11`, though `kpl_list` itself is 5,000-pt per docs: confirmed access-denied on this account regardless) | n/a |
| CN-B3.13 | True seal-duration share | needs minute/tick interval states, NOT `first_time`/`last_time` alone (reopens can occur between them) | `diag` | intraday | SPEC-HEAT | `S:O D:L P:U` | n/a |
| CN-B3.14 | **Locked-limit-down share (all-day 一字跌停)** | `Σ 1(limit_status_i = 6) / N^{eligible}_t`, from `daily_basic.limit_status` (**field verified live, v3.2**: values 0-6, 5=ordinary limit-down, 6=locked/一字; must request `fields=` explicitly or the field is silently omitted) | `state` | daily | SPEC-HEAT | `S:C D:T P:N` (**source+numerator verified; one pooled scalar contradicts this family's own board-conditioning mandate: needs a Main/ChiNext/STAR/BSE split or a frozen aggregation before `S:F`, v3.3**) | n/a |
| CN-B4.1 | 融资余额 21d Δ z | margin-balance change | `−` | **T+1 morning** | LEV | `S:F D:T P:N` | B |
| CN-B4.2 | 融资余额 / float mcap | percentile | `−` | T+1 | LEV | `S:F D:T P:N` | B |
| CN-B5 | New investor accounts | 新增投资者数 (CSDC) → percentile | `−` | monthly ~2wk | SPEC-HEAT | `S:F D:P P:U` | C |
| CN-B6 | New fund issuance | **raised assets** (not launch count) → 3m sum percentile, per category | `−` | establishment announcement | FLOW | `S:F D:P P:U` | B |
| CN-B7.1 | SSE 50ETF put/call | volume & OI ratio (**per venue & underlying separate**) | `+` | after close → next session | SENT | `S:F D:P P:N` | C |
| CN-B7.2 | CSI300 option put/call | volume & OI ratio | `+` | after close | SENT | `S:F D:P P:N` | C |
| CN-B8 | Financing purchase intensity | 融资买入额 / turnover **of margin-eligible names on that date** | `−` | T+1 morning | LEV | `S:F D:T P:N` | C |
| CN-CM-S.1 | Completed IPO count | count | `−` | per-event | ISSUANCE-HEAT | `S:F D:T P:U` | C |
| CN-CM-S.2 | IPO proceeds / mcap | ratio | `−` | per-event | ISSUANCE-HEAT | `S:F D:T P:U` | C |
| CN-CM-S.3 | Listing speed | **inverse** filing→listing duration (`1/days`): a longer queue is NOT unconditionally positive receptivity; raw duration is a **policy/backlog state**, not a signal | `+` | per-event | ISSUANCE-HEAT | `S:C D:T P:U` | C |
| CN-CM-D.1 | Online oversubscription | ratio (**online & offline kept separate**) | `−` | per-event | ISSUANCE-HEAT | `S:F D:T P:U` | C |
| CN-CM-D.2 | Offline oversubscription | ratio | `−` | per-event | ISSUANCE-HEAT | `S:F D:T P:U` | C |
| CN-F1.1 | Index-futures basis | IF/IC/IH annualized basis vs fair value → percentile | `+` | intraday/close | POS | `S:F D:T P:N` | C |
| CN-F1.2 | Futures ΔOI | open-interest change | `state` | intraday/close | POS | `S:F D:T P:N` | C |
| CN-F2 | ETF share creation | broad-index Δshares × NAV | `+` | T+1 | FLOW | `S:F D:T P:N` | C |
| CN-F3 | Major-holder net 增持/减持 | announced net value → 21d sum z | `+` | announcement evening | FLOW | `S:F D:P P:U` | C |
| CN-F4 | Southbound flows 港股通 | daily net buy → 21d z | `+` | daily | FLOW | `S:F D:T P:N` | C |
| CN-F5 | Fund positioning 公募仓位测算 | vendor-estimated equity ratio → percentile | `−` | weekly, model-based | POS | `S:O D:L P:N` | C |
| CN-X1.1 | Copper 63d Δ z | SHFE/LME | `+` | none | XASSET | `S:F D:T P:N` | B |
| CN-X1.2 | Rebar 63d Δ z | n/a | `+` | none | XASSET | `S:F D:T P:N` | B |
| CN-X1.3 | Iron ore 63d Δ z | n/a | `+` | none | XASSET | `S:F D:T P:N` | B |
| CN-X1.4 | Supply/inflation leg | separate decomposition | `state` | none | XASSET | `S:C D:T P:N` | B |
| CN-X2.1 | Gold bid | 21d z | `−` | none | XASSET | `S:F D:T P:N` | C |
| CN-X2.2 | CGB duration bid | 21d z | `−` | none | XASSET | `S:F D:T P:N` | C |
| CN-X3 | HK/ADR overnight gap | HSCEI + ADR-implied A-share gap at open | `+` | pre-open | XASSET | `S:F D:T P:N` | C |
| CN-X4 | Defensive leadership | banks/utilities/dividend RS 21–63d vs CSI300 | `−` | none | XASSET | `S:F D:P P:U` (P9) | C |
| CN-R1 | Realized vol ratio | 21d RV / 252d RV | `−` | none | VOL | `S:F D:T P:N` | A (persistence) |
| CN-R2 | GARCH/HAR forecast | index daily RV → forecast | `−` | none | VOL | `S:C D:T P:N` (**model unpinned**) | A |
| CN-R3.1 | Cross-sectional dispersion | 63d rolling | `state` | none | CORR | `S:F D:T P:N` | B |
| CN-R3.2 | Avg pairwise correlation | 63d rolling | `−` | none | CORR | `S:F D:T P:N` | B |
| CN-R4a.1 | R007−DR007 spread | spread level | `−` | daily | LIQ | `S:F D:T P:N` | B |
| CN-R4a.2 | NCD yields | level | `−` | daily | LIQ | `S:F D:T P:N` | B |
| CN-R4b.1 | Amihud (index/ETF) | Amihud measure | `−` | close → t+1 | LIQ | `S:F D:T P:N` | B |
| CN-R4b.2 | Spread **estimator** (index/ETF) | **Roll or Corwin–Schultz from daily prices**: a true quoted spread needs L1/L2 quote history (`D:L`) | `−` | close → t+1 | LIQ | `S:F D:B P:N` | B |
| CN-R5 | Limit-down breadth (composite, **rule not yet chosen**) | **v3.2's "`.10` + `.14`" was wrong: `.10`'s population (N5+N6) already CONTAINS `.14`'s (N6), so summing double-weights locked names.** Candidate rules, none yet frozen: (a) `CN-R5 = CN-B3.10` alone (locked names counted once, as a subset); (b) two separately-consumed states, never summed; (c) an explicit severity-weighted composite with declared weights. **Pick one before use.** | `state` | close → t+1 | LIQ | `S:C D:T P:N` (**downgraded from `S:F`, v3.3: the composite rule is undefined, not just unweighted**) | B |
| CN-R6 | Drawdown state | DD from 252d high | `state` | none | VOL | `S:F D:T P:N` | descriptive |
| CN-R7 | CGB–equity correlation | 63d rolling stock–bond corr | `state` | close → t+1 | CORR | `S:F D:T P:N` | B |
| CN-R8 | **RTI (global as conditioner)** | → §12 | n/a | weekly | RISK-APPETITE-XA | `S:F D:A P:N` (→§12) | C |

**⚠ `CN-B3.4` sign alignment (v2.3).** `CN-B3.1` 涨停家数 and `CN-B3.2` 连板高度 need one common orientation before weighting, and `CN-B3.7` 炸板率 (formerly duplicated as `.3`, now retired. See below) must enter with the opposite sign from the other two. **A weighted sum of raw z-scores across mixed signs is economically undefined.**

**⚠ `CN-B3.1–.14` are `state`/`diag`, not signed alpha (v3.0 correction).** Limit-heat is **horizon-dependent, not monotonic**: moderate heat can predict short continuation, extreme heat can signal exhaustion, a rising failed-limit rate signals deterioration, and locked-limit-down is primarily a liquidity/execution-feasibility risk, not a return bet. A fixed `Dir` on any of these bakes in an assumption the data doesn't support. **Horizon-specific alpha hypotheses are separate, pre-registered objects that consume these states. Never assign `Dir` at the raw-measure level.**

**⚠ `CN-B3.5–.14`: raw numerators and endpoint access smoke-tested live, NOT the full share indicators (v3.0–v3.4).** The record below confirms fields exist, join correctly, and return internally-consistent counts, it does NOT confirm `N^eligible` (undefined), board-conditioned aggregation (`.1`/`.5`/`.6`/`.10`/`.14` are all `S:C` pending it), or `CN-R5`'s composite rule (also undefined). "Verified live" in the entries below means the numerator construction and data access, never the frozen share. `TouchUp`/`CloseUp`/`BrokenBoardRate`/`SealSuccess`/`CloseLimitDown` (`.5–.8`, `.10`) are **smoke-tested and buildable now** from `stk_limit` (up/down limit price) joined to `daily` (high/close). **Canonical reproducible numbers, three independent trading dates (v3.4, `tools/probe_cn_b3.py`):** 2026-07-30 → 79 touches, 56 closes, 23 broken, 83 close-down; **2026-07-31 → 231 touches, 103 closes, 128 broken**: this reproduces the original v3.0 citation EXACTLY, correcting a v3.3 error that wrongly called it "unreproducible" (the mismatch was that v3.3's reconciliation script queried 07-30 for the single-day stats when the original number was from 07-31, a date-selection mistake in the fix, not a real data gap); **2026-08-10 → 121 touches, 103 closes, 18 broken, 6 close-down**, fresh 11-day-later resample, order-of-magnitude consistent with both July dates. Continuation rate cross-checked on a second date pair (2026-08-07→08-10, trading-calendar-aware, correctly skipping the weekend): 13/75 = 17.33%, close to the original 10/56 = 17.86%. **Board-conditioning is now empirically demonstrated to matter, not just asserted:** 2026-08-10 touch-up rate ran Main 3.47% vs ChiNext 0.43% vs STAR 0.65% vs BSE 0% (an 8x spread) directly motivating the `.1`/`.5`/`.6`/`.10` downgrades below. **`CN-B3.7`/`.8` are exact complements sharing one denominator, register ONE as primary, the other as a derived readout, never both as independent votes. `CN-B3.3` was an undetected THIRD vote on the same construct as `.7` and is retired (v3.2).**

**⚠ `CN-B3.10` vs `.14`: a real conflation, corrected v3.2.** v3.1 labelled `Close = DownLimit` as "locked-limit-down." That measures **closing at limit-down**, not being locked there, a name can trade normally all day and only reach the limit near the close. **Verified live (2026-07-30):** `daily_basic.limit_status` (values 0–6; **5** = ordinary limit-down, **6** = locked/一字跌停, must be requested via explicit `fields=` or it is silently omitted from the response) shows **81 names at `limit_status=5` and only 2 at `limit_status=6`**: matching the 83-name `Close=DownLimit` reconstruction almost exactly, and showing the true "locked all day" population is **2, not 83**. `.10` is renamed **close-limit-down share**; the genuinely locked measure is the new `.14`, built from `limit_status=6` directly rather than reconstructed. `CN-R5` (§11 parent table) is `S:C` (v3.3): **NOT a frozen composite.** Summing `.10`+`.14` double-weights locked names (`.10`'s population already contains `.14`'s as a subset); three candidate rules are named in the `CN-R5` row and none is chosen. This paragraph previously said "frozen composite," which was stale and directly contradicted the `CN-R5` row below it, corrected v3.4.

**`CN-B3.9` continuation rate, arithmetic verified live, but board aggregation and edge rules are still open (v3.2 downgrade, `S:F → S:C`).** A pure 2-day chain of the `.6` close-up flag, no new endpoint or join:
```
CN-B3.9_t = Σ_i 1(CloseUp_{i,t}=1 ∧ CloseUp_{i,t−1}=1) / Σ_i 1(CloseUp_{i,t−1}=1)
```
Numerator and denominator both restricted to names **eligible on both days** (continuously listed, not suspended, not newly ST'd between `t−1` and `t`): a name delisted or suspended between the two dates is excluded from the denominator, not counted as a failure to continue. **Confirmed live:** 2026-07-30→07-31, 56 names closed limit-up on day 0, 10 continued closed limit-up on day 1 → rate 17.9%. **v3.1 wrongly promoted this to `S:F`: reverted.** The number is real, but the specification is not yet frozen. Open, unresolved as of v3.2:
- **Board aggregation**: one pooled scalar contradicts this family's own board-conditioning mandate (`.5`/`.6`). Must either report Main/ChiNext/STAR/BSE separately or freeze an explicit standardized aggregation across them.
- **Previous *trading* day, not calendar day**: `t−1` must skip weekends/holidays, not subtract one calendar day.
- **Denominator-zero → `NA`**, not undefined or zero.
- **Tick-integer price comparison**, not raw floating-point equality (limit prices are quoted to the tick; float equality on prices is fragile).
- **A rule for board/ST/limit-regime changes** between `t−1` and `t` (e.g. a name entering/leaving ST changes its limit band mid-comparison).
- **A suspension-treatment decision**: excluding suspended names from the denominator makes this a *continuation rate conditional on tradability*, which must be stated as such, not silently assumed.
- **Eligibility indicators written directly into the numerator and denominator**, not left as prose.

**`.11`/`.12` (reopening count, queue intensity) need `limit_list_d` or `kpl_list`: both CONFIRMED denied on this account (v3.1):** `limit_list_d` errors "抱歉，您没有接口访问权限" despite Tushare's docs claiming 5,000-pt access; **`kpl_list` and `kpl_concept` were tested directly and return the identical access-denied error**: this is a real entitlement gap, not an untested assumption. File a Tushare support ticket or verify whether a separate product code is required beyond the points balance. `.13` true seal duration needs minute/tick data (`S:O`), `first_time`/`last_time` alone **undercounts**: a name can reopen and reseal between those two timestamps, so the gap between them is not seal duration.

**⚠ Board-conditioning is mandatory, not optional.** 10%/20%/30% limit bands have structurally different hit probabilities: **pooling raw counts across Main/ChiNext/STAR/BSE is invalid.** Every `CN-B3.*` breadth measure needs board-segmented denominators; a single pooled ratio conflates regimes.

**⚠ Haven and flow rows are regime states, not standing bearish signals.** `CN-X2.1/.2` (gold, CGB duration) and `US-X4.1/.2` are marked `−` for convenience, but **under an inflation shock bonds stop hedging equities**, which is precisely why the parents carry a growth×inflation map. Route them through the regime state rather than hard-coding a bearish sign. The same caution applies to `CN-M5b` (PPI surprise), `CN-F2` (ETF creation), `CN-F1.1` (futures basis) and `CN-F4` (southbound): each is better read as a **conditional state** until the actor/regime attribution is frozen.

**`CN-M4.3` is not a robustness variant.** NBS and Caixin PMI sample different firm populations (large/SOE-weighted vs smaller/export-oriented). Treat as two indicators, not one with a check.

---

## 12. Cross-asset states & book-dependent diagnostics

| ID | Name | Class | Dependency | Own |
|---|---|---|---|---|
| **PR-R1A** | RTI: reconstruction (BII-inspired) | cross-asset state | 12-asset universe only: **computable before any stock portfolio exists** | `S:F D:A P:N` |
| **PR-R1B** | RTI: fixed economic ordinal comparator | cross-asset state | same | `S:F D:A P:N` |
| **PR-D1** | Diversification Ratio | **BOOK-DEPENDENT** | portfolio weights + covariance | `S:F D:A P:N` |
| **PR-D2** | DR concentration/correlation decomposition | **BOOK-DEPENDENT** | PR-D1 | `S:F D:A P:N` |
| **PR-D4** | Effective Number of Bets | **BOOK-DEPENDENT** | Meucci minimum-linear-torsion `w_MT = T^{−ᵀ}w` | `S:F D:A P:N` |
| **PR-T1** | Turbulence & absorption ratio | **BOOK-DEPENDENT** | covariance history | `S:F D:A P:N` |

**RTI (`PR-R1A`):** Spearman rank-correlation of recent asset-class returns against ex-ante risk ranks over a 12-asset universe (equity / duration / credit / commodities / gold). Deterministic **linear 40-day weights `w_j = (40 − j)/820`**, **63-day half-life EWMA**. `PR-R1B` is a fixed economic ordinal comparator on the same universe. Weekly. Data via yfinance + Tushare: **available now**.
**ENB (`PR-D4`)** reports **three numbers**: systematic ENB / residual share / residual HHI. **Co-primary with DR, not preferred**: different questions.
**Lifecycle:** all six are `registered` in Combination's registry (specified, not computed): an *empirical* status owned there, independent of `S/D/P`. DR/ENB/turbulence stay dormant until Combination runs; **RTI does not**: computable today, gated only on demonstrating incremental value.

---

---

## 12b. Registered-but-inactive cards (v2.4)

**Why these are cards and not backlog prose.** A *reference* library must document an important indicator even when it is licensed, current-only, unvalidated or deliberately inactive. **The anti-zoo rule governs what enters the portfolio, not what gets documented.** Every row below is `ACTIVATION: inactive`: catalogued, not voting.

**⚠ Honest label (v2.5): these are REGISTRATIONS, not full implementation cards.** v2.4 called them "full cards"; they carry 5–12 of the 14 mandatory fields. Most are `S:C` or `S:O`, not frozen. §12b.5 is expanded below to the mandatory schema because those rows are the ones you would actually reach for first; §12b.3 and §12b.4 remain **deliberately partial**: a licensed series you cannot yet obtain does not earn a full field map, and pretending otherwise is the exact overstatement this section is correcting.

### 12b.1 Foundational characteristics

| ID | Name | Out | Dir | TR | Formula | Min hist | Miss | CLK | Own | Eff US | Eff CN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **X-SIZE-T** | Total market equity | control | `−` | `TR-RANK` | `ln(price × total shares incl. non-tradable)` | 1d | NA | `CLK-CLOSE` | `S:F D:B` | `D:B P:P` | `D:T P:U` |
| **X-SIZE-F** | Free-float market equity | control | `−` | `TR-RANK` | `ln(price × free-float shares)` | 1d | NA | `CLK-CLOSE` | `S:F D:B` | **`D:L P:U`** | `D:T P:U` |
| **X-ILLIQ** | Amihud illiquidity | risk | `+` | `TR-RANK` | `mean(abs(r_d) / (turnover_value_d / 1e6))` over trailing **252d**, ranked **within market** | **120 valid days** | suspension & zero-volume days **excluded from numerator and denominator count**, not zero-filled | `CLK-CLOSE` | `S:F D:A` | `D:A P:N` | `D:T P:N` |
| **X-TURN** | Turnover (standalone) | alpha | `−` | `TR-RANK` | mean of `daily volume / free-float shares`, trailing **252d** | **120 valid days** | suspension days excluded | `CLK-CLOSE` | **`S:C D:A`** (denominator: free-float vs total vs provider-reported) | `D:A P:N` | `D:T P:N` |
| **X-PRC** | Nominal price level | alpha | `+` | `TR-RANK` | `ln(unadjusted close)` | 1d | NA | `CLK-CLOSE` | `S:F D:A` | `D:A P:N` | `D:T P:N` |
| **X-AGE** | Listing age | control | `+` | `TR-STATE` | months since first listing date | n/a | NA | `CLK-CLOSE` | `S:F D:A` | `D:B P:N` | `D:T P:N` |

**⚠ `X-SIZE-T` vs `X-SIZE-F` are two different objects, not a primary and a variant.** Factor exposure and CH3 replication require **total** market equity (§2.1); capacity, investable weighting and cost modelling require **free-float**. Using one where the other belongs is a silent error, in A-shares the gap is large and systematically related to SOE status.
**`X-TURN` is registered as an INACTIVE ALPHA HYPOTHESIS, not an established alpha.** LSY report CH-3 **fails** to explain the turnover category, which is a reason to *test* it standalone, not evidence that this particular 252-day formula predicts returns. v2.4's promotion语 overstated it. It stays RG-linked to `T-X6a` and `CN-B2`: **one budget, mandatory ablation.**
**`X-SIZE`/`X-ILLIQ` US feasibility corrected (v2.5):** historical **total shares outstanding** need a filing/market-data build (`D:B`), and historical **free-float shares are not a clean public series** (`D:L`): v2.4's `D:A P:N` was too optimistic for both.

### 12b.2 US macro, credit supply & term structure

| ID | Name | Out | Dir | TR | Formula | Lag | CLK | Own |
|---|---|---|---|---|---|---|---|---|
| **US-M9.1** | SLOOS: C&I standards, **large & middle-market firms** | state | `−` | `TR-STATE` | net % of banks **tightening** (pin the exact published series: C&I vs aggregate, large/middle vs small, weighted vs unweighted) | quarterly, ~2wk post-survey | **`CLK-RELEASE`** | `S:C D:A P:U` |
| **US-M9.2** | SLOOS: C&I loan demand | state | `+` | `TR-STATE` | net % reporting **stronger** demand, same firm-size cut as `.1` | quarterly | **`CLK-RELEASE`** | `S:C D:A P:U` |
| **US-M10.1** | ACM 10y term premium: level | state | **`state`** | `TR-STATE` | NY Fed ACM `ACMTP10` | daily, 1d | `CLK-RELEASE` | `S:F D:A P:U` |
| **US-M10.2** | ACM 10y term premium: 63d Δ | state | **`state`** | `TR-STATE` | 63-day change | daily | `CLK-RELEASE` | `S:F D:A P:U` |
| **US-M10.3** | ACM expected short rate: level | state | `state` | `TR-STATE` | expected-average-short-rate component: **pin the exact downloadable column** | daily | `CLK-RELEASE` | `S:C D:A P:U` |
| **US-M10.4** | ACM expected short rate: 63d Δ | state | `state` | `TR-STATE` | 63-day change | daily | `CLK-RELEASE` | `S:C D:A P:U` |

**`P:V → P:U` and `CLK-FILING → CLK-RELEASE` (v2.5).** SLOOS is a **scheduled macro release, not a corporate filing**, and the Fed has historically **corrected observations and redefined series**, so `P:V` was unearned without a release-vintage archive. "Net percentage" is also ambiguous until you pin C&I-vs-aggregate, firm-size cut and weighting; hence `S:C`. The raw data is freely downloadable.

**Supply and demand are separate constructs. Do not merge them into one `US-M9`.** Tightening standards with *rising* demand is a different macro state from tightening with collapsing demand; a net measure destroys exactly the information that makes the series useful.
**⚠ ACM is a MODEL ESTIMATE, not an observed price: `P:N → P:U` (v2.5).** The NY Fed describes the term premium as unobservable and statistically estimated; the series is **revised when the model is re-estimated**, so it behaves like agency output, not a market quote. Vintages must be archived before it is backtest-causal. **`Dir` also corrected to `state`**: a rising term premium can reflect changing discount rates, inflation risk *or* risk compensation, a hard-coded negative equity sign was unjustified.

**ACM closes a real hole:** `US-M1.*` treats the curve as one undifferentiated slope and `US-M8.*` splits only real vs breakeven. **A steepening driven by term premium is a different economic event from one driven by expected policy**, and the register previously could not distinguish them. Both free and daily.

### 12b.3 Baker–Wurgler sentiment, all six proxies

| ID | Proxy | Dir | Own | Note |
|---|---|---|---|---|
| **US-BW1** | Closed-end fund discount | `+` | `S:F D:L P:U` | clean history is licensed |
| **US-BW2** | NYSE share turnover (detrended) | `−` | `S:F D:B P:U` | **had no ID anywhere** |
| **US-BW3** | IPO count | `−` | `S:F D:B P:U` | = `US-CM1.1` |
| **US-BW4** | IPO first-day return | `−` | `S:F D:B P:U` | = `US-CM2.1` |
| **US-BW5** | Equity share of new issues | `−` | `S:F D:B P:U` | = `US-CM3` |
| **US-BW6** | Dividend premium | `−` | `S:F D:B P:U` | **had no ID anywhere** |

**⚠ `Dir` above is SENTIMENT-alignment, not return-direction (v2.5 clarification).** Read them as: **higher CEF discount → LOWER sentiment**; **higher turnover, IPO count, first-day return and equity share → HIGHER sentiment**; **higher dividend premium → LOWER sentiment**. Build the sentiment index first, *then* invert it once if you want a contrarian timing score. v2.4 mixed the two conventions in one column.
**Not reproducible yet: `S:C` at the family level.** A source-faithful build additionally needs: exact raw proxy definitions · the **current-vs-lagged** proxy convention · the macro controls used for orthogonalization · the standardization window · the **PCA training/refit policy** · a missing-proxy rule · annual-vs-monthly frequency. Sentiment is the **first principal component of the six**, orthogonalized to business-cycle controls: **not a mean of z-scores**.
**Two distinct objects:** the **historical academic series** (freely available from Wurgler's site) versus a **live maintained reconstruction** (needs paid CEF data). They are not interchangeable.
**`US-BW1`, `US-BW2` and `US-BW6` were entirely absent from the register. `US-BW3/4/5` are CROSS-REFERENCES to `US-CM1.1`/`US-CM2.1`/`US-CM3`**: they are not new atomic outputs and are excluded from the catalogue count.

### 12b.4 Limits-to-arbitrage, documented, mostly licensed

| ID | Name | Own | Note |
|---|---|---|---|
| **MS-C1a** | Borrow availability | `S:F D:L P:U` | US securities-finance vendors; CN broker-specific security×broker×date |
| **MS-C1b** | Borrow fee / utilization | `S:F D:L P:U` | licensed |
| **MS-C1c** | Short interest / float | `S:C D:B P:P` | FINRA short interest is **public and free**, twice monthly, distinct from daily short-sale volume. **`PUBLIC-BUILD` because the float denominator, identifier history and publication-date join must be constructed.** Info-timestamp = the **official publication date, NOT the settlement date.** |
| **MS-C2a** | Institutional ownership (13F) | **`S:C D:B P:P`** | **Access is PUBLIC-BUILD**: SEC structured 13F datasets are public and as-filed from May 2013. **Coverage is partial** (quarterly, ≤45d late, qualifying managers, 13(f) securities only: **not** total institutional ownership) but that is a *coverage* limit, not an *access* class. Needs rules for amendments, duplicate managers, confidential-treatment delays, security mapping, shares outstanding. |
| **MS-C2b** | Passive-lendable share | `S:F D:L P:U` | licensed |
| **MS-C3b** | Analyst coverage count | `S:F D:L P:U` | consensus gap |
| **MS-C3c** | Forecast dispersion | `S:F D:L P:U` | consensus gap |
| **MS-C4a** | Timestamped negative news | **`S:O D:L P:U`** | Not `S:F` without a declared **news universe, deduplication policy, NLP model/dictionary + version, and aggregation window**. Filings are **not** a substitute for a market-wide corpus. |

### 12b.5 A-share-native, expanded to the mandatory schema (v2.5)

| ID | Name | Out | Dir | TR | Formula (exact scalar) | Min hist | Miss/tie | CLK | Info-ts | RG | Own | E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CN-N1a** | Northbound holdings: quarterly panel | state | `+` | `TR-RANK` | `northbound_shares / free-float shares`, quarter-end | 4q | absent = **not held (0 valid)**; unmapped = NA | `CLK-RELEASE` | 5th Connect day after quarter-end | `NB-FLOW` | `S:F D:T P:P` | -/C |
| **CN-N1b** | Northbound: daily top-ten net | state | `+` | `TR-STATE` | **net buy value** on the daily top-ten actives list ÷ that name's turnover value | 21d | **not on list = NA, NOT 0** (absence ≠ no flow) | `CLK-CLOSE` | post-close, T+0 | `NB-FLOW` | `S:C D:T P:F` | -/D |
| **CN-N1c** | Northbound holdings: legacy daily | state | `+` | `TR-RANK` | as `CN-N1a`, daily | 63d | n/a | `CLK-CLOSE` | **series ENDS 2024-08-19** | `NB-FLOW` | `S:F D:T P:V` | -/C |
| **CN-N2a** | Margin balance: level | state | `−` | `TR-RANK` | `融资余额 / free-float mcap` | 63d | non-eligible names = **NA, not 0** | `CLK-CLOSE` | T+1 morning | `LEV-CN` | `S:F D:T P:U` | -/C |
| **CN-N2b** | Margin balance: 21d change | alpha | `−` | `TR-RANK` | `Δ21d(融资余额) / 融资余额_{t−21}` | 84d | as above | `CLK-CLOSE` | T+1 morning | `LEV-CN` | `S:F D:T P:U` | -/C |
| **CN-N4** | Unlock (解禁) overhang | penalty | `tail−` | `TR-TAIL` | `Σ unlock value over the next 90 calendar days / free-float mcap` | n/a | no scheduled unlock = **0 valid** | `CLK-CORPACTION` | unlock **announcement** date drives the signal; **ex-unlock date** drives execution | `SUPPLY-CN` | `S:C D:T P:U` (horizon 30/60/90 + tail thresholds) | -/C |
| **CN-N5a** | Pledge ratio: level | penalty | `tail−` | `TR-TAIL` | `pledged shares / total shares` | n/a | no pledge = **0 valid** | `CLK-FILING` | disclosure date | `PLEDGE-CN` | `S:C D:T P:U` (thresholds) | -/C |
| **CN-N5b** | Pledge ratio: change | penalty | `tail−` | `TR-TAIL` | `Δ(pledge ratio)` vs prior disclosure | 2 obs | first disclosure = NA | `CLK-FILING` | disclosure date | `PLEDGE-CN` | `S:C D:T P:U` | -/C |
| **CN-N6** | Insider net 增持/减持 | alpha | `+` | `TR-EVENTZ` | `Σ(buy value − sell value) over trailing 63d / free-float mcap`, **董监高 + 控股股东 only**, excluding 大宗交易 transfers and 股权激励 exercises | 63d | no transaction = **0 valid** | `CLK-FILING` | announcement **evening** → executable next session | `INSIDER-CN` | `S:C D:T P:U` (insider class + txn-type filter) | -/C |
| **CN-RET1a** | Retail-skewed small-order imbalance: level | state | `−` (contrarian-heat) | `TR-RANK` | `SOI_t = Sum_i(BuySmall_i - SellSmall_i) / Sum_i(BuySmall_i + SellSmall_i)`, from `moneyflow`: **NOT verified retail flow**, a proxy inferred from fixed nominal order-size bands + active buy/sell classification | 63d (rolling percentile window) | zero-volume names = NA | `CLK-CLOSE` | T+1 morning (vendor batch) | `RETAIL-CN` | `S:C D:T P:U` (rolling-percentile window unpinned) | -/C |
| **CN-RET1b** | Retail-skewed small-order imbalance: turnover-normalized | state | `−` | `TR-RANK` | `SOI_t` scaled by same-session, same-universe turnover value: **normalizer must match SOI's session/universe exactly or the ratio is meaningless** | 63d | zero-turnover names = NA | `CLK-CLOSE` | T+1 morning | `RETAIL-CN` | `S:C D:T P:U` | -/C |

**⚠ `CN-RET1` is `D:T`, not `D:A`: `moneyflow` requires >=2,000 Tushare points, it is not public-free.** Every A-share endpoint on this stack is entitlement-gated; this is the register's own convention (§1.2), applied here after an earlier draft wrongly labelled it `D:A`.
**⚠ "Small order" != "retail investor."** The vendor classifies by fixed nominal RMB order-size bands plus an active buy/sell inference, institutions routinely split large orders into small tickets, and retail can submit large ones. Label it a **retail-skewed proxy**, never "verified retail flow."
**⚠ Fixed RMB thresholds create a secular comparability problem.** Band cutoffs don't move with market-cap growth or inflation, so a raw `SOI` level drifts in meaning across years. Use **rolling percentiles, not full-sample z-scores**, and test residualizing against price, market cap and turnover before trusting a cross-sectional comparison.
**⚠ Overlaps the existing `AShare_Fear_Greed_Index` project's turnover-heat leg**: cross-reference rather than let the two drift into separately-maintained retail-heat readings.

**⚠ `CN-N1b` is not a scalar until you pick one.** "Top-ten presence" is a *list membership*, not a signal. The declared output above is **net buy value scaled by the name's turnover**; inclusion-flag, gross buy, gross sell and share-of-aggregate-northbound-turnover are **different indicators**, not variants. Hence `S:C`.
**⚠ `CN-N2` split into level and change**: v2.4 had one row. Level is a *state* (how levered is this name), change is a *flow*; they have different horizons and are not one output.
**⚠ `CN-N5` split into level and change** for the same reason. Pledge *level* is a standing structural risk; a *rising* pledge ratio near a margin-call threshold is the acute signal.
**⚠ `CN-N6` scope must be declared**: "insider" in A-shares spans 董监高, 控股股东 and 一致行动人, and the transaction tape mixes open-market trades with 大宗交易 block transfers and 股权激励 exercises that carry no information. Without the filter this measures paperwork.
**⚠ `CN-N1a/b/c` are three cards because the DATA GENERATING PROCESS changed**: real-time northbound disclosure ended 2024-05-13; security-level holdings went **daily → quarterly on 2024-08-19**. `CN-N1c` is **history-only**: a backtest trained on it describes a signal that no longer exists at that frequency. Regime-date it exactly like the 2024 国九条 break in `F7`.
**`CN-N4` finally has an owner**: §6.4 states 解禁 "is a supply variable, NOT NSI" and then gave it no home; orphaned across four versions.

---

## 13. Relationship map

**Typed vocabulary (v2.1, v2.0 overused `=`):**
`identity` algebraically the same quantity · `nested` one is a component of the other · `shared-input` different outputs from a common intermediate · `alt-estimator` different measurements of the *same* mechanism · `correlated-family` distinct mechanisms with attribution overlap · `conditioner` one modifies the other · `ablate` mandatory redundancy test · `exclusive` at most one may be active · `untested` independence is an assumption, not a result.

| A ↔ B | Type | Rule |
|---|---|---|
| `F1-EP` ↔ `B/M × ROE` | **identity** | the product is E/P; not a third measure |
| `F1-FCFFEV` ↔ `F1-ECFOEV` | **nested** | `FCFF = EnterpriseCFO − capex`; only one in the base composite |
| `F1-NOPATEV` ↔ `F1-EBITEV` | **nested** | `NOPAT = NormalizedEBIT·(1−T_op)` |
| `F7-NPY` ↔ `F7-DSH` | **alt-estimator** | both measure the **equity payout/dilution** channel; reconcile, never add |
| `F7-DBNETIS` ↔ `F7-NPY`/`F7-DSH` | **correlated-family** | a **distinct financing-policy channel**, not an alternative estimator: three channels under one `CAPALLOC` budget |
| `F7-NSI1Y` ↔ `F7-CSI5Y` | **alt-estimator** | combine via tail classification, not averaging |
| `R-X1` ↔ `R-X3` | **shared-input** | both consume P6's `ε` vector; not the same output |
| `R-X1` ↔ `R-X7` | **correlated-family** | R-X7's **primary is peer-basket** residual risk; IVOL is only a named baseline alternative |
| `P6 output` ↔ `adjRet9` denominator | **shared-input** | `adjRet9` is a **separate comparator, not T-X2**; its denominator is P6's output: no second IVOL vote |
| `R-X2` ↔ `R-X6a` | **ablate** | `β = vol × corr`: mandatory horse race |
| `R-X4a` ↔ `R-X1` | **ablate** | MAX absorbs and *reverses* IVOL's coefficient |
| `R-X4*` ↔ `CN-B3.*` | **ablate** | limit-up complex overlap, cross-file |
| `T-X6a/b` ↔ `CN-B2` | **ablate** | abnormal-turnover overlap, cross-file |
| `T-X4` ↔ `F1-*` | **ablate** | long reversal overlaps value by construction |
| `T-X8` ↔ `T-X1`/`T-X2` | **untested** | independence is an empirical result, not an assumption |
| `T-X1` ↔ `T-X2` ↔ `F5-CAR`/`F5-SUE` | **ablate** | momentum and surprise may carry incremental info after mutual control |
| `T-X5`, `T-X6*` → `T-X1`/`T-X2` | **conditioner** | never standalone scores |
| `T-X7a` ↔ `T-X7b` | **exclusive** | a product activates exactly one |
| `F6-AG` ↔ `F6-q5` | **correlated-family, opposite signs** | never composited; separate RGs |
| `F2b-dROE` ↔ `F5` forecast-ROE rev ↔ `q5 dROE` | **correlated-family** | **three different variables** (realized improvement / analyst revision / q5's realized quarterly predictor) with genuine attribution overlap: **not an identity**; must not become three votes |
| `F3-*` ↔ `F2-*` | **ablate** | operating profitability may subsume accruals, esp. CN |
| `F2b-*` ↔ `F2-*` | **ablate** | change vs level |
| `F8-FS*`/`F8-GS*` ↔ `F2`/`F3`/`F4` | **nested** | overlay components are drawn from these; must not re-vote |
| `R-X5` ↔ Fundamental F-stability | **identity of ownership** | instantiate once |
| `T-X1` stage-2 → `US-T3`/`CN-T3` | **ownership** | neutralization strips industry momentum; the parent owns it |
| `MS-R2a/b` ↔ `T-X1` | **shared-input** | CoMomentum forms on the 12-1 deciles; reuse the sort |
| `MS-R5`, `MS-R8a`, `MS-R8a-agg` ↔ `X-ILLIQ`, `MS-I1` | **shared-input** | days-to-liquidate & Amihud (raw + basket agg.) reuse the capacity/illiquidity objects: no parallel metric |
| `MS-R7a1/a2/b1/b2` ↔ `CN-N2a/b`, `CN-N5a/b` | **shared-input** | A-share leverage *vulnerability* = existing 两融 + pledge cards, not new data (NOT forced flow. See §9b.2) |
| `MS-R9` ↔ `F5-CAR`, `F5-SUE` | **shared-input** | BadReactionBreadth = event CAR×SUE; positioning read, not a 2nd earnings vote |
| book RC/ENB → `PR-D4` | **extends, ≠ identity** | ENB/residual-share exist in PR-D4; momentum-RC + theme-cosine must be ADDED to PortfolioRisk, not assumed present |
| all `MS-R*` → Combination | **PENDING wiring (§9b.5)** | *proposed* cap/scalar consumer: **not yet consumed**; Combination still references only legacy `MS-R1`. Never an alpha sign. |
| `F7-EFNOA` ↔ `F7-DINOA` + `F7-EINOA` | **nested** (v3.6) | `EFNOA` is the sum of the debt and equity legs: a **derived readout**, not a third independent source; one budget |
| `F3-ACC-BS` ↔ `F3-ACC` | **alt-estimator, ablate** (v3.6) | both estimate the same accrual mechanism (balance-sheet vs cash-flow-statement method), Hribar–Collins show they diverge around M&A/FX, which motivates carrying both, but they are **one redundancy group**, never two independent votes |
| `F2c-CFOS` ↔ `F3-CFOA` | **alt-estimator** (v3.6) | same numerator (CFO), different denominator (sales vs assets): a denominator choice, not two mechanisms |
| `F2c-DAT` ↔ `F8-FS9` | **shared-mechanism, continuous-vs-binary** (v3.6) | `F2c-DAT` is the continuous alpha version of the same Δasset-turnover signal `F8-FS9` already votes on as a Piotroski binary. Do not double-count inside one composite |
| `F2c-OPLEV` ↔ `F2-OL` | **UNRESOLVED: possibly identical** (v3.6) | attribution ambiguity, see both rows; do not treat as confirmed-independent until the source text is checked |

---

## 14. *(reserved)*

## 15. Excluded register

| Object | Blocking reason |
|---|---|
| **F1 forward E/P**, **US-V2** | Analyst consensus. 朝阳永续/Wind (CN) or I·B·E·S/Zacks (US); **not** in the 5000-pt tier (`report_rc` @¥500/yr is unstructured PDF, not a PIT panel). **= Sorensen–Hua–Qian (2005) `RV` composite's "earnings yield (IBES FY1)" leg: v3.5 cross-check confirms this is the only one of their five RV factors not covered; the other four (B/P, sales/EV, historical E/P, EBIT/EV) already map to `F1-BP`/`F1-SEV`/`F1-EP`/`F1-EBITEV`.** |
| **F5-REV** | Same gap. Structural rules frozen; **vendor/PIT field contract open** (dispersion endpoint, `ε`, `N_min`, staleness, aggregator, FY-roll, `N_eligible`). **= Sorensen–Hua–Qian (2005) `MO` composite's "nine-month earnings revision" leg: v3.5 cross-check confirms this is the only one of their three MO factors not covered; the other two (6-month price momentum, earnings surprise score) already map to `T-X1v6`/`F5-SUE`.** |
| **F5-RECO** | Consensus gap **+** primary undeclared (recommendation vs price-target). |
| **F5-LTG** | **Deferred research-catalogue item, not in the operational registry.** Sign not automatically positive: `ΔLTG` direction vs `LTG-level` over-optimism; main effects mandatory alongside the interaction. CN E:D / R:D. |
| **F2-RNOA / F2-CRNOA / F6-NOAG** | **NOA field contract is a checklist, not fixed**: pin six: goodwill/acquired-intangibles, net DTA/DTL, pensions, minority interests, operating-lease capitalization, denominator floor on `abs(avg NOA)`. **Negative/near-zero NOA is NOT auto-NA**: normal for retailers/distributors/platforms; flag as a state with sector-specific eligibility. |
| **F2-OL / ΔOL** | Research-only conditioner by decision. Sign not universally positive; OL mechanically levers RNOA. |
| **US-V3.\*, CN-V5.\*** | Index-level consensus revisions. |
| **Surprise legs**: `US-M5.2` `US-M6.1/.2` `CN-M4.4` `CN-M5a` `CN-M5b` | Need a **frozen consensus vintage**. **The realized-data legs are buildable now**. Split the row rather than blocking the indicator. |
| **CN-F5** | Vendor-modelled positioning estimate; licensed and model-based. |
| **CN-M9** | Modelled construct; cyclically-adjusted-primary-balance construction unspecified. |
| **US-S10a** | Licensed timestamped daily news feed. |
| **US-VRP1** | Option-implied surface, licensed. Both terms must share horizon `H` and measure. |
| **Financials `FIN-B1…B21`** | Bank regulatory disclosures (NPL, provision coverage, CET1, NIM) need Wind 💲 or 公司公告 PDF + NLP 🔨. LGFV/property look-through is footnote text (R:D). `registered`, several estimators unfitted. |
| **`FIN-I*` / `FIN-K*`** | Registered diagnostic outlines; no per-indicator contract. Insurer ALM `blocked-by-data`. |
| **`FIN-USB*`** | Research agenda, no contract. |
| **MS-C1** | Borrow/loan-supply: 💲 (US) / broker-specific security×broker×date (CN). |
| **MS-C2** | Active/passive-lendable ownership decomposition: licensed. |
| **MS-C3 coverage leg** | Analyst coverage/dispersion: consensus gap. **The delay leg is buildable, §9.** |
| **MS-C4** | Licensed news measures. |
| **MS-R1** | Holdings/flow data: licensed. |
| ~~**CH3 construction (P7-CN)**~~ | **SPECIFICATION-resolved v2.2** (§2.1, from Liu–Stambaugh–Yuan), but `R-X1`/`R-X3`/`T-X2` remain **PIT-blocked** for A-shares because CH3's value factor consumes reported earnings (§2.1). Specification-unblocked ≠ backtest-ready. *(It never gated `R-X7`, whose primary is the peer-basket regression.)* |
| **Expected-IVOL (EGARCH)** | Separate deferred hypothesis, **opposite sign** to R-X1; published positive result largely look-ahead. |
| **CN daily cross-sectional momentum** | Distinct *daily* attention-driven phenomenon; needs an intraday/T+1 execution model. |
| **Leveraged BAB** | Financing and shorting integral to the published portfolio: separate strategy contract. |
| **Survivorship-free universe / PIT ST-status (P4/P5)** | Partial both markets. **A prerequisite for trusting every row above, not an indicator.** |

---

## 16. Build order

1. **PIT spines**: P8/P13/P14 (fundamentals + events) **and P15 (macro vintages)**. Longest lead; vendors overwrite history, **forward archiving starts now**. **P15-CN has no verified standardized archive in the current stack, either validate a commercial vintage source at procurement, or snapshot from today; otherwise those rows stay `P:F`.**
2. **P2/P3 price + P4/P5 universe**: delisting and PIT ST history. Pin P4's liquidity threshold and P1's open-vs-VWAP.
3. **P9 PIT sector membership**: gates `R-X7`, `F8-GS*`, `CN-T3`, `CN-X4` and all `TR-SECRANK`.
4. **P7 factor returns → P6 engine**: US pulls Ken French immediately; **CN CH3 is now SPECIFIED (§2.1) but still needs CONSTRUCTION plus an earnings-vintage audit** before its residuals are backtest-causal. Critical path for three A-share indicators.
5. **§0.1 entries**: everything formula-ready and PIT-clean. Fastest to first result.
6. **Factor-model cards**: R-X1, R-X3, T-X2 (US now; CN after step 4).
7. **Fundamentals**: F1-EQ → F2 → F3 → F4 → F7 → F1-EV (heaviest) → F6 → F2b.
8. **Events**: F5-CAR, F5-CNPRE/CNEXP, F5-SUE.
9. **F6-q5**: the 120-month rolling library plus response-maturity is the most machinery for one signal.
10. **Conditioners**: T-X5, T-X6a/b, MS-C3a.
11. **RTI (PR-R1A/B)**: independent; parallel from step 1.
12. **DR/ENB/turbulence**: only once Combination produces a book.
13. **MS-R crowding family**: specify `MS-R2` CoMomentum to a full field contract first (it is the anchor and avoids licensed holdings data, but still needs a PIT-eligible universe (`P4`/`P5`), a momentum sort, and (for A-shares) PIT industry membership (`P9`); it is the *lightest* dependency chain in the family, not a dependency-free one). Then wire the three summary states into Combination/PortfolioRisk (§9b.5, currently PENDING) before any other MS-R card is built.

---

## 17. Maintenance

- **This register is authoritative for implementation.** On disagreement over a formula, direction, field or timing rule, fix the contract and log it here.
- **Divergence log:** *(none open: MS-R consumer wiring into Combination/PortfolioRisk is tracked as a PENDING task in §9b.5, not a divergence)*
- **Source basis:** Fundamental **v1.11** · **Financials v1.13** · TrendReversal **v1.10** · StatRisk **v1.5** · MarketStructure **v1.3** · PortfolioRisk **v1.6** · Combination **v1.11** · US **v2.8** · A-share **v2.8**.
- **Promotion paths:** `S:C → S:F` when the named choice is pinned (record it here *and* in the contract) · `S:R → S:F` after source verification (§0.6) · `S:O → S:C` when a construction is specified · `D:L → D:A` when a feed is acquired (move out of §15) · `P:U → P:V` when the vintage audit passes.
- **§0 must be regenerated whenever any readiness changes**: it is a derived view, not an independent list.
- **Do not add an indicator with no owning contract.** This register documents; it does not originate.

---

### Change log

**v3.6 (source-verification correction pass on the v3.5 Sorensen–Hua–Qian additions).** A review found real errors, not just presentation issues:
- **Source-audit-trail overclaim corrected.** v3.5 said "source verified directly" / "pulled Exhibit 1 directly from the paper" for a table obtained from a third-party course slide deck (confirmed title page: Sorensen/Hua/Qian, "Contextual Fundamentals, Models, and Active Management," reproducing the 2005 JPM paper): **the deck gives factor NAMES, not calculation formulas.** `F2c-DAT` and `F2c-CFOS`'s exact constructions were plausible standard ratios, not confirmed against primary text, both **downgraded where overclaimed** (`F2c-CFOS` `S:F → S:C`).
- **`F2c-OPLEV` attribution retracted from settled to unresolved.** v3.5 asserted "level of operating leverage" = degree-of-operating-leverage (`%ΔEBIT/%ΔSales`) and called it "the first true operating-leverage card... no prior card." **Both claims were false or unverifiable:** the register's own pre-existing `F2-OL` (operating liabilities/NOA, Nissim–Penman "operating liability leverage") is a textually closer match under this same author team's QEPM glossary, and neither reading is confirmed from primary text. `F2c-OPLEV` is now registered as **candidate reading A**, `S:O` (not `S:C`), with the row and the relationship map explicitly flagging the unresolved overlap with `F2-OL` rather than asserting independence.
- **`F3-ACC-BS` had a real formula error, missing depreciation.** Confirmed against Sloan (1996): the balance-sheet accrual construction is `−[(ΔCA−ΔCash)−(ΔCL−ΔSTD−ΔTP)−Dep]/avgAssets`; v3.5 omitted `−Dep`, which materially changes the ranking for capital-intensive firms. Fixed. Also reclassified in the relationship map as `alt-estimator, ablate` against `F3-ACC` (Hribar–Collins show they diverge around M&A/FX, that motivates carrying both, not treating them as independent votes; both stay in one redundancy group).
- **Relationship map gained 4 typed entries** the new cards needed and didn't have: `F7-EFNOA` = `nested` (sum of `F7-DINOA`+`F7-EINOA`, a derived readout not a third source), `F3-ACC-BS` ↔ `F3-ACC` = `alt-estimator`, `F2c-CFOS` ↔ `F3-CFOA` = `alt-estimator` (denominator choice, not two mechanisms), `F2c-DAT` ↔ `F8-FS9` = shared mechanism (continuous vs binary of the same signal. Don't double-count).
- **The "3–8x" contextual-weighting claim was a market-regime mischaracterization, not just imprecise.** The paper's contexts are **cross-sectional stock characteristics** (value/growth/earnings-variability), not time-varying regimes; the paper reports two *specific* composite-weight comparisons (EF 43.0% vs 5.1% across value; OE 52.7% vs 16.9% across growth), not a general 3–8x pattern across all weights, and its own **earnings-variability context was not clearly differentiated from the static model**. Also noted: a source-faithful replication needs licensed Compustat/IBES/Barra data. Corrected in the architecture note, and in `Indicators_Pool_Combination_v1.md` (v1.12→**v1.13**): item (g) reframed from "regime-conditional" to "cross-sectional stock-context × factor interactions," explicitly flagged as substantially overlapping the pre-existing item (d) moderator-routing mechanism rather than a wholly new architectural gap.
- **Fixed 4 stale `Combination v1.11` references in `README.md`** (2 more than initially flagged) that survived the v1.11→v1.12 bump.
- **NOA readiness (`D:U`) on the new `F7-EFNOA`/`F7-DINOA`/`F7-EINOA` reviewed, not changed**, a reviewer suggested `D:B`/`D:T` since NOA's raw inputs are publicly reachable; these three rows were classified `D:U` to match the **pre-existing, already-established** pattern on `F2-RNOA`/`F2-CRNOA`/`F6-NOAG` (§15): the blocker is that NOA's 6-item field-mapping checklist is undeclared, not that the underlying statements are unreachable. Left consistent with precedent rather than changed unilaterally on only the 3 new rows; revisiting all four together is a fair follow-up if the `D:U` convention itself is judged wrong.
- **A-share PIT (`P:U` vs `P:F`) on the new fundamental rows reviewed, not changed**, the new rows match every existing fundamental row in §6 (all show `P:U`), which itself appears to sit in tension with the §0.2 summary line asserting blanket `P:F`. This is a **pre-existing inconsistency spanning 30+ rows**, not something introduced by the new cards; flagged here rather than patched on 3 rows in a way that would create fresh inconsistency against the other 30.
- Counts unchanged: **377 rows / 373 unique** (this pass corrected content, not row count), `RESULT: PASS`.

### Change log, v3.5

**v3.5 (Sorensen–Hua–Qian 2005 cross-check, 5 factor composites, 3 genuine gaps).** User asked whether the register covers the five factor composites (`RV`/`OE`/`AA`/`EF`/`MO`) from Sorensen, Hua & Qian, *Contextual Fundamentals, Models, and Active Management*, JPM 32(1):23–36 (2005): the same author team as the QEPM book already cross-mapped into this register. Source verified directly (Exhibit 1, the paper's own factor-composite definition table, obtained from a course slide deck reproducing it). All 17 underlying factors checked against the live register:
- **`RV` (Valuation): 4/5 already covered**, 1 gap (IBES FY1 forward E/P) is the **same pre-existing consensus gap** as `F1` forward E/P / `US-V2`: cross-referenced, no new card needed.
- **`OE` (Operating Efficiency): 0/3 existed as standalone cards.** Added **`F2c-DAT`** (Δ asset turnover, previously only a Piotroski *binary*, `F8-FS9`, never a continuous alpha), **`F2c-OPLEV`** (operating leverage, no prior card of any kind, the register's first cost-structure-sensitivity factor), **`F2c-CFOS`** (CFO/sales, previously conflated with the assets-denominator `F3-CFOA`; the two use different denominators and are not interchangeable).
- **`AA` (Accounting Accruals): 1/2 existed.** Added **`F3-ACC-BS`** (balance-sheet method, Sloan 1996 original construction) alongside the pre-existing `F3-ACC` (cash-flow-statement method), Hribar–Collins (2002) show these **diverge materially** around M&A/FX/discontinued ops, and the source paper treats them as two separate factors, not two implementations of one number.
- **`EF` (External Financing): partial, and the 3 gaps are NOA-denominator variants blocked by the register's own already-tracked NOA field contract.** Added `F7-EFNOA`/`F7-DINOA`/`F7-EINOA` as `S:O`, cross-referenced to the same blocker as `F2-RNOA`/`F2-CRNOA`/`F6-NOAG` (§15): these unblock together once NOA is frozen, not independently.
- **`MO` (Momentum): 2/3 already covered**, 1 gap (9-month analyst earnings revision) is the **same pre-existing consensus gap** as `F5-REV`: cross-referenced, no new card needed.
- **Architecture finding, not a card:** the paper's central result is that optimal factor weights vary **3–8x** across value/growth/earnings-variability contextual buckets, a mechanism this register has no equivalent of (Combination applies fixed per-mechanism weights + moderator multipliers, not bucket-conditional reweighting). Flagged as **Combination open item (g)**, `Indicators_Pool_Combination_v1.md` v1.11→**v1.12**, rather than invented as an indicator card, this is a product-architecture decision, not a data gap.
- 7 new cards, all genuinely new content (no renumbering, no restatement): **377 rows / 373 unique**, `RESULT: PASS`.

### Change log, v3.4

**v3.4 (fresh live retest + remaining prose/readiness fixes).** A review found the v3.3 fixes structurally landed but left one live contradiction and an overstated readiness pattern; a fresh test against current data (2026-08-10/11, ~11 days after the v3.3 sample) both confirmed and corrected further:
- **Fixed a live contradiction.** The prose at `CN-B3.10 vs.14` still said `CN-R5` was a "frozen composite of `.10`+`.14`", the exact double-counting construction v3.3's `CN-R5` row already rejected. The table was right; this one paragraph was not. Corrected to match.
- **Downgraded `CN-B3.1`, `.5`, `.6`, `.10` from `S:F` to `S:C`.** Their raw numerators are verified, but `N^eligible` (ex-ST, ex-suspended, listed ≥6m, per `P4`) is undefined everywhere in the register, so the *share* (what the card actually claims to output) isn't frozen just because the count is. **`.1` additionally gained empirical evidence, not just a rule citation:** a fresh board split on 2026-08-10 showed touch-up rates of Main 3.47% vs ChiNext 0.43% vs STAR 0.65% vs BSE 0% (an 8x spread) directly demonstrating that all-boards-pooled distorts the reading rather than merely violating a stated convention.
- **"Verified live" narrowed to what was actually verified.** Was read as confirming the frozen share indicators; now states explicitly that it confirms raw numerator construction and endpoint access only, board conditioning, `N^eligible`, and `CN-R5`'s rule remain open regardless of what the probe returns.
- **Pinned `tools/requirements.txt`** (`tushare==1.4.29`, `pandas==2.2.3`) instead of unpinned names.
- **Rebuilt the probe with merge-integrity assertions** (duplicate-`ts_code` check, unmatched-row counts on both sides of every join) and a board-split diagnostic, run against **three independent trading dates** (2026-07-30, 07-31, 08-10) plus a second continuation-rate pair (2026-08-07→08-10, correctly trading-calendar-aware).
- **A genuine finding from the fresh run, corrected mid-session:** the v3.3 claim that the original `231/103/128` figure was "an untracked, unreproducible session" was **wrong**: the fuller probe reproduced it exactly, from **2026-07-31** (v3.3's reconciliation script had queried 2026-07-30 for the single-day stats, a date-selection mistake, not a real data gap). The "not independently verifiable, do not cite it" language and the "SUPERSEDED" mark on the v3.0 changelog entry were both retracted in this same pass, rather than left standing once the fresh data contradicted them.
- **Confirmed 2026-08-11 (the current session's "today") returns zero rows on `stk_limit`/`daily`**: same-day end-of-day data had not posted yet at probe time. Documented as expected publication-timing behavior in the probe, not an error.
- **Cross-validated across three dates:** touch/close/broken counts are internally consistent within each date (`touch − broken = close` holds exactly on all three), and continuation rate agrees to within noise on two 2-week-apart samples (17.9% vs 17.3%): evidence the construction is stable, not the product of one lucky sample.
- Counts unchanged: **370 rows / 366 unique**, `RESULT: PASS`.

### Change log, v3.3

**v3.3 (v3.2's fixes never actually landed, root cause + real fix).** A review found that the v3.2 table still showed the OLD `CN-B3.9`/`.10` errors despite the v3.2 changelog claiming both were fixed. **Root cause identified:** the script that edited both rows crashed on an unrelated assertion error (a column-count mismatch on `CN-B3.13`) *after* mutating the in-memory string for `.9`/`.10` but *before* the `open(...).write()` call, so those two edits were silently lost, while a *separate*, later script successfully edited the surrounding prose paragraphs (which matched different anchor strings and ran in an unrelated call). The prose was right; the table (the thing an implementer actually reads) was not. This is now fixed directly, verified with `grep` immediately after write, not just a script's own "success" printout:
- **`CN-B3.9` row: `S:F → S:C`, actually applied.** Table now matches the prose that has said `S:C` since v3.2.
- **`CN-B3.10` row: renamed "Locked-limit-down share" → "Close-limit-down share", actually applied.** Formula unchanged (`Close = DownLimit`); only the label was wrong.
- **Deleted a stale paragraph** that re-asserted the old `.10` name and formula after the correct paragraph above it, a leftover from v3.1 that never got removed when v3.2 added the real explanation.
- **`CN-B3.14` downgraded `S:F → S:C`.** The source field and numerator are verified, but one pooled scalar contradicts this family's own board-conditioning mandate (`.5`/`.6`): same defect `.9` already had, just missed on `.14` in v3.2.
- **`CN-R5` composite math was wrong, not just unweighted.** `.10`'s population (`N5+N6`, i.e. all close-limit-down) already *contains* `.14`'s population (`N6`, the locked subset), so v3.2's "`.10` + `.14`" summed a set with its own subset, silently double-weighting locked names. Downgraded `S:F → S:C` with three named candidate rules (`.10` alone; two separately-consumed states; an explicit severity-weighted composite) and none chosen. The A-share parent contract (`Indicators_Pool_AShare_v2.md` `CN-R5`) carried the same additive wording, flagged there too, pointing to the register for the resolution.
- **Fixed the index alias count**: declared "3 cross-references," the validator had declared 4 (`CN-B3.3` added in v3.2 alongside the pre-existing `US-BW3/4/5`). Now states 4 and names both.
- **Rebuilt `tools/probe_cn_b3.py`: three real bugs, not just missing coverage.** (1) The continuation-rate join used `fillna(False)`, silently counting names absent from day-1 data (delisted/suspended) as *failed* continuations rather than excluding them, contradicting the prose's own "eligible on both days" rule. Rewritten as an inner join that drops and reports them separately (`n_dropped_missing_day1`). (2) The script's single-day counts (79/56/23) never matched the document's cited 231/103/128, because that earlier figure came from an untracked ephemeral session on a different date. Reconciled: the document now cites the same 79/56/23/83 the saved script actually reproduces, and says so. (3) The script's docstring claimed a "CN-N7-collision check" that was never implemented, that was a one-time document-authoring check (grep for a duplicate ID), not a data probe; removed the false claim. Added `requirements.txt` and documented the exact interpreter/versions used (`/opt/anaconda3/bin/python3`, tushare 1.4.29, pandas 2.2.3) after a review reported `tushare` unimportable on a bare `python3`: confirmed importable on the environment actually used here, now stated explicitly rather than assumed portable.
- Counts unchanged: **370 rows / 366 unique** (this pass corrected existing rows and one script, added no new cards), `RESULT: PASS`.

### Change log, v3.2

**v3.2 (CN-B3 correctness pass, five confirmed errors fixed).** A review independently reproduced every v3.1 number and found five material errors in specification, not arithmetic. All five verified live before fixing (`tools/probe_cn_b3.py`, output saved to `tools/probe_cn_b3.log.json`):
- **`CN-B3.10` was wrongly defined as "locked-limit-down."** `Close = DownLimit` measures closing at limit-down, not being locked there all day, a name can trade normally and only hit the limit near the close. **Verified live:** `daily_basic.limit_status` (must be requested via explicit `fields=` or it's silently omitted) shows **81 names at `limit_status=5`** (ordinary limit-down) **and only 2 at `limit_status=6`** (一字/locked) on 2026-07-30, against 83 names in the `Close=DownLimit` reconstruction, confirming the two are almost the same population and neither is "locked." **`.10` renamed close-limit-down share; added `CN-B3.14`** built directly from `limit_status=6`, the genuinely locked measure. `CN-R5` (§11 parent table), which bundled both concepts into one row, is now marked as the **frozen composite of `.10`+`.14`**, not an independent bundle.
- **`CN-B3.9` continuation rate wrongly promoted to `S:F` in v3.1.** The arithmetic reproduces exactly (56→10, 17.9%), but this family's own board-conditioning mandate (`.5`/`.6`) was left unapplied to one pooled scalar. **Reverted to `S:C`** with the specific open items named: board split vs. explicit aggregation, previous-*trading*-day not calendar day, denominator-zero→`NA`, tick-integer price comparison (not float equality), a board/ST/regime-change rule, and an explicit suspension-treatment decision (excluding suspended names makes this conditional-on-tradability, which must be stated).
- **`.11`/`.12` field contracts were wrong, not just entitlement-gated.** `kpl_list` has **no reopening-count field**: only `open_time` (a timestamp, not a count), and **no `fd_amount` field**. Corrected: `.11` now cites **`limit_list_ths.open_num`** (verified via docs, but this endpoint needs **8,000 points**, above the register's 5,000-pt baseline, starts only 2023-11-01, and is **restricted to personal research use**, commercial use requiring separate 同花顺 licensing). `.12` now cites `kpl_list`'s actual queue fields (`limit_order`/`lu_limit_order`/`free_float`), with closing-vs-maximum-queue left as the genuinely open choice.
- **`CN-B3.3` was an undetected third vote.** It is the identical construct to `.7` (both "failed-limit rate"): retired as an explicit alias, added to the validator's `ALIASES` list alongside the existing `US-BW3/4/5` pattern (same formatting convention: not struck through, so it stays counted as a row and correctly excluded from the unique total).
- **Saved the missing evidence artifact.** Every prior "verified live" claim existed only in prose with no reproducible script. Added `tools/probe_cn_b3.py`: API calls, exact dates, join row counts, numerator/denominator, and raw error messages for denied endpoints, writing a dated JSON log. Not wired into CI; a dated artifact to re-run before citing a number in a future review, not an assumption that yesterday's counts hold today.
- Counts: **370 rows / 366 unique** (net: +1 `CN-B3.14`, `CN-B3.3` retained as a counted-but-aliased row matching the `US-BW*` convention), `RESULT: PASS`.

### Change log, v3.1

**v3.1 (CN-B3.9/.10 construction verified live).** Follow-up to the v3.0 feasibility check.
- **`CN-B3.9` continuation rate, construction frozen and promoted `S:C → S:F`.** A pure 2-day chain of the already-verified `.6` close-up flag: `Σ 1(CloseUp_t=1 ∧ CloseUp_{t−1}=1) / Σ 1(CloseUp_{t−1}=1)`, restricted to names eligible on both days. **Confirmed live** (2026-07-30→07-31): 56 closed limit-up day 0, 10 continued day 1, rate 17.9%. No new endpoint, same `stk_limit`+`daily` join as `.5`/`.6`.
- **`CN-B3.10` locked-limit-down, construction confirmed mechanically identical to `.5`/`.6`** (same join, down-limit side). Not separately re-tested live (limit-down was rare in the sampled window) but carries no new access risk.
- **`.11`/`.12` blockage upgraded from "untested" to "confirmed."** v3.0 said `kpl_list` was "documented at 5,000-pt but not tested here." Tested directly: **`kpl_list` and `kpl_concept` both return the identical access-denied error as `limit_list_d`.** This is a real entitlement gap on the account, not an assumption, worth a Tushare support ticket or checking whether a separate product code is required beyond the points balance.
- Counts unchanged: **369 rows / 366 unique**, `RESULT: PASS` (no rows added, this pass upgraded existing rows' readiness and formulas, not row count).

### Change log, v3.0

**v3.0 (sentiment-framework integration & limit-family expansion).** A review of a proposed sentiment architecture found ~70% overlap with existing register content, one genuine ID collision, and two data-feasibility errors I introduced, all fixed:
- **Fixed a real ID collision.** The proposed retail small-order card used `CN-N7`, already assigned to 龙虎榜 (§12b.5). Renamed to a new family, **`CN-RET1a/b`**.
- **Corrected `CN-RET1`'s data class `D:A → D:T`.** `moneyflow` requires ≥2,000 Tushare points, every A-share endpoint on this stack is entitlement-gated, none is public-free; this is the register's own §1.2 convention, misapplied in an earlier draft.
- **Relabelled the construct honestly.** "Small order" is a fixed-nominal-RMB-band + active-buy/sell inference, not verified retail identity, institutions split orders, retail submits large ones. Labelled **retail-skewed proxy**, never "retail flow." Added the secular comparability problem (fixed RMB thresholds drift in meaning as market cap grows) and the fix (rolling percentiles, residualize vs price/mcap/turnover).
- **[v3.4 correction: this 231/103/128 figure is CONFIRMED reproducible, it is the 2026-07-31 single-day count (a v3.3 reconciliation pass wrongly called it unreproducible because it queried the wrong date, 07-30; both dates' numbers are now in the saved probe log). Retracting the v3.3 "superseded" framing that briefly stood here.]** **The limit-event family was under-built and mis-scored.** v2.x had only `CN-B3.1-4`. **Verified live** (`stk_limit` up/down price joined to `daily` high/close: 231 touches, 103 closes, 128 broken boards on one sample date) that `TouchUp`/`CloseUp`/`BrokenBoardRate`/`SealSuccess`/`LockedLimitDown` are buildable **now**, contrary to an earlier claim that they were blocked. Added **`CN-B3.5-13`**, board-conditioned (pooling Main/ChiNext/STAR/BSE is invalid, different limit-band hit probabilities). `.7`/`.8` (broken-board / seal-success) are exact complements sharing one denominator, registered as **one primary + one derived readout**, not two votes. Reopening count and queue intensity (`.11`/`.12`) genuinely need `limit_list_d`/`kpl_list`; **confirmed `limit_list_d` is entitlement-blocked on this account despite Tushare's docs claiming 5,000-pt access**: `kpl_list` is untested, not assumed working. True seal duration (`.13`) needs minute/tick data and is `S:O`: `first_time`/`last_time` alone undercounts because a name can reopen between them.
- **`CN-B3.1-4` and the new `.5-13` changed from signed `Dir` to `state`/`diag`.** Limit heat is horizon-dependent, moderate heat can predict continuation, extreme heat can signal exhaustion, locked-limit-down is a liquidity/feasibility risk, not a return bet. A fixed sign at the raw-measure level baked in an assumption the data doesn't support; horizon-specific alpha is now a separate, pre-registered hypothesis that *consumes* these states.
- **Added §9c**: sector-sentiment sparse-count specification (a beta-binomial/shrinkage board-adjusted expected-count statistic for limit events, since z-scoring an 8-name sector is noise; continuous series keep the simple β-adjusted z-transform), and an honest **narrative/LLM outline** (`SENT-N1-7`, all `S:O`) replacing the prior `SENT-LLM1-7` mislabel, a research list is not a card set without corpus/timestamp/dedup/entity-map/prompt-version/formula/horizon/missingness/license/consumer specified per row. Two of the seven are **not new constructs**: fundamental/price-reaction mismatch = `MS-R9` (do not duplicate), narrative concentration extends `MS-R3`.
- **Corrected the Fear/Greed project cross-reference.** It is not a "validated composite", its own README shows the 25/75 timing rule **ties** a drawdown-matched benchmark; it's an implemented development benchmark whose incremental edge did not survive honest accounting. Its six legs materially overlap this framework (turnover→demand, margin→demand+fragility, momentum→trend, valuation→exuberance). Rule now stated: register its components as atomic indicators if they get IDs, register the composite as a benchmark/dashboard, **never consume both in the same allocation decision.**
- **No fourth sentiment composite was added.** `MS-R`'s three summary states already own "positioning fragility"; a proposed four-tier fast/medium/slow/fragility architecture would have substantially duplicated `MS-R` + existing breadth/limit/margin/IPO cards + the Fear/Greed project. §9c integrates the genuine gaps into the existing structure instead.
- Counts: **369 rows / 366 unique**, `RESULT: PASS`.

### Change log, v2.9

**v2.9 (validator honesty + remaining readiness/history fixes).** A review caught that v2.8's own "PASS" overclaimed and that I had retroactively rewritten the v2.7 changelog to match v2.8's card count (26→32 got backdated into the v2.7 entry). Both are the same failure mode as the register's earlier overclaims, one layer down, fixed without repeating it:
- **v2.7's changelog entry restored to what v2.7 actually did** (26 cards, not 32): history is not rewritten to match a later state; a note points forward to where the remaining atomization happened.
- **Validator's own docstring corrected to match its code.** It claimed a README-vs-title version check that did not exist: **now implemented** (exit 1 on mismatch) rather than either lie removed or check faked. A second claimed check (Eff-readiness ≤ Own-readiness propagation) was **attempted, found unreliable across the register's varying table shapes, and explicitly removed rather than shipped as a false-positive-prone stub**: the docstring says so and marks it human-review-only.
- **`S:O` outline exemption removed.** Outline rows must now carry explicit `D:U P:U` rather than a blank cell, a blank could silently hide an unassessed row and still pass. Applied to `F2-RNOA`/`F2-CRNOA`/`F2-OL`/`F6-NOAG`.
- **§9b heading version corrected** (said v2.7, now v2.8-era text updated).
- **Readiness propagation fixed on 6 cards** flagged as inheriting Own's readiness with no dependency discount: `MS-R3d` (needs a frozen thematic basket + factor construction, not raw prices), `MS-R4a` (public *access* to N-PORT/`fund_portfolio` is not a public *implementation* of the overlap construction, stays `D:L`), `MS-R10a/d/e` (inherit the momentum factor's PIT universe, `P5`/`P4`+`P9`), CoMomentum US leg (inherits `P5`, not bare `D:A P:N`).
- **`MS-R8a` split raw vs aggregated**, the stock-level Amihud cross-ref is genuinely `S:F`; its basket-weighted aggregation over a crowded basket is a separate card (`MS-R8a-agg`) that inherits the basket's formation dependencies and is `S:C`.
- **`MS-R6b` and `MS-R11a` split into explicit market adapters** (`R6b-US`/`R6b-CN`, `R11a-US`/`R11a-CN`) rather than one US-labelled card carrying a footnote: US short interest and CN margin-short balance are not economically identical and must not share one ID.
- **Owner-contract table rewritten for one-primary-target discipline** (MarketStructure v1.2→**v1.3**): every MS-R family previously listed 2–3 co-equal "primary" targets; now exactly one primary per family with the rest labelled secondary diagnostics that ride along but do not gate promotion (e.g. CoMomentum's primary is now the *tail-loss event*, not "return/vol/skew" as three targets). Added the explicit **MarketStructure-defines-primitive / PortfolioRisk-owns-book-state** boundary for `MS-R5` and `MS-R6c-own`, and a missing-data rule (**`UNKNOWN`, never a default-safe value**).
- **Two wording overclaims narrowed:** "CoMomentum needs only prices" → it avoids licensed holdings data but still needs a PIT universe, momentum sort, and (CN) PIT industry membership, the *lightest* dependency chain in the family, not a dependency-free one. "A-share HML-residual CoMomentum has no PIT history" → narrowed to *not backtestable from the current normalized data stack without reconstructing historical filings*, since the constraint is about the current stack, not a permanent impossibility.
- **`MS-R9` prose market-qualified**, was blanket `P:F`; corrected to US `P:P` / CN `P:F`, matching what its own table row already said.
- **README's stray double-bold marker fixed**; unique-count strings resynced. Counts: **358 rows / 355 unique** (net +3 for the R8a/R6b/R11a splits), `RESULT: PASS` under the corrected validator.

### Change log, v2.8

**v2.8 (MS-R integration-debt closure).** Fixed the consistency bugs a review caught in v2.7, all were stale-reference or overclaim, not new design:
- **Relationship map migrated to the new IDs**: it still named `MS-R6-CN`, linked `MS-R5/R7` to liquidity (now `MS-R8`) and `MS-R8` to CAR/SUE (now `MS-R9`), and said "all MS-R consumed once by Combination" (contradicting §9b.5). All five rows corrected; the Combination row now reads **PENDING**.
- **Remaining non-atomic cards split**: `MS-R3a`→a1/a2 (long/short legs), `MS-R7a`→a1/a2 (level/accel), `MS-R7b`→b1/b2 (level/change), `MS-R8d`→d1/d2 (depth/Kyle-λ), `MS-R11`→a/b (short-interest/days-to-cover). `MS-R6c` split **own-book vs licensed-external-AUM** (`c-own`/`c-mkt`), the external version is `D:L`, not `D:A`. 32 atomic cards now.
- **"Nothing is `S:F`" corrected to precise**, `MS-R8a` IS `S:F` (a cross-ref to the frozen `X-ILLIQ`); the true statement is "no newly-specified MS-R construction is frozen."
- **US effective readiness fixed**: CoMomentum and the basket-aggregated/breadth cards inherit `P5` (no free US survivorship-free universe); sector-HHI and theme-cosine inherit `P9`. v2.7 propagated only the A-share `P4`/`P9`.
- **`MS-R9` PIT made market-specific**, US `P:P` (EDGAR/price construction), CN `P:F`; v2.7 had `P:F` both. **`MS-R11` output `screen`→`cond`** (the family allows only state/cond/diag).
- **Owner contract added**: MarketStructure v1.2 now carries a **per-card MS-R2–R11 registration table** (target/sign/RG/status/rejection test), satisfying the "no indicator without an owning contract" rule; the changelog was not a substitute.
- **Source-basis line fixed**: it still said MarketStructure **v1.1**; now v1.2, with the divergence-log note that MS-R consumer wiring is a tracked PENDING task, not a divergence.
- **Validator deepened and its scope stated honestly**: v2.7's `tools/validate.py` only checked for an `S:` token, so "0 schema-incomplete" overclaimed. It now requires the **full S:/D:/P: triple** (exempting `S:O` outlines and F8 binaries, whose D/P are not yet determinate), detects **duplicate IDs**, **reconciles the master-index totals against the computed counts**, and **exits non-zero on any failure**, and the docstring now lists what it does *not* check (formula/inputs/clock/one-scalar semantics remain human review). Counts: **355 rows / 352 unique**, `RESULT: PASS`.
- **Build order** gained an MS-R step (specify CoMomentum first, then wire the summary states before other cards).

### Change log, v2.7

**v2.7 (MS-R honesty & atomization pass).** v2.6 was an overclaim, it marked crowding cards `S:F`, said the summary states were "consumed once by Combination" when **nothing consumes them**, bundled multiple scalars per ID, and cited a counting script that lived in `/tmp`, not the repo. All corrected:
- **§9b relabelled a REGISTERED RESEARCH OUTLINE.** Nothing is `S:F`; CoMomentum is `S:C` (formation cadence, min-weeks, weighting, A-share factor set all still open). The consumer states are **PENDING** (§9b.5): Combination/PortfolioRisk still reference only legacy `MS-R1`; wiring is an open cross-document task, now stated as such rather than claimed done.
- **Atomized 9 → 26 one-scalar cards.** `MS-R3`→R3a-d, `MS-R6`→R6a-c, `MS-R7`(liquidity)→R8a-d; added the missing **reversal-trigger** family (`MS-R10a-e`: the AND-gate's undefined leg), **short-leg squeeze/borrow** (`MS-R11`, cross-ref `MS-C1`/`US-S9`), and split every level/change and free/licensed leg. *(v2.7 left several of these still non-atomic (MS-R3a, MS-R6c, MS-R7a/b, MS-R8d, MS-R11) fully split in v2.8.)*
- **A-share forced-flow relabelled VULNERABILITY.** `MS-R7a/b` (两融/质押, cross-ref `CN-N2`/`CN-N5`) measure leverage *present*, not *liquidated*; true `ForcedFlow_CN` (`MS-R7c`) needs observable liquidation events → `S:O`.
- **AND-gate → tiered response** (§9b.4). A strict Boolean AND activates late or fails on a missing slow input; replaced with slow-structural→gradual-cap / fast-trigger→de-risk / liquidity-failure→execution-restriction / missing-data→"unknown-not-safe".
- **`PR-D4` claim corrected** from "identity of object" to "extends": ENB/residual-share exist there; momentum-RC and theme-cosine must be **added** to PortfolioRisk, not assumed present.
- **Readiness honesty:** `MS-R9` BadReactionBreadth is `S:R D:B P:F` (inherits `F5-SUE` `S:R`, needs forward-archived CAR), not a free A-share leg; `MS-R4` fragility is `S:O` (needs the Greenwood–Thesmar flow-covariance matrix, `G=W'ΩW/mcap²`); A-share cards show `Eff CN` bounded by `P4`/`P9`.
- **Validator saved to `tools/validate.py`**: counts, malformed-table check, and schema-incomplete (missing readiness triple) check; F8 binary components exempted (section-level readiness). Counts regenerated: **349 rows / 346 unique**. (Two RTI parent rows given explicit triples this pass.)
- **Sibling versions actually bumped:** MarketStructure v1.1→**v1.2** (title + README), its changelog corrected to say *outline/pending*, not *frozen/consumed*.

### Change log, v2.6

**v2.6 (crowding/leverage/forced-flow subfamily).** Added **§9b `MS-R`**: 9 cards for the measurable risk chain `crowding → forced selling → liquidity stress → factor crash`, prompted by the July-2026 momentum crash. **Every output is `risk`/`state`/`cond`/`diag`: a hard rule forbids any MS-R alpha sign**; the family feeds three summary states (`StructuralVulnerability` / `ForcedFlowPressure` / `LiquidityAbsorption`) consumed once by Combination as a cap. Anchor is **CoMomentum** (Lou–Polk), winner/loser legs kept separate; the A-share residual choice (market+size+industry, HML dropped) is now **forced by the §2.4 F1-EP finding**, accounting is `P:F`, so an HML-residual CoMomentum cannot be built PIT on history. Four refinements vs the source proposal: (1) each leg **split into a free-live and a licensed-slow leg** (CoMomentum free; Greenwood–Thesmar fragility/holdings needs N-PORT/`fund_portfolio`); (2) **book risk-contribution / effective-bets routed to `PR-D4`**, not duplicated as an MS card (book-dependent, already exists); (3) **forced-flow market-split**: US leveraged-ETF `L(L−1)A·r` + CTA scenario, A-share = existing `CN-N2` 两融 + `CN-N5` pledge; (4) **cross-refs** `X-ILLIQ`/`MS-I1`/`F5-CAR`/`F5-SUE` instead of parallel objects. Added a **percentile-reproducibility rule** (declare numerator/denominator/universe/frequency/window; quarterly ≈20 obs is too coarse for a "98th-percentile" claim; never forward-fill quarterly into "daily"). Added **article-number cautions**: the 92/98-percentile figures are proprietary; "leverage was retail not institutional" is **not identifiable** from public data (absence of observable institutional leverage ≠ its absence); "liquidity didn't withdraw" must be **tested** via `MS-R7`, not inferred from a flat index. Counts regenerated: **332 rows / 329 unique**. Not promoted (research-prose only): July seasonality, the −20%→+6% stat, anecdotes, exact bank flow numbers.

### Change log, v2.5

**v2.5 (integration pass).** Mostly fixing integration debt from v2.4's own fixes, improvements made in prose that never reached the rows.
**Counts now script-generated.** §12b was claimed at **39 against an actual 33**; the total (325) reconciled with neither. A parser now walks row IDs: **323 catalogued rows · 320 unique** net of three cross-references (`US-BW3/4/5` alias `US-CM1.1`/`US-CM2.1`/`US-CM3`: a Baker–Wurgler proxy that already exists under an issuance ID is not a new atomic output). Four consecutive versions had hand-maintained counts and all four were wrong.
**§0 regenerated against actual row state.** Removed `F8-PS` from T1 (it inherits `F8-FS`'s `S:C`), removed `US-R6b.2` from T2 (its row now correctly requires licensed TAQ/SIP), corrected the `F8-GS*` entry (the 5y/3y window is frozen, only the missing-data treatment is open), and marked `X-SIZE`/`X-ILLIQ` done in §0.7.
**Raw value vs ranked score separated.** A stock's raw momentum is causal with prices alone; a **cross-sectional rank additionally needs a PIT-eligible universe**. Every `TR-RANK` score is therefore one tier below its raw value, which is why `T-X1` can sit in T2 while its card shows `Eff D:P P:U`. That looked like a contradiction because two different outputs shared one row.
**T2 and T3a made independent axes.** v2.4 defined `T3a = T2 + clock`, misclassifying in both directions: a licensed real-time news feed can be live-production-ready with **no** historical archive, and a decommissioned archive can be backtest-causal but no longer producible.
**Data classes propagated to the primitives**, `P7-CN` `D:A → D:T` (CH3 is built from entitlement-gated Tushare inputs, which its own prose said), `P13`/`P14` split market-specific (`D:B` US / `D:T` CN, they are constructed spines, not feeds), `R-X5` `D:A → D:B/D:T`.
**New `CLK-RELEASE`** for scheduled macro/statistical releases: SLOOS was wrongly on `CLK-FILING`, which is a corporate-filing clock.
**Factual corrections in the new §12b cards.** **SLOOS `P:V → P:U`** (the Fed corrects observations and redefines series; `P:V` was unearned) and `S:C` until the exact series is pinned (C&I vs aggregate, firm-size cut, weighting). **ACM `P:N → P:U` and `Dir − → state`**. the term premium is a *model estimate*, revised on re-estimation, and a rising term premium can reflect discount rates, inflation risk *or* risk compensation. **Baker–Wurgler `Dir` clarified as sentiment-alignment, not return-direction** (v2.4 mixed both in one column), with the full reproducibility gap named and the academic-series-vs-live-reconstruction distinction added. **`MS-C2a` `D:P → D:B`**. SEC structured 13F data is public and as-filed from 2013; *coverage* is partial but that is not an *access* class. **`MS-C4a` `S:F → S:O`**: "timestamped negative news" is not frozen without a news universe, dedup policy, model version and aggregation window. **`X-SIZE-T/F` US feasibility corrected**, historical total shares need a build (`D:B`) and free-float shares are not a clean public series (`D:L`). **`X-ILLIQ` contradiction fixed** (`S:C (window)` while the formula pinned 252d) with currency scaling and suspension handling added; **`X-TURN` reframed as an inactive alpha *hypothesis***: CH-3 failing on turnover is a reason to test, not evidence that one 252-day formula is alpha.
**§12b.5 expanded to the mandatory schema** and split where one row held two outputs: `CN-N2a/b` (margin level vs change), `CN-N5a/b` (pledge level vs change). **`CN-N1b` given an actual scalar**: "top-ten presence" is list membership, not a signal; the declared output is net buy value over turnover, with inclusion-flag/gross-buy/gross-sell named as *different indicators*. **`CN-N6` scope declared** (董监高 + 控股股东, excluding 大宗交易 transfers and 股权激励 exercises, without the filter it measures paperwork).
**§12b relabelled REGISTRATIONS, not "full cards"**: they carry 5–12 of 14 fields. §12b.3/§12b.4 are left deliberately partial: a licensed series you cannot obtain does not earn a full field map.
**Mohanram wording corrected**: the source **assigns 0** on insufficient history; `NA` is a production adaptation, not an equally source-faithful reading. v2.4 presented them as two readings.
**Stale material cleared**: §18 marked mostly-cleared with the audit trail retained; build order now says CH3 needs *construction plus vintage audit*, not specification; the excluded table no longer implies CH3-dependent rows are unblocked (**specification-unblocked ≠ backtest-ready**); **P15's "no CN vendor archive" softened in the row and build order**, which v2.4's changelog claimed but only did in one place; **Financials v1.13 added to the source basis.**

### Change log, v2.4

**v2.4 (taxonomy propagation & source-faithful closure).**
**The six data classes are now actually applied.** v2.3 defined `PUBLIC-DIRECT`/`PUBLIC-BUILD`/`ACCOUNT-TIER`/`PARTIAL`/`LICENSED`/`UNAVAILABLE` and then left **233 `D:A` labels and zero `D:B`/`D:T`**. the taxonomy existed only in prose. Propagated section-wise: **every A-share row → `D:T`** (entitlement-gated, PIT-unvalidated, never "free"), **all fundamentals → `D:B`** (EDGAR XBRL and Tushare statements both require normalization), **filing/constituent-derived US parents → `D:B`**, **licensed rows → `D:L`**. Now `D:A 96 · D:B 61 · D:T 74 · D:P 80 · D:L 26 · D:U 3`.
**T1 gate corrected**, it admitted only `D:A/P`, excluding `D:B` and `D:T` (both compute today) while admitting `D:P` (current-only, which can *never* reach T2). **T3 split into `T3a` indicator-production and `T3b` strategy-execution**: a Treasury-curve state or the ACM term premium needs no survivorship-free equity universe, so requiring P4/P5 of them was a category error. Several macro/volatility states are **T3a-eligible now**.
**Piotroski–So corners were inverted.** v2.3 called high-B/M × high-F "congruent-value". **Both tradable legs are INCONGRUENT**: long incongruent-value (high B/M × **high** F), short incongruent-glamour (low B/M × **low** F); the *congruent* cells are high-B/M × low-F and low-B/M × high-F and show little spread. This inverted the paper's central construct. Also: `F8-PS` was `S:F` and listed in T1 while depending on `F8-FS`, which is `S:C`, **effective readiness corrected to `S:C`** by the register's own worst-of-dependencies rule.
**Mohanram's minimum history frozen**: the source specifies **5-year windows with a 3-year minimum**; that was never open. What *is* open is only the downstream treatment (source-faithful **0** vs production-conservative **NA** + coverage gating), which implementations genuinely read differently.
**Schema gap named rather than papered over.** §10/§11 carry **7 of 14 mandatory fields**; "percentile vs 5y", "rolling z" and "surprise" are under-specified without lookback, vintage, standardization population and minimum sample. Added `CLK` and `Info-ts` as mandatory fields, a block of **standing defaults** for the 181 parent rows, and an explicit statement that **for those rows the register does not yet meet its own mission**. `F5-CAR` now states three timestamps (event day 0 · signal complete after close +1 · **first execution day +2**); `CLK-CORPACTION` splits declaration/record/ex/payment.
**Counting rule added; counts regenerated.** §6.2 held 16 rows against an index claiming 14. Entries are now typed (primary/variant/component/composite/outline/backlog) and **"active" renamed "catalogued"**: much of the register is choice-open, licensed or outline-only, so the old label overstated it.
**§12b added, 39 registered-but-inactive cards.** Reference completeness and production activation are different things: the anti-zoo rule governs what enters the *portfolio*, not what gets *documented*. Promoted from backlog prose to full cards: **`X-SIZE-T` vs `X-SIZE-F`** (two objects, total ME for factor exposure/CH3, free-float for capacity and weighting; conflating them is a silent error, and the gap is large in A-shares), `X-ILLIQ`, **`X-TURN` reclassified `cond` → `alpha`** (CH-3 *fails* on turnover, which is where standalone alpha may live), `X-PRC`, `X-AGE`; **`US-M9.1/.2` SLOOS split into standards and demand** (a net measure destroys the information); **`US-M10.1–.4` ACM** term premium vs expected short rate; **all six Baker–Wurgler proxies**, of which CEF discount, NYSE turnover and dividend premium had **no ID anywhere**; limits-to-arbitrage with honest `LICENSED`/`PARTIAL` labels (13F is quarterly, ≤45d late, and **not** total institutional ownership); and A-share natives including **`CN-N1a/b/c` as three cards because the data generating process changed**: `CN-N1c` is history-only and describes a signal that no longer exists. **`CN-N4` unlock overhang finally has an owner** after being orphaned across three versions.
**Feasibility corrections:** GDPNow `P:F → D:B P:U` (vintage archive exists back to 2011Q3) · US/CN "quoted spread" needs TAQ/L2 → `D:L`, with the CN row renamed a **Roll/Corwin–Schultz estimator** · Cboe put/call → `D:P` (discontinuous history) · Investors Intelligence and EPFR → `D:L` · CN macro vintages: "no vendor archive exists" softened to **no verified standardized archive in the current stack**.

### Change log, v2.3

**v2.3 (external audit closure).** Eight priority-zero corrections; several were errors I introduced.
**CH3 (§2.1): two material fixes.** Shell value corrected **40% → ~30% (mean `S/V` = 29.5%)**: v2.2 quoted the **Jan-2018 working draft**, revised before JFE publication. And **CH3 is NOT PIT-clean**, its value factor consumes reported earnings, so it inherits the P8/P13 vintage problem; `P7-CN` moved `P:N → P:U`, which demotes A-share `R-X1`/`R-X3`/`T-X2` from backtest-causal to computable-only. Added that the 60/00/30 ticker set is the **source's legacy universe** (omits STAR/BSE) on a sample ending **2016**, so it is a *source-faithful legacy primary*, not automatically a live universe.
**Split-authority failures fixed, the register was less accurate than its own contract.** `F8-FS*` used `NI / avgAssets`; Piotroski uses **net income before extraordinary items over BEGINNING-of-year assets**, which the Fundamental contract already had right, corrected, with the average-assets version demoted to a named harmonized variant, plus the high-B/M population and 8–9 vs 0–1 comparison. `F8-PS` was marked "undeclared `S:C`" while the contract already **froze** the 3×3 (B/M <30th / 30–70th / >70th × F-Score 0–3 / 4–6 / 7–9), now `S:F`. `F8-GS*` gained its missing source-faithful population (lowest B/M quintile, two-digit-SIC medians *within* it, beginning assets, 5y windows).
**§0 regenerated and re-scoped.** v2.2's counts were fabricated (claimed 34, listed 60; claimed 38, listed 40) and the filter used **owner** rather than **effective** readiness, so `S:C` rows appeared ready. Replaced with **three ordered gates: T1 computable / T2 backtest-causal / T3 production**, and the explicit finding that **nothing is T3 today**.
**Direction errors.** **`US-S9` was backwards**: informed shorts mean high short interest predicts *lower* returns → `Dir −` on raw SI. `CN-M2.1–.4` policy rows re-expressed as **easing-signed** (`−Δrate`). **`CN-B3.4` flagged as economically undefined**: a weighted z-sum across `涨停家数`(−)/`连板高度`(−)/`炸板率`(+) without sign alignment. `CN-CM-S.3` redefined as **listing speed** (inverse duration). Haven/flow rows (`US-X4.*`, `CN-X2.*`, `CN-M5b`, `CN-F1.1`, `CN-F2`, `CN-F4`) relabelled regime-conditional, bonds stop hedging equities under inflation shocks.
**Canonical names vs actual formulas.** `F2-GPA`/`F2-OPA` carried canonical names on harmonized formulas. Added **`F2-GPA-NM`** (Novy-Marx: `(Rev − COGS)/TotalAssets`, not averaged) and **`F2-OP-FF`** (Fama–French: `(Rev − COGS − SG&A − Interest)/BookEquity`); the averaged versions stay, renamed harmonized, and **must not be reported under the source authors' grades**.
**`P1` → a six-clock family (§2.2).** One universal close→next-open rule was wrong for pre-open, intraday, filing-timestamp, weekly and corporate-action information.
**Data labels → six operational classes** (`PUBLIC-DIRECT` / `PUBLIC-BUILD` / `ACCOUNT-TIER` / `PARTIAL` / `LICENSED` / `UNAVAILABLE`). `D:A` had merged "clean downloadable series" with "raw disclosures you must normalize." Consequence: A-share rows are **`ACCOUNT-TIER`, not free**; US fundamentals are **`PUBLIC-BUILD`, not `PUBLIC-DIRECT`**.
**Completeness, the "no missing top-level mechanism" claim was too strong and is narrowed.** Added **`US-M9` SLOOS** (credit *supply*, the register had price and conditions but no quantity channel) and **`US-M10.*` ACM term-premium decomposition** (the curve was one undifferentiated slope), both free. Noted that **three of Baker–Wurgler's six proxies** (CEF discount, NYSE turnover, dividend premium) have no ID anywhere. **`CN-N1` northbound carries a hard frequency break**: real-time disclosure ended 13 May 2024 and security-level holdings went **daily → quarterly on 19 Aug 2024**, so the daily history describes a signal that no longer exists.

### Change log, v2.2

**v2.2 (verification & completeness audit).** Self-review against primary sources.
**`P7-CN` CH3 SOLVED, the register's declared top blocker.** Full construction extracted from Liu–Stambaugh–Yuan and written as **§2.1**: exclude the bottom 30% by size (shell contamination, 83% of reverse mergers, ~40% of a typical bottom-30% stock's value, only 7% of total cap), plus listed<6m and trading-record minimums; ME uses **total shares incl. non-tradable**; EP uses **扣非** annualized net profit over *previous* month's ME; independent 2×3 sort (median ME × 30/40/30 EP) → six VW portfolios → `SMB`/`VMG`; **`MKT` in excess of the ONE-YEAR DEPOSIT RATE** (v2.1 wrongly said repo/SHIBOR). `R-X1`, `R-X3`, `T-X2` promoted `S:O → S:C` for A-shares. Added the warning that **the CH3 factor universe ≠ the P4 signal universe**, and that LSY document CH-3 **failing** on parts of the reversal and turnover categories.
**Three verification-queue items cleared.** `F2-COP` → `S:F` (Ball–Gerakos–Linnainmaa–Nikolaev: the six removed accrual accounts confirmed). `MS-C3a` → `S:F` (Hou–Moskowitz: **Wednesday-to-Wednesday** weekly returns, four lags, **D1 primary**, D2/D3 weighting `max[m−|m−n|,0]`, `m=4`; plus the evidence note that delay **captures the size effect and half the value premium**, so it must be ablated against size and value). `F8-FS*` components verified → `S:R → S:C` (only the tie/missingness rule remains open).
**§18 registration backlog added, the completeness audit's main finding.** Tier 1: five **canonical characteristics the register depends on but never defines**, most importantly **`X-SIZE`** (used by SMB, breakpoints, peer baskets and every neutralization, with no ID) and **`X-ILLIQ`** (index-level only today, though MS-I1's cost model needs it per name). Tier 2: **eight A-share-native datasets already reachable at 5,000 points and entirely absent**: northbound holdings, stock-level margin, holder count, unlock overhang (currently **orphaned**: §6.4 says 解禁 is not NSI and then gives it no owner), pledge ratio, stock-level insider trades, 龙虎榜, block trades. Tier 3: NOA level, R&D intensity, earnings persistence. **All staged as NOT-ACTIVE pending contract registration** (§17 forbids this register from originating indicators), with an explicit warning against registering all eight CN items. §18.4 records what the audit found **not** missing, so the list is bounded.

### Change log, v2.1

**v2.1 (determinism pass).**
**Dependency semantics fixed**: `Own` vs `Eff` columns, with `Eff` propagating only over **value** dependencies; **P1/P3 reclassified as execution primitives** so an unpinned VWAP choice no longer downgrades an accounting ratio. **P6/R-X1 circularity resolved**: P6 is now the residual-regression *engine* (consumes P2+P7, emits `ε`); R-X1 consumes it. **R-X7 corrected**: its primary is the peer-basket regression, so CH3 does not gate it; its real blocker is P9. **Fundamental PIT split applied per row** (US `P:P` / CN `P:U`) instead of prose only.
**Two formula errors fixed.** `F2-COP` had a **dimensional error** (subtracting a scaled ratio from a currency amount), replaced with the currency-unit working-capital accrual form, `S:R`. `F6-q5`'s `Cop` wording **double-added R&D**: corrected to `REVT − COGS − XSGA + XRD − …`, where `XSGA` is as-reported (embedding R&D) and `+XRD` reverses it exactly once.
**Clock indexing repaired.** Introduced the **`m0` formation-month convention** (§1.3) and reindexed `T-X2`, `T-X4`, `T-X4v` and **`T-X8`** (whose lags become 23/35/47/59, since the source targets the *held* calendar month).
**`Dir` column added** to separate raw→score direction from portfolio role, the F4 penalties in particular carry **opposite raw directions** (`tail−` for leverage, `+inv` for coverage and current ratio); parent sentiment rows likewise (`US-S7`/`US-S9` are informed-positioning `+`, not contrarian).
**P12 replaced by the §1.5 named-transform menu** (`TR-RANK`/`TR-Z`/`TR-SECRANK`/`TR-BINARY`/`TR-TAIL`/`TR-STATE`/`TR-EVENTZ`/`TR-NONE`); breakpoint population and neutralization method are declared separately.
**Parent tables atomized**: 100 family rows → **181 atomic entries**; `US-R2b` (relocated to `US-VRP2`) and `US-R9` (retired identifier) removed rather than carried as empty placeholders. Counts recomputed: **284 active entries** (§3 is regenerated from the tables, not estimated).
**Macro PIT statuses corrected**, `P:N` now reserved for market-observable non-revised series; statistical-agency output is `P:U` and nowcasts `P:F`, with **P15 macro vintage spine** added as a primitive (**CN `D:U`**. no *verified standardized* free archive in the current stack; commercial options unvalidated).
**Relationship map retyped**: `=` reserved for algebraic identity; four v2.0 claims corrected (`F7-DBNETIS` is a distinct channel not an alt-estimator; the three ΔROE variables are a correlated family not an identity; R-X7's primary is not IVOL; `adjRet9` is not T-X2).
**§0 ready-now view added**: the filtered answer to the original question, with formula-ready/PIT-clean, PIT-unverified, one-choice-blocked, demo-only, licensed and verification-queue lists.

---

## 18. Registration backlog: **mostly CLEARED in v2.4/v2.5**

> **⚠ Status update.** Everything in §18.1 (size, illiquidity, turnover, age, price), §18.2b (SLOOS, ACM, Baker–Wurgler) and most of §18.2 (northbound, margin, unlocks, pledge, insiders) has been **promoted to registrations in §12b**. The sections below are retained as the **audit trail of how the gaps were found**, not as an open to-do list. Still genuinely open: `CN-N3` (股东户数), `CN-N7` (龙虎榜), `CN-N8` (大宗交易), and all of §18.3.

## 18-audit. Registration backlog: **gaps found in the v2.2 completeness audit**

**Status: NOT ACTIVE.** §17 forbids this register from originating indicators. Every item below is a **documented gap requiring registration in its owning contract first** (ID, sign, RG, target, PIT contract, promotion test). They are listed here because omitting them from an *A-share-first* platform is a substantive coverage defect, not because they are approved.

**Data-feasibility legend:** ✅ free at your live tier · 💲 paid · 🔨 free but you build it.

### 18.1 Tier 1, canonical characteristics the register uses but never registers

These are not new factors. They are foundational quantities the register **already depends on implicitly** (breakpoints, peer baskets, neutralization, CH3 itself) while never defining them as objects. That is a structural hole.

| Proposed ID | Name | Formula | Why it cannot be missing | Data | Owner contract |
|---|---|---|---|---|---|
| **X-SIZE** | Log market equity | `ln(ME)`, ME = price × total shares **incl. non-tradable** (CH3 convention) | **The single most-used characteristic in the cross-section.** SMB is built on it, P4/P5 breakpoints use it, R-X7's peer basket buckets on it, every stage-2 neutralization controls for it, and it has no ID. In China it is also the *dominant* raw anomaly, and LSY show the bottom 30% is **shell-value contaminated**, which is a modelling decision, not a footnote. | ✅ `daily_basic.total_mv` | StatRisk or a new characteristics child |
| **X-ILLIQ** | Amihud illiquidity | `mean(abs(r_d) / turnover_value_d)` over a declared window | LSY list **illiquidity** as one of nine A-share anomaly categories. The register has Amihud at **index** level (`US-R6b.1`, `CN-R4b.1`) but **not at stock level**, even though MS-I1's cost model needs exactly this. | ✅ `daily` | MarketStructure (MS-I1 adjacent) |
| **X-TURN** | Turnover as standalone alpha | mean daily turnover, declared window | The register carries turnover only as a **conditioner** (`T-X6a/b`). But LSY find **CH-3 fails to explain the turnover category**: a factor model's failure is precisely where standalone alpha may live. Demoting it to conditioner-only pre-judges that. | ✅ `daily_basic.turnover_rate` | TrendReversal or StatRisk |
| **X-AGE** | Listing age | months since IPO | Used as an *exclusion* (IPO<6m) but never as a characteristic. Young A-share listings behave differently (lockup, index-inclusion, retail attention). | ✅ `stock_basic.list_date` | MarketStructure |
| **X-PRC** | Nominal price level | `ln(price)` | Low-price lottery demand is well documented and **especially strong in A-shares**; overlaps R-X4 MAX but is not the same object. | ✅ `daily` | StatRisk (`LOTTERY` RG) |

### 18.2 Tier 2: **A-share-native data you already pay for and do not use**

This is the largest single gap relative to the platform's stated **A-share-first** mission. The register's cross-sectional layer is almost entirely translated US literature. Every endpoint below needs **2,000 points; you hold 5,000.**

| Proposed ID | Name | Signal content | Endpoint | Data |
|---|---|---|---|---|
| **CN-N1** | Northbound (陆股通) holdings | foreign-institutional holding share and its change. **⚠ STRUCTURAL BREAK. See note below.** | `hk_hold` (2,000 pt) | `ACCOUNT-TIER`, **frequency break** |
| **CN-N2** | Stock-level margin balance | 融资余额 per name / float: name-level leverage and speculative intensity. The register has this only at **index** level (`CN-B4.*`). | `margin_detail` (2,000 pt) | ✅ |
| **CN-N3** | 股东户数 (holder count) | change in shareholder count = retail dispersion vs concentration; a widely-used A-share crowding proxy | `stk_holdernumber` | ✅ |
| **CN-N4** | 限售解禁 overhang | upcoming unlock value / float: the register explicitly says 解禁 "is a supply variable, **NOT** NSI" (§6.4) and then **never gives it an owner**. It is currently orphaned. | `share_float` | ✅ |
| **CN-N5** | 股权质押 (pledge ratio) | pledged shares / total: an **A-share-specific tail risk** with no US analogue (cf. the 2018 pledge unwind cascade). F4's distress rows miss it entirely. | `pledge_stat` | ✅ |
| **CN-N6** | 股东增减持 (insider trades) | net insider buy/sell at **stock** level. The register has the US analogue (`US-S7`) only at **index** level and has **no CN stock-level counterpart**. | `stk_holdertrade` (2,000 pt) | ✅ |
| **CN-N7** | 龙虎榜 (dragon-tiger list) | speculative attention / 游资 participation | `top_list`, `top_inst` | ✅ |
| **CN-N8** | 大宗交易 (block trades) | discount and volume: institutional repositioning | `block_trade` | ✅ |

**⚠ `CN-N1` northbound, a hard frequency break, not a data gap (v2.3).** The exchanges ended **real-time** northbound disclosure on **13 May 2024**, and from **19 Aug 2024** individual-security holdings moved from **daily to QUARTERLY** (published on the fifth Connect trading day after quarter-end). Daily disclosure now covers only aggregate turnover and the **top-ten most-active securities**. So the series is **daily up to Aug 2024, quarterly thereafter**: a backtest trained on the daily history describes a signal that **no longer exists at that frequency**. This is the same class of hazard as the 2024 国九条 break in `F7`, and it must be regime-dated the same way. A live northbound signal must be rebuilt on either the quarterly panel or the daily top-ten list, different objects, each needing its own card.

**⚠ Do not register all eight.** That would be exactly the factor-zoo behaviour the suite forbids. `CN-N1`, `CN-N2`, `CN-N5` and `CN-N4` have the clearest independent economic mechanisms (foreign flow, name-level leverage, pledge tail risk, supply overhang). `CN-N6`/`N7`/`N8` overlap the existing `SPEC-HEAT` and `FLOW` groups and must be ablated against them **before** any of them earns an ID.

### 18.2b Tier 2b: **free US macro/sentiment families that are economically distinct and simply absent**

| Proposed ID | Name | Why it is not covered by an existing row | Data |
|---|---|---|---|
| **US-M9** | **SLOOS credit supply**: net % of banks tightening C&I standards; loan demand as a separate series | The register has *price* of credit (`US-M2.*` OAS) and *conditions* (`US-M4.*` NFCI) but **no quantity/supply-side credit channel**. Bank willingness to lend is a distinct transmission mechanism and is economically upstream of spreads. Quarterly. | ✅ `PUBLIC-DIRECT` (Federal Reserve SLOOS) |
| **US-M10.1/.2** | **ACM term-premium decomposition**: term premium and expected-short-rate components of the 10y | `US-M1.*` treats the curve as one undifferentiated slope, and `US-M8.*` splits only real vs breakeven. A slope steepening driven by term premium is a different economic event from one driven by expected policy: the register currently cannot tell them apart. | ✅ `PUBLIC-DIRECT` (NY Fed, daily) |

**Baker–Wurgler sentiment, the six proxies belong in the register, not only in the research contract.** The US parent carries a Baker–Wurgler *sleeve*, but the implementation reference only atomizes the issuance legs (`US-CM1.*`–`US-CM5.*`). The full six-proxy map is: **closed-end-fund discount · NYSE turnover · IPO count · IPO first-day return · equity share of new issues · dividend premium.** Three of the six (`CEF discount`, `NYSE turnover`, `dividend premium`) have **no ID anywhere in this register**. Listing them is completeness, not activation: `PUBLIC-BUILD` for the dividend premium and turnover legs, `LICENSED` for clean historical CEF discounts.

### 18.3 Tier 3, canonical US anomalies absent or blocked

| Proposed ID | Name | Note | Data |
|---|---|---|---|
| **F6-NOA** | Net operating assets **level** (Hirshleifer et al. 2004) | A strong US anomaly in its own right; the register has only NOA *growth* (`F6-NOAG`), and that is `S:O` on the unfixed NOA contract. Both unblock together. | ✅ (blocked by NOA field contract) |
| **F2-RDI** | R&D intensity | Exists only buried inside `F8-GS6`. R&D-to-market is a standalone documented anomaly. **CN disclosure is inconsistent** → `D:P`. | 🔨 |
| **F3-EPERS** | Earnings persistence / smoothness | AR(1) of earnings; quality dimension not covered by accruals or level profitability | ✅ |

### 18.4 Scope of the completeness claim: **narrowed in v2.3**

v2.2 claimed "no missing top-level mechanism." **That was too strong**, and §18.2b is the counter-example: credit *supply* and term-premium *decomposition* are top-level macro mechanisms that were genuinely absent, and three of Baker–Wurgler's six sentiment proxies have no ID at all.

The defensible claim is narrower: **within the cross-sectional equity return-mechanism space**: value, profitability, investment, capital allocation, momentum, reversal, seasonality, lottery/volatility, defensive beta, earnings events, the architecture is complete, and measured against a 150+ characteristic library like JKP you do **not** need another hundred anomalies. The gaps are concentrated in four places: **(a)** characteristics used-but-unregistered (§18.1), **(b)** A-share-native datasets (§18.2), **(c)** macro/sentiment mechanisms (§18.2b), **(d)** limits-to-arbitrage, most of which is licensed. Replication work (Hou–Xue–Zhang) is also a standing warning against treating every published friction variable as deployable alpha, breadth here is not the binding constraint; **causal data is.**
