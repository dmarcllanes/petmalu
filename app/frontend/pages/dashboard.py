from fasthtml.common import Div, H2, P, A, Span, Title

from app.frontend.components.navbar import navbar
from app.frontend.components.pet_card import pet_card
from app.frontend.components.bottom_nav import bottom_nav


def dashboard_page(pets, calorie_map: dict[str, float] | None = None):
    calorie_map = calorie_map or {}
    pet_count = len(pets) if pets else 0
    total_calories = sum(calorie_map.values())
    avg_weight = sum(p.weight_kg for p in pets) / len(pets) if pets else 0

    if not pets:
        content = Div(
            Span("\U0001f43e", cls="empty-state-icon"),
            H2("Welcome to MukaPet!"),
            P("You haven't added a pet yet. Get started by creating your first pet profile."),
            A("Add Your Pet", href="/pets/new", cls="btn btn-primary btn-lg"),
            cls="empty-state",
        )
    else:
        cards = [pet_card(p, calorie_map.get(p.id)) for p in pets]
        content = Div(
            H2("Your Pets"),
            Div(*cards, cls="pet-grid"),
            cls="pet-list",
        )

    return (
        Title("MukaPet Dashboard"),
        navbar(),
        Div(content, cls="container"),
        bottom_nav(
            pet_count=pet_count,
            total_calories=total_calories,
            avg_weight=avg_weight,
            active_pets=pet_count,
        ),
    )
