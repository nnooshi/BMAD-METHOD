# German SME Consultant Suite (Mittelstand-AI)

**The "Consultant in a Pocket" for the German Manufacturing/SME Sector**

Version: 1.0.0
Module Code: `german-sme`
Status: Production Ready

---

## Overview

This BMAD module implements a **Multi-Agent Consulting System** that transforms raw AI project ideas into validated, German-context-aware execution roadmaps.

It combines **four proven frameworks** into a sequential pipeline:

1. **AI Canvas** (Prediction Machines) - Business Strategy
2. **AI Hierarchy of Needs** (Monica Rogati) - Data Maturity Assessment
3. **4-P Readiness Model** (Custom) - German Compliance & Culture
4. **CRISP-DM** (Industry Standard) - Project Execution Planning

### Why This Module Exists

**The Problem:**
- German SMEs (Mittelstand) want to do AI/ML projects
- International frameworks ignore German peculiarities (DSGVO, Betriebsrat, SAP R/3)
- Many projects fail due to:
  - Poor data infrastructure (40% still use Excel)
  - Legal/HR blockers discovered too late (Betriebsrat approval takes 3-6 months)
  - Vague business cases ("we want to optimize things")
  - Unrealistic timelines (ignoring German context)

**The Solution:**
A systematic consulting process that:
- Assesses data readiness HONESTLY (no sugarcoating)
- Identifies German-specific risks EARLY (before money is wasted)
- Forces strategic clarity (what are we predicting? why?)
- Produces realistic roadmaps (accounting for Betriebsrat, DSGVO, legacy IT)

---

## The 4 Frameworks

### 1. AI Canvas (Strategy Layer)
**Source:** "Prediction Machines" by Agrawal, Gans, and Goldfarb

**Purpose:** Strip away AI hype and define a clear business case.

**The 4 Boxes:**
- **PREDICTION:** What specific number/outcome are we predicting?
- **JUDGMENT:** Who decides what to do with that prediction?
- **ACTION:** What physical action changes based on the decision?
- **OUTCOME:** What's the business value (in Euros)?

**Why It Matters:** Forces precision. Rejects vague goals like "optimize operations" until they become measurable predictions like "probability of machine failure in next 7 days."

### 2. AI Hierarchy of Needs (Readiness Layer)
**Source:** Monica Rogati's Data Science framework

**Purpose:** Assess where the organization sits on the maturity pyramid.

**The 6 Levels:**
1. **Collection** - Paper/Excel (NOT READY)
2. **Storage/Flow** - Database but manual (NOT READY)
3. **Cleaning** - Automated pipelines but poor quality (ALMOST)
4. **Analytics** - Ready for BI and reporting (GO FOR ANALYTICS)
5. **Experimentation** - Ready for simple ML (GO FOR ML PILOTS)
6. **Advanced AI** - Production ML capability (GO FOR ANYTHING)

**Why It Matters:** Most German SMEs THINK they're at Level 5-6. Reality: 40% are at Level 1, 35% at Level 2-3. This prevents wasted investment in AI when the data foundation doesn't exist.

### 3. 4-P Readiness Model (Risk Layer)
**Source:** Custom framework for German/DACH context

**Purpose:** Identify German-specific legal and cultural risks.

**The 4 P's:**
- **Privacy:** DSGVO/GDPR compliance (strict in Germany)
- **Platform:** Legacy IT integration (SAP R/3, DATEV)
- **People:** Betriebsrat (Works Council) approval requirements
- **Proprietary:** IP/trade secret protection concerns

**Why It Matters:** International frameworks ignore that:
- German data protection authorities are aggressive (€20M fines possible)
- Betriebsrat can BLOCK projects for 3-6 months
- SAP R/3 integration costs 3-5x more than modern APIs
- German manufacturers are rightfully paranoid about IP theft

### 4. CRISP-DM (Execution Layer)
**Source:** Cross-Industry Standard Process for Data Mining (1996)

**Purpose:** Structure the project into 6 manageable phases with clear deliverables.

**The 6 Phases:**
1. **Business Understanding** - Define problem and success criteria
2. **Data Understanding** - Assess data availability and quality
3. **Data Preparation** - Clean and transform data
4. **Modeling** - Build and validate ML models
5. **Evaluation** - Validate with stakeholders and get approvals
6. **Deployment** - Production deployment and monitoring

**Why It Matters:** Proven methodology since 1996. Germans trust established processes. CRISP-DM provides the roadmap structure that integrates inputs from the other 3 frameworks.

---

## Module Architecture

### 4 Specialist Agents

#### 1. AI Canvas Strategist (`01-canvas-strategist.agent.yaml`)
**Role:** Business Strategy Consultant
**Framework:** Prediction Machines / AI Canvas
**Personality:** Direct, challenging, Socratic. Refuses vague goals.

**Key Behavior:**
- Asks: "What SPECIFIC NUMBER are you predicting?"
- Pushes back: "That's not a prediction, that's a wish."
- Forces quantification: "What's the cost in Euros?"

**Commands:**
- `/canvas-workshop` - Facilitate AI Canvas session
- `/validate-canvas` - Check completeness of existing canvas

#### 2. Data Maturity Auditor (`02-maturity-auditor.agent.yaml`)
**Role:** Data Infrastructure Auditor
**Framework:** AI Hierarchy of Needs
**Personality:** Brutally honest. "You want AI, but do you have a database?"

**Key Behavior:**
- Assesses actual maturity (not claimed maturity)
- Identifies blockers (Excel = Level 1 = NOT READY)
- Delivers NO-GO verdicts when needed

**Commands:**
- `/audit-maturity` - Full data maturity assessment
- `/maturity-report` - Generate detailed report

#### 3. DACH Compliance Officer (`03-compliance-officer.agent.yaml`)
**Role:** Legal & Cultural Compliance Specialist
**Framework:** 4-P Model
**Personality:** Cautious, detail-oriented. German Rechtsanwalt energy.

**Key Behavior:**
- Checks DSGVO compliance rigorously
- Identifies Betriebsrat risks early
- Warns about legacy IT integration pain
- Flags IP protection concerns

**Commands:**
- `/assess-4p` - Conduct 4-P risk assessment
- `/compliance-report` - Generate compliance report

#### 4. CRISP-DM Project Manager (`04-crisp-pm.agent.yaml`)
**Role:** AI/ML Project Manager
**Framework:** CRISP-DM
**Personality:** Organized, realistic. German Projektleiter precision.

**Key Behavior:**
- Synthesizes inputs from 3 frameworks
- Calculates realistic timelines (with German multiplier)
- Estimates budgets
- Defines phase-by-phase execution plan

**Commands:**
- `/generate-roadmap` - Create complete CRISP-DM roadmap
- `/phase-planning` - Detailed planning for specific phase

### Python Tools

Located in `tools/frameworks/`:

#### `canvas_tools.py`
- `structure_ai_canvas()` - Format AI Canvas as Markdown
- `validate_canvas_completeness()` - Check for missing/vague fields

#### `maturity_scorer.py`
- `assess_hierarchy_level()` - Assess maturity level (1-6)
- `calculate_readiness_score()` - Convert to 0-100 score
- `generate_maturity_report()` - Create formatted Markdown report

#### `dach_compliance.py`
- `score_4p_readiness()` - Calculate compliance score (0-100)
- `generate_4p_report()` - Create detailed risk assessment

#### `roadmap_generator.py`
- `generate_crisp_dm_pdf()` - Create complete CRISP-DM roadmap
- Timeline, budget, and phase calculation helpers

### Master Workflow

**File:** `workflows/master-sme-consult/workflow.yaml`

**Process Flow:**
```
START
  ↓
Stage 1: Maturity Assessment (GATE)
  └─ NO-GO → STOP (build infrastructure first)
  └─ GO/CAUTION → Continue
  ↓
Stage 2: Compliance Assessment (GATE)
  └─ HIGH RISK → STOP (address legal/HR blockers)
  └─ LOW/MEDIUM → Continue
  ↓
Stage 3: AI Canvas Workshop
  └─ Vague goals? → Loop until clear
  └─ Clear goals → Continue
  ↓
Stage 4: CRISP-DM Roadmap Generation
  ↓
Stage 5: Summary & Handoff
  ↓
END (4 deliverables created)
```

**Duration:** 1-2 hours for full process

**Outputs:**
1. `01-maturity-assessment.md`
2. `02-compliance-assessment.md`
3. `03-ai-canvas.md`
4. `04-CRISP-DM-ROADMAP.md`

---

## Installation

### Prerequisites
- BMAD Method installed
- Python 3.8+ (for framework tools)
- Output folder configured

### Install via BMAD CLI
```bash
bmad install german-sme
```

### Configuration Options

During installation, you'll be asked:

1. **Output Location:** Where to save consulting reports
   - Default: `{output_folder}/german-sme-reports`

2. **Default Company Name:** Used in reports (can override per project)
   - Default: "German SME"

3. **Default Currency:** For ROI calculations
   - EUR (€) - Recommended
   - CHF, USD

4. **Language Preference:**
   - German - Reports in German
   - English - Reports in English
   - Bilingual - Key terms in German, explanations in English (Recommended)

5. **Betriebsrat Context:** Do your clients typically have Works Councils?
   - Yes/No/Mixed

6. **Industry Focus:** Primary industry for context-specific advice
   - Manufacturing, Automotive, Logistics, Retail, Finance, Healthcare, General

7. **DSGVO Strict Mode:** Apply strictest German interpretations?
   - Yes (Recommended for Germany)
   - No (Standard EU GDPR)

8. **Documentation:** Install framework guides?
   - Yes (Recommended)

9. **Examples:** Include sample assessments?
   - Yes (Helpful for learning)

---

## Usage

### Quick Start: Full Consulting Process

```bash
# Run the master workflow
bmad run german-sme/master-sme-consult
```

This launches the 4-stage consulting pipeline. The agents will guide you through:
1. Data maturity assessment
2. Compliance risk assessment
3. AI Canvas workshop
4. CRISP-DM roadmap generation

**Time Required:** 1-2 hours
**Outputs:** 4 comprehensive documents in your configured output folder

### Use Individual Agents

#### Chat with the AI Canvas Strategist
```bash
bmad chat german-sme/canvas-strategist
```
Use for: Defining business cases, validating AI project ideas

#### Chat with the Data Maturity Auditor
```bash
bmad chat german-sme/maturity-auditor
```
Use for: Assessing data readiness before projects

#### Chat with the DACH Compliance Officer
```bash
bmad chat german-sme/compliance-officer
```
Use for: Risk assessment, DSGVO compliance checks

#### Chat with the CRISP-DM Project Manager
```bash
bmad chat german-sme/crisp-pm
```
Use for: Creating project roadmaps, timeline estimation

### Use Python Tools Directly

```python
from german_sme.tools.frameworks import (
    structure_ai_canvas,
    assess_hierarchy_level,
    score_4p_readiness,
    generate_crisp_dm_pdf
)

# Example: Assess maturity
assessment = assess_hierarchy_level(
    data_storage="sql",
    data_volume=50000,
    data_cleanliness="medium",
    has_data_pipeline=True,
    has_analytics_team=False,
    has_ml_experience=False
)
print(f"Maturity Level: {assessment['level']}/6")
print(f"Status: {assessment['status']}")
```

---

## Example Scenarios

### Scenario 1: Traditional Mittelstand Manufacturer
**Company Profile:**
- 150 employees
- Uses SAP R/3 (installed 1998)
- Data mostly in Excel exports
- Has Betriebsrat
- Wants "predictive maintenance AI"

**Module Output:**
- **Maturity:** Level 2 (NOT READY) - Need to build data pipelines first
- **Compliance:** Score 45 (HIGH RISK) - Betriebsrat + SAP R/3 integration
- **Recommendation:** Stop AI project. Invest 12 months in data infrastructure.
- **Timeline if proceeding anyway:** 24 months, €300K-500K

**Value:** Saved company from €100K+ wasted on premature AI project.

### Scenario 2: Modern SME with Good Data
**Company Profile:**
- 80 employees
- Modern ERP (Odoo)
- SQL database + automated pipelines
- No Betriebsrat
- Wants demand forecasting

**Module Output:**
- **Maturity:** Level 4 (READY for ML)
- **Compliance:** Score 85 (LOW RISK)
- **AI Canvas:** Clear prediction goal (forecast next 4 weeks demand)
- **Timeline:** 6 months, €80K-120K
- **Recommendation:** GO - Start with pilot in one product line

**Value:** Realistic roadmap with executive-ready business case.

### Scenario 3: Finance Company with PII
**Company Profile:**
- 200 employees
- Customer credit scoring project
- High-quality data but involves PII
- Has Betriebsrat

**Module Output:**
- **Maturity:** Level 5 (ML READY)
- **Compliance:** Score 55 (MEDIUM RISK) - PII + Betriebsrat
- **Key Risks:** DSGVO compliance, Betriebsrat approval (6 months)
- **Timeline:** 12 months (6 for legal/HR, 6 for technical)
- **Recommendation:** GO but budget 2x time for compliance

**Value:** Identified 6-month legal delay BEFORE starting development.

---

## Expected Outcomes

### What This Module Delivers

✅ **Honest Assessment**
- No sugarcoating of data maturity
- Clear NO-GO verdicts when appropriate
- Realistic timelines (not optimistic fantasies)

✅ **Early Risk Identification**
- Legal/HR blockers found BEFORE development
- German-specific issues highlighted
- Mitigation plans provided

✅ **Strategic Clarity**
- Vague goals ("optimize") become specific predictions
- ROI quantified in Euros
- Business value clearly defined

✅ **Actionable Roadmaps**
- Phase-by-phase execution plan
- Budget estimates
- Team requirements
- Success criteria

### What This Module Prevents

❌ **Wasted Investment**
- Don't build AI on Excel data
- Don't ignore Betriebsrat until month 8
- Don't discover DSGVO violations after deployment

❌ **Failed Projects**
- Poor problem definition
- Unrealistic timelines
- Missing stakeholder buy-in

❌ **Compliance Disasters**
- €20M DSGVO fines
- Project blocked by Works Council
- IP leaked to cloud providers

---

## Typical Timelines

**German AI Project Duration by Maturity:**

| Maturity Level | Compliance Score | Total Duration | Cost Estimate |
|----------------|------------------|----------------|---------------|
| 1-2 (Low) | <50 (High Risk) | 24+ months | €300K-500K |
| 3 (Medium) | 50-79 (Medium) | 15-18 months | €200K-350K |
| 4-5 (High) | 80+ (Low Risk) | 6-9 months | €80K-150K |
| 6 (Advanced) | 80+ (Low Risk) | 4-6 months | €60K-100K |

**Note:** US/UK equivalents would be 30-50% faster. German projects trade speed for:
- DSGVO compliance
- Worker participation (Betriebsrat)
- Engineering rigor (Gründlichkeit)
- Legal defensibility

---

## Best Practices

### For Consultants Using This Module

1. **Don't Skip Maturity Assessment:** It's tempting to jump to strategy. Resist. Bad data = failed AI.

2. **Deliver Bad News Early:** If they're not ready, say so NOW. Saves money and builds trust.

3. **Use German Time:** Always apply 1.5-2x multiplier to timelines. Under-promise, over-deliver.

4. **Involve Legal/HR Early:** Betriebsrat approval takes months. Start conversations immediately.

5. **Force Clarity on Canvas:** Don't accept "optimize" or "improve." Demand numbers.

### For German SMEs Using This Module

1. **Be Honest About Data:** Exaggerating quality wastes your money, not ours.

2. **Accept Timelines:** German projects take longer. It's not a bug, it's quality.

3. **Involve Betriebsrat Early:** Transparency builds trust. Surprises build resistance.

4. **Start with Pilots:** Prove value small before scaling big.

5. **Read All 4 Documents:** They build on each other. Don't skip to the roadmap.

---

## Troubleshooting

### "The maturity assessment says we're not ready, but we want to proceed anyway"
**Response:** You can, but you'll fail. Build data infrastructure first, THEN do AI. We're trying to save you money.

### "The timeline seems too long"
**Response:** It accounts for Betriebsrat approval (3-6 months), legal review (2-3 months), and SAP integration (2-4 months). If you don't have these, the timeline shortens. But most German SMEs DO have these.

### "Can we skip the compliance assessment?"
**Response:** No. Discovering DSGVO violations after deployment costs €20M in fines. Discovering Betriebsrat resistance in month 8 kills the project. Do it early.

### "The AI Canvas seems too simple"
**Response:** That's the point. If you can't fill 4 boxes, your strategy isn't clear. Complexity comes later, in execution.

### "We don't have a Betriebsrat"
**Response:** Great! Your timeline just got 3-6 months shorter. The module will reflect this in the compliance score.

---

## Technical Details

### Dependencies
- Python 3.8+
- BMAD Method core
- No external API calls (all local processing)

### File Structure
```
german-sme/
├── agents/                         # 4 agent definitions
│   ├── 01-canvas-strategist.agent.yaml
│   ├── 02-maturity-auditor.agent.yaml
│   ├── 03-compliance-officer.agent.yaml
│   └── 04-crisp-pm.agent.yaml
├── tools/frameworks/               # Python framework tools
│   ├── __init__.py
│   ├── canvas_tools.py
│   ├── maturity_scorer.py
│   ├── dach_compliance.py
│   └── roadmap_generator.py
├── workflows/
│   └── master-sme-consult/        # Main workflow
│       ├── workflow.yaml
│       ├── instructions.md
│       └── checklist.md
├── _module-installer/
│   └── install-config.yaml         # Installation configuration
├── docs/                           # Framework guides (optional)
├── data/                           # Static reference data
├── templates/                      # Report templates
└── README.md                       # This file
```

### Data Privacy
- All processing is local (no cloud APIs)
- No data leaves the user's machine
- Reports stored in user-configured output folder
- Suitable for sensitive/proprietary data

---

## Credits & References

### Frameworks
- **AI Canvas:** "Prediction Machines" by Ajay Agrawal, Joshua Gans, Avi Goldfarb
- **Hierarchy of Needs:** Monica Rogati's Data Science framework
- **CRISP-DM:** Cross-Industry Standard Process for Data Mining (1996)
- **4-P Model:** Custom framework for German AI readiness

### Inspiration
- German Mittelstand consulting experience
- Real-world AI project failures in DACH region
- DSGVO enforcement case studies
- Betriebsrat negotiation patterns

---

## License

Part of the BMAD Method.
See main repository for license details.

---

## Support & Contribution

**Issues:** Report bugs or suggest improvements via BMAD Method issue tracker

**Contribution:** This module is designed for the specific context of German/DACH SMEs. Adaptations for other regions welcome (but may require significant changes to compliance model).

**Version:** 1.0.0 (Production Ready)

---

## Final Note: The German Advantage

German AI projects take longer. But they:
- Comply with the world's strictest data protection laws
- Have worker buy-in (not resistance)
- Integrate with legacy systems (not ignore them)
- Are built to LAST (not just to launch)

This module helps you navigate that complexity. Use it wisely.

**Viel Erfolg!** (Good luck!)
