from pydantic import ValidationError

from app.database import pet_repo, weight_repo
from app.models.pet_models import PetCreate, PetUpdate
from app.backend.core.constants import FREE_PET_LIMIT
from app.backend.services.calorie_engine import calculate_daily_calories
from app.backend.services.weight_analyzer import analyze_trend
from app.models.feeding_models import FeedingCalcRequest
from app.frontend.pages.dashboard import dashboard_page
from app.frontend.pages.pet_profile import (
    pet_form_page, pet_detail_page, wizard_page,
    wizard_step_1_content, wizard_step_2_content, wizard_step_3_content,
)


def register_pet_routes(app):

    @app.get("/dashboard")
    def home(session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)

        pets = pet_repo.get_all_pets()
        calorie_map: dict[str, float] = {}
        for p in pets:
            try:
                req = FeedingCalcRequest(
                    weight_kg=p.weight_kg,
                    age_months=p.age_months,
                    activity_level=p.activity_level,
                    is_neutered=p.is_neutered,
                    medical_conditions=p.medical_conditions,
                )
                result = calculate_daily_calories(req)
                calorie_map[p.id] = result.daily_calories
            except ValueError:
                pass
        return dashboard_page(pets, calorie_map)

    @app.get("/pets/new")
    def new_pet_form(session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        return wizard_page()

    # --- Wizard step endpoints ---

    @app.post("/pets/wizard/step/1")
    def wizard_back_to_step_1(
        name: str = "", species: str = "dog", breed: str = "",
        weight_kg: str = "", age_months: str = "", is_neutered: str = "",
        activity_level: str = "",
    ):
        data = dict(
            name=name, species=species, breed=breed,
            weight_kg=weight_kg, age_months=age_months,
            is_neutered=is_neutered, activity_level=activity_level,
        )
        return wizard_step_1_content(data)

    @app.post("/pets/wizard/step/2")
    def wizard_to_step_2(
        name: str = "", species: str = "dog", breed: str = "",
        weight_kg: str = "", age_months: str = "", is_neutered: str = "",
        activity_level: str = "",
    ):
        data = dict(
            name=name, species=species, breed=breed,
            weight_kg=weight_kg, age_months=age_months,
            is_neutered=is_neutered, activity_level=activity_level,
        )
        # Validate step 1 fields
        if not name.strip():
            return wizard_step_1_content(data, error="Name is required.")
        return wizard_step_2_content(data)

    @app.post("/pets/wizard/step/3")
    def wizard_to_step_3(
        name: str = "", species: str = "dog", breed: str = "",
        weight_kg: str = "", age_months: str = "", is_neutered: str = "",
        activity_level: str = "",
    ):
        data = dict(
            name=name, species=species, breed=breed,
            weight_kg=weight_kg, age_months=age_months,
            is_neutered=is_neutered, activity_level=activity_level,
        )
        # Validate step 2 fields
        if not weight_kg:
            return wizard_step_2_content(data, error="Weight is required.")
        try:
            w = float(weight_kg)
            if w <= 0:
                raise ValueError
        except ValueError:
            return wizard_step_2_content(data, error="Weight must be a positive number.")

        if not age_months:
            return wizard_step_2_content(data, error="Age is required.")
        try:
            a = int(age_months)
            if a < 0:
                raise ValueError
        except ValueError:
            return wizard_step_2_content(data, error="Age must be a non-negative whole number.")

        return wizard_step_3_content(data)

    # --- End wizard endpoints ---

    @app.post("/pets/new")
    def create_pet(name: str, species: str, breed: str, weight_kg: str,
                   age_months: str, activity_level: str, is_neutered: str = ""):
        if pet_repo.count_pets() >= FREE_PET_LIMIT:
            return wizard_page(
                step=1,
                error=f"Free tier limited to {FREE_PET_LIMIT} pet(s). Delete existing pet first.",
            )

        try:
            data = PetCreate(
                name=name,
                species=species,
                breed=breed or None,
                weight_kg=float(weight_kg),
                age_months=int(age_months),
                activity_level=activity_level,
                is_neutered=is_neutered == "true",
            )
        except (ValidationError, ValueError) as e:
            return wizard_page(
                step=3,
                data=dict(
                    name=name, species=species, breed=breed,
                    weight_kg=weight_kg, age_months=age_months,
                    activity_level=activity_level, is_neutered=is_neutered,
                ),
                error=str(e),
            )

        pet_repo.create_pet(data)
        from fasthtml.common import RedirectResponse
        return RedirectResponse("/", status_code=303)

    @app.get("/pets/{pet_id}")
    def get_pet(pet_id: str, session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        pet = pet_repo.get_pet(pet_id)
        if not pet:
            return dashboard_page(pet_repo.get_all_pets())

        daily_cal = None
        try:
            req = FeedingCalcRequest(
                weight_kg=pet.weight_kg,
                age_months=pet.age_months,
                activity_level=pet.activity_level,
                is_neutered=pet.is_neutered,
                medical_conditions=pet.medical_conditions,
            )
            daily_cal = calculate_daily_calories(req).daily_calories
        except ValueError:
            pass

        logs = weight_repo.get_weight_logs(pet_id)
        trend = analyze_trend(logs)
        return pet_detail_page(pet, daily_cal, logs, trend)

    @app.get("/pets/{pet_id}/edit")
    def edit_pet_form(pet_id: str, session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        pet = pet_repo.get_pet(pet_id)
        if not pet:
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        return pet_form_page(pet)

    @app.post("/pets/{pet_id}/edit")
    def update_pet(pet_id: str, name: str, species: str, breed: str,
                   weight_kg: str, age_months: str, activity_level: str,
                   session, is_neutered: str = ""):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        try:
            data = PetUpdate(
                name=name,
                species=species,
                breed=breed or None,
                weight_kg=float(weight_kg),
                age_months=int(age_months),
                activity_level=activity_level,
                is_neutered=is_neutered == "true",
            )
        except (ValidationError, ValueError) as e:
            pet = pet_repo.get_pet(pet_id)
            return pet_form_page(pet, error=str(e))

        pet_repo.update_pet(pet_id, data)
        from fasthtml.common import RedirectResponse
        return RedirectResponse(f"/pets/{pet_id}", status_code=303)

    @app.post("/pets/{pet_id}/delete")
    def delete_pet(pet_id: str, session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        pet_repo.delete_pet(pet_id)
        from fasthtml.common import RedirectResponse
        return RedirectResponse("/", status_code=303)
