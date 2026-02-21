from fasthtml.common import *
from app.frontend.components.navbar import navbar


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
        "answer": "Yes! You can cancel your subscription at any time from the Subscription page. You'll continue to have access until the end of your billing period."
    },
    {
        "question": "Is my pet's data secure?",
        "answer": "Absolutely. We use industry-standard encryption and secure hosting. Your data is never sold to third parties. You can manage your privacy settings in your Profile."
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


def help_page():
    """Help center and support page"""
    
    return (
        navbar(),
        Div(
            H2("Help Center"),
            
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
            
            # Pet Care Tips Section
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
            
            # Contact Form Section
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
            
            cls="container help-container",
        ),
    )
