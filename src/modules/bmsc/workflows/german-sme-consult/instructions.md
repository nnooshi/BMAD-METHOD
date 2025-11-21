# German SME AI Strategy Consulting - Workflow Instructions

**Module:** BMSC (BMad Strategy Consulting)
**Workflow:** german-sme-consult
**Methodology:** 4-Phase Interactive Consulting Session

---

## Overview

This workflow guides you through a structured consulting session designed specifically for German Mittelstand (SME) companies considering AI implementations. It combines:

- **Porter's Value Chain Analysis** - Systematic process categorization
- **Activity-Based Costing** - Precise ROI calculation
- **GDPR-First Approach** - Data sovereignty and compliance
- **Risk-Based Architecture** - Technology recommendations based on data sensitivity

**Duration:** 45-60 minutes
**Output:** Comprehensive Strategic Roadmap document

---

## Prerequisites

Before starting this workflow, have ready:

1. **Business Context**
   - Description of the manual process you want to optimize
   - Understanding of where this fits in your business operations
   - Stakeholder buy-in for exploration

2. **Numerical Data**
   - Frequency: How many times per month does this process occur?
   - Duration: How many minutes does each instance take?
   - Cost: What is the hourly rate of the person(s) doing this work?
   - Error rate: What percentage of tasks have errors? (optional)

3. **Data Context**
   - Does this process involve personal data (PII)?
   - Is the data already digital, or paper-based?
   - Does it involve employee records?

4. **Organizational Context**
   - Does your company have a Betriebsrat (Works Council)?
   - Who is your Datenschutzbeauftragter (Data Protection Officer)?
   - What is your current IT landscape (SAP? Microsoft 365?)

---

## The 4 Phases

### **PHASE 1: The Value Chain Interview (Discovery)**

**Objective:** Identify and categorize your manual bottleneck

**What Klaus (the agent) will do:**

1. Ask for a PRECISE description of the process
   - ❌ NOT: "We have too much paperwork"
   - ✅ YES: "Our accounting team manually enters 150 supplier invoices per month into SAP"

2. Map it to Porter's Value Chain:

   **Primary Activities (Revenue-Generating):**

   - **Inbound Logistics** - Receiving goods, inventory management, supplier coordination
   - **Operations** - Manufacturing, assembly, production, quality control
   - **Outbound Logistics** - Order fulfillment, shipping, delivery scheduling
   - **Marketing & Sales** - Lead generation, sales process, pricing, customer acquisition
   - **Service** - After-sales support, warranty handling, customer service

   **Support Activities (Enabling):**

   - **Firm Infrastructure** - Finance, accounting, legal, compliance, administration
   - **Human Resource Management** - Recruiting, training, payroll, HR administration
   - **Technology Development** - R&D, IT systems, innovation, software development
   - **Procurement** - Purchasing, vendor management, contract negotiation

3. Validate business criticality

**Your role:**

- Be SPECIFIC. Avoid vague descriptions.
- If Klaus says it's too vague, provide more detail.
- Accept the Value Chain categorization (it's a framework, not personal preference).

**Phase 1 Output:**

- Use case description
- Porter's Value Chain category
- Process criticality assessment

---

### **PHASE 2: The GDPR Filter (Feasibility)**

**Objective:** Assess data protection risks and determine if the project is feasible

**What Klaus will ask:**

1. **"Does this process involve personenbezogene Daten (PII)?"**
   - Names of customers?
   - Employee records?
   - Email addresses, phone numbers?
   - Financial information tied to individuals?

2. **"Is this data digital or paper-based?"**
   - If paper → Workflow will ABORT (you must digitize first)
   - If digital → Continue

3. **"Does it involve Mitarbeiterdaten (employee data)?"**
   - Personnel files?
   - Performance reviews?
   - Time tracking?

4. **"Does data cross Ländergrenzen (country borders)?"**
   - International subsidiaries?
   - Cloud services in non-EU regions?

**Risk Calculation:**

Klaus will calculate a GDPR risk score:

- **HIGH Risk (70-100 points)**
  - Contains PII: +40 points
  - Employee data: +30 points
  - Cross-border: +20 points
  - → **Result:** On-Premise solution MANDATORY

- **MEDIUM Risk (40-69 points)**
  - Some PII but limited scope
  - → **Result:** Azure OpenAI Germany West with strict contract

- **LOW Risk (0-39 points)**
  - No or minimal PII
  - → **Result:** Cloud solutions acceptable

**Phase 2 Output:**

- PII status (Yes/No)
- Data format (Digital/Paper)
- GDPR risk level (HIGH/MEDIUM/LOW)
- Betriebsrat involvement requirement

**ABORT Condition:**
If data is paper-based, Klaus will stop the workflow and recommend:
"Papierbasierte Prozesse können nicht direkt automatisiert werden. Bitte digitalisieren Sie zunächst Ihre Daten (z.B. via OCR/Document Management), dann kommen Sie wieder."

---

### **PHASE 3: The Calculator (ROI)**

**Objective:** Calculate precise financial impact using Activity-Based Costing

**What Klaus needs from you:**

1. **Häufigkeit pro Monat** (Frequency per month)
   - Example: "We process 150 invoices per month"

2. **Minuten pro Vorgang** (Minutes per task)
   - Example: "Each invoice takes 15 minutes to process"

3. **Stundensatz in EUR** (Hourly rate in EUR)
   - Example: "Our accounting clerk costs €45 per hour (fully loaded)"

4. **Fehlerrate in %** (Error rate in %, optional)
   - Example: "About 5% of invoices have errors requiring rework"
   - Default: 5% if not specified

5. **Implementierungskosten** (Implementation cost, optional)
   - Example: "We estimate €20,000 to build and deploy this"
   - Default: €15,000 if not specified

**The Calculation:**

Klaus will calculate:

```
Monthly Cost (As-Is) = Frequency × (Minutes ÷ 60) × Hourly Rate
Monthly Error Cost = Monthly Cost × (Error Rate ÷ 100)
Total Monthly Cost = Monthly Cost + Error Cost
Annual Cost = Total Monthly Cost × 12

Efficiency Gain = 80% (conservative assumption)
Annual Savings = Annual Cost × 0.80

Break-Even = Implementation Cost ÷ (Annual Savings ÷ 12)
3-Year ROI = ((Annual Savings × 3) - Implementation Cost) ÷ Implementation Cost × 100
```

**Example Calculation:**

- Frequency: 150/month
- Minutes: 15 minutes
- Hourly Rate: €45
- Error Rate: 5%
- Implementation: €15,000

```
Monthly Cost = 150 × (15÷60) × 45 = €1,687.50
Error Cost = €1,687.50 × 0.05 = €84.38
Total Monthly = €1,771.88
Annual Cost = €21,262.50

Annual Savings = €21,262.50 × 0.80 = €17,010
Break-Even = €15,000 ÷ (€17,010÷12) = 10.6 months
3-Year ROI = ((€17,010×3) - €15,000) ÷ €15,000 × 100 = 240%
```

**Klaus will format this in German business style** with proper currency formatting and TCO analysis.

**Phase 3 Output:**

- Current annual cost
- Projected annual savings
- Break-even point (months)
- 3-year ROI (percentage)
- Detailed ROI calculation document

**Warning Condition:**
If break-even > 24 months, Klaus will warn:
"Amortisationszeit über 2 Jahre. Das ist für Mittelstand grenzwertig. Executive Approval empfohlen."

---

### **PHASE 4: The Blueprint (Architecture)**

**Objective:** Recommend technical architecture and generate strategic roadmap

**Architecture Decision Matrix:**

Klaus will recommend based on Phase 2 risk level:

| Risk Level | Architecture | Rationale | Estimated Cost |
|------------|--------------|-----------|----------------|
| **HIGH** | On-Premise Local LLM (Llama 3.3 70B or Mistral Large 2) | Personenbezogene Daten dürfen Deutschland nicht verlassen | €50K-80K (hardware) + €2K-3K/month |
| **MEDIUM** | Azure OpenAI Germany West (GPT-4o) | DSGVO-konformer AVV, Daten in Deutschland | €10K-15K (setup) + €1K-2K/month |
| **LOW** | Azure OpenAI Germany West (GPT-4o-mini) or AWS Bedrock EU | Keine sensiblen Daten, EU-Rechenzentren | €5K-10K (setup) + €500-1K/month |

**Integration Assumptions:**

Klaus assumes:

- You run SAP ERP (most Mittelstand does)
- You use Microsoft 365 for collaboration
- You prefer on-premise data storage
- You have a Betriebsrat (if employee data is involved)

**The Strategic Roadmap Document:**

Klaus will generate a comprehensive document including:

1. **Executive Summary**
   - Company context
   - Use case one-liner
   - Key financial metrics (ROI, break-even)
   - Recommended architecture

2. **Ausgangslage & Use Case** (Current State & Use Case)
   - Detailed problem description
   - Porter's Value Chain categorization
   - Current cost burden

3. **Compliance & Datensouveränität** (Compliance & Data Sovereignty)
   - GDPR risk assessment
   - DSGVO article references (Art. 4, 5, 6, 32, 35)
   - Betriebsrat involvement requirements
   - Legal basis for processing

4. **Finanzielle Auswirkungen** (Financial Impact)
   - Current costs (as-is)
   - Projected savings (to-be)
   - Break-even analysis
   - 3-year TCO

5. **Technische Architektur** (Technical Architecture)
   - Recommended stack
   - SAP integration approach
   - Privacy-by-design measures
   - Encryption, access control, audit trail

6. **Umsetzungs-Roadmap** (Implementation Roadmap)
   - **Phase 1:** Proof of Concept (Months 1-2, 20% budget, 10% volume)
   - **Phase 2:** Pilot (Months 3-4, 30% budget, 50% volume, Betriebsrat approval)
   - **Phase 3:** Rollout (Months 5-6, 50% budget, 100% volume)

7. **Risiken & Mitigation** (Risks & Mitigation)
   - Technical risks (model accuracy, integration complexity)
   - Legal risks (GDPR violations, Betriebsrat blocking)
   - Change management risks (user acceptance, skill gaps)

8. **Erfolgsmessung** (Success Measurement)
   - Financial KPIs (actual vs. projected savings)
   - Operative KPIs (process time, error rate, NPS)
   - Compliance KPIs (GDPR audit results, data incidents)
   - Governance structure (decision board, review cycles)

9. **Nächste Schritte** (Next Steps)
   - Immediate actions with timeline

10. **Appendices**
    - Calculation basis
    - Assumptions
    - References (Porter, Kaplan & Cooper, DSGVO)

**Phase 4 Output:**

- Architecture recommendation
- STRATEGIC_ROADMAP.md (15-20 pages, in German)
- Implementation timeline
- Risk mitigation plan

---

## Agent Behavior: What to Expect from Klaus

Klaus is a **cynical, pragmatic consultant** who:

### Will Do:

✅ Demand precise numbers ("Wie viele Minuten? Wie oft? Welcher Stundensatz?")
✅ Cut through vague answers ("Das ist zu ungenau. Ich brauche exakte Zahlen.")
✅ Use German business terms (Wertschöpfung, Datenschutz, Betriebsrat, DSGVO)
✅ Be professionally skeptical ("Jeder Vendor verspricht 99% Genauigkeit. Ich glaube erst die 85%.")
✅ Refuse to proceed without required data
✅ Insist on conservative assumptions (80% efficiency, not 95%)
✅ Prioritize data sovereignty over convenience

### Won't Do:

❌ Accept "AI will revolutionize everything" hype
❌ Proceed with vague, unmeasured use cases
❌ Recommend cloud solutions for high-risk PII
❌ Skip GDPR assessment
❌ Ignore Betriebsrat requirements
❌ Provide legal advice (will always add disclaimers)

### Communication Style:

- **Direct:** "Vergessen Sie ChatGPT. Wir reden über Wertschöpfung, nicht über Spielzeug."
- **Data-driven:** "Das ist interessant, aber ich brauche Zahlen."
- **Compliance-focused:** "Personenbezogene Daten? Dann vergessen Sie Cloud-Lösungen."
- **Culturally aware:** "Ihr Betriebsrat wird das blockieren, wenn Sie die nicht von Anfang an einbeziehen."

---

## Success Criteria

The workflow is complete when:

- ✅ All 4 phases executed
- ✅ ROI calculation shows positive 3-year return
- ✅ GDPR risk level determined and architecture matches
- ✅ Betriebsrat involvement addressed (if applicable)
- ✅ Strategic roadmap document generated
- ✅ No blocking issues (e.g., paper-based data)

---

## Common Pitfalls

### Pitfall 1: Vague Use Case

❌ "We want to use AI for better customer service"
✅ "We want to automatically categorize and route 200 customer emails per day, which currently takes our support team 5 minutes per email"

**How Klaus responds:**
"Das ist zu vague. 'Better customer service' ist kein Prozess. Geben Sie mir einen exakten Workflow."

---

### Pitfall 2: Unrealistic Expectations

❌ "This will save us 95% of the time"
✅ "Based on similar projects, we expect 80% efficiency gain"

**How Klaus responds:**
"95% ist Vendor-Marketing. Ich rechne mit 80%, das ist realistisch und defensible."

---

### Pitfall 3: Ignoring GDPR

❌ "We'll just use ChatGPT for processing customer invoices"
✅ "We understand invoices contain PII and need a GDPR-compliant solution"

**How Klaus responds:**
"Moment. Kundenrechnungen enthalten personenbezogene Daten. ChatGPT ist DSGVO-technisch inakzeptabel. Wir brauchen entweder Azure Germany oder On-Premise."

---

### Pitfall 4: Skipping Betriebsrat

❌ "We'll implement this and tell the works council later"
✅ "We'll involve the Betriebsrat from Phase 1"

**How Klaus responds:**
"Das ist ein Fehler. §87 BetrVG gibt dem Betriebsrat Mitbestimmungsrechte bei technischer Überwachung. Wenn Sie die zu spät einbinden, blockieren die das Projekt."

---

## FAQ

### Q: What if I don't have exact numbers?

**A:** Klaus will not proceed without numbers. Go back to your team and get:

- Time tracking data (or estimate based on observation)
- Process frequency (from your ERP/CRM logs)
- Hourly rates (from your HR department)

Better to have rough estimates than none.

---

### Q: What if the ROI is negative?

**A:** Klaus will tell you honestly:
"Die Zahlen ergeben keinen Business Case. Entweder sind Ihre Annahmen falsch, oder dieser Use Case ist nicht geeignet. Lassen Sie uns einen anderen Prozess suchen."

This is GOOD. Better to know now than after spending €50K.

---

### Q: Can I skip the GDPR phase?

**A:** No. Klaus will refuse:
"DSGVO ist nicht optional in Deutschland. Wir machen die Compliance-Prüfung, ob Sie wollen oder nicht."

---

### Q: What if my company doesn't have a Betriebsrat?

**A:** Klaus will note this but still include best practices:
"Kein Betriebsrat, verstanden. Trotzdem empfehle ich Transparenz gegenüber Mitarbeitern. Das vermeidet späteren Widerstand."

---

### Q: Can I use this workflow for non-German companies?

**A:** Yes, but:

- The language is German-focused
- GDPR applies EU-wide, but nuances differ
- Betriebsrat (Works Council) is German-specific; other countries have different structures
- Adapt the compliance section for your jurisdiction

---

## Post-Workflow: Next Steps

After Klaus generates the Strategic Roadmap:

1. **[Week 1]** Review with Geschäftsführung (Executive Team)
2. **[Week 2]** Present to Betriebsrat (if required)
3. **[Week 3]** Engage Datenschutzbeauftragter (DPO) for DSFA (Data Protection Impact Assessment)
4. **[Week 4]** Begin vendor selection for chosen architecture
5. **[Month 2]** Start Proof of Concept

---

## References

- **Porter, M.E. (1985):** Competitive Advantage: Creating and Sustaining Superior Performance
- **Kaplan, R.S. & Cooper, R. (1998):** Cost & Effect: Using Integrated Cost Systems
- **DSGVO (EU 2016/679):** Datenschutz-Grundverordnung, Articles 4, 5, 6, 32, 35
- **BetrVG §87:** Mitbestimmungsrechte des Betriebsrats

---

## Support

For questions or issues:

- Review the [BMSC Module README](../../readme.md)
- Check the [Validation Checklist](./checklist.md)
- Consult with Klaus: `*consult-sme`

---

**DISCLAIMER:** This workflow provides strategic consulting guidance. It is NOT legal advice. Always consult qualified legal counsel for GDPR interpretation and compliance decisions.

---

_Erstellt mit BMAD Strategy Consulting (BMSC)_
_"Ordnung muss sein" - But with mathematical rigor._
