from app.backend.core.constants import MAX_ADJUSTMENT_PCT


def validate_adjustment(original: float, adjusted: float) -> None:
    if original <= 0:
        raise ValueError("Original calorie value must be positive")
    change_pct = abs(adjusted - original) / original
    if change_pct > MAX_ADJUSTMENT_PCT:
        raise ValueError(
            f"Calorie adjustment of {change_pct:.0%} exceeds "
            f"the maximum allowed ±{MAX_ADJUSTMENT_PCT:.0%}"
        )


def apply_adjustment(original: float, pct: float) -> float:
    if abs(pct) > MAX_ADJUSTMENT_PCT:
        raise ValueError(
            f"Adjustment of {pct:.0%} exceeds ±{MAX_ADJUSTMENT_PCT:.0%}"
        )
    return round(original * (1 + pct), 1)
