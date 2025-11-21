/**
 * Financial Tools for German SME AI Strategy Consulting
 * Provides Activity-Based Costing and ROI calculations
 */

/**
 * Calculate Process ROI using Activity-Based Costing methodology
 *
 * @param {Object} params - Calculation parameters
 * @param {number} params.frequency_per_month - How many times the task occurs per month
 * @param {number} params.minutes_per_task - Duration of each task in minutes
 * @param {number} params.hourly_rate_euro - Employee hourly rate in EUR
 * @param {number} [params.error_rate_percent=0] - Error rate as percentage (0-100)
 * @param {number} [params.implementation_cost=15000] - One-time implementation cost in EUR
 * @returns {Object} ROI calculation results
 */
function calculateProcessROI({
  frequency_per_month,
  minutes_per_task,
  hourly_rate_euro,
  error_rate_percent = 0,
  implementation_cost = 15000,
}) {
  // Input validation
  if (
    !frequency_per_month ||
    !minutes_per_task ||
    !hourly_rate_euro ||
    frequency_per_month <= 0 ||
    minutes_per_task <= 0 ||
    hourly_rate_euro <= 0
  ) {
    throw new Error(
      "Invalid input: frequency, minutes, and hourly rate must be positive numbers",
    );
  }

  if (error_rate_percent < 0 || error_rate_percent > 100) {
    throw new Error("Error rate must be between 0 and 100 percent");
  }

  // Core calculations
  const monthly_cost_asis = frequency_per_month * (minutes_per_task / 60) * hourly_rate_euro;
  const monthly_error_cost = monthly_cost_asis * (error_rate_percent / 100);
  const total_monthly_cost = monthly_cost_asis + monthly_error_cost;
  const total_annual_cost = total_monthly_cost * 12;

  // Projected savings (80% efficiency gain assumption)
  const efficiency_gain_percent = 80;
  const projected_annual_savings = total_annual_cost * (efficiency_gain_percent / 100);
  const projected_monthly_savings = projected_annual_savings / 12;

  // Break-even analysis
  const break_even_months =
    projected_monthly_savings > 0 ? implementation_cost / projected_monthly_savings : Infinity;

  // 3-year TCO analysis
  const three_year_savings = projected_annual_savings * 3;
  const net_three_year_benefit = three_year_savings - implementation_cost;
  const roi_percent = (net_three_year_benefit / implementation_cost) * 100;

  return {
    // Input summary
    inputs: {
      frequency_per_month,
      minutes_per_task,
      hourly_rate_euro,
      error_rate_percent,
      implementation_cost,
    },

    // Current state costs
    current_state: {
      monthly_cost_asis: Math.round(monthly_cost_asis * 100) / 100,
      monthly_error_cost: Math.round(monthly_error_cost * 100) / 100,
      total_monthly_cost: Math.round(total_monthly_cost * 100) / 100,
      annual_cost: Math.round(total_annual_cost * 100) / 100,
    },

    // Projected future state
    future_state: {
      efficiency_gain_percent,
      monthly_savings: Math.round(projected_monthly_savings * 100) / 100,
      annual_savings: Math.round(projected_annual_savings * 100) / 100,
    },

    // Investment analysis
    roi_analysis: {
      implementation_cost,
      break_even_months: Math.round(break_even_months * 10) / 10,
      break_even_years: Math.round((break_even_months / 12) * 10) / 10,
      three_year_total_savings: Math.round(three_year_savings * 100) / 100,
      three_year_net_benefit: Math.round(net_three_year_benefit * 100) / 100,
      roi_percent: Math.round(roi_percent * 10) / 10,
    },

    // Summary for reporting
    summary: {
      annual_cost_current: Math.round(total_annual_cost * 100) / 100,
      annual_savings_projected: Math.round(projected_annual_savings * 100) / 100,
      payback_months: Math.round(break_even_months * 10) / 10,
      three_year_roi_percent: Math.round(roi_percent * 10) / 10,
    },
  };
}

/**
 * Format ROI results as a German business report section
 *
 * @param {Object} roiData - Output from calculateProcessROI
 * @returns {string} Formatted markdown section
 */
function formatROIReport(roiData) {
  const { current_state, future_state, roi_analysis, summary } = roiData;

  return `
## 3. FINANZIELLE AUSWIRKUNGEN (ROI-Analyse)

### 3.1 Aktuelle Kostensituation (Status Quo)

**Monatliche Kosten:**
- Basis-Prozesskosten: €${current_state.monthly_cost_asis.toLocaleString("de-DE", { minimumFractionDigits: 2 })}
- Fehlerkosten: €${current_state.monthly_error_cost.toLocaleString("de-DE", { minimumFractionDigits: 2 })}
- **Gesamtkosten/Monat: €${current_state.total_monthly_cost.toLocaleString("de-DE", { minimumFractionDigits: 2 })}**

**Jährliche Gesamtkosten: €${current_state.annual_cost.toLocaleString("de-DE", { minimumFractionDigits: 2 })}**

### 3.2 Projektion nach Automatisierung

**Effizienzgewinn:** ${future_state.efficiency_gain_percent}% (konservative Schätzung)

**Erwartete Einsparungen:**
- Pro Monat: €${future_state.monthly_savings.toLocaleString("de-DE", { minimumFractionDigits: 2 })}
- Pro Jahr: €${future_state.annual_savings.toLocaleString("de-DE", { minimumFractionDigits: 2 })}

### 3.3 Investitionsanalyse

**Implementierungskosten:** €${roi_analysis.implementation_cost.toLocaleString("de-DE", { minimumFractionDigits: 2 })}

**Break-Even-Punkt:**
- Nach ${roi_analysis.break_even_months} Monaten (${roi_analysis.break_even_years} Jahre)

**3-Jahres-TCO:**
- Gesamteinsparungen: €${roi_analysis.three_year_total_savings.toLocaleString("de-DE", { minimumFractionDigits: 2 })}
- Netto-Nutzen: €${roi_analysis.three_year_net_benefit.toLocaleString("de-DE", { minimumFractionDigits: 2 })}
- **ROI: ${roi_analysis.roi_percent}%**

### 3.4 Management Summary

| Kennzahl | Wert |
|----------|------|
| Aktuelle Jahreskosten | €${summary.annual_cost_current.toLocaleString("de-DE")} |
| Erwartete Jahreseinsparungen | €${summary.annual_savings_projected.toLocaleString("de-DE")} |
| Amortisation | ${summary.payback_months} Monate |
| 3-Jahres-ROI | ${summary.three_year_roi_percent}% |
`;
}

/**
 * Validate inputs for Porter's Value Chain categorization
 *
 * @param {string} category - Value chain category
 * @returns {boolean} Whether category is valid
 */
function validateValueChainCategory(category) {
  const validCategories = [
    // Primary Activities
    "Inbound Logistics",
    "Operations",
    "Outbound Logistics",
    "Marketing & Sales",
    "Service",
    // Support Activities
    "Firm Infrastructure",
    "Human Resource Management",
    "Technology Development",
    "Procurement",
  ];

  return validCategories.includes(category);
}

/**
 * Calculate risk score based on data characteristics
 *
 * @param {Object} params - Risk parameters
 * @param {boolean} params.contains_pii - Contains personally identifiable information
 * @param {boolean} params.is_digital - Data is already digital
 * @param {boolean} params.involves_employee_data - Involves employee records
 * @param {boolean} params.crosses_borders - Data crosses country borders
 * @returns {Object} Risk assessment
 */
function assessGDPRRisk({ contains_pii, is_digital, involves_employee_data, crosses_borders }) {
  let risk_score = 0;
  const risk_factors = [];

  if (!is_digital) {
    return {
      risk_level: "ABORT",
      risk_score: 100,
      recommendation:
        "Papierbasierte Prozesse können nicht digitalisiert werden ohne vorherige Digitalisierung.",
      factors: ["Keine digitalen Daten verfügbar"],
    };
  }

  if (contains_pii) {
    risk_score += 40;
    risk_factors.push("Verarbeitung personenbezogener Daten (DSGVO Art. 4)");
  }

  if (involves_employee_data) {
    risk_score += 30;
    risk_factors.push("Mitarbeiterdaten (Betriebsrat-pflichtig)");
  }

  if (crosses_borders) {
    risk_score += 20;
    risk_factors.push("Grenzüberschreitende Datenübertragung");
  }

  let risk_level;
  let recommendation;

  if (risk_score >= 70) {
    risk_level = "HIGH";
    recommendation = "On-Premise Lösung mit lokalen LLMs erforderlich";
  } else if (risk_score >= 40) {
    risk_level = "MEDIUM";
    recommendation = "Azure OpenAI Germany West mit DSGVO-Vertrag möglich";
  } else {
    risk_level = "LOW";
    recommendation = "Cloud-Lösungen mit EU-Rechenzentren akzeptabel";
  }

  return {
    risk_level,
    risk_score,
    recommendation,
    factors: risk_factors,
  };
}

module.exports = {
  calculateProcessROI,
  formatROIReport,
  validateValueChainCategory,
  assessGDPRRisk,
};
