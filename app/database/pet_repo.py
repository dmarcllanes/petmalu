from app.database.supabase_client import get_supabase
from app.models.pet_models import PetCreate, PetUpdate, PetResponse


def create_pet(data: PetCreate, user_id: str) -> PetResponse:
    pet_data = data.model_dump()
    pet_data["user_id"] = user_id  # Add user_id to pet data
    result = (
        get_supabase()
        .table("pets")
        .insert(pet_data)
        .execute()
    )
    return PetResponse(**result.data[0])


def get_pet(pet_id: str, user_id: str) -> PetResponse | None:
    result = (
        get_supabase()
        .table("pets")
        .select("*")
        .eq("id", pet_id)
        .eq("user_id", user_id)  # Filter by user
        .execute()
    )
    if not result.data:
        return None
    return PetResponse(**result.data[0])


def get_all_pets(user_id: str) -> list[PetResponse]:
    result = (
        get_supabase()
        .table("pets")
        .select("*")
        .eq("user_id", user_id)  # Filter by user
        .order("created_at", desc=True)
        .execute()
    )
    return [PetResponse(**row) for row in result.data]


def update_pet(pet_id: str, data: PetUpdate, user_id: str) -> PetResponse | None:
    payload = data.model_dump(exclude_none=True)
    if not payload:
        return get_pet(pet_id, user_id)
    result = (
        get_supabase()
        .table("pets")
        .update(payload)
        .eq("id", pet_id)
        .eq("user_id", user_id)  # Filter by user
        .execute()
    )
    if not result.data:
        return None
    return PetResponse(**result.data[0])


def delete_pet(pet_id: str, user_id: str) -> bool:
    result = (
        get_supabase()
        .table("pets")
        .delete()
        .eq("id", pet_id)
        .eq("user_id", user_id)  # Filter by user
        .execute()
    )
    return bool(result.data)


def count_pets(user_id: str) -> int:
    result = (
        get_supabase()
        .table("pets")
        .select("id", count="exact")
        .eq("user_id", user_id)  # Filter by user
        .execute()
    )
    return result.count or 0
