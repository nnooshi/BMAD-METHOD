# Trade Plan - Draft

**Plan ID:** {{plan_id}}
**Ticker:** {{ticker}}
**Draft Date:** {{draft_date}}
**Analyst:** {{analyst_name}}
**Status:** DRAFT

---

## Thesis

### Market Outlook
{{market_outlook}}

### Price Target & Timeline
- **Price Target:** {{price_target}}
- **Target Timeline:** {{target_timeline}}
- **Confidence Level:** {{confidence_level}}

### Key Supporting Evidence

**Fundamental Drivers:**
- Driver 1: {{driver1}}
- Driver 2: {{driver2}}
- Driver 3: {{driver3}}

**Technical Setup:**
{{technical_setup}}

**Catalyst Events:**
- Catalyst 1: {{catalyst1}} (Expected Date: {{catalyst1_date}})
- Catalyst 2: {{catalyst2}} (Expected Date: {{catalyst2_date}})

---

## Profit Mechanism

### How We Make Money

**Primary Profit Source:**
{{primary_profit_mechanism}}

**Secondary Profit Sources:**
- {{secondary_mechanism_1}}
- {{secondary_mechanism_2}}

### Expected Payoff Profile

```
Payoff Diagram:
{{payoff_diagram}}
```

### Greeks & Sensitivity Analysis

**Directional Assumptions:**
- Stock Move Required: {{stock_move_required}}
- Breakeven Stock Price: {{breakeven_price}}

**Time Decay Consideration:**
- Theta Decay Expected: {{theta_decay}}
- Days to Expiration: {{days_to_expiration}}
- Impact of Time Decay: {{time_decay_impact}}

**Volatility Sensitivity:**
- Current IV Percentile: {{iv_percentile}}
- Vega Exposure: {{vega_exposure}}
- IV Move Impact: {{iv_impact}}

---

## Proposed Structure

### Trade Type
{{trade_type}} (e.g., Long Call, Bull Call Spread, Iron Condor, Long Stock, etc.)

### Components

{{#structure_legs}}

**Leg {{leg_number}}:** {{leg_type}}
- Instrument: {{instrument}}
- Strike: {{strike}}
- Expiration: {{expiration}}
- Action: {{action}} (Buy/Sell)
- Quantity: {{quantity}}
- Premium/Price: {{price}}

{{/structure_legs}}

### Alternative Structures Considered

| Structure | Pros | Cons | Recommendation |
|-----------|------|------|-----------------|
{{#alt_structures}}
| {{alt_structure}} | {{alt_pros}} | {{alt_cons}} | {{alt_rec}} |
{{/alt_structures}}

### Why This Structure?

{{structure_justification}}

---

## Initial Sizing

### Risk Parameters

**Maximum Loss per Trade:**
- Max Theoretical Loss: {{max_loss}}
- Max Acceptable Loss: {{max_acceptable_loss}}

**Position Sizing:**
- Account Size: {{account_size}}
- Risk Allocation %: {{risk_allocation_pct}}
- Capital to Deploy: {{capital_to_deploy}}
- Units to Trade: {{units_to_trade}}

### Margin & Capital Requirements

- Initial Margin Required: {{initial_margin}}
- Maintenance Margin: {{maintenance_margin}}
- Collateral Available: {{collateral_available}}
- Margin Impact: {{margin_impact}}

### Suggested Scaling Plan

**Entry Breakdown:**
- Tranche 1 ({{tranche1_pct}}%): {{tranche1_units}} units at {{tranche1_trigger}}
- Tranche 2 ({{tranche2_pct}}%): {{tranche2_units}} units at {{tranche2_trigger}}
- Tranche 3 ({{tranche3_pct}}%): {{tranche3_units}} units at {{tranche3_trigger}}

---

## Risk Management

### Exit Criteria

**Profit Taking:**
- 25% Profit Target: {{profit_25pct}}
- 50% Profit Target: {{profit_50pct}}
- 100% Profit Target: {{profit_100pct}}

**Loss Mitigation:**
- Hard Stop Loss: {{hard_stop_loss}}
- Soft Stop Loss: {{soft_stop_loss}} (Action: {{stop_action}})
- Panic Level: {{panic_level}} (Forced Exit)

### Monitoring Checklist

- [ ] Monitor underlying price action vs {{key_support_resistance}}
- [ ] Track IV changes vs {{iv_benchmark}}
- [ ] Review earnings date changes
- [ ] Check for corporate actions (splits, dividends)
- [ ] Monitor sector and macro developments
- [ ] Review position Greeks daily
- [ ] Rebalance if delta exceeds {{delta_rebalance_threshold}}

---

## Calendar & Timing

**Entry Window:**
- Optimal Entry: {{optimal_entry_window}}
- Latest Entry: {{latest_entry_date}}

**Expiration Consideration:**
- Leg Expirations: {{leg_expiration_dates}}
- Roll Plan: {{roll_plan_description}}

**Time to Adjustment:**
- If Stock at {{adjustment_trigger1}}: {{adjustment_action1}}
- If Stock at {{adjustment_trigger2}}: {{adjustment_action2}}

---

## Related Positions

**Correlated Existing Positions:**
- {{existing_position1}}: {{correlation1}}, {{interaction1}}
- {{existing_position2}}: {{correlation2}}, {{interaction2}}

**Hedge Interactions:**
{{hedge_interactions}}

---

## Notes & Research

{{additional_notes}}

---

## Review Checklist

- [ ] Thesis is clearly documented and testable
- [ ] Profit mechanism is well understood
- [ ] Structure appropriately matches outlook
- [ ] Sizing adheres to risk limits
- [ ] Exit criteria are defined
- [ ] Related positions considered
- [ ] Liquidity verified for all legs
- [ ] Corporate action calendar checked

---

**Next Step:** Guardian Review → {{next_stage}}
