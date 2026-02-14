from datetime import datetime
from pydantic import BaseModel, Field


class WeightLogCreate(BaseModel):
    pet_id: str
    weight_kg: float = Field(gt=0, le=200)


class WeightLogResponse(BaseModel):
    id: str
    pet_id: str
    weight_kg: float
    recorded_at: datetime
