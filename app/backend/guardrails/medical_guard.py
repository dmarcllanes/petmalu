from app.backend.core.constants import BLOCKED_MEDICAL_CONDITIONS


def has_blocked_condition(conditions: list[str]) -> bool:
    return any(c in BLOCKED_MEDICAL_CONDITIONS for c in conditions)


def block_if_medical_condition(conditions: list[str]) -> None:
    blocked = [c for c in conditions if c in BLOCKED_MEDICAL_CONDITIONS]
    if blocked:
        raise ValueError(
            f"Advanced features blocked for pets with: {', '.join(blocked)}. "
            "Please consult a veterinarian for dietary guidance."
        )
