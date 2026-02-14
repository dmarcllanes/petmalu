from fasthtml.common import Div, H2, P, A, Span

from app.frontend.components.navbar import navbar
from app.frontend.components.pet_card import pet_card


def dashboard_page(pets, calorie_map: dict[str, float] | None = None):
    calorie_map = calorie_map or {}

    if not pets:
        content = Div(
            Span("\U0001f43e", cls="empty-state-icon"),
            H2("Welcome to LuluPet!"),
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
        navbar(),
        Div(content, cls="container"),
    )
