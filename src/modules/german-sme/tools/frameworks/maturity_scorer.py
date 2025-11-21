"""
Data Maturity Scoring - AI Hierarchy of Needs Implementation
Based on Monica Rogati's "Data Science Hierarchy of Needs"
"""

from typing import Dict, List, Tuple
from enum import Enum


class DataStorage(Enum):
    """Data storage maturity levels"""
    PAPER = "paper"
    EXCEL = "excel"
    ACCESS_DB = "access"
    SQL_DB = "sql"
    DATA_WAREHOUSE = "warehouse"
    DATA_LAKE = "lake"
    MODERN_STACK = "modern"


class DataCleanliness(Enum):
    """Data quality levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MaturityLevel(Enum):
    """AI Hierarchy of Needs Levels"""
    LEVEL_1_COLLECTION = 1  # Instrumentation, Logging, Sensors, External Data
    LEVEL_2_STORAGE = 2  # Reliable Data Flow, Infrastructure, Pipelines, ETL
    LEVEL_3_CLEANING = 3  # Data Cleaning, Anomaly Detection, Prep
    LEVEL_4_ANALYTICS = 4  # Business Intelligence, Metrics, Segments, Aggregates
    LEVEL_5_EXPERIMENTATION = 5  # A/B Testing, Simple ML, Feature Engineering
    LEVEL_6_AI_ML = 6  # Deep Learning, Advanced ML, Real-time Predictions


def assess_hierarchy_level(
    data_storage: str,
    data_volume: int,
    data_cleanliness: str,
    has_data_pipeline: bool = False,
    has_analytics_team: bool = False,
    has_ml_experience: bool = False
) -> Dict:
    """
    Assess organization's position on the AI Hierarchy of Needs.

    This is the BRUTAL HONESTY function. Most German SMEs think they're ready for AI.
    This function tells them they're still figuring out Excel.

    Args:
        data_storage: Where data lives - "paper", "excel", "access", "sql", "warehouse", "lake", "modern"
        data_volume: Number of records (rows) available
        data_cleanliness: Quality level - "low", "medium", "high"
        has_data_pipeline: Do you have automated ETL/data pipelines?
        has_analytics_team: Do you have dedicated data analysts?
        has_ml_experience: Has anyone on the team built ML models before?

    Returns:
        Dictionary with:
        - level: int (1-6)
        - level_name: str
        - status: "NO-GO" | "GO" | "READY"
        - recommendation: str (what to do next)
        - blockers: List[str] (what's preventing next level)
        - estimated_months_to_ml: int (realistic timeline to ML readiness)
    """

    storage = data_storage.lower()
    cleanliness = data_cleanliness.lower()

    # LEVEL 1: COLLECTION - Still gathering data, not ready for anything
    if storage in ["paper", "excel", "access"]:
        return {
            "level": 1,
            "level_name": "Data Collection",
            "status": "NO-GO",
            "recommendation": "**STOP THE AI PROJECT.** You are at the foundation of the pyramid. "
                            "Focus on: (1) Moving to a proper database (SQL), (2) Automating data collection, "
                            "(3) Establishing consistent data formats. AI is 12-24 months away.",
            "blockers": [
                "Data stored in unstructured formats (Paper/Excel)",
                "No centralized data repository",
                "Manual data entry processes",
                "Inconsistent data formats"
            ],
            "estimated_months_to_ml": 24,
            "next_steps": [
                "Implement SQL database (PostgreSQL or SQL Server)",
                "Digitize paper records",
                "Consolidate Excel files into database",
                "Establish data entry standards"
            ],
            "german_context": "Typical for traditional Mittelstand. Start with 'Digitalisierung' before AI."
        }

    # LEVEL 2: STORAGE - Has database, but data flow is manual/unreliable
    if storage == "sql" and not has_data_pipeline:
        return {
            "level": 2,
            "level_name": "Data Storage & Flow",
            "status": "NO-GO",
            "recommendation": "You have a database, but data flow is manual. Build automated pipelines first. "
                            "AI requires reliable, continuous data updates. Focus on ETL automation.",
            "blockers": [
                "Manual data imports/exports",
                "No automated data pipelines",
                "Unreliable data updates",
                "Siloed databases (not integrated)"
            ],
            "estimated_months_to_ml": 18,
            "next_steps": [
                "Implement automated ETL pipelines",
                "Integrate data sources (ERP, MES, sensors)",
                "Establish data quality monitoring",
                "Set up regular data backups"
            ],
            "german_context": "Common with SAP R/3 users - data exists but trapped in silos."
        }

    # LEVEL 3: CLEANING - Data exists and flows, but quality is poor
    if storage == "sql" and has_data_pipeline and cleanliness == "low":
        return {
            "level": 3,
            "level_name": "Data Cleaning & Preparation",
            "status": "NO-GO",
            "recommendation": "Data infrastructure exists, but quality is too low for ML. "
                            "Invest in data cleaning before AI. Garbage in = Garbage out.",
            "blockers": [
                "High error rates in data",
                "Missing values (>20% of records)",
                "Inconsistent formats",
                "No data validation rules"
            ],
            "estimated_months_to_ml": 12,
            "next_steps": [
                "Implement data validation rules",
                "Clean historical data",
                "Establish data quality metrics",
                "Train staff on data entry standards"
            ],
            "german_context": "Focus on 'Datenqualität' - quality over quantity for Mittelstand."
        }

    # LEVEL 4: ANALYTICS - Ready for BI and basic analytics
    if storage in ["sql", "warehouse"] and has_data_pipeline and cleanliness in ["medium", "high"] and not has_analytics_team:
        return {
            "level": 4,
            "level_name": "Analytics & Business Intelligence",
            "status": "GO",
            "recommendation": "You're ready for analytics and BI, but NOT deep learning yet. "
                            "Start with dashboards, reports, and simple statistical analysis. "
                            "Build analytics capability before jumping to ML.",
            "blockers": [
                "No analytics team or expertise",
                "Limited statistical knowledge",
                "No experience with ML projects"
            ],
            "estimated_months_to_ml": 9,
            "next_steps": [
                "Implement BI dashboards (Power BI, Tableau)",
                "Train team on basic statistics",
                "Hire or train a data analyst",
                "Define key business metrics (KPIs)"
            ],
            "german_context": "Perfect stage for 'Controlling' and 'Kennzahlen' - familiar to German managers."
        }

    # LEVEL 5: EXPERIMENTATION - Ready for simple ML and A/B testing
    if storage in ["sql", "warehouse"] and has_data_pipeline and cleanliness == "high" and has_analytics_team and not has_ml_experience:
        return {
            "level": 5,
            "level_name": "Experimentation & Simple ML",
            "status": "GO",
            "recommendation": "You're ready for pilot ML projects! Start with simple models: "
                            "linear regression, decision trees, clustering. Avoid deep learning for now.",
            "blockers": [
                "No ML experience on team",
                "Limited Python/R skills",
                "No model deployment infrastructure"
            ],
            "estimated_months_to_ml": 6,
            "next_steps": [
                "Run ML pilot project (predictive maintenance, demand forecasting)",
                "Train team on Python/scikit-learn basics",
                "Establish model validation process",
                "Build simple ML pipeline (training → validation → deployment)"
            ],
            "german_context": "Ideal for Mittelstand - proven ROI with explainable models."
        }

    # LEVEL 6: ADVANCED AI/ML - Ready for production ML and deep learning
    if (storage in ["warehouse", "lake", "modern"] and
        has_data_pipeline and
        cleanliness == "high" and
        has_analytics_team and
        has_ml_experience and
        data_volume > 10000):
        return {
            "level": 6,
            "level_name": "Advanced AI & Deep Learning",
            "status": "READY",
            "recommendation": "Congratulations! You're in the top 5% of German SMEs. "
                            "You can pursue advanced ML: deep learning, NLP, computer vision. "
                            "Focus on production MLOps and scaling.",
            "blockers": [],
            "estimated_months_to_ml": 0,
            "next_steps": [
                "Implement MLOps platform (MLflow, Kubeflow)",
                "Scale ML infrastructure (GPU compute)",
                "Build model monitoring and retraining pipelines",
                "Explore advanced techniques (neural networks, transformers)"
            ],
            "german_context": "You're ready for 'Industrie 4.0' - but still follow German compliance rules!"
        }

    # DEFAULT: Need more information
    return {
        "level": 3,
        "level_name": "Assessment Incomplete",
        "status": "UNCLEAR",
        "recommendation": "Not enough information to assess maturity. Answer all questions honestly.",
        "blockers": ["Incomplete assessment"],
        "estimated_months_to_ml": 12,
        "next_steps": ["Complete the full maturity assessment"],
        "german_context": "Provide full details of your data infrastructure."
    }


def calculate_readiness_score(assessment: Dict) -> int:
    """
    Convert maturity assessment to a simple 0-100 readiness score.

    Returns:
        Score from 0-100 where:
        - 0-40: Not ready (Stop)
        - 41-70: Prepare (Fix blockers)
        - 71-100: Ready (Go ahead)
    """
    level = assessment["level"]
    blockers_count = len(assessment["blockers"])

    # Base score from level (each level = 16.67 points)
    base_score = (level - 1) * 20

    # Deduct points for blockers
    blocker_penalty = blockers_count * 5

    final_score = max(0, min(100, base_score - blocker_penalty))

    return final_score


def generate_maturity_report(assessment: Dict) -> str:
    """Generate a formatted Markdown report of the maturity assessment."""

    score = calculate_readiness_score(assessment)
    level = assessment["level"]
    status_emoji = {"NO-GO": "🛑", "GO": "⚠️", "READY": "✅", "UNCLEAR": "❓"}

    report = f"""# AI Readiness Maturity Assessment

## Overall Status: {status_emoji.get(assessment['status'], '❓')} {assessment['status']}

**Maturity Level:** {level}/6 - {assessment['level_name']}
**Readiness Score:** {score}/100
**Estimated Time to ML Production:** {assessment['estimated_months_to_ml']} months

---

## Recommendation

{assessment['recommendation']}

---

## Current Blockers

"""

    if assessment["blockers"]:
        for blocker in assessment["blockers"]:
            report += f"- ❌ {blocker}\n"
    else:
        report += "- ✅ No major blockers identified!\n"

    report += f"""
---

## Next Steps

"""

    for i, step in enumerate(assessment["next_steps"], 1):
        report += f"{i}. {step}\n"

    report += f"""
---

## German Context Note

{assessment['german_context']}

---

## The Hierarchy of Needs (Monica Rogati Framework)

```
        /\\
       /AI\\              ← Level 6: Deep Learning, Advanced ML
      /____\\
     /Simple\\            ← Level 5: A/B Testing, Basic ML
    /   ML   \\
   /__________\\
  /  Learning  \\         ← Level 4: Analytics, BI, Metrics
 / Aggregation \\
/_______________\\
/   Cleaning &  \\        ← Level 3: Data Quality, Validation  ← YOU ARE HERE (Level {level})
/   Exploration \\
/_________________\\
/  Reliable Data  \\      ← Level 2: Pipelines, ETL, Flow
/      Flow       \\
/___________________\\
/    Collection &   \\    ← Level 1: Instrumentation, Logging
/     Monitoring     \\
/______________________\\
```

**Key Insight:** You cannot skip levels. Each level builds on the previous one.
If your foundation is shaky, your AI will fail.

"""

    return report


# Example usage and test cases
if __name__ == "__main__":
    # Test Case 1: Traditional Mittelstand with Excel
    print("="*80)
    print("TEST CASE 1: Traditional Mittelstand (Excel-based)")
    print("="*80)
    assessment1 = assess_hierarchy_level(
        data_storage="excel",
        data_volume=5000,
        data_cleanliness="low",
        has_data_pipeline=False,
        has_analytics_team=False,
        has_ml_experience=False
    )
    print(generate_maturity_report(assessment1))

    # Test Case 2: Mid-maturity company with SQL but poor quality
    print("\n" + "="*80)
    print("TEST CASE 2: Mid-Maturity Company (SQL + Poor Quality)")
    print("="*80)
    assessment2 = assess_hierarchy_level(
        data_storage="sql",
        data_volume=50000,
        data_cleanliness="low",
        has_data_pipeline=True,
        has_analytics_team=False,
        has_ml_experience=False
    )
    print(generate_maturity_report(assessment2))

    # Test Case 3: ML-Ready organization
    print("\n" + "="*80)
    print("TEST CASE 3: ML-Ready Organization")
    print("="*80)
    assessment3 = assess_hierarchy_level(
        data_storage="warehouse",
        data_volume=500000,
        data_cleanliness="high",
        has_data_pipeline=True,
        has_analytics_team=True,
        has_ml_experience=True
    )
    print(generate_maturity_report(assessment3))
