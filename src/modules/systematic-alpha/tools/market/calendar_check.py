"""
Calendar Check Tool

Checks for earnings announcement conflicts with option expiration dates.
Helps avoid volatility risk around earnings events.
"""

from typing import Dict, Union
from datetime import datetime, timedelta
import warnings

try:
    from .market_data_mock import get_earnings_date
    LOCAL_IMPORT = True
except ImportError:
    try:
        from market_data_mock import get_earnings_date
        LOCAL_IMPORT = True
    except ImportError:
        LOCAL_IMPORT = False
        warnings.warn(
            "Could not import get_earnings_date. "
            "Earnings conflict checking will use mock data only.",
            UserWarning
        )


def check_earnings_conflict(
    ticker: str,
    expiration_date: Union[str, datetime],
    buffer_days: int = 7,
    use_mock: bool = False
) -> Dict:
    """
    Check if an option expiration date conflicts with an earnings announcement.

    Trading options around earnings is risky due to volatility. This function
    identifies potential conflicts to help avoid earnings-related risk.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        expiration_date: Option expiration date (ISO string 'YYYY-MM-DD' or datetime)
        buffer_days: Number of days before/after earnings to flag as conflict (default: 7)
        use_mock: Force use of mock earnings data

    Returns:
        Dictionary containing:
        - ticker: Stock ticker symbol
        - expiration_date: Option expiration date (ISO format)
        - earnings_date: Next earnings date (ISO format) or None if not found
        - has_conflict: Boolean indicating if there's a conflict
        - days_between: Days between expiration and earnings (negative if earnings is before)
        - warning: Warning message if conflict exists, otherwise None
        - severity: 'high', 'medium', 'low', or None based on conflict timing
        - recommendation: Suggested action

    Raises:
        ValueError: If inputs are invalid

    Example:
        >>> result = check_earnings_conflict('AAPL', '2024-01-19')
        >>> if result['has_conflict']:
        >>>     print(result['warning'])
        >>>     print(result['recommendation'])
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")

    ticker = ticker.upper().strip()

    # Parse expiration date
    if isinstance(expiration_date, str):
        try:
            exp_date = datetime.strptime(expiration_date.strip(), '%Y-%m-%d').date()
        except ValueError as e:
            raise ValueError(
                f"Invalid expiration_date format. Expected 'YYYY-MM-DD', got '{expiration_date}'"
            ) from e
    elif isinstance(expiration_date, datetime):
        exp_date = expiration_date.date()
    else:
        raise ValueError(
            f"expiration_date must be string or datetime, got {type(expiration_date)}"
        )

    # Validate buffer days
    if not isinstance(buffer_days, int) or buffer_days < 0:
        raise ValueError(f"buffer_days must be non-negative integer, got {buffer_days}")

    # Get earnings date
    try:
        if LOCAL_IMPORT:
            earnings_info = get_earnings_date(ticker, use_mock=use_mock)
        else:
            # Fallback mock implementation if import failed
            earnings_info = _fallback_earnings_date(ticker)

        earnings_date_str = earnings_info.get('next_earnings_date')

        if not earnings_date_str:
            # No earnings date available
            return {
                'ticker': ticker,
                'expiration_date': exp_date.strftime('%Y-%m-%d'),
                'earnings_date': None,
                'has_conflict': False,
                'days_between': None,
                'warning': None,
                'severity': None,
                'recommendation': 'No earnings date found. Proceed with caution.',
                'data_source': earnings_info.get('data_source', 'unknown')
            }

        # Parse earnings date
        earnings_date = datetime.strptime(earnings_date_str, '%Y-%m-%d').date()

        # Calculate days between dates
        days_between = (earnings_date - exp_date).days

        # Check for conflict (earnings within buffer window of expiration)
        has_conflict = abs(days_between) <= buffer_days

        # Determine severity and generate warning
        severity = None
        warning = None
        recommendation = None

        if has_conflict:
            if abs(days_between) <= 2:
                severity = 'high'
                warning = (
                    f"HIGH RISK: Earnings on {earnings_date_str} is within {abs(days_between)} "
                    f"day(s) of expiration {exp_date.strftime('%Y-%m-%d')}"
                )
                recommendation = (
                    "AVOID: Choose different expiration date or avoid this trade. "
                    "Extreme volatility expected around earnings."
                )
            elif abs(days_between) <= 5:
                severity = 'medium'
                warning = (
                    f"MODERATE RISK: Earnings on {earnings_date_str} is within {abs(days_between)} "
                    f"days of expiration {exp_date.strftime('%Y-%m-%d')}"
                )
                recommendation = (
                    "CAUTION: Consider different expiration date. "
                    "Earnings volatility may impact position."
                )
            else:
                severity = 'low'
                warning = (
                    f"LOW RISK: Earnings on {earnings_date_str} is {abs(days_between)} "
                    f"days from expiration {exp_date.strftime('%Y-%m-%d')}"
                )
                recommendation = (
                    "MONITOR: Earnings is within buffer window. "
                    "Monitor position closely for volatility."
                )
        else:
            # No conflict
            if days_between > 0:
                recommendation = (
                    f"Clear: Expiration is {days_between} days before earnings. "
                    "No earnings conflict."
                )
            else:
                recommendation = (
                    f"Clear: Expiration is {abs(days_between)} days after earnings. "
                    "Earnings will have passed."
                )

        return {
            'ticker': ticker,
            'expiration_date': exp_date.strftime('%Y-%m-%d'),
            'earnings_date': earnings_date_str,
            'earnings_time': earnings_info.get('earnings_time', 'Unknown'),
            'has_conflict': has_conflict,
            'days_between': days_between,
            'abs_days_between': abs(days_between),
            'warning': warning,
            'severity': severity,
            'recommendation': recommendation,
            'buffer_days': buffer_days,
            'data_source': earnings_info.get('data_source', 'unknown')
        }

    except Exception as e:
        raise RuntimeError(f"Failed to check earnings conflict: {str(e)}") from e


def _fallback_earnings_date(ticker: str) -> Dict:
    """Fallback earnings date generator if imports fail."""
    ticker_hash = sum(ord(c) for c in ticker)
    days_ahead = 1 + (ticker_hash % 90)
    earnings_date = datetime.now().date() + timedelta(days=days_ahead)

    return {
        'ticker': ticker,
        'next_earnings_date': earnings_date.strftime('%Y-%m-%d'),
        'earnings_time': 'AMC' if ticker_hash % 2 == 0 else 'BMO',
        'data_source': 'fallback_mock'
    }


def get_safe_expirations(
    ticker: str,
    start_date: Union[str, datetime],
    num_expirations: int = 4,
    buffer_days: int = 7,
    use_mock: bool = False
) -> Dict:
    """
    Find option expirations that don't conflict with earnings.

    Analyzes standard monthly option expirations to identify safe dates.

    Args:
        ticker: Stock ticker symbol
        start_date: Starting date to search from (ISO string or datetime)
        num_expirations: Number of safe expirations to find (default: 4)
        buffer_days: Earnings buffer in days (default: 7)
        use_mock: Force use of mock earnings data

    Returns:
        Dictionary containing:
        - ticker: Stock ticker
        - safe_expirations: List of safe expiration dates
        - unsafe_expirations: List of expiration dates with conflicts
        - earnings_date: Next earnings date

    Example:
        >>> result = get_safe_expirations('AAPL', '2024-01-01')
        >>> print("Safe expirations:", result['safe_expirations'])
    """
    # Parse start date
    if isinstance(start_date, str):
        start = datetime.strptime(start_date.strip(), '%Y-%m-%d').date()
    elif isinstance(start_date, datetime):
        start = start_date.date()
    else:
        raise ValueError("start_date must be string or datetime")

    safe_expirations = []
    unsafe_expirations = []

    # Generate typical monthly option expirations (third Friday of each month)
    current_date = start
    checked = 0
    max_checks = 24  # Check up to 24 months

    while len(safe_expirations) < num_expirations and checked < max_checks:
        # Find third Friday of current month
        year = current_date.year
        month = current_date.month

        # First day of month
        first_day = datetime(year, month, 1).date()

        # Find first Friday
        days_until_friday = (4 - first_day.weekday()) % 7
        first_friday = first_day + timedelta(days=days_until_friday)

        # Third Friday
        third_friday = first_friday + timedelta(days=14)

        # Only consider if in the future
        if third_friday > start:
            # Check for earnings conflict
            result = check_earnings_conflict(
                ticker,
                third_friday.strftime('%Y-%m-%d'),
                buffer_days=buffer_days,
                use_mock=use_mock
            )

            if result['has_conflict']:
                unsafe_expirations.append({
                    'date': third_friday.strftime('%Y-%m-%d'),
                    'severity': result['severity'],
                    'warning': result['warning']
                })
            else:
                safe_expirations.append(third_friday.strftime('%Y-%m-%d'))

            checked += 1

        # Move to next month
        if month == 12:
            current_date = datetime(year + 1, 1, 1).date()
        else:
            current_date = datetime(year, month + 1, 1).date()

    # Get earnings info
    try:
        if LOCAL_IMPORT:
            earnings_info = get_earnings_date(ticker, use_mock=use_mock)
        else:
            earnings_info = _fallback_earnings_date(ticker)
    except:
        earnings_info = {'next_earnings_date': None}

    return {
        'ticker': ticker,
        'safe_expirations': safe_expirations,
        'unsafe_expirations': unsafe_expirations,
        'earnings_date': earnings_info.get('next_earnings_date'),
        'buffer_days': buffer_days
    }


if __name__ == "__main__":
    # Example usage and testing
    import sys

    print("Calendar Check Tool Test")
    print("=" * 70)

    test_cases = [
        {'ticker': 'AAPL', 'exp_date': '2024-02-16', 'desc': 'Feb monthly expiration'},
        {'ticker': 'TSLA', 'exp_date': '2024-03-15', 'desc': 'Mar monthly expiration'},
        {'ticker': 'NVDA', 'exp_date': '2024-04-19', 'desc': 'Apr monthly expiration'},
    ]

    print("\nEarnings Conflict Checks:")
    print("-" * 70)

    for test in test_cases:
        print(f"\n{test['ticker']} - {test['desc']}:")
        try:
            result = check_earnings_conflict(test['ticker'], test['exp_date'])
            print(f"  Expiration: {result['expiration_date']}")
            print(f"  Earnings: {result['earnings_date']} ({result.get('earnings_time', 'Unknown')})")
            print(f"  Conflict: {result['has_conflict']}")
            if result['has_conflict']:
                print(f"  Severity: {result['severity'].upper()}")
                print(f"  Warning: {result['warning']}")
            print(f"  Recommendation: {result['recommendation']}")
            print(f"  Data Source: {result['data_source']}")
        except Exception as e:
            print(f"  ERROR: {str(e)}")

    # Test safe expirations finder
    print("\n\nFinding Safe Expirations:")
    print("-" * 70)

    ticker = 'AAPL'
    print(f"\n{ticker} - Next 4 safe expirations:")
    try:
        result = get_safe_expirations(ticker, datetime.now(), num_expirations=4)
        print(f"  Earnings Date: {result['earnings_date']}")
        print(f"  Safe Expirations: {', '.join(result['safe_expirations'])}")
        if result['unsafe_expirations']:
            print(f"  Unsafe Expirations:")
            for unsafe in result['unsafe_expirations']:
                print(f"    - {unsafe['date']}: {unsafe['warning']}")
    except Exception as e:
        print(f"  ERROR: {str(e)}")
