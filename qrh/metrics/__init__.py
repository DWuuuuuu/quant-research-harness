"""Performance and risk metrics.

Each metric takes a NAV series and nothing else. Keeping them free of strategy
state lets the same suite run over every study.
"""

from qrh.metrics.performance import (
    annualised_volatility,
    cagr,
    drawdown_series,
    mar_ratio,
    max_drawdown,
    max_drawdown_duration,
    recovery_duration,
    sharpe_ratio,
    summary,
    total_return,
)

__all__ = [
    "annualised_volatility",
    "cagr",
    "drawdown_series",
    "mar_ratio",
    "max_drawdown",
    "max_drawdown_duration",
    "recovery_duration",
    "sharpe_ratio",
    "summary",
    "total_return",
]
