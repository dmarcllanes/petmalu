from fasthtml.common import *


def feeding_progress(daily_calories: float, max_calories: float = 3000.0):
    pct = min((daily_calories / max_calories) * 100, 100)

    return Div(
        P("Daily Calorie Target"),
        Div(
            Div(
                Div(
                    Span(f"{daily_calories:.0f}", cls="calorie-ring-value"),
                    Span("kcal/day", cls="calorie-ring-unit"),
                    cls="calorie-ring-inner",
                ),
                cls="calorie-ring-bg",
                style=f"--progress: {pct}",
            ),
            cls="calorie-ring",
        ),
        cls="feeding-progress",
    )
