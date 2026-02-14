from fasthtml.common import *
from pydantic import BaseModel

class SessionData(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str

def register_auth_routes(app):
    @app.post("/api/auth/session")
    async def set_session(data: SessionData, session):
        # Store Supabase tokens in server-side session
        session['access_token'] = data.access_token
        session['user_id'] = data.user_id
        return {"status": "success"}

    @app.post("/logout")
    async def logout(session):
        session.clear()
        return RedirectResponse("/", status_code=303)
