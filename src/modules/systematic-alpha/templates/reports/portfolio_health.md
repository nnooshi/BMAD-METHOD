# Portfolio Health Report

**Report Generated:** {{generated_timestamp}}
**Analysis Date:** {{analysis_date}}
**Portfolio ID:** {{portfolio_id}}

---

## Executive Summary

- **Total Positions:** {{total_positions}}
- **Net Portfolio Delta:** {{net_delta}}
- **Average Correlation:** {{avg_correlation}}
- **Overall Risk Level:** {{risk_level}}

---

## Current Positions

| Ticker | Type | Quantity | Entry Price | Current Price | P&L | Delta | Gamma | Vega | Theta |
|--------|------|----------|-------------|---------------|-----|-------|-------|------|-------|
{{#positions}}
| {{ticker}} | {{type}} | {{quantity}} | {{entry_price}} | {{current_price}} | {{pl}} | {{delta}} | {{gamma}} | {{vega}} | {{theta}} |
{{/positions}}

**Summary Stats:**
- Total Notional Value: {{total_notional}}
- Total P&L: {{total_pl}}
- Total P&L %: {{total_pl_pct}}

---

## Beta Weighted Deltas

| Risk Factor | Beta | Weighted Delta | Contribution |
|-------------|------|-----------------|--------------|
{{#risk_factors}}
| {{factor_name}} | {{beta}} | {{weighted_delta}} | {{contribution}} |
{{/risk_factors}}

**Portfolio Sensitivity:**
- Market Beta: {{market_beta}}
- Sector Beta Exposure: {{sector_betas}}
- Implied Correlation Risk: {{correlation_risk}}

---

## Correlations

### Pairwise Correlations

| Asset Pair | Correlation | 30-Day Trend | Risk Assessment |
|------------|-------------|--------------|-----------------|
{{#correlations}}
| {{asset1}} - {{asset2}} | {{correlation}} | {{trend}} | {{assessment}} |
{{/correlations}}

### Correlation Heatmap Summary
```
{{correlation_matrix}}
```

**Key Observations:**
- Highest Correlation: {{max_correlation}} ({{max_corr_pair}})
- Lowest Correlation: {{min_correlation}} ({{min_corr_pair}})
- Diversification Index: {{diversification_index}}

---

## Needs Analysis

### Immediate Actions Required

| Priority | Item | Reason | Recommended Action |
|----------|------|--------|-------------------|
{{#action_items}}
| {{priority}} | {{item}} | {{reason}} | {{action}} |
{{/action_items}}

### Risk Adjustments Suggested

**Delta Rebalancing:**
- Target Delta: {{target_delta}}
- Current Delta: {{current_delta}}
- Adjustment Needed: {{delta_adjustment}}
- Suggested Trades: {{delta_trades}}

**Correlation Management:**
- Reduce Correlated Exposure: {{corr_reduction_needed}}
- Diversification Opportunity: {{diversification_opportunity}}

**Capital Allocation:**
- Currently Deployed: {{deployed_capital}}
- Available Capital: {{available_capital}}
- Recommended Allocation: {{recommended_allocation}}

---

## Notes

{{analysis_notes}}

---

**Report Status:** {{report_status}}
**Next Review:** {{next_review_date}}
