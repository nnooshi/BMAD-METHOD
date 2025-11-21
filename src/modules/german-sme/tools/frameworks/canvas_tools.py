"""
AI Canvas Tools - Prediction Machines Framework Implementation
Based on "Prediction Machines" by Agrawal, Gans, and Goldfarb
"""

from typing import Dict, Optional


def structure_ai_canvas(
    prediction_goal: str,
    judgment_owner: str,
    action_trigger: str,
    outcome_value: str,
    data_source: Optional[str] = None,
    prediction_frequency: Optional[str] = None
) -> str:
    """
    Structure an AI Canvas based on the Prediction Machines framework.

    The AI Canvas forces clarity on what AI actually does: reduce the cost of prediction.
    This tool strips away the magic and forces concrete answers.

    Args:
        prediction_goal: What specific number/prediction is missing? (e.g., "Probability that machine X will fail in next 7 days")
        judgment_owner: Who decides what to do with that prediction? (e.g., "Maintenance Manager")
        action_trigger: What physical action happens based on the prediction? (e.g., "Schedule preventive maintenance")
        outcome_value: How does this save money or create value? (e.g., "Avoid €50K emergency downtime")
        data_source: Where does the training data come from? (optional)
        prediction_frequency: How often is the prediction needed? (optional)

    Returns:
        A formatted Markdown string representing the AI Canvas
    """

    canvas = f"""# AI Canvas - Prediction Machines Framework

## 1. PREDICTION (The Core AI Function)
**What specific number or outcome are we predicting?**
{prediction_goal}

> ⚠️ **The Clarity Test:** Can you express this as a number, probability, or classification?
> If not, you don't have an AI problem yet - you have a strategy problem.

## 2. JUDGMENT (The Human Decision)
**Who owns the decision based on this prediction?**
{judgment_owner}

> 🎯 **Key Insight:** AI reduces the cost of prediction, but humans still own judgment.
> The prediction is worthless if the decision-maker doesn't trust or use it.

## 3. ACTION (The Physical Consequence)
**What specific action is triggered by this decision?**
{action_trigger}

> 🔧 **Reality Check:** If no action changes, the AI has zero value.
> This must be a concrete, measurable change in operations.

## 4. OUTCOME (The Business Value)
**How does this action create measurable value?**
{outcome_value}

> 💰 **ROI Foundation:** This is where we justify the investment.
> If you can't quantify the outcome, stop the project now.

"""

    # Add optional sections if provided
    if data_source:
        canvas += f"""## 5. DATA SOURCE (The Training Foundation)
**Where does the prediction model get its training data?**
{data_source}

"""

    if prediction_frequency:
        canvas += f"""## 6. PREDICTION FREQUENCY
**How often must this prediction be made?**
{prediction_frequency}

"""

    # Add framework principles
    canvas += """---

## Framework Principles (Prediction Machines)

1. **AI = Prediction, not Magic**
   - Every AI application reduces to: Input → Prediction → Decision → Action

2. **Judgment ≠ Prediction**
   - Prediction: "Machine X has 85% failure probability"
   - Judgment: "Should we shut it down?" (Risk tolerance, cost, alternatives)

3. **Value = (Prediction Quality) × (Decision Impact) × (Action Frequency)**
   - A perfect prediction that doesn't change behavior is worthless
   - A frequent bad decision made 1% better can be worth millions

4. **The Unbundling Test**
   - Can you separate the prediction task from the decision task?
   - If not, you're trying to automate judgment (much harder!)

---

## Next Steps for Validation

- [ ] Verify the prediction goal is specific and measurable
- [ ] Confirm the judgment owner has authority and capacity
- [ ] Document the current decision-making process (the baseline)
- [ ] Calculate the cost of wrong predictions (false positives and false negatives)
- [ ] Estimate prediction volume (predictions per day/week/month)

"""

    return canvas


def validate_canvas_completeness(canvas_dict: Dict) -> Dict[str, any]:
    """
    Validate that an AI Canvas has all required components.

    Args:
        canvas_dict: Dictionary with keys: prediction_goal, judgment_owner, action_trigger, outcome_value

    Returns:
        Dict with validation results: {"valid": bool, "missing_fields": List[str], "warnings": List[str]}
    """
    required_fields = ["prediction_goal", "judgment_owner", "action_trigger", "outcome_value"]
    missing_fields = [field for field in required_fields if not canvas_dict.get(field)]

    warnings = []

    # Check if prediction goal is specific enough
    if canvas_dict.get("prediction_goal"):
        pred = canvas_dict["prediction_goal"].lower()
        vague_terms = ["improve", "optimize", "better", "increase", "reduce"]
        if any(term in pred for term in vague_terms) and not any(char.isdigit() for char in pred):
            warnings.append("Prediction goal seems vague - should include specific metrics or numbers")

    # Check if outcome has monetary value
    if canvas_dict.get("outcome_value"):
        outcome = canvas_dict["outcome_value"]
        if not any(symbol in outcome for symbol in ["€", "$", "£", "CHF"]) and not any(word in outcome.lower() for word in ["cost", "save", "revenue", "profit"]):
            warnings.append("Outcome value should include monetary impact for ROI calculation")

    return {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "warnings": warnings
    }


# Example usage and test cases
if __name__ == "__main__":
    # Example: Predictive Maintenance for German Mittelstand manufacturer
    example_canvas = structure_ai_canvas(
        prediction_goal="Probability (0-100%) that CNC machine will fail within next 7 days",
        judgment_owner="Werksleiter (Plant Manager) - Hans Schmidt",
        action_trigger="Schedule preventive maintenance during planned downtime window",
        outcome_value="Avoid €50,000 emergency downtime cost + €15,000 rush spare parts",
        data_source="Machine sensor logs (vibration, temperature, runtime) from last 3 years",
        prediction_frequency="Daily prediction for each of 12 critical machines"
    )

    print(example_canvas)
    print("\n" + "="*80 + "\n")

    # Validation example
    test_canvas = {
        "prediction_goal": "Predict machine failures",
        "judgment_owner": "Manager",
        "action_trigger": "Fix the machine",
        "outcome_value": "Reduce downtime"
    }

    validation_result = validate_canvas_completeness(test_canvas)
    print("Validation Result:")
    print(f"Valid: {validation_result['valid']}")
    print(f"Warnings: {validation_result['warnings']}")
