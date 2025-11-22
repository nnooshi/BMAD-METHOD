# Systematic Alpha Tools

Python tools for systematic options trading analysis and execution.

## Installation

Install required dependencies:

```bash
pip install -r ../requirements.txt
```

Or install individually:

```bash
pip install yfinance numpy
```

## Module Structure

```
tools/
├── math/
│   ├── beta_calculator.py    # Beta calculation using linear regression
│   └── position_sizer.py     # Position sizing based on risk buckets
├── market/
│   ├── market_data_mock.py   # Liquidity metrics and earnings dates
│   └── calendar_check.py     # Earnings conflict detection
└── utils/
    └── file_ops.py           # File I/O operations
```

## Tools Overview

### Math Tools

#### 1. Beta Calculator (`math/beta_calculator.py`)

Calculate the beta coefficient of a stock against a benchmark index.

```python
from tools.math.beta_calculator import calculate_beta

# Calculate beta for AAPL vs SPY
beta, metadata = calculate_beta('AAPL', 'SPY')
print(f"Beta: {beta:.3f}")
print(f"Correlation: {metadata['correlation']:.3f}")
print(f"R-squared: {metadata['r_squared']:.3f}")
```

**Function:** `calculate_beta(ticker, benchmark='SPY', period='1y')`

**Returns:**
- `beta`: Float representing the beta coefficient
- `metadata`: Dictionary with correlation, r_squared, volatilities, and data points

**Features:**
- Uses yfinance for historical data
- Linear regression on daily returns
- Annualized volatility calculations
- Comprehensive error handling

---

#### 2. Position Sizer (`math/position_sizer.py`)

Calculate position allocation based on account size, risk bucket, and conviction level.

```python
from tools.math.position_sizer import get_allocation, get_max_position_size

# Calculate allocation for Core position with conviction 8/10
result = get_allocation(
    account_size=100000,
    bucket="Core",
    conviction=8
)

print(f"Allocate: ${result['allocation_dollars']:,.2f}")
print(f"Percentage: {result['allocation_pct']:.1%}")
```

**Function:** `get_allocation(account_size, bucket, conviction, risk_pct=None)`

**Parameters:**
- `account_size`: Total account value in dollars
- `bucket`: "Core" (10% max) or "Speculative" (2% max)
- `conviction`: 1-10 scale (1=lowest, 10=highest)
- `risk_pct`: Optional additional risk constraint

**Returns:** Dictionary with allocation details and warnings

**Sizing Rules:**
- Core positions: Maximum 10% of account
- Speculative positions: Maximum 2% of account
- Conviction multiplier scales within the cap

---

### Market Tools

#### 3. Market Data (`market/market_data_mock.py`)

Get liquidity metrics and earnings dates for stocks.

```python
from tools.market.market_data_mock import get_liquidity_metrics, get_earnings_date

# Get liquidity metrics
metrics = get_liquidity_metrics('AAPL')
print(f"Spread: {metrics['spread_pct']:.3%}")
print(f"Volume: {metrics['avg_volume']:,}")

# Get next earnings date
earnings = get_earnings_date('AAPL')
print(f"Earnings: {earnings['next_earnings_date']}")
print(f"Days until: {earnings['days_until']}")
```

**Functions:**
- `get_liquidity_metrics(ticker, use_mock=False)`: Returns bid, ask, spread, volume
- `get_earnings_date(ticker, use_mock=False)`: Returns next earnings date and timing

**Features:**
- Uses yfinance for real data when available
- Graceful fallback to mock data
- Realistic mock data generation for testing

---

#### 4. Calendar Check (`market/calendar_check.py`)

Check for earnings conflicts with option expirations.

```python
from tools.market.calendar_check import check_earnings_conflict, get_safe_expirations

# Check for earnings conflict
result = check_earnings_conflict('AAPL', '2024-02-16')

if result['has_conflict']:
    print(f"WARNING: {result['warning']}")
    print(f"Recommendation: {result['recommendation']}")

# Find safe expirations
safe = get_safe_expirations('AAPL', '2024-01-01', num_expirations=4)
print(f"Safe expirations: {safe['safe_expirations']}")
```

**Function:** `check_earnings_conflict(ticker, expiration_date, buffer_days=7)`

**Returns:**
- `has_conflict`: Boolean indicating conflict
- `severity`: 'high', 'medium', 'low', or None
- `warning`: Warning message if conflict exists
- `recommendation`: Suggested action

**Conflict Severity:**
- High: 0-2 days from earnings (AVOID)
- Medium: 3-5 days from earnings (CAUTION)
- Low: 6-7 days from earnings (MONITOR)

---

### Utility Tools

#### 5. File Operations (`utils/file_ops.py`)

Read and write portfolio data, reports, and trade orders.

```python
from tools.utils.file_ops import (
    read_portfolio_csv,
    write_report,
    write_trade_order_json
)

# Read portfolio CSV
portfolio = read_portfolio_csv('portfolio.csv')
for position in portfolio:
    print(f"{position['ticker']}: {position['shares']} shares")

# Write analysis report
report_data = {
    'ticker': 'AAPL',
    'beta': 1.23,
    'recommendation': 'BUY'
}
write_report(report_data, 'analysis.json', format='json')

# Write trade order
order = {
    'ticker': 'AAPL',
    'action': 'BUY',
    'quantity': 100,
    'order_type': 'LIMIT',
    'price': 175.00
}
write_trade_order_json(order, 'orders/aapl_buy.json')
```

**Functions:**
- `read_portfolio_csv(filepath)`: Read CSV portfolio file
- `write_report(data, filepath, format='auto')`: Write report in text/JSON/markdown
- `write_trade_order_json(order_data, filepath)`: Write validated trade order

**Features:**
- Automatic type conversion for CSV data
- Multiple output formats
- Validation for trade orders
- Automatic directory creation

---

## Quick Start

### Import All Tools

```python
# Import all tools at once
from tools import (
    # Math
    calculate_beta,
    get_allocation,
    get_max_position_size,

    # Market
    get_liquidity_metrics,
    get_earnings_date,
    check_earnings_conflict,
    get_safe_expirations,

    # File ops
    read_portfolio_csv,
    write_report,
    write_trade_order_json
)
```

### Example Workflow

```python
# 1. Calculate beta
beta, _ = calculate_beta('AAPL', 'SPY')
print(f"AAPL Beta: {beta:.2f}")

# 2. Check liquidity
liquidity = get_liquidity_metrics('AAPL')
print(f"Spread: {liquidity['spread_pct']:.3%}")

# 3. Check earnings conflicts
conflict = check_earnings_conflict('AAPL', '2024-02-16')
if conflict['has_conflict']:
    print(f"Warning: {conflict['warning']}")

# 4. Calculate position size
allocation = get_allocation(100000, "Core", conviction=8)
print(f"Position size: ${allocation['allocation_dollars']:,.2f}")

# 5. Write trade order
order = {
    'ticker': 'AAPL',
    'action': 'BUY',
    'quantity': 100,
    'price': 175.00,
    'order_type': 'LIMIT'
}
write_trade_order_json(order, 'orders/aapl.json')
```

## Testing

Each tool includes a test section in its `if __name__ == "__main__"` block.

Run individual tool tests:

```bash
# Test beta calculator
python tools/math/beta_calculator.py

# Test position sizer
python tools/math/position_sizer.py

# Test market data
python tools/market/market_data_mock.py

# Test calendar check
python tools/market/calendar_check.py

# Test file operations
python tools/utils/file_ops.py
```

## Error Handling

All tools include comprehensive error handling:

- **ValueError**: Invalid input parameters
- **FileNotFoundError**: Missing files
- **RuntimeError**: Operational failures
- **ImportError**: Missing dependencies

All functions include detailed docstrings with examples.

## Dependencies

- **yfinance**: Market data retrieval
- **numpy**: Numerical calculations

Both are optional - tools will use mock data if dependencies are unavailable.

## Notes

- All functions include type hints for better IDE support
- Mock data is deterministic (same ticker always returns same mock values)
- Market data tools gracefully degrade to mock data on errors
- File operations create parent directories automatically
- Trade orders are validated before writing

## License

Part of the BMAD-METHOD project.
