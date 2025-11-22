# Fit Profit Mechanism

## Purpose

Match a ticker/trade idea to the appropriate profit mechanism and determine the optimal options structure. This ensures each trade is aligned with the underlying market inefficiency being exploited.

## Overview

Different market conditions and stock characteristics favor different profit mechanisms. This task analyzes the ticker's setup and current market regime to select the profit mechanism that maximizes edge, then recommends specific trade structures.

## Inputs

**Required:**
- `ticker`: Stock symbol to analyze
- `market_disposition`: Current disposition from define_disposition task
- `sector_relative_strength`: Sector RS from sector_stacking task
- `stock_technical_setup`: Price trend, volatility, momentum indicators

**Optional:**
- `earnings_date`: Next earnings announcement date
- `iv_rank`: Implied volatility percentile rank
- `current_portfolio_exposure`: Existing positions in ticker

**Reference Data:**
- `data/profit_mechanisms.json`: Mechanism definitions and ideal conditions

## Processing Logic

### Step 1: Load Profit Mechanisms

```
Load from data/profit_mechanisms.json:
- VRP (Variance Risk Premium)
- Momentum Drift
- Mean Reversion
- Earnings Volatility
```

### Step 2: Analyze Ticker Characteristics

**Trend Analysis:**

```
Classify current trend:
IF price > 20MA AND 20MA > 50MA AND 50MA > 200MA:
  trend_state = "STRONG_UPTREND"
ELSE IF price > 50MA AND 50MA > 200MA:
  trend_state = "UPTREND"
ELSE IF price > 200MA:
  trend_state = "WEAK_UPTREND"
ELSE IF price < 20MA AND 20MA < 50MA AND 50MA < 200MA:
  trend_state = "STRONG_DOWNTREND"
ELSE IF price < 50MA AND 50MA < 200MA:
  trend_state = "DOWNTREND"
ELSE:
  trend_state = "RANGE_BOUND"
```

**Volatility Analysis:**

```
Analyze implied vs realized volatility:
IF iv_rank provided:
  IF iv_rank > 70:
    vol_state = "HIGH_IV" (expensive options)
  ELSE IF iv_rank > 40:
    vol_state = "NORMAL_IV"
  ELSE:
    vol_state = "LOW_IV" (cheap options)

Calculate historical volatility (20-day):
realized_vol = STDEV(daily_returns) × SQRT(252)

IF iv_rank > 50 AND realized_vol < implied_vol × 0.8:
  vol_premium_state = "OVERPRICED" (favor selling)
ELSE IF iv_rank < 30 AND realized_vol > implied_vol × 1.2:
  vol_premium_state = "UNDERPRICED" (favor buying)
ELSE:
  vol_premium_state = "FAIR"
```

**Momentum Analysis:**

```
Calculate relative strength score (from sector_stacking):
IF stock_rs_vs_spy > 10%:
  momentum_state = "STRONG_MOMENTUM"
ELSE IF stock_rs_vs_spy > 5%:
  momentum_state = "MODERATE_MOMENTUM"
ELSE IF stock_rs_vs_spy > -5%:
  momentum_state = "NEUTRAL"
ELSE:
  momentum_state = "NEGATIVE_MOMENTUM"
```

### Step 3: Match to Profit Mechanism

**Decision Tree:**

```
Priority 1: Check for Event-Driven Opportunities
IF earnings_date AND days_to_earnings <= 30:
  IF iv_rank < 40:
    mechanism = "EARNINGS_VOLATILITY"
    rationale = "IV underpriced ahead of earnings catalyst"
    GOTO Step 4

Priority 2: Check for VRP Opportunities
IF vol_premium_state == "OVERPRICED" AND iv_rank > 60:
  IF trend_state IN ["RANGE_BOUND", "WEAK_UPTREND"]:
    mechanism = "VRP"
    rationale = "High IV in range-bound environment, sell premium"
    GOTO Step 4

Priority 3: Check for Momentum Opportunities
IF momentum_state IN ["STRONG_MOMENTUM", "MODERATE_MOMENTUM"]:
  IF trend_state IN ["STRONG_UPTREND", "UPTREND"]:
    IF market_disposition IN ["STRONG_BULL", "BULL"]:
      mechanism = "MOMENTUM_DRIFT"
      rationale = "Strong trend + high RS + bullish market = ride momentum"
      GOTO Step 4

Priority 4: Check for Mean Reversion Opportunities
IF trend_state == "RANGE_BOUND":
  IF price_deviation > 2_sigma FROM mean:
    mechanism = "MEAN_REVERSION"
    rationale = "Price extended from mean in range-bound market"
    GOTO Step 4

Default: No Clear Edge
IF no mechanism assigned:
  mechanism = "NO_EDGE"
  rationale = "Setup does not align with any proven mechanism"
  recommendation = "PASS on this trade"
```

### Step 4: Select Trade Structure

**Based on selected mechanism:**

**MOMENTUM_DRIFT Structures:**

```
Primary Structures (in order of preference):

1. Long Call Vertical (Bullish)
   - Buy lower strike ATM or slightly ITM call
   - Sell higher strike call (typically 5-10% above)
   - Expiration: 30-60 DTE
   - Risk/Reward: Defined risk, capped upside
   - When: High conviction + bullish momentum

2. Bull Call Spread (Bullish)
   - Similar to call vertical
   - Use when stock has moderate but not extreme momentum
   - Wider strikes for more upside potential

3. Synthetic Long
   - Buy ATM call + Sell ATM put (same strike, same expiration)
   - Acts like long stock with defined max loss
   - When: Very high conviction + want maximum upside
   - Risk: Higher than vertical spreads

Selection Logic:
IF momentum_state == "STRONG_MOMENTUM" AND conviction == "HIGH":
  structure = "LONG_CALL_VERTICAL"
  strike_selection = "ATM to +5% strike width"
ELSE IF momentum_state == "MODERATE_MOMENTUM":
  structure = "BULL_CALL_SPREAD"
  strike_selection = "Slightly OTM to +8% strike width"
```

**VRP (Variance Risk Premium) Structures:**

```
Primary Structures:

1. Short Strangle
   - Sell OTM call + Sell OTM put
   - Expiration: 30-45 DTE
   - Delta: Approx 16 delta each side (0.16 probability ITM)
   - When: High IV, range-bound market, neutral bias

2. Iron Condor
   - Short strangle + long wings for protection
   - Safer than naked strangle
   - Lower profit but defined risk
   - When: Want protection in uncertain market

3. Calendar Spread
   - Sell near-term option, buy longer-term option (same strike)
   - Profit from time decay differential
   - When: Expecting near-term range-bound, longer-term move

Selection Logic:
IF iv_rank > 70 AND account_allows_undefined_risk:
  structure = "SHORT_STRANGLE"
  strike_selection = "16 delta OTM on each side"
ELSE IF iv_rank > 60:
  structure = "IRON_CONDOR"
  strike_selection = "Short strikes at 16 delta, long wings at 5 delta"
ELSE:
  structure = "CALENDAR_SPREAD"
  strike_selection = "ATM strike, sell 30 DTE, buy 60 DTE"
```

**MEAN_REVERSION Structures:**

```
Primary Structures:

1. Long Calendar Spread
   - Sell front-month ATM option
   - Buy back-month ATM option
   - Profit from front-month decay + expected return to mean
   - When: Stock extended, expecting consolidation then resumption

2. Pairs Trade (Long/Short)
   - Long oversold stock + Short overbought stock (same sector)
   - Profit when spread normalizes
   - When: Clear relative value disparity in pair

3. Collar Strategy
   - Long stock + Short OTM call + Long OTM put
   - Hedged position waiting for mean reversion
   - When: Want to hold through reversion with protection

Selection Logic:
IF price > 2_sigma above mean:
  structure = "SHORT_CALL_CALENDAR"
  rationale = "Expecting pullback to mean"
ELSE IF price < 2_sigma below mean:
  structure = "LONG_CALL_CALENDAR"
  rationale = "Expecting bounce back to mean"
```

**EARNINGS_VOLATILITY Structures:**

```
Primary Structures:

1. Long Straddle (Pre-Earnings)
   - Buy ATM call + Buy ATM put
   - Profit from large move either direction
   - When: IV low + expected big move

2. Long Strangle
   - Buy OTM call + Buy OTM put
   - Cheaper than straddle, needs bigger move
   - When: Want to reduce cost, expect monster move

3. Call or Put Spread (Directional)
   - Directional bet with earnings catalyst
   - When: Have directional conviction + earnings catalyst

Selection Logic:
IF iv_rank < 30 AND historical_earnings_moves > 8%:
  structure = "LONG_STRADDLE"
  strike_selection = "ATM, expiration week after earnings"
ELSE IF iv_rank < 40:
  structure = "LONG_STRANGLE"
  strike_selection = "Strikes 1 SD away, expiration week after earnings"
```

### Step 5: Determine Conviction Level

```
Score components (0-10 each):
1. Mechanism alignment with market disposition
2. Technical setup quality
3. Relative strength vs sector/market
4. Risk/reward attractiveness
5. Liquidity and tradability

total_conviction_score = SUM(components) / 5

IF total_conviction_score >= 8:
  conviction = "HIGH"
  position_sizing_guide = "Core position, up to 10% portfolio"
ELSE IF total_conviction_score >= 6:
  conviction = "MODERATE"
  position_sizing_guide = "Standard position, 5-7% portfolio"
ELSE IF total_conviction_score >= 4:
  conviction = "LOW"
  position_sizing_guide = "Speculative position, 2-3% portfolio"
ELSE:
  conviction = "VERY_LOW"
  recommendation = "PASS - insufficient edge"
```

### Step 6: Generate Trade Plan

```
Create structured trade plan:
1. Ticker + Entry rationale
2. Profit mechanism + why it fits
3. Specific structure + strikes
4. Entry price range
5. Profit target (price or %)
6. Stop loss / exit criteria
7. Position size
8. Risk/reward ratio
9. Time horizon
```

## Output Format

### Console Output

```
PROFIT MECHANISM FITTING ANALYSIS
==================================
Ticker: NVDA
Analysis Date: 2025-11-22
Stock Price: $502.50

TICKER CHARACTERISTICS:
-----------------------
Trend State: STRONG_UPTREND ✓
  - Price ($502.50) > 20MA ($495) > 50MA ($485) > 200MA ($450)

Momentum State: STRONG_MOMENTUM ✓
  - RS vs SPY: +20.5%
  - RS vs Sector (XLK): +12.3%

Volatility State: NORMAL_IV
  - IV Rank: 42 (mid-range)
  - Realized Vol (20d): 28%
  - Implied Vol: 32%
  - Premium State: FAIR

Market Alignment:
  - Market Disposition: STRONG_BULL ✓
  - Sector (XLK) RS: +7.1% (Leading sector) ✓

PROFIT MECHANISM SELECTION:
===========================

Selected Mechanism: MOMENTUM_DRIFT 🚀

Rationale:
✓ Strong uptrend with price > all major MAs
✓ Exceptional relative strength (+20.5% vs SPY)
✓ Leading stock in leading sector
✓ Bull market disposition supports long bias
✓ No immediate event risk (earnings in 28 days)

Mechanism Details (from profit_mechanisms.json):
-------------------------------------------------
Description: Capture systematic price trends driven by behavioral
  factors, technical momentum, and trend-following strategies.

Ideal Conditions Match:
✓ Established Uptrend: YES
✓ Moderate-to-High Volatility: YES (IV rank 42)
✓ Strong Trending Market: YES
✓ High Trend Strength: YES (RS +20.5%)

RECOMMENDED TRADE STRUCTURE:
============================

Structure: LONG CALL VERTICAL (Bull Call Spread)

Specific Setup:
- BUY NVDA 500 Call
- SELL NVDA 520 Call
- Expiration: 45 DTE (January 2026 monthly)
- Net Debit: ~$12.00 per spread
- Max Profit: $8.00 per spread ($20 width - $12 cost)
- Max Loss: $12.00 per spread (debit paid)
- Breakeven: $512.00

Strike Selection Rationale:
- 500 strike: Slightly ITM (~55 delta) for good directional exposure
- 520 strike: ~35 delta, gives room for 3.5% move to max profit
- Width: $20 (4% of stock price) balances cost and profit potential

Position Metrics:
-----------------
Entry Range: $11.50 - $12.50 (current $12.00)
Profit Target: $16.00 - $18.00 (80-100% gain)
  → Achieved if NVDA reaches $516-$520 (2.7%-3.5% stock move)
Stop Loss: $8.00 (33% loss)
  → Trigger if NVDA breaks below $490 (20MA support)
Risk/Reward: 1:2.0 (risk $4 to make $8 at max profit)
Time Horizon: 3-5 weeks (close before final week decay)

CONVICTION ANALYSIS:
====================

Component Scores:
-----------------
1. Mechanism/Disposition Alignment: 10/10 ✓
   (Momentum in strong bull = perfect fit)

2. Technical Setup Quality: 10/10 ✓
   (Clean uptrend, all MAs aligned, above resistance)

3. Relative Strength: 10/10 ✓
   (Extreme outperformance, leading stock in leading sector)

4. Risk/Reward: 8/10 ✓
   (1:2 R/R with high probability)

5. Liquidity/Tradability: 10/10 ✓
   (NVDA options extremely liquid)

Total Conviction Score: 9.6/10

CONVICTION LEVEL: HIGH 🔥

Position Sizing Guide: CORE POSITION
- Allocate 8-10% of portfolio
- This is a foundational position, not speculative

TRADE PLAN SUMMARY:
===================

Setup: High-conviction momentum play in market leader

Entry:
  - Structure: NVDA Jan 500/520 Call Vertical
  - Entry Price: $11.50-$12.50 (current $12.00)
  - Position Size: 8-10% portfolio (calculate exact $ in sizing task)
  - Entry Timing: Enter within next 1-2 days, scale if needed

Targets:
  - T1 (50% position): $16.00 (80% gain) → Take profit on half
  - T2 (remaining 50%): $18.00 (100% gain) → Close remainder
  - Stock Target: $516-$520

Stops:
  - Hard Stop: $8.00 (33% loss)
  - Technical Stop: Close if NVDA closes below $490 (20MA)
  - Time Stop: Exit 7 days before expiration regardless

Risk Management:
  - Max Loss: $12.00/spread (debit paid) × # of spreads
  - Position will be sized to risk 2-3% of total portfolio
  - No earnings risk (28 days away, position will be closed)

Thesis Invalidation:
  - Break below 20MA ($495)
  - Sector rotation out of technology
  - Market disposition changes to bearish

Expected Holding Period: 3-5 weeks

Next Steps:
-----------
→ Run safeguards/check_liquidity to verify options liquidity
→ Run strategy/calculate_sizing to determine exact # of contracts
→ Run safeguards/pre_trade_checklist before execution
```

**Example: VRP Mechanism Output**

```
PROFIT MECHANISM FITTING ANALYSIS
==================================
Ticker: SPY
Analysis Date: 2025-11-22
Stock Price: $450.25

TICKER CHARACTERISTICS:
-----------------------
Trend State: WEAK_UPTREND
  - Price > 200MA but below recent highs
  - Consolidating in range $445-$455

Volatility State: HIGH_IV ⚠️
  - IV Rank: 72 (elevated)
  - Realized Vol (20d): 12%
  - Implied Vol: 18%
  - Premium State: OVERPRICED (IV >> Realized)

Market Alignment:
  - Market Disposition: NEUTRAL
  - Range-bound conditions

PROFIT MECHANISM SELECTION:
===========================

Selected Mechanism: VRP (Variance Risk Premium) 💰

Rationale:
✓ IV Rank at 72 = options expensive
✓ Realized volatility (12%) significantly below implied (18%)
✓ Market in consolidation range = ideal for premium selling
✓ VIX elevated but not crisis levels
✓ Neutral disposition supports range-trading

Mechanism Details:
-------------------------------------------------
Description: Profit from the difference between realized and
  implied volatility. Market overpays for volatility protection.

Ideal Conditions Match:
✓ Low Realized Volatility: YES (12%)
✓ VIX Below 20: NO (VIX at 22, but acceptable)
✓ Contango Term Structure: YES
✓ Range-Bound Market: YES

RECOMMENDED TRADE STRUCTURE:
============================

Structure: SHORT STRANGLE

Specific Setup:
- SELL SPY 465 Call (16 delta)
- SELL SPY 435 Put (16 delta)
- Expiration: 35 DTE
- Credit Received: ~$4.50 per strangle
- Max Profit: $4.50 (if SPY between 435-465 at expiration)
- Max Loss: Undefined (can be very large)
- Breakevens: $430.50 (downside), $469.50 (upside)
- Profit Range: 35 points / $450 = ~15.5% range

Position Metrics:
-----------------
Entry Range: $4.25 - $4.75 credit
Profit Target: $2.25 (50% max profit)
Management: Close at 50% profit OR 21 DTE, whichever first
Stop Loss: $9.00 debit (100% loss)
  → Or if SPY breaks out of range decisively
Risk/Reward: Undefined risk, manage actively

CONVICTION LEVEL: MODERATE

Position Sizing Guide: SMALL POSITION
- Max 2-3% portfolio risk
- Premium selling requires active management

⚠️ CRITICAL: Undefined risk structure - use strict position sizing
```

### JSON Output

```json
{
  "ticker": "NVDA",
  "analysis_date": "2025-11-22T12:00:00Z",
  "stock_price": 502.50,
  "characteristics": {
    "trend_state": "STRONG_UPTREND",
    "momentum_state": "STRONG_MOMENTUM",
    "volatility_state": "NORMAL_IV",
    "iv_rank": 42,
    "rs_vs_spy": 20.5,
    "rs_vs_sector": 12.3
  },
  "mechanism": {
    "id": "momentum_drift",
    "name": "Momentum Drift",
    "rationale": "Strong uptrend + exceptional RS + bull market",
    "conditions_met": [
      "established_uptrend",
      "high_trend_strength",
      "strong_trending_market"
    ]
  },
  "trade_structure": {
    "name": "LONG_CALL_VERTICAL",
    "details": {
      "buy_strike": 500,
      "sell_strike": 520,
      "expiration_dte": 45,
      "net_debit": 12.00,
      "max_profit": 8.00,
      "max_loss": 12.00,
      "breakeven": 512.00,
      "risk_reward_ratio": 2.0
    },
    "targets": {
      "profit_target_1": 16.00,
      "profit_target_2": 18.00,
      "stop_loss": 8.00
    }
  },
  "conviction": {
    "scores": {
      "alignment": 10,
      "technical_quality": 10,
      "relative_strength": 10,
      "risk_reward": 8,
      "liquidity": 10
    },
    "total_score": 9.6,
    "level": "HIGH",
    "position_type": "core",
    "sizing_guide": "8-10% portfolio"
  }
}
```

## Decision Rules

### Mechanism Selection Priority

```
1. EARNINGS_VOLATILITY - If earnings within 30 days AND IV rank < 40
2. VRP - If IV rank > 60 AND vol premium overpriced
3. MOMENTUM_DRIFT - If strong trend + high RS + aligned disposition
4. MEAN_REVERSION - If range-bound + price extended from mean
5. NO_EDGE - Pass on trade if no mechanism fits
```

### Structure Selection Within Mechanism

**Momentum Drift:**
- High conviction + high momentum → Long Call Vertical
- Moderate conviction → Bull Call Spread (wider strikes)
- Very high conviction + unlimited upside desired → Synthetic Long

**VRP:**
- IV rank > 70 + undefined risk OK → Short Strangle
- IV rank > 60 + want defined risk → Iron Condor
- IV rank 50-60 → Calendar Spread

**Mean Reversion:**
- Extended above mean → Short Call Calendar
- Extended below mean → Long Call Calendar
- Paired opportunity → Pairs Trade

**Earnings:**
- IV rank < 30 + big historical moves → Long Straddle
- IV rank < 40 + directional conviction → Directional Spread

### Override Conditions

```
Override to "NO_EDGE" if:
- Earnings within 7 days (too close)
- Liquidity insufficient (see check_liquidity task)
- Ticker correlation > 0.8 with existing position
- Mechanism conflicts with market disposition
- Technical setup quality score < 5/10
```

## Validation Checks

- [ ] Mechanism selection aligns with market disposition
- [ ] Recommended structure matches mechanism guidelines
- [ ] Strike selection follows mechanism rules
- [ ] Expiration timeframe appropriate for mechanism
- [ ] Risk/reward ratio is favorable (>1.5:1 preferred)
- [ ] Conviction score calculated correctly

## Notes

- Always reference `data/profit_mechanisms.json` for mechanism definitions
- Multiple mechanisms can apply - select the one with highest edge
- When in doubt between two mechanisms, choose the one aligned with market disposition
- Structure selection should balance conviction with risk management
- High conviction doesn't mean unlimited risk - always use defined risk structures unless experienced

## Related Tasks

- `analysis/sector_stacking.task.md` - Provides ticker candidates and RS data
- `strategy/calculate_sizing.task.md` - Determines exact position size
- `safeguards/check_liquidity.task.md` - Validates options are tradeable
- `safeguards/pre_trade_checklist.task.md` - Final approval before execution
