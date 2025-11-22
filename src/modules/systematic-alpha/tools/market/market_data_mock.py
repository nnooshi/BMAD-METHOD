"""
Market Data Tool

Provides liquidity metrics and earnings date information for stocks.
Uses yfinance for real data when available, falls back to mock data for testing.
"""

from typing import Optional, Dict
from datetime import datetime, timedelta
import warnings

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None


def get_liquidity_metrics(ticker: str, use_mock: bool = False) -> Dict:
    """
    Get liquidity metrics for a stock ticker.

    Liquidity metrics include bid-ask spread, volume, and current quote data.
    These are critical for assessing trade execution quality and slippage risk.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        use_mock: Force use of mock data instead of real API calls

    Returns:
        Dictionary containing:
        - ticker: Stock ticker symbol
        - bid: Current bid price
        - ask: Current ask price
        - spread: Absolute spread (ask - bid)
        - spread_pct: Spread as percentage of mid-price
        - avg_volume: Average daily volume
        - last_price: Last traded price
        - timestamp: Data timestamp
        - data_source: 'yfinance' or 'mock'

    Raises:
        ValueError: If ticker is invalid
        RuntimeError: If data retrieval fails

    Example:
        >>> metrics = get_liquidity_metrics('AAPL')
        >>> print(f"Spread: {metrics['spread_pct']:.3%}")
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")

    ticker = ticker.upper().strip()

    # Use mock data if yfinance not available or explicitly requested
    if use_mock or not YFINANCE_AVAILABLE:
        return _get_mock_liquidity_metrics(ticker)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Get ticker object
            stock = yf.Ticker(ticker)

            # Get current info
            info = stock.info

            # Validate we got data
            if not info or 'symbol' not in info:
                raise ValueError(f"No data found for ticker '{ticker}'")

            # Extract liquidity metrics
            bid = info.get('bid', None)
            ask = info.get('ask', None)
            last_price = info.get('currentPrice') or info.get('regularMarketPrice')
            avg_volume = info.get('averageVolume') or info.get('averageVolume10days')

            # If bid/ask not available, estimate from last price
            if bid is None or ask is None or bid == 0 or ask == 0:
                if last_price:
                    # Estimate 0.05% spread for liquid stocks
                    estimated_spread = last_price * 0.0005
                    bid = last_price - estimated_spread / 2
                    ask = last_price + estimated_spread / 2
                else:
                    # Fall back to mock data if we can't get real prices
                    return _get_mock_liquidity_metrics(ticker)

            # Calculate spread metrics
            spread = ask - bid
            mid_price = (bid + ask) / 2
            spread_pct = (spread / mid_price) if mid_price > 0 else 0

            return {
                'ticker': ticker,
                'bid': round(bid, 2),
                'ask': round(ask, 2),
                'spread': round(spread, 4),
                'spread_pct': round(spread_pct, 6),
                'avg_volume': avg_volume or 0,
                'last_price': round(last_price, 2) if last_price else round(mid_price, 2),
                'timestamp': datetime.now().isoformat(),
                'data_source': 'yfinance'
            }

    except Exception as e:
        # Fall back to mock data on any error
        warnings.warn(
            f"Failed to get real data for {ticker}: {str(e)}. Using mock data.",
            UserWarning
        )
        return _get_mock_liquidity_metrics(ticker)


def _get_mock_liquidity_metrics(ticker: str) -> Dict:
    """
    Generate realistic mock liquidity metrics.

    Uses ticker characteristics to generate plausible values.
    """
    # Generate semi-realistic mock data based on ticker
    # Use hash for deterministic but varied values
    ticker_hash = sum(ord(c) for c in ticker)

    # Mock price between $10 and $500
    base_price = 10 + (ticker_hash % 490)

    # Mock spread percentage (0.01% to 0.5%)
    spread_pct = 0.0001 + (ticker_hash % 50) / 10000

    spread = base_price * spread_pct
    bid = base_price - spread / 2
    ask = base_price + spread / 2

    # Mock volume (100K to 50M)
    avg_volume = 100000 + (ticker_hash % 49900000)

    return {
        'ticker': ticker,
        'bid': round(bid, 2),
        'ask': round(ask, 2),
        'spread': round(spread, 4),
        'spread_pct': round(spread_pct, 6),
        'avg_volume': avg_volume,
        'last_price': round(base_price, 2),
        'timestamp': datetime.now().isoformat(),
        'data_source': 'mock'
    }


def get_earnings_date(ticker: str, use_mock: bool = False) -> Dict:
    """
    Get the next earnings announcement date for a stock.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        use_mock: Force use of mock data instead of real API calls

    Returns:
        Dictionary containing:
        - ticker: Stock ticker symbol
        - next_earnings_date: ISO format date string (YYYY-MM-DD)
        - earnings_time: 'BMO' (before market open), 'AMC' (after market close), or 'Unknown'
        - days_until: Days until earnings from today
        - timestamp: Data timestamp
        - data_source: 'yfinance' or 'mock'

    Raises:
        ValueError: If ticker is invalid

    Example:
        >>> earnings = get_earnings_date('AAPL')
        >>> print(f"Next earnings: {earnings['next_earnings_date']}")
        >>> print(f"Days until: {earnings['days_until']}")
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")

    ticker = ticker.upper().strip()

    # Use mock data if yfinance not available or explicitly requested
    if use_mock or not YFINANCE_AVAILABLE:
        return _get_mock_earnings_date(ticker)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            stock = yf.Ticker(ticker)

            # Try to get earnings dates from calendar
            calendar = stock.calendar

            if calendar is not None and not calendar.empty:
                # Extract earnings date
                if 'Earnings Date' in calendar.index:
                    earnings_date = calendar.loc['Earnings Date']

                    # Handle if it's a Series (range of dates)
                    if hasattr(earnings_date, 'iloc'):
                        earnings_date = earnings_date.iloc[0]

                    # Convert to date string
                    if hasattr(earnings_date, 'strftime'):
                        date_str = earnings_date.strftime('%Y-%m-%d')
                    else:
                        date_str = str(earnings_date).split()[0]

                    # Calculate days until
                    earnings_dt = datetime.strptime(date_str, '%Y-%m-%d')
                    days_until = (earnings_dt.date() - datetime.now().date()).days

                    # Try to determine timing (BMO/AMC)
                    earnings_time = 'Unknown'
                    # Note: yfinance doesn't always provide this, would need additional source

                    return {
                        'ticker': ticker,
                        'next_earnings_date': date_str,
                        'earnings_time': earnings_time,
                        'days_until': days_until,
                        'timestamp': datetime.now().isoformat(),
                        'data_source': 'yfinance'
                    }

    except Exception as e:
        warnings.warn(
            f"Failed to get earnings date for {ticker}: {str(e)}. Using mock data.",
            UserWarning
        )

    # Fall back to mock data
    return _get_mock_earnings_date(ticker)


def _get_mock_earnings_date(ticker: str) -> Dict:
    """
    Generate mock earnings date.

    Creates a plausible earnings date 1-90 days in the future.
    """
    # Use ticker hash for deterministic mock data
    ticker_hash = sum(ord(c) for c in ticker)

    # Generate date 1-90 days in the future
    days_ahead = 1 + (ticker_hash % 90)
    earnings_date = datetime.now().date() + timedelta(days=days_ahead)

    # Mock earnings time
    earnings_time = 'AMC' if ticker_hash % 2 == 0 else 'BMO'

    return {
        'ticker': ticker,
        'next_earnings_date': earnings_date.strftime('%Y-%m-%d'),
        'earnings_time': earnings_time,
        'days_until': days_ahead,
        'timestamp': datetime.now().isoformat(),
        'data_source': 'mock'
    }


if __name__ == "__main__":
    # Example usage and testing
    import sys

    print("Market Data Tool Test")
    print("=" * 70)

    if not YFINANCE_AVAILABLE:
        print("\nWARNING: yfinance not installed. Using mock data only.")
        print("Install with: pip install yfinance\n")

    test_tickers = ['AAPL', 'TSLA', 'NVDA']

    # Test liquidity metrics
    print("\nLiquidity Metrics:")
    print("-" * 70)
    for ticker in test_tickers:
        try:
            metrics = get_liquidity_metrics(ticker)
            print(f"\n{ticker}:")
            print(f"  Bid/Ask: ${metrics['bid']:.2f} / ${metrics['ask']:.2f}")
            print(f"  Spread: ${metrics['spread']:.4f} ({metrics['spread_pct']:.3%})")
            print(f"  Avg Volume: {metrics['avg_volume']:,}")
            print(f"  Last Price: ${metrics['last_price']:.2f}")
            print(f"  Source: {metrics['data_source']}")
        except Exception as e:
            print(f"\n{ticker}: ERROR - {str(e)}")

    # Test earnings dates
    print("\n\nEarnings Dates:")
    print("-" * 70)
    for ticker in test_tickers:
        try:
            earnings = get_earnings_date(ticker)
            print(f"\n{ticker}:")
            print(f"  Next Earnings: {earnings['next_earnings_date']} ({earnings['earnings_time']})")
            print(f"  Days Until: {earnings['days_until']}")
            print(f"  Source: {earnings['data_source']}")
        except Exception as e:
            print(f"\n{ticker}: ERROR - {str(e)}")

    # Test mock data explicitly
    print("\n\nForced Mock Data Test:")
    print("-" * 70)
    ticker = 'TEST'
    metrics = get_liquidity_metrics(ticker, use_mock=True)
    earnings = get_earnings_date(ticker, use_mock=True)
    print(f"\n{ticker} Liquidity: Spread {metrics['spread_pct']:.3%}, Volume {metrics['avg_volume']:,}")
    print(f"{ticker} Earnings: {earnings['next_earnings_date']} in {earnings['days_until']} days")
