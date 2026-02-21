from app.database.supabase_client import get_supabase
from app.models.user_settings import UserSettings, UserSettingsUpdate


def get_user_settings(user_id: str) -> UserSettings | None:
    """Get user settings by user ID"""
    supabase = get_supabase()
    result = supabase.table("user_settings").select("*").eq("user_id", user_id).execute()
    
    if result.data:
        return UserSettings(**result.data[0])
    return None


def create_default_settings(user_id: str) -> UserSettings:
    """Create default settings for a new user"""
    supabase = get_supabase()
    
    settings_data = {
        "user_id": user_id,
        "email_notifications": True,
        "feeding_reminders": True,
        "weight_reminders": True,
        "data_sharing": False,
    }
    
    result = supabase.table("user_settings").insert(settings_data).execute()
    return UserSettings(**result.data[0]) if result.data else None


def get_or_create_settings(user_id: str) -> UserSettings:
    """Get existing settings or create default ones"""
    settings = get_user_settings(user_id)
    if not settings:
        settings = create_default_settings(user_id)
    return settings


def update_user_settings(user_id: str, updates: UserSettingsUpdate) -> UserSettings | None:
    """Update user settings"""
    supabase = get_supabase()
    
    # Only update fields that are provided
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    
    if not update_data:
        return get_user_settings(user_id)
    
    result = supabase.table("user_settings").update(update_data).eq("user_id", user_id).execute()
    return UserSettings(**result.data[0]) if result.data else None
