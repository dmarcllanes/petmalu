from fasthtml.common import Div, H3, P, A, Span


SPECIES_EMOJI = {"dog": "\U0001f436", "cat": "\U0001f431"}


def pet_card(pet, daily_calories: float | None = None):
    emoji = SPECIES_EMOJI.get(pet.species, "\U0001f43e")
    cal_text = f"{daily_calories:.0f} kcal/day" if daily_calories else "Not calculated"

    return Div(
        Div(
            Span(emoji, cls="pet-avatar"),
            Div(
                H3(pet.name),
                Span(pet.species.capitalize(), cls="badge"),
            ),
            cls="card-header",
        ),
        Div(
            Div(
                Span(f"{pet.weight_kg}", cls="stat-value"),
                Span("kg", cls="stat-label"),
                cls="stat-item",
            ),
            Div(
                Span(f"{pet.age_months}", cls="stat-value"),
                Span("months", cls="stat-label"),
                cls="stat-item",
            ),
            Div(
                Span(pet.activity_level.replace("_", " ").capitalize(), cls="stat-value"),
                Span("activity", cls="stat-label"),
                cls="stat-item",
            ),
            cls="stat-grid",
        ),
        Div(
            P(cal_text, cls="calorie-display"),
            A("View Details", href=f"/pets/{pet.id}", cls="btn btn-primary"),
            A("Feeding", href=f"/feeding/{pet.id}", cls="btn btn-secondary"),
            cls="card-footer",
        ),
        cls="pet-card",
    )
