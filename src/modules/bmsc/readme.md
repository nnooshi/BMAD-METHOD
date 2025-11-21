# BMSC - BMad Strategy Consulting

**German SME AI Strategy Module ("Projekt Ordnung")**

Pragmatic, GDPR-compliant AI strategy consulting specifically designed for German Mittelstand (SME) companies. This module cuts through AI hype with mathematical rigor, Activity-Based Costing, and strict data sovereignty focus.

## Table of Contents

- [Philosophy](#philosophy)
- [Core Capabilities](#core-capabilities)
- [Specialized Agent](#specialized-agent)
- [Interactive Workflow](#interactive-workflow)
- [Quick Start](#quick-start)
- [Key Differentiators](#key-differentiators)
- [Configuration](#configuration)

## Philosophy

**Skeptical of Hype. Focused on Wertschöpfung (Value Creation).**

This module is built on three pillars:

1. **Mathematical Rigor** - Activity-Based Costing, no handwaving
2. **GDPR Compliance** - Datensouveränität (data sovereignty) first
3. **Porter's Value Chain** - Systematic process categorization

## Core Capabilities

BMSC provides structured consulting methodology through an expert persona who:

- Demands precise numbers: "How many minutes? How often? What hourly rate?"
- Maps every use case to Porter's Value Chain
- Calculates ROI using Activity-Based Costing
- Evaluates GDPR risks before technical feasibility
- Recommends architecture based on data sensitivity

## Specialized Agent

[View detailed agent description →](./agents/README.md)

**Klaus** - Senior AI Strategy Consultant (DACH Region)

- Cynical, pragmatic German management consultant
- 15+ years experience with Mittelstand companies
- Expert in DSGVO (GDPR), Activity-Based Costing, Porter's frameworks
- Speaks in German business terminology (Wertschöpfung, Betriebsrat, etc.)

## Interactive Workflow

[View workflow details →](./workflows/README.md)

**German SME Consulting Workflow** - 4 structured phases:

### Phase 1: Value Chain Interview (Discovery)

- Identify manual bottleneck
- Map to Porter's Value Chain
- Categorize as Primary vs. Support activity

### Phase 2: GDPR Filter (Feasibility)

- PII assessment
- Digital vs. paper check
- Risk scoring (HIGH/MEDIUM/LOW)

### Phase 3: The Calculator (ROI)

- Collect: frequency, time, hourly rate
- Calculate: current costs, projected savings, break-even
- Use Activity-Based Costing methodology

### Phase 4: The Blueprint (Architecture)

- Propose technical stack based on risk level
- HIGH risk → On-Premise / Local LLM
- LOW risk → Azure OpenAI Germany West
- Generate comprehensive strategic roadmap

## Quick Start

### Direct Workflow

```bash
# Start interactive consulting session
workflow german-sme-consult
```

### Agent-Facilitated

```bash
# Load the Strategy Coach agent
agent bmsc/strategy-coach

# Start workflow
> *consult-sme
```

### Example Session

```
Klaus: "Guten Tag. Ich bin Klaus, Senior Partner für KI-Strategie im DACH-Raum.

Vergessen Sie den KI-Hype. Wir sprechen heute nur über Wertschöpfung und Datenschutz.

Sagen Sie mir: Was ist Ihr größter manueller Flaschenhals?
Und bitte keine vagen Antworten wie 'Dokumentenverwaltung' -
ich brauche den exakten Prozess."

You: "Unsere Buchhaltung erfasst monatlich 150 Eingangsrechnungen manuell,
     dauert jeweils ca. 15 Minuten pro Rechnung."

Klaus: "Ausgezeichnet. Das ist 'Inbound Logistics' nach Porter.

       Zweite Frage: Enthalten diese Rechnungen personenbezogene Daten?
       Namen von Mitarbeitern? Spesenbelege?"

[... workflow continues through all 4 phases ...]
```

## Key Differentiators

- **Anti-Hype Stance** - No buzzwords, only math
- **GDPR-First** - Compliance before technology
- **Mittelstand-Specific** - Understands SAP, Betriebsrat, German business culture
- **Activity-Based Costing** - Precise financial impact calculation
- **Architecture Pragmatism** - Risk-based technology recommendations

## Configuration

Edit `/{bmad_folder}/bmsc/config.yaml`:

```yaml
output_folder: ./bmsc-output
user_name: CEO
communication_language: german
document_output_language: german
user_skill_level: advanced

default_assumptions:
  implementation_cost: 15000 # EUR
  efficiency_gain_percent: 80
  error_rate_percent: 5

compliance:
  assume_sap_landscape: true
  assume_works_council: true
  default_privacy_stance: strict
```

## Module Structure

```
bmsc/
├── agents/
│   └── strategy-coach.agent.yaml   # Klaus - The Strategy Coach
├── workflows/
│   └── german-sme-consult/
│       ├── workflow.yaml            # 4-phase consulting flow
│       ├── instructions.md          # Detailed methodology
│       ├── template.md              # Output template
│       └── checklist.md             # Validation checklist
├── tools/
│   ├── financial_tools.js           # ROI & ABC calculations
│   └── report_generator.js          # Strategic blueprint generator
├── config.yaml                      # Module configuration
└── readme.md                        # This file
```

## Output Artifacts

The workflow generates:

1. **STRATEGIC_ROADMAP.md** - Comprehensive strategic document including:
   - Executive Summary
   - Use Case Analysis (Porter's Value Chain)
   - GDPR Compliance Assessment
   - ROI Analysis (3-year TCO)
   - Technical Architecture Recommendation
   - Implementation Roadmap (3 phases)
   - Risk Assessment & Mitigation
   - KPIs & Governance

## Tools & Calculations

### Financial Tools

- `calculateProcessROI()` - Activity-Based Costing ROI calculator
- `formatROIReport()` - German financial report formatter
- `assessGDPRRisk()` - GDPR risk scoring engine
- `validateValueChainCategory()` - Porter's framework validator

### Report Generator

- `createStrategicBlueprint()` - Full strategic roadmap generator
- `generateExecutiveSummary()` - Quick summary extractor

## Integration Points

BMSC workflows integrate with:

- **BMM** - Can feed into technical planning phase
- **BMB** - Can create custom industry-specific variants
- **Custom Modules** - Reusable consulting methodology

## Best Practices

1. **Have Numbers Ready** - Frequency, time, hourly rates
2. **Know Your Data** - PII yes/no, digital status
3. **Be Honest** - Don't oversell the use case
4. **Involve Stakeholders Early** - Betriebsrat, Datenschutzbeauftragter
5. **Start Small** - PoC before full rollout

## Legal Disclaimer

This module provides strategic consulting guidance based on:

- Porter, M.E. (1985): Competitive Advantage
- Kaplan, R.S. & Cooper, R. (1998): Activity-Based Costing
- DSGVO (EU 2016/679): Articles 4, 5, 6, 32, 35

**This is NOT legal advice.** Always consult with:

- Qualified legal counsel for GDPR interpretation
- Datenschutzbeauftragter (Data Protection Officer)
- Betriebsrat (Works Council) before employee data processing

## Related Documentation

- **[Workflow Guide](./workflows/README.md)** - Detailed workflow instructions
- **[Agent Persona](./agents/README.md)** - Full agent description
- **[Tools Documentation](./tools/README.md)** - Technical API reference

## Language & Terminology

This module uses German business terminology:

- **Mittelstand** - Small and medium-sized enterprises (SME)
- **Wertschöpfung** - Value creation
- **Datenschutz** - Data protection / privacy
- **DSGVO** - German name for GDPR (Datenschutz-Grundverordnung)
- **Betriebsrat** - Works council (employee representation)
- **Datensouveränität** - Data sovereignty

## Roadmap

Future enhancements:

- [ ] Industry-specific templates (Manufacturing, Logistics, Financial Services)
- [ ] Multi-use-case portfolio optimization
- [ ] Integration with actual SAP APIs for real-time costing
- [ ] Automated DSFA (Datenschutz-Folgenabschätzung) generator

---

Part of BMad Method v6.0 - **"Ordnung muss sein"** (There must be order)

Built with ❤️ (and skepticism) for the German Mittelstand.
