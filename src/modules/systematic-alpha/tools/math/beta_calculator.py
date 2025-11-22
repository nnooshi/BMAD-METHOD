"""
Beta Calculator Tool

Calculates the beta coefficient for a given stock ticker against a benchmark index.
Beta measures the volatility of a stock relative to the market.
"""

from typing import Optional, Tuple
import warnings

try:
    import yfinance as yf
    import numpy as np
    from numpy.typing import NDArray
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None
    np = None
    NDArray = None


def calculate_beta(
    ticker: str,
    benchmark: str = 'SPY',
    period: str = '1y'
) -> Tuple[float, dict]:
    """
    Calculate the beta coefficient of a stock against a benchmark index.

    Beta is calculated using linear regression on daily returns:
    - Beta > 1: Stock is more volatile than the market
    - Beta = 1: Stock moves with the market
    - Beta < 1: Stock is less volatile than the market
    - Beta < 0: Stock moves inversely to the market

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        benchmark: Benchmark index ticker (default: 'SPY' for S&P 500)
        period: Historical data period (default: '1y')
                Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

    Returns:
        Tuple of (beta_value, metadata_dict) where metadata includes:
        - correlation: Correlation coefficient between stock and benchmark
        - r_squared: Coefficient of determination
        - stock_volatility: Annualized volatility of the stock
        - benchmark_volatility: Annualized volatility of the benchmark
        - data_points: Number of trading days used in calculation

    Raises:
        ImportError: If yfinance or numpy is not installed
        ValueError: If ticker data cannot be retrieved or insufficient data
        RuntimeError: If calculation fails

    Example:
        >>> beta, metadata = calculate_beta('AAPL', 'SPY')
        >>> print(f"AAPL Beta: {beta:.2f}")
        >>> print(f"Correlation: {metadata['correlation']:.2f}")
    """
    if not YFINANCE_AVAILABLE:
        raise ImportError(
            "yfinance and numpy are required for beta calculation. "
            "Install with: pip install yfinance numpy"
        )

    # Validate inputs
    ticker = ticker.upper().strip()
    benchmark = benchmark.upper().strip()

    if not ticker:
        raise ValueError("Ticker symbol cannot be empty")

    try:
        # Suppress yfinance warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Download historical data
            stock_data = yf.download(
                ticker,
                period=period,
                progress=False,
                show_errors=False
            )

            benchmark_data = yf.download(
                benchmark,
                period=period,
                progress=False,
                show_errors=False
            )

        # Validate data retrieval
        if stock_data.empty:
            raise ValueError(
                f"No data retrieved for ticker '{ticker}'. "
                "Please verify the ticker symbol is correct."
            )

        if benchmark_data.empty:
            raise ValueError(
                f"No data retrieved for benchmark '{benchmark}'. "
                "Please verify the benchmark symbol is correct."
            )

        # Extract adjusted close prices
        stock_prices = stock_data['Adj Close'] if 'Adj Close' in stock_data.columns else stock_data['Close']
        benchmark_prices = benchmark_data['Adj Close'] if 'Adj Close' in benchmark_data.columns else benchmark_data['Close']

        # Calculate daily returns (percentage change)
        stock_returns = stock_prices.pct_change().dropna()
        benchmark_returns = benchmark_prices.pct_change().dropna()

        # Align the data (ensure same dates)
        combined_returns = np.column_stack([
            stock_returns.values,
            benchmark_returns.reindex(stock_returns.index).values
        ])

        # Remove any rows with NaN values
        combined_returns = combined_returns[~np.isnan(combined_returns).any(axis=1)]

        if len(combined_returns) < 30:
            raise ValueError(
                f"Insufficient data for calculation. "
                f"Only {len(combined_returns)} valid trading days found. "
                "Minimum 30 days required for reliable beta calculation."
            )

        # Extract aligned returns
        stock_ret = combined_returns[:, 0]
        benchmark_ret = combined_returns[:, 1]

        # Calculate beta using linear regression (covariance method)
        covariance = np.cov(stock_ret, benchmark_ret)[0, 1]
        benchmark_variance = np.var(benchmark_ret)

        if benchmark_variance == 0:
            raise RuntimeError(
                "Benchmark variance is zero. Cannot calculate beta."
            )

        beta = covariance / benchmark_variance

        # Calculate additional metrics
        correlation = np.corrcoef(stock_ret, benchmark_ret)[0, 1]
        r_squared = correlation ** 2

        # Annualized volatility (assuming 252 trading days)
        stock_volatility = np.std(stock_ret) * np.sqrt(252)
        benchmark_volatility = np.std(benchmark_ret) * np.sqrt(252)

        metadata = {
            'correlation': float(correlation),
            'r_squared': float(r_squared),
            'stock_volatility': float(stock_volatility),
            'benchmark_volatility': float(benchmark_volatility),
            'data_points': len(combined_returns),
            'ticker': ticker,
            'benchmark': benchmark,
            'period': period
        }

        return float(beta), metadata

    except Exception as e:
        if isinstance(e, (ValueError, RuntimeError)):
            raise
        raise RuntimeError(f"Failed to calculate beta: {str(e)}") from e


if __name__ == "__main__":
    # Example usage and testing
    import sys

    if not YFINANCE_AVAILABLE:
        print("ERROR: yfinance not installed. Run: pip install yfinance numpy")
        sys.exit(1)

    # Test with a few popular stocks
    test_tickers = ['AAPL', 'TSLA', 'NVDA']

    print("Beta Calculator Test")
    print("=" * 60)

    for ticker in test_tickers:
        try:
            beta, metadata = calculate_beta(ticker)
            print(f"\n{ticker} vs SPY:")
            print(f"  Beta: {beta:.3f}")
            print(f"  Correlation: {metadata['correlation']:.3f}")
            print(f"  R-squared: {metadata['r_squared']:.3f}")
            print(f"  Stock Volatility: {metadata['stock_volatility']:.1%}")
            print(f"  Data Points: {metadata['data_points']}")
        except Exception as e:
            print(f"\n{ticker}: ERROR - {str(e)}")
