/**
 * Report Generator for German SME AI Strategy Consulting
 * Creates comprehensive strategic blueprints in Markdown format
 */

const fs = require("fs-extra");
const path = require("path");

/**
 * Create a strategic AI blueprint document
 *
 * @param {Object} data - Blueprint data
 * @param {string} data.company_name - Name of the SME
 * @param {string} data.use_case - Description of the AI use case
 * @param {string} data.value_chain_category - Porter's Value Chain category
 * @param {Object} data.risk_assessment - GDPR risk assessment results
 * @param {Object} data.roi_stats - ROI calculation results
 * @param {string} data.architecture_choice - Recommended technical architecture
 * @param {string} [data.output_path] - Custom output path
 * @returns {Promise<string>} Path to generated document
 */
async function createStrategicBlueprint(data) {
  const {
    company_name = "Unternehmen",
    use_case,
    value_chain_category,
    risk_assessment,
    roi_stats,
    architecture_choice,
    output_path,
  } = data;

  // Validate required fields
  if (!use_case || !value_chain_category || !risk_assessment || !roi_stats || !architecture_choice) {
    throw new Error(
      "Missing required fields: use_case, value_chain_category, risk_assessment, roi_stats, architecture_choice",
    );
  }

  const date = new Date().toISOString().split("T")[0];

  // Generate the blueprint document
  const blueprint = generateBlueprintMarkdown({
    company_name,
    use_case,
    value_chain_category,
    risk_assessment,
    roi_stats,
    architecture_choice,
    date,
  });

  // Determine output path
  const defaultPath = path.join(process.cwd(), "docs", "STRATEGIC_ROADMAP.md");
  const finalPath = output_path || defaultPath;

  // Ensure directory exists
  await fs.ensureDir(path.dirname(finalPath));

  // Write the document
  await fs.writeFile(finalPath, blueprint, "utf8");

  return finalPath;
}

/**
 * Generate the complete blueprint markdown
 *
 * @private
 */
function generateBlueprintMarkdown({
  company_name,
  use_case,
  value_chain_category,
  risk_assessment,
  roi_stats,
  architecture_choice,
  date,
}) {
  const { formatROIReport } = require("./financial_tools");

  return `# VERTRAULICH - STRATEGISCHE KI-ROADMAP

**Unternehmen:** ${company_name}
**Datum:** ${date}
**Status:** Strategisches Konzept

---

## EXECUTIVE SUMMARY

Dieses Dokument präsentiert eine datengetriebene Strategie zur KI-Integration basierend auf Activity-Based Costing, DSGVO-Compliance und Porter's Value Chain Analyse.

**Kernaussagen:**
- **Wertschöpfung:** ${value_chain_category}
- **Datenschutz-Risiko:** ${risk_assessment.risk_level}
- **ROI (3 Jahre):** ${roi_stats.roi_analysis.roi_percent}%
- **Amortisation:** ${roi_stats.roi_analysis.break_even_months} Monate
- **Empfohlene Architektur:** ${architecture_choice}

---

## 1. AUSGANGSLAGE & USE CASE

### 1.1 Geschäftskontext

**Use Case:**
${use_case}

**Einordnung in Wertkette (Porter):**
${value_chain_category}

### 1.2 Problemstellung

Der identifizierte Prozess verursacht aktuell:
- **Monatliche Kosten:** €${roi_stats.current_state.total_monthly_cost.toLocaleString("de-DE")}
- **Jährliche Belastung:** €${roi_stats.current_state.annual_cost.toLocaleString("de-DE")}

Diese Kosten setzen sich zusammen aus:
- Direkte Arbeitszeit: €${roi_stats.current_state.monthly_cost_asis.toLocaleString("de-DE")}/Monat
- Fehlerfolgekosten: €${roi_stats.current_state.monthly_error_cost.toLocaleString("de-DE")}/Monat

---

## 2. COMPLIANCE & DATENSOUVERÄNITÄT

### 2.1 DSGVO-Bewertung (Artikel 4, 5, 6 DSGVO)

**Risikostufe:** ${risk_assessment.risk_level}
**Risiko-Score:** ${risk_assessment.risk_score}/100

**Identifizierte Risikofaktoren:**
${risk_assessment.factors.map((factor) => `- ${factor}`).join("\n")}

### 2.2 Rechtliche Anforderungen

${generateComplianceSection(risk_assessment.risk_level)}

### 2.3 Betriebsrat-Relevanz

${generateWorksCouncilSection(risk_assessment)}

---

${formatROIReport(roi_stats)}

---

## 4. TECHNISCHE ARCHITEKTUR

### 4.1 Empfohlene Lösung

**Architektur:** ${architecture_choice}

${generateArchitectureDetails(architecture_choice, risk_assessment.risk_level)}

### 4.2 Integrationsstrategie

**Bestehende Systemlandschaft:**
- Annahme: SAP ERP als Kernsystem
- Annahme: Microsoft 365 für Collaboration
- Annahme: On-Premise Datenhaltung präferiert

**Integrationspunkte:**
1. **Datenextraktion:** REST APIs / BAPI Calls
2. **Verarbeitung:** Dedizierte KI-Schicht
3. **Rückführung:** Structured Data Import

### 4.3 Datenschutz-Architektur

${generatePrivacyArchitecture(risk_assessment.risk_level)}

---

## 5. UMSETZUNGS-ROADMAP

### Phase 1: Proof of Concept (Monate 1-2)
- **Ziel:** Technische Machbarkeit validieren
- **Scope:** 10% des Prozessvolumens
- **Budget:** €${Math.round(roi_stats.roi_analysis.implementation_cost * 0.2).toLocaleString("de-DE")}
- **Success Criteria:** 60% Effizienzgewinn nachweisbar

### Phase 2: Pilotierung (Monate 3-4)
- **Ziel:** Produktivbetrieb mit ausgewählten Nutzern
- **Scope:** 50% des Prozessvolumens
- **Budget:** €${Math.round(roi_stats.roi_analysis.implementation_cost * 0.3).toLocaleString("de-DE")}
- **Success Criteria:** 75% Effizienzgewinn, Betriebsrat-Zustimmung

### Phase 3: Rollout (Monate 5-6)
- **Ziel:** Vollständige Implementierung
- **Scope:** 100% des Prozessvolumens
- **Budget:** €${Math.round(roi_stats.roi_analysis.implementation_cost * 0.5).toLocaleString("de-DE")}
- **Success Criteria:** 80% Effizienzgewinn erreicht

---

## 6. RISIKEN & MITIGATION

### 6.1 Technische Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|---------|------------|
| Modell-Genauigkeit unzureichend | Mittel | Hoch | PoC mit klaren Akzeptanzkriterien |
| Integration komplex | Hoch | Mittel | Schrittweise Integration, API-First |
| Performance-Probleme | Niedrig | Mittel | Load Testing in Pilotphase |

### 6.2 Rechtliche Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|---------|------------|
| DSGVO-Verstoß | ${risk_assessment.risk_level === "HIGH" ? "Hoch" : "Niedrig"} | Sehr Hoch | ${risk_assessment.recommendation} |
| Betriebsrat blockiert | Mittel | Hoch | Frühzeitige Einbindung, Transparenz |
| Audit-Trail unzureichend | Niedrig | Mittel | Logging-Konzept ab Tag 1 |

### 6.3 Change Management

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|---------|------------|
| Nutzerakzeptanz niedrig | Mittel | Hoch | Training, Champions-Programm |
| Skill-Gap im Team | Hoch | Mittel | Externe Unterstützung, Wissenstransfer |

---

## 7. ERFOLGSMESSUNG

### 7.1 Key Performance Indicators (KPIs)

**Finanzielle KPIs:**
- Tatsächliche vs. prognostizierte Einsparungen
- Time-to-Break-Even
- TCO nach 12/24/36 Monaten

**Operative KPIs:**
- Prozessdurchlaufzeit (vorher/nachher)
- Fehlerrate (vorher/nachher)
- Nutzerakzeptanz (NPS-Score)

**Compliance KPIs:**
- DSGVO-Audit-Ergebnisse
- Anzahl Datenschutzvorfälle
- Betriebsrat-Zufriedenheit

### 7.2 Governance

**Entscheidungsgremium:**
- Sponsor: Geschäftsführung
- Product Owner: Fachbereichsleitung
- Technical Lead: IT-Leitung
- Compliance: Datenschutzbeauftragter
- Stakeholder: Betriebsrat

**Review-Zyklen:**
- Wöchentlich: Projektteam
- Monatlich: Steering Committee
- Quartalsweise: Geschäftsführung

---

## 8. NÄCHSTE SCHRITTE

1. **[SOFORT]** Dieses Konzept mit Geschäftsführung abstimmen
2. **[Woche 1]** Betriebsrat informieren und Workshop terminieren
3. **[Woche 2]** Datenschutzbeauftragten einbinden, DSFA initiieren
4. **[Woche 3-4]** Vendor-Auswahl für ${architecture_choice}
5. **[Monat 2]** PoC-Start

---

## APPENDIX A: Berechnungsgrundlagen

**Input-Parameter:**
- Häufigkeit: ${roi_stats.inputs.frequency_per_month}x pro Monat
- Zeitaufwand: ${roi_stats.inputs.minutes_per_task} Minuten pro Vorgang
- Stundensatz: €${roi_stats.inputs.hourly_rate_euro}
- Fehlerrate: ${roi_stats.inputs.error_rate_percent}%
- Implementierungskosten: €${roi_stats.inputs.implementation_cost.toLocaleString("de-DE")}

**Annahmen:**
- Effizienzgewinn: ${roi_stats.future_state.efficiency_gain_percent}% (konservativ)
- Laufzeit: 3 Jahre
- Maintenance: 15% p.a. der Implementierungskosten (separat zu kalkulieren)

---

## APPENDIX B: Referenzen

**Methodologie:**
- Porter, M.E. (1985): Competitive Advantage
- Kaplan, R.S. & Cooper, R. (1998): Activity-Based Costing
- DSGVO (EU 2016/679): Artikel 4, 5, 6, 32, 35

**Vergleichbare Fälle:**
- (Hier würden bei einer echten Beratung anonymisierte Case Studies stehen)

---

**DISCLAIMER:** Dieses Dokument stellt ein strategisches Konzept dar und ersetzt keine Rechtsberatung. Vor Implementierung ist eine Datenschutz-Folgenabschätzung (DSFA gem. Art. 35 DSGVO) durchzuführen.

---

*Erstellt mit BMAD Strategy Consulting (BMSC) Module*
*Basierend auf mathematischer Fundierung, NICHT auf KI-Hype*
`;
}

/**
 * Generate compliance section based on risk level
 *
 * @private
 */
function generateComplianceSection(riskLevel) {
  if (riskLevel === "HIGH") {
    return `**Hohe Compliance-Anforderungen:**

- ✅ Datenschutz-Folgenabschätzung (DSFA) gem. Art. 35 DSGVO **PFLICHT**
- ✅ Betriebsrat-Zustimmung nach §87 BetrVG erforderlich
- ✅ Verarbeitungsverzeichnis gem. Art. 30 DSGVO erweitern
- ✅ Auftragsverarbeitungsvertrag (AVV) bei externen Dienstleistern
- ⚠️ **EMPFEHLUNG:** Keine Cloud-Verarbeitung von Personendaten

**Rechtliche Grundlage für Verarbeitung:**
- Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse)
- ggf. Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung)
- Bei Mitarbeiterdaten: §26 BDSG (Beschäftigtendaten)`;
  } else if (riskLevel === "MEDIUM") {
    return `**Mittlere Compliance-Anforderungen:**

- ✅ Datenschutz-Folgenabschätzung (DSFA) empfohlen
- ✅ Betriebsrat informieren nach §80 BetrVG
- ✅ Verarbeitungsverzeichnis gem. Art. 30 DSGVO aktualisieren
- ✅ Auftragsverarbeitungsvertrag (AVV) bei Cloud-Diensten

**Rechtliche Grundlage für Verarbeitung:**
- Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse)
- Art. 28 DSGVO (Auftragsverarbeitung) bei Cloud-Nutzung`;
  } else {
    return `**Standard Compliance-Anforderungen:**

- ✅ Verarbeitungsverzeichnis gem. Art. 30 DSGVO aktualisieren
- ✅ Betriebsrat informieren (optional, aber empfohlen)
- ✅ Standard-Sicherheitsmaßnahmen gem. Art. 32 DSGVO

**Rechtliche Grundlage für Verarbeitung:**
- Art. 6 Abs. 1 lit. f DSGVO (Berechtigtes Interesse)`;
  }
}

/**
 * Generate works council section
 *
 * @private
 */
function generateWorksCouncilSection(riskAssessment) {
  const hasEmployeeData = riskAssessment.factors.some((f) => f.includes("Mitarbeiterdaten"));

  if (hasEmployeeData) {
    return `**Betriebsrat-Mitbestimmung:** JA (§87 Abs. 1 Nr. 6 BetrVG - technische Überwachung)

**Erforderliche Maßnahmen:**
1. Frühzeitige Information des Betriebsrats
2. Gemeinsame Erarbeitung einer Betriebsvereinbarung
3. Klare Regelungen zu:
   - Zweck der Datenverarbeitung
   - Umfang der erfassten Daten
   - Speicherdauer
   - Zugriffsrechte
   - Keine Leistungs-/Verhaltenskontrolle

**Timeline:** +4-8 Wochen für Betriebsvereinbarung einplanen`;
  } else {
    return `**Betriebsrat-Mitbestimmung:** OPTIONAL

**Empfehlung:**
- Betriebsrat trotzdem informieren (§80 BetrVG - Informationsrecht)
- Transparenz schafft Akzeptanz
- Vorbeugt späteren Konflikten`;
  }
}

/**
 * Generate architecture details based on choice
 *
 * @private
 */
function generateArchitectureDetails(architectureChoice, riskLevel) {
  const architectures = {
    "On-Premise / Local LLM": `
**Komponenten:**
- **LLM:** Llama 3.3 70B oder Mistral Large 2 (self-hosted)
- **Infrastruktur:** Eigene GPU-Server (z.B. NVIDIA A100)
- **Orchestration:** LangChain + ChromaDB (Vector Store)
- **Integration:** REST API zu SAP via PI/PO

**Vorteile:**
- ✅ Maximale Datensouveränität
- ✅ Keine Daten verlassen deutsches Rechenzentrum
- ✅ Volle Kontrolle über Modell und Daten

**Nachteile:**
- ❌ Höhere Initialkosten (GPU-Hardware)
- ❌ Eigener Betrieb erforderlich (24/7)
- ❌ Längere Time-to-Market

**Geschätzte Kosten:**
- Hardware: €50.000-80.000 (einmalig)
- Betrieb: €2.000-3.000/Monat`,

    "Azure OpenAI Germany West": `
**Komponenten:**
- **LLM:** GPT-4o via Azure OpenAI Service
- **Region:** Germany West (Frankfurt)
- **Integration:** Azure API Management + Logic Apps
- **Sicherheit:** Private Endpoints, VNet Integration

**Vorteile:**
- ✅ Schneller Start (kein Hardware-Setup)
- ✅ Enterprise-Support von Microsoft
- ✅ DSGVO-konformer AVV verfügbar
- ✅ Datenhaltung in Deutschland

**Nachteile:**
- ❌ Abhängigkeit von Microsoft
- ❌ Laufende Kosten pro Token
- ❌ Weniger Flexibilität

**Geschätzte Kosten:**
- Setup: €10.000-15.000
- Betrieb: €1.000-2.000/Monat (je nach Volumen)`,

    "Hybrid (Azure + On-Premise)": `
**Komponenten:**
- **Sensitive Daten:** Lokales LLM (z.B. Llama 3.3)
- **Standard-Workflows:** Azure OpenAI Germany West
- **Orchestration:** Intelligentes Routing (PII-Detection)

**Vorteile:**
- ✅ Balance zwischen Kosten und Compliance
- ✅ Flexibilität je nach Use Case
- ✅ Skalierbarkeit

**Nachteile:**
- ❌ Komplexere Architektur
- ❌ Zwei Systeme zu betreiben
- ❌ Routing-Logik muss fehlerlos sein

**Geschätzte Kosten:**
- Setup: €40.000-60.000
- Betrieb: €2.500-4.000/Monat`,
  };

  return architectures[architectureChoice] || `Benutzerdefinierte Architektur: ${architectureChoice}`;
}

/**
 * Generate privacy architecture section
 *
 * @private
 */
function generatePrivacyArchitecture(riskLevel) {
  if (riskLevel === "HIGH") {
    return `**Privacy-by-Design Maßnahmen:**

1. **Datensparsamkeit:** Nur notwendige Datenfelder verarbeiten
2. **Pseudonymisierung:** Namen/IDs durch Tokens ersetzen vor LLM-Verarbeitung
3. **Verschlüsselung:** AES-256 für Data-at-Rest, TLS 1.3 für Data-in-Transit
4. **Zugriffskontrolle:** Role-Based Access Control (RBAC)
5. **Audit-Trail:** Vollständiges Logging aller Datenverarbeitungen
6. **Löschkonzept:** Automatische Löschung nach Aufbewahrungsfrist

**Technische Maßnahmen gem. Art. 32 DSGVO:**
- End-to-End Verschlüsselung
- Air-Gap zwischen LLM und Internet (bei On-Premise)
- Regelmäßige Penetrationstests
- Incident Response Plan`;
  } else {
    return `**Standard Privacy-by-Design Maßnahmen:**

1. **Datensparsamkeit:** Nur erforderliche Daten nutzen
2. **Verschlüsselung:** TLS 1.3 für Datenübertragung
3. **Zugriffskontrolle:** Standard RBAC
4. **Logging:** Basis-Audit-Trail
5. **AVV:** Standard-Auftragsverarbeitungsvertrag mit Cloud-Provider

**Technische Maßnahmen gem. Art. 32 DSGVO:**
- Verschlüsselte Übertragung
- Regelmäßige Updates
- Backup-Strategie`;
  }
}

/**
 * Export a summary for quick reference
 *
 * @param {Object} data - Blueprint data
 * @returns {Object} Executive summary
 */
function generateExecutiveSummary(data) {
  const { roi_stats, risk_assessment, architecture_choice } = data;

  return {
    annual_savings: roi_stats.future_state.annual_savings,
    break_even_months: roi_stats.roi_analysis.break_even_months,
    roi_percent: roi_stats.roi_analysis.roi_percent,
    risk_level: risk_assessment.risk_level,
    recommended_architecture: architecture_choice,
    investment_required: roi_stats.roi_analysis.implementation_cost,
  };
}

module.exports = {
  createStrategicBlueprint,
  generateExecutiveSummary,
};
