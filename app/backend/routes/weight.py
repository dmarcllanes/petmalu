from pydantic import ValidationError

from app.database import weight_repo
from app.models.weight_models import WeightLogCreate


def register_weight_routes(app):

    @app.post("/weight/{pet_id}")
    def log_weight(pet_id: str, weight_kg: str, session):
        if not session.get('user_id'):
            from fasthtml.common import RedirectResponse
            return RedirectResponse("/login", status_code=303)
        try:
            data = WeightLogCreate(pet_id=pet_id, weight_kg=float(weight_kg))
        except (ValidationError, ValueError):
            from fasthtml.common import RedirectResponse
            return RedirectResponse(f"/feeding/{pet_id}", status_code=303)

        weight_repo.create_weight_log(data)
        from fasthtml.common import RedirectResponse
        return RedirectResponse(f"/feeding/{pet_id}", status_code=303)
