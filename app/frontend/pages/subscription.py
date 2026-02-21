from fasthtml.common import *
from app.frontend.components.navbar import navbar


PLAN_DETAILS = {
    "free": {
        "name": "Free",
        "price": "$0",
        "features": [
            "Track up to 2 pets",
            "Basic calorie calculator",
            "Weight logging",
        ],
    },
    "pro": {
        "name": "Pro",
        "price": "$9.99/mo",
        "features": [
            "Unlimited pets",
            "Advanced analytics",
            "Weight trend graphs",
            "Email reminders",
            "Priority support",
        ],
    },
    "premium": {
        "name": "Premium",
        "price": "$19.99/mo",
        "features": [
            "Everything in Pro",
            "Custom meal plans",
            "Vet appointment reminders",
            "Supplement tracking",
            "Early access to new features",
        ],
    },
}


def subscription_page(subscription):
    """Subscription and billing page"""
    current_plan = subscription.plan if subscription else "free"
    plan_info = PLAN_DETAILS[current_plan]
    
    return (
        navbar(),
        Div(
            H2("Subscription & Billing"),
            
            # Current Plan Section
            Div(
                H3("Current Plan"),
                Div(
                    Div(
                        Span(plan_info["name"], cls="plan-name"),
                        Span(plan_info["price"], cls="plan-price"),
                        cls="plan-header",
                    ),
                    Div(
                        *[P(f"✓ {feature}") for feature in plan_info["features"]],
                        cls="plan-features",
                    ),
                    Div(
                        Span(f"Status: ", cls="label"),
                        Strong(subscription.status.capitalize() if subscription else "Active", cls="status-badge"),
                        cls="plan-status",
                    ) if subscription else "",
                    cls="current-plan-card",
                ),
                cls="section",
            ),
            
            # Upgrade Options Section
            Div(
                H3("Upgrade Your Plan"),
                Div(
                    # Pro Plan Card
                    Div(
                        H3("Pro"),
                        P("$9.99/month", cls="price"),
                        Div(*[P(f"✓ {f}") for f in PLAN_DETAILS["pro"]["features"]], cls="features"),
                        Button(
                            "Upgrade to Pro",
                            hx_post="/subscription/checkout",
                            hx_vals='{"plan": "pro"}',
                            cls="btn btn-primary" if current_plan == "free" else "btn btn-secondary",
                            disabled=current_plan != "free",
                        ) if current_plan == "free" else Span("Current Plan", cls="current-badge"),
                        cls="plan-card",
                    ),
                    # Premium Plan Card
                    Div(
                        H3("Premium"),
                        P("$19.99/month", cls="price"),
                        Div(*[P(f"✓ {f}") for f in PLAN_DETAILS["premium"]["features"]], cls="features"),
                        Button(
                            "Upgrade to Premium",
                            hx_post="/subscription/checkout",
                            hx_vals='{"plan": "premium"}',
                            cls="btn btn-primary" if current_plan in ["free", "pro"] else "btn btn-secondary",
                            disabled=current_plan == "premium",
                        ) if current_plan != "premium" else Span("Current Plan", cls="current-badge"),
                        cls="plan-card",
                    ),
                    cls="plans-grid",
                ),
                cls="section",
            ) if current_plan != "premium" else "",
            
            # Manage Subscription Section
            Div(
                H3("Manage Subscription"),
                P("Manage your payment methods, view invoices, and update billing information."),
                A(
                    "Manage Billing",
                    href="/subscription/portal",
                    cls="btn btn-secondary",
                ) if subscription and subscription.lemon_subscription_id else P("No active subscription to manage."),
                cls="section",
            ) if current_plan != "free" else "",
            
            cls="container subscription-container",
        ),
    )
