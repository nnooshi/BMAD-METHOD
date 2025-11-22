"""
Math Tools for Systematic Alpha

Provides mathematical calculations for trading analysis.
"""

from .beta_calculator import calculate_beta
from .position_sizer import get_allocation, get_max_position_size

__all__ = [
    'calculate_beta',
    'get_allocation',
    'get_max_position_size',
]
