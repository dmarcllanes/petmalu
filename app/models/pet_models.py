from datetime import datetime
from pydantic import BaseModel, Field


class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str = Field(min_length=1, max_length=50)
    breed: str | None = None
    weight_kg: float = Field(gt=0, le=200)
    age_months: int = Field(ge=0, le=360)
    activity_level: str = Field(default="moderate")
    is_neutered: bool = False
    medical_conditions: list[str] = Field(default_factory=list)


class PetUpdate(BaseModel):
    name: str | None = None
    species: str | None = None
    breed: str | None = None
    weight_kg: float | None = Field(default=None, gt=0, le=200)
    age_months: int | None = Field(default=None, ge=0, le=360)
    activity_level: str | None = None
    is_neutered: bool | None = None
    medical_conditions: list[str] | None = None


class PetResponse(BaseModel):
    id: str
    name: str
    species: str
    breed: str | None = None
    weight_kg: float
    age_months: int
    activity_level: str
    is_neutered: bool
    medical_conditions: list[str]
    created_at: datetime
    updated_at: datetime
