from fasthtml.common import Div, H2, H3, P, Span, Strong, Form, Label, Input, Button, A

from app.frontend.components.navbar import navbar
from app.frontend.components.feeding_progress import feeding_progress


def feeding_page(pet, calc_result=None, error: str | None = None):
    result_section = ""
    if calc_result:
        result_section = Div(
            feeding_progress(calc_result.daily_calories),
            Div(
                H3("Calculation Breakdown"),
                Div(Span("RER"), Strong(f"{calc_result.rer} kcal"), cls="info-row"),
                Div(Span("Activity Multiplier"), Strong(f"{calc_result.activity_multiplier}x"), cls="info-row"),
                Div(Span("Age Multiplier"), Strong(f"{calc_result.age_multiplier}x"), cls="info-row"),
                Div(Span("Neutered Multiplier"), Strong(f"{calc_result.neutered_multiplier}x"), cls="info-row"),
                cls="calc-breakdown",
            ),
            cls="calc-result",
        )

    return (
        navbar(),
        Div(
            H2(f"Feeding Calculator — {pet.name}"),
            P(error, cls="error") if error else "",
            Div(
                Div(Span("Current Weight"), Strong(f"{pet.weight_kg} kg"), cls="info-row"),
                Div(Span("Activity"), Strong(pet.activity_level.replace("_", " ").capitalize()), cls="info-row"),
                Button(
                    "Calculate Calories",
                    hx_post=f"/feeding/{pet.id}/calculate",
                    hx_target="#calc-result",
                    hx_swap="innerHTML",
                    cls="btn btn-primary",
                ),
                cls="pet-summary",
            ),
            Div(result_section, id="calc-result"),
            Div(
                H3("Log Weight"),
                Form(
                    Div(
                        Label("Weight (kg)", _for="weight_kg"),
                        Input(
                            name="weight_kg", id="weight_kg", type="number",
                            step="0.1", min="0.1", required=True,
                        ),
                        cls="form-group",
                    ),
                    Input(name="pet_id", type="hidden", value=pet.id),
                    Button("Log Weight", type="submit", cls="btn btn-secondary"),
                    method="post", action=f"/weight/{pet.id}",
                ),
                cls="weight-log-form",
            ),
            A("Back to Dashboard", href="/", cls="btn"),
            cls="container",
        ),
    )
