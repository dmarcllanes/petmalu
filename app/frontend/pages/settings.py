from fasthtml.common import *
from app.frontend.components.navbar import navbar
from app.frontend.components.bottom_nav import bottom_nav


def settings_page(user, settings, subscription, tab="profile", pet_count: int = 0, total_calories: float = 0, avg_weight: float = 0):
    """Unified settings page with tabs for Profile, Subscription, and Help"""

    # Determine active tab
    is_profile = tab == "profile"
    is_subscription = tab == "subscription"
    is_help = tab == "help"

    return (
        navbar(),
        Div(
            H2("Settings"),

            # Tab Navigation
            Div(
                Ul(
                    Li(
                        A("Profile",
                          href="#",
                          cls="tab-link active" if is_profile else "tab-link",
                          onclick="switchTab('profile', event)",
                          data_tab="profile"),
                    ),
                    Li(
                        A("Subscription",
                          href="#",
                          cls="tab-link active" if is_subscription else "tab-link",
                          onclick="switchTab('subscription', event)",
                          data_tab="subscription"),
                    ),
                    Li(
                        A("Help",
                          href="#",
                          cls="tab-link active" if is_help else "tab-link",
                          onclick="switchTab('help', event)",
                          data_tab="help"),
                    ),
                    cls="tabs",
                ),
                cls="tabs-container",
            ),

            # Tab Content
            Div(
                # Profile Tab
                Div(
                    profile_tab_content(user, settings),
                    cls="tab-content active" if is_profile else "tab-content hidden",
                    id="profile-tab",
                ),

                # Subscription Tab
                Div(
                    subscription_tab_content(subscription),
                    cls="tab-content active" if is_subscription else "tab-content hidden",
                    id="subscription-tab",
                ),

                # Help Tab
                Div(
                    help_tab_content(),
                    cls="tab-content active" if is_help else "tab-content hidden",
                    id="help-tab",
                ),

                cls="tab-content-container",
            ),

            Script("""
                function switchTab(tab, event) {
                    event.preventDefault();
                    // Update tab links
                    document.querySelectorAll('.tab-link').forEach(function(link) {
                        link.classList.remove('active');
                    });
                    event.currentTarget.classList.add('active');
                    // Update tab content
                    document.querySelectorAll('.tab-content').forEach(function(content) {
                        content.classList.remove('active');
                        content.classList.add('hidden');
                    });
                    var target = document.getElementById(tab + '-tab');
                    if (target) {
                        target.classList.remove('hidden');
                        target.classList.add('active');
                    }
                    // Update URL without reload
                    history.replaceState(null, '', '/settings?tab=' + tab);
                }
            """),

            cls="container settings-container",
        ),
        bottom_nav(
            pet_count=pet_count,
            total_calories=total_calories,
            avg_weight=avg_weight,
            active_pets=pet_count,
        ),
    )


def profile_tab_content(user, settings):
    """Profile settings content"""
    from app.frontend.pages.subscription import PLAN_DETAILS
    
    return Div(
        # Account Details Section
        Div(
            H3("Account Details"),
            Form(
                Div(
                    Label("Email", _for="email"),
                    Input(
                        name="email",
                        id="email",
                        type="email",
                        value=user.get('email', ''),
                        disabled=True,
                    ),
                    P("Email cannot be changed", cls="field-hint"),
                    cls="form-group",
                ),
                Div(
                    Label("Full Name", _for="full_name"),
                    Input(
                        name="full_name",
                        id="full_name",
                        type="text",
                        value=user.get('full_name', ''),
                    ),
                    cls="form-group",
                ),
                Button("Update Profile", type="submit", cls="btn btn-primary"),
                method="post",
                action="/profile/update",
            ),
            cls="section",
        ),
        
        # Notification Preferences
        Div(
            H3("Notification Preferences"),
            Form(
                Div(
                    Input(
                        type="checkbox",
                        name="email_notifications",
                        id="email_notifications",
                        checked=settings.email_notifications,
                    ),
                    Label("Email Notifications", _for="email_notifications"),
                    cls="checkbox-group",
                ),
                Div(
                    Input(
                        type="checkbox",
                        name="feeding_reminders",
                        id="feeding_reminders",
                        checked=settings.feeding_reminders,
                    ),
                    Label("Feeding Reminders", _for="feeding_reminders"),
                    cls="checkbox-group",
                ),
                Div(
                    Input(
                        type="checkbox",
                        name="weight_reminders",
                        id="weight_reminders",
                        checked=settings.weight_reminders,
                    ),
                    Label("Weight Tracking Reminders", _for="weight_reminders"),
                    cls="checkbox-group",
                ),
                Button("Save Preferences", type="submit", cls="btn btn-primary"),
                method="post",
                action="/profile/settings",
            ),
            cls="section",
        ),
        
        # Privacy Settings
        Div(
            H3("Privacy"),
            Form(
                Div(
                    Input(
                        type="checkbox",
                        name="data_sharing",
                        id="data_sharing",
                        checked=settings.data_sharing,
                    ),
                    Label("Share anonymized data to improve MukaPet", _for="data_sharing"),
                    cls="checkbox-group",
                ),
                Button("Update Privacy", type="submit", cls="btn btn-primary"),
                method="post",
                action="/profile/privacy",
            ),
            cls="section",
        ),
    )


def subscription_tab_content(subscription):
    """Subscription settings content"""
    from app.frontend.pages.subscription import PLAN_DETAILS
    
    current_plan = subscription.plan if subscription else "free"
    plan_info = PLAN_DETAILS[current_plan]
    
    return Div(
        # Current Plan
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
        
        # Upgrade Options
        Div(
            H3("Upgrade Your Plan"),
            Div(
                # Pro Plan
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
                # Premium Plan
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
        
        # Manage Subscription
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
    )


def help_tab_content():
    """Help center content"""
    FAQ_ITEMS = [
        {
            "question": "How do I calculate my pet's daily calorie needs?",
            "answer": "Navigate to your pet's profile and click 'Calculate Calories'. Our calculator uses your pet's weight, age, activity level, and neutering status to determine their daily caloric needs based on veterinary standards."
        },
        {
            "question": "How often should I track my pet's weight?",
            "answer": "We recommend tracking your pet's weight weekly for growing puppies/kittens and monthly for adult pets. Regular monitoring helps detect health issues early."
        },
        {
            "question": "What do the different subscription plans include?",
            "answer": "Free plan allows tracking up to 2 pets. Pro plan ($9.99/mo) includes unlimited pets, advanced analytics, and email reminders. Premium plan ($19.99/mo) adds custom meal plans and vet appointment reminders."
        },
        {
            "question": "Can I cancel my subscription anytime?",
            "answer": "Yes! You can cancel your subscription at any time from the Subscription tab. You'll continue to have access until the end of your billing period."
        },
        {
            "question": "Is my pet's data secure?",
            "answer": "Absolutely. We use industry-standard encryption and secure hosting. Your data is never sold to third parties. You can manage your privacy settings in the Profile tab."
        },
    ]
    
    PET_CARE_TIPS = [
        {
            "title": "🥣 Portion Control",
            "tip": "Use measuring cups to ensure consistent portions. Free-feeding can lead to obesity in pets."
        },
        {
            "title": "💧 Hydration Matters",
            "tip": "Always provide fresh water. Cats especially need encouragement to drink - consider a water fountain."
        },
        {
            "title": "🏃 Exercise Daily",
            "tip": "Dogs need 30-120 minutes of exercise daily depending on breed. Cats benefit from 15 minutes of play twice a day."
        },
        {
            "title": "⚖️ Monitor Weight Trends",
            "tip": "A sudden weight change (>10%) can indicate health issues. Use MukaPet's weight tracking to spot trends early."
        },
    ]
    
    return Div(
        # FAQ Section
        Div(
            H3("Frequently Asked Questions"),
            *[
                Details(
                    Summary(faq["question"]),
                    P(faq["answer"]),
                    cls="faq-item",
                )
                for faq in FAQ_ITEMS
            ],
            cls="faq-section section",
        ),
        
        # Pet Care Tips
        Div(
            H3("Pet Care Resources"),
            Div(
                *[
                    Div(
                        P(tip["title"], cls="tip-title"),
                        P(tip["tip"], cls="tip-content"),
                        cls="tip-card",
                    )
                    for tip in PET_CARE_TIPS
                ],
                cls="tips-grid",
            ),
            cls="tips-section section",
        ),
        
        # Contact Form
        Div(
            H3("Contact Support"),
            P("Have a question or issue? Send us a message and we'll get back to you soon."),
            Form(
                Div(
                    Label("Name", _for="name"),
                    Input(
                        name="name",
                        id="name",
                        type="text",
                        required=True,
                    ),
                    cls="form-group",
                ),
                Div(
                    Label("Email", _for="email"),
                    Input(
                        name="email",
                        id="email",
                        type="email",
                        required=True,
                    ),
                    cls="form-group",
                ),
                Div(
                    Label("Message", _for="message"),
                    Textarea(
                        name="message",
                        id="message",
                        rows=6,
                        required=True,
                        placeholder="Describe your question or issue...",
                    ),
                    cls="form-group",
                ),
                Button("Send Message", type="submit", cls="btn btn-primary"),
                method="post",
                action="/help/contact",
                cls="contact-form",
            ),
            cls="contact-section section",
        ),
    )
