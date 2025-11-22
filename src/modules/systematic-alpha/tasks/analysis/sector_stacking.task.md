# Sector Stacking

## Purpose

Rank sectors by relative strength and identify the strongest stocks within the top-performing sector. This creates a "stacked" approach: best stocks in best sector, maximizing probability of success.

## Overview

Sector stacking is the core of relative strength analysis. Instead of picking stocks randomly across the market, we systematically identify leadership at the sector level, then drill down to find the strongest stocks within that sector. This approach stacks probabilities in our favor.

## Inputs

**Required:**
- `sector_etf_data`: Performance data for 9 major sector ETFs (20-60 day history)
  - XLK (Technology)
  - XLF (Financials)
  - XLE (Energy)
  - XLV (Healthcare)
  - XLI (Industrials)
  - XLY (Consumer Discretionary)
  - XLP (Consumer Staples)
  - XLU (Utilities)
  - XLB (Materials)
- `spy_data`: SPY benchmark data for relative comparison
- `market_disposition`: Current market disposition from define_disposition task

**Optional:**
- `stock_universe`: List of stocks to analyze within sectors (default: top 20 stocks by market cap per sector)
- `lookback_period`: Days for relative strength calculation (default: 20 days)

## Processing Logic

### Step 1: Calculate Sector Relative Strength

**For each sector ETF:**

```
Calculate returns over lookback period:
sector_return = (current_price - price_N_days_ago) / price_N_days_ago * 100

Calculate SPY benchmark return:
spy_return = (spy_current - spy_N_days_ago) / spy_N_days_ago * 100

Relative Strength Score:
rs_score = sector_return - spy_return

Interpretation:
- Positive RS: Sector outperforming market
- Negative RS: Sector underperforming market
```

**Multiple Timeframe Analysis:**

```
Calculate RS scores for multiple periods:
- RS_20: 20-day relative strength
- RS_40: 40-day relative strength
- RS_60: 60-day relative strength

Composite RS Score:
composite_rs = (RS_20 × 0.5) + (RS_40 × 0.3) + (RS_60 × 0.2)

Weighting rationale:
- Recent strength (20d) = 50% weight (most important)
- Intermediate (40d) = 30% weight (confirms trend)
- Longer-term (60d) = 20% weight (validates sustainability)
```

### Step 2: Rank Sectors by Relative Strength

```
Sort sectors by composite_rs in descending order:
1. Highest RS = Strongest sector (LEADER)
2. Second highest = Secondary leader
...
9. Lowest RS = Weakest sector (LAGGARD)

Categorize sectors:
IF composite_rs > 5%:
  category = "STRONG_LEADER"
ELSE IF composite_rs > 2%:
  category = "LEADER"
ELSE IF composite_rs > -2%:
  category = "INLINE"
ELSE IF composite_rs > -5%:
  category = "LAGGARD"
ELSE:
  category = "STRONG_LAGGARD"
```

### Step 3: Assess Sector Trend Quality

**For the top 3 sectors, evaluate trend quality:**

```
Price vs Moving Averages:
IF sector_price > SMA_20 AND SMA_20 > SMA_50:
  trend_quality = "CLEAN_UPTREND"
  quality_score = 10
ELSE IF sector_price > SMA_20:
  trend_quality = "EMERGING_UPTREND"
  quality_score = 7
ELSE IF sector_price > SMA_50:
  trend_quality = "CHOPPY"
  quality_score = 5
ELSE:
  trend_quality = "DOWNTREND"
  quality_score = 0

Volatility Assessment:
Calculate 20-day standard deviation of returns:
IF std_dev < sector_median_std_dev:
  volatility_quality = "SMOOTH" (preferred)
ELSE:
  volatility_quality = "CHOPPY" (caution)
```

### Step 4: Filter Sectors by Market Disposition

```
Align sector selection with market disposition:

IF market_disposition IN ["STRONG_BULL", "BULL"]:
  preferred_sectors = ["XLK", "XLY", "XLI"] (Growth sectors)
  avoid_sectors = ["XLU", "XLP"] (Defensives)

ELSE IF market_disposition == "NEUTRAL":
  preferred_sectors = ALL sectors with positive RS
  avoid_sectors = Sectors with RS < -3%

ELSE IF market_disposition IN ["BEAR", "STRONG_BEAR"]:
  preferred_sectors = ["XLU", "XLP", "XLV"] (Defensives)
  avoid_sectors = ["XLK", "XLY"] (Growth)

Apply filter:
IF top_sector IN avoid_sectors:
  WARNING: "Top sector conflicts with market disposition"
  recommendation = "Proceed with caution or select next sector"
```

### Step 5: Identify Strongest Stocks Within Top Sector

**For stocks in the #1 ranked sector:**

```
FOR each stock in sector_stock_list:

  Calculate stock relative strength vs sector ETF:
  stock_return_20d = (stock_price - stock_price_20d_ago) / stock_price_20d_ago
  sector_return_20d = (sector_etf_price - sector_etf_20d_ago) / sector_etf_20d_ago

  stock_rs_vs_sector = stock_return_20d - sector_return_20d

  Calculate stock relative strength vs SPY:
  stock_rs_vs_spy = stock_return_20d - spy_return_20d

Rank stocks by composite score:
stock_composite_score = (stock_rs_vs_sector × 0.6) + (stock_rs_vs_spy × 0.4)

Filter criteria:
- stock_composite_score > 0 (outperforming both sector and market)
- stock_price > 50MA > 200MA (technical strength)
- average_volume > 500,000 shares (liquidity requirement)
```

### Step 6: Apply Quality Filters

```
FOR each top-ranked stock:

  Technical Quality Check:
  - [ ] Price above all major MAs (20, 50, 200)
  - [ ] No recent earnings within 7 days (avoid event risk)
  - [ ] No major resistance within 3% overhead
  - [ ] Volume above 20-day average (accumulation)

  Fundamental Quality (Optional):
  - [ ] Market cap > $10 billion (institutional quality)
  - [ ] Positive earnings growth
  - [ ] Sector-leading company

Quality Score:
quality_score = COUNT(criteria met) / COUNT(total criteria) × 100

Final Ranking:
final_score = (stock_composite_score × 0.7) + (quality_score × 0.3)
```

### Step 7: Generate Top Picks

```
Select top 3-5 stocks with highest final_score

FOR each selected stock:
  - Verify liquidity (bid/ask spread < 0.5%)
  - Confirm no immediate earnings
  - Check for recent insider buying (positive signal)
  - Note any upcoming catalysts (product launches, etc.)
```

## Output Format

### Console Output

```
SECTOR STACKING ANALYSIS
========================
Analysis Date: 2025-11-22
Market Disposition: STRONG_BULL
Lookback Period: 20 days

SECTOR RANKINGS:
================

1. Technology (XLK) ⭐ STRONG_LEADER
   ------------------------------------
   RS vs SPY: +8.2% (20d), +6.5% (40d), +5.1% (60d)
   Composite RS: +7.1%
   Trend Quality: CLEAN_UPTREND (10/10)
   Volatility: SMOOTH

   Disposition Alignment: ✓ ALIGNED (Growth sector in bull market)
   Recommendation: PRIMARY TARGET SECTOR

2. Consumer Discretionary (XLY) ⭐ LEADER
   ------------------------------------
   RS vs SPY: +5.8% (20d), +4.2% (40d), +3.1% (60d)
   Composite RS: +4.8%
   Trend Quality: CLEAN_UPTREND (10/10)
   Volatility: SMOOTH

   Disposition Alignment: ✓ ALIGNED
   Recommendation: SECONDARY TARGET

3. Industrials (XLI) - LEADER
   ------------------------------------
   RS vs SPY: +3.5% (20d), +2.8% (40d), +2.2% (60d)
   Composite RS: +2.9%
   Trend Quality: EMERGING_UPTREND (7/10)
   Volatility: CHOPPY

   Disposition Alignment: ✓ ALIGNED
   Recommendation: TERTIARY CONSIDERATION

4. Healthcare (XLV) - INLINE
   RS vs SPY: +0.5%

5. Financials (XLF) - INLINE
   RS vs SPY: -0.8%

6. Materials (XLB) - LAGGARD
   RS vs SPY: -2.3%

7. Energy (XLE) - LAGGARD
   RS vs SPY: -3.5%

8. Consumer Staples (XLP) - STRONG_LAGGARD
   RS vs SPY: -4.2%

9. Utilities (XLU) - STRONG_LAGGARD
   RS vs SPY: -5.1%

===============================================

TOP STOCK PICKS IN TECHNOLOGY (XLK):
====================================

1. NVDA (NVIDIA Corp) 🏆
   ----------------------
   Price: $502.50
   RS vs XLK: +12.3%
   RS vs SPY: +20.5%
   Composite Score: 95.2

   Technical Status:
   ✓ Price > 20MA ($495) > 50MA ($485) > 200MA ($450)
   ✓ Volume: 125% of 20-day average (accumulation)
   ✓ No earnings for 28 days
   ✓ Broke above resistance at $495

   Quality Metrics:
   ✓ Market Cap: $1.2T (mega-cap leader)
   ✓ Liquidity: Excellent (50M+ daily volume)
   ✓ Bid/Ask: $0.02 (0.004%)

   Rating: STRONG BUY for momentum trades

2. MSFT (Microsoft Corp) 🏆
   ----------------------
   Price: $375.20
   RS vs XLK: +6.8%
   RS vs SPY: +15.0%
   Composite Score: 88.5

   Technical Status:
   ✓ Price > 20MA ($372) > 50MA ($365) > 200MA ($350)
   ✓ Volume: 110% of average
   ✓ No earnings for 21 days
   ✓ Clean uptrend, no overhead resistance

   Quality Metrics:
   ✓ Market Cap: $2.8T (mega-cap)
   ✓ Liquidity: Excellent
   ✓ Institutional favorite

   Rating: BUY for core positions

3. AAPL (Apple Inc)
   ----------------------
   Price: $182.50
   RS vs XLK: +4.2%
   RS vs SPY: +12.4%
   Composite Score: 82.1

   Technical Status:
   ✓ Price > 20MA > 50MA > 200MA
   ✓ Volume: Normal
   ⚠️ Minor resistance at $185
   ✓ No earnings for 35 days

   Quality Metrics:
   ✓ Market Cap: $2.9T
   ✓ Liquidity: Excellent

   Rating: BUY (slightly behind leaders)

4. AMD (Advanced Micro Devices)
   ----------------------
   Price: $155.75
   RS vs XLK: +3.8%
   RS vs SPY: +12.0%
   Composite Score: 78.5

   ⚠️ Higher volatility than NVDA/MSFT
   ✓ Strong trend in place

   Rating: SPECULATIVE BUY

5. AVGO (Broadcom)
   ----------------------
   Price: $925.30
   RS vs XLK: +3.2%
   RS vs SPY: +11.4%
   Composite Score: 75.8

   Rating: HOLD/WATCH (just outside top tier)

===============================================

TRADE RECOMMENDATIONS:
======================

PRIMARY SETUP: NVDA
- Structure: Long call vertical (momentum mechanism)
- Entry: Current price $502-505
- Target: $525-530 (5% move)
- Stop: Below $490 (20MA support)
- Size: Core position (10% portfolio max)

SECONDARY SETUP: MSFT
- Structure: Long call vertical or stock
- Entry: Pullback to $370-372 preferred
- Target: $390-395
- Size: Core position (10% portfolio max)

ALTERNATIVE: XLK ETF
- If individual stocks too concentrated
- Get exposure to entire sector
- Lower risk, lower return

AVOID:
❌ Utilities (XLU) - Wrong sector for bull market
❌ Consumer Staples (XLP) - Defensive, underperforming
❌ Energy (XLE) - Weak relative strength
```

### JSON Output

```json
{
  "analysis_date": "2025-11-22T11:00:00Z",
  "market_disposition": "STRONG_BULL",
  "lookback_period": 20,
  "sector_rankings": [
    {
      "rank": 1,
      "ticker": "XLK",
      "name": "Technology",
      "rs_20d": 8.2,
      "rs_40d": 6.5,
      "rs_60d": 5.1,
      "composite_rs": 7.1,
      "category": "STRONG_LEADER",
      "trend_quality": "CLEAN_UPTREND",
      "trend_quality_score": 10,
      "disposition_aligned": true,
      "recommendation": "PRIMARY_TARGET"
    }
  ],
  "top_stocks": [
    {
      "rank": 1,
      "ticker": "NVDA",
      "name": "NVIDIA Corp",
      "price": 502.50,
      "rs_vs_sector": 12.3,
      "rs_vs_spy": 20.5,
      "composite_score": 95.2,
      "technical_status": {
        "above_20ma": true,
        "above_50ma": true,
        "above_200ma": true,
        "volume_accumulation": true,
        "earnings_clear": true
      },
      "quality_score": 100,
      "rating": "STRONG_BUY",
      "trade_recommendation": {
        "structure": "long_call_vertical",
        "mechanism": "momentum_drift",
        "entry": "502-505",
        "target": "525-530",
        "stop": 490,
        "position_type": "core"
      }
    }
  ],
  "avoid_sectors": ["XLU", "XLP", "XLE"]
}
```

## Decision Rules

### Sector Selection Priority

```
Priority 1: Disposition-aligned sector with highest RS
Priority 2: Non-conflicting sector with RS > 3%
Priority 3: Any sector with clean uptrend, even if lower RS
```

### Stock Selection Thresholds

```
Minimum Requirements:
- RS vs sector: > 0%
- RS vs SPY: > 2%
- Quality score: > 60%
- Liquidity: > 500K shares daily volume
- Price > $20 (avoid penny stocks)
```

### When to Override Top Sector

```
Override if:
- Top sector conflicts with disposition (e.g., XLU leading in bull market)
- Top sector trend quality score < 5
- Top sector lacks tradeable stocks meeting quality criteria
- Top sector has elevated volatility (>2x median)

Action: Move to next ranked sector that passes all criteria
```

## Validation Checks

- [ ] All 9 sectors included in analysis
- [ ] RS calculations use consistent timeframes
- [ ] Composite scores weighted correctly
- [ ] Stock universe includes sufficient candidates
- [ ] Quality filters applied consistently
- [ ] Top picks have sufficient liquidity

## Example Use Cases

**Scenario 1: Clear Bull Market**
- Market Disposition: STRONG_BULL
- Top Sector: XLK (Technology) +7.1% RS
- Top Stock: NVDA +20.5% RS vs SPY
- **Action:** Aggressive long position in NVDA using call spreads

**Scenario 2: Sector Conflict**
- Market Disposition: BEAR
- Top Sector by RS: XLK +2.1%
- **Conflict:** Growth sector shouldn't lead in bear market
- **Action:** Skip XLK, use #2 sector (defensive) or wait

**Scenario 3: Neutral Market**
- Market Disposition: NEUTRAL
- Top 3 sectors all within 1% RS
- **Action:** Pick sector with cleanest trend, smaller position sizes

## Notes

- Sector rotation is a leading indicator of market regime change
- If defensives (XLU, XLP) start leading, market regime may be shifting bearish
- Update sector rankings weekly at minimum
- Stock picks within sector should be updated when entering new positions
- Relative strength is NOT the same as absolute return (sector can be down but still outperforming)

## Related Tasks

- `analysis/define_disposition.task.md` - Provides market disposition input
- `strategy/fit_mechanism.task.md` - Determines trade structure for selected stocks
- `safeguards/check_liquidity.task.md` - Validates stocks are tradeable
