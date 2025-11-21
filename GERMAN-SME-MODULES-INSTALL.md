# German SME Consulting Modules - Installation Guide

## Overview

This guide explains how to install and use the two new German SME consulting modules added to the BMAD Method:

1. **BMSC** (BMad Strategy Consulting) - German SME AI strategy consulting
2. **German SME** - Multi-agent consulting suite with 4 frameworks

Both modules are designed specifically for German Mittelstand (SME) companies and provide comprehensive AI project consulting capabilities.

---

## Module Compatibility

Both modules have been verified to be fully compatible with the BMAD Module Structure Guide requirements:

### ✅ Structure Compliance

**BMSC Module:**
- ✅ Agents: `strategy-coach.agent.yaml`
- ✅ Workflows: `german-sme-consult/`
- ✅ Tools: `financial_tools.js`, `report_generator.js`
- ✅ Module Installer: `_module-installer/install-config.yaml`, `installer.js`
- ✅ README.md
- ✅ No config.yaml in source (generated during installation)

**German SME Module:**
- ✅ Agents: 4 specialist agents (Canvas Strategist, Maturity Auditor, Compliance Officer, CRISP-DM PM)
- ✅ Workflows: `master-sme-consult/`
- ✅ Tools: Python frameworks (canvas_tools, maturity_scorer, dach_compliance, roadmap_generator)
- ✅ Module Installer: `_module-installer/install-config.yaml`
- ✅ README.md
- ✅ No config.yaml in source (generated during installation)

---

## Prerequisites

Before installing these modules, ensure you have:

1. **BMAD Method v6.0+** installed
2. **Node.js** (for BMAD CLI)
3. **Python 3.8+** (for German SME framework tools)
4. A **BMAD project** initialized (or you can install during project setup)

---

## Installation Methods

### Method 1: Install During New Project Setup (Recommended)

When creating a new BMAD project, both modules will be available in the module selection menu:

```bash
# Initialize a new BMAD project
bmad init my-german-sme-project

# During installation, you'll see:
# ┌─────────────────────────────────────┐
# │ Select Modules to Install           │
# ├─────────────────────────────────────┤
# │ [x] Core                            │
# │ [x] BMM (BMad Method)               │
# │ [ ] BMSC (BMad Strategy Consulting) │  ← Select this for BMSC
# │ [ ] German SME Consultant Suite     │  ← Select this for German SME
# │ [ ] CIS                             │
# │ ...                                 │
# └─────────────────────────────────────┘
```

**Note:** Both modules have `default_selected: false` because they are specialized modules. You need to manually select them during installation.

### Method 2: Add to Existing Project

If you already have a BMAD project, you can add the modules:

```bash
# Navigate to your project
cd my-bmad-project

# Re-run the installer and select additional modules
bmad install

# Or install specific modules directly
bmad install bmsc
bmad install german-sme
```

---

## Configuration During Installation

### BMSC Configuration Questions

When installing BMSC, you'll be asked:

1. **Output Location** - Where to save strategic consulting documents
   - Default: `{output_folder}/bmsc-output`

2. **Default Implementation Cost** - EUR estimate for ROI calculations
   - Default: 15000

3. **Default Efficiency Gain** - Percentage for ROI projections
   - Default: 80%

4. **Default Error Rate** - Percentage if not specified
   - Default: 5%

5. **Assume SAP Landscape** - Do German SME clients typically use SAP?
   - Default: Yes

6. **Assume Works Council** - Do clients have Betriebsrat?
   - Default: Yes

### German SME Configuration Questions

When installing German SME, you'll be asked:

1. **Output Location** - Where to save consulting reports and roadmaps
   - Default: `{output_folder}/german-sme-reports`

2. **Default Company Name** - Used in reports (can override per project)
   - Default: "German SME"

3. **Default Currency** - For ROI calculations
   - Options: EUR (recommended), CHF, USD

4. **Language Preference**
   - German: Reports in German
   - English: Reports in English
   - **Bilingual** (recommended): Key terms in German, explanations in English

5. **Betriebsrat Default** - Do organizations typically have Works Council?
   - Options: Yes, No, Mixed

6. **Industry Focus** - Primary industry for context-specific advice
   - Options: Manufacturing, Automotive, Logistics, Retail, Finance, Healthcare, General

7. **DSGVO Strict Mode** - Apply strictest German GDPR interpretations?
   - Default: Yes (recommended for Germany)

8. **Install Framework Docs** - Install all guides (AI Canvas, Hierarchy, 4-P, CRISP-DM)?
   - Default: Yes

9. **Include Examples** - Install example assessments and roadmaps?
   - Default: Yes

---

## Post-Installation Verification

After installation, verify both modules are installed correctly:

```bash
# Check installed modules in your project
ls {your-bmad-folder}/

# You should see:
# - core/
# - bmm/
# - bmsc/           ← BMSC module
# - german-sme/     ← German SME module

# Check module configuration
cat {your-bmad-folder}/bmsc/config.yaml
cat {your-bmad-folder}/german-sme/config.yaml
```

---

## Usage Guide

### BMSC Module

#### Quick Start

```bash
# Navigate to your project
cd my-bmad-project

# Option 1: Run the workflow directly
bmad workflow run bmsc/german-sme-consult

# Option 2: Load the agent and use commands
bmad agent load bmsc/strategy-coach
# Then use: *consult-sme, *calculate-roi, *assess-gdpr-risk, *validate-value-chain, *generate-blueprint
```

#### Example Session

```
Klaus (Strategy Coach): "Guten Tag. Ich bin Klaus, Senior Partner für KI-Strategie im DACH-Raum.

Vergessen Sie den KI-Hype. Wir sprechen heute nur über Wertschöpfung und Datenschutz.

Sagen Sie mir: Was ist Ihr größter manueller Flaschenhals?"

You: "Unsere Buchhaltung erfasst monatlich 150 Eingangsrechnungen manuell,
     dauert jeweils ca. 15 Minuten pro Rechnung."

Klaus: "Ausgezeichnet. Das ist 'Inbound Logistics' nach Porter.
       Zweite Frage: Enthalten diese Rechnungen personenbezogene Daten?"
```

#### Output Artifacts

BMSC generates:
- `STRATEGIC_ROADMAP.md` - Comprehensive strategic blueprint
- `ROI_CALCULATION.md` - Activity-Based Costing breakdown
- `ARCHITECTURE_RECOMMENDATION.md` - Risk-based technical architecture

### German SME Module

#### Quick Start

```bash
# Run the master consulting workflow (recommended)
bmad workflow run german-sme/master-sme-consult

# Or chat with individual agents:
bmad agent load german-sme/01-canvas-strategist
bmad agent load german-sme/02-maturity-auditor
bmad agent load german-sme/03-compliance-officer
bmad agent load german-sme/04-crisp-pm
```

#### Master Workflow Process

The master workflow runs through 4 stages:

1. **Maturity Assessment** (GATE)
   - Assesses data readiness (Level 1-6)
   - NO-GO if infrastructure isn't ready
   - Output: `01-maturity-assessment.md`

2. **Compliance Assessment** (GATE)
   - Evaluates 4-P risks (Privacy, Platform, People, Proprietary)
   - HIGH RISK if legal/HR blockers exist
   - Output: `02-compliance-assessment.md`

3. **AI Canvas Workshop**
   - Defines clear business case
   - Forces precision in goals
   - Output: `03-ai-canvas.md`

4. **CRISP-DM Roadmap Generation**
   - Creates 6-phase execution plan
   - Realistic timelines and budgets
   - Output: `04-CRISP-DM-ROADMAP.md`

**Duration:** 1-2 hours for full process

---

## Module Comparison

| Feature | BMSC | German SME |
|---------|------|------------|
| **Focus** | Single-agent strategy consulting | Multi-agent consulting suite |
| **Agents** | 1 (Klaus, Strategy Coach) | 4 (Canvas, Maturity, Compliance, CRISP-DM) |
| **Frameworks** | Porter's Value Chain, Activity-Based Costing | AI Canvas, Hierarchy of Needs, 4-P, CRISP-DM |
| **Best For** | Quick ROI calculations, strategic blueprints | Comprehensive assessments, full project roadmaps |
| **Tools** | JavaScript (financial_tools, report_generator) | Python (canvas_tools, maturity_scorer, etc.) |
| **Output** | Strategic roadmap, ROI report, architecture | 4 assessments (maturity, compliance, canvas, roadmap) |
| **Complexity** | Simple Module (1 agent, 1 workflow) | Standard Module (4 agents, 1 master workflow) |

### When to Use Which Module

**Use BMSC when:**
- You need a quick strategic assessment
- Focus is on ROI calculations
- You want Porter's Value Chain analysis
- Single consultant persona is preferred

**Use German SME when:**
- You need comprehensive assessment across all dimensions
- Data maturity is uncertain
- Compliance risks are complex
- You want a full CRISP-DM roadmap

**Use Both together:**
- Run German SME first for comprehensive assessment
- Use BMSC for follow-up strategic refinement
- German SME identifies "what," BMSC optimizes "how"

---

## Troubleshooting

### Module Not Appearing During Installation

**Issue:** Module doesn't show up in selection menu

**Solution:**
1. Ensure you're using BMAD Method v6.0+
2. Check that `_module-installer/install-config.yaml` exists in both module directories
3. Verify `code` field is defined in install-config.yaml
4. Re-run `bmad init` or `bmad install`

### Configuration Not Saving

**Issue:** Module installs but configuration doesn't persist

**Solution:**
1. Check that `config.yaml` exists in `{bmad-folder}/bmsc/` or `{bmad-folder}/german-sme/`
2. Verify write permissions on project directory
3. Re-run installation with `bmad install --force`

### Python Tools Not Working (German SME)

**Issue:** Framework tools fail to execute

**Solution:**
1. Ensure Python 3.8+ is installed: `python --version`
2. Check tools are in correct location: `ls {bmad-folder}/german-sme/tools/frameworks/`
3. Verify `__init__.py` exists in frameworks directory
4. Install any missing Python dependencies

---

## Integration with Existing Modules

Both modules integrate seamlessly with existing BMAD modules:

### BMM Integration

- BMSC/German SME can feed into BMM's technical planning phase
- Use consulting outputs as input for BMM workflows
- Combine strategic assessment with agile execution

### BMB Integration

- Can create custom industry-specific module variants
- Reuse consulting methodologies in new contexts
- Build specialized modules for different sectors

---

## Updating Modules

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Re-run installer to update modules
bmad install --update

# Or update specific modules
bmad update bmsc
bmad update german-sme
```

---

## Module Documentation

For detailed module information, see:

- **BMSC:** `{bmad-folder}/bmsc/README.md`
- **German SME:** `{bmad-folder}/german-sme/README.md`
- **Module Structure Guide:** `src/modules/bmb/workflows/create-module/module-structure.md`

---

## Support

### Getting Help

1. **Module Issues:** Check module README files
2. **Installation Issues:** Review this guide
3. **Framework Questions:** Refer to framework documentation in module docs
4. **Bug Reports:** Submit to BMAD Method repository

### Contribution

Both modules are open for:
- Industry-specific adaptations
- Additional frameworks
- Tool enhancements
- Localization (other languages)

---

## Legal Disclaimer

Both modules provide consulting guidance based on established frameworks:

- Porter, M.E. (1985): Competitive Advantage
- Kaplan, R.S. & Cooper, R. (1998): Activity-Based Costing
- Agrawal et al. (2018): Prediction Machines
- Monica Rogati: AI Hierarchy of Needs
- DSGVO (EU 2016/679): Articles 4, 5, 6, 32, 35

**This is NOT legal advice.** Always consult with:
- Qualified legal counsel for GDPR interpretation
- Datenschutzbeauftragter (Data Protection Officer)
- Betriebsrat (Works Council) before employee data processing

---

## Version History

- **v1.0.0** (2025-11-21): Initial release
  - BMSC module with Activity-Based Costing
  - German SME module with 4-framework approach
  - Full installer integration
  - Comprehensive documentation

---

## Quick Reference

```bash
# Install both modules
bmad init my-project
# Select: BMSC + German SME during installation

# Run BMSC workflow
bmad workflow run bmsc/german-sme-consult

# Run German SME master workflow
bmad workflow run german-sme/master-sme-consult

# Load agents
bmad agent load bmsc/strategy-coach
bmad agent load german-sme/01-canvas-strategist
bmad agent load german-sme/02-maturity-auditor
bmad agent load german-sme/03-compliance-officer
bmad agent load german-sme/04-crisp-pm
```

---

**Viel Erfolg!** (Good luck!)

Built with ❤️ (and skepticism) for the German Mittelstand.
