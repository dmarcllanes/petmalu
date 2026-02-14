# --- Calorie calculation ---
# RER = 70 * weight_kg ^ 0.75
RER_COEFFICIENT = 70
RER_EXPONENT = 0.75

ACTIVITY_MULTIPLIERS: dict[str, float] = {
    "sedentary": 1.2,
    "low": 1.4,
    "moderate": 1.6,
    "high": 1.8,
    "very_high": 2.0,
}

NEUTERED_MULTIPLIER = 0.80

# (max_age_months, multiplier) — first match wins
AGE_MULTIPLIERS: list[tuple[int, float]] = [
    (4, 3.0),    # 0-4 months
    (12, 2.0),   # 4-12 months
    (84, 1.0),   # 1-7 years
    (999, 0.9),  # 7+ years
]

MIN_DAILY_CALORIES = 100
MAX_DAILY_CALORIES = 5000
MAX_ADJUSTMENT_PCT = 0.10

# --- Free tier limits ---
FREE_PET_LIMIT = 1

# --- Medical conditions that block advanced features ---
BLOCKED_MEDICAL_CONDITIONS: list[str] = [
    "diabetes",
    "kidney_disease",
    "liver_disease",
    "pancreatitis",
    "heart_disease",
    "cancer",
    "hypothyroidism",
    "hyperthyroidism",
    "cushings_disease",
    "addisons_disease",
]
