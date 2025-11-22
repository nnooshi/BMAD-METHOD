# Define Market Disposition

## Purpose

Assess the overall market environment and regime to determine whether the market disposition is Bullish, Bearish, or Neutral. This foundational analysis guides all subsequent trading decisions, position sizing, and strategy selection.

## Overview

Market disposition combines technical analysis, economic indicators, and sector trends to create a holistic view of market conditions. This is the strategic "North Star" that aligns all trading activities with the current market regime.

## Inputs

**Required:**
- `spy_price_history`: SPY price data (daily, last 90 days minimum)
- `vix_current`: Current VIX level
- `sector_etf_data`: Sector ETF performance data (XLK, XLF, XLE, XLV, XLI, XLY, XLP, XLU, XLB)

**Optional:**
- `economic_indicators`: GDP growth, unemployment, inflation data
- `fed_policy_stance`: Current and expected Fed policy
- `market_breadth`: Advance/decline line, new highs/lows
- `sentiment_indicators`: Put/call ratio, AAII sentiment

## Processing Logic

### Step 1: Technical Market Analysis

**Price Trend Assessment:**

```
Calculate moving averages:
- SMA_20 = 20-day simple moving average of SPY
- SMA_50 = 50-day simple moving average
- SMA_200 = 200-day simple moving average

Trend Rules:
IF (SPY > SMA_20) AND (SMA_20 > SMA_50) AND (SMA_50 > SMA_200):
  trend_signal = "STRONG_UPTREND" (+3 points)
ELSE IF (SPY > SMA_50) AND (SMA_50 > SMA_200):
  trend_signal = "UPTREND" (+2 points)
ELSE IF (SPY > SMA_200):
  trend_signal = "WEAK_UPTREND" (+1 point)
ELSE IF (SPY < SMA_20) AND (SMA_20 < SMA_50) AND (SMA_50 < SMA_200):
  trend_signal = "STRONG_DOWNTREND" (-3 points)
ELSE IF (SPY < SMA_50) AND (SMA_50 < SMA_200):
  trend_signal = "DOWNTREND" (-2 points)
ELSE IF (SPY < SMA_200):
  trend_signal = "WEAK_DOWNTREND" (-1 point)
ELSE:
  trend_signal = "CHOPPY" (0 points)
```

**Momentum Assessment:**

```
Calculate RSI (14-day):
IF RSI > 60:
  momentum_signal = "BULLISH" (+1 point)
ELSE IF RSI < 40:
  momentum_signal = "BEARISH" (-1 point)
ELSE:
  momentum_signal = "NEUTRAL" (0 points)
```

### Step 2: Volatility Regime Assessment

```
VIX Analysis:
IF VIX < 15:
  volatility_regime = "LOW_VOL"
  vol_signal = "BULLISH" (+1 point)
  environment = "Complacent, favorable for long positions"
ELSE IF VIX >= 15 AND VIX < 20:
  volatility_regime = "NORMAL_VOL"
  vol_signal = "NEUTRAL" (0 points)
  environment = "Normal conditions"
ELSE IF VIX >= 20 AND VIX < 30:
  volatility_regime = "ELEVATED_VOL"
  vol_signal = "CAUTION" (-1 point)
  environment = "Elevated uncertainty, reduce size"
ELSE IF VIX >= 30:
  volatility_regime = "HIGH_VOL"
  vol_signal = "BEARISH" (-2 points)
  environment = "Fear regime, defensive positioning"
```

**VIX Trend:**

```
IF VIX < VIX_20_day_average:
  vix_trend = "DECLINING" (+1 point, bullish)
ELSE:
  vix_trend = "RISING" (-1 point, bearish)
```

### Step 3: Sector Analysis

**Sector Rotation Assessment:**

```
Calculate sector returns (last 20 days):
FOR each sector_etf:
  sector_return = (current_price - price_20_days_ago) / price_20_days_ago

Count sectors with positive returns:
bullish_sector_count = COUNT(sector_return > 0)

Sector Breadth Signal:
IF bullish_sector_count >= 7 (out of 9):
  sector_signal = "BROAD_STRENGTH" (+2 points)
ELSE IF bullish_sector_count >= 5:
  sector_signal = "MODERATE_STRENGTH" (+1 point)
ELSE IF bullish_sector_count <= 2:
  sector_signal = "BROAD_WEAKNESS" (-2 points)
ELSE IF bullish_sector_count <= 4:
  sector_signal = "MODERATE_WEAKNESS" (-1 point)
ELSE:
  sector_signal = "MIXED" (0 points)
```

**Leadership Quality:**

```
Identify top performing sector:
IF top_sector IN [XLK (Tech), XLY (Consumer Discretionary)]:
  leadership_signal = "GROWTH_LEADING" (+1 point, bullish)
ELSE IF top_sector IN [XLU (Utilities), XLP (Consumer Staples)]:
  leadership_signal = "DEFENSIVE_LEADING" (-1 point, bearish)
ELSE:
  leadership_signal = "NEUTRAL" (0 points)
```

### Step 4: Economic Overview (Optional Enhancement)

```
IF economic_indicators provided:
  GDP Growth:
    IF gdp_growth > 2.5%: econ_signal += 1
    IF gdp_growth < 1.0%: econ_signal -= 1

  Unemployment:
    IF unemployment < 4.5%: econ_signal += 1
    IF unemployment > 6.0%: econ_signal -= 1

  Inflation:
    IF inflation > 4%: econ_signal -= 1 (risk of hawkish Fed)
    IF inflation < 2%: econ_signal += 1 (accommodative policy)
ELSE:
  econ_signal = 0
```

### Step 5: Aggregate Score and Determine Disposition

```
total_score = trend_signal + momentum_signal + vol_signal + vix_trend + sector_signal + leadership_signal + econ_signal

Disposition Determination:
IF total_score >= 5:
  market_disposition = "STRONG_BULL"
  recommended_delta_target = +60 SPY shares
  stance = "Aggressive long positions, full risk-on"

ELSE IF total_score >= 2:
  market_disposition = "BULL"
  recommended_delta_target = +40 SPY shares
  stance = "Moderately bullish, favor long setups"

ELSE IF total_score >= -1:
  market_disposition = "NEUTRAL"
  recommended_delta_target = 0 SPY shares
  stance = "Balanced, opportunistic both directions"

ELSE IF total_score >= -4:
  market_disposition = "BEAR"
  recommended_delta_target = -40 SPY shares
  stance = "Moderately bearish, favor short/hedge setups"

ELSE:
  market_disposition = "STRONG_BEAR"
  recommended_delta_target = -60 SPY shares
  stance = "Defensive, aggressive hedging, reduce exposure"
```

### Step 6: Generate Confidence Score

```
Count number of signals pointing same direction:
aligned_signals = COUNT(signals with same sign as total_score)
total_signals = COUNT(all signals evaluated)

confidence = (aligned_signals / total_signals) * 100

IF confidence >= 80%:
  conviction = "HIGH"
ELSE IF confidence >= 60%:
  conviction = "MODERATE"
ELSE:
  conviction = "LOW"
```

## Output Format

### Console Output

```
MARKET DISPOSITION ANALYSIS
===========================
Analysis Date: 2025-11-22
SPY Price: $450.25

TECHNICAL SIGNALS:
------------------
Trend: STRONG_UPTREND (+3) ✓
  - SPY > 20MA ($448) > 50MA ($442) > 200MA ($430)
Momentum: BULLISH (+1) ✓
  - RSI(14): 62.5
Volatility: NORMAL_VOL (0)
  - VIX: 16.2 (declining, +1) ✓

SECTOR ANALYSIS:
----------------
Sector Breadth: BROAD_STRENGTH (+2) ✓
  - 7 of 9 sectors positive over 20 days
Leadership: GROWTH_LEADING (+1) ✓
  - Top Sector: XLK (Technology) +8.5%
  - Technology and Consumer Discretionary leading

AGGREGATE ASSESSMENT:
--------------------
Total Score: +8 out of 10 possible

MARKET DISPOSITION: STRONG_BULL 🐂

Confidence: 85% (HIGH)
Regime: Healthy uptrend with broad participation

RECOMMENDED STANCE:
-------------------
✓ Aggressive long positioning
✓ Target Delta: +60 SPY shares
✓ Risk-On environment
✓ Favor growth sectors and momentum strategies

STRATEGIC GUIDANCE:
-------------------
1. Primary Strategy: Momentum trades in leading sectors
2. Position Sizing: Core positions at 10% max
3. Hedge Strategy: Minimal hedging, keep 5-10% portfolio in protection
4. Profit Mechanisms:
   - PRIMARY: Momentum Drift (long call spreads)
   - SECONDARY: VRP (sell premium in low vol)
5. Sectors to Focus: Technology (XLK), Consumer Discretionary (XLY)

RISK CONSIDERATIONS:
--------------------
⚠️ Monitor for VIX spike above 20
⚠️ Watch for SPY break below 20MA ($448)
⚠️ Sector rotation into defensives would be early warning
```

**Example: Bearish Disposition**

```
MARKET DISPOSITION ANALYSIS
===========================
Analysis Date: 2025-11-22
SPY Price: $425.50

TECHNICAL SIGNALS:
------------------
Trend: DOWNTREND (-2) ✗
  - SPY < 50MA ($432) < 200MA ($438)
Momentum: BEARISH (-1) ✗
  - RSI(14): 38.2
Volatility: ELEVATED_VOL (-1) ✗
  - VIX: 24.5 (rising, -1) ✗

SECTOR ANALYSIS:
----------------
Sector Breadth: BROAD_WEAKNESS (-2) ✗
  - 2 of 9 sectors positive (only XLU, XLP)
Leadership: DEFENSIVE_LEADING (-1) ✗
  - Top Sector: XLU (Utilities) +2.1%
  - Flight to safety underway

AGGREGATE ASSESSMENT:
--------------------
Total Score: -8 out of 10 possible

MARKET DISPOSITION: STRONG_BEAR 🐻

Confidence: 90% (HIGH)
Regime: Deteriorating trend with defensive rotation

RECOMMENDED STANCE:
-------------------
⚠️ Defensive positioning required
✓ Target Delta: -60 SPY shares
✓ Risk-Off environment
✓ Focus on hedging and capital preservation

STRATEGIC GUIDANCE:
-------------------
1. Primary Strategy: Reduce long exposure, add hedges
2. Position Sizing: Cut speculative positions to 1% max
3. Hedge Strategy: Maintain 20-30% portfolio in SPY/QQQ puts
4. Profit Mechanisms:
   - PRIMARY: Mean Reversion (sell bounces)
   - SECONDARY: VRP (elevated vol environment)
5. Sectors to Avoid: Technology, Consumer Discretionary
6. Sectors to Consider: Utilities, Consumer Staples, Healthcare

RISK CONSIDERATIONS:
--------------------
✓ Already positioned defensively
⚠️ Watch for capitulation (VIX >30) - potential oversold bounce
⚠️ Fed intervention or policy shift could reverse trend quickly
```

### JSON Output

```json
{
  "analysis_date": "2025-11-22T10:00:00Z",
  "spy_price": 450.25,
  "signals": {
    "technical": {
      "trend": {
        "value": "STRONG_UPTREND",
        "score": 3,
        "details": "SPY > 20MA > 50MA > 200MA"
      },
      "momentum": {
        "value": "BULLISH",
        "score": 1,
        "rsi": 62.5
      }
    },
    "volatility": {
      "regime": "NORMAL_VOL",
      "vix_current": 16.2,
      "vix_trend": "DECLINING",
      "score": 1
    },
    "sectors": {
      "breadth": {
        "value": "BROAD_STRENGTH",
        "score": 2,
        "positive_count": 7
      },
      "leadership": {
        "value": "GROWTH_LEADING",
        "score": 1,
        "top_sector": "XLK",
        "top_sector_return": 8.5
      }
    }
  },
  "disposition": {
    "total_score": 8,
    "classification": "STRONG_BULL",
    "confidence": 85,
    "conviction": "HIGH",
    "recommended_delta_target": 60,
    "stance": "Aggressive long positions, full risk-on"
  },
  "recommendations": {
    "primary_strategy": "Momentum trades in leading sectors",
    "position_sizing": "Core positions at 10% max",
    "hedge_strategy": "Minimal hedging, keep 5-10% portfolio in protection",
    "primary_mechanism": "momentum_drift",
    "secondary_mechanism": "vrp",
    "focus_sectors": ["XLK", "XLY"]
  }
}
```

## Decision Rules

### Score Interpretation

| Total Score | Disposition | Delta Target | Environment |
|-------------|-------------|--------------|-------------|
| +7 to +10   | STRONG_BULL | +60 shares   | Risk-On, aggressive |
| +2 to +6    | BULL        | +40 shares   | Moderately bullish |
| -1 to +1    | NEUTRAL     | 0 shares     | Balanced, selective |
| -6 to -2    | BEAR        | -40 shares   | Moderately bearish |
| -10 to -7   | STRONG_BEAR | -60 shares   | Risk-Off, defensive |

### Regime Change Detection

```
IF disposition changes from BULL → BEAR or vice versa:
  ALERT: "Major regime change detected"
  ACTION: Review all open positions
  ACTION: Adjust portfolio delta targets
  ACTION: Update profit mechanism priorities
```

### Override Conditions

```
IF VIX > 35 (panic):
  disposition = "CRISIS" (override all other signals)
  recommended_action = "Preserve capital, minimal exposure"

IF SPY < 200MA AND VIX > 25:
  disposition_override = "Add BEAR bias regardless of score"
```

## Validation Checks

- [ ] All moving averages calculated from sufficient data (>200 days)
- [ ] VIX is current market value (<5 minutes old)
- [ ] Sector data includes all 9 major sectors
- [ ] Score components sum correctly
- [ ] Confidence calculation is mathematically sound
- [ ] Recommended delta target aligns with disposition

## Notes

- Update disposition analysis weekly or when major market events occur
- Disposition drives ALL downstream trading decisions
- When signals are mixed (low confidence), reduce position sizes
- Disposition is descriptive (what IS) not predictive (what WILL BE)
- Use disposition to filter trade ideas, not generate them

## Related Tasks

- `portfolio/determine_needs.task.md` - Uses disposition to set target delta
- `analysis/sector_stacking.task.md` - Identifies sectors aligned with disposition
- `strategy/fit_mechanism.task.md` - Selects strategies matching market regime
