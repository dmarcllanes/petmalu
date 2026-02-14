from pydantic import BaseModel, Field


class FeedingCalcRequest(BaseModel):
    weight_kg: float = Field(gt=0, le=200)
    age_months: int = Field(ge=0, le=360)
    activity_level: str = Field(default="moderate")
    is_neutered: bool = False
    medical_conditions: list[str] = Field(default_factory=list)


class FeedingCalcResponse(BaseModel):
    daily_calories: float
    rer: float
    activity_multiplier: float
    age_multiplier: float
    neutered_multiplier: float
