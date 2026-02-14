from app.database.supabase_client import get_supabase
from app.models.weight_models import WeightLogCreate, WeightLogResponse


def create_weight_log(data: WeightLogCreate) -> WeightLogResponse:
    result = (
        get_supabase()
        .table("weight_logs")
        .insert(data.model_dump())
        .execute()
    )
    return WeightLogResponse(**result.data[0])


def get_weight_logs(pet_id: str, limit: int = 30) -> list[WeightLogResponse]:
    result = (
        get_supabase()
        .table("weight_logs")
        .select("*")
        .eq("pet_id", pet_id)
        .order("recorded_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [WeightLogResponse(**row) for row in result.data]


def get_latest_weight(pet_id: str) -> WeightLogResponse | None:
    result = (
        get_supabase()
        .table("weight_logs")
        .select("*")
        .eq("pet_id", pet_id)
        .order("recorded_at", desc=True)
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return WeightLogResponse(**result.data[0])
