from app.backend.core.constants import (
    RER_COEFFICIENT,
    RER_EXPONENT,
    ACTIVITY_MULTIPLIERS,
    AGE_MULTIPLIERS,
    NEUTERED_MULTIPLIER,
    MIN_DAILY_CALORIES,
    MAX_DAILY_CALORIES,
)
from app.models.feeding_models import FeedingCalcRequest, FeedingCalcResponse
from app.backend.guardrails.medical_guard import block_if_medical_condition


def calculate_rer(weight_kg: float) -> float:
    return RER_COEFFICIENT * (weight_kg ** RER_EXPONENT)


def get_activity_multiplier(level: str) -> float:
    return ACTIVITY_MULTIPLIERS.get(level, ACTIVITY_MULTIPLIERS["moderate"])


def get_age_multiplier(age_months: int) -> float:
    for max_months, multiplier in AGE_MULTIPLIERS:
        if age_months <= max_months:
            return multiplier
    return 1.0


def calculate_daily_calories(req: FeedingCalcRequest) -> FeedingCalcResponse:
    block_if_medical_condition(req.medical_conditions)

    rer = calculate_rer(req.weight_kg)
    activity_mult = get_activity_multiplier(req.activity_level)
    age_mult = get_age_multiplier(req.age_months)
    neutered_mult = NEUTERED_MULTIPLIER if req.is_neutered else 1.0

    daily = rer * activity_mult * age_mult * neutered_mult
    daily = max(MIN_DAILY_CALORIES, min(MAX_DAILY_CALORIES, daily))
    daily = round(daily, 1)

    return FeedingCalcResponse(
        daily_calories=daily,
        rer=round(rer, 1),
        activity_multiplier=activity_mult,
        age_multiplier=age_mult,
        neutered_multiplier=neutered_mult,
    )
