"""A backtesting harness for cross-sectional equity strategy research.

One engine and one metric suite run every study, so results are comparable
across strategies rather than each carrying its own evaluation code.
"""

__version__ = "0.1.0"

from qrh.backtest.engine import BacktestConfig, BacktestResult, run_backtest
from qrh.metrics.performance import summary

__all__ = ["BacktestConfig", "BacktestResult", "run_backtest", "summary", "__version__"]
