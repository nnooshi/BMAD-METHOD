"""
Position Sizer Tool

Calculates appropriate position allocation based on account size, risk bucket,
and conviction level. Implements position sizing rules for systematic trading.
"""

from typing import Literal, Optional
from enum import Enum


class RiskBucket(Enum):
    """Risk bucket classifications for position sizing."""
    CORE = "Core"
    SPECULATIVE = "Speculative"


# Position size caps by bucket (as percentage of account)
BUCKET_CAPS = {
    RiskBucket.CORE: 0.10,        # 10% max for Core positions
    RiskBucket.SPECULATIVE: 0.02  # 2% max for Speculative positions
}

# Conviction scale bounds
MIN_CONVICTION = 1
MAX_CONVICTION = 10


def get_allocation(
    account_size: float,
    bucket: str,
    conviction: float,
    risk_pct: Optional[float] = None
) -> dict:
    """
    Calculate position allocation based on account size, risk bucket, and conviction.

    Position sizing logic:
    1. Determine base allocation cap based on risk bucket:
       - Core: Maximum 10% of account
       - Speculative: Maximum 2% of account
    2. Apply conviction multiplier (1-10 scale) to scale within the cap
    3. Optional: Apply additional risk percentage constraint

    Args:
        account_size: Total account value in dollars
        bucket: Risk bucket classification ("Core" or "Speculative")
        conviction: Conviction level from 1 (lowest) to 10 (highest)
        risk_pct: Optional additional risk percentage cap (0-1)

    Returns:
        Dictionary containing:
        - allocation_dollars: Position size in dollars
        - allocation_pct: Position size as percentage of account
        - max_cap_dollars: Maximum allowed position size
        - max_cap_pct: Maximum allowed position percentage
        - conviction_multiplier: Applied conviction multiplier (0-1)
        - bucket: Risk bucket used
        - warnings: List of any warnings or adjustments made

    Raises:
        ValueError: If inputs are invalid (negative account, invalid bucket, etc.)

    Example:
        >>> result = get_allocation(100000, "Core", 8)
        >>> print(f"Allocate ${result['allocation_dollars']:,.2f}")
        Allocate $8,000.00
    """
    # Validate account size
    if account_size <= 0:
        raise ValueError(
            f"Account size must be positive. Got: ${account_size:,.2f}"
        )

    # Validate and normalize bucket
    bucket = bucket.strip()
    try:
        if bucket.lower() == "core":
            risk_bucket = RiskBucket.CORE
        elif bucket.lower() == "speculative":
            risk_bucket = RiskBucket.SPECULATIVE
        else:
            raise ValueError(
                f"Invalid bucket '{bucket}'. Must be 'Core' or 'Speculative'"
            )
    except AttributeError:
        raise ValueError(f"Bucket must be a string. Got: {type(bucket)}")

    # Validate conviction
    if not isinstance(conviction, (int, float)):
        raise ValueError(
            f"Conviction must be a number. Got: {type(conviction)}"
        )

    if not (MIN_CONVICTION <= conviction <= MAX_CONVICTION):
        raise ValueError(
            f"Conviction must be between {MIN_CONVICTION} and {MAX_CONVICTION}. "
            f"Got: {conviction}"
        )

    # Validate optional risk percentage
    if risk_pct is not None:
        if not isinstance(risk_pct, (int, float)):
            raise ValueError(
                f"risk_pct must be a number. Got: {type(risk_pct)}"
            )
        if not (0 < risk_pct <= 1):
            raise ValueError(
                f"risk_pct must be between 0 and 1. Got: {risk_pct}"
            )

    warnings = []

    # Get base cap for the bucket
    base_cap_pct = BUCKET_CAPS[risk_bucket]
    base_cap_dollars = account_size * base_cap_pct

    # Calculate conviction multiplier (normalize to 0-1 scale)
    # Full conviction (10) = 100% of cap, minimum conviction (1) = 10% of cap
    conviction_multiplier = conviction / MAX_CONVICTION

    # Calculate initial allocation
    allocation_pct = base_cap_pct * conviction_multiplier
    allocation_dollars = account_size * allocation_pct

    # Apply additional risk percentage constraint if provided
    max_cap_pct = base_cap_pct
    max_cap_dollars = base_cap_dollars

    if risk_pct is not None:
        risk_cap_dollars = account_size * risk_pct
        if risk_cap_dollars < allocation_dollars:
            warnings.append(
                f"Allocation reduced from ${allocation_dollars:,.2f} to "
                f"${risk_cap_dollars:,.2f} due to risk_pct constraint"
            )
            allocation_dollars = risk_cap_dollars
            allocation_pct = risk_pct

        # Update max cap if risk_pct is more restrictive
        if risk_pct < max_cap_pct:
            max_cap_pct = risk_pct
            max_cap_dollars = risk_cap_dollars

    # Ensure we don't exceed the bucket cap (defensive check)
    if allocation_dollars > base_cap_dollars:
        warnings.append(
            f"Allocation capped at bucket maximum: ${base_cap_dollars:,.2f}"
        )
        allocation_dollars = base_cap_dollars
        allocation_pct = base_cap_pct

    # Add informational message for low conviction
    if conviction <= 3:
        warnings.append(
            f"Low conviction ({conviction}/10) - consider reducing position size"
        )

    return {
        'allocation_dollars': round(allocation_dollars, 2),
        'allocation_pct': round(allocation_pct, 4),
        'max_cap_dollars': round(max_cap_dollars, 2),
        'max_cap_pct': round(max_cap_pct, 4),
        'conviction_multiplier': round(conviction_multiplier, 2),
        'bucket': risk_bucket.value,
        'conviction': conviction,
        'account_size': account_size,
        'warnings': warnings
    }


def get_max_position_size(account_size: float, bucket: str) -> dict:
    """
    Get maximum position size for a given bucket regardless of conviction.

    Args:
        account_size: Total account value in dollars
        bucket: Risk bucket classification ("Core" or "Speculative")

    Returns:
        Dictionary with max_dollars and max_pct

    Example:
        >>> max_pos = get_max_position_size(100000, "Core")
        >>> print(f"Max Core position: ${max_pos['max_dollars']:,.2f}")
    """
    # Reuse validation from get_allocation
    result = get_allocation(account_size, bucket, MAX_CONVICTION)

    return {
        'max_dollars': result['max_cap_dollars'],
        'max_pct': result['max_cap_pct'],
        'bucket': result['bucket']
    }


if __name__ == "__main__":
    # Example usage and testing
    import sys

    print("Position Sizer Test")
    print("=" * 70)

    account = 100000  # $100,000 account

    # Test scenarios
    test_cases = [
        {"bucket": "Core", "conviction": 10, "desc": "Core - Max Conviction"},
        {"bucket": "Core", "conviction": 5, "desc": "Core - Medium Conviction"},
        {"bucket": "Core", "conviction": 1, "desc": "Core - Low Conviction"},
        {"bucket": "Speculative", "conviction": 10, "desc": "Spec - Max Conviction"},
        {"bucket": "Speculative", "conviction": 5, "desc": "Spec - Medium Conviction"},
        {"bucket": "Speculative", "conviction": 2, "desc": "Spec - Low Conviction"},
    ]

    print(f"\nAccount Size: ${account:,}\n")

    for test in test_cases:
        result = get_allocation(account, test["bucket"], test["conviction"])
        print(f"{test['desc']}:")
        print(f"  Allocation: ${result['allocation_dollars']:,.2f} "
              f"({result['allocation_pct']:.1%})")
        print(f"  Max Cap: ${result['max_cap_dollars']:,.2f} "
              f"({result['max_cap_pct']:.1%})")
        print(f"  Conviction Multiplier: {result['conviction_multiplier']:.1%}")
        if result['warnings']:
            print(f"  Warnings: {result['warnings']}")
        print()

    # Test with risk constraint
    print("\nTest with risk_pct constraint (1.5%):")
    result = get_allocation(account, "Core", 8, risk_pct=0.015)
    print(f"  Allocation: ${result['allocation_dollars']:,.2f} "
          f"({result['allocation_pct']:.1%})")
    if result['warnings']:
        print(f"  Warnings: {', '.join(result['warnings'])}")

    # Test max position sizes
    print("\n" + "=" * 70)
    print("Maximum Position Sizes:")
    for bucket in ["Core", "Speculative"]:
        max_pos = get_max_position_size(account, bucket)
        print(f"  {bucket}: ${max_pos['max_dollars']:,.2f} ({max_pos['max_pct']:.1%})")
