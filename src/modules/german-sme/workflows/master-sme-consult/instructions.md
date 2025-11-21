# German SME Master Consultant - Workflow Instructions

## Overview

This workflow implements a 4-stage consulting pipeline that takes raw AI ideas and filters them through proven frameworks to produce validated, German-context-aware execution roadmaps.

## The 4 Stages

### Stage 1: Data Maturity Assessment (THE GATE)
**Agent:** Data Maturity Auditor
**Framework:** AI Hierarchy of Needs (Monica Rogati)
**Purpose:** Determine if the organization has the data foundation needed for AI

**Key Question:** "Where is your data stored RIGHT NOW?"

**Possible Outcomes:**
- ❌ **NO-GO (Level 1-2):** Data infrastructure doesn't exist - Stop and build foundation first
- ⚠️ **CAUTION (Level 3):** Data exists but needs cleaning - Proceed with data prep focus
- ✅ **GO (Level 4+):** Data foundation is solid - Ready for ML

**Why This is First:** No point planning an AI project if the data doesn't exist or is unusable.

### Stage 2: German Compliance & Risk Assessment (THE FILTER)
**Agent:** DACH Compliance Officer
**Framework:** 4-P Model (Privacy, Platform, People, Proprietary)
**Purpose:** Identify German-specific legal and cultural risks that could block the project

**Key Questions:**
- Privacy: "Does this involve personal data (PII)?"
- Platform: "What legacy systems do you use?" (SAP R/3? DATEV?)
- People: "Do you have a Betriebsrat (Works Council)?"
- Proprietary: "Does this involve company IP?"

**Possible Outcomes:**
- 🛑 **RED (<50 points):** High risk - Address legal/HR blockers before technical work
- ⚠️ **YELLOW (50-79):** Medium risk - Mitigation plan required
- ✅ **GREEN (80+):** Low risk - Standard governance applies

**Why This is Second:** Better to know about 6-month Betriebsrat delays NOW than after building the model.

### Stage 3: AI Canvas Strategy Workshop (THE DEFINITION)
**Agent:** AI Canvas Strategist
**Framework:** Prediction Machines / AI Canvas (Agrawal, Gans, Goldfarb)
**Purpose:** Define a clear, specific, measurable business case

**The 4 Canvas Boxes:**
1. **PREDICTION:** What specific number are we predicting?
2. **JUDGMENT:** Who decides what to do with that prediction?
3. **ACTION:** What physical action changes?
4. **OUTCOME:** What's the business value (in Euros)?

**Why This is Third:** Now that we know it's technically and legally feasible, define WHAT we're building and WHY.

### Stage 4: CRISP-DM Roadmap Generation (THE EXECUTION)
**Agent:** CRISP-DM Project Manager
**Framework:** CRISP-DM (Cross-Industry Standard Process for Data Mining)
**Purpose:** Create a phase-by-phase execution plan based on all previous assessments

**Inputs:**
- Maturity level (from Stage 1) → Affects Phases 2-3 duration
- Compliance score (from Stage 2) → Affects Phase 5 duration
- AI Canvas (from Stage 3) → Defines Phase 1 scope

**Output:** Complete project roadmap with:
- 6 CRISP-DM phases (Business Understanding → Data Understanding → Preparation → Modeling → Evaluation → Deployment)
- Realistic timeline (adjusted for German context)
- Budget estimation
- Team requirements
- Risk mitigation plan
- Success criteria

**Why This is Last:** Synthesizes all inputs into an actionable plan.

## The Flow Logic

```
START
  ↓
[Stage 1: Maturity Check] → NO-GO? → STOP (recommend infrastructure work)
  ↓ GO/CAUTION
[Stage 2: Compliance Check] → HIGH RISK? → STOP (address legal/HR blockers)
  ↓ LOW/MEDIUM RISK
[Stage 3: AI Canvas] → Vague goals? → LOOP (force clarity)
  ↓ CLEAR GOALS
[Stage 4: CRISP-DM Roadmap] → Generate final plan
  ↓
[Summary & Handoff] → END
```

## What Makes This "German-Aware"?

### Stage 1 (Maturity)
- Recognizes that 40% of German SMEs still use Excel/Paper
- Accounts for SAP R/3 data silos
- References "Digitalisierung" initiatives

### Stage 2 (Compliance)
- Checks for DSGVO compliance (stricter enforcement in Germany)
- Assesses Betriebsrat (Works Council) impact - unique to Germany
- Identifies legacy platform integration pain (SAP, DATEV)
- Considers German IP paranoia (justified by industrial espionage history)

### Stage 3 (Strategy)
- Uses Euros (not Dollars) for ROI calculations
- References German roles (Werksleiter, Geschäftsführer)
- Values precision over hype (German cultural preference)

### Stage 4 (Execution)
- Applies "German Time" multiplier (1.5-2x international timelines)
- Adds time for Betriebsrat negotiations (3-6 months)
- Budgets for legacy IT integration overhead
- Emphasizes "Gründlichkeit" (thoroughness) over speed

## Expected Timeline

**For a typical German SME AI project:**

| Maturity Level | Compliance Score | Total Duration |
|----------------|------------------|----------------|
| 1-2 (Low) | <50 (High Risk) | 24+ months |
| 3 (Medium) | 50-79 (Medium Risk) | 15-18 months |
| 4-5 (High) | 80+ (Low Risk) | 6-9 months |
| 6 (Advanced) | 80+ (Low Risk) | 4-6 months |

**Note:** US/UK equivalents would be 30-50% faster. German projects trade speed for sustainability, compliance, and worker buy-in.

## Deliverables

After completing the workflow, the user will have 4 documents:

1. `01-maturity-assessment.md` - Data readiness report
2. `02-compliance-assessment.md` - Risk assessment and mitigation plan
3. `03-ai-canvas.md` - Business case and strategy
4. `04-CRISP-DM-ROADMAP.md` - Complete execution plan

These documents can be presented to:
- Executive team (for budget approval)
- Legal department (for compliance sign-off)
- Betriebsrat (for worker approval)
- Technical team (for execution)

## When to Use This Workflow

**Ideal for:**
- German/DACH manufacturing SMEs ("Mittelstand")
- Companies new to AI/ML (need guidance)
- Projects involving PII or works council approval
- Organizations with legacy IT systems

**Not ideal for:**
- Startups with modern tech stacks (too much overhead)
- Non-German contexts (US, UK) - compliance model doesn't apply
- Companies that have already done multiple ML projects (too basic)

## Success Metrics

**The workflow is successful if:**
- User gets HONEST assessment of readiness (not just "yes, do AI")
- Legal/HR blockers are identified EARLY (not after months of dev work)
- Timeline expectations are REALISTIC (not optimistically wrong)
- Final roadmap is ACTIONABLE (not just theory)

**The workflow has FAILED if:**
- User is surprised by 6-month Betriebsrat delay in month 8
- Project gets blocked by DSGVO violation after building the model
- Data quality issues emerge in month 6 (should have been caught in Stage 1)
- ROI is vague and unmeasurable (Stage 3 failed)

## Tips for Users

1. **Be honest in Stage 1:** Don't exaggerate data quality or infrastructure
2. **Don't skip compliance:** Legal issues are project-killers
3. **Force clarity in Stage 3:** Vague goals = failed projects
4. **Accept German timelines:** Slow and steady wins the race
5. **Read ALL 4 documents:** They build on each other

## Framework Sources

- **AI Canvas:** "Prediction Machines" by Agrawal, Gans, Goldfarb
- **Hierarchy of Needs:** Monica Rogati's Data Science framework
- **4-P Model:** German AI readiness assessment (custom framework)
- **CRISP-DM:** Cross-Industry Standard Process for Data Mining (1996)

## Questions?

This workflow is part of the **German SME Consultant Module** for the BMAD Method.
For issues or suggestions, consult the module documentation.
