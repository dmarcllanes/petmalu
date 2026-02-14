from app.database.supabase_client import get_supabase


def store_feeding_calc(pet_id: str, daily_calories: float, rer: float) -> dict:
    result = (
        get_supabase()
        .table("feeding_calculations")
        .insert({
            "pet_id": pet_id,
            "daily_calories": daily_calories,
            "rer": rer,
        })
        .execute()
    )
    return result.data[0]


def get_latest_feeding_calc(pet_id: str) -> dict | None:
    result = (
        get_supabase()
        .table("feeding_calculations")
        .select("*")
        .eq("pet_id", pet_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None
