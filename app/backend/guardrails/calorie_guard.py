from app.backend.core.constants import MIN_DAILY_CALORIES, MAX_DAILY_CALORIES


def clamp_calories(calories: float) -> float:
    return max(MIN_DAILY_CALORIES, min(MAX_DAILY_CALORIES, calories))


def validate_calorie_range(calories: float) -> None:
    if calories < MIN_DAILY_CALORIES or calories > MAX_DAILY_CALORIES:
        raise ValueError(
            f"Calories {calories} outside allowed range "
            f"[{MIN_DAILY_CALORIES}, {MAX_DAILY_CALORIES}]"
        )
