# quant-research-harness

A backtesting harness for long-only, cross-sectional equity strategies at
weekly to monthly rebalance frequencies, plus the indicator inventory it was
built to test.

[![tests](https://github.com/DWuuuuuu/quant-research-harness/actions/workflows/tests.yml/badge.svg)](https://github.com/DWuuuuuu/quant-research-harness/actions/workflows/tests.yml)

I wrote this because I kept re-implementing the same evaluation code per
strategy and getting results I could not compare. Every study here runs through
one engine and one metric suite, so a weak strategy looks weak next to a
stronger one instead of looking different.

## Contents

* `qrh/data` defines the data contract and three loaders (synthetic, Tushare,
  yfinance).
* `qrh/indicators` has momentum, dividend yield, earnings yield, inverse
  volatility, and z-scored blending.
* `qrh/backtest` is the engine and the cost model.
* `qrh/metrics` computes Sharpe, CAGR, MAR, maximum drawdown, drawdown
  duration, and recovery duration.
* `docs/indicators` is the research inventory: ten indicator modules across
  A-share and US markets plus a reference sheet, about 4,100 lines.
* `tests` has 51 tests. `examples` has three studies, one of which fails.

What it does not do: trading, order management, live data, short selling,
weight optimisation, or anything impact-aware. The default data is synthetic.
Nothing here is investment advice, and the tax rates are illustrative.

## Quickstart

No credentials and no vendor account needed. The default loader is synthetic
and seeded, so the numbers below reproduce exactly.

```bash
git clone https://github.com/DWuuuuuu/quant-research-harness
cd quant-research-harness
pip install -e ".[dev]"
pytest
python examples/01_single_factor_momentum.py
```

```python
from qrh import BacktestConfig, run_backtest, summary
from qrh.data import SyntheticLoader
from qrh.indicators import momentum

panel = SyntheticLoader().load([f"S{i:02d}" for i in range(24)], "2016-01-01", "2026-06-30")
result = run_backtest(panel, momentum, BacktestConfig(top_n=5, rebalance="ME"))
print(summary(result.nav))
```

For real data, set `TUSHARE_TOKEN` in your environment (see `.env.example`) and
change the loader:

```python
from qrh.data.tushare_loader import TushareLoader   # pip install tushare
panel = TushareLoader().load(["600036.SH", "601166.SH"], "2018-01-01", "2026-06-30")
```

## Three design decisions

**Signals cannot read the future.** The engine holds a `PanelData` object whose
only read method is `as_of(date)`, which slices up to and including that date.
Trades then execute at the next period's close. Writing a look-ahead bug takes
effort rather than inattention.

Two tests check this. One records the last date visible in every signal window
and requires it to precede the end of the sample. The other multiplies the
second half of the price history by five and requires NAV before the cutoff to
be unchanged, since any dependence on future data would move it.

**Costs are reported next to the strategy, not after it.** Turnover costs scale
linearly while edge per trade does not, so each study runs twice, once with
costs and once without. The A-share defaults carry the asymmetries that change
rankings: stamp duty applies to sales only, and dividend tax depends on holding
period (20% up to a month, 10% up to a year, nil after).

**Long only, equal weight.** Borrow cost, recall risk and squeeze exposure make
short legs a poor fit for a small account, and A-share retail shorting barely
exists. Equal weighting avoids a covariance estimate, which on a short sample
is mostly estimation error. Both constraints give up some efficiency and remove
a lot of ways to fool yourself.

## The studies

All three use the same seeded synthetic panel: 24 symbols, 2016-01-01 to
2026-06-30, 5 names held, 1,000,000 starting capital.

### 1. Momentum against its own turnover

`examples/01_single_factor_momentum.py`

|                   | CAGR % | Vol % | Sharpe | MaxDD % |  MAR | Cost drag |
|-------------------|-------:|------:|-------:|--------:|-----:|----------:|
| frictionless, ME  |   6.03 | 16.33 |   0.43 |  -31.76 | 0.19 |         0 |
| a-share costs, ME |   4.79 | 16.34 |   0.36 |  -32.97 | 0.15 |   137,418 |
| frictionless, QE  |   4.98 | 15.99 |   0.37 |  -36.22 | 0.14 |         0 |
| a-share costs, QE |   4.32 | 15.99 |   0.34 |  -36.64 | 0.12 |    69,889 |

Momentum survives costs but loses about a sixth of its Sharpe to them. Monthly
rebalancing costs roughly twice what quarterly does and returns about half a
point more per year. Recovery from the worst drawdown takes 400 periods, which
is the figure that decides whether anyone could hold it.

### 2. Blending yield with momentum

`examples/02_blended_factors.py`

| momentum / yield weight | CAGR % | Sharpe | MaxDD % |
|-------------------------|-------:|-------:|--------:|
| 0% / 100%               |   1.08 |   0.14 |  -39.73 |
| 25% / 75%               |   0.84 |   0.13 |  -40.66 |
| 50% / 50%               |   1.18 |   0.15 |  -36.15 |
| 75% / 25%               |   3.80 |   0.30 |  -35.39 |
| 100% / 0%               |   4.79 |   0.36 |  -32.97 |

The blend adds nothing. Sharpe rises monotonically with the momentum weight, so
the yield sleeve only dilutes. I report the sweep rather than the best cell
because a single strong interior weight surrounded by weak neighbours would
indicate sample-fitting, not a factor.

### 3. Short-horizon reversal, rejected

`examples/03_rejected_mean_reversion.py`

|                        | CAGR % | Sharpe | MaxDD % | Recovery | Cost drag |
|------------------------|-------:|-------:|--------:|---------:|----------:|
| weekly, frictionless   |   7.16 |   0.49 |  -31.01 |      550 |         0 |
| weekly, a-share costs  |  -5.26 |  -0.23 |  -61.06 |  *never* |   961,764 |
| monthly, frictionless  |   7.74 |   0.52 |  -30.25 |      601 |         0 |
| monthly, a-share costs |   4.67 |   0.35 |  -32.28 |     1188 |   368,745 |

Frictionless, weekly reversal has the highest Sharpe in this repository at 0.49.
With costs it returns -5.26% a year, roughly doubles its drawdown, and never
regains its high. Costs reach 961,764 against 1,000,000 of starting capital.

This study is here because a record that keeps only its successes tells a
reader nothing about how many attempts came first.

## The indicator inventory

`docs/indicators/` holds 11 files covering A-share and US timing,
cross-sectional fundamentals, financial-statement quality, market structure,
sector rotation, trend and reversal, statistical risk, portfolio risk, and
composite construction.

These are research contracts rather than code. Each indicator records an
availability lag, an evidence grade on three axes (empirical strength,
portability to the target market, point-in-time data readiness), a sign
hypothesis, and a rejection rule fixed before any backtest. Grades of C and D
are common. The inventory exists to stop an indicator reaching a live signal
without the work that would justify it, so most rows are hypotheses and none
claims to make money.

See [`docs/indicators/README.md`](docs/indicators/README.md) for the file map.

## Licensing and citation

| | License | |
|---|---|---|
| Code: `qrh/`, `tests/`, `examples/` | [MIT](LICENSE) | permissive reuse |
| Research: `docs/` | [CC BY 4.0](LICENSE-docs) | attribution required |

MIT would not have been enough for the research on its own. It asks only that a
copyright notice be kept, not that the work be credited. CC BY asks for
attribution.

`CITATION.cff` gives GitHub's "Cite this repository" button and BibTeX export:

> Wu, J. D. (2026). *quant-research-harness: a harness and falsifiable
> indicator inventory for cross-sectional equity research.* Version 0.1.0.
> https://github.com/DWuuuuuu/quant-research-harness

## Limitations

The synthetic generator exists for reproducibility. It has one common factor,
constant volatility, no regimes, no fat tails, and no correlation structure
beyond that factor. Results on it show the pipeline runs; they say nothing
about whether a strategy works.

Slippage is a flat rate per side. Scaling it with participation rate would need
volume data this harness does not carry.

There is no survivorship-bias handling. The synthetic universe is fixed, and a
real study needs point-in-time membership with delistings. That is the largest
remaining gap.

Sizing positions against post-cost capital leaves a residual of a few parts per
million in the weight sum. A test bounds it.

No vendor data is included. The caches my own work runs against are licensed
and not mine to redistribute, so the loaders fetch and the repository ships
code only.
