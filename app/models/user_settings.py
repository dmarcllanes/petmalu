from pydantic import BaseModel
from datetime import datetime


class UserSettings(BaseModel):
    """User notification and privacy settings"""
    user_id: str
    email_notifications: bool = True
    feeding_reminders: bool = True
    weight_reminders: bool = True
    data_sharing: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserSettingsUpdate(BaseModel):
    """Update user settings"""
    email_notifications: bool | None = None
    feeding_reminders: bool | None = None
    weight_reminders: bool | None = None
    data_sharing: bool | None = None
