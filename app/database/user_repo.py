from app.database.supabase_client import get_supabase


def get_or_create_user(user_id: str, email: str, full_name: str = None, avatar_url: str = None):
    """Get existing user or create new one from Google Auth data"""
    supabase = get_supabase()
    
    # Try to get existing user
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if result.data:
        # User exists, update info
        update_data = {"email": email}
        if full_name:
            update_data["full_name"] = full_name
        if avatar_url:
            update_data["avatar_url"] = avatar_url
        
        supabase.table("users").update(update_data).eq("id", user_id).execute()
        return result.data[0]
    else:
        # Create new user
        user_data = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "avatar_url": avatar_url,
        }
        result = supabase.table("users").insert(user_data).execute()
        return result.data[0] if result.data else None


def get_user(user_id: str):
    """Get user by ID"""
    supabase = get_supabase()
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None


def update_user(user_id: str, data: dict):
    """Update user info"""
    supabase = get_supabase()
    result = supabase.table("users").update(data).eq("id", user_id).execute()
    return result.data[0] if result.data else None
