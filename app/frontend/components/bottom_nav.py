from fasthtml.common import Div, Span


def bottom_nav(
    pet_count: int = 0,
    total_calories: float = 0,
    avg_weight: float = 0,
    active_pets: int = 0,
):
    """Sticky bottom analytics bar showing key pet stats."""

    cal_display = f"{total_calories:,.0f}" if total_calories else "—"
    weight_display = f"{avg_weight:.1f}" if avg_weight else "—"

    return Div(
        Div(
            # Pets stat
            Div(
                Span(str(pet_count), cls="stat-bar-value"),
                Span("Pets", cls="stat-bar-label"),
                cls="stat-bar-item",
            ),
            # Divider
            Span(cls="stat-bar-divider"),
            # Total daily calories
            Div(
                Span(cal_display, cls="stat-bar-value"),
                Span("kcal/day", cls="stat-bar-label"),
                cls="stat-bar-item",
            ),
            # Divider
            Span(cls="stat-bar-divider"),
            # Avg weight
            Div(
                Span(weight_display, cls="stat-bar-value"),
                Span("avg kg", cls="stat-bar-label"),
                cls="stat-bar-item",
            ),
            # Divider
            Span(cls="stat-bar-divider"),
            # Active profiles
            Div(
                Span(str(active_pets), cls="stat-bar-value stat-bar-active"),
                Span("Active", cls="stat-bar-label"),
                cls="stat-bar-item",
            ),
            cls="stat-bar-container",
        ),
        cls="stat-bar",
    )
