# German SME Master Consultant - Workflow Checklist

## Pre-Workflow Preparation

Before starting the consulting process, ensure:

- [ ] User has a specific AI project idea (even if vague)
- [ ] User has 1-2 hours available for the full assessment
- [ ] User has access to information about:
  - [ ] Current data storage systems
  - [ ] Legal/compliance status
  - [ ] Organizational structure (Betriebsrat?)
  - [ ] Budget constraints (approximate)
- [ ] Output folder is configured for saving deliverables

## Stage 1: Data Maturity Assessment

### Information Gathering
- [ ] Where is data stored? (Paper / Excel / SQL / Warehouse / Lake)
- [ ] How many records exist? (approximate volume)
- [ ] Data quality level? (Low / Medium / High)
- [ ] Automated data pipelines exist?
- [ ] Dedicated analytics/data team exists?
- [ ] Any ML experience on the team?

### Assessment
- [ ] Maturity level determined (1-6)
- [ ] Readiness score calculated (0-100)
- [ ] Status assigned (NO-GO / PROCEED WITH CAUTION / GO)
- [ ] Blockers identified
- [ ] Timeline to ML readiness estimated

### Deliverable
- [ ] Maturity assessment report saved: `01-maturity-assessment.md`

### Gate Decision
- [ ] If NO-GO: User acknowledges need to stop and build infrastructure
- [ ] If GO/CAUTION: User agrees to proceed to compliance assessment

## Stage 2: German Compliance & Risk Assessment

### Privacy (DSGVO/GDPR)
- [ ] Does project involve PII? (Yes/No)
- [ ] Data Protection Officer appointed? (Yes/No)
- [ ] Data storage location? (Germany / EU / US / Other)
- [ ] Legal review completed? (Yes/No)

### Platform (Legacy IT)
- [ ] Primary ERP/business system identified (SAP / DATEV / Custom / Modern)
- [ ] Data extraction method documented (Manual / Script / API)
- [ ] Integration complexity assessed

### People (Betriebsrat)
- [ ] Betriebsrat (Works Council) exists? (Yes/No)
- [ ] Project involves employee monitoring/changes? (Yes/No)
- [ ] Initial communication strategy planned

### Proprietary (IP Protection)
- [ ] Company IP/trade secrets involved? (Yes/No)
- [ ] Cloud AI services planned? (Yes/No)
- [ ] NDA requirements identified

### Assessment
- [ ] 4-P compliance score calculated (0-100)
- [ ] Risk level assigned (RED / YELLOW / GREEN)
- [ ] Blockers identified per P
- [ ] Mitigation recommendations provided
- [ ] Estimated delay calculated (weeks)

### Deliverable
- [ ] Compliance assessment report saved: `02-compliance-assessment.md`

### Gate Decision
- [ ] User acknowledges compliance risks
- [ ] User commits to mitigation plan
- [ ] If RED: User agrees to address blockers before technical work

## Stage 3: AI Canvas Strategy Workshop

### Prediction Box
- [ ] Specific prediction goal defined (not vague)
- [ ] Format identified (number, percentage, classification)
- [ ] Prediction frequency documented (hourly, daily, weekly)
- [ ] Current "cost of not knowing" quantified

### Judgment Box
- [ ] Decision owner identified (name and title)
- [ ] Decision authority confirmed
- [ ] Current decision-making process documented
- [ ] Risk tolerance assessed

### Action Box
- [ ] Specific operational action defined
- [ ] Action is observable and concrete
- [ ] Who executes the action identified
- [ ] Action frequency determined

### Outcome Box
- [ ] Business value quantified in Euros
- [ ] Current problem cost documented
- [ ] Potential savings/revenue calculated
- [ ] ROI timeline estimated

### Validation
- [ ] All 4 boxes filled with specific answers
- [ ] No vague language ("improve", "optimize", etc.)
- [ ] Monetary value clear
- [ ] Canvas completeness validated

### Deliverable
- [ ] AI Canvas document saved: `03-ai-canvas.md`

### Gate Decision
- [ ] User confirms canvas accurately represents project
- [ ] User validates ROI justifies investment

## Stage 4: CRISP-DM Roadmap Generation

### Data Collection
- [ ] Maturity assessment retrieved
- [ ] Compliance assessment retrieved
- [ ] AI Canvas data extracted
- [ ] Additional project constraints gathered (budget, deadlines, team)

### Timeline Calculation
- [ ] Base timeline calculated from maturity level
- [ ] Compliance delays added
- [ ] German context multiplier applied (1.5-2x)
- [ ] Total project duration determined

### Phase Planning
- [ ] Phase 1 (Business Understanding) - 1 month
- [ ] Phase 2 (Data Understanding) - duration based on maturity
- [ ] Phase 3 (Data Preparation) - duration based on maturity
- [ ] Phase 4 (Modeling) - 2-3 months
- [ ] Phase 5 (Evaluation) - duration based on compliance
- [ ] Phase 6 (Deployment) - 2-3 months

### Budget Estimation
- [ ] Base budget calculated (€10K/month × duration)
- [ ] Maturity adjustment applied
- [ ] Compliance adjustment applied
- [ ] Contingency added (20%)
- [ ] Budget range provided

### Team Requirements
- [ ] Roles identified per phase
- [ ] FTE allocations determined
- [ ] External support needs identified
- [ ] Training requirements documented

### Deliverable
- [ ] CRISP-DM roadmap saved: `04-CRISP-DM-ROADMAP.md`

## Stage 5: Final Summary & Handoff

### Summary Presentation
- [ ] All 4 deliverables reviewed with user
- [ ] Strengths highlighted
- [ ] Risks/challenges acknowledged
- [ ] Timeline reality-check delivered
- [ ] German context factors emphasized

### Next Steps Defined
- [ ] Week 1 action: Present to executive team
- [ ] Week 2 action: Secure budget commitment
- [ ] Week 3 action: Inform Betriebsrat (if applicable)
- [ ] Week 4 action: Kick off Phase 1

### Handoff Complete
- [ ] User has all 4 documents
- [ ] User understands realistic timeline
- [ ] User acknowledges German-specific delays
- [ ] User ready to present to stakeholders

## Post-Workflow Actions

### For the User
- [ ] Review all 4 documents thoroughly
- [ ] Schedule executive presentation
- [ ] Prepare budget request
- [ ] Plan Betriebsrat communication (if needed)
- [ ] Identify project team members

### For Future Reference
- [ ] Save all outputs to project folder
- [ ] Share with legal/compliance team
- [ ] Share with IT/data team
- [ ] Use as baseline for project tracking

## Quality Checks

### Maturity Assessment Quality
- [ ] Level assignment matches evidence provided
- [ ] Blockers are specific, not generic
- [ ] Timeline estimate is realistic, not optimistic

### Compliance Assessment Quality
- [ ] All 4 P's assessed (not just 1-2)
- [ ] German context considered (not generic GDPR)
- [ ] Risk score reflects actual complexity

### AI Canvas Quality
- [ ] Prediction is measurable (has a number/format)
- [ ] Judgment owner is a real person/role
- [ ] Action is physical and observable
- [ ] Outcome has Euro value

### Roadmap Quality
- [ ] Timeline includes German delays
- [ ] Budget is realistic (not just base calculation)
- [ ] Phases have clear deliverables
- [ ] Success criteria are measurable

## Red Flags (Stop and Reassess)

- [ ] ⚠️ User claims "perfect data quality" without evidence
- [ ] ⚠️ User dismisses DSGVO concerns ("we'll figure it out later")
- [ ] ⚠️ User has Betriebsrat but hasn't informed them
- [ ] ⚠️ AI Canvas prediction is still vague ("improve efficiency")
- [ ] ⚠️ User expects 3-month timeline for maturity level 2 project
- [ ] ⚠️ User has no budget estimate or approval process

If any red flag appears, pause and address before proceeding.

## Success Indicators

- [ ] ✅ User says "I didn't realize we weren't ready" (honest assessment)
- [ ] ✅ User acknowledges longer timeline than expected (realistic)
- [ ] ✅ User identifies specific next steps (actionable)
- [ ] ✅ User can explain their AI Canvas to a non-technical person (clarity)
- [ ] ✅ Legal/HR teams are already involved (early buy-in)

## Workflow Complete

All stages completed, all deliverables generated, user ready to proceed with informed decision.

**Final Status:**
- [ ] READY TO PROCEED (Green light with realistic expectations)
- [ ] PROCEED WITH MAJOR PREP WORK (Yellow - infrastructure/compliance work first)
- [ ] STOP AND REGROUP (Red - foundational gaps too large)

Date completed: _______________
Next review date: _______________
