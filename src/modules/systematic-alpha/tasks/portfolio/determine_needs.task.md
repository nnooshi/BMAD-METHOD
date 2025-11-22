# Determine Portfolio Needs

## Purpose

Compare current portfolio delta exposure against target allocation to identify whether the portfolio needs additional long or short delta to achieve desired balance.

## Overview

After calculating beta-weighted portfolio delta, this task determines the gap between current and target exposure, providing specific guidance on what type of trades are needed to achieve portfolio balance.

## Inputs

**Required:**
- `current_beta_weighted_delta`: Output from calc_beta_weighting task (SPY-equivalent shares)
- `target_delta_exposure`: Desired beta-weighted delta (SPY shares)
- `spy_price`: Current SPY price

**Optional:**
- `tolerance_range`: Acceptable deviation from target (default: ±15 SPY shares)
- `portfolio_size`: Total portfolio value (for percentage-based targets)

## Processing Logic

### Step 1: Calculate Delta Gap

```
delta_gap = target_delta_exposure - current_beta_weighted_delta
```

**Sign Convention:**
- Positive gap → Need to ADD long delta
- Negative gap → Need to ADD short delta (or reduce long delta)

### Step 2: Calculate Dollar Value of Gap

```
dollar_gap = delta_gap * spy_price
```

This represents the notional dollar exposure needed to close the gap.

### Step 3: Determine if Adjustment is Needed

```
IF ABS(delta_gap) <= tolerance_range:
  status = "BALANCED"
  action_required = false
ELSE:
  status = "ADJUSTMENT_NEEDED"
  action_required = true
```

### Step 4: Categorize Need Type

```
IF action_required == false:
  need_type = "NONE"
ELSE IF delta_gap > 0:
  need_type = "ADD_LONG_DELTA"
ELSE:
  need_type = "ADD_SHORT_DELTA"
```

### Step 5: Calculate Magnitude of Need

```
magnitude = ABS(delta_gap)

IF magnitude < 25:
  urgency = "LOW"
ELSE IF magnitude < 75:
  urgency = "MODERATE"
ELSE:
  urgency = "HIGH"
```

**Urgency Thresholds:**
- LOW (<25 shares): Minor adjustment, can wait for opportunistic entry
- MODERATE (25-75 shares): Normal rebalancing, execute within 1-2 days
- HIGH (>75 shares): Significant imbalance, prioritize correction

### Step 6: Generate Trade Recommendations

Based on `need_type` and `magnitude`, suggest appropriate trade structures:

**For ADD_LONG_DELTA:**
- Small (0-25): Long call verticals, buy shares on dips
- Medium (25-75): Bull call spreads, synthetic long positions
- Large (>75): Direct stock purchase, deep ITM calls

**For ADD_SHORT_DELTA:**
- Small (0-25): Short call verticals, covered calls on existing longs
- Medium (25-75): Bear put spreads, ratio spreads
- Large (>75): Direct short stock, deep ITM puts, protective positions

## Output Format

### Console Output

```
PORTFOLIO NEEDS ANALYSIS
========================

Current Portfolio State:
------------------------
Beta-Weighted Delta: +27.41 SPY shares
Target Delta: +50.00 SPY shares
Tolerance Range: ±15.00 SPY shares

Gap Analysis:
-------------
Delta Gap: +22.59 SPY shares (NEED MORE LONG DELTA)
Dollar Gap: $10,165.50 (+22.59 × $450)

Assessment:
-----------
Status: BALANCED ✓
Reason: Gap (+22.59) is within tolerance (±15.00)
Action Required: NO

Recommendation:
---------------
Current exposure is acceptable. Monitor for larger deviations.
If adjusting, consider small long delta additions on market pullbacks.
```

**Example with Action Required:**

```
PORTFOLIO NEEDS ANALYSIS
========================

Current Portfolio State:
------------------------
Beta-Weighted Delta: -15.50 SPY shares
Target Delta: +50.00 SPY shares
Tolerance Range: ±15.00 SPY shares

Gap Analysis:
-------------
Delta Gap: +65.50 SPY shares (NEED MORE LONG DELTA)
Dollar Gap: $29,475.00 (+65.50 × $450)

Assessment:
-----------
Status: ADJUSTMENT_NEEDED ⚠️
Need Type: ADD_LONG_DELTA
Magnitude: 65.50 shares
Urgency: MODERATE

Recommendation:
---------------
Portfolio is significantly underexposed to upside.

Suggested Actions:
1. PRIMARY: Add 65-70 long delta through:
   - Bull call spreads in high-conviction sectors
   - Long stock positions in quality names
   - ITM calls with >60 delta

2. ALTERNATIVE: Reduce short positions by:
   - Closing short calls (-30 to -40 delta)
   - Rolling short strikes further OTM

3. TIMING: Execute within 1-2 trading days
   - Scale in if market is elevated
   - Full position if market pulls back 1-2%

Next Steps:
-----------
→ Run analysis/define_disposition to assess market environment
→ Run analysis/sector_stacking to find optimal tickers
→ Run strategy/fit_mechanism to determine best trade structures
```

### JSON Output

```json
{
  "current_state": {
    "beta_weighted_delta": -15.50,
    "target_delta": 50.00,
    "tolerance_range": 15.00,
    "spy_price": 450.00
  },
  "gap_analysis": {
    "delta_gap": 65.50,
    "dollar_gap": 29475.00,
    "gap_direction": "need_long_delta"
  },
  "assessment": {
    "status": "ADJUSTMENT_NEEDED",
    "action_required": true,
    "need_type": "ADD_LONG_DELTA",
    "magnitude": 65.50,
    "urgency": "MODERATE"
  },
  "recommendations": {
    "primary_actions": [
      "Bull call spreads in high-conviction sectors",
      "Long stock positions in quality names",
      "ITM calls with >60 delta"
    ],
    "alternative_actions": [
      "Close short calls (-30 to -40 delta)",
      "Roll short strikes further OTM"
    ],
    "timing": "Execute within 1-2 trading days"
  },
  "timestamp": "2025-11-22T10:45:00Z"
}
```

## Decision Rules

### Target Setting Rules

1. **Bullish Market (Bull Disposition)**
   - Target: +30 to +60 SPY shares
   - Tolerance: ±20 shares

2. **Neutral Market**
   - Target: -10 to +10 SPY shares
   - Tolerance: ±15 shares

3. **Bearish Market (Bear Disposition)**
   - Target: -60 to -30 SPY shares
   - Tolerance: ±20 shares

### Portfolio Size Adjustments

```
IF portfolio_size > $500,000:
  tolerance_range = tolerance_range * 2
ELSE IF portfolio_size < $100,000:
  tolerance_range = tolerance_range * 0.5
```

### Risk Management Overrides

```
IF urgency == "HIGH" AND market_volatility > 25 (VIX):
  recommendation += "CAUTION: High volatility - scale entries"

IF delta_gap > 100 SPY shares:
  recommendation += "WARNING: Large adjustment needed - split into 2-3 tranches"
```

## Validation Checks

- [ ] Current delta is from recent calculation (<1 hour old)
- [ ] Target delta aligns with overall market disposition
- [ ] Tolerance range is appropriate for portfolio size
- [ ] Gap calculation is mathematically correct
- [ ] Urgency level matches magnitude thresholds

## Example Scenarios

### Scenario 1: Well-Balanced Portfolio
- Current: +48 SPY shares
- Target: +50 SPY shares
- Gap: +2 shares
- **Result:** BALANCED, no action needed

### Scenario 2: Need Long Delta
- Current: -20 SPY shares
- Target: +50 SPY shares
- Gap: +70 shares
- **Result:** MODERATE urgency, add bullish positions

### Scenario 3: Over-Exposed Long
- Current: +120 SPY shares
- Target: +50 SPY shares
- Gap: -70 shares
- **Result:** HIGH urgency, reduce long exposure or add hedges

### Scenario 4: Flip from Short to Long
- Current: -80 SPY shares
- Target: +50 SPY shares
- Gap: +130 shares
- **Result:** HIGH urgency, major restructuring needed

## Notes

- Always consider transaction costs when determining if adjustment is worth it
- Market conditions may override mathematical targets (e.g., don't add long delta into obvious resistance)
- Use this analysis in conjunction with market disposition and sector analysis
- Update targets when market regime changes

## Related Tasks

- `portfolio/calc_beta_weighting.task.md` - Provides current delta input
- `analysis/define_disposition.task.md` - Sets appropriate target ranges
- `strategy/calculate_sizing.task.md` - Determines position sizes for adjustments
