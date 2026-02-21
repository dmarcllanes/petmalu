from fasthtml.common import *
from app.frontend.components.navbar import navbar
from app.frontend.components.bottom_nav import bottom_nav
from app.frontend.components.wizard_steps import wizard_steps

SPECIES_OPTIONS = ["dog", "cat"]
ACTIVITY_OPTIONS = ["sedentary", "low", "moderate", "high", "very_high"]


# ---------------------------------------------------------------------------
# Wizard: 3-step pet creation
# ---------------------------------------------------------------------------

def wizard_page(step: int = 1, data: dict | None = None, error: str | None = None):
    data = data or {}
    return (
        navbar(),
        Div(
            H2("Add New Pet"),
            Div(
                _wizard_step_content(step, data, error),
                cls="wizard-shell",
            ),
            cls="container",
        ),
    )


def _wizard_step_content(step: int, data: dict, error: str | None = None):
    if step == 1:
        return wizard_step_1_content(data, error)
    elif step == 2:
        return wizard_step_2_content(data, error)
    return wizard_step_3_content(data, error)


def wizard_step_1_content(data: dict, error: str | None = None):
    return Form(
        wizard_steps(1),
        P(error, cls="error") if error else "",
        H3("Basic Info"),
        Div(
            Label("Name", _for="name"),
            Input(name="name", id="name", required=True, value=data.get("name", "")),
            cls="form-group",
        ),
        Div(
            Label("Species", _for="species"),
            Select(
                *[
                    Option(s.capitalize(), value=s, selected=(data.get("species") == s))
                    for s in SPECIES_OPTIONS
                ],
                name="species", id="species",
            ),
            cls="form-group",
        ),
        Div(
            Label("Breed (optional)", _for="breed"),
            Input(name="breed", id="breed", value=data.get("breed", "")),
            cls="form-group",
        ),
        Div(
            Button(
                "Next", type="submit",
                hx_post="/pets/wizard/step/2",
                hx_target="#wizard-content",
                hx_swap="outerHTML",
                cls="btn btn-primary btn-lg btn-block",
            ),
            cls="wizard-actions",
            style="justify-content: center;",
        ),
        id="wizard-content",
    )


def wizard_step_2_content(data: dict, error: str | None = None):
    return Form(
        wizard_steps(2),
        P(error, cls="error") if error else "",
        H3("Health Profile"),
        # Hidden inputs carry step 1 data forward
        Input(type="hidden", name="name", value=data.get("name", "")),
        Input(type="hidden", name="species", value=data.get("species", "")),
        Input(type="hidden", name="breed", value=data.get("breed", "")),
        Div(
            Label("Weight (kg)", _for="weight_kg"),
            Input(
                name="weight_kg", id="weight_kg", type="number",
                step="0.1", min="0.1", required=True,
                value=data.get("weight_kg", ""),
            ),
            cls="form-group",
        ),
        Div(
            Label("Age (months)", _for="age_months"),
            Input(
                name="age_months", id="age_months", type="number",
                min="0", required=True,
                value=data.get("age_months", ""),
            ),
            cls="form-group",
        ),
        Div(
            Label(
                Input(
                    name="is_neutered", type="checkbox", value="true",
                    checked=data.get("is_neutered") == "true",
                ),
                " Neutered / Spayed",
            ),
            cls="form-group checkbox-group",
        ),
        Div(
            Button(
                "Back", type="submit",
                hx_post="/pets/wizard/step/1",
                hx_target="#wizard-content",
                hx_swap="outerHTML",
                cls="btn",
            ),
            Button(
                "Next", type="submit",
                hx_post="/pets/wizard/step/3",
                hx_target="#wizard-content",
                hx_swap="outerHTML",
                cls="btn btn-primary btn-lg",
            ),
            cls="wizard-actions",
        ),
        id="wizard-content",
    )


def wizard_step_3_content(data: dict, error: str | None = None):
    neutered_display = "Yes" if data.get("is_neutered") == "true" else "No"

    return Form(
        wizard_steps(3),
        P(error, cls="error") if error else "",
        H3("Activity & Review"),
        # Hidden inputs carry all previous data
        Input(type="hidden", name="name", value=data.get("name", "")),
        Input(type="hidden", name="species", value=data.get("species", "")),
        Input(type="hidden", name="breed", value=data.get("breed", "")),
        Input(type="hidden", name="weight_kg", value=data.get("weight_kg", "")),
        Input(type="hidden", name="age_months", value=data.get("age_months", "")),
        Input(type="hidden", name="is_neutered", value=data.get("is_neutered", "")),
        Div(
            Label("Activity Level", _for="activity_level"),
            Select(
                *[
                    Option(
                        a.replace("_", " ").capitalize(), value=a,
                        selected=(data.get("activity_level") == a),
                    )
                    for a in ACTIVITY_OPTIONS
                ],
                name="activity_level", id="activity_level",
            ),
            cls="form-group",
        ),
        # Review summary
        Div(
            H4("Review"),
            Div(
                Div(
                    Span("Name", cls="label"),
                    Span(data.get("name", "—"), cls="value"),
                    cls="review-item",
                ),
                Div(
                    Span("Species", cls="label"),
                    Span(data.get("species", "—").capitalize(), cls="value"),
                    cls="review-item",
                ),
                Div(
                    Span("Breed", cls="label"),
                    Span(data.get("breed") or "Not specified", cls="value"),
                    cls="review-item",
                ),
                Div(
                    Span("Weight", cls="label"),
                    Span(f"{data.get('weight_kg', '—')} kg", cls="value"),
                    cls="review-item",
                ),
                Div(
                    Span("Age", cls="label"),
                    Span(f"{data.get('age_months', '—')} months", cls="value"),
                    cls="review-item",
                ),
                Div(
                    Span("Neutered", cls="label"),
                    Span(neutered_display, cls="value"),
                    cls="review-item",
                ),
                cls="review-grid",
            ),
            cls="review-card",
        ),
        Div(
            Button(
                "Back", type="submit",
                hx_post="/pets/wizard/step/2",
                hx_target="#wizard-content",
                hx_swap="outerHTML",
                cls="btn",
            ),
            Button("Create Pet", type="button",
                   cls="btn btn-primary btn-lg",
                   onclick="var btn=this;btn.disabled=true;btn.textContent='Creating...';fetch('/pets/new',{method:'POST',body:new FormData(btn.closest('form')),redirect:'manual'}).then(function(r){console.log('Response:',r.status,r.type,r.ok);if(r.type==='opaqueredirect'){window.location.href='/dashboard';return}return r.text().then(function(t){console.log('Body:',t.substring(0,500));var tmp=document.createElement('div');tmp.innerHTML=t;var errEl=tmp.querySelector('#create-error');var msg=errEl?errEl.textContent.trim():'Status '+r.status+': '+tmp.textContent.substring(0,200);alert(msg);btn.disabled=false;btn.textContent='Create Pet'})}).catch(function(e){alert('Error: '+e);btn.disabled=false;btn.textContent='Create Pet'})"),
            cls="wizard-actions",
        ),
        id="wizard-content",
    )


# ---------------------------------------------------------------------------
# Edit form (single page, restyled)
# ---------------------------------------------------------------------------

def pet_form_page(pet=None, error: str | None = None):
    is_edit = pet is not None
    if not is_edit:
        return wizard_page()

    title = f"Edit {pet.name}"
    action = f"/pets/{pet.id}/edit"

    return (
        navbar(),
        Div(
            H2(title),
            Div(
                P(error, cls="error") if error else "",
                Form(
                    Div(
                        Label("Name", _for="name"),
                        Input(name="name", id="name", required=True, value=pet.name),
                        cls="form-group",
                    ),
                    Div(
                        Label("Species", _for="species"),
                        Select(
                            *[
                                Option(s.capitalize(), value=s, selected=(pet.species == s))
                                for s in SPECIES_OPTIONS
                            ],
                            name="species", id="species",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Breed (optional)", _for="breed"),
                        Input(
                            name="breed", id="breed",
                            value=pet.breed if pet.breed else "",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Weight (kg)", _for="weight_kg"),
                        Input(
                            name="weight_kg", id="weight_kg", type="number",
                            step="0.1", min="0.1", required=True,
                            value=str(pet.weight_kg),
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Age (months)", _for="age_months"),
                        Input(
                            name="age_months", id="age_months", type="number",
                            min="0", required=True,
                            value=str(pet.age_months),
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Activity Level", _for="activity_level"),
                        Select(
                            *[
                                Option(
                                    a.replace("_", " ").capitalize(), value=a,
                                    selected=(pet.activity_level == a),
                                )
                                for a in ACTIVITY_OPTIONS
                            ],
                            name="activity_level", id="activity_level",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label(
                            Input(
                                name="is_neutered", type="checkbox", value="true",
                                checked=pet.is_neutered,
                            ),
                            " Neutered / Spayed",
                        ),
                        cls="form-group checkbox-group",
                    ),
                    Div(
                        Button("Save Pet", type="submit", cls="btn btn-primary"),
                        A("Cancel", href=f"/pets/{pet.id}", cls="btn"),
                        cls="form-actions",
                    ),
                    method="post", action=action,
                ),
                cls="wizard-shell",
            ),
            cls="container",
        ),
    )


# ---------------------------------------------------------------------------
# Detail page (restyled)
# ---------------------------------------------------------------------------

def pet_detail_page(pet, daily_calories: float | None = None, weight_logs=None, trend: str = "insufficient_data", pet_count: int = 0, total_calories: float = 0, avg_weight: float = 0):
    cal_text = f"{daily_calories:.0f} kcal/day" if daily_calories else "Not yet calculated"
    trend_labels = {
        "gaining": "Gaining weight",
        "losing": "Losing weight",
        "stable": "Stable",
        "insufficient_data": "Not enough data",
    }

    log_rows = []
    if weight_logs:
        for log in weight_logs:
            log_rows.append(
                P(f"{log.recorded_at.strftime('%b %d, %Y')} — {log.weight_kg} kg")
            )

    return (
        navbar(),
        Div(
            H2(pet.name),
            Div(
                Div(Span("Species"), Strong(pet.species.capitalize()), cls="info-row"),
                Div(Span("Breed"), Strong(pet.breed or "Unknown"), cls="info-row"),
                Div(Span("Weight"), Strong(f"{pet.weight_kg} kg"), cls="info-row"),
                Div(Span("Age"), Strong(f"{pet.age_months} months"), cls="info-row"),
                Div(Span("Activity"), Strong(pet.activity_level.replace("_", " ").capitalize()), cls="info-row"),
                Div(Span("Neutered"), Strong("Yes" if pet.is_neutered else "No"), cls="info-row"),
                Div(Span("Daily Calories"), Strong(cal_text), cls="info-row highlight"),
                Div(Span("Weight Trend"), Strong(trend_labels.get(trend, trend)), cls="info-row"),
                cls="pet-detail",
            ),
            Div(
                H2("Weight History"),
                *(log_rows if log_rows else [P("No weight logs yet.")]),
                cls="weight-history",
            ),
            Div(
                A("Edit Pet", href=f"/pets/{pet.id}/edit", cls="btn btn-primary"),
                A("Calculate Feeding", href=f"/feeding/{pet.id}", cls="btn btn-secondary"),
                A("Back to Dashboard", href="/", cls="btn"),
                cls="actions",
            ),
            cls="container",
        ),
        bottom_nav(
            pet_count=pet_count,
            total_calories=total_calories,
            avg_weight=avg_weight,
            active_pets=pet_count,
        ),
    )
