# Calculate Beta Weighting

## Purpose

Calculate the beta-weighted delta exposure of a portfolio relative to SPY (S&P 500 ETF) to understand how the portfolio behaves in relation to overall market movements.

## Overview

Beta weighting translates individual position deltas into SPY-equivalent shares, allowing traders to understand their directional exposure in terms of a single benchmark. This is essential for portfolio-level delta management and hedging decisions.

## Inputs

**Required:**
- `portfolio_csv`: Path to portfolio CSV file
- `spy_price`: Current SPY market price

**CSV Format:**
```csv
ticker,position_delta,stock_price,beta
AAPL,50,180.50,1.25
MSFT,-30,350.00,1.10
TSLA,25,245.00,2.05
```

**Field Definitions:**
- `ticker`: Stock symbol
- `position_delta`: Net delta of all positions in this ticker (positive = long, negative = short)
- `stock_price`: Current stock price
- `beta`: Beta coefficient relative to SPY (use historical beta or compute from correlation)

## Processing Logic

### Step 1: Load Portfolio Data

```
FOR each position in portfolio_csv:
  - Validate required fields exist
  - Convert numeric fields to float/decimal
  - Check for missing or invalid data
```

### Step 2: Calculate Position Beta-Weighted Deltas

**Formula for each position:**

```
beta_weighted_delta = (position_delta * beta * stock_price) / spy_price
```

**Breakdown:**
1. `position_delta * stock_price` = Dollar value of position delta
2. Multiply by `beta` = Adjust for stock's sensitivity to market
3. Divide by `spy_price` = Convert to equivalent SPY shares

**Example:**
- Position: AAPL with 50 delta, price $180.50, beta 1.25
- SPY price: $450.00
- Beta-weighted delta = (50 × 1.25 × 180.50) / 450 = 25.07 SPY shares

### Step 3: Aggregate Portfolio Beta-Weighted Delta

```
total_beta_weighted_delta = SUM(all beta_weighted_deltas)
```

### Step 4: Calculate Dollar Exposure

```
dollar_exposure = total_beta_weighted_delta * spy_price
```

### Step 5: Determine Portfolio Directional Bias

```
IF total_beta_weighted_delta > 10:
  bias = "LONG"
ELSE IF total_beta_weighted_delta < -10:
  bias = "SHORT"
ELSE:
  bias = "NEUTRAL"
```

**Threshold Explanation:**
- +/- 10 shares accounts for small rounding errors and noise
- Adjust threshold based on portfolio size

## Output Format

### Console Output

```
PORTFOLIO BETA WEIGHTING ANALYSIS
===================================

SPY Reference Price: $450.00

Position Breakdown:
-------------------
AAPL:  +25.07 SPY shares  (50 delta × 1.25 beta × $180.50 / $450)
MSFT:  -25.67 SPY shares  (-30 delta × 1.10 beta × $350.00 / $450)
TSLA:  +28.01 SPY shares  (25 delta × 2.05 beta × $245.00 / $450)

Portfolio Summary:
------------------
Total Beta-Weighted Delta: +27.41 SPY shares
Dollar Exposure: $12,334.50 (+27.41 × $450)
Directional Bias: LONG

INTERPRETATION:
Your portfolio behaves like owning 27.41 shares of SPY.
A $1 move in SPY translates to approximately $27.41 portfolio change.
```

### JSON Output (Optional)

```json
{
  "spy_price": 450.00,
  "positions": [
    {
      "ticker": "AAPL",
      "position_delta": 50,
      "beta": 1.25,
      "stock_price": 180.50,
      "beta_weighted_delta": 25.07
    }
  ],
  "summary": {
    "total_beta_weighted_delta": 27.41,
    "dollar_exposure": 12334.50,
    "directional_bias": "LONG"
  },
  "timestamp": "2025-11-22T10:30:00Z"
}
```

## Decision Rules

1. **Invalid Data Handling**
   - Missing beta → Default to 1.0 (market beta)
   - Missing position_delta → Skip position with warning
   - Zero or negative prices → Reject with error

2. **SPY Price**
   - Must be current market price (< 5 minutes old)
   - Validate SPY price is within reasonable range ($300-$600)

3. **Delta Normalization**
   - Options deltas should already be normalized (0-100 per contract)
   - Stock positions: 100 shares = 100 delta

## Validation Checks

- [ ] All positions have valid beta values
- [ ] Position deltas are within reasonable limits (-10,000 to +10,000)
- [ ] SPY price is recent and valid
- [ ] Sum of beta-weighted deltas matches manual calculation
- [ ] Dollar exposure calculation is correct

## Example Use Case

**Scenario:** Trader has mixed portfolio and wants to add hedging position

**Input Portfolio:**
- Long 100 NVDA shares (delta +100, beta 1.8, price $500)
- Short 2 NVDA $520 calls (delta -80, beta 1.8)
- Long 5 SPY $450 puts (delta -250, beta 1.0)

**Calculation:**
1. NVDA stock: (100 × 1.8 × 500) / 450 = 200 SPY shares
2. NVDA calls: (-80 × 1.8 × 500) / 450 = -160 SPY shares
3. SPY puts: (-250 × 1.0 × 450) / 450 = -250 SPY shares

**Result:** Net -210 SPY shares (SHORT bias, needs +210 delta to neutralize)

## Notes

- Beta values should be updated weekly from market data
- Consider using 30-day or 60-day beta for more stable calculations
- High-beta stocks (>2.0) can skew portfolio dramatically
- SPY alternatives: Use IVV or VOO if SPY unavailable

## Related Tasks

- `portfolio/determine_needs.task.md` - Uses beta weighting to determine trade needs
- `safeguards/check_liquidity.task.md` - Validates positions are tradeable
