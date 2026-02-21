from app.database.supabase_client import get_supabase
from app.models.subscription_models import Subscription, SubscriptionCreate, SubscriptionUpdate


def get_user_subscription(user_id: str) -> Subscription | None:
    """Get active subscription for a user"""
    supabase = get_supabase()
    result = supabase.table("subscriptions").select("*").eq("user_id", user_id).execute()
    
    if result.data:
        return Subscription(**result.data[0])
    return None


def create_subscription(data: SubscriptionCreate) -> Subscription | None:
    """Create a new subscription"""
    supabase = get_supabase()
    
    subscription_data = data.dict()
    result = supabase.table("subscriptions").insert(subscription_data).execute()
    return Subscription(**result.data[0]) if result.data else None


def get_or_create_free_subscription(user_id: str) -> Subscription:
    """Get existing subscription or create free tier"""
    subscription = get_user_subscription(user_id)
    if not subscription:
        subscription = create_subscription(
            SubscriptionCreate(user_id=user_id, plan="free")
        )
    return subscription


def update_subscription(user_id: str, updates: SubscriptionUpdate) -> Subscription | None:
    """Update subscription status"""
    supabase = get_supabase()
    
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    
    if not update_data:
        return get_user_subscription(user_id)
    
    result = supabase.table("subscriptions").update(update_data).eq("user_id", user_id).execute()
    return Subscription(**result.data[0]) if result.data else None


def cancel_subscription(user_id: str) -> Subscription | None:
    """Cancel a subscription"""
    return update_subscription(user_id, SubscriptionUpdate(status="canceled"))
