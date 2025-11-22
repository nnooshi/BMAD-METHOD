"""
Systematic Alpha Tools

Collection of Python tools for systematic trading analysis.
"""

from .math.beta_calculator import calculate_beta
from .math.position_sizer import get_allocation, get_max_position_size
from .market.market_data_mock import get_liquidity_metrics, get_earnings_date
from .market.calendar_check import check_earnings_conflict, get_safe_expirations
from .utils.file_ops import (
    read_portfolio_csv,
    write_report,
    write_trade_order_json
)

__all__ = [
    # Math tools
    'calculate_beta',
    'get_allocation',
    'get_max_position_size',

    # Market tools
    'get_liquidity_metrics',
    'get_earnings_date',
    'check_earnings_conflict',
    'get_safe_expirations',

    # File operations
    'read_portfolio_csv',
    'write_report',
    'write_trade_order_json',
]
