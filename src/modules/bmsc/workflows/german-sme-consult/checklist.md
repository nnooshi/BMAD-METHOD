# German SME AI Strategy Consulting - Validation Checklist

**Workflow:** german-sme-consult
**Module:** BMSC (BMad Strategy Consulting)

Use this checklist to validate that the consulting session was completed thoroughly and all requirements met.

---

## Phase 1: Value Chain Interview (Discovery)

### ✅ Use Case Definition

- [ ] Use case is SPECIFIC, not vague (e.g., "process 150 invoices/month", NOT "improve admin")
- [ ] Process is clearly bounded (clear start and end)
- [ ] Process is currently manual or semi-manual
- [ ] Business owner/stakeholder identified

### ✅ Porter's Value Chain Categorization

- [ ] Use case mapped to ONE of the 9 Value Chain categories:
  - [ ] Inbound Logistics
  - [ ] Operations
  - [ ] Outbound Logistics
  - [ ] Marketing & Sales
  - [ ] Service
  - [ ] Firm Infrastructure
  - [ ] Human Resource Management
  - [ ] Technology Development
  - [ ] Procurement

- [ ] Categorization is justified (not arbitrary)
- [ ] Distinction made between Primary (revenue) vs Support (enabling) activity

### ✅ Process Criticality

- [ ] Business impact articulated (cost, time, or quality issue)
- [ ] Volume/frequency is significant enough to warrant automation
- [ ] Process is repeatable (not ad-hoc or one-off)

---

## Phase 2: GDPR Filter (Feasibility)

### ✅ Data Characteristics

- [ ] **PII Assessment:** Clearly determined if personally identifiable information is involved (Yes/No)
- [ ] **Data Format:** Confirmed data is digital (NOT paper-based)
  - If paper → ⛔ **ABORT CONDITION:** Workflow cannot proceed
- [ ] **Employee Data:** Assessed if Mitarbeiterdaten (employee records) are involved
- [ ] **Cross-Border:** Determined if data crosses country borders

### ✅ GDPR Risk Assessment

- [ ] Risk level calculated: **HIGH** / **MEDIUM** / **LOW**
- [ ] Risk score computed (0-100 scale)
- [ ] Risk factors explicitly listed
- [ ] Architectural constraints identified based on risk level:
  - HIGH → On-Premise mandatory
  - MEDIUM → Azure Germany West with AVV
  - LOW → Cloud solutions acceptable

### ✅ Betriebsrat (Works Council)

- [ ] Betriebsrat involvement requirement determined (Yes/No)
- [ ] If Yes: Timeline impact noted (+4-8 weeks)
- [ ] If employee data involved: §87 BetrVG referenced

### ✅ Legal Compliance

- [ ] Relevant DSGVO articles referenced (Art. 4, 5, 6, 32, 35)
- [ ] DSFA (Data Protection Impact Assessment) requirement determined
- [ ] Legal basis for data processing identified (Art. 6)
- [ ] Verarbeitungsverzeichnis (processing register) update noted

---

## Phase 3: The Calculator (ROI)

### ✅ Input Data Collection

All THREE required inputs collected:

- [ ] **Frequency per month:** Numerical value (e.g., 150 occurrences/month)
- [ ] **Minutes per task:** Numerical value (e.g., 15 minutes)
- [ ] **Hourly rate (EUR):** Numerical value (e.g., €45/hour)

Optional inputs:

- [ ] **Error rate (%):** Collected OR default 5% applied
- [ ] **Implementation cost (EUR):** Collected OR default €15,000 applied

### ✅ Calculation Accuracy

- [ ] **Monthly cost (as-is)** calculated: `Frequency × (Minutes÷60) × Hourly Rate`
- [ ] **Monthly error cost** calculated: `Monthly Cost × (Error Rate÷100)`
- [ ] **Total monthly cost** calculated: `Monthly Cost + Error Cost`
- [ ] **Annual cost** calculated: `Total Monthly Cost × 12`

### ✅ Projection Quality

- [ ] **Efficiency gain** set at 80% (NOT 95%+ unrealistic values)
- [ ] **Annual savings** calculated: `Annual Cost × 0.80`
- [ ] **Monthly savings** calculated: `Annual Savings ÷ 12`

### ✅ Investment Analysis

- [ ] **Break-even months** calculated: `Implementation Cost ÷ Monthly Savings`
- [ ] **Break-even years** calculated: `Break-even Months ÷ 12`
- [ ] **3-year total savings** calculated: `Annual Savings × 3`
- [ ] **3-year net benefit** calculated: `3-Year Savings - Implementation Cost`
- [ ] **ROI percentage** calculated: `(Net Benefit ÷ Implementation Cost) × 100`

### ✅ Sanity Checks

- [ ] Break-even is reasonable (< 24 months preferred, > 24 months flagged)
- [ ] ROI is positive (if negative, flagged)
- [ ] Hourly rate is realistic (€30-€150 typical range for Mittelstand)
- [ ] Frequency and minutes pass "smell test" (not 10,000 times/month for manual work)

### ✅ Documentation

- [ ] All calculations shown with formulas (transparent methodology)
- [ ] Results formatted in German style (e.g., €1.234,56)
- [ ] Conservative assumptions explicitly stated

---

## Phase 4: The Blueprint (Architecture)

### ✅ Architecture Recommendation

- [ ] Architecture matches risk level:
  - **HIGH risk** → On-Premise Local LLM
  - **MEDIUM risk** → Azure OpenAI Germany West
  - **LOW risk** → Cloud solution with EU data centers

- [ ] Specific models/technologies named (e.g., "Llama 3.3 70B", "GPT-4o")
- [ ] Rationale provided (why this architecture for this risk level)
- [ ] Cost estimate provided (setup + monthly operation)

### ✅ Integration Strategy

- [ ] Existing system landscape acknowledged (SAP, Microsoft 365, etc.)
- [ ] Integration points identified:
  - [ ] Data extraction method
  - [ ] AI processing layer
  - [ ] Data return method
- [ ] Integration challenges anticipated

### ✅ Privacy-by-Design

- [ ] Technical measures listed (Art. 32 DSGVO):
  - [ ] Encryption at rest
  - [ ] Encryption in transit (TLS 1.3)
  - [ ] Access control (RBAC)
  - [ ] Audit trail / logging
  - [ ] Data retention policy

- [ ] Pseudonymization considered (if HIGH risk PII)
- [ ] Data flow diagram provided or described

### ✅ Implementation Roadmap

- [ ] **Phase 1 (PoC)** defined:
  - [ ] Timeline: Months 1-2
  - [ ] Scope: ~10% of volume
  - [ ] Budget: ~20% of total
  - [ ] Success criteria specified

- [ ] **Phase 2 (Pilot)** defined:
  - [ ] Timeline: Months 3-4
  - [ ] Scope: ~50% of volume
  - [ ] Budget: ~30% of total
  - [ ] Betriebsrat approval milestone (if required)
  - [ ] Success criteria specified

- [ ] **Phase 3 (Rollout)** defined:
  - [ ] Timeline: Months 5-6
  - [ ] Scope: 100% of volume
  - [ ] Budget: ~50% of total
  - [ ] Success criteria specified

### ✅ Risk Assessment

- [ ] **Technical risks** identified with mitigation (e.g., model accuracy, integration complexity)
- [ ] **Legal risks** identified with mitigation (GDPR, Betriebsrat)
- [ ] **Change management risks** identified with mitigation (user acceptance, skill gaps)
- [ ] Risk matrix provided (Probability × Impact → Mitigation)

### ✅ Success Metrics

- [ ] **Financial KPIs** defined (actual vs. projected savings, TCO variance)
- [ ] **Operational KPIs** defined (cycle time, error rate, NPS)
- [ ] **Compliance KPIs** defined (GDPR incidents, audit findings)

### ✅ Governance

- [ ] Decision board defined:
  - [ ] Sponsor (executive level)
  - [ ] Product Owner (business side)
  - [ ] Technical Lead (IT side)
  - [ ] Compliance (Datenschutzbeauftragter)
  - [ ] Stakeholder (Betriebsrat, if applicable)

- [ ] Review cadence defined:
  - [ ] Weekly team meetings
  - [ ] Monthly steering committee
  - [ ] Quarterly executive review

### ✅ Next Steps

- [ ] Immediate actions listed (Week 1)
- [ ] Short-term actions listed (Weeks 2-4)
- [ ] Medium-term actions listed (Month 2)
- [ ] Clear ownership/timeline for each action

---

## Final Deliverable: Strategic Roadmap Document

### ✅ Document Structure

- [ ] Executive Summary (1 page)
- [ ] Section 1: Ausgangslage & Use Case
- [ ] Section 2: Compliance & Datensouveränität
- [ ] Section 3: Finanzielle Auswirkungen (ROI)
- [ ] Section 4: Technische Architektur
- [ ] Section 5: Umsetzungs-Roadmap
- [ ] Section 6: Risiken & Mitigation
- [ ] Section 7: Erfolgsmessung
- [ ] Section 8: Nächste Schritte
- [ ] Appendix A: Berechnungsgrundlagen
- [ ] Appendix B: Referenzen
- [ ] Disclaimer

### ✅ Document Quality

- [ ] Written in German (or language specified in config)
- [ ] Uses German business terminology:
  - [ ] Wertschöpfung (value creation)
  - [ ] Datenschutz / DSGVO (data protection / GDPR)
  - [ ] Betriebsrat (works council)
  - [ ] Mittelstand (SME)
  - [ ] Datensouveränität (data sovereignty)

- [ ] Professional tone (formal "Sie", not informal "du")
- [ ] References included:
  - [ ] Porter (1985) - Competitive Advantage
  - [ ] Kaplan & Cooper (1998) - Activity-Based Costing
  - [ ] DSGVO (EU 2016/679)
  - [ ] BetrVG (German Works Constitution Act)

- [ ] Calculations are transparent and reproducible
- [ ] No AI hype language ("revolutionize", "transform everything", etc.)
- [ ] Conservative assumptions clearly stated

### ✅ File Naming & Storage

- [ ] File saved as: `STRATEGIC_ROADMAP-{{company_name}}-{{date}}.md`
- [ ] Saved in output folder specified in config
- [ ] File marked as VERTRAULICH (confidential)

---

## Workflow Completion Criteria

### ✅ All Phases Completed

- [ ] Phase 1 (Discovery) ✅
- [ ] Phase 2 (GDPR Filter) ✅
- [ ] Phase 3 (ROI Calculator) ✅
- [ ] Phase 4 (Blueprint) ✅

### ✅ Abort Conditions Handled

- [ ] If paper-based data detected → Workflow aborted with explanation
- [ ] If ROI negative → Flagged and discussed with user
- [ ] If break-even > 24 months → Warning issued, executive approval recommended

### ✅ Quality Standards Met

- [ ] All calculations use Activity-Based Costing methodology (not guesswork)
- [ ] GDPR assessment references specific DSGVO articles
- [ ] Porter's Value Chain categorization is explicit and justified
- [ ] ROI projections are conservative (80% efficiency, not 95%+)
- [ ] Architecture is risk-appropriate (HIGH risk = no cloud)
- [ ] Betriebsrat involvement addressed (if employee data involved)
- [ ] No AI hype or buzzwords
- [ ] Disclaimer included (this is NOT legal advice)

---

## Agent Persona Validation

### ✅ Klaus (the Strategy Coach) Behavior

- [ ] Demanded precise numbers (frequency, time, cost)
- [ ] Refused vague answers ("Das ist zu ungenau")
- [ ] Used German business terminology
- [ ] Was professionally skeptical of AI hype
- [ ] Insisted on Porter's Value Chain mapping
- [ ] Prioritized GDPR compliance before technology
- [ ] Warned about Betriebsrat if employee data involved
- [ ] Used conservative assumptions (80% efficiency, not 95%)
- [ ] Refused to proceed without required inputs

---

## Post-Workflow Actions

### ✅ User Handoff

- [ ] User has received STRATEGIC_ROADMAP.md
- [ ] User understands next steps (present to Geschäftsführung, engage Betriebsrat)
- [ ] User knows who to involve:
  - [ ] Datenschutzbeauftragter (DPO)
  - [ ] Betriebsrat (if applicable)
  - [ ] Legal counsel (for GDPR interpretation)
  - [ ] IT architecture team (for technical validation)

### ✅ Disclaimers Acknowledged

- [ ] User understands this is strategic consulting, NOT legal advice
- [ ] User knows DSFA (Data Protection Impact Assessment) may be required
- [ ] User knows Betriebsvereinbarung (works agreement) may be required
- [ ] User understands ROI calculations are projections, not guarantees

---

## Checklist Summary

**Total Requirements:** {{TOTAL_CHECKLIST_ITEMS}}

**Completed:** {{COMPLETED_ITEMS}} / {{TOTAL_CHECKLIST_ITEMS}}

**Pass Criteria:** ≥ 95% of items checked (allowing for optional items)

---

## Issues / Gaps Identified

If any critical items are NOT checked, document why:

**Missing Items:**

1. [ ] Item: _______________ | Reason: _______________
2. [ ] Item: _______________ | Reason: _______________
3. [ ] Item: _______________ | Reason: _______________

**Mitigation Plan:**

_______________________________________________________________________________
_______________________________________________________________________________

---

## Sign-Off

**Consultant (Agent):** Klaus - Senior AI Strategy Consultant (DACH)

**Date:** {{DATE}}

**Workflow Status:** ✅ Complete / ⚠️ Complete with Gaps / ❌ Incomplete

**Notes:**

_______________________________________________________________________________
_______________________________________________________________________________
_______________________________________________________________________________

---

**IMPORTANT REMINDER:**

This consulting workflow is designed to be:

- **Mathematically rigorous** (Activity-Based Costing, not handwaving)
- **GDPR-first** (Compliance before convenience)
- **Mittelstand-appropriate** (SAP, Betriebsrat, German business culture)
- **Anti-hype** (Conservative assumptions, professional skepticism)

If any of these principles were violated during the workflow, **FAIL the validation** and repeat the relevant phase.

---

_Validation Checklist v1.0 - BMSC Module_
_"Ordnung muss sein" - And we check EVERY box._
