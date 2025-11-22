# Check Liquidity

## Purpose

Verify that options contracts or stock have sufficient liquidity to enter and exit positions without significant slippage or market impact. Poor liquidity = wider spreads = guaranteed loss on entry/exit.

## Overview

Liquidity is the FIRST safeguard in systematic trading. Even the best trade idea becomes a losing trade if you pay 5% in spread to enter and 5% to exit. This task implements strict liquidity requirements that filter out illiquid contracts before capital is risked.

## Inputs

**Required:**
- `ticker`: Stock symbol
- `option_details`: Array of option contracts to check
  - Each contract: {strike, expiration, type (call/put)}
- `position_size`: Number of contracts planned

**Optional:**
- `stock_check`: Boolean, whether to check stock liquidity (for stock positions)
- `min_volume_override`: Custom minimum volume requirement

## Processing Logic

### Step 1: Get Real-Time Market Data

```
FOR each option contract:
  Fetch current market data:
  - bid_price
  - ask_price
  - last_price
  - bid_size (contracts at bid)
  - ask_size (contracts at ask)
  - volume_today (contracts traded today)
  - open_interest (total open contracts)
  - implied_volatility
```

### Step 2: Calculate Bid-Ask Spread

**Absolute Spread:**

```
spread_dollars = ask_price - bid_price
```

**Percentage Spread:**

```
Calculate as percentage of mid-price:

mid_price = (bid_price + ask_price) / 2

IF mid_price > 0:
  spread_pct = (spread_dollars / mid_price) × 100
ELSE:
  spread_pct = UNDEFINED (no valid market)
  FAIL: "No valid market for this contract"
```

**Alternative: Spread as % of Stock Price**

```
For options, also calculate spread relative to underlying:

spread_pct_of_stock = (spread_dollars / stock_price) × 100
```

### Step 3: Apply Liquidity Thresholds

**PRIMARY RULE: Bid-Ask Spread**

```
CRITICAL THRESHOLD:

IF spread_pct > 0.5% (of mid-price):
  liquidity_status = "FAILED"
  reason = "Bid-ask spread too wide"
  REJECT_TRADE

Example:
- Bid: $9.80
- Ask: $10.20
- Mid: $10.00
- Spread: $0.40
- Spread %: 0.40 / 10.00 = 4.0%
- STATUS: FAILED (4.0% > 0.5%)

This means you lose 4% just entering the position!
```

**TIERED THRESHOLDS:**

```
For better granularity:

Spread Quality Tiers:

IF spread_pct <= 0.2%:
  tier = "EXCELLENT" (institutional quality)
ELSE IF spread_pct <= 0.5%:
  tier = "ACCEPTABLE" (retail acceptable)
ELSE IF spread_pct <= 1.0%:
  tier = "POOR" (warning, only if high conviction)
ELSE:
  tier = "UNACCEPTABLE"
  REJECT_TRADE
```

### Step 4: Volume Requirements

**Daily Volume Check:**

```
Minimum volume requirements:

Options:
IF volume_today < 100 contracts:
  volume_status = "VERY_LOW"
  warning = "Insufficient daily volume"

IF volume_today < 500 contracts:
  volume_status = "LOW"
  caution = "Below preferred volume"

IF volume_today >= 1000 contracts:
  volume_status = "GOOD"

IF volume_today >= 5000 contracts:
  volume_status = "EXCELLENT"

Reject if:
IF volume_today < min_volume_threshold:
  WHERE min_volume_threshold = MAX(100, position_size × 20)
  REJECT_TRADE
```

**Rationale:**
- If you want to trade 10 contracts, daily volume should be at least 200
- This ensures you're <5% of daily volume (low market impact)

### Step 5: Open Interest Check

```
Open Interest (OI) = Total outstanding contracts

Minimum OI requirements:

IF open_interest < 500:
  oi_status = "VERY_LOW"
  warning = "Low open interest - difficult exit"

IF open_interest < 1000:
  oi_status = "LOW"
  caution = "Below preferred OI"

IF open_interest >= 5000:
  oi_status = "GOOD"

IF open_interest >= 10000:
  oi_status = "EXCELLENT"

Reject if:
IF open_interest < position_size × 50:
  REJECT: "Open interest insufficient for position size"

Example:
- Want to trade 10 contracts
- Minimum OI: 10 × 50 = 500 contracts
```

### Step 6: Market Depth (Bid/Ask Size)

```
Check if market can absorb your order:

min_size_each_side = position_size × 0.5

IF bid_size < min_size_each_side OR ask_size < min_size_each_side:
  depth_warning = "Insufficient market depth"
  note = "May need to split order or use limit orders"

Example:
- Want to buy 20 contracts
- Min size needed: 20 × 0.5 = 10 contracts on ask
- Ask size showing: 8 contracts
- WARNING: Market depth insufficient, order will move market
```

### Step 7: Last Trade Recency

```
Check when last trade occurred:

IF last_trade_time > 30 minutes ago:
  recency_warning = "Stale pricing - no recent trades"
  caution = "Market may be inactive"

IF last_trade_time > 2 hours ago:
  recency_status = "STALE"
  REJECT: "No recent trading activity"
```

### Step 8: Strike Distance Check (Options Specific)

```
Verify strike is near the money (tradeable range):

stock_price = current_stock_price

distance_from_atm = ABS(strike - stock_price) / stock_price × 100

IF distance_from_atm > 20%:
  strike_warning = "Strike far from ATM - likely illiquid"
  IF spread_pct > 1.0%:
    REJECT: "Deep OTM strike with poor liquidity"

Rationale:
- Strikes >20% OTM typically have poor liquidity
- Only acceptable if spread is still tight
```

### Step 9: Stock Liquidity Check (If Applicable)

```
IF stock_check == true:

  Average Daily Volume (ADV):

  IF stock_avg_daily_volume < 500000 shares:
    stock_liquidity = "LOW"
    warning = "Stock has low average volume"

  IF stock_avg_daily_volume < 200000 shares:
    REJECT: "Stock too illiquid"

  Stock Bid-Ask Spread:

  stock_spread_pct = (stock_ask - stock_bid) / stock_mid × 100

  IF stock_spread_pct > 0.1%:
    warning = "Wide spread on underlying stock"

  IF stock_spread_pct > 0.5%:
    REJECT: "Stock bid-ask too wide"
```

### Step 10: Aggregate Liquidity Score

```
Calculate overall liquidity score (0-100):

Components (each 0-20 points):
1. Spread Quality:
   - ≤0.2%: 20 pts
   - 0.2-0.5%: 15 pts
   - 0.5-1.0%: 10 pts
   - >1.0%: 0 pts

2. Volume:
   - ≥5000: 20 pts
   - 1000-5000: 15 pts
   - 500-1000: 10 pts
   - 100-500: 5 pts
   - <100: 0 pts

3. Open Interest:
   - ≥10000: 20 pts
   - 5000-10000: 15 pts
   - 1000-5000: 10 pts
   - 500-1000: 5 pts
   - <500: 0 pts

4. Market Depth:
   - Size ≥ 2× position: 20 pts
   - Size ≥ 1× position: 15 pts
   - Size ≥ 0.5× position: 10 pts
   - Size < 0.5× position: 0 pts

5. Recency:
   - Last trade < 5 min: 20 pts
   - Last trade < 30 min: 15 pts
   - Last trade < 2 hrs: 10 pts
   - Last trade > 2 hrs: 0 pts

liquidity_score = SUM(all components)

Rating:
IF liquidity_score >= 80:
  rating = "EXCELLENT"
ELSE IF liquidity_score >= 60:
  rating = "GOOD"
ELSE IF liquidity_score >= 40:
  rating = "MARGINAL"
ELSE:
  rating = "POOR"
  RECOMMEND_REJECT
```

### Step 11: Final Decision Logic

```
Automatic REJECT conditions (any one triggers rejection):

1. Spread > 1.0% of mid
2. Volume < 100 contracts (or position_size × 20)
3. Open Interest < 500 (or position_size × 50)
4. No trades in last 2 hours
5. Stock volume < 200,000 shares/day (if stock trade)

WARNING conditions (proceed with caution):

1. Spread 0.5-1.0% (acceptable but not great)
2. Volume 100-500 contracts (low but tradeable)
3. OI 500-1000 (low but acceptable for small positions)
4. Bid/ask size < position size (may need to work order)

PASS conditions:

1. Spread ≤ 0.5%
2. Volume ≥ 500 contracts
3. OI ≥ 1000 contracts
4. Recent trading activity
5. Liquidity score ≥ 60
```

## Output Format

### Console Output - PASS Example

```
LIQUIDITY CHECK
===============
Ticker: NVDA
Analysis Date: 2025-11-22 10:45:30

OPTIONS BEING CHECKED:
----------------------
1. NVDA Jan 2026 $500 Call
2. NVDA Jan 2026 $520 Call

Position Size: 2 contracts each

CONTRACT 1: NVDA Jan 500 Call
==============================

Market Data:
------------
Bid: $28.40 × 150 contracts
Ask: $28.60 × 200 contracts
Last: $28.50 (2 minutes ago)
Mid: $28.50

Volume: 8,524 contracts today
Open Interest: 15,234 contracts
Implied Vol: 32.5%

Spread Analysis:
----------------
Spread: $0.20
Spread %: 0.70% of mid ✓ ACCEPTABLE
Spread % of Stock: 0.04% ✓ EXCELLENT

This spread costs you $0.20 × 2 contracts × 100 = $40 to enter

Volume Analysis:
----------------
Daily Volume: 8,524 ✓ EXCELLENT
Your Position: 2 contracts
% of Daily Volume: 0.02% ✓ Negligible impact

Open Interest:
--------------
Open Interest: 15,234 ✓ EXCELLENT
Your Position: 2 contracts
% of OI: 0.01% ✓ Easy exit available

Market Depth:
-------------
Bid Size: 150 contracts ✓ (75× your size)
Ask Size: 200 contracts ✓ (100× your size)
Assessment: Excellent depth, no market impact expected

Recency:
--------
Last Trade: 2 minutes ago ✓ ACTIVE

LIQUIDITY SCORE: 95/100 ✓ EXCELLENT

-------------------------------------------------

CONTRACT 2: NVDA Jan 520 Call
==============================

Market Data:
------------
Bid: $16.40 × 120 contracts
Ask: $16.60 × 180 contracts
Last: $16.50 (1 minute ago)
Mid: $16.50

Volume: 6,892 contracts today
Open Interest: 12,456 contracts

Spread Analysis:
----------------
Spread: $0.20
Spread %: 1.21% of mid ✓ ACCEPTABLE
Spread % of Stock: 0.04% ✓ EXCELLENT

Volume Analysis:
----------------
Daily Volume: 6,892 ✓ EXCELLENT
Your Position: 2 contracts
% of Daily Volume: 0.03% ✓ Negligible impact

Open Interest: 12,456 ✓ EXCELLENT
Market Depth: ✓ GOOD
Recency: ✓ ACTIVE

LIQUIDITY SCORE: 92/100 ✓ EXCELLENT

═════════════════════════════════════════════════

OVERALL ASSESSMENT:
===================

Status: ✓ APPROVED

All contracts pass liquidity requirements.

Spread Cost Analysis:
---------------------
500 Call spread cost: $0.20 × 2 × 100 = $40
520 Call spread cost: $0.20 × 2 × 100 = $40
Total spread cost: $80 (0.08% of position)

This is acceptable slippage for entry.

Execution Recommendations:
--------------------------
✓ Use limit orders at mid price ($28.50 / $16.50)
✓ If no fill in 2 minutes, adjust to $28.55 / $16.55
✓ Do NOT use market orders (unnecessary slippage)
✓ All-or-none (AON) not needed - sufficient depth

Next Step:
----------
Proceed to pre_trade_checklist for final approval.
```

### Console Output - REJECT Example

```
LIQUIDITY CHECK
===============
Ticker: XYZ
Analysis Date: 2025-11-22 10:45:30

CONTRACT: XYZ Feb 2026 $50 Call
================================

Market Data:
------------
Bid: $2.10 × 10 contracts
Ask: $2.50 × 15 contracts
Last: $2.20 (45 minutes ago)
Mid: $2.30

Volume: 35 contracts today
Open Interest: 248 contracts

❌ CRITICAL ISSUES DETECTED:

Spread Analysis:
----------------
Spread: $0.40
Spread %: 17.4% of mid ❌ UNACCEPTABLE
Spread % of Stock: 0.8% ❌ EXCESSIVE

⚠️ PROBLEM: You would lose 17.4% just entering this position!
Entry cost: $2.50
Exit (at mid): $2.30
Guaranteed loss: $0.40 (17.4%)

Volume Analysis:
----------------
Daily Volume: 35 contracts ❌ VERY LOW
Your Position: 5 contracts
% of Daily Volume: 14.3% ⚠️ You would be 14% of all volume

Open Interest:
--------------
Open Interest: 248 ❌ VERY LOW
Your Position: 5 contracts
Minimum Required: 250 contracts (50× position)
❌ FAILS: Insufficient open interest for position size

Market Depth:
-------------
Bid Size: 10 contracts ⚠️ (only 2× your size)
Ask Size: 15 contracts ⚠️ (only 3× your size)
Assessment: Shallow market, your order will move price

Recency:
--------
Last Trade: 45 minutes ago ⚠️ STALE

LIQUIDITY SCORE: 15/100 ❌ POOR

═════════════════════════════════════════════════

OVERALL ASSESSMENT:
===================

Status: ❌ REJECTED

REASONS FOR REJECTION:
----------------------
1. ❌ Spread (17.4%) exceeds maximum (1.0%)
2. ❌ Volume (35) below minimum (100)
3. ❌ Open interest (248) below minimum for position size (250)
4. ⚠️ Stale pricing (last trade 45 min ago)

ESTIMATED COST OF ILLIQUIDITY:
------------------------------
Spread cost on entry: $0.40 × 5 × 100 = $200
Expected spread on exit: ~$0.40 × 5 × 100 = $200
Total liquidity tax: $400

This represents an 8.7% drag on a $4,600 position.
You would need stock to move >8.7% just to break even on spreads.

RECOMMENDATION: ❌ DO NOT TRADE

Alternative Actions:
--------------------
1. Find a more liquid strike (closer to ATM)
2. Choose a nearer expiration (usually more liquid)
3. Trade the stock directly instead of options
4. Look for similar trade in more liquid ticker
5. PASS on this opportunity entirely (recommended)

Trade REJECTED. Do not proceed.
```

### JSON Output

```json
{
  "ticker": "NVDA",
  "analysis_timestamp": "2025-11-22T10:45:30Z",
  "position_size": 2,
  "contracts": [
    {
      "contract": "NVDA Jan 2026 500 Call",
      "market_data": {
        "bid": 28.40,
        "ask": 28.60,
        "last": 28.50,
        "mid": 28.50,
        "bid_size": 150,
        "ask_size": 200,
        "volume": 8524,
        "open_interest": 15234,
        "last_trade_minutes_ago": 2
      },
      "spread_analysis": {
        "spread_dollars": 0.20,
        "spread_pct_of_mid": 0.70,
        "spread_pct_of_stock": 0.04,
        "spread_cost_total": 40,
        "status": "ACCEPTABLE"
      },
      "volume_analysis": {
        "volume": 8524,
        "position_pct_of_volume": 0.02,
        "status": "EXCELLENT"
      },
      "open_interest_analysis": {
        "open_interest": 15234,
        "position_pct_of_oi": 0.01,
        "status": "EXCELLENT"
      },
      "depth_analysis": {
        "bid_size_ratio": 75.0,
        "ask_size_ratio": 100.0,
        "status": "EXCELLENT"
      },
      "liquidity_score": 95,
      "rating": "EXCELLENT",
      "approved": true
    }
  ],
  "overall_assessment": {
    "all_approved": true,
    "status": "APPROVED",
    "total_spread_cost": 80,
    "total_spread_cost_pct": 0.08,
    "execution_recommendations": [
      "Use limit orders at mid price",
      "Adjust price slowly if no fill",
      "Do not use market orders"
    ]
  }
}
```

## Decision Rules

### Automatic Rejection Criteria

```
REJECT if ANY of the following:

1. Spread > 1.0% of mid price
2. Daily volume < 100 contracts
3. Daily volume < position_size × 20
4. Open interest < 500 contracts
5. Open interest < position_size × 50
6. No trades in last 2 hours
7. Bid or Ask is $0.00 (no market)
8. Liquidity score < 40
```

### Warning Criteria (Proceed with Caution)

```
WARN if ANY of the following:

1. Spread 0.5% - 1.0%
2. Volume 100-500 contracts
3. Open interest 500-1000 contracts
4. Market depth < 2× position size
5. Last trade 30-120 minutes ago
6. Liquidity score 40-60
```

### Approval Criteria

```
APPROVE if ALL of the following:

1. Spread ≤ 0.5% (or ≤ 1.0% with warning)
2. Volume ≥ 500 contracts (or ≥ 100 with caution)
3. Open interest ≥ 1000 contracts
4. Recent trading activity (< 30 min preferred)
5. Liquidity score ≥ 60
6. No automatic rejection triggers
```

## Validation Checks

- [ ] Market data is real-time (< 5 minutes old)
- [ ] All required fields present (bid, ask, volume, OI)
- [ ] Spread calculations are correct
- [ ] Position size validated against volume/OI
- [ ] All contracts in the spread checked (not just one leg)

## Notes

- **Liquidity is NON-NEGOTIABLE** - never trade illiquid options
- Wide spreads guarantee losses even if directionally correct
- Options near expiration and far OTM are typically illiquid
- Earnings week can temporarily increase liquidity (but also vol)
- Consider stock alternatives if options fail liquidity test
- SPY, QQQ, and mega-cap tech typically have excellent liquidity
- Small-cap and low-volume stocks rarely have tradeable options

## Related Tasks

- `strategy/fit_mechanism.task.md` - Provides trade structure to check
- `strategy/calculate_sizing.task.md` - Provides position size for validation
- `safeguards/pre_trade_checklist.task.md` - Final check after liquidity passes
