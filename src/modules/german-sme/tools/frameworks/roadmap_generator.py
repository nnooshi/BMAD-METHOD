"""
CRISP-DM Roadmap Generator
Cross-Industry Standard Process for Data Mining - adapted for German SME context
"""

from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json


def generate_crisp_dm_pdf(
    project_name: str,
    canvas_data: Dict,
    maturity_level: int,
    compliance_score: int,
    company_name: str = "German SME",
    start_date: Optional[str] = None
) -> str:
    """
    Generate a CRISP-DM structured roadmap integrating all three frameworks.

    This is the culmination - taking outputs from AI Canvas, Maturity Assessment,
    and 4-P Compliance to create an actionable, German-context-aware roadmap.

    Args:
        project_name: Name of the AI project
        canvas_data: Output from structure_ai_canvas (dict with prediction, judgment, action, outcome)
        maturity_level: From assess_hierarchy_level (1-6)
        compliance_score: From score_4p_readiness (0-100)
        company_name: Company name for the report
        start_date: Project start date (YYYY-MM-DD), defaults to today

    Returns:
        Formatted Markdown roadmap document
    """

    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")

    # Parse canvas data
    prediction = canvas_data.get("prediction_goal", "Not defined")
    judgment = canvas_data.get("judgment_owner", "Not defined")
    action = canvas_data.get("action_trigger", "Not defined")
    outcome = canvas_data.get("outcome_value", "Not defined")

    # Determine timeline based on maturity and compliance
    timeline_months = _calculate_timeline(maturity_level, compliance_score)
    phases = _generate_phases(maturity_level, compliance_score, timeline_months)

    roadmap = f"""# AI Project Roadmap: {project_name}
**Company:** {company_name}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Planned Start:** {start_date}
**Estimated Duration:** {timeline_months} months

---

## Executive Summary

This roadmap integrates three proven frameworks to ensure project success:

1. **AI Canvas** (Strategy) - What we're building and why
2. **Hierarchy of Needs** (Data Readiness) - Where we are technically
3. **4-P Model** (German Context) - What risks we face

**Current Status:**
- Data Maturity: Level {maturity_level}/6
- Compliance Score: {compliance_score}/100
- Risk Level: {_risk_level_from_score(compliance_score)}

---

## 🎯 Project Definition (From AI Canvas)

### The Prediction Task
**What specific outcome are we predicting?**
{prediction}

### The Decision Owner
**Who will use this prediction?**
{judgment}

### The Action
**What changes in operations?**
{action}

### The Business Value
**Why this matters financially:**
{outcome}

---

## 📊 Current State Assessment

### Data Maturity: Level {maturity_level}/6

{_maturity_description(maturity_level)}

### Compliance Readiness: {compliance_score}/100

{_compliance_description(compliance_score)}

---

## 🗺️ CRISP-DM Roadmap

The project follows the industry-standard CRISP-DM methodology, adapted for German SME context.

"""

    # Generate phase details
    for phase in phases:
        roadmap += f"""
### Phase {phase['number']}: {phase['name']}
**Duration:** {phase['duration']}
**Start:** {phase['start_date']}

{phase['description']}

**Deliverables:**
"""
        for deliverable in phase['deliverables']:
            roadmap += f"- {deliverable}\n"

        roadmap += f"""
**Key Activities:**
"""
        for activity in phase['activities']:
            roadmap += f"- {activity}\n"

        if phase.get('german_considerations'):
            roadmap += f"""
**German Context Considerations:**
"""
            for consideration in phase['german_considerations']:
                roadmap += f"- ⚠️ {consideration}\n"

        roadmap += "\n---\n"

    # Add risk section
    roadmap += f"""
## ⚠️ Risk Management

### Technical Risks
{_technical_risks(maturity_level)}

### Compliance Risks
{_compliance_risks(compliance_score)}

### Mitigation Strategies
{_mitigation_strategies(maturity_level, compliance_score)}

---

## 📈 Success Metrics & KPIs

### Phase-Gate Criteria
Each phase must meet these criteria before proceeding:

**Phase 1 (Business Understanding):**
- [ ] Clear, measurable prediction goal defined
- [ ] Decision owner identified and committed
- [ ] Business value quantified (€ amount)
- [ ] Legal/compliance review initiated

**Phase 2 (Data Understanding):**
- [ ] Data sources identified and accessible
- [ ] Data quality assessment completed
- [ ] Sample data extracted and profiled
- [ ] Technical feasibility confirmed

**Phase 3 (Data Preparation):**
- [ ] Clean dataset created (>80% quality score)
- [ ] Feature engineering completed
- [ ] Train/test split established
- [ ] Data pipeline automated

**Phase 4 (Modeling):**
- [ ] Baseline model trained (simple algorithm)
- [ ] Model performance exceeds baseline by 20%
- [ ] Model is explainable (not black box)
- [ ] Validation metrics documented

**Phase 5 (Evaluation):**
- [ ] Business stakeholders accept model performance
- [ ] Legal/compliance sign-off obtained
- [ ] Betriebsrat approval (if required)
- [ ] Deployment plan approved

**Phase 6 (Deployment):**
- [ ] Model deployed to production
- [ ] Monitoring dashboard active
- [ ] Retraining pipeline established
- [ ] User training completed

### Project Success Criteria

**Must Have:**
- Model accuracy > 70% (or domain-specific threshold)
- No DSGVO violations
- Betriebsrat approval (if applicable)
- Positive ROI within 12 months

**Should Have:**
- Model explainability for end users
- Integration with existing IT systems
- Automated retraining pipeline

**Nice to Have:**
- Real-time predictions
- Mobile/web interface
- Advanced visualization dashboard

---

## 💰 Budget Estimation

{_budget_estimation(maturity_level, compliance_score, timeline_months)}

---

## 👥 Team & Resources

### Required Roles

**Phase 1-2 (Months 1-{int(timeline_months * 0.3)}):**
- Project Manager (50%)
- Business Analyst (75%)
- Data Engineer (50%)
- Legal/Compliance Officer (25%)

**Phase 3-4 (Months {int(timeline_months * 0.3)}-{int(timeline_months * 0.7)}):**
- Data Engineer (100%)
- Data Scientist / ML Engineer (100%)
- IT Infrastructure (25%)

**Phase 5-6 (Months {int(timeline_months * 0.7)}-{timeline_months}):**
- ML Engineer (100%)
- DevOps Engineer (50%)
- Change Management (50%)
- Trainer (25%)

### External Support Needed
{_external_support_needed(maturity_level, compliance_score)}

---

## 🇩🇪 German-Specific Considerations

### Legal & Compliance
- DSGVO compliance review at Phase 1 and Phase 5
- Data Protection Impact Assessment (DPIA) if processing PII
- Regular updates to Datenschutzbeauftragter (DPO)

### Works Council (Betriebsrat)
- Initial presentation: Before Phase 2 starts
- Formal approval needed: Before Phase 5 (Evaluation)
- Emphasize: AI as tool for workers, not replacement

### Cultural Factors
- **Perfectionism:** Germans want 95% accuracy; start with 70% and iterate
- **Risk Aversion:** Pilot project first, then scale
- **Documentation:** Extensive documentation expected (more than US/UK projects)
- **Hierarchy:** Get C-level buy-in early; decisions take time

---

## 📅 Detailed Timeline

{_generate_timeline_chart(phases)}

---

## 🎓 Recommended Training

### For Management
- AI Fundamentals for Decision Makers (1 day workshop)
- DSGVO and AI Compliance (half-day)

### For Technical Team
- Python & scikit-learn basics (if needed) (2 weeks online)
- ML Engineering best practices (1 week)
- Specific domain training (e.g., predictive maintenance, forecasting)

### For End Users
- How to interpret AI predictions (half-day workshop)
- When to trust vs. question the model (ongoing)

---

## 📚 Next Steps (Immediate Actions)

1. **Week 1:** Present this roadmap to executive team for approval
2. **Week 2:** Secure budget and resource commitments
3. **Week 3:** If Betriebsrat exists, schedule initial information session
4. **Week 4:** Kick off Phase 1 (Business Understanding)

---

## Appendix A: CRISP-DM Overview

CRISP-DM (Cross-Industry Standard Process for Data Mining) is the de facto methodology for data science projects, with 6 iterative phases:

```
Business Understanding → Data Understanding → Data Preparation
         ↑                                              ↓
    Deployment  ← ← ←  Evaluation  ← ← ←  Modeling
```

**Why CRISP-DM for German SMEs?**
- Proven methodology (since 1996)
- Iterative (allows course correction)
- Business-focused (not just technical)
- Well-documented (Germans love documentation)

---

## Appendix B: Framework Integration

This roadmap uniquely combines three frameworks:

| Framework | Purpose | Output |
|-----------|---------|--------|
| **AI Canvas** | Strategy & Value | Clear prediction task + ROI |
| **Hierarchy of Needs** | Technical Readiness | Honest assessment of data maturity |
| **4-P Model** | Risk Assessment | German-specific compliance risks |
| **CRISP-DM** | Execution Plan | Phase-by-phase implementation roadmap |

**Integration Logic:**
1. AI Canvas defines WHAT we're building (feeds into Phase 1)
2. Maturity Assessment defines WHERE we start (determines Phases 2-3 duration)
3. 4-P Model defines CONSTRAINTS (affects Phases 5-6 timeline)
4. CRISP-DM structures HOW we execute (the backbone)

---

## Appendix C: Glossary (German Terms)

- **Betriebsrat:** Works Council (employee representation)
- **Datenschutzbeauftragter (DPO):** Data Protection Officer
- **DSGVO:** German acronym for GDPR (Datenschutz-Grundverordnung)
- **Mittelstand:** German SME sector (typically 50-3000 employees)
- **Personenbezogene Daten:** Personal Identifiable Information (PII)
- **Werksleiter:** Plant Manager
- **Geschäftsführer:** Managing Director / CEO

---

**Document Version:** 1.0
**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

*This roadmap was generated using the BMAD Method - German SME Consultant Suite*
*For questions or modifications, consult with your AI project manager.*
"""

    return roadmap


def _calculate_timeline(maturity_level: int, compliance_score: int) -> int:
    """Calculate realistic project timeline based on maturity and compliance."""
    # Base timeline by maturity level
    base_months = {
        1: 18,  # Need to build data infrastructure first
        2: 15,  # Need data pipeline automation
        3: 12,  # Need data cleaning
        4: 9,   # Ready for ML experimentation
        5: 6,   # Ready for production ML
        6: 4    # Advanced ML capabilities
    }

    months = base_months.get(maturity_level, 12)

    # Add time for compliance issues
    if compliance_score < 50:
        months += 6  # Major compliance work
    elif compliance_score < 70:
        months += 3  # Moderate compliance work

    return months


def _risk_level_from_score(score: int) -> str:
    """Convert compliance score to risk level."""
    if score >= 80:
        return "🟢 LOW"
    elif score >= 50:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"


def _maturity_description(level: int) -> str:
    """Get description for maturity level."""
    descriptions = {
        1: "**Critical Gap:** Data collection is manual/paper-based. Must digitize before AI is possible.",
        2: "**Infrastructure Needed:** Database exists but data flow is manual. Automate pipelines first.",
        3: "**Quality Issues:** Data infrastructure exists but quality is poor. Clean data before ML.",
        4: "**Analytics Ready:** Good for BI and reporting. Simple ML possible with preparation.",
        5: "**ML Ready:** Can start pilot ML projects. Team needs ML training.",
        6: "**Advanced ML Ready:** Production ML capability exists. Can pursue deep learning."
    }
    return descriptions.get(level, "Unknown maturity level")


def _compliance_description(score: int) -> str:
    """Get description for compliance score."""
    if score >= 80:
        return "**Low Risk:** Few compliance barriers. Proceed with standard governance."
    elif score >= 50:
        return "**Medium Risk:** Some compliance barriers exist. Mitigation plan required."
    else:
        return "**High Risk:** Significant compliance barriers. Extensive legal/HR work needed before technical work."


def _generate_phases(maturity_level: int, compliance_score: int, total_months: int) -> List[Dict]:
    """Generate CRISP-DM phases with German context."""
    phases = []
    current_month = 0

    # Phase 1: Business Understanding
    phase1_duration = 1
    phases.append({
        "number": 1,
        "name": "Business Understanding",
        "duration": f"{phase1_duration} month",
        "start_date": f"Month {current_month + 1}",
        "description": "Define the business problem, success criteria, and project scope. This phase integrates the AI Canvas framework.",
        "deliverables": [
            "AI Canvas document (Prediction/Judgment/Action/Outcome)",
            "Business case with ROI calculation",
            "Success metrics and KPIs",
            "Stakeholder map",
            "Initial risk assessment"
        ],
        "activities": [
            "Workshop with business stakeholders",
            "Fill out AI Canvas collaboratively",
            "Quantify business value (€)",
            "Identify decision owners",
            "Initial legal/compliance review"
        ],
        "german_considerations": [
            "Get C-level buy-in early (decision hierarchies are strict)",
            "If Betriebsrat exists, inform them now (transparency = trust)",
            "Document everything (Germans expect thorough documentation)"
        ]
    })
    current_month += phase1_duration

    # Phase 2: Data Understanding
    phase2_duration = max(1, int(total_months * 0.2))
    phases.append({
        "number": 2,
        "name": "Data Understanding",
        "duration": f"{phase2_duration} month(s)",
        "start_date": f"Month {current_month + 1}",
        "description": "Assess current data landscape, quality, and availability. Validate technical feasibility.",
        "deliverables": [
            "Data inventory (sources, volume, quality)",
            "Data quality report",
            "Sample datasets",
            "Technical feasibility assessment",
            "Data access permissions documented"
        ],
        "activities": [
            "Map all data sources (ERP, MES, sensors, Excel, etc.)",
            "Assess data quality (completeness, accuracy, timeliness)",
            "Check data accessibility (API, database, manual export?)",
            "Profile sample data",
            "Identify data gaps"
        ],
        "german_considerations": [
            "Legacy systems (SAP R/3, DATEV) - plan for integration complexity",
            "Data silos are common - expect fragmented landscape",
            "If PII is involved, involve DPO (Datenschutzbeauftragter) now"
        ]
    })
    current_month += phase2_duration

    # Phase 3: Data Preparation
    phase3_duration = max(2, int(total_months * 0.25))
    if maturity_level <= 3:
        phase3_duration = max(3, int(total_months * 0.35))  # More time needed for low maturity

    phases.append({
        "number": 3,
        "name": "Data Preparation",
        "duration": f"{phase3_duration} month(s)",
        "start_date": f"Month {current_month + 1}",
        "description": "Clean, transform, and prepare data for modeling. Build automated data pipelines.",
        "deliverables": [
            "Clean training dataset",
            "Automated data pipeline (ETL)",
            "Feature engineering documentation",
            "Train/validation/test split",
            "Data quality monitoring dashboard"
        ],
        "activities": [
            "Data cleaning (missing values, outliers, duplicates)",
            "Feature engineering (create predictive variables)",
            "Data transformation (normalization, encoding)",
            "Build automated ETL pipeline",
            "Establish data versioning"
        ],
        "german_considerations": [
            "Perfectionism alert: 100% clean data is impossible - aim for 80% and iterate",
            "If integrating with SAP: budget 50-100 developer-hours just for integration",
            "Document data lineage (required for DSGVO audits if PII involved)"
        ]
    })
    current_month += phase3_duration

    # Phase 4: Modeling
    phase4_duration = max(2, int(total_months * 0.2))
    phases.append({
        "number": 4,
        "name": "Modeling",
        "duration": f"{phase4_duration} month(s)",
        "start_date": f"Month {current_month + 1}",
        "description": "Build, train, and validate machine learning models. Start simple, iterate to complexity.",
        "deliverables": [
            "Baseline model (simple algorithm)",
            "Advanced model(s) (if needed)",
            "Model performance report",
            "Model explainability documentation",
            "Hyperparameter tuning results"
        ],
        "activities": [
            "Train baseline model (linear regression, decision tree)",
            "Experiment with algorithms (random forest, gradient boosting)",
            "Hyperparameter tuning",
            "Cross-validation",
            "Error analysis"
        ],
        "german_considerations": [
            "Explainability is critical - black boxes face resistance",
            "Start with simple models (decision trees) before deep learning",
            "Germans trust statistical models more than 'AI magic'"
        ]
    })
    current_month += phase4_duration

    # Phase 5: Evaluation
    phase5_duration = max(1, int(total_months * 0.15))
    if compliance_score < 70:
        phase5_duration += 2  # Add time for compliance work

    phases.append({
        "number": 5,
        "name": "Evaluation",
        "duration": f"{phase5_duration} month(s)",
        "start_date": f"Month {current_month + 1}",
        "description": "Validate model with business stakeholders. Obtain legal and Betriebsrat approvals.",
        "deliverables": [
            "Business validation report",
            "Legal/compliance sign-off",
            "Betriebsrat approval (if required)",
            "Deployment plan",
            "Risk mitigation plan"
        ],
        "activities": [
            "Present model to business stakeholders",
            "Conduct pilot test with real users",
            "Legal review (DSGVO compliance check)",
            "Betriebsrat presentation and negotiation (if applicable)",
            "Finalize deployment architecture"
        ],
        "german_considerations": [
            "Betriebsrat approval can take 3-6 months - plan accordingly",
            "Emphasize: AI assists workers, does not replace them",
            "Prepare extensive documentation for legal review",
            "Be ready for skeptical questions - Germans are risk-averse"
        ]
    })
    current_month += phase5_duration

    # Phase 6: Deployment
    phase6_duration = total_months - current_month
    phases.append({
        "number": 6,
        "name": "Deployment",
        "duration": f"{phase6_duration} month(s)",
        "start_date": f"Month {current_month + 1}",
        "description": "Deploy model to production. Monitor performance. Train users. Establish retraining pipeline.",
        "deliverables": [
            "Production ML system",
            "Monitoring dashboard",
            "User training materials",
            "Retraining pipeline",
            "Handover documentation"
        ],
        "activities": [
            "Deploy model to production environment",
            "Set up monitoring and alerting",
            "Train end users",
            "Establish model retraining schedule",
            "Document maintenance procedures"
        ],
        "german_considerations": [
            "Germans expect extensive user manuals - budget for documentation",
            "Provide hands-on training (not just PowerPoint)",
            "Plan for 'Anlaufzeit' (ramp-up period) - users need time to adapt",
            "Expect feedback and iteration - Germans will test thoroughly"
        ]
    })

    return phases


def _technical_risks(maturity_level: int) -> str:
    """Generate technical risks based on maturity level."""
    if maturity_level <= 2:
        return """- **Critical:** Data infrastructure does not exist - project may fail entirely
- **High:** Data quality unknown - may be unusable for ML
- **High:** No automated data pipelines - manual work unsustainable"""
    elif maturity_level <= 4:
        return """- **Medium:** Data quality issues may limit model performance
- **Medium:** Integration with legacy systems may be complex
- **Low:** Technical team may need ML training"""
    else:
        return """- **Low:** Technical foundation is solid
- **Low:** Team has ML experience
- Focus on model optimization and production deployment"""


def _compliance_risks(compliance_score: int) -> str:
    """Generate compliance risks based on score."""
    if compliance_score < 50:
        return """- **Critical:** DSGVO compliance gaps - project may be blocked entirely
- **Critical:** Betriebsrat opposition - expect 6+ month delays
- **High:** Legal review will be extensive and slow
- **High:** May need to redesign solution for compliance"""
    elif compliance_score < 70:
        return """- **Medium:** Some DSGVO compliance work needed
- **Medium:** Betriebsrat approval required - add 3-4 months
- **Medium:** Legal review will flag issues to address"""
    else:
        return """- **Low:** Few compliance barriers
- **Low:** Standard legal review process
- Proceed with normal governance"""


def _mitigation_strategies(maturity_level: int, compliance_score: int) -> str:
    """Generate mitigation strategies."""
    strategies = []

    if maturity_level <= 3:
        strategies.append("**Technical:** Hire data engineering consultant to accelerate infrastructure build")
        strategies.append("**Technical:** Use cloud services (AWS, Azure) to avoid building from scratch")

    if compliance_score < 70:
        strategies.append("**Compliance:** Engage external DSGVO expert for review")
        strategies.append("**Compliance:** Present early to Betriebsrat - transparency builds trust")
        strategies.append("**Compliance:** Offer AI training to Betriebsrat members")

    if not strategies:
        strategies.append("**Standard:** Follow CRISP-DM best practices")
        strategies.append("**Standard:** Regular stakeholder communication")

    return "\n".join(strategies)


def _budget_estimation(maturity_level: int, compliance_score: int, months: int) -> str:
    """Generate budget estimation."""
    # Base budget: €10K per month
    base_budget = months * 10000

    # Adjust for maturity (low maturity = more infrastructure cost)
    if maturity_level <= 2:
        base_budget *= 1.5
    elif maturity_level <= 3:
        base_budget *= 1.25

    # Adjust for compliance (low compliance = more legal/consulting cost)
    if compliance_score < 50:
        base_budget *= 1.4
    elif compliance_score < 70:
        base_budget *= 1.2

    low = int(base_budget * 0.8)
    high = int(base_budget * 1.2)

    return f"""**Estimated Total Budget:** €{low:,} - €{high:,}

**Budget Breakdown:**
- Personnel (internal team): 50-60%
- External consultants/contractors: 20-30%
- Infrastructure (cloud, software): 10-15%
- Training & change management: 5-10%

**Note:** German AI projects typically cost 1.5-2x more than US equivalents due to:
- Higher labor costs
- More extensive documentation requirements
- Legal/compliance overhead
- Betriebsrat negotiations"""


def _external_support_needed(maturity_level: int, compliance_score: int) -> str:
    """Determine what external support is needed."""
    needs = []

    if maturity_level <= 2:
        needs.append("- **Data Engineering Consultant** (3-6 months) - Build data infrastructure")

    if maturity_level <= 4:
        needs.append("- **ML Engineer/Data Scientist** (6-12 months) - If no internal ML expertise")

    if compliance_score < 70:
        needs.append("- **DSGVO/Legal Consultant** (2-3 months) - Compliance review")
        needs.append("- **Betriebsrat Mediator** (optional) - If works council negotiations are difficult")

    needs.append("- **Change Management Consultant** (2-3 months) - User adoption and training")

    if not needs:
        needs.append("- Minimal external support needed - internal team is capable")

    return "\n".join(needs)


def _generate_timeline_chart(phases: List[Dict]) -> str:
    """Generate a simple text-based Gantt chart."""
    chart = "```\n"
    for phase in phases:
        phase_num = phase['number']
        start = phase['start_date']
        duration = phase['duration']
        name = phase['name']
        chart += f"Phase {phase_num} ({start:10}) [{duration:10}]: {name}\n"

    chart += "```\n"
    return chart


# Example usage
if __name__ == "__main__":
    # Example: Generate roadmap for a predictive maintenance project
    canvas_data = {
        "prediction_goal": "Probability (0-100%) that CNC machine will fail within next 7 days",
        "judgment_owner": "Werksleiter (Plant Manager) - Hans Schmidt",
        "action_trigger": "Schedule preventive maintenance during planned downtime window",
        "outcome_value": "Avoid €50,000 emergency downtime cost + €15,000 rush spare parts"
    }

    roadmap = generate_crisp_dm_pdf(
        project_name="Predictive Maintenance Pilot",
        canvas_data=canvas_data,
        maturity_level=3,
        compliance_score=65,
        company_name="Müller Maschinenbau GmbH",
        start_date="2025-02-01"
    )

    print(roadmap)

    # Save to file
    with open("SME_AI_ROADMAP_EXAMPLE.md", "w", encoding="utf-8") as f:
        f.write(roadmap)
    print("\nRoadmap saved to: SME_AI_ROADMAP_EXAMPLE.md")
