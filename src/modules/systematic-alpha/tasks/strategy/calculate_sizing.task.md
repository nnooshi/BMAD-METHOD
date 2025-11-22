# Calculate Position Sizing

## Purpose

Determine the exact position size (number of contracts or shares) for a trade based on portfolio size, position type (core vs speculative), conviction level, and risk management rules.

## Overview

Proper position sizing is the difference between systematic wealth building and account destruction. This task applies mathematical position sizing rules that ensure no single trade can significantly damage the portfolio while allowing winners to compound meaningfully.

## Inputs

**Required:**
- `portfolio_total_value`: Current total portfolio value ($)
- `position_type`: "core" or "speculative"
- `conviction_level`: "HIGH", "MODERATE", or "LOW"
- `trade_structure`: Specific trade details from fit_mechanism task
- `max_loss_per_spread`: Maximum loss per contract/spread ($)

**Optional:**
- `current_position_correlation`: Correlation with existing positions (0-1)
- `existing_exposure_pct`: Current portfolio exposure to this ticker (%)

## Processing Logic

### Step 1: Determine Base Allocation Percentage

**Position Type Rules:**

```
Core Positions (High Quality, Long-Term Holds):
- Base allocation: 10% of portfolio max
- Examples: AAPL, MSFT, high-conviction sector leaders
- Hold time: Weeks to months
- Can have multiple core positions

Speculative Positions (Higher Risk, Shorter-Term):
- Base allocation: 2% of portfolio max
- Examples: Earnings plays, low-conviction setups
- Hold time: Days to weeks
- Limit total speculative exposure to 10% portfolio
```

```
IF position_type == "core":
  base_allocation_pct = 0.10 (10%)
ELSE IF position_type == "speculative":
  base_allocation_pct = 0.02 (2%)
ELSE:
  ERROR: Invalid position_type
```

### Step 2: Apply Conviction Multiplier

```
Conviction adjusts the base allocation:

IF conviction_level == "HIGH":
  conviction_multiplier = 1.0 (use full base allocation)
ELSE IF conviction_level == "MODERATE":
  conviction_multiplier = 0.7 (reduce to 70% of base)
ELSE IF conviction_level == "LOW":
  conviction_multiplier = 0.5 (reduce to 50% of base)
ELSE:
  ERROR: Invalid conviction_level
```

**Adjusted Allocation:**

```
adjusted_allocation_pct = base_allocation_pct × conviction_multiplier
```

**Examples:**
- Core + High Conviction: 10% × 1.0 = 10%
- Core + Moderate Conviction: 10% × 0.7 = 7%
- Core + Low Conviction: 10% × 0.5 = 5%
- Speculative + High Conviction: 2% × 1.0 = 2%
- Speculative + Moderate Conviction: 2% × 0.7 = 1.4%

### Step 3: Calculate Dollar Allocation

```
dollar_allocation = portfolio_total_value × adjusted_allocation_pct
```

**Example:**
- Portfolio: $100,000
- Adjusted Allocation: 10%
- Dollar Allocation: $10,000

### Step 4: Determine Risk Per Trade

**Risk Budget Rules:**

```
Maximum risk per trade (potential loss if stopped out):

Core Positions:
- High Conviction: Risk up to 3% of portfolio
- Moderate Conviction: Risk up to 2% of portfolio
- Low Conviction: Risk up to 1% of portfolio

Speculative Positions:
- High Conviction: Risk up to 2% of portfolio
- Moderate Conviction: Risk up to 1.5% of portfolio
- Low Conviction: Risk up to 1% of portfolio
```

```
Determine max_risk_pct:

IF position_type == "core":
  IF conviction_level == "HIGH":
    max_risk_pct = 0.03
  ELSE IF conviction_level == "MODERATE":
    max_risk_pct = 0.02
  ELSE IF conviction_level == "LOW":
    max_risk_pct = 0.01
ELSE IF position_type == "speculative":
  IF conviction_level == "HIGH":
    max_risk_pct = 0.02
  ELSE IF conviction_level == "MODERATE":
    max_risk_pct = 0.015
  ELSE IF conviction_level == "LOW":
    max_risk_pct = 0.01

max_dollar_risk = portfolio_total_value × max_risk_pct
```

**Example:**
- Portfolio: $100,000
- Core + High Conviction
- Max Risk: 3% = $3,000

### Step 5: Calculate Number of Contracts

**For Debit Spreads (Call/Put Verticals):**

```
Max loss per spread = debit_paid per spread

Method 1: Based on Dollar Allocation
contracts_from_allocation = dollar_allocation / debit_paid
  → Round down to nearest whole number

Method 2: Based on Risk Budget
contracts_from_risk = max_dollar_risk / max_loss_per_spread
  → Round down to nearest whole number

final_contracts = MIN(contracts_from_allocation, contracts_from_risk)
```

**Example: NVDA 500/520 Call Vertical**
- Debit: $12.00 per spread ($1,200 per contract)
- Portfolio: $100,000
- Position: Core, High Conviction
- Dollar Allocation: $10,000
- Max Risk: $3,000

```
Contracts from allocation = $10,000 / $1,200 = 8.33 → 8 contracts
Contracts from risk = $3,000 / $1,200 = 2.5 → 2 contracts

Final: 2 contracts (risk constraint is limiting factor)

Actual Capital Deployed: 2 × $1,200 = $2,400
Actual Max Risk: 2 × $1,200 = $2,400 (2.4% of portfolio) ✓
```

**For Credit Spreads (Iron Condors, Short Strangles):**

```
Max loss per spread = (spread_width - credit_received) × 100

OR for undefined risk structures:
Use margin requirement as proxy for max loss

Contracts based on risk:
contracts = max_dollar_risk / max_loss_per_spread

Round down to whole number
```

**For Stock Positions:**

```
Shares calculation:

shares = dollar_allocation / stock_price

Round down to nearest 100 shares (for round lots)

Alternatively, based on stop loss:

Distance to stop = entry_price - stop_loss_price
max_dollar_risk = portfolio_value × max_risk_pct

shares = max_dollar_risk / distance_to_stop
```

### Step 6: Apply Correlation Adjustment

**If position is correlated with existing holdings:**

```
IF current_position_correlation provided AND correlation > 0.5:

  Correlation Adjustment Factor:
  IF correlation > 0.8:
    correlation_reduction = 0.5 (cut position by 50%)
  ELSE IF correlation > 0.7:
    correlation_reduction = 0.7 (cut position by 30%)
  ELSE IF correlation > 0.5:
    correlation_reduction = 0.85 (cut position by 15%)

  adjusted_contracts = final_contracts × correlation_reduction

  Round down to whole number

  WARNING: "Position size reduced due to correlation with existing holdings"
```

**Example:**
- Calculated: 5 contracts
- Already hold MSFT (correlation with new AAPL position = 0.75)
- Adjustment: 5 × 0.7 = 3.5 → 3 contracts

### Step 7: Apply Concentration Limits

**Check total exposure to single ticker:**

```
IF existing_exposure_pct provided:

  new_exposure_value = final_contracts × position_value_per_contract
  new_exposure_pct = new_exposure_value / portfolio_total_value

  total_ticker_exposure = existing_exposure_pct + new_exposure_pct

  IF total_ticker_exposure > 0.15 (15%):
    WARNING: "Total exposure to ticker exceeds 15% limit"

    max_allowable_new = (0.15 - existing_exposure_pct) × portfolio_total_value
    max_contracts = max_allowable_new / position_value_per_contract

    final_contracts = MIN(final_contracts, max_contracts)

    IF final_contracts < 1:
      recommendation = "SKIP - already at max exposure for this ticker"
```

### Step 8: Validate and Finalize

**Final Checks:**

```
1. Minimum Position Check:
   IF final_contracts < 1:
     recommendation = "Position too small - consider larger portfolio or different trade"

2. Odd Lot Check:
   IF final_contracts == 1:
     note = "Single contract position - consider if worth transaction costs"

3. Maximum Position Check:
   position_value = final_contracts × capital_per_contract
   IF position_value > portfolio_total_value × 0.15:
     WARNING: "Position exceeds 15% portfolio - reduce size"

4. Risk Verification:
   total_risk = final_contracts × max_loss_per_spread
   risk_pct = total_risk / portfolio_total_value × 100

   IF risk_pct > 5%:
     ERROR: "Position risk exceeds 5% portfolio - ABORT"
```

## Output Format

### Console Output

```
POSITION SIZING CALCULATION
============================
Trade: NVDA Jan 500/520 Call Vertical
Portfolio Value: $100,000

INPUTS:
-------
Position Type: CORE
Conviction Level: HIGH
Debit Per Spread: $12.00 ($1,200 per contract)
Max Loss Per Spread: $12.00 ($1,200 per contract)

ALLOCATION CALCULATION:
-----------------------
Base Allocation (Core): 10.0%
Conviction Multiplier (High): 1.0×
Adjusted Allocation: 10.0%
Dollar Allocation: $10,000

RISK CALCULATION:
------------------
Max Risk % (Core + High): 3.0%
Max Dollar Risk: $3,000

CONTRACT CALCULATION:
---------------------
Method 1 - Allocation Based:
  $10,000 / $1,200 = 8.33 → 8 contracts

Method 2 - Risk Based:
  $3,000 / $1,200 = 2.5 → 2 contracts

Selected Method: RISK BASED (more conservative)
Initial Contracts: 2

ADJUSTMENTS:
------------
✓ No correlation adjustment needed (no existing correlated positions)
✓ No concentration limit exceeded
✓ Position passes all validation checks

FINAL POSITION SIZE: 2 CONTRACTS

POSITION METRICS:
-----------------
Capital Deployed: $2,400 (2.4% of portfolio)
Maximum Risk: $2,400 (2.4% of portfolio) ✓
Maximum Profit: $1,600 (1.6% of portfolio)
Risk/Reward Ratio: 1:0.67 (inverted because debit spread)
  → Better metric: At target profit of $16/spread: 1:1.33

Position Value Breakdown:
- Buy 2 × NVDA Jan 500 Call: -$28.50 × 200 = -$5,700
- Sell 2 × NVDA Jan 520 Call: +$16.50 × 200 = +$3,300
- Net Debit: -$2,400

RISK VERIFICATION:
------------------
✓ Risk (2.4%) within limit for Core + High (3.0%)
✓ Position size (2.4%) within single position limit (15%)
✓ Absolute risk ($2,400) acceptable for portfolio size
✓ Minimum position size met (2 contracts > 1)

RECOMMENDATION: APPROVED ✓

Position is properly sized for:
- Portfolio value
- Position type (Core)
- Conviction level (High)
- Risk tolerance

Proceed to pre-trade checklist for final approval.
```

**Example: Speculative Position**

```
POSITION SIZING CALCULATION
============================
Trade: AMD Short Strangle (Speculative play)
Portfolio Value: $100,000

INPUTS:
-------
Position Type: SPECULATIVE
Conviction Level: MODERATE
Credit Per Spread: $4.50 ($450 per contract)
Max Loss Per Spread: $25.00 ($2,500 per contract - estimated undefined risk)

ALLOCATION CALCULATION:
-----------------------
Base Allocation (Speculative): 2.0%
Conviction Multiplier (Moderate): 0.7×
Adjusted Allocation: 1.4%
Dollar Allocation: $1,400

RISK CALCULATION:
------------------
Max Risk % (Speculative + Moderate): 1.5%
Max Dollar Risk: $1,500

CONTRACT CALCULATION:
---------------------
Method 1 - Allocation Based:
  $1,400 / $450 = 3.1 → 3 contracts

Method 2 - Risk Based:
  $1,500 / $2,500 = 0.6 → 0 contracts

⚠️ ISSUE DETECTED:
Risk-based calculation suggests position too large for risk tolerance.

Recalculating with stricter risk management:
Using 50% of max loss estimate: $1,250 per contract
Contracts = $1,500 / $1,250 = 1.2 → 1 contract

FINAL POSITION SIZE: 1 CONTRACT

POSITION METRICS:
-----------------
Capital Deployed: $0 (credit received)
Credit Received: $450 (0.45% of portfolio)
Maximum Risk: ~$2,500 (2.5% of portfolio) ⚠️
  → Exceeds ideal max risk of 1.5%
  → ACCEPTABLE for speculative position with active management

⚠️ CRITICAL MANAGEMENT REQUIRED:
- Close at 50% profit ($225)
- Stop loss at 100% loss ($450 debit to close)
- Monitor daily for breach of short strikes
- Do not hold through increased volatility

RECOMMENDATION: APPROVED WITH CONDITIONS ⚠️

This is a SMALL SPECULATIVE position requiring active management.
Set alerts for short strikes being tested.
```

**Example: Position Rejected**

```
POSITION SIZING CALCULATION
============================
Trade: TSLA Feb 250/270 Call Vertical
Portfolio Value: $50,000

INPUTS:
-------
Position Type: CORE
Conviction Level: HIGH
Debit Per Spread: $15.00 ($1,500 per contract)
Existing TSLA Exposure: 8% of portfolio ($4,000)

ALLOCATION CALCULATION:
-----------------------
Base Allocation (Core): 10.0%
Conviction Multiplier (High): 1.0×
Adjusted Allocation: 10.0%
Dollar Allocation: $5,000

RISK CALCULATION:
------------------
Max Risk % (Core + High): 3.0%
Max Dollar Risk: $1,500

CONTRACT CALCULATION:
---------------------
Method 1: $5,000 / $1,500 = 3.33 → 3 contracts
Method 2: $1,500 / $1,500 = 1.0 → 1 contract

Selected: 1 contract

CONCENTRATION CHECK:
--------------------
Existing TSLA Exposure: 8.0%
New Position Value: $1,500 (3.0%)
Total TSLA Exposure: 11.0%

⚠️ Within 15% single ticker limit, but approaching

CORRELATION CHECK:
------------------
No other positions with high correlation

FINAL POSITION SIZE: 1 CONTRACT

POSITION METRICS:
-----------------
Capital Deployed: $1,500 (3.0% of portfolio)
Total TSLA Exposure: $5,500 (11.0% of portfolio) ⚠️
Maximum Risk: $1,500 (3.0% of portfolio)

⚠️ WARNING: MARGINAL APPROVAL

Position meets sizing requirements but:
- Total TSLA exposure is 11% (approaching 15% limit)
- Only 1 contract (minimum size, high transaction cost impact)
- Consider: Is this worth commissions for 1 contract?

RECOMMENDATION: CONDITIONAL APPROVAL ⚠️

Suggestions:
1. Close existing TSLA position first, then enter this trade
2. Wait for better entry to justify 1-contract position
3. Consider a larger account size before taking this trade
```

### JSON Output

```json
{
  "trade": {
    "ticker": "NVDA",
    "structure": "500/520 Call Vertical",
    "expiration": "Jan 2026",
    "debit_per_contract": 1200
  },
  "portfolio": {
    "total_value": 100000
  },
  "inputs": {
    "position_type": "core",
    "conviction_level": "HIGH",
    "max_loss_per_spread": 1200
  },
  "allocation": {
    "base_pct": 10.0,
    "conviction_multiplier": 1.0,
    "adjusted_pct": 10.0,
    "dollar_amount": 10000
  },
  "risk": {
    "max_risk_pct": 3.0,
    "max_dollar_risk": 3000
  },
  "sizing": {
    "contracts_from_allocation": 8,
    "contracts_from_risk": 2,
    "initial_contracts": 2,
    "correlation_adjustment": 1.0,
    "final_contracts": 2
  },
  "position_metrics": {
    "capital_deployed": 2400,
    "capital_deployed_pct": 2.4,
    "max_risk": 2400,
    "max_risk_pct": 2.4,
    "max_profit": 1600,
    "max_profit_pct": 1.6
  },
  "validation": {
    "risk_within_limits": true,
    "position_size_acceptable": true,
    "concentration_ok": true,
    "minimum_size_met": true,
    "approved": true
  },
  "recommendation": "APPROVED"
}
```

## Decision Rules

### Position Type Selection

```
Core Position Criteria:
- High quality company (market cap > $50B preferred)
- Liquid options (volume > 10,000 contracts/day)
- Part of systematic strategy (momentum, VRP)
- Hold time: 2+ weeks

Speculative Position Criteria:
- Earnings plays
- Lower conviction setups
- Higher risk/reward plays
- Hold time: <2 weeks
```

### Risk Budget Allocation

```
Portfolio-Wide Risk Limits:
- Total risk across ALL positions: Max 10-15% of portfolio
- Single position max risk: 3% (core) or 2% (speculative)
- If total risk exceeds 10%, reduce new positions or close losers
```

### Position Size Overrides

```
Reduce position size if:
- Correlation > 0.7 with existing positions
- Ticker exposure > 10% already
- Total speculative exposure > 10% portfolio
- Unusual market conditions (VIX > 30)

Increase position size if:
- Conviction is VERY HIGH (rare, manual override only)
- Part of diversified basket (correlated positions work together)
- Scale-in strategy (building position over time)
```

## Validation Checks

- [ ] Position type is either "core" or "speculative"
- [ ] Conviction level is HIGH, MODERATE, or LOW
- [ ] Final contracts ≥ 1 (or position rejected)
- [ ] Total risk per position ≤ 5% portfolio
- [ ] Capital deployed ≤ 15% portfolio per position
- [ ] Correlation adjustments applied if necessary
- [ ] All math calculations verified

## Example Scenarios

### Scenario 1: Large Account, Core Position
- Portfolio: $500,000
- Trade: AAPL Call Vertical, $8/contract
- Type: Core, High Conviction
- Result: 15-20 contracts, $12,000-16,000 deployed

### Scenario 2: Small Account, Speculative
- Portfolio: $25,000
- Trade: Earnings Straddle, $6/contract
- Type: Speculative, Moderate Conviction
- Result: 1 contract, $600 deployed (max)

### Scenario 3: High Correlation
- Portfolio: $200,000
- Trade: MSFT (already hold AAPL, GOOGL)
- Correlation: 0.8 with existing tech holdings
- Result: Position size cut by 50% due to correlation

## Notes

- **NEVER exceed maximum risk limits** - this is the #1 rule
- Position sizing is MORE important than trade selection
- When in doubt, size smaller - you can always add more
- Paper trade to verify calculations before using real money
- Review position sizes monthly and adjust for portfolio growth
- Consider transaction costs - 1 contract positions often not worth it with high commissions

## Related Tasks

- `strategy/fit_mechanism.task.md` - Provides conviction level and trade structure
- `safeguards/pre_trade_checklist.task.md` - Final check before execution
- `portfolio/determine_needs.task.md` - Informs overall portfolio allocation
