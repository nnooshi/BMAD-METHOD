"""
DACH Compliance Scoring - 4-P Readiness Model
The "German Context" framework for AI projects in DACH region (Germany, Austria, Switzerland)

The 4 P's:
1. Privacy (DSGVO/GDPR)
2. Platform (Legacy IT)
3. People (Works Council / Betriebsrat)
4. Proprietary (IP Protection)
"""

from typing import Dict, List, Tuple
from enum import Enum


class RiskLevel(Enum):
    """Risk assessment levels"""
    GREEN = "green"  # 80-100: Low risk, proceed
    YELLOW = "yellow"  # 50-79: Medium risk, mitigation needed
    RED = "red"  # 0-49: High risk, major changes required


class PlatformType(Enum):
    """Common platform types in German SMEs"""
    SAP_R3 = "sap_r3"  # Legacy SAP
    SAP_S4 = "sap_s4"  # Modern SAP
    SAGE = "sage"
    DATEV = "datev"  # Accounting software
    CUSTOM = "custom"  # Custom built
    MODERN = "modern"  # Cloud-native
    NONE = "none"


def score_4p_readiness(
    privacy_pii: bool,
    platform_legacy: str,
    people_works_council: bool,
    proprietary_ip: bool,
    data_location: str = "germany",
    has_dpo: bool = False,
    has_legal_review: bool = False
) -> Dict:
    """
    Score AI project readiness based on the 4-P German Context Model.

    This function applies the brutal reality check for German/DACH AI projects.
    International frameworks ignore German peculiarities. This doesn't.

    Args:
        privacy_pii: Does the project involve "Personenbezogene Daten" (PII)?
        platform_legacy: Legacy platform type - "sap_r3", "sage", "datev", "custom", "modern", "none"
        people_works_council: Does the Betriebsrat (Works Council) exist and need approval?
        proprietary_ip: Does this involve company IP / trade secrets?
        data_location: Where will data be stored? "germany", "eu", "us", "cloud"
        has_dpo: Do you have a Data Protection Officer (Datenschutzbeauftragter)?
        has_legal_review: Has legal department reviewed the project?

    Returns:
        Dictionary with:
        - score: int (0-100)
        - risk_level: "green" | "yellow" | "red"
        - privacy_risk: Dict
        - platform_risk: Dict
        - people_risk: Dict
        - proprietary_risk: Dict
        - recommendations: List[str]
        - blockers: List[str]
        - estimated_delay_weeks: int
    """

    score = 100  # Start optimistic, deduct points for each risk
    blockers = []
    recommendations = []
    estimated_delay_weeks = 0

    # ====================
    # 1. PRIVACY (DSGVO/GDPR)
    # ====================
    privacy_score = 100
    privacy_blockers = []
    privacy_recommendations = []

    if privacy_pii:
        privacy_score -= 30
        estimated_delay_weeks += 8
        privacy_recommendations.append("Conduct DSGVO/GDPR compliance assessment")
        privacy_recommendations.append("Document legal basis for processing (Art. 6 DSGVO)")

        if not has_dpo:
            privacy_score -= 15
            privacy_blockers.append("No Data Protection Officer appointed (required by DSGVO Art. 37)")
            privacy_recommendations.append("Appoint internal or external Datenschutzbeauftragter")

        if not has_legal_review:
            privacy_score -= 10
            privacy_blockers.append("No legal review completed")

        if data_location == "us":
            privacy_score -= 25
            privacy_blockers.append("US data storage - violates Schrems II ruling")
            privacy_recommendations.append("Move data to EU/Germany or implement Standard Contractual Clauses")
            estimated_delay_weeks += 4

        if data_location == "cloud" and not has_legal_review:
            privacy_score -= 15
            privacy_blockers.append("Cloud storage without legal review")
            privacy_recommendations.append("Verify cloud provider DSGVO compliance (e.g., AWS Frankfurt, Azure Germany)")

    privacy_risk = {
        "score": max(0, privacy_score),
        "blockers": privacy_blockers,
        "recommendations": privacy_recommendations
    }

    # ====================
    # 2. PLATFORM (Legacy IT)
    # ====================
    platform_score = 100
    platform_blockers = []
    platform_recommendations = []

    platform = platform_legacy.lower()

    if platform == "sap_r3":
        platform_score -= 20
        estimated_delay_weeks += 6
        platform_blockers.append("SAP R/3 integration is notoriously difficult")
        platform_recommendations.append("Use SAP PI/PO or RFC connections")
        platform_recommendations.append("Consider data replication instead of real-time integration")
        platform_recommendations.append("Budget 50-100 developer-hours for integration")

    elif platform == "datev":
        platform_score -= 15
        estimated_delay_weeks += 4
        platform_blockers.append("DATEV systems have limited API access")
        platform_recommendations.append("Export data to intermediate database")
        platform_recommendations.append("Work with DATEV-certified partner")

    elif platform == "custom":
        platform_score -= 25
        estimated_delay_weeks += 8
        platform_blockers.append("Custom legacy system - unknown integration complexity")
        platform_recommendations.append("Conduct technical architecture review")
        platform_recommendations.append("Identify or build APIs for data access")
        platform_recommendations.append("Plan for significant custom integration work")

    elif platform == "sage":
        platform_score -= 10
        platform_recommendations.append("Use Sage API v3 for integration")

    elif platform == "modern":
        platform_score -= 0
        # No penalties for modern platforms

    platform_risk = {
        "score": max(0, platform_score),
        "blockers": platform_blockers,
        "recommendations": platform_recommendations
    }

    # ====================
    # 3. PEOPLE (Works Council / Betriebsrat)
    # ====================
    people_score = 100
    people_blockers = []
    people_recommendations = []

    if people_works_council:
        people_score -= 20
        estimated_delay_weeks += 12  # This is the BIG delay in Germany
        people_blockers.append("Betriebsrat (Works Council) approval required - expect 3-6 month delay")
        people_recommendations.append("Present AI project to Betriebsrat early (transparency builds trust)")
        people_recommendations.append("Emphasize: AI assists workers, does not replace them")
        people_recommendations.append("Offer Betriebsrat members AI training/education")
        people_recommendations.append("Document that no employee monitoring/surveillance is involved")
        people_recommendations.append("Consider Betriebsvereinbarung (works agreement) for AI use")

        # Extra penalty if PII is involved AND works council exists
        if privacy_pii:
            people_score -= 15
            people_blockers.append("Betriebsrat + PII = Double scrutiny (expect longer delays)")
            estimated_delay_weeks += 4

    people_risk = {
        "score": max(0, people_score),
        "blockers": people_blockers,
        "recommendations": people_recommendations
    }

    # ====================
    # 4. PROPRIETARY (IP Protection)
    # ====================
    proprietary_score = 100
    proprietary_blockers = []
    proprietary_recommendations = []

    if proprietary_ip:
        proprietary_score -= 15
        proprietary_recommendations.append("Avoid cloud AI services (AWS, Azure ML) - they may train on your data")
        proprietary_recommendations.append("Use on-premise or dedicated instances")
        proprietary_recommendations.append("Review vendor contracts for IP ownership clauses")

        if data_location not in ["germany", "eu"]:
            proprietary_score -= 20
            proprietary_blockers.append("IP/trade secrets stored outside Germany - risk of foreign access")
            proprietary_recommendations.append("Move sensitive data to German data centers")
            estimated_delay_weeks += 4

    proprietary_risk = {
        "score": max(0, proprietary_score),
        "blockers": proprietary_blockers,
        "recommendations": proprietary_recommendations
    }

    # ====================
    # FINAL SCORING
    # ====================
    # Weighted average of all 4 P's
    final_score = int(
        (privacy_score * 0.35) +  # Privacy is most critical
        (platform_score * 0.25) +
        (people_score * 0.30) +  # People risk causes biggest delays
        (proprietary_score * 0.10)
    )

    # Determine risk level
    if final_score >= 80:
        risk_level = RiskLevel.GREEN
    elif final_score >= 50:
        risk_level = RiskLevel.YELLOW
    else:
        risk_level = RiskLevel.RED

    # Aggregate blockers and recommendations
    all_blockers = (privacy_blockers + platform_blockers +
                    people_blockers + proprietary_blockers)
    all_recommendations = (privacy_recommendations + platform_recommendations +
                          people_recommendations + proprietary_recommendations)

    return {
        "score": final_score,
        "risk_level": risk_level.value,
        "privacy_risk": privacy_risk,
        "platform_risk": platform_risk,
        "people_risk": people_risk,
        "proprietary_risk": proprietary_risk,
        "blockers": all_blockers,
        "recommendations": all_recommendations,
        "estimated_delay_weeks": estimated_delay_weeks,
        "status": _determine_status(final_score, all_blockers)
    }


def _determine_status(score: int, blockers: List[str]) -> str:
    """Determine project status based on score and blockers."""
    if score >= 80 and len(blockers) == 0:
        return "GO"
    elif score >= 50:
        return "PROCEED WITH CAUTION"
    else:
        return "HIGH RISK - MITIGATION REQUIRED"


def generate_4p_report(assessment: Dict) -> str:
    """Generate a formatted Markdown report of the 4-P assessment."""

    score = assessment["score"]
    risk_level = assessment["risk_level"]
    status = assessment["status"]

    risk_emoji = {
        "green": "✅",
        "yellow": "⚠️",
        "red": "🛑"
    }

    report = f"""# 4-P Readiness Assessment (German Context)

## Overall Status: {risk_emoji.get(risk_level, '❓')} {status}

**Compliance Score:** {score}/100
**Risk Level:** {risk_level.upper()}
**Estimated Delay:** {assessment['estimated_delay_weeks']} weeks

---

## The 4 P's of German AI Projects

### 1. 🔒 PRIVACY (DSGVO/GDPR) - Score: {assessment['privacy_risk']['score']}/100

"""

    if assessment['privacy_risk']['blockers']:
        report += "**Blockers:**\n"
        for blocker in assessment['privacy_risk']['blockers']:
            report += f"- ❌ {blocker}\n"
    else:
        report += "✅ No privacy blockers\n"

    if assessment['privacy_risk']['recommendations']:
        report += "\n**Recommendations:**\n"
        for rec in assessment['privacy_risk']['recommendations']:
            report += f"- {rec}\n"

    report += f"""
---

### 2. 🏗️ PLATFORM (Legacy IT Integration) - Score: {assessment['platform_risk']['score']}/100

"""

    if assessment['platform_risk']['blockers']:
        report += "**Blockers:**\n"
        for blocker in assessment['platform_risk']['blockers']:
            report += f"- ❌ {blocker}\n"
    else:
        report += "✅ No platform blockers\n"

    if assessment['platform_risk']['recommendations']:
        report += "\n**Recommendations:**\n"
        for rec in assessment['platform_risk']['recommendations']:
            report += f"- {rec}\n"

    report += f"""
---

### 3. 👥 PEOPLE (Betriebsrat / Works Council) - Score: {assessment['people_risk']['score']}/100

"""

    if assessment['people_risk']['blockers']:
        report += "**Blockers:**\n"
        for blocker in assessment['people_risk']['blockers']:
            report += f"- ❌ {blocker}\n"
    else:
        report += "✅ No people/works council blockers\n"

    if assessment['people_risk']['recommendations']:
        report += "\n**Recommendations:**\n"
        for rec in assessment['people_risk']['recommendations']:
            report += f"- {rec}\n"

    report += f"""
---

### 4. 🛡️ PROPRIETARY (IP & Trade Secrets) - Score: {assessment['proprietary_risk']['score']}/100

"""

    if assessment['proprietary_risk']['blockers']:
        report += "**Blockers:**\n"
        for blocker in assessment['proprietary_risk']['blockers']:
            report += f"- ❌ {blocker}\n"
    else:
        report += "✅ No IP/proprietary blockers\n"

    if assessment['proprietary_risk']['recommendations']:
        report += "\n**Recommendations:**\n"
        for rec in assessment['proprietary_risk']['recommendations']:
            report += f"- {rec}\n"

    report += """
---

## Why German AI Projects Are Different

1. **DSGVO is STRICT**: Germany enforces GDPR more strictly than most EU countries
   - Fines can reach €20M or 4% of global revenue
   - German DPAs (Datenschutzbehörden) are aggressive

2. **Betriebsrat Has POWER**: Works councils can delay or block projects
   - Co-determination rights (Mitbestimmung) are legally protected
   - "AI = Job Loss" is the default assumption - you must prove otherwise

3. **Legacy IT is EVERYWHERE**: German Mittelstand runs on SAP R/3, DATEV, custom systems
   - Modern APIs are rare
   - Integration costs are 3-5x higher than US

4. **IP Paranoia is JUSTIFIED**: German manufacturing IP is worth billions
   - Competitors (especially from Asia) actively seek trade secrets
   - Cloud AI services are viewed with suspicion

---

## Risk Mitigation Priority

"""

    if score < 50:
        report += """
🛑 **RED ZONE**: Address ALL blockers before proceeding
- Conduct formal risk assessment
- Get executive-level approval for budget and timeline increases
- Consider scaling back project scope
"""
    elif score < 80:
        report += """
⚠️ **YELLOW ZONE**: Mitigate risks before full deployment
- Create mitigation plan for each blocker
- Get legal and Betriebsrat buy-in early
- Budget extra time and money (2-3x initial estimate)
"""
    else:
        report += """
✅ **GREEN ZONE**: Low risk, but stay vigilant
- Document compliance measures
- Maintain regular communication with stakeholders
- Monitor regulatory changes
"""

    report += """
---

## Key Insight: "German Time" for AI Projects

International timeline × 1.5 to 2.0 = German timeline

**Why?**
- Legal review: +4-8 weeks
- Betriebsrat negotiation: +12-24 weeks
- DSGVO compliance: +4-8 weeks
- Legacy IT integration: +6-12 weeks

**Plan accordingly.** Under-promising and over-delivering is the German way.

"""

    return report


# Example usage and test cases
if __name__ == "__main__":
    # Test Case 1: High-risk project (all flags triggered)
    print("="*80)
    print("TEST CASE 1: High-Risk German SME Project")
    print("="*80)
    assessment1 = score_4p_readiness(
        privacy_pii=True,
        platform_legacy="sap_r3",
        people_works_council=True,
        proprietary_ip=True,
        data_location="us",
        has_dpo=False,
        has_legal_review=False
    )
    print(generate_4p_report(assessment1))

    # Test Case 2: Medium-risk project
    print("\n" + "="*80)
    print("TEST CASE 2: Medium-Risk Project (Some Flags)")
    print("="*80)
    assessment2 = score_4p_readiness(
        privacy_pii=False,
        platform_legacy="modern",
        people_works_council=True,
        proprietary_ip=True,
        data_location="germany",
        has_dpo=True,
        has_legal_review=True
    )
    print(generate_4p_report(assessment2))

    # Test Case 3: Low-risk project
    print("\n" + "="*80)
    print("TEST CASE 3: Low-Risk Project (Modern Setup)")
    print("="*80)
    assessment3 = score_4p_readiness(
        privacy_pii=False,
        platform_legacy="modern",
        people_works_council=False,
        proprietary_ip=False,
        data_location="germany",
        has_dpo=True,
        has_legal_review=True
    )
    print(generate_4p_report(assessment3))
