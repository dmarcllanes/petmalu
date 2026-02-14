from fasthtml.common import *
from pydantic import BaseModel, ValidationError

# Database & Models
from app.database import pet_repo, weight_repo, user_repo
from app.models.pet_models import PetCreate, PetUpdate
from app.models.feeding_models import FeedingCalcRequest
from app.models.weight_models import WeightLogCreate

# Services
from app.backend.core.constants import FREE_PET_LIMIT
from app.backend.services.calorie_engine import calculate_daily_calories
from app.backend.services.weight_analyzer import analyze_trend

# Frontend Pages
from app.frontend.pages.homepage import home_page
from app.frontend.pages.login import login_page
from app.frontend.pages.dashboard import dashboard_page
from app.frontend.pages.pet_profile import (
    pet_form_page, pet_detail_page, wizard_page,
    wizard_step_1_content, wizard_step_2_content, wizard_step_3_content,
)
from app.frontend.pages.feeding import feeding_page
from app.frontend.components.feeding_progress import feeding_progress

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app, rt = fast_app(
    static_path="static",
    pico=False,
    hdrs=[
        Meta(name="viewport", content="width=device-width, initial-scale=1, viewport-fit=cover"),
        Meta(name="theme-color", content="#2F7A73"),
        Meta(name="apple-mobile-web-app-capable", content="yes"),
        Meta(name="apple-mobile-web-app-status-bar-style", content="black-translucent"),
        Meta(name="apple-mobile-web-app-title", content="LuluPet"),
        Link(rel="manifest", href="/manifest.json"),
        Link(rel="apple-touch-icon", href="/icons/icon-192.png"),
        Link(rel="stylesheet", href="/styles.css"),
        Script("""
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/sw.js');
            }
        """),
    ],
)

# ============================================================================
# MODELS
# ============================================================================

class SessionData(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    full_name: str | None = None

# ============================================================================
# FRONTEND PAGES
# ============================================================================

@rt("/")
def home():
    """Marketing homepage"""
    return home_page()

@rt("/login")
def login():
    """Login page with Google Auth"""
    return login_page()

@rt("/manifest.json")
def manifest():
    """Serve PWA manifest"""
    return FileResponse("static/manifest.json", media_type="application/json")

@rt("/dashboard")
def dashboard(session):
    """Pet dashboard - protected route"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    
    user_id = session['user_id']
    pets = pet_repo.get_all_pets(user_id)
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

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@rt("/api/auth/session", methods=["POST"])
async def set_session(data: SessionData, session):
    """Sync Supabase session with server-side session and create/update user in database"""
    # Create or update user in database
    user_repo.get_or_create_user(
        user_id=data.user_id,
        email=data.email,
        full_name=data.full_name
    )
    
    # Store in server session
    session['access_token'] = data.access_token
    session['user_id'] = data.user_id
    return {"status": "success"}

@rt("/logout", methods=["POST"])
async def logout(session):
    """Clear session and redirect to login"""
    session.clear()
    return RedirectResponse("/login", status_code=303)

# ============================================================================
# PET MANAGEMENT ROUTES
# ============================================================================

@rt("/pets/new")
def new_pet_form(session):
    """New pet wizard form - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    return wizard_page()

@rt("/pets/wizard/step/1", methods=["POST"])
def wizard_back_to_step_1(
    name: str = "", species: str = "dog", breed: str = "",
    weight_kg: str = "", age_months: str = "", is_neutered: str = "",
    activity_level: str = "",
):
    """Return to wizard step 1"""
    data = dict(
        name=name, species=species, breed=breed,
        weight_kg=weight_kg, age_months=age_months,
        is_neutered=is_neutered, activity_level=activity_level,
    )
    return wizard_step_1_content(data)

@rt("/pets/wizard/step/2", methods=["POST"])
def wizard_to_step_2(
    name: str = "", species: str = "dog", breed: str = "",
    weight_kg: str = "", age_months: str = "", is_neutered: str = "",
    activity_level: str = "",
):
    """Advance to wizard step 2"""
    data = dict(
        name=name, species=species, breed=breed,
        weight_kg=weight_kg, age_months=age_months,
        is_neutered=is_neutered, activity_level=activity_level,
    )
    # Validate step 1 fields
    if not name.strip():
        return wizard_step_1_content(data, error="Name is required.")
    return wizard_step_2_content(data)

@rt("/pets/wizard/step/3", methods=["POST"])
def wizard_to_step_3(
    name: str = "", species: str = "dog", breed: str = "",
    weight_kg: str = "", age_months: str = "", is_neutered: str = "",
    activity_level: str = "",
):
    """Advance to wizard step 3"""
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

@rt("/pets/new", methods=["POST"])
def create_pet(name: str, species: str, breed: str, weight_kg: str,
               age_months: str, activity_level: str, session, is_neutered: str = ""):
    """Submit new pet"""
    user_id = session.get('user_id')
    if pet_repo.count_pets(user_id) >= FREE_PET_LIMIT:
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

    user_id = session.get('user_id')
    pet_repo.create_pet(data, user_id)
    return RedirectResponse("/dashboard", status_code=303)

@rt("/pets/{pet_id}")
def get_pet(pet_id: str, session):
    """View pet profile - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    
    user_id = session.get('user_id')
    pet = pet_repo.get_pet(pet_id, user_id)
    if not pet:
        return dashboard_page(pet_repo.get_all_pets(user_id))

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

@rt("/pets/{pet_id}/edit")
def edit_pet_form(pet_id: str, session):
    """Edit pet form - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    
    user_id = session.get('user_id')
    pet = pet_repo.get_pet(pet_id, user_id)
    if not pet:
        return RedirectResponse("/login", status_code=303)
    return pet_form_page(pet)

@rt("/pets/{pet_id}/edit", methods=["POST"])
def update_pet(pet_id: str, name: str, species: str, breed: str,
               weight_kg: str, age_months: str, activity_level: str,
               session, is_neutered: str = ""):
    """Submit pet updates - protected"""
    if not session.get('user_id'):
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
        user_id = session.get('user_id')
        pet = pet_repo.get_pet(pet_id, user_id)
        return pet_form_page(pet, error=str(e))

    user_id = session.get('user_id')
    pet_repo.update_pet(pet_id, data, user_id)
    return RedirectResponse(f"/pets/{pet_id}", status_code=303)

@rt("/pets/{pet_id}/delete", methods=["POST"])
def delete_pet(pet_id: str, session):
    """Delete pet - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    
    user_id = session.get('user_id')
    pet_repo.delete_pet(pet_id, user_id)
    return RedirectResponse("/dashboard", status_code=303)

# ============================================================================
# FEEDING & CALORIE ROUTES
# ============================================================================

@rt("/feeding/{pet_id}")
def feeding_view(pet_id: str, session):
    """Feeding page with calorie calculator - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)

    user_id = session.get('user_id')
    pet = pet_repo.get_pet(pet_id, user_id)
    if not pet:
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

@rt("/feeding/{pet_id}/calculate", methods=["POST"])
def calculate_feeding(pet_id: str, session):
    """Calculate daily calories - HTMX endpoint - protected"""
    if not session.get('user_id'):
        return P("Unauthorized", cls="error")

    user_id = session.get('user_id')
    pet = pet_repo.get_pet(pet_id, user_id)
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

# ============================================================================
# WEIGHT TRACKING ROUTES
# ============================================================================

@rt("/weight/{pet_id}", methods=["POST"])
def log_weight(pet_id: str, weight_kg: str, session):
    """Log weight entry - protected"""
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)
    
    try:
        data = WeightLogCreate(pet_id=pet_id, weight_kg=float(weight_kg))
    except (ValidationError, ValueError):
        return RedirectResponse(f"/feeding/{pet_id}", status_code=303)

    weight_repo.create_weight_log(data)
    return RedirectResponse(f"/feeding/{pet_id}", status_code=303)
