# Market Disposition Analysis Report

**Report Generated:** {{generated_timestamp}}
**Analysis Period:** {{analysis_period_start}} to {{analysis_period_end}}
**Market Regime:** {{market_regime}}

---

## Executive Summary

- **Overall Market Sentiment:** {{market_sentiment}}
- **Volatility Regime:** {{volatility_regime}}
- **Liquidity Assessment:** {{liquidity_assessment}}
- **Trading Signal Strength:** {{signal_strength}}

---

## Economic Overview

### Macroeconomic Indicators

| Indicator | Current | Previous | Change | 3M Trend | Assessment |
|-----------|---------|----------|--------|----------|------------|
{{#macro_indicators}}
| {{indicator_name}} | {{current_value}} | {{previous_value}} | {{change}} | {{trend}} | {{assessment}} |
{{/macro_indicators}}

### Key Economic Drivers

**Growth Outlook:**
- GDP Growth Rate: {{gdp_growth}}
- Employment Status: {{employment_status}}
- Inflation Trajectory: {{inflation_trajectory}}

**Monetary Policy:**
- Current Rate Environment: {{rate_environment}}
- Expected Rate Changes: {{expected_rate_changes}}
- Central Bank Stance: {{cb_stance}}

**Credit Conditions:**
- Credit Spreads: {{credit_spreads}}
- Lending Standards: {{lending_standards}}
- Risk Appetite: {{risk_appetite}}

---

## Sector Rankings

### Performance Ranking

| Rank | Sector | YTD Return | 1M Return | Relative Strength | Momentum | Outlook |
|------|--------|------------|-----------|-------------------|----------|---------|
{{#sector_rankings}}
| {{rank}} | {{sector}} | {{ytd_return}} | {{one_m_return}} | {{rel_strength}} | {{momentum}} | {{outlook}} |
{{/sector_rankings}}

### Sector Rotation Signals

| From Sector | To Sector | Signal Strength | Catalyst | Timeline |
|------------|-----------|-----------------|-----------|----------|
{{#rotation_signals}}
| {{from_sector}} | {{to_sector}} | {{strength}} | {{catalyst}} | {{timeline}} |
{{/rotation_signals}}

### Sector Health Metrics

**Leading Sectors:**
- Sector: {{leading_sector1}}, Relative Strength: {{rs_score1}}
- Sector: {{leading_sector2}}, Relative Strength: {{rs_score2}}

**Lagging Sectors:**
- Sector: {{lagging_sector1}}, Relative Strength: {{rs_score3}}
- Sector: {{lagging_sector2}}, Relative Strength: {{rs_score4}}

---

## Volatility Analysis

### Volatility Metrics

| Metric | Current | 20D Average | 60D Average | Percentile | Assessment |
|--------|---------|------------|------------|-----------|------------|
{{#vol_metrics}}
| {{metric_name}} | {{current}} | {{avg_20d}} | {{avg_60d}} | {{percentile}} | {{assessment}} |
{{/vol_metrics}}

### Volatility Drivers

**Near-term Catalysts:**
- Event: {{catalyst1}}, Expected Move: {{expected_move1}}, Probability: {{prob1}}
- Event: {{catalyst2}}, Expected Move: {{expected_move2}}, Probability: {{prob2}}

**Implied vs Realized:**
- Current IV: {{current_iv}}
- 30-Day Realized Vol: {{realized_vol_30d}}
- IV vs Realized Spread: {{iv_realized_spread}}
- Trading Implication: {{vol_implication}}

**Volatility Structure:**
- Near-Term (0-30 days): {{vol_near_term}}
- Medium-Term (30-90 days): {{vol_medium_term}}
- Long-Term (90+ days): {{vol_long_term}}
- Skew Assessment: {{skew_assessment}}

---

## Watchlist

### High Priority Watch

| Ticker | Sector | Trigger Condition | Entry Level | Target | Stop | Rationale |
|--------|--------|------------------|-------------|--------|------|-----------|
{{#watchlist_high}}
| {{ticker}} | {{sector}} | {{condition}} | {{entry}} | {{target}} | {{stop}} | {{rationale}} |
{{/watchlist_high}}

### Secondary Watch

| Ticker | Sector | Watch Reason | Key Levels | Catalyst |
|--------|--------|--------------|------------|-----------|
{{#watchlist_secondary}}
| {{ticker}} | {{sector}} | {{reason}} | {{levels}} | {{catalyst}} |
{{/watchlist_secondary}}

### Earnings Calendar

| Date | Ticker | Sector | Expected Move | IV Rank | Status |
|------|--------|--------|----------------|---------|--------|
{{#earnings_calendar}}
| {{date}} | {{ticker}} | {{sector}} | {{exp_move}} | {{iv_rank}} | {{status}} |
{{/earnings_calendar}}

---

## Market Opportunity Matrix

### Risk/Reward Opportunities

**High Conviction Setups:**
- {{setup1_ticker}}: {{setup1_description}}
  - Risk/Reward: {{setup1_rr}}
  - Probability: {{setup1_prob}}

- {{setup2_ticker}}: {{setup2_description}}
  - Risk/Reward: {{setup2_rr}}
  - Probability: {{setup2_prob}}

**Hedging Recommendations:**
- Primary Hedge: {{hedge1_instrument}}, Recommendation: {{hedge1_rec}}
- Secondary Hedge: {{hedge2_instrument}}, Recommendation: {{hedge2_rec}}

---

## Technical Summary

{{technical_summary}}

---

**Analysis Status:** {{analysis_status}}
**Data Quality:** {{data_quality}}
**Next Update:** {{next_update}}
