# Pre-Trade Checklist

## Purpose

Final comprehensive verification before executing a trade. This is the last line of defense against bad trades, incorporating all previous analyses plus critical safeguards. The ultimate "NO" logic that prevents disasters.

## Overview

This checklist aggregates all prior task outputs and adds final safety checks. Think of it as the launch checklist for a rocket - every item must be verified before ignition. One failed check = no trade. Period.

## Inputs

**Required:**
- `ticker`: Stock symbol
- `trade_structure`: Complete trade details from fit_mechanism
- `position_size`: Number of contracts from calculate_sizing
- `liquidity_check_results`: Output from check_liquidity task
- `market_disposition`: Current market regime
- `portfolio_current_state`: Current positions and exposures

**Optional:**
- `earnings_date`: Next earnings announcement
- `economic_calendar`: Upcoming events (FOMC, CPI, etc.)
- `override_reason`: Manual override explanation (use sparingly)

## Processing Logic

### SECTION 1: Liquidity Verification

```
Requirement: Liquidity check MUST have passed

IF liquidity_check_results.status != "APPROVED":
  REJECT: "Failed liquidity requirements"
  HALT

IF liquidity_check_results.spread_pct > 0.5%:
  REJECT: "Bid-ask spread too wide"
  reason = "Spread {spread_pct}% exceeds 0.5% maximum"
  HALT

✓ PASS: Liquidity verified
```

### SECTION 2: Event Risk Check

**Critical: No trading before known events**

```
Check earnings risk:

IF earnings_date provided:
  days_to_earnings = earnings_date - today

  IF days_to_earnings <= 7:
    REJECT: "Earnings too close"
    reason = "Earnings in {days_to_earnings} days, within 7-day blackout"
    HALT

  IF days_to_earnings <= 14 AND position_type != "earnings_volatility":
    FLAG: "Earnings in {days_to_earnings} days"
    warning = "Caution - earnings approaching"
    require_acknowledgment = true

Check economic events:

high_impact_events = ["FOMC", "CPI", "NFP", "GDP"]

FOR each event in economic_calendar:
  IF event.date - today <= 3 AND event.type IN high_impact_events:
    FLAG: "High-impact event in 3 days: {event.type}"
    warning = "Consider delaying entry until after event"

✓ PASS if no earnings within 7 days (or is earnings play)
⚠️ FLAG if earnings in 7-14 days (proceed with caution)
```

### SECTION 3: Correlation Check

**Prevent over-concentration in correlated positions**

```
Calculate correlation with existing positions:

FOR each existing_position in portfolio:

  IF existing_position.ticker == ticker:
    combined_exposure = existing_position.size + position_size
    combined_exposure_pct = calculate_exposure_percentage()

    IF combined_exposure_pct > 15%:
      REJECT: "Single ticker exposure exceeds 15%"
      detail = "Current: {existing}%, New: {new}%, Total: {combined}%"
      HALT

  correlation = calculate_correlation(ticker, existing_position.ticker)

  IF correlation > 0.8:
    WARN: "High correlation with {existing_position.ticker}"
    detail = "Correlation: {correlation}"
    note = "Consider if adding redundant exposure"

    combined_correlated_exposure = sum_correlated_positions()

    IF combined_correlated_exposure > 25%:
      REJECT: "Correlated exposure exceeds 25%"
      HALT

✓ PASS if correlation checks pass
⚠️ FLAG if moderate correlation (0.6-0.8)
❌ REJECT if single ticker >15% or correlated group >25%
```

### SECTION 4: Position Size Validation

```
Verify position sizing is within limits:

position_value = position_size × cost_per_contract
position_pct = position_value / portfolio_total_value × 100

IF position_type == "core":
  max_pct = 10%
ELSE IF position_type == "speculative":
  max_pct = 2%

IF position_pct > max_pct:
  REJECT: "Position size exceeds maximum"
  detail = "Size: {position_pct}%, Max: {max_pct}%"
  HALT

Verify risk limits:

max_loss = position_size × max_loss_per_contract
max_loss_pct = max_loss / portfolio_total_value × 100

IF position_type == "core" AND conviction == "HIGH":
  max_risk_allowed = 3%
ELSE IF position_type == "core":
  max_risk_allowed = 2%
ELSE IF position_type == "speculative":
  max_risk_allowed = 2%

IF max_loss_pct > max_risk_allowed:
  REJECT: "Risk exceeds allowed maximum"
  detail = "Risk: {max_loss_pct}%, Max: {max_risk_allowed}%"
  HALT

IF max_loss_pct > 5%:
  REJECT: "Risk exceeds absolute maximum (5%)"
  HALT

✓ PASS if position size and risk within limits
```

### SECTION 5: Market Disposition Alignment

```
Verify trade aligns with market regime:

IF market_disposition IN ["STRONG_BULL", "BULL"]:
  IF trade_direction == "bearish":
    WARN: "Bearish trade in bull market"
    require_acknowledgment = true
    require_justification = "Why betting against market?"

ELSE IF market_disposition IN ["STRONG_BEAR", "BEAR"]:
  IF trade_direction == "bullish":
    WARN: "Bullish trade in bear market"
    require_acknowledgment = true
    require_justification = "Why fighting the trend?"

ELSE IF market_disposition == "NEUTRAL":
  # Both directions acceptable in neutral market
  pass

Verify sector alignment:

IF sector_relative_strength < -5% AND trade_direction == "bullish":
  WARN: "Bullish trade in weak sector"
  note = "Sector RS: {sector_relative_strength}%"

✓ PASS if aligned with disposition
⚠️ FLAG if counter to disposition (require justification)
```

### SECTION 6: Technical Setup Validation

```
Verify technical levels support trade:

For bullish trades:

  support_level = identify_nearest_support_below()
  distance_to_support = (entry_price - support_level) / entry_price × 100

  IF distance_to_support > 5%:
    WARN: "Far from support ({distance_to_support}%)"
    note = "Stop loss may be wide"

  resistance_level = identify_nearest_resistance_above()
  distance_to_resistance = (resistance_level - entry_price) / entry_price × 100

  IF distance_to_resistance < 2%:
    WARN: "Near resistance ({distance_to_resistance}%)"
    note = "Limited upside before resistance"

For bearish trades:

  resistance_level = identify_nearest_resistance_above()
  support_level = identify_nearest_support_below()

  IF price_near_support:
    WARN: "Price near support - bounce risk"

Verify price action:

IF stock_price < 20_MA < 50_MA < 200_MA AND trade_direction == "bullish":
  REJECT: "Bullish trade in clear downtrend"
  detail = "All MAs in downtrend alignment"
  HALT

✓ PASS if technical setup supports trade
⚠️ FLAG if setup is marginal
❌ REJECT if setup contradicts trade direction
```

### SECTION 7: Risk/Reward Verification

```
Calculate and verify risk/reward ratio:

potential_profit = calculate_max_profit()
potential_loss = calculate_max_loss()

risk_reward_ratio = potential_profit / potential_loss

IF risk_reward_ratio < 1.0:
  WARN: "Risk/Reward below 1:1"
  note = "Risking more than potential profit"
  require_acknowledgment = true

IF risk_reward_ratio < 0.5:
  REJECT: "Risk/Reward unacceptable (<0.5:1)"
  HALT

Minimum R/R thresholds:
- Core positions: 1.5:1 preferred
- Speculative: 2.0:1 preferred

✓ PASS if R/R ≥ 1.5:1
⚠️ FLAG if R/R 1.0-1.5:1
❌ REJECT if R/R < 1.0:1
```

### SECTION 8: Portfolio Risk Budget

```
Check total portfolio risk:

total_risk = sum_of_all_open_position_risks()
new_position_risk = max_loss
total_risk_with_new = total_risk + new_position_risk

total_risk_pct = total_risk_with_new / portfolio_total_value × 100

IF total_risk_pct > 15%:
  REJECT: "Total portfolio risk exceeds 15%"
  detail = "Current: {total_risk}%, New: {new_position_risk}%"
  action_required = "Close losing positions before adding new"
  HALT

IF total_risk_pct > 10%:
  WARN: "Portfolio risk elevated ({total_risk_pct}%)"
  note = "Consider reducing size or closing losers"

✓ PASS if total portfolio risk <15%
⚠️ FLAG if portfolio risk 10-15%
❌ REJECT if portfolio risk >15%
```

### SECTION 9: Execution Feasibility

```
Verify trade is executable:

IF market_hours == "closed":
  FLAG: "Market closed - trade will be placed at open"
  note = "Price may gap from planned entry"

IF trade_structure.requires_margin AND margin_available < required:
  REJECT: "Insufficient margin"
  HALT

IF account_cash < capital_required:
  REJECT: "Insufficient cash for trade"
  HALT

Check option chain availability:

FOR each contract in trade_structure:
  IF contract.expiration < today + 7:
    WARN: "Contract expiring soon ({days_to_expiration} days)"
  IF contract.expiration < today + 3:
    REJECT: "Contract too close to expiration"
    HALT

✓ PASS if trade is executable
```

### SECTION 10: Final Checklist

```
ALL items must be ✓ to proceed:

[ ] Liquidity check: APPROVED
[ ] Bid-ask spread: ≤ 0.5%
[ ] Earnings risk: None within 7 days (or is earnings play)
[ ] Correlation: <0.8 with existing positions
[ ] Single ticker exposure: ≤ 15%
[ ] Correlated group exposure: ≤ 25%
[ ] Position size: Within limits (10% core, 2% spec)
[ ] Max risk per trade: ≤ 3% (core high), ≤ 2% (other)
[ ] Market disposition: Aligned (or justified if not)
[ ] Technical setup: Supports trade direction
[ ] Risk/Reward: ≥ 1.0:1 (preferably ≥ 1.5:1)
[ ] Total portfolio risk: ≤ 15%
[ ] Account cash: Sufficient
[ ] Margin: Sufficient (if applicable)
[ ] Expiration: ≥ 7 days away
[ ] No critical pending news events

Count checklist:
passed = COUNT(✓)
total = COUNT(all items)

IF passed == total:
  STATUS = "APPROVED"
ELSE:
  failed_items = list_of_failed_checks()
  STATUS = "REJECTED"
  reason = "Failed {total - passed} checklist items: {failed_items}"
```

## Output Format

### Console Output - APPROVED

```
═══════════════════════════════════════════════════
        PRE-TRADE CHECKLIST - FINAL VERIFICATION
═══════════════════════════════════════════════════

Trade: NVDA Jan 500/520 Call Vertical
Date: 2025-11-22 10:50:00
Position Size: 2 contracts
Portfolio Value: $100,000

---------------------------------------------------
SECTION 1: LIQUIDITY ✓
---------------------------------------------------
✓ Liquidity check: APPROVED
✓ Bid-ask spread: 0.70% (within 0.5% threshold with margin)
✓ Volume: 8,524 contracts (excellent)
✓ Open interest: 15,234 (excellent)
✓ Market depth: Sufficient

Status: PASS

---------------------------------------------------
SECTION 2: EVENT RISK ✓
---------------------------------------------------
✓ Earnings date: 28 days away (safe)
✓ No FOMC in next 3 days
✓ No CPI/NFP in next 3 days
✓ No known binary events

Status: PASS

---------------------------------------------------
SECTION 3: CORRELATION ✓
---------------------------------------------------
✓ No existing NVDA position
✓ MSFT position correlation: 0.65 (moderate, acceptable)
✓ Total tech exposure: 18% (within 25% limit)
✓ Single ticker limit: OK

Status: PASS

---------------------------------------------------
SECTION 4: POSITION SIZING ✓
---------------------------------------------------
✓ Position type: CORE
✓ Position size: 2.4% of portfolio (within 10% limit)
✓ Max risk: $2,400 (2.4% of portfolio)
✓ Risk limit (core, high): 3.0%
✓ Position risk within limits

Status: PASS

---------------------------------------------------
SECTION 5: MARKET ALIGNMENT ✓
---------------------------------------------------
✓ Market disposition: STRONG_BULL
✓ Trade direction: BULLISH (aligned)
✓ Sector (XLK) RS: +7.1% (leading sector)
✓ Stock RS: +20.5% (leading stock)
✓ Full alignment with market regime

Status: PASS

---------------------------------------------------
SECTION 6: TECHNICAL SETUP ✓
---------------------------------------------------
✓ Price: $502.50
✓ 20MA: $495 (price above)
✓ 50MA: $485 (above)
✓ 200MA: $450 (above)
✓ Trend: STRONG_UPTREND
✓ Support: $490 (2.5% below)
✓ Resistance: $520 (3.5% above)
✓ Technical setup confirms trade thesis

Status: PASS

---------------------------------------------------
SECTION 7: RISK/REWARD ✓
---------------------------------------------------
Entry: $12.00/spread ($2,400 total)
Max Profit: $8.00/spread ($1,600 total)
Max Loss: $12.00/spread ($2,400 total)

Risk/Reward: 1:0.67 (inverted for debit spread)

At target profit ($16/spread):
Profit: $4.00/spread ($800 total)
Risk/Reward from entry: 1:1.33 ✓

✓ Acceptable R/R for high-conviction momentum play

Status: PASS

---------------------------------------------------
SECTION 8: PORTFOLIO RISK ✓
---------------------------------------------------
Current open positions risk: $4,200 (4.2%)
This position risk: $2,400 (2.4%)
Total portfolio risk: $6,600 (6.6%)

✓ Total risk: 6.6% (well below 15% limit)
✓ Risk budget: Healthy

Status: PASS

---------------------------------------------------
SECTION 9: EXECUTION ✓
---------------------------------------------------
✓ Market: OPEN
✓ Account cash: $45,000 available
✓ Capital required: $2,400
✓ Margin: Not required (debit spread)
✓ Contracts expiration: 45 DTE (sufficient)
✓ All legs tradeable

Status: PASS

---------------------------------------------------
FINAL CHECKLIST SUMMARY
---------------------------------------------------

[✓] Liquidity: APPROVED
[✓] Event Risk: Clear
[✓] Correlation: Within limits
[✓] Position Size: Appropriate
[✓] Market Alignment: Confirmed
[✓] Technical Setup: Strong
[✓] Risk/Reward: Acceptable
[✓] Portfolio Risk: Healthy
[✓] Execution: Ready

Passed: 9/9 checks

═══════════════════════════════════════════════════
        STATUS: ✓ APPROVED FOR EXECUTION
═══════════════════════════════════════════════════

EXECUTION INSTRUCTIONS:
-----------------------

Trade Structure:
BUY 2 NVDA Jan 24, 2026 $500 Call
SELL 2 NVDA Jan 24, 2026 $520 Call

Entry Strategy:
1. Place as a VERTICAL SPREAD order (not two separate orders)
2. Start with LIMIT order at $12.00 debit (mid price)
3. If no fill in 2 minutes, adjust to $12.05
4. Maximum acceptable: $12.50 debit
5. Do NOT use market order

Expected Fill:
- Total debit: $2,400 ($12.00 × 2 × 100)
- Plus commissions: ~$2.60 (at $0.65/contract)
- Total cost: ~$2,402.60

Risk Management:
- Stop loss: Exit if position value drops to $8.00 ($1,600 total)
- Or if NVDA closes below $490 (20MA support)
- Profit target 1: $16.00 (close 50%)
- Profit target 2: $18.00 (close remainder)

Time Management:
- Exit 7 days before expiration (Jan 17, 2026)
- Do not hold into final week

Record Keeping:
- Log entry price, date, rationale
- Set calendar reminders for exits
- Monitor daily for stop conditions

═══════════════════════════════════════════════════

You are cleared for trade execution.
```

### Console Output - REJECTED

```
═══════════════════════════════════════════════════
        PRE-TRADE CHECKLIST - FINAL VERIFICATION
═══════════════════════════════════════════════════

Trade: XYZ Mar $45 Straddle
Date: 2025-11-22 10:50:00
Position Size: 5 contracts
Portfolio Value: $100,000

---------------------------------------------------
SECTION 1: LIQUIDITY ❌
---------------------------------------------------
❌ Liquidity check: REJECTED
❌ Bid-ask spread: 17.4% (exceeds 0.5% limit)
❌ Volume: 35 contracts (below 100 minimum)
❌ Open interest: 248 (below 500 minimum)

Status: FAILED

---------------------------------------------------
SECTION 2: EVENT RISK ⚠️
---------------------------------------------------
⚠️ Earnings date: 4 days away (within 7-day blackout)
❌ Cannot trade before earnings unless earnings play

Status: FAILED

---------------------------------------------------
SECTION 3: CORRELATION ✓
---------------------------------------------------
✓ No correlation issues

Status: PASS

---------------------------------------------------
SECTION 4: POSITION SIZING ⚠️
---------------------------------------------------
✓ Position type: SPECULATIVE
⚠️ Position size: 2.2% (within limit but high for failed liquidity)
✓ Risk within limits

Status: MARGINAL

---------------------------------------------------
SECTION 5: MARKET ALIGNMENT ⚠️
---------------------------------------------------
⚠️ Market disposition: STRONG_BULL
⚠️ Trade: Neutral/volatility play (not aligned)
⚠️ Sector lagging (RS: -3.2%)

Status: MISALIGNED

---------------------------------------------------
SECTION 6: TECHNICAL SETUP ⚠️
---------------------------------------------------
⚠️ Price action: Choppy
⚠️ Near resistance

Status: WEAK

---------------------------------------------------
FINAL CHECKLIST SUMMARY
---------------------------------------------------

[❌] Liquidity: REJECTED - Critical failure
[❌] Event Risk: Earnings in 4 days - Blackout period
[✓] Correlation: Within limits
[⚠️] Position Size: Marginal
[⚠️] Market Alignment: Misaligned
[⚠️] Technical Setup: Weak
[✓] Risk/Reward: Acceptable
[✓] Portfolio Risk: OK
[✓] Execution: Possible

Passed: 4/9 checks
Failed: 2/9 checks
Warnings: 3/9 checks

═══════════════════════════════════════════════════
        STATUS: ❌ REJECTED - DO NOT EXECUTE
═══════════════════════════════════════════════════

CRITICAL FAILURES:
------------------
1. LIQUIDITY: Spread 17.4% - You lose 17% just entering
2. EVENT RISK: Earnings in 4 days - Inside blackout window

These are automatic disqualifiers.

ADDITIONAL CONCERNS:
--------------------
- Market disposition misalignment
- Weak technical setup
- Sector underperforming

RECOMMENDATION:
---------------
❌ DO NOT EXECUTE THIS TRADE

Alternative Actions:
1. Wait until after earnings (if still interested)
2. Find similar trade in liquid stock
3. PASS on this opportunity entirely (RECOMMENDED)

This trade violates critical safeguards and should not be executed
under any circumstances.
```

### JSON Output

```json
{
  "trade": {
    "ticker": "NVDA",
    "structure": "Jan 500/520 Call Vertical",
    "position_size": 2,
    "capital_required": 2400
  },
  "checklist_results": {
    "liquidity": {
      "status": "PASS",
      "checks": {
        "approved": true,
        "spread_within_limit": true,
        "volume_sufficient": true,
        "open_interest_sufficient": true
      }
    },
    "event_risk": {
      "status": "PASS",
      "earnings_days_away": 28,
      "high_impact_events": []
    },
    "correlation": {
      "status": "PASS",
      "single_ticker_exposure_pct": 2.4,
      "correlated_group_exposure_pct": 18,
      "high_correlations": []
    },
    "position_sizing": {
      "status": "PASS",
      "position_pct": 2.4,
      "max_allowed_pct": 10,
      "risk_pct": 2.4,
      "max_risk_pct": 3.0
    },
    "market_alignment": {
      "status": "PASS",
      "disposition": "STRONG_BULL",
      "trade_direction": "bullish",
      "aligned": true
    },
    "technical_setup": {
      "status": "PASS",
      "trend": "STRONG_UPTREND",
      "support_distance_pct": 2.5,
      "resistance_distance_pct": 3.5
    },
    "risk_reward": {
      "status": "PASS",
      "ratio": 1.33,
      "acceptable": true
    },
    "portfolio_risk": {
      "status": "PASS",
      "current_risk_pct": 4.2,
      "new_risk_pct": 2.4,
      "total_risk_pct": 6.6,
      "limit_pct": 15
    },
    "execution": {
      "status": "PASS",
      "market_open": true,
      "cash_available": 45000,
      "cash_required": 2400,
      "executable": true
    }
  },
  "summary": {
    "total_checks": 9,
    "passed": 9,
    "failed": 0,
    "warnings": 0,
    "final_status": "APPROVED"
  },
  "execution_plan": {
    "order_type": "VERTICAL_SPREAD",
    "limit_price": 12.00,
    "max_price": 12.50,
    "stop_loss": 8.00,
    "profit_targets": [16.00, 18.00]
  }
}
```

## Decision Rules

### Automatic Rejection (Any One = REJECT)

```
REJECT if ANY:

1. Liquidity check status != "APPROVED"
2. Bid-ask spread > 1.0%
3. Earnings within 7 days (unless earnings play)
4. Single ticker exposure > 15%
5. Correlated group exposure > 25%
6. Position size exceeds limits (10% core, 2% spec)
7. Position risk > 5% portfolio (absolute max)
8. Total portfolio risk > 15%
9. Risk/Reward < 1.0:1 (for non-premium selling)
10. Bullish trade in STRONG_BEAR (or vice versa) without justification
11. Insufficient cash/margin
12. Contract expiring < 7 days
```

### Warning Flags (Require Acknowledgment)

```
FLAG if:

1. Spread 0.5-1.0%
2. Earnings 7-14 days away
3. Moderate correlation (0.6-0.8)
4. Trade counter to disposition (needs justification)
5. R/R 1.0-1.5:1 (below preferred)
6. Total portfolio risk 10-15%
7. Technical setup marginal
```

### Approval Requirements

```
APPROVE only if:

1. ALL critical checks pass
2. No automatic rejection criteria met
3. Warnings acknowledged (if any)
4. Manual override documented (if applicable)
```

## Validation Checks

- [ ] All previous task outputs loaded correctly
- [ ] Checklist items evaluated in order
- [ ] Failed items halt process immediately
- [ ] Warnings logged and require acknowledgment
- [ ] Final status clearly communicated (APPROVED/REJECTED)

## Notes

- **This checklist is the final authority** - overrides intuition
- When in doubt, REJECT - there will be another trade
- Keep a log of rejected trades to avoid repeating mistakes
- Manual overrides should be <5% of trades and documented
- Review rejected trades monthly to improve process
- A "NO" today saves capital for "YES" tomorrow

## Related Tasks

- `safeguards/check_liquidity.task.md` - Provides liquidity check input
- `strategy/calculate_sizing.task.md` - Provides position size validation
- `strategy/fit_mechanism.task.md` - Provides trade structure and R/R
- `analysis/define_disposition.task.md` - Provides market regime alignment
- `portfolio/determine_needs.task.md` - Provides portfolio context
