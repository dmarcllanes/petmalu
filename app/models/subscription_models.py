from pydantic import BaseModel
from datetime import datetime


class Subscription(BaseModel):
    """User subscription data"""
    id: str | None = None
    user_id: str
    plan: str = "free"  # free, pro, premium
    status: str = "active"  # active, canceled, expired, past_due
    lemon_subscription_id: str | None = None
    lemon_customer_id: str | None = None
    renews_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SubscriptionCreate(BaseModel):
    """Create new subscription"""
    user_id: str
    plan: str
    lemon_subscription_id: str | None = None
    lemon_customer_id: str | None = None
    renews_at: datetime | None = None


class SubscriptionUpdate(BaseModel):
    """Update subscription"""
    plan: str | None = None
    status: str | None = None
    lemon_subscription_id: str | None = None
    renews_at: datetime | None = None
