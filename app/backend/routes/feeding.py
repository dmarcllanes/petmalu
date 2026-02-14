from app.database import pet_repo
from app.models.feeding_models import FeedingCalcRequest
from app.backend.services.calorie_engine import calculate_daily_calories
from app.frontend.pages.feeding import feeding_page
from app.frontend.components.feeding_progress import feeding_progress
from fasthtml.common import Div, H3, P


def register_feeding_routes(app):

    @app.get("/feeding/{pet_id}")
    def feeding_view(pet_id: str, session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)

        pet = pet_repo.get_pet(pet_id)
        if not pet:
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/dashboard", status_code=303)

        calc_result = None
        error = None
        try:
            req = FeedingCalcRequest(
                weight_kg=pet.weight_kg,
                age_months=pet.age_months,
                activity_level=pet.activity_level,
                is_neutered=pet.is_neutered,
                medical_conditions=pet.medical_conditions,
            )
            calc_result = calculate_daily_calories(req)
        except ValueError as e:
            error = str(e)

        return feeding_page(pet, calc_result, error)

    @app.post("/feeding/{pet_id}/calculate")
    def calculate_feeding(pet_id: str, session):
        if not session.get('user_id'):
            return P("Unauthorized", cls="error")

        pet = pet_repo.get_pet(pet_id)
        if not pet:
            return P("Pet not found", cls="error")

        try:
            req = FeedingCalcRequest(
                weight_kg=pet.weight_kg,
                age_months=pet.age_months,
                activity_level=pet.activity_level,
                is_neutered=pet.is_neutered,
                medical_conditions=pet.medical_conditions,
            )
            result = calculate_daily_calories(req)
        except ValueError as e:
            return P(str(e), cls="error")

        return Div(
            feeding_progress(result.daily_calories),
            Div(
                H3("Calculation Breakdown"),
                P(f"RER (Resting Energy Requirement): {result.rer} kcal"),
                P(f"Activity Multiplier: {result.activity_multiplier}x"),
                P(f"Age Multiplier: {result.age_multiplier}x"),
                P(f"Neutered Multiplier: {result.neutered_multiplier}x"),
                cls="calc-breakdown",
            ),
            cls="calc-result",
        )
